#!/usr/bin/env python3
"""Step 09: autocorrelation of topological summaries on the primary match.

Computes frame-level H0 and total H1 persistence at 1 Hz (every 10th complete
frame) and plots ACF against lag in seconds. This is a supplement: it supports
the uniform_150 stride (~29 s) without becoming the operational sampling rule.

Event association remains on the full-rate stream (step 05).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import FIGURES_DIR, OUTPUT_DIR, ensure_dirs, load_config, repo_root  # noqa: E402

REPO = repo_root()
sys.path.insert(0, str(REPO / "03_football_analysis" / "AvailableData"))
sys.path.insert(0, str(REPO / "02_tda_core"))

from primary_match_skillcorner_analysis import (  # noqa: E402
    ensure_match_assets,
    load_tracking_data,
    h1_at_cutoff,
    VALIDATED_CUTOFFS,
    FPS,
)
from tda_utils import persistence_stats  # noqa: E402


def acf_biased(x: np.ndarray, max_lag: int) -> np.ndarray:
    """Pearson autocorrelation at lags 0..max_lag (NaNs skipped)."""
    x = np.asarray(x, dtype=float)
    x = x - np.nanmean(x)
    out = np.full(max_lag + 1, np.nan)
    var = np.nanvar(x)
    if not np.isfinite(var) or var == 0:
        return out
    for k in range(max_lag + 1):
        if k == 0:
            out[k] = 1.0
            continue
        a, b = x[:-k], x[k:]
        mask = np.isfinite(a) & np.isfinite(b)
        if mask.sum() < 20:
            continue
        out[k] = float(np.corrcoef(a[mask], b[mask])[0, 1])
    return out


def first_lag_below(acf: np.ndarray, dt: float, thresh: float = 0.1) -> float | None:
    for k, v in enumerate(acf):
        if k == 0 or not np.isfinite(v):
            continue
        if abs(v) < thresh:
            return k * dt
    return None


def main() -> None:
    ensure_dirs()
    cfg = load_config()
    decimate = int(cfg["sampling"]["acf_supplement"]["decimate"])
    max_lag_s = float(cfg["sampling"]["acf_supplement"]["max_lag_s"])
    n_uniform = int(cfg["sampling"]["uniform_150"]["n_frames"])

    try:
        ensure_match_assets()
        frames, home, away = load_tracking_data(require_complete=True)
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"ACF supplement skipped (tracking data unavailable): {exc}")
        return
    series_frames = frames[::decimate]
    dt = decimate / FPS
    max_lag = int(round(max_lag_s / dt))
    uniform_step = max(1, len(frames) // n_uniform)
    uniform_s = uniform_step / FPS

    print(
        f"ACF series: {len(series_frames)} frames at ~{1 / dt:.2f} Hz "
        f"from {len(frames)} complete frames; max lag {max_lag_s:.0f} s"
    )

    records = {name: [] for name in (
        "h0_individual", "h0_tactical",
        "h1_pers_individual", "h1_pers_tactical",
    )}
    for i, frame in enumerate(series_frames):
        pos = frame["positions"]
        for scale in ("individual", "tactical"):
            h0_d, h1_d, _, _ = h1_at_cutoff(pos, VALIDATED_CUTOFFS[scale])
            records[f"h0_{scale}"].append(len(h0_d))
            records[f"h1_pers_{scale}"].append(
                persistence_stats(h1_d)["total"] if h1_d is not None else 0.0
            )
        if (i + 1) % 250 == 0:
            print(f"  {i + 1}/{len(series_frames)}", flush=True)

    lags_s = np.arange(max_lag + 1) * dt
    series_acf = {k: acf_biased(np.array(v), max_lag) for k, v in records.items()}

    labels = {
        "h0_individual": r"$H_0$ individual",
        "h0_tactical": r"$H_0$ tactical",
        "h1_pers_individual": r"total $H_1$ persistence, individual",
        "h1_pers_tactical": r"total $H_1$ persistence, tactical",
    }
    # Three series for the panel: drop individual H0 (near-saturated, slow)
    plot_keys = ("h0_tactical", "h1_pers_individual", "h1_pers_tactical")

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    colours = ("#1565C0", "#E65100", "#6A1B9A")
    for key, col in zip(plot_keys, colours):
        ax.plot(lags_s, series_acf[key], color=col, lw=1.6, label=labels[key])
    ax.axhline(0.0, color="#9E9E9E", lw=0.8)
    ax.axhline(0.1, color="#BDBDBD", lw=0.7, ls="--")
    ax.axvline(10, color="#757575", lw=0.8, ls=":")
    ax.axvline(20, color="#757575", lw=0.8, ls=":")
    ax.axvline(uniform_s, color="#C62828", lw=1.1, ls="--",
               label=rf"uniform\_150 stride ({uniform_s:.0f} s)")
    ax.set_xlim(0, max_lag_s)
    ax.set_ylim(-0.15, 1.05)
    ax.set_xlabel("lag (s)")
    ax.set_ylabel("autocorrelation")
    ax.set_title(f"Topological summaries, {home} vs {away} (1 Hz)")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()

    out_dir = OUTPUT_DIR / "acf_supplement"
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = FIGURES_DIR / "figS1_acf.pdf"
    png = FIGURES_DIR / "figS1_acf.png"
    fig.savefig(pdf, bbox_inches="tight")
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)

    summary = {
        "n_complete": len(frames),
        "n_series": len(series_frames),
        "dt_s": dt,
        "uniform_150_stride_frames": uniform_step,
        "uniform_150_stride_s": uniform_s,
        "first_lag_acf_abs_lt_0.1_s": {
            k: first_lag_below(series_acf[k], dt) for k in plot_keys
        },
        "acf_at_10s": {k: float(series_acf[k][int(round(10 / dt))]) for k in plot_keys},
        "acf_at_20s": {k: float(series_acf[k][int(round(20 / dt))]) for k in plot_keys},
        "acf_at_uniform_stride": {
            k: float(series_acf[k][min(int(round(uniform_s / dt)), max_lag)])
            for k in plot_keys
        },
    }
    with open(out_dir / "acf_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {pdf}")
    print(json.dumps(summary["first_lag_acf_abs_lt_0.1_s"], indent=2))


if __name__ == "__main__":
    main()
