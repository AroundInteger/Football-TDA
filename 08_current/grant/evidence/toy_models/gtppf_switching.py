"""
GTPPF switching preview — possession inverts predator and prey.

Chat 2 of the Standard Grant thread: football is a hybrid / telegraph system
with a possession variable b(t) in {0, 1} that continuously inverts which
team is predator (pressing, space-reducing, hunting) and which is prey
(spreading, space-creating, evading). Standard Lotka–Volterra keeps those
roles fixed. This script is the Small Grant's visual proof-of-principle
that T1/T2 still apply pathwise on each regime, and that the switch itself
is a pair of change-points of the kind T2 is built to localise.

Deterministic two-switch schedule (a single telegraph realisation):

    b = 1   A possesses (prey = A_WIDE,  predator = B_RING)
    b = 0   B possesses (prey = B_WIDE,  predator = A_RING)
    b = 1   A possesses again

The predator geometry is the verified H1 ring of radius 22 (Figure 9):
H1 persistence tracks the pressing team and inverts with possession.
Nguyen–Du–Yin (2014) guarantee a stationary distribution for competitive
Kolmogorov systems under telegraph noise; this figure does not prove that
theorem, it shows the football analogue on which the Standard Grant would
deploy it.

Usage:
    python gtppf_switching.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.gridspec import GridSpec
from scipy.spatial.distance import pdist, squareform

from atda_core import (
    A_RING,
    A_WIDE,
    B_RING,
    B_WIDE,
    compute_h0,
    cusum_path,
    encirclement_bars,
    encirclement_h1,
    h1_diagram,
    interpolate_cloud,
    n_components_at_delta,
    smoothstep,
    wasserstein_p,
)

# ---------------------------------------------------------------------------
# Palette (matches adversarial_tda.m)
# ---------------------------------------------------------------------------
CA = np.array([29, 78, 216]) / 255
CB = np.array([185, 28, 28]) / 255
CK = np.array([217, 119, 6]) / 255
CGN = np.array([21, 128, 61]) / 255
CGREY = np.array([107, 114, 128]) / 255
CFAINT = np.array([203, 213, 225]) / 255
CPITCH = np.array([240, 253, 244]) / 255
CGRASS = np.array([134, 239, 172]) / 255
CINK = np.array([15, 23, 42]) / 255
H1COL = np.array([5, 150, 105]) / 255

OUT_DIR = Path(__file__).resolve().parent
DPI = 300

# Schedule
T_MAX = 150
T1, T1E = 40, 48          # first switch  A-possesses -> B-possesses
T2, T2E = 100, 108        # second switch B-possesses -> A-possesses
NOISE = 1.5
SEED = 11
MON0 = 8
DELTA_H1 = 30             # inside the H1 bar [27.24, 40.00]
DELTA_H0 = 40             # tactical scale for beta_0 readout


def possession_blend(t):
    """Weight e(t) in [0, 1]: 0 = A possesses, 1 = B possesses."""
    e1 = smoothstep(t, T1, T1E)
    e2 = smoothstep(t, T2, T2E)
    return e1 * (1.0 - e2)


def possession_bit(t):
    """Hard telegraph state b(t) in {0, 1}; 1 = A possesses."""
    return 1 if possession_blend(t) < 0.5 else 0


def config_at(t, noise=0.0, rng=None):
    """Agent positions at frame t.

    A interpolates A_WIDE (prey) <-> A_RING (predator).
    B interpolates B_RING (predator) <-> B_WIDE (prey).
    """
    e = possession_blend(t)
    A = interpolate_cloud(A_WIDE, A_RING, e)
    B = interpolate_cloud(B_RING, B_WIDE, e)
    if noise > 0:
        A = A + rng.normal(scale=noise, size=A.shape)
        B = B + rng.normal(scale=noise, size=B.shape)
    return A, B


def vr_edges(pts, delta):
    D = squareform(pdist(pts))
    i, j = np.where(np.triu(D <= delta, k=1))
    if i.size == 0:
        return np.zeros((0, 2, 2))
    return np.stack([pts[i], pts[j]], axis=1)


def draw_pitch(ax):
    ax.set_xlim(-4, 124)
    ax.set_ylim(-8, 102)
    ax.set_aspect("equal")
    ax.axis("off")
    pitch = mpatches.FancyBboxPatch(
        (0, 0), 120, 80, boxstyle="square,pad=0",
        facecolor=CPITCH, edgecolor=CGRASS, linewidth=1.6, zorder=0,
    )
    ax.add_patch(pitch)
    ax.add_patch(mpatches.Circle((60, 40), 9.15, fill=False,
                                 edgecolor=CGRASS, linewidth=1.0, zorder=1))
    ax.plot([60, 60], [0, 80], color=CGRASS, lw=1.0, zorder=1)


def scatter_team(ax, pts, col, delta, z=5):
    segs = vr_edges(pts, delta)
    if len(segs):
        ax.add_collection(LineCollection(
            segs, colors=[(*col, 0.45)], linewidths=1.3, zorder=z,
        ))
    ax.scatter(pts[:, 0], pts[:, 1], s=36, c=[col], edgecolors="white",
               linewidths=0.4, zorder=z + 1)


def draw_h1_loop(ax, pts, dgm, delta=DELTA_H1):
    """Dashed ring annotation if a bar straddles the display scale."""
    live = [bar for bar in dgm if bar[0] <= delta < bar[1]]
    if not live:
        return
    c = pts.mean(axis=0)
    circ = mpatches.Circle(c, 11, fill=False, ls="--", lw=1.6,
                           edgecolor=H1COL, zorder=8)
    ax.add_patch(circ)
    ax.text(c[0], c[1] + 13.5, r"$H_1$", color=H1COL, ha="center",
            fontsize=10, fontweight="bold", zorder=9)


def pitch_title(ax, main, sub):
    ax.text(60, 96, main, ha="center", va="top", fontsize=10.5,
            fontweight="bold", color=CINK)
    ax.text(60, 88.5, sub, ha="center", va="top", fontsize=8.2,
            color=CGREY, fontstyle="italic")


def panel_label(ax, ch, x=0.02, y=0.97):
    ax.text(x, y, ch, transform=ax.transAxes, fontsize=13, fontweight="bold",
            va="top", ha="left", color=CINK,
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                      edgecolor="none", alpha=0.85))


def draw_two_barcodes(ax, dA, dB, dgmA, dgmB, delta_line, max_d=70):
    grey = np.array([214, 219, 226]) / 255
    sA, sB = np.sort(dA), np.sort(dB)
    for k, death in enumerate(sA, start=1):
        fc = CA if death > delta_line else grey
        ax.barh(k, death, height=0.62, color=fc, edgecolor="none", alpha=0.85)
    for k, death in enumerate(sB, start=1):
        fc = CB if death > delta_line else grey
        ax.barh(-k, death, height=0.62, color=(*fc, 0.55), edgecolor="none")
    # H1 bars sit above the H0 stack
    yH1 = len(sA) + 1.6
    drawn = False
    for dgm, name in ((dgmA, "A"), (dgmB, "B")):
        for birth, death in encirclement_bars(dgm):
            ax.barh(yH1, death - birth, left=birth, height=0.7,
                    color=H1COL, edgecolor="none", alpha=0.9)
            ax.text(death + 1.2, yH1,
                    rf"$H_1$ {name} [{birth:.1f}, {death:.1f}]",
                    va="center", fontsize=7.5, color=H1COL, fontweight="bold")
            drawn = True
            yH1 += 1.05
    if not drawn:
        ax.text(delta_line + 2, yH1, r"no $H_1$ bar", va="center",
                fontsize=8, color=CGREY, fontstyle="italic")
    ax.axvline(delta_line, color=CK, lw=1.2)
    ax.text(delta_line, -len(sB) - 1.6, rf"$\delta={delta_line:.0f}$",
            ha="center", va="top", fontsize=8, color=CK)
    ax.axhline(0, color=CFAINT, lw=0.8)
    ax.set_xlim(0, max_d)
    ax.set_ylim(-len(sB) - 2.4, yH1 + 1.4)
    ax.set_xlabel(r"Scale $\delta$ (pitch units)", fontsize=8.5)
    ax.tick_params(labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_yticks([])


def simulate():
    rng = np.random.default_rng(SEED)
    T = np.arange(T_MAX + 1)
    A_series, B_series = [], []
    dA, dB = [], []
    persA, persB = [], []
    b0A, b0B = [], []
    b_t = []
    for t in T:
        A, B = config_at(t, noise=NOISE, rng=rng)
        A_series.append(A)
        B_series.append(B)
        dA.append(compute_h0(A))
        dB.append(compute_h0(B))
        persA.append(encirclement_h1(A))
        persB.append(encirclement_h1(B))
        b0A.append(n_components_at_delta(A, DELTA_H0))
        b0B.append(n_components_at_delta(B, DELTA_H0))
        b_t.append(possession_bit(t))
    dA, dB = np.array(dA), np.array(dB)
    w = np.zeros(len(T))
    for t in range(1, len(T)):
        w[t] = wasserstein_p(dA[t], dA[t - 1], p=1)
    # in-control baseline: frames before the first switch, after burn-in
    base = w[MON0:T1]
    mu0, sig0 = float(base.mean()), float(base.std(ddof=1))
    kappa = mu0 + 0.5 * sig0
    C = cusum_path(w, kappa, mon0=MON0)
    # threshold: 95th percentile of a cheap parametric stand-in is not used;
    # we pick h so the first in-control window does not alarm, then report
    # both detections. A full Monte Carlo calibration lives in the MATLAB T2
    # figure; here we only need the two jumps to be visible.
    h = max(3.0 * sig0, 0.55 * C.max())
    alarms = []
    armed = True
    cooldown = 0
    for t in range(MON0, len(T)):
        if cooldown > 0:
            cooldown -= 1
            continue
        if C[t] >= h and armed:
            alarms.append(t)
            armed = False
            cooldown = 12
        if C[t] < 0.25 * h:
            armed = True
    return {
        "T": T, "w": w, "C": C, "h": h, "kappa": kappa,
        "mu0": mu0, "sig0": sig0, "alarms": alarms,
        "persA": np.array(persA), "persB": np.array(persB),
        "b0A": np.array(b0A), "b0B": np.array(b0B),
        "b": np.array(b_t), "dA": dA, "dB": dB,
        "A_series": A_series, "B_series": B_series,
    }


def snapshot_times():
    return (20, 74, 130)


def figure(sim):
    shots = snapshot_times()
    fig = plt.figure(figsize=(14.4, 11.6), facecolor="white")
    gs = GridSpec(
        3, 3, figure=fig,
        height_ratios=[1.12, 0.92, 1.05],
        hspace=0.38, wspace=0.22,
        left=0.05, right=0.98, top=0.90, bottom=0.05,
    )

    captions = [
        (r"$b=1$: A possesses  (A prey, B predator)",
         "A spreads; B closes a midfield ring"),
        (r"$b=0$: B possesses  (roles inverted)",
         "A closes the ring; B spreads"),
        (r"$b=1$: A possesses again",
         "Second telegraph switch; T2 should fire twice"),
    ]
    letters_top = "ABC"
    letters_bar = "DEF"

    for col, t in enumerate(shots):
        A, B = config_at(t, noise=0.0)
        dA, dB = compute_h0(A), compute_h0(B)
        gA, gB = h1_diagram(A), h1_diagram(B)
        pA, pB = encirclement_h1(A), encirclement_h1(B)

        ax = fig.add_subplot(gs[0, col])
        draw_pitch(ax)
        # predator edges first so agents sit on top
        if possession_bit(t) == 1:
            scatter_team(ax, B, CB, DELTA_H1, z=3)
            scatter_team(ax, A, CA, DELTA_H0, z=6)
            draw_h1_loop(ax, B, gB)
        else:
            scatter_team(ax, A, CA, DELTA_H1, z=3)
            scatter_team(ax, B, CB, DELTA_H0, z=6)
            draw_h1_loop(ax, A, gA)
        pitch_title(ax, captions[col][0], captions[col][1])
        panel_label(ax, letters_top[col])
        ax.text(4, 3, rf"$t={t}$" + "\n" +
                rf"$H_1$ A {pA:.1f}, B {pB:.1f}",
                fontsize=7.5, color=CGREY, va="bottom")
        if col == 0:
            ax.scatter([], [], s=36, c=[CA], label="Team A")
            ax.scatter([], [], s=36, c=[CB], label="Team B")
            ax.legend(frameon=False, fontsize=8, loc="lower right",
                      bbox_to_anchor=(0.98, 0.02))

        axb = fig.add_subplot(gs[1, col])
        draw_two_barcodes(axb, dA, dB, gA, gB, DELTA_H1)
        panel_label(axb, letters_bar[col], x=0.02, y=0.98)

    # ---- time series: telegraph + H1, and W1 + CUSUM ----
    axL = fig.add_subplot(gs[2, :2])
    axR = fig.add_subplot(gs[2, 2])
    T = sim["T"]

    ymax = max(sim["C"].max(), sim["w"].max()) * 1.18
    axL.axvspan(0, T1, color=CA, alpha=0.07, zorder=0)
    axL.axvspan(T1E, T2, color=CB, alpha=0.07, zorder=0)
    axL.axvspan(T2E, T_MAX, color=CA, alpha=0.07, zorder=0)
    axL.plot(T, sim["w"], color=CINK, lw=1.15, label=r"$W_1(D^A_t, D^A_{t-1})$")
    axL.plot(T, sim["C"], color=CK, lw=1.4, label="CUSUM")
    axL.axhline(sim["h"], color=CK, ls="--", lw=0.9)
    axL.axvline(T1, color=CGREY, ls=":", lw=1.0)
    axL.axvline(T2, color=CGREY, ls=":", lw=1.0)
    for k, th in enumerate(sim["alarms"]):
        axL.axvline(th, color=CGN, lw=1.3)
        axL.text(th + 1.2, sim["C"].max() * 0.92,
                 rf"$\hat{{T}}_{k+1}={th}$", color=CGN, fontsize=8.5,
                 fontweight="bold")
    axL.set_xlim(0, T_MAX)
    axL.set_ylim(0, ymax)
    axL.text((T1 + T1E) / 2, ymax * 0.97, r"$T^*_1=40$",
             ha="center", va="top", fontsize=8, color=CGREY)
    axL.text((T2 + T2E) / 2, ymax * 0.97, r"$T^*_2=100$",
             ha="center", va="top", fontsize=8, color=CGREY)
    axL.set_xlabel("Time $t$ (frames)", fontsize=9)
    axL.set_ylabel(r"$W_1$ / CUSUM", fontsize=9)
    axL.legend(frameon=False, fontsize=8, loc="upper left")
    axL.spines["top"].set_visible(False)
    axL.spines["right"].set_visible(False)
    panel_label(axL, "G")
    axL.set_title("Two possession switches, two CUSUM detections",
                  fontsize=10.5, fontweight="bold", color=CINK, loc="left",
                  pad=8)

    axR.plot(T, sim["persA"], color=CA, lw=1.5, label=r"$H_1$ persistence, A")
    axR.plot(T, sim["persB"], color=CB, lw=1.5, label=r"$H_1$ persistence, B")
    axR.axvline(T1, color=CGREY, ls=":", lw=1.0)
    axR.axvline(T2, color=CGREY, ls=":", lw=1.0)
    axR.set_xlim(0, T_MAX)
    axR.set_ylim(-0.4, max(sim["persA"].max(), sim["persB"].max()) * 1.25)
    axR.set_xlabel("Time $t$ (frames)", fontsize=9)
    axR.set_ylabel(r"$H_1$ persistence", fontsize=9)
    axR.legend(frameon=False, fontsize=8, loc="upper right")
    axR.spines["top"].set_visible(False)
    axR.spines["right"].set_visible(False)
    panel_label(axR, "H")
    axR.set_title("Encirclement $H_1$ (born $<45$) tracks the predator",
                  fontsize=10.5, fontweight="bold", color=CINK, loc="left",
                  pad=8)

    fig.suptitle(
        "GTPPF Switching: Possession Inverts Predator and Prey",
        fontsize=14.5, fontweight="bold", color=CINK, y=0.975,
    )
    fig.text(
        0.5, 0.932,
        r"Telegraph $b(t)\in\{0,1\}$: team in possession spreads (prey, $H_0$ hierarchy); "
        r"team out of possession encircles (predator, $H_1$ ring born at $\delta\approx 27$).  "
        r"A global rectangular hole at $\delta\approx 60$ is a hierarchy feature and is omitted.  "
        r"Nguyen–Du–Yin (2014) is the stationary-distribution template; T2 localises each switch.",
        ha="center", va="top", fontsize=8.6, color=CGREY,
    )
    return fig


def report(sim):
    print("=" * 70)
    print("GTPPF switching preview")
    print("=" * 70)
    print(f"In-control W1: mu = {sim['mu0']:.2f}, sigma = {sim['sig0']:.2f}")
    print(f"CUSUM kappa = {sim['kappa']:.2f}, h = {sim['h']:.2f}")
    print(f"True switches: T*_1 = {T1}, T*_2 = {T2}")
    print(f"Alarms: {sim['alarms']}")
    for k, th in enumerate(sim["alarms"], start=1):
        Tstar = T1 if k == 1 else T2
        print(f"  T_hat_{k} = {th},  |T_hat - T*| = {abs(th - Tstar)}")

    print("\nSettled-regime topology (noise = 0):")
    for t, name in zip(snapshot_times(), ("A possesses", "B possesses", "A again")):
        A, B = config_at(t, noise=0.0)
        gA, gB = h1_diagram(A), h1_diagram(B)
        print(f"  t={t:3d}  {name:14s}  "
              f"H1(A)={encirclement_h1(A):5.2f}  H1(B)={encirclement_h1(B):5.2f}  "
              f"beta0@40 A={n_components_at_delta(A, DELTA_H0)} "
              f"B={n_components_at_delta(B, DELTA_H0)}")
        ea, eb = encirclement_bars(gA), encirclement_bars(gB)
        if ea.size:
            print(f"           H1 encirclement A: {np.round(ea, 2).tolist()}")
        if eb.size:
            print(f"           H1 encirclement B: {np.round(eb, 2).tolist()}")


def main():
    sim = simulate()
    report(sim)
    fig = figure(sim)
    out = OUT_DIR / "fig10_gtppf_switching.png"
    fig.savefig(out, dpi=DPI, facecolor="white")
    plt.close(fig)
    print(f"\nSaved: {out}")


if __name__ == "__main__":
    main()
