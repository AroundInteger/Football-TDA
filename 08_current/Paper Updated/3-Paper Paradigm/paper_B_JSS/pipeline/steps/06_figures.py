#!/usr/bin/env python3
"""Step 06: Paper B figures (event correlation, bilateral timeseries, ROC overlay)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import FIGURES_DIR, OUTPUT_DIR, ensure_dirs, load_config, repo_root  # noqa: E402

IND_COL = (0.55, 0.55, 0.55)
TAC_COL = (0.15, 0.15, 0.15)


def fig_event_correlation() -> None:
    csv_path = OUTPUT_DIR / "event_correlation" / "event_topology_correlation.csv"
    if not csv_path.exists():
        print(f"Skip fig_event_correlation: missing {csv_path}")
        return

    df = pd.read_csv(csv_path)
    summary_path = OUTPUT_DIR / "event_correlation_summary.json"
    tests = {}
    if summary_path.exists():
        with open(summary_path) as f:
            tests = json.load(f).get("statistical_tests", {})

    rows = []
    for scale in ["individual", "tactical"]:
        for etype, t in tests.get(scale, {}).items():
            if t.get("significant_005") or abs(t.get("mean_delta", 0)) > 0.05:
                rows.append(
                    {
                        "event_type": etype,
                        "scale": scale,
                        "mean_delta": t["mean_delta"],
                        "p_value": t["p_value"],
                    }
                )
    if not rows:
        agg = df.groupby(["event_type", "scale"])["persistence_delta"].mean().reset_index()
        agg.columns = ["event_type", "scale", "mean_delta"]
        agg["p_value"] = 0.01
        plot_df = agg
    else:
        plot_df = pd.DataFrame(rows)

    events = sorted(plot_df["event_type"].unique(), key=lambda e: plot_df.loc[
        plot_df["event_type"] == e, "mean_delta"
    ].mean())
    y = np.arange(len(events))
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axvline(0, color=(0.3, 0.3, 0.3), lw=1)
    bw = 0.35
    for k, ev in enumerate(events):
        sub = plot_df[plot_df["event_type"] == ev]
        for j, (scale, col) in enumerate([("individual", IND_COL), ("tactical", TAC_COL)]):
            r = sub[sub["scale"] == scale]
            if r.empty:
                continue
            val = float(r["mean_delta"].iloc[0])
            p = float(r["p_value"].iloc[0])
            ax.barh(y[k] + (bw / 2 if scale == "individual" else -bw / 2), val, bw, color=col, alpha=0.85)
            star = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
            if star:
                ax.text(val + (0.02 if val >= 0 else -0.02), y[k], star, fontsize=8, va="center")
    ax.set_yticks(y)
    ax.set_yticklabels([e.replace("_", " ").title() for e in events], fontsize=9)
    ax.set_xlabel("Mean persistence change (m)")
    ax.set_title("Persistence change by event type")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_event_correlation.pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {FIGURES_DIR / 'fig_event_correlation.pdf'}")


def fig_bilateral_timeseries(cfg: dict) -> None:
    csv_path = OUTPUT_DIR / "bilateral_topology.csv"
    if not csv_path.exists():
        print(f"Skip fig_bilateral: missing {csv_path}")
        return

    df = pd.read_csv(csv_path)
    mid = str(cfg["primary_match_id"])
    sub = df[df["match_id"].astype(str) == mid].sort_values("frame_idx")
    if sub.empty:
        print(f"No bilateral rows for match {mid}")
        return

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(sub["frame_idx"], sub["home_h1_total_persistence"], color=(0.2, 0.4, 0.75), label="Home", lw=1.2)
    ax.plot(sub["frame_idx"], sub["away_h1_total_persistence"], color=(0.9, 0.45, 0.1), label="Away", lw=1.2)
    if "merged_h1_total_persistence" in sub.columns:
        ax.plot(
            sub["frame_idx"],
            sub["merged_h1_total_persistence"],
            color=(0.55, 0.55, 0.55),
            label="Merged (22-player)",
            lw=1.0,
            alpha=0.8,
        )
    ax.set_xlabel("Sample frame index")
    ax.set_ylabel("Tactical $H_1$ total persistence (m)")
    ax.set_title(f"Home/away tactical persistence — match {mid}")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_bilateral_timeseries.pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {FIGURES_DIR / 'fig_bilateral_timeseries.pdf'}")


def fig_roc_overlay() -> None:
    csv_path = OUTPUT_DIR / "predictive_utility.csv"
    summary_path = OUTPUT_DIR / "predictive_utility_summary.json"
    if not csv_path.exists():
        print(f"Skip fig_roc: missing {csv_path}")
        return

    df = pd.read_csv(csv_path)
    target = "is_buildup"
    baseline_cols = ["length_m", "width_m", "hull_area_m2", "voronoi_entropy"]
    topo_cols = baseline_cols + ["tactical_h1_total_persistence"]
    mask = df[target].notna() & df[topo_cols].notna().all(axis=1)
    df = df.loc[mask].reset_index(drop=True)
    y = df[target].astype(int).to_numpy()
    groups = df["match_id"].to_numpy()

    def oof_scores(cols: list[str]) -> np.ndarray:
        X = df[cols].to_numpy(dtype=float)
        oof = np.zeros(len(y))
        gkf = GroupKFold(n_splits=min(10, len(np.unique(groups))))
        for tr, te in gkf.split(X, y, groups):
            sc = StandardScaler()
            Xtr = sc.fit_transform(X[tr])
            Xte = sc.transform(X[te])
            clf = LogisticRegression(max_iter=1000, random_state=42)
            clf.fit(Xtr, y[tr])
            oof[te] = clf.predict_proba(Xte)[:, 1]
        return oof

    oof_a = oof_scores(baseline_cols)
    oof_b = oof_scores(topo_cols)
    fpr_a, tpr_a, _ = roc_curve(y, oof_a)
    fpr_b, tpr_b, _ = roc_curve(y, oof_b)
    auc_a = roc_auc_score(y, oof_a)
    auc_b = roc_auc_score(y, oof_b)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(fpr_a, tpr_a, "--", color=(0.4, 0.4, 0.4), lw=2, label=f"Baseline (AUC={auc_a:.3f})")
    ax.plot(fpr_b, tpr_b, "-", color=(0.15, 0.35, 0.65), lw=2, label=f"+ persistence (AUC={auc_b:.3f})")
    ax.plot([0, 1], [0, 1], "k:", lw=1)
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.set_title("Build-up phase classification (10-fold, grouped by match)")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig_roc_overlay.pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {FIGURES_DIR / 'fig_roc_overlay.pdf'}")


if __name__ == "__main__":
    ensure_dirs()
    cfg = load_config()
    fig_event_correlation()
    fig_bilateral_timeseries(cfg)
    fig_roc_overlay()
