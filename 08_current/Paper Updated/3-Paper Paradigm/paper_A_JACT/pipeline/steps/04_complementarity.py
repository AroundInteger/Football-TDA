#!/usr/bin/env python3
"""Step 04: complementarity, bootstrap CIs, TDA-native distances."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, spearmanr

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, ensure_dirs, load_config, repo_root  # noqa: E402

REPO = repo_root()


def complementarity_from_per_frame(per_frame: pd.DataFrame) -> dict:
    """Frame-level complementarity from long-format multi_match CSV."""
    ind = per_frame[per_frame["scale"] == "individual"].copy()
    tac = per_frame[per_frame["scale"] == "tactical"].copy()
    keys = ["match_id", "frame_idx"]
    merged = ind.merge(
        tac,
        on=keys,
        suffixes=("_ind", "_tac"),
    )
    # Headline statistic is total persistence, not loop count. The counts
    # version is reported alongside as a robustness check; both appear in
    # results.tex, so both must be traceable to this file.
    rho, p_rho = spearmanr(
        merged["h1_total_persistence_ind"],
        merged["h1_total_persistence_tac"],
        nan_policy="omit",
    )
    rho_counts, p_rho_counts = spearmanr(
        merged["h1_ind"],
        merged["h1_tac"],
        nan_policy="omit",
    )

    ind_bin = (merged["h1_ind"] > 0).astype(int)
    tac_bin = (merged["h1_tac"] > 0).astype(int)
    a = int(((ind_bin == 1) & (tac_bin == 1)).sum())
    b = int(((ind_bin == 1) & (tac_bin == 0)).sum())
    c = int(((ind_bin == 0) & (tac_bin == 1)).sum())
    d = int(((ind_bin == 0) & (tac_bin == 0)).sum())
    or_val, p_fisher = fisher_exact([[a, b], [c, d]])

    return {
        "n_frames": int(len(merged)),
        "spearman_statistic": "h1_total_persistence",
        "spearman_rho": float(rho),
        "spearman_p": float(p_rho),
        "spearman_rho_counts": float(rho_counts),
        "spearman_p_counts": float(p_rho_counts),
        "fisher_statistic": "h1_presence (h1 > 0)",
        "fisher_odds_ratio": float(or_val),
        "fisher_p": float(p_fisher),
        "contingency": [[a, b], [c, d]],
    }


def run_bootstrap(cfg: dict) -> None:
    sys.path.insert(0, str(REPO / "03_football_analysis" / "paper_v5_revisions"))
    import bootstrap_multi_match_ci as boot  # noqa: E402

    data_dir = OUTPUT_DIR
    boot.DATA_DIR = data_dir
    boot.OUT_DIR = OUTPUT_DIR / "complementarity"
    boot.OUT_DIR.mkdir(parents=True, exist_ok=True)

    sys.argv = [
        "bootstrap_multi_match_ci.py",
        "--n-boot",
        str(cfg["bootstrap"]["n_boot"]),
        "--seed",
        str(cfg["bootstrap"]["seed"]),
    ]
    boot.main()


def run_tda_native() -> None:
    sys.path.insert(0, str(REPO / "01_data"))
    sys.path.insert(0, str(REPO / "02_tda_core"))
    sys.path.insert(0, str(REPO / "03_football_analysis" / "paper_v5_revisions"))
    import tda_native_distances as tda  # noqa: E402

    tda.OUT_DIR = OUTPUT_DIR / "complementarity"
    tda.OUT_DIR.mkdir(parents=True, exist_ok=True)
    sys.argv = ["tda_native_distances.py", "--skillcorner-only"]
    tda.main()


if __name__ == "__main__":
    ensure_dirs()
    cfg = load_config()
    comp_dir = OUTPUT_DIR / "complementarity"
    comp_dir.mkdir(parents=True, exist_ok=True)

    per_frame_path = OUTPUT_DIR / "multi_match" / "per_frame_results.csv"
    if not per_frame_path.exists():
        raise FileNotFoundError(f"Missing {per_frame_path}; run step 03 first.")

    per_frame = pd.read_csv(per_frame_path)
    comp = complementarity_from_per_frame(per_frame)

    summary = {"complementarity": comp}
    with open(comp_dir / "complementarity_tests.json", "w") as f:
        json.dump(summary, f, indent=2)

    run_bootstrap(cfg)
    if __import__("os").environ.get("RUN_TDA_NATIVE", "").lower() in ("1", "true", "yes"):
        try:
            run_tda_native()
        except Exception as exc:
            print(f"WARNING: tda_native_distances skipped: {exc}")
    else:
        print("Skipping tda_native_distances (set RUN_TDA_NATIVE=1 to enable).")

    # Merge TDA-native summary into complementarity_tests.json
    tda_summary_path = comp_dir / "tda_native_distances_summary.json"
    if tda_summary_path.exists():
        with open(tda_summary_path) as f:
            tda_summary = json.load(f)
        summary["tda_native"] = tda_summary
        with open(comp_dir / "complementarity_tests.json", "w") as f:
            json.dump(summary, f, indent=2)

    print(json.dumps(comp, indent=2))
