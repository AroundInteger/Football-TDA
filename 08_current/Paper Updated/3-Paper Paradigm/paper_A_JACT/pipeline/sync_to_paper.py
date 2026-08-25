#!/usr/bin/env python3
"""Validate Paper A LaTeX numbers against pipeline/outputs/numbers.json."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parent
PAPER_DIR = PIPELINE_DIR.parent
NUMBERS_PATH = PIPELINE_DIR / "outputs" / "numbers.json"
MAIN_TEX = PAPER_DIR / "main.tex"


def extract_abstract(tex: str) -> str:
    match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S)
    return match.group(1) if match else ""


def main() -> None:
    if not NUMBERS_PATH.exists():
        print(f"ERROR: {NUMBERS_PATH} not found. Run pipeline first.")
        sys.exit(1)
    with open(NUMBERS_PATH) as f:
        data = json.load(f)
    h = data.get("headline", {})
    regimes = data.get("regimes", {})
    fig = data.get("figure_cycle_geometry", {})
    comp = data.get("complementarity", {})
    linkage = data.get("linkage", {}).get("tactical_h1_total", {})

    tex_files = list((PAPER_DIR / "sections").glob("*.tex")) + [MAIN_TEX]
    tex = "\n".join(p.read_text() for p in tex_files if p.exists())
    main_tex = MAIN_TEX.read_text() if MAIN_TEX.exists() else ""
    abstract = extract_abstract(main_tex)

    print("=== sync_to_paper: Paper A ===")
    ok = True
    rho = round(h.get("spearman_rho", 0), 3)
    n_frames = comp.get("n_frames")
    ind_idx = fig.get("individual_frame_idx")
    tac_idx = fig.get("tactical_frame_idx")

    # Bottleneck tail: the tex quotes the 95th percentile, so the value is read
    # back from the backing file rather than hard-coded. If a re-run of
    # tda_native_distances.py drops the p95 key, this fails loudly instead of
    # leaving an unbacked number in the manuscript (ruling R14).
    bneck = data.get("tda_native", {}).get("bottleneck", {})
    bneck_p95 = bneck.get("p95")
    bneck_median = bneck.get("median")
    checks = [
        ("primary_ind_presence", h.get("primary_h1_individual_presence_pct"), r"143/150 \(95\.3"),
        ("primary_tac_presence", h.get("primary_h1_tactical_presence_pct"), r"19/150 \(12\.7"),
        ("multi_ind_presence", h.get("multi_h1_individual_presence_pct"), r"97\.0"),
        ("spearman_rho", rho, r"\\rho=0\.264"),
        ("stability_individual", h.get("stability_individual"), r"0\.875"),
        ("stability_tactical", h.get("stability_tactical"), r"0\.836"),
        ("event_pairs", h.get("event_topology_pairs"), r"104\{,}722"),
        ("ripser_version", "0.6.12", r"Ripser\.py~0\.6\.12"),
        ("numpy_version", "2.0.2", r"NumPy~2\.0\.2"),
        ("scipy_version", "1.13.1", r"SciPy~1\.13\.1"),
        ("zenodo_community", True, r"Swansea University Zenodo community"),
        ("complementarity_n_frames", n_frames, r"1\{,\}500 uniformly sampled frames"),
        ("figure_ind_frame", ind_idx, rf"sample frame~{ind_idx}"),
        ("figure_tac_frame", tac_idx, rf"sample frame~{tac_idx}"),
        ("ch_optimum", 1.39, r"1\.39"),
        ("null_tactical_excess", True, r"\$\+11\.0\$"),
        ("null_individual_excess", True, r"\$\+5\.8\$"),
        (
            "bottleneck_p95",
            bneck_p95,
            rf"{bneck_p95:.3f}~m" if bneck_p95 is not None else None,
        ),
        (
            "bottleneck_median",
            bneck_median,
            rf"{bneck_median:.3f}~m" if bneck_median is not None else None,
        ),
        ("linkage_single", linkage.get("single"), r"153 tactical"),
        ("linkage_complete", linkage.get("complete"), r"923 for complete"),
        ("linkage_ward", linkage.get("ward"), r"936 for Ward"),
    ]
    for name, expected, pattern in checks:
        if expected is None:
            print(f"  SKIP {name}")
            continue
        if not re.search(pattern, tex):
            print(f"  FAIL {name}: pattern not found ({pattern})")
            ok = False
        else:
            print(f"  OK {name}")

    print("--- stale / forbidden ---")
    forbidden = [
        ("no_stale_900_frames", r"900 frames"),
        ("no_stale_frame_28", r"frame~28"),
        ("no_stale_frame_35", r"frame~35"),
        # 1.511 is now backed by outputs/complementarity/tda_native_distances_summary.json
        # (ruling R14). What must not reappear is 7.994, which is the maximum and was
        # previously quoted as if it were the 95th percentile.
        ("no_bottleneck_max_as_p95", r"7\.994"),
        ("no_dockerfile", r"[Dd]ockerfile"),
        ("no_github_archive", r"github\.com/AroundInteger"),
        ("no_stale_ripser", r"0\.6\.4"),
        ("no_stale_numpy", r"NumPy~1\.26"),
        ("no_epsrc_placeholder", r"EPSRC grant reference"),
        ("no_fake_zenodo_doi", r"zenodo\.XXXXXXX"),
        ("no_grant_only", r"grant-only"),
    ]
    for name, pattern in forbidden:
        if re.search(pattern, tex):
            print(f"  FAIL {name}: forbidden pattern found ({pattern})")
            ok = False
        else:
            print(f"  OK {name}")

    print("--- abstract checks ---")
    abstract_checks = [
        ("abstract_spearman_rho", r"\\rho=0\.264", False),
        ("abstract_no_stale_rho", r"\\rho=0\.254", True),
        ("abstract_no_stale_persistence", r"2\.693", True),
        ("abstract_1500_frames", r"1\{,\}500 sampled frames", False),
    ]
    for name, pattern, is_forbidden in abstract_checks:
        if not abstract:
            print(f"  FAIL {name}: abstract not found in main.tex")
            ok = False
            continue
        found = bool(re.search(pattern, abstract))
        if is_forbidden:
            if found:
                print(f"  FAIL {name}: stale value found in abstract")
                ok = False
            else:
                print(f"  OK {name}")
        else:
            if not found:
                print(f"  FAIL {name}: pattern not found in abstract ({pattern})")
                ok = False
            else:
                print(f"  OK {name}")

    if ok:
        print("\nPASS: headline patterns found in manuscript.")
        sys.exit(0)
    print("\nFAIL: update tex or re-run pipeline.")
    sys.exit(1)


if __name__ == "__main__":
    main()
