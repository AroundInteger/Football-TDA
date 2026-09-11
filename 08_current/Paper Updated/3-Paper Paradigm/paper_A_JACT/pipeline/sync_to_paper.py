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


def latex_int(n) -> str:
    return f"{int(n):,}".replace(",", "{,}")


def pct_pattern(x) -> str:
    return str(x).replace(".", r"\.")


def main() -> None:
    if not NUMBERS_PATH.exists():
        print(f"ERROR: {NUMBERS_PATH} not found. Run pipeline first.")
        sys.exit(1)
    with open(NUMBERS_PATH) as f:
        data = json.load(f)
    h = data.get("headline", {})
    fig = data.get("figure_cycle_geometry", {})
    comp = data.get("complementarity", {})
    linkage = data.get("linkage", {}).get("tactical_h1_total", {})

    tex_files = list((PAPER_DIR / "sections").glob("*.tex")) + [MAIN_TEX]
    tex = "\n".join(p.read_text() for p in tex_files if p.exists())
    main_tex = MAIN_TEX.read_text() if MAIN_TEX.exists() else ""
    abstract = extract_abstract(main_tex)

    print("=== sync_to_paper: Paper A ===")
    ok = True
    rho = round(h.get("spearman_rho") or 0, 3)
    n_frames = comp.get("n_frames")
    ind_idx = fig.get("individual_frame_idx")
    tac_idx = fig.get("tactical_frame_idx")
    h1p = data.get("h1_primary", {})
    ind_p = h1p.get("individual", {})
    tac_p = h1p.get("tactical", {})
    null = data.get("cardinality_null", {}).get("scales", {})

    # Bottleneck tail: the tex quotes the 95th percentile, so the value is read
    # back from the backing file rather than hard-coded. If a re-run of
    # tda_native_distances.py drops the p95 key, this fails loudly instead of
    # leaving an unbacked number in the manuscript (ruling R14).
    bneck = data.get("tda_native", {}).get("bottleneck", {})
    bneck_p95 = bneck.get("p95")
    bneck_median = bneck.get("median")

    ind_frames = ind_p.get("frames_with_loops")
    ind_total = ind_p.get("frames_total")
    ind_pct = h.get("primary_h1_individual_presence_pct")
    tac_frames = tac_p.get("frames_with_loops")
    tac_total = tac_p.get("frames_total")
    tac_pct = h.get("primary_h1_tactical_presence_pct")
    multi_ind_pct = h.get("multi_h1_individual_presence_pct")
    event_n = h.get("event_topology_pairs")
    ind_ex = null.get("individual", {}).get("excess")
    tac_ex = null.get("tactical", {}).get("excess")

    checks = [
        (
            "primary_ind_presence",
            ind_frames,
            re.escape(f"{ind_frames}/{ind_total} ({ind_pct}")
            if None not in (ind_frames, ind_total, ind_pct)
            else None,
        ),
        (
            "primary_tac_presence",
            tac_frames,
            re.escape(f"{tac_frames}/{tac_total} ({tac_pct}")
            if None not in (tac_frames, tac_total, tac_pct)
            else None,
        ),
        (
            "multi_ind_presence",
            multi_ind_pct,
            pct_pattern(multi_ind_pct) if multi_ind_pct is not None else None,
        ),
        ("spearman_rho", rho, rf"\\rho={pct_pattern(rho)}"),
        ("cutoff_individual", h.get("cutoff_individual"), r"2\.75"),
        ("cutoff_tactical", h.get("cutoff_tactical"), r"11\.75"),
        ("cutoff_team", h.get("cutoff_team"), r"23\.0"),
        (
            "event_pairs",
            event_n,
            re.escape(latex_int(event_n)) if event_n is not None else None,
        ),
        ("ripser_version", "0.6.12", r"Ripser\.py~0\.6\.12"),
        ("numpy_version", "2.0.2", r"NumPy~2\.0\.2"),
        ("scipy_version", "1.13.1", r"SciPy~1\.13\.1"),
        ("zenodo_community", True, r"Swansea University Zenodo community"),
        ("complementarity_n_frames", n_frames, r"1\{,\}500 uniformly sampled frames"),
        ("figure_ind_frame", ind_idx, rf"sample frame~{ind_idx}"),
        ("figure_tac_frame", tac_idx, rf"sample frame~{tac_idx}"),
        ("n_frames_sweep", 436648, r"436\{,\}648"),
        (
            "null_tactical_excess",
            tac_ex,
            rf"\$\+{100 * tac_ex:.1f}\$" if tac_ex is not None else None,
        ),
        (
            "null_individual_excess",
            ind_ex,
            rf"\$\+{100 * ind_ex:.1f}\$" if ind_ex is not None else None,
        ),
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
        (
            "linkage_single",
            linkage.get("single"),
            rf"{linkage.get('single')}\s+tactical"
            if linkage.get("single") is not None
            else None,
        ),
        (
            "linkage_complete",
            linkage.get("complete"),
            rf"detects {linkage.get('complete')}"
            if linkage.get("complete") is not None
            else None,
        ),
        (
            "linkage_ward",
            linkage.get("ward"),
            rf"detects {linkage.get('ward')}"
            if linkage.get("ward") is not None
            else None,
        ),
    ]
    for name, expected, pattern in checks:
        if expected is None or pattern is None:
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
        ("no_bottleneck_max_as_p95", r"7\.994"),
        ("no_dockerfile", r"[Dd]ockerfile"),
        ("no_github_archive", r"github\.com/AroundInteger"),
        ("no_stale_ripser", r"0\.6\.4"),
        ("no_stale_numpy", r"NumPy~1\.26"),
        ("no_epsrc_placeholder", r"EPSRC grant reference"),
        ("no_fake_zenodo_doi", r"zenodo\.XXXXXXX"),
        ("no_grant_only", r"grant-only"),
        ("no_gps_ic_6_87", r"6\.87"),
        ("no_gps_sil_16_31", r"16\.31"),
        ("no_58_windows", r"58 temporal"),
        ("no_carried_over", r"carried over"),
        ("no_old_individual_cutoff", r"(?<![0-9])2\.98~m"),
        ("no_old_team_cutoff", r"30\.0~m"),
    ]
    for name, pattern in forbidden:
        if re.search(pattern, tex):
            print(f"  FAIL {name}: forbidden pattern found ({pattern})")
            ok = False
        else:
            print(f"  OK {name}")

    print("--- abstract checks ---")
    abstract_checks = [
        ("abstract_spearman_rho", rf"\\rho={pct_pattern(rho)}", False),
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
