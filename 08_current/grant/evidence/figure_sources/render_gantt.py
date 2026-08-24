"""Render the compact JeS Gantt (timeline only). Locked to TIMELINE.md."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

OUT = Path(__file__).with_name("grant_figure_gantt.png")

DARK, BLUE, GREEN, ORANGE, PURPLE = "#1C2B40", "#2A5FA5", "#2E7D52", "#C4611E", "#5B3FA0"
MUTED, GRID, HDR, BORD = "#6B7C93", "#DDE3EC", "#EEF2F7", "#B8C5D6"

# 16 cm × 5.2 cm: title dropped (in caption); no dead band under the key.
fig, ax = plt.subplots(figsize=(16 / 2.54, 5.2 / 2.54), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(1.7, 27.2)
ax.axis("off")
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

SL = 1.4
CL, CR = 23.0, 98.6
MW = (CR - CL) / 12
BH = 1.10
PITCH = 2.25


def mx(month, edge="centre"):
    if edge == "left":
        return CL + (month - 1) * MW
    if edge == "right":
        return CL + month * MW
    return CL + (month - 0.5) * MW


def bar(m0, m1, y, facecolor, edgecolor=None, alpha=1.0):
    ax.add_patch(Rectangle(
        (mx(m0, "left"), y), mx(m1, "right") - mx(m0, "left"), BH,
        linewidth=0.35, facecolor=facecolor, edgecolor=edgecolor or facecolor,
        alpha=alpha,
    ))


def row(label, y, m0, m1, facecolor, alpha, edgecolor=None):
    ax.text(CL - 1.1, y + BH / 2, label, ha="right", va="center",
            fontsize=8.5, color=DARK, clip_on=False)
    bar(m0, m1, y, facecolor, edgecolor, alpha)


def section(name, y0, y1):
    ax.text(SL, (y0 + y1) / 2, name, ha="left", va="center",
            fontsize=8, color=MUTED, style="italic")


# Slim month header
ax.add_patch(Rectangle((CL, 25.85), CR - CL, 1.05, facecolor=HDR, edgecolor="none"))
ax.text(CL - 1.1, 26.35, "Month", ha="right", va="center", fontsize=8, color=MUTED)
grid_bottom = 7.85
for n in range(1, 13):
    ax.text(mx(n), 26.35, str(n), ha="center", va="center", fontsize=8, color="#4A5568")
    ax.plot([mx(n, "left"), mx(n, "left")], [grid_bottom, 25.85], color=GRID, lw=0.4)
ax.plot([CR, CR], [grid_bottom, 25.85], color=GRID, lw=0.4)

y_pi = 24.15
y_co = y_pi - PITCH
y_ra = y_co - PITCH
row("PI (0.2 FTE)", y_pi, 1, 12, DARK, 0.18, DARK)
row("Co-Is (0.1)", y_co, 1, 12, PURPLE, 0.22, PURPLE)
row("Res. Associate", y_ra, 2, 10, BLUE, 0.85)
section("Team", y_ra, y_pi + BH)

div1 = y_ra - 0.40
ax.plot([SL, 99.2], [div1, div1], color=BORD, lw=0.5)

y_o1 = div1 - 0.50 - BH
y_o2 = y_o1 - PITCH
row("O1 Geometry", y_o1, 1, 9, GREEN, 0.85)
row("O2 Inference", y_o2, 4, 10, ORANGE, 0.85)
section("Objectives", y_o2, y_o1 + BH)

div2 = y_o2 - 0.40
ax.plot([SL, 99.2], [div2, div2], color=BORD, lw=0.5)

y_gate = div2 - 1.55
section("Gates", y_gate - 0.45, y_gate + 0.95)
for n, lbl in ((2, "1"), (7, "2"), (8, "3"), (9, "4")):
    ax.text(mx(n), y_gate + 0.85, lbl, ha="center", va="center", fontsize=8, color=DARK)
    c = mx(n)
    ax.add_patch(Polygon(
        [(c, y_gate + 0.35), (c + 0.50, y_gate - 0.25), (c, y_gate - 0.85), (c - 0.50, y_gate - 0.25)],
        closed=True, facecolor=DARK, edgecolor="none",
    ))

div3 = y_gate - 1.10
ax.plot([SL, 99.2], [div3, div3], color=BORD, lw=0.5)

y_out = div3 - 1.15
section("Outputs", y_out - 0.55, y_out + 0.55)
for n in (2, 10, 11, 12):
    c = mx(n)
    ax.add_patch(Polygon(
        [(c, y_out + 0.40), (c + 0.50, y_out - 0.40), (c - 0.50, y_out - 0.40)],
        closed=True, facecolor=PURPLE, edgecolor="none",
    ))

# [17] has room; M10–12 hang diagonally down-left so they cannot collide.
ax.text(mx(2), y_out - 0.70, "[17]", ha="center", va="top",
        fontsize=7.5, color=PURPLE)
for n, lbl in ((10, "Handover"), (11, "Paper"), (12, "Pack")):
    ax.text(
        mx(n) + 0.15, y_out - 0.58, lbl,
        ha="right", va="top", rotation=42, rotation_mode="anchor",
        fontsize=7.5, color=PURPLE, clip_on=False,
    )

# Key sits immediately under the diagonal labels
ax.add_patch(Polygon([(2.4, 5.35), (3.0, 4.70), (2.4, 4.05), (1.8, 4.70)],
                     closed=True, facecolor=DARK, edgecolor="none"))
ax.text(3.5, 4.70, "1  OSF + cutoff (M2)   2  barcodes (M7)   3  landscape module (M8)   4  T1/T2 + O1 geometry (M9)",
        ha="left", va="center", fontsize=7, color=DARK)
ax.add_patch(Polygon([(2.4, 3.45), (3.0, 2.60), (1.8, 2.60)],
                     closed=True, facecolor=PURPLE, edgecolor="none"))
ax.text(3.5, 2.85, "[17] (M2)   RA handover (M10)   season paper (M11)   evidence pack (M12)",
        ha="left", va="center", fontsize=7, color=PURPLE)

fig.subplots_adjust(left=0.02, right=0.995, top=0.99, bottom=0.02)
fig.savefig(OUT, dpi=300, facecolor="white")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
