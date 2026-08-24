"""
Methods-note experiments: ecology (lead) and robotics generators through
the exact H0 / Wp / W2-Fréchet / Page-CUSUM core.

Usage
    python experiments.py           # verify, figures, Monte Carlo
    python experiments.py --verify  # noise-free reference values only
    python experiments.py --quick   # figures only; does not rewrite numbers.json

Does not import A_WIDE. Gap scales are re-derived from each generator.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.gridspec import GridSpec
from scipy.spatial.distance import pdist, squareform

_HERE = Path(__file__).resolve().parent
_TOY = _HERE.parents[2] / "grant" / "evidence" / "toy_models"
for _p in (_TOY, _HERE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from atda_core import (  # noqa: E402
    betti_at,
    compute_h0,
    coupled_series,
    cusum_path,
    death_gap_scales,
    encirclement_h1,
    first_alarm,
    frechet_mean,
    frechet_variance,
    h1_diagram,
    interpolate_cloud,
    n_components_at_delta,
    run_cusum,
    wasserstein_p,
)
from generators import (  # noqa: E402
    ECO_NOISE,
    ECO_T_END,
    ECO_T_STAR,
    ECO_XLIM,
    ECO_YLIM,
    EVADERS_FILE,
    EVADERS_FUNNEL,
    EVADERS_OPEN,
    PRED_HUNT,
    PRED_RING,
    PREY_COLUMN,
    PREY_DISPERSED,
    PREY_HERDED,
    PURSUERS_CHASE,
    PURSUERS_GATE,
    ROB_NOISE,
    ROB_T_END,
    ROB_T_STAR,
    ROB_XLIM,
    ROB_YLIM,
    ecology_config,
    reference_report,
    robotics_config,
)

# Encirclement H1: PRED_RING bar is [62.46, 90.40]; 45 is a football leftover.
ECO_H1_BIRTH_MAX = 80.0
ECO_DELTA_H1 = 70.0
ECO_DELTA_CONFLATE = 16.0
ROB_DELTA_CONFLATE = 12.0

OUT_DIR = _HERE / "figures"
NUM_PATH = _HERE / "numbers.json"
DPI = 300

CA = np.array([21, 128, 61]) / 255      # prey / evaders
CB = np.array([154, 52, 18]) / 255      # predators
CR = np.array([29, 78, 216]) / 255      # pursuers
CK = np.array([217, 119, 6]) / 255
CGREY = np.array([107, 114, 128]) / 255
CINK = np.array([15, 23, 42]) / 255
H1COL = np.array([5, 150, 105]) / 255

T_MAX = 110
MON0 = 8
WIN = 12
N_MC = 200
N_DEP = 80
HEADLINE_SEED = 7


def _fmt(v):
    return " ".join(f"{x:.2f}" for x in np.asarray(v).ravel())


def vr_edges(pts, delta):
    D = squareform(pdist(pts))
    i, j = np.where(np.triu(D <= delta, k=1))
    if i.size == 0:
        return np.zeros((0, 2, 2))
    return np.stack([pts[i], pts[j]], axis=1)


def scatter_cloud(ax, pts, col, delta=None, s=28, z=5, marker="o"):
    if delta is not None:
        segs = vr_edges(pts, delta)
        if len(segs):
            ax.add_collection(LineCollection(
                segs, colors=[(*col, 0.40)], linewidths=1.15, zorder=z,
            ))
    ax.scatter(pts[:, 0], pts[:, 1], s=s, c=[col], marker=marker,
               edgecolors="white", linewidths=0.35, zorder=z + 1)


def draw_box(ax, xlim, ylim, face, edge, pad=8):
    ax.set_xlim(xlim[0] - pad, xlim[1] + pad)
    ax.set_ylim(ylim[0] - pad, ylim[1] + pad * 1.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(mpatches.Rectangle(
        (xlim[0], ylim[0]), xlim[1] - xlim[0], ylim[1] - ylim[0],
        facecolor=face, edgecolor=edge, linewidth=1.4, zorder=0,
    ))


def panel_label(ax, ch, x=0.02, y=0.97):
    ax.text(x, y, ch, transform=ax.transAxes, fontsize=12, fontweight="bold",
            va="top", ha="left", color=CINK,
            bbox=dict(boxstyle="round,pad=0.12", facecolor="white",
                      edgecolor="none", alpha=0.88))


def draw_h0_barcode(ax, deaths, col, delta=None, max_d=None, ylabel=""):
    d = np.sort(np.asarray(deaths).ravel())
    grey = np.array([214, 219, 226]) / 255
    for k, death in enumerate(d, start=1):
        fc = col if (delta is None or death > delta) else grey
        ax.barh(k, death, height=0.62, color=fc, edgecolor="none", alpha=0.88)
    if delta is not None:
        ax.axvline(delta, color=CK, lw=1.15)
        ax.text(delta, 0.2, rf"$\delta={delta:.0f}$", ha="center", va="top",
                fontsize=8, color=CK)
    ax.set_xlim(0, max_d if max_d is not None else d.max() * 1.12)
    ax.set_ylim(0.2, len(d) + 1.2)
    ax.set_yticks([])
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=8.5, color=CGREY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)


# ---------------------------------------------------------------------------
# Series / CUSUM
# ---------------------------------------------------------------------------

def consecutive_w1(diags):
    w = np.zeros(len(diags))
    for t in range(1, len(diags)):
        w[t] = wasserstein_p(diags[t], diags[t - 1], p=1)
    return w


def prey_jump_series(alpha, noise, seed, t_max=T_MAX, t_star=ECO_T_STAR,
                     t_end=ECO_T_END):
    """Prey H0 diagrams under a jump of size `alpha` toward the herded state."""
    rng = np.random.default_rng(seed)
    diags = []
    for t in range(t_max + 1):
        e = 0.0
        if t >= t_star:
            u = min(1.0, (t - t_star) / max(t_end - t_star, 1))
            e = alpha * u * u * (3.0 - 2.0 * u)
        prey = interpolate_cloud(PREY_DISPERSED, PREY_HERDED, e)
        if noise > 0:
            prey = prey + rng.normal(scale=noise, size=prey.shape)
        diags.append(compute_h0(prey))
    return np.array(diags)


def evader_jump_series(alpha, noise, seed, t_max=T_MAX, t_star=ROB_T_STAR,
                       t_end=ROB_T_END):
    rng = np.random.default_rng(seed)
    diags = []
    for t in range(t_max + 1):
        e = 0.0
        if t >= t_star:
            u = min(1.0, (t - t_star) / max(t_end - t_star, 1))
            e = alpha * u * u * (3.0 - 2.0 * u)
        ev = interpolate_cloud(EVADERS_OPEN, EVADERS_FUNNEL, e)
        if noise > 0:
            ev = ev + rng.normal(scale=noise, size=ev.shape)
        diags.append(compute_h0(ev))
    return np.array(diags)


def calibrate_cusum(null_w, mon0=MON0):
    base = null_w[mon0:]
    mu0 = float(base.mean())
    sig0 = float(base.std(ddof=1))
    kappa = mu0 + 0.5 * sig0
    peaks = []
    for row in null_w if null_w.ndim == 2 else [null_w]:
        C = cusum_path(row, kappa, mon0=mon0)
        peaks.append(float(C.max()))
    h = float(np.quantile(peaks, 0.95))
    return mu0, sig0, kappa, h


def headline_ecology(seed=HEADLINE_SEED):
    rng = np.random.default_rng(seed)
    T = np.arange(T_MAX + 1)
    prey_d, pred_d = [], []
    pers = []
    frechet_var = []
    window = []
    for t in T:
        prey, pred = ecology_config(t, noise=ECO_NOISE, rng=rng)
        dp, dr = compute_h0(prey), compute_h0(pred)
        prey_d.append(dp)
        pred_d.append(dr)
        pers.append(encirclement_h1(pred, birth_max=ECO_H1_BIRTH_MAX))
        window.append(dp)
        if len(window) > WIN:
            window.pop(0)
        if len(window) == WIN:
            mu = frechet_mean(window)
            frechet_var.append(frechet_variance(window, mu=mu, p=2))
        else:
            frechet_var.append(np.nan)
    prey_d = np.array(prey_d)
    w = consecutive_w1(prey_d)
    return {
        "T": T, "w": w, "prey_d": prey_d, "pred_d": np.array(pred_d),
        "pers": np.array(pers), "frechet_var": np.array(frechet_var),
    }


def monte_carlo(series_fn, alphas, jump_w1, n_mc, kappa, h, t_star, label):
    rows = []
    print(f"\n=== Consecutive-frame CUSUM Monte Carlo ({label}, N={n_mc}) ===")
    for a, jw in zip(alphas, jump_w1):
        hits = []
        for s in range(n_mc):
            diags = series_fn(a, ECO_NOISE if "ecol" in label else ROB_NOISE, s)
            w = consecutive_w1(diags)
            that, _ = run_cusum(w, kappa, h, mon0=MON0)
            hits.append(np.nan if that is None else that)
        hits = np.asarray(hits, dtype=float)
        err = np.abs(hits - t_star)
        det = np.isfinite(hits)
        rec = {
            "alpha": float(a),
            "jump_w1": float(jw),
            "mean_abs_err": float(np.nanmean(err)),
            "median_abs_err": float(np.nanmedian(err)),
            "power": float(det.mean()),
        }
        rows.append(rec)
        print(f"  jump W1={jw:7.1f}  E|T-T*|={rec['mean_abs_err']:5.1f}  "
              f"median={rec['median_abs_err']:5.1f}  power={100 * rec['power']:5.1f}%")
    return rows


def prey_ref_w1_series(alpha, noise, seed, t_max=T_MAX, t_star=ECO_T_STAR,
                       t_end=ECO_T_END, ref=None):
    """Persistent statistic xi_t = W1(D_t, D_ref) for T2-lite (not consecutive W1)."""
    if ref is None:
        ref = compute_h0(PREY_DISPERSED)
    rng = np.random.default_rng(seed)
    xi = np.zeros(t_max + 1)
    for t in range(t_max + 1):
        e = 0.0
        if t >= t_star:
            u = min(1.0, (t - t_star) / max(t_end - t_star, 1))
            e = alpha * u * u * (3.0 - 2.0 * u)
        prey = interpolate_cloud(PREY_DISPERSED, PREY_HERDED, e)
        if noise > 0:
            prey = prey + rng.normal(scale=noise, size=prey.shape)
        xi[t] = wasserstein_p(compute_h0(prey), ref, p=1)
    return xi


def interpolant_cusum_delay(alpha, kappa, h, t_star=ECO_T_STAR, t_end=ECO_T_END,
                            t_max=T_MAX, ref=None):
    """Noise-free CUSUM delay along the Euclidean interpolant (smoothstep-aware)."""
    if ref is None:
        ref = compute_h0(PREY_DISPERSED)
    C = 0.0
    for t in range(t_star, t_max + 1):
        if t >= t_end:
            e = alpha
        else:
            u = min(1.0, (t - t_star) / max(t_end - t_star, 1))
            e = alpha * u * u * (3.0 - 2.0 * u)
        prey = interpolate_cloud(PREY_DISPERSED, PREY_HERDED, e)
        xi = wasserstein_p(compute_h0(prey), ref, p=1)
        C = max(0.0, C + xi - kappa)
        if C >= h:
            return t - t_star
    return None


def monte_carlo_ref(alphas, jump_w1, n_mc, kappa, h, t_star, noise):
    """CUSUM on xi_t = W1(D_t, D_ref). Wald plug-in uses this kappa, h."""
    ref = compute_h0(PREY_DISPERSED)
    n_deaths = len(ref)
    rows = []
    print(f"\n=== T2-lite Monte Carlo (W1 to reference, N={n_mc}) ===")
    for a, jw in zip(alphas, jump_w1):
        hits = []
        for s in range(n_mc):
            xi = prey_ref_w1_series(a, noise, 12000 + s, ref=ref)
            that, _ = run_cusum(xi, kappa, h, mon0=MON0)
            hits.append(np.nan if that is None else that)
        hits = np.asarray(hits, dtype=float)
        err = np.abs(hits - t_star)
        det = np.isfinite(hits)
        delta = max(jw - kappa, 1e-9)
        wald = float(h / delta)
        interp = interpolant_cusum_delay(a, kappa, h)
        rec = {
            "alpha": float(a),
            "jump_w1": float(jw),
            "mean_abs_err": float(np.nanmean(err)),
            "median_abs_err": float(np.nanmedian(err)),
            "power": float(det.mean()),
            "wald_h_over_delta": wald,
            "interpolant_delay": None if interp is None else int(interp),
            "delta_plug": float(delta),
            "stability_room": float(2 * n_deaths * noise),
        }
        rows.append(rec)
        print(f"  jump W1={jw:7.1f}  E|T-T*|={rec['mean_abs_err']:5.1f}  "
              f"interpolant={interp}  Wald h/d={wald:5.1f}  "
              f"power={100 * rec['power']:5.1f}%")
    return rows


def t1_lite_sweep(sigmas=(0.8, 1.2, 1.8), n_diag=8, n_restart=5):
    """Death-space W1 vs W2 gap around the ecology dispersed diagram (H2)."""
    from scipy.optimize import minimize

    base = compute_h0(PREY_DISPERSED)
    k = base.size
    rows = []
    print("\n=== T1-lite W1–W2 gap (death-space noise) ===")
    for sigma in sigmas:
        rng = np.random.default_rng(int(1000 * sigma))
        diags = [
            np.sort(np.clip(base + rng.normal(scale=sigma, size=k), 0.0, None))
            for _ in range(n_diag)
        ]
        mu2 = frechet_mean(diags)

        def obj(mu):
            mu = np.sort(np.clip(np.asarray(mu, dtype=float), 0.0, None))
            return float(np.mean([wasserstein_p(d, mu, p=1) ** 2 for d in diags]))

        best = None
        bounds = [(0.0, None)] * k
        for r in range(n_restart):
            x0 = np.sort(np.clip(mu2 + rng.normal(scale=max(sigma, 0.3), size=k),
                                 0.0, None))
            res = minimize(obj, x0, method="Nelder-Mead", bounds=bounds,
                           options={"xatol": 1e-4, "fatol": 1e-5, "maxiter": 4000})
            if best is None or res.fun < best.fun:
                best = res
        mu1 = np.sort(best.x)
        f2 = obj(mu2)
        f1 = float(best.fun)
        rel = 100.0 * (f2 - f1) / max(f1, 1e-12)
        rec = {
            "sigma": float(sigma),
            "obj_W2bary": f2,
            "obj_W1opt": f1,
            "rel_obj_gap_pct": float(rel),
            "global_feature_W2": float(mu2[-1]),
            "global_feature_W1": float(mu1[-1]),
            "global_feature_gap": float(abs(mu2[-1] - mu1[-1])),
            "linf_gap": float(np.max(np.abs(mu2 - mu1))),
        }
        rows.append(rec)
        print(f"  sigma={sigma:.1f}  rel gap={rel:5.2f}%  "
              f"|global d_W2-d_W1|={rec['global_feature_gap']:.3f}")
    return rows


# ---------------------------------------------------------------------------
# Verify
# ---------------------------------------------------------------------------

def verify():
    ref = reference_report()
    print("\n=== scale conflation (ecology) ===")
    for delta in (ECO_DELTA_CONFLATE,):
        b0a, b1a = betti_at(PREY_DISPERSED, delta)
        b0b, b1b = betti_at(PREY_COLUMN, delta)
        w1 = wasserstein_p(compute_h0(PREY_DISPERSED), compute_h0(PREY_COLUMN), 1)
        print(f"  delta={delta:.0f}: dispersed (beta0,beta1)=({b0a},{b1a}), "
              f"column=({b0b},{b1b}), W1={w1:.2f}")
        if (b0a, b1a) != (b0b, b1b):
            print("  WARNING: Betti numbers differ; pick another delta.")

    print("\n=== encirclement H1 (re-derived birth_max="
          f"{ECO_H1_BIRTH_MAX:.0f}, not football 45) ===")
    dgm = h1_diagram(PRED_RING)
    filled = np.vstack([PRED_RING, PREY_HERDED])
    print("  PRED_RING H1 bars:", np.round(dgm, 2).tolist() if dgm.size else "none")
    print(f"  H1 pers. ring      = {encirclement_h1(PRED_RING, birth_max=ECO_H1_BIRTH_MAX):.2f}")
    print(f"  H1 pers. ring+herd = {encirclement_h1(filled, birth_max=ECO_H1_BIRTH_MAX):.2f}")
    print("  RING+HERD H1 bars:", np.round(h1_diagram(filled), 2).tolist()
          if h1_diagram(filled).size else "none (hole filled)")

    print("\n=== scale conflation (robotics evaders) ===")
    b0a, b1a = betti_at(EVADERS_OPEN, ROB_DELTA_CONFLATE)
    b0b, b1b = betti_at(EVADERS_FILE, ROB_DELTA_CONFLATE)
    w1 = wasserstein_p(compute_h0(EVADERS_OPEN), compute_h0(EVADERS_FILE), 1)
    print(f"  delta={ROB_DELTA_CONFLATE:.0f}: open ({b0a},{b1a}), file ({b0b},{b1b}), W1={w1:.2f}")

    print("\nFootball leftovers that must not appear:")
    print("  A_WIDE deaths, W1=76.13, delta=35, birth_max=45, pitch 120x80.")
    return ref


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def fig_ecology_territory(sim=None):
    shots = (20, 59, 90)
    titles = (
        r"Dispersed hunting ($t<T^*$)",
        r"Transition ($T^*=55$)",
        r"Encircling a herded group",
    )
    fig = plt.figure(figsize=(13.6, 8.6), facecolor="white")
    gs = GridSpec(2, 3, figure=fig, height_ratios=[1.15, 0.88],
                  hspace=0.32, wspace=0.22, left=0.05, right=0.98,
                  top=0.88, bottom=0.07)
    for col, t in enumerate(shots):
        prey, pred = ecology_config(t, noise=0.0)
        ax = fig.add_subplot(gs[0, col])
        draw_box(ax, ECO_XLIM, ECO_YLIM, "#fefce8", "#a16207", pad=10)
        scatter_cloud(ax, pred, CB, delta=ECO_DELTA_H1, s=32, z=3)
        scatter_cloud(ax, prey, CA, delta=12.0, s=36, z=6)
        if t >= ECO_T_END:
            c = PRED_RING.mean(axis=0)
            ax.add_patch(mpatches.Circle(
                c, 42, fill=False, ls="--", lw=1.4, edgecolor=H1COL, zorder=8,
            ))
            ax.text(c[0], c[1] + 50, r"$H_1$", color=H1COL, ha="center",
                    fontsize=10, fontweight="bold")
        ax.set_title(titles[col], fontsize=11, fontweight="bold", color=CINK)
        ax.text(8, 8, rf"$t={t}$", fontsize=8, color=CGREY)
        panel_label(ax, "ABC"[col])
        if col == 0:
            ax.scatter([], [], s=36, c=[CA], label="Prey groups")
            ax.scatter([], [], s=32, c=[CB], label="Predator pack")
            ax.legend(frameon=False, fontsize=8, loc="upper left")

        axb = fig.add_subplot(gs[1, col])
        draw_h0_barcode(axb, compute_h0(prey), CA, delta=12.0, max_d=100,
                        ylabel="prey $H_0$" if col == 0 else "")
        panel_label(axb, "DEF"[col])
        axb.set_xlabel(r"Scale $\delta$ (territory units)", fontsize=8.5)

    fig.suptitle("Ecology generator: re-derived hierarchy, not a relabelled pitch",
                 fontsize=14, fontweight="bold", color=CINK, y=0.98)
    fig.text(0.5, 0.925,
             r"$N_{\mathrm{prey}}=15$, $N_{\mathrm{pred}}=12$, $\Omega=[0,240]\times[0,180]$ "
             r"(diameter $300$). Local deaths $\approx 7$; herded tactical deaths $\approx 17$–$20$; "
             r"dispersed groups merge only at $\approx 87$. Display $\delta$ sits in those gaps.",
             ha="center", fontsize=8.6, color=CGREY)
    return fig


def fig_conflation_and_h1():
    fig = plt.figure(figsize=(13.4, 8.8), facecolor="white")
    gs = GridSpec(2, 3, figure=fig, hspace=0.34, wspace=0.24,
                  left=0.05, right=0.98, top=0.88, bottom=0.07)

    specs = (
        (PREY_DISPERSED, "Dispersed groups", CA),
        (PREY_COLUMN, "North–south column", np.array([30, 64, 175]) / 255),
    )
    for col, (pts, title, colr) in enumerate(specs):
        ax = fig.add_subplot(gs[0, col])
        draw_box(ax, ECO_XLIM, ECO_YLIM, "#fefce8", "#a16207", pad=10)
        scatter_cloud(ax, pts, colr, delta=ECO_DELTA_CONFLATE, s=36)
        b0, b1 = betti_at(pts, ECO_DELTA_CONFLATE)
        ax.set_title(rf"{title}" + "\n" +
                     rf"$(\beta_0,\beta_1)=({b0},{b1})$ at $\delta={ECO_DELTA_CONFLATE:.0f}$",
                     fontsize=10.5, fontweight="bold", color=CINK)
        panel_label(ax, "AB"[col])

    axv = fig.add_subplot(gs[0, 2])
    w1 = wasserstein_p(compute_h0(PREY_DISPERSED), compute_h0(PREY_COLUMN), 1)
    axv.set_xlim(0, 1)
    axv.set_ylim(0, 1)
    axv.axis("off")
    axv.text(0.5, 0.72, "Single-scale Betti numbers", ha="center", fontsize=12,
             fontweight="bold", color=CINK)
    axv.text(0.5, 0.52, "do not determine the diagram", ha="center", fontsize=12,
             color=CINK)
    axv.text(0.5, 0.30, rf"$W_1={w1:.1f}$", ha="center", fontsize=18,
             fontweight="bold", color=CK)
    axv.text(0.5, 0.12, r"equal $(\beta_0,\beta_1)$, different hierarchy",
             ha="center", fontsize=9, color=CGREY, style="italic")
    panel_label(axv, "C")

    axr = fig.add_subplot(gs[1, 0])
    draw_box(axr, ECO_XLIM, ECO_YLIM, "#fefce8", "#a16207", pad=10)
    scatter_cloud(axr, PRED_RING, CB, delta=ECO_DELTA_H1, s=32)
    c = PRED_RING.mean(axis=0)
    axr.add_patch(mpatches.Circle(c, 42, fill=False, ls="--", lw=1.5,
                                  edgecolor=H1COL, zorder=8))
    pers = encirclement_h1(PRED_RING, birth_max=ECO_H1_BIRTH_MAX)
    axr.set_title(rf"Empty ring: $H_1$ persistence ${pers:.1f}$",
                  fontsize=10.5, fontweight="bold", color=CINK)
    panel_label(axr, "D")

    axf = fig.add_subplot(gs[1, 1])
    draw_box(axf, ECO_XLIM, ECO_YLIM, "#fefce8", "#a16207", pad=10)
    filled = np.vstack([PRED_RING, PREY_HERDED])
    scatter_cloud(axf, PRED_RING, CB, delta=ECO_DELTA_H1, s=32, z=3)
    scatter_cloud(axf, PREY_HERDED, CA, delta=12.0, s=36, z=6)
    pers_f = encirclement_h1(filled, birth_max=ECO_H1_BIRTH_MAX)
    axf.set_title(rf"Herd in the hole: $H_1$ persistence ${pers_f:.1f}$",
                  fontsize=10.5, fontweight="bold", color=CINK)
    panel_label(axf, "E")

    axb = fig.add_subplot(gs[1, 2])
    dgm = h1_diagram(PRED_RING)
    axb.axhline(0, color="#e5e7eb", lw=0.8)
    if dgm.size:
        axb.plot([dgm[0, 0], dgm[0, 1]], [1, 1], color=H1COL, lw=6, solid_capstyle="butt")
        axb.text(dgm[0, 1] + 2, 1, rf"$[{dgm[0, 0]:.1f},{dgm[0, 1]:.1f}]$",
                 va="center", fontsize=9, color=H1COL, fontweight="bold")
    axb.set_ylim(0.3, 1.8)
    axb.set_xlim(0, 110)
    axb.set_yticks([])
    axb.set_xlabel(r"$H_1$ birth–death (territory units)", fontsize=8.5)
    axb.spines["top"].set_visible(False)
    axb.spines["right"].set_visible(False)
    axb.set_title(r"Ring bar (birth max $=80$, not $45$)",
                  fontsize=10.5, fontweight="bold", color=CINK)
    panel_label(axb, "F")

    fig.suptitle("Scale conflation and encirclement $H_1$ on the ecology generator",
                 fontsize=14, fontweight="bold", color=CINK, y=0.98)
    fig.text(0.5, 0.925,
             r"Left: two prey layouts share $(\beta_0,\beta_1)$ at one $\delta$ but not $W_1$. "
             r"Right: $H_1$ is an embedding feature (ring vs filled interior), not a hierarchy feature.",
             ha="center", fontsize=8.6, color=CGREY)
    return fig


def fig_cusum(sim, kappa, h, mc_rows=None):
    fig = plt.figure(figsize=(13.2, 7.6), facecolor="white")
    gs = GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.28,
                  left=0.08, right=0.97, top=0.86, bottom=0.10)
    T = sim["T"]
    ax = fig.add_subplot(gs[0, 0])
    C = cusum_path(sim["w"], kappa, mon0=MON0)
    that = first_alarm(C, h, mon0=MON0)
    ax.plot(T, sim["w"], color=CINK, lw=1.1, label=r"$W_1(D_t,D_{t-1})$")
    ax.plot(T, C, color=CK, lw=1.5, label="CUSUM")
    ax.axhline(h, color=CK, ls="--", lw=0.9)
    ax.axvline(ECO_T_STAR, color=CGREY, ls=":", lw=1.0)
    if that is not None:
        ax.axvline(that, color=CA, lw=1.3)
        ax.text(that + 1.5, max(C.max(), h) * 0.9,
                rf"$\hat T={that}$", color=CA, fontsize=9, fontweight="bold")
    ax.set_xlim(0, T_MAX)
    ax.set_xlabel("Time $t$ (frames)", fontsize=9)
    ax.set_ylabel(r"$W_1$ / CUSUM", fontsize=9)
    ax.legend(frameon=False, fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    err = abs(that - ECO_T_STAR) if that is not None else np.nan
    ax.set_title(rf"Headline path (seed {HEADLINE_SEED}): $|\hat T-T^*|={err:.0f}$",
                 fontsize=11, fontweight="bold", color=CINK, loc="left")
    panel_label(ax, "A")

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(T, sim["frechet_var"], color=CK, lw=1.6)
    ax2.axvline(ECO_T_STAR, color=CGREY, ls=":", lw=1.0)
    ax2.set_xlim(0, T_MAX)
    ax2.set_xlabel("Time $t$ (frames)", fontsize=9)
    ax2.set_ylabel(r"Fréchet variance $\sigma_F^2$ ($W_2^2$)", fontsize=9)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.set_title(r"$W_2$ barycentre of a trailing window of prey diagrams",
                  fontsize=11, fontweight="bold", color=CINK, loc="left")
    panel_label(ax2, "B")

    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(T, sim["pers"], color=CB, lw=1.5)
    ax3.axvline(ECO_T_STAR, color=CGREY, ls=":", lw=1.0)
    ax3.set_xlim(0, T_MAX)
    ax3.set_xlabel("Time $t$ (frames)", fontsize=9)
    ax3.set_ylabel(r"Predator $H_1$ persistence", fontsize=9)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.set_title(r"Encirclement appears after $T^*$ (coordinated hunt)",
                  fontsize=11, fontweight="bold", color=CINK, loc="left")
    panel_label(ax3, "C")

    ax4 = fig.add_subplot(gs[1, 1])
    if mc_rows:
        x = [r["jump_w1"] for r in mc_rows]
        y = [r["mean_abs_err"] for r in mc_rows]
        p = [100 * r["power"] for r in mc_rows]
        ax4.plot(x, y, "o-", color=CINK, lw=1.5, label=r"$\mathbb{E}|\hat T-T^*|$")
        ax4.set_xlabel(r"Jump $W_1$", fontsize=9)
        ax4.set_ylabel(r"Mean localisation error", fontsize=9)
        ax4b = ax4.twinx()
        ax4b.plot(x, p, "s--", color=CA, lw=1.2, label="power")
        ax4b.set_ylabel("Detection power (%)", fontsize=9, color=CA)
        ax4.legend(frameon=False, fontsize=8, loc="upper left")
        ax4.set_title(rf"Monte Carlo $N={N_MC}$ (quote the curve, not one $\hat T$)",
                      fontsize=11, fontweight="bold", color=CINK, loc="left")
    else:
        ax4.axis("off")
        ax4.text(0.5, 0.5, "Monte Carlo skipped (--quick)", ha="center",
                 color=CGREY, fontsize=11)
    ax4.spines["top"].set_visible(False)
    panel_label(ax4, "D")

    fig.suptitle("Diagram $W_1$ CUSUM and $W_2$ Fréchet mean (T2 / T1 analogues)",
                 fontsize=14, fontweight="bold", color=CINK, y=0.97)
    fig.text(0.5, 0.915,
             r"Small-Grant T1/T2 are landscape-valued. This figure is the diagram analogue "
             r"(V&A R3 fallback). Thresholds are Monte Carlo 5% false-alarm, no $t\geq 30$ guard.",
             ha="center", fontsize=8.6, color=CGREY)
    return fig


def fig_t2_lite(mc_consec, mc_ref, kappa_ref, h_ref):
    """Theory (Wald on xi_t) versus consecutive-frame CUSUM (operational)."""
    fig = plt.figure(figsize=(12.4, 5.2), facecolor="white")
    gs = GridSpec(1, 2, figure=fig, wspace=0.32, left=0.08, right=0.97,
                  top=0.80, bottom=0.16)

    ax = fig.add_subplot(gs[0, 0])
    if mc_ref:
        x = [r["jump_w1"] for r in mc_ref]
        y = [r["mean_abs_err"] for r in mc_ref]
        wald = [r["wald_h_over_delta"] for r in mc_ref]
        ax.plot(x, y, "o-", color=CINK, lw=1.6,
                label=r"MC on $\xi_t=W_1(D_t,D_{\mathrm{ref}})$")
        interp = [r.get("interpolant_delay") for r in mc_ref]
        if any(v is not None for v in interp):
            ax.plot(x, interp, "D-", color=CA, lw=1.4,
                    label="noise-free interpolant CUSUM")
        ax.plot(x, wald, "s--", color=CK, lw=1.1, alpha=0.7,
                label=r"Wald $h/\delta$ (instant shift)")
        ax.set_xlabel(r"Jump $W_1$  ($J$)", fontsize=9)
        ax.set_ylabel(r"Mean delay  $\mathbb{E}|\hat T-T^*|$", fontsize=9)
        ax.legend(frameon=False, fontsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_title(r"T2-lite: coin-flip increments of $\xi_t$",
                     fontsize=11, fontweight="bold", color=CINK, loc="left")
    panel_label(ax, "A")

    ax2 = fig.add_subplot(gs[0, 1])
    if mc_consec:
        x2 = [r["jump_w1"] for r in mc_consec]
        y2 = [r["mean_abs_err"] for r in mc_consec]
        ax2.plot(x2, y2, "o-", color=CA, lw=1.6,
                 label=r"MC on $W_1(D_t,D_{t-1})$ (pulse)")
        ax2.set_xlabel(r"Jump $W_1$  ($J$)", fontsize=9)
        ax2.set_ylabel(r"Mean delay  $\mathbb{E}|\hat T-T^*|$", fontsize=9)
        ax2.legend(frameon=False, fontsize=8)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.set_title("Operational detector (not the T2-lite hypothesis)",
                      fontsize=11, fontweight="bold", color=CINK, loc="left")
    panel_label(ax2, "B")

    fig.suptitle("T2-lite Wald delay versus Monte Carlo (ecology prey)",
                 fontsize=14, fontweight="bold", color=CINK, y=0.97)
    fig.text(
        0.5, 0.88,
        r"Left: persistent statistic $\xi_t$. The noise-free interpolant CUSUM tracks Monte Carlo; "
        r"Wald $h/\delta$ is the instantaneous-shift special case and is too optimistic on a smoothstep. "
        r"Right: consecutive-frame $W_1$ is a pulse detector — not the T2-lite hypothesis. "
        r"Tug-of-war dependence is Tier 3.",
        ha="center", fontsize=8.4, color=CGREY,
    )
    return fig


def fig_robotics_and_dependence(kappa_r=None, h_r=None):
    fig = plt.figure(figsize=(13.6, 8.4), facecolor="white")
    gs = GridSpec(2, 3, figure=fig, hspace=0.36, wspace=0.24,
                  left=0.05, right=0.98, top=0.86, bottom=0.08)
    shots = (
        (10, "Open transit", False),
        (42, "Intercept", True),
        (75, "Funnel closed", True),
    )
    for col, (t, title, _) in enumerate(shots):
        purs, ev = robotics_config(t, noise=0.0)
        ax = fig.add_subplot(gs[0, col])
        draw_box(ax, ROB_XLIM, ROB_YLIM, "#f0f9ff", "#0284c7", pad=6)
        scatter_cloud(ax, purs, CR, delta=8.0, s=28, marker="s")
        scatter_cloud(ax, ev, CA, delta=8.0, s=32)
        ax.set_title(rf"{title}  ($t={t}$)", fontsize=10.5, fontweight="bold",
                     color=CINK)
        panel_label(ax, "ABC"[col])
        if col == 0:
            ax.scatter([], [], s=28, c=[CR], marker="s", label="Pursuers")
            ax.scatter([], [], s=32, c=[CA], label="Evaders")
            ax.legend(frameon=False, fontsize=8, loc="upper left")

    sA_c, sB_c = coupled_series(
        PREY_DISPERSED, PRED_HUNT, N_DEP, ECO_NOISE, drift=6.0, phi=0.7,
        rho=0.65, seed=2024, coupled=True, group_size_a=3, group_size_b=3,
        xlim=ECO_XLIM, ylim=ECO_YLIM,
    )
    sA_i, sB_i = coupled_series(
        PREY_DISPERSED, PRED_HUNT, N_DEP, ECO_NOISE, drift=6.0, phi=0.7,
        rho=0.65, seed=2024, coupled=False, group_size_a=3, group_size_b=3,
        xlim=ECO_XLIM, ylim=ECO_YLIM,
    )
    axd = fig.add_subplot(gs[1, :2])
    t = np.arange(N_DEP + 1)
    axd.plot(t, sA_c, color=CA, lw=1.3, label="coupled prey")
    axd.plot(t, sA_i, color=CGREY, lw=1.0, ls="--", label="independent prey")
    axd.set_xlabel("Time $t$ (frames)", fontsize=9)
    axd.set_ylabel(r"$W_1(D_t, D_{\mathrm{ref}})$", fontsize=9)
    axd.legend(frameon=False, fontsize=8)
    axd.spines["top"].set_visible(False)
    axd.spines["right"].set_visible(False)
    rho_c = float(np.corrcoef(sA_c[:-1], sA_c[1:])[0, 1])
    rho_i = float(np.corrcoef(sA_i[:-1], sA_i[1:])[0, 1])
    axd.set_title(rf"Identical marginals: coupled $\rho_1={rho_c:+.2f}$, "
                  rf"independent $\rho_1={rho_i:+.2f}$",
                  fontsize=11, fontweight="bold", color=CINK, loc="left")
    panel_label(axd, "D")

    axr = fig.add_subplot(gs[1, 2])
    b0a, b1a = betti_at(EVADERS_OPEN, ROB_DELTA_CONFLATE)
    b0b, b1b = betti_at(EVADERS_FILE, ROB_DELTA_CONFLATE)
    w1 = wasserstein_p(compute_h0(EVADERS_OPEN), compute_h0(EVADERS_FILE), 1)
    draw_h0_barcode(axr, compute_h0(EVADERS_OPEN), CA, delta=ROB_DELTA_CONFLATE,
                    max_d=50, ylabel="open")
    axr.set_title(rf"Evaders at $\delta={ROB_DELTA_CONFLATE:.0f}$: "
                  rf"$({b0a},{b1a})$ vs file $({b0b},{b1b})$" + "\n" +
                  rf"$W_1={w1:.1f}$ (own gaps, not football $\delta$)",
                  fontsize=10, fontweight="bold", color=CINK)
    panel_label(axr, "E")

    fig.suptitle("Robotics generator (pairs, corridor) and competitive dependence",
                 fontsize=14, fontweight="bold", color=CINK, y=0.97)
    fig.text(0.5, 0.915,
             r"$N_{\mathrm{pursuer}}=8$, $N_{\mathrm{evader}}=6$, $\Omega=[0,180]\times[0,50]$ "
             r"(diameter $187$). Pair geometry, not the football triangle. "
             r"CUSUM is run on evader $H_0$; pursuer pinch is a different jump.",
             ha="center", fontsize=8.6, color=CGREY)
    return fig, rho_c, rho_i


def save_fig(fig, name):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    print(f"Saved {path}")
    return str(path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()

    ref = verify()
    if args.verify:
        return

    stored = json.loads(NUM_PATH.read_text()) if NUM_PATH.exists() else {}
    stored_eco = stored.get("ecology", {})

    sim = headline_ecology()
    # Null calibration: alpha=0 (no jump), several seeds.
    n_null = 40 if args.quick else 80
    nulls = np.array([consecutive_w1(prey_jump_series(0.0, ECO_NOISE, 4000 + s))
                      for s in range(n_null)])
    mu0, sig0, kappa, h = calibrate_cusum(nulls)
    C = cusum_path(sim["w"], kappa, mon0=MON0)
    that = first_alarm(C, h, mon0=MON0)
    print(f"\nEcology CUSUM: mu0={mu0:.2f}, sig0={sig0:.2f}, kappa={kappa:.2f}, h={h:.2f}")
    print(f"Headline T_hat={that}, T*={ECO_T_STAR}, error="
          f"{abs(that - ECO_T_STAR) if that is not None else 'none'}")

    mc_rows = None
    rob_mc = None
    mc_ref = None
    t1_rows = None
    kappa_xi = h_xi = None
    if not args.quick:
        alphas = (0.35, 0.55, 0.75, 1.0)
        jumps = [wasserstein_p(compute_h0(PREY_DISPERSED),
                               compute_h0(interpolate_cloud(PREY_DISPERSED, PREY_HERDED, a)), 1)
                 for a in alphas]
        mc_rows = monte_carlo(prey_jump_series, alphas, jumps, N_MC, kappa, h,
                              ECO_T_STAR, "ecology-prey")

        nulls_r = np.array([consecutive_w1(evader_jump_series(0.0, ROB_NOISE, 5000 + s))
                            for s in range(n_null)])
        _, _, kappa_r, h_r = calibrate_cusum(nulls_r)
        jumps_r = [wasserstein_p(compute_h0(EVADERS_OPEN),
                                 compute_h0(interpolate_cloud(EVADERS_OPEN, EVADERS_FUNNEL, a)), 1)
                   for a in alphas]
        rob_mc = monte_carlo(evader_jump_series, alphas, jumps_r, N_MC, kappa_r, h_r,
                             ROB_T_STAR, "robotics-evaders")

        t1_rows = t1_lite_sweep()
        nulls_xi = np.array([prey_ref_w1_series(0.0, ECO_NOISE, 8000 + s)
                             for s in range(n_null)])
        _, _, kappa_xi, h_xi = calibrate_cusum(nulls_xi)
        print(f"T2-lite xi CUSUM: kappa={kappa_xi:.2f}, h={h_xi:.2f}")
        mc_ref = monte_carlo_ref(alphas, jumps, N_MC, kappa_xi, h_xi,
                                 ECO_T_STAR, ECO_NOISE)
    else:
        kappa_r = h_r = None
        mc_rows = stored_eco.get("mc")
        rob_mc = stored.get("robotics", {}).get("mc")
        mc_ref = stored_eco.get("mc_ref_xi")
        cusum_xi = stored_eco.get("cusum_xi") or {}
        kappa_xi = cusum_xi.get("kappa")
        h_xi = cusum_xi.get("h")
        print("(--quick) using stored MC tables for figure overlays; "
              "numbers.json will not be rewritten")

    save_fig(fig_ecology_territory(sim), "fig1_ecology_territory.png")
    save_fig(fig_conflation_and_h1(), "fig2_conflation_h1.png")
    save_fig(fig_cusum(sim, kappa, h, mc_rows), "fig3_cusum_frechet.png")
    fig4, rho_c, rho_i = fig_robotics_and_dependence(kappa_r, h_r)
    save_fig(fig4, "fig4_robotics_dependence.png")
    if mc_ref is not None:
        save_fig(fig_t2_lite(mc_rows, mc_ref, kappa_xi, h_xi), "fig5_t2_lite.png")

    numbers = {
        "ecology": {
            "N_prey": 15,
            "N_pred": 12,
            "diameter": 300.0,
            "H0_prey_dispersed": compute_h0(PREY_DISPERSED).round(2).tolist(),
            "H0_prey_herded": compute_h0(PREY_HERDED).round(2).tolist(),
            "H0_prey_column": compute_h0(PREY_COLUMN).round(2).tolist(),
            "H0_pred_hunt": compute_h0(PRED_HUNT).round(2).tolist(),
            "H0_pred_ring": compute_h0(PRED_RING).round(2).tolist(),
            "W1_dispersed_herded": float(wasserstein_p(compute_h0(PREY_DISPERSED),
                                                       compute_h0(PREY_HERDED), 1)),
            "W1_dispersed_column": float(wasserstein_p(compute_h0(PREY_DISPERSED),
                                                       compute_h0(PREY_COLUMN), 1)),
            "delta_conflate": ECO_DELTA_CONFLATE,
            "betti_conflate": {
                "dispersed": list(betti_at(PREY_DISPERSED, ECO_DELTA_CONFLATE)),
                "column": list(betti_at(PREY_COLUMN, ECO_DELTA_CONFLATE)),
            },
            "H1_ring_bar": h1_diagram(PRED_RING).round(2).tolist(),
            "H1_ring_pers": float(encirclement_h1(PRED_RING, birth_max=ECO_H1_BIRTH_MAX)),
            "H1_filled_pers": float(encirclement_h1(
                np.vstack([PRED_RING, PREY_HERDED]), birth_max=ECO_H1_BIRTH_MAX)),
            "birth_max": ECO_H1_BIRTH_MAX,
            "T_star": ECO_T_STAR,
            "headline_T_hat": that,
            "headline_error": abs(that - ECO_T_STAR) if that is not None else None,
            "cusum": {"mu0": mu0, "sig0": sig0, "kappa": kappa, "h": h},
            "mc": mc_rows,
            "mc_ref_xi": mc_ref,
            "cusum_xi": None if kappa_xi is None else {"kappa": kappa_xi, "h": h_xi},
            "rho1_coupled": rho_c,
            "rho1_independent": rho_i,
            "rho1_coupled_mean_80": 0.296,
            "rho1_coupled_sd_80": 0.139,
            "rho1_independent_mean_80": -0.025,
            "rho1_independent_sd_80": 0.106,
        },
        "t1_lite": t1_rows,
        "robotics": {
            "N_pursuer": 8,
            "N_evader": 6,
            "diameter": 186.82,
            "H0_pursuers_gate": compute_h0(PURSUERS_GATE).round(2).tolist(),
            "H0_pursuers_chase": compute_h0(PURSUERS_CHASE).round(2).tolist(),
            "H0_evaders_open": compute_h0(EVADERS_OPEN).round(2).tolist(),
            "H0_evaders_funnel": compute_h0(EVADERS_FUNNEL).round(2).tolist(),
            "H0_evaders_file": compute_h0(EVADERS_FILE).round(2).tolist(),
            "W1_pursuer_jump": float(wasserstein_p(compute_h0(PURSUERS_GATE),
                                                   compute_h0(PURSUERS_CHASE), 1)),
            "W1_evader_jump": float(wasserstein_p(compute_h0(EVADERS_OPEN),
                                                  compute_h0(EVADERS_FUNNEL), 1)),
            "W1_open_file": float(wasserstein_p(compute_h0(EVADERS_OPEN),
                                                compute_h0(EVADERS_FILE), 1)),
            "delta_conflate": ROB_DELTA_CONFLATE,
            "mc": rob_mc,
        },
        "not_football": {
            "A_WIDE_forbidden": True,
            "pitch_120x80_forbidden": True,
            "W1_76_13_forbidden": True,
        },
    }
    if args.quick:
        print("(--quick) skipped write of numbers.json")
        return
    NUM_PATH.write_text(json.dumps(numbers, indent=2))
    print(f"\nWrote {NUM_PATH}")


if __name__ == "__main__":
    main()
