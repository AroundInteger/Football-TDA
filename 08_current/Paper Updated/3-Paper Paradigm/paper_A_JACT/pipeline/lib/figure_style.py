"""Publication style for Paper A figures.

Starting point, not a rigid template. The caption carries the narrative.
Axis titles are omitted. Panel letters sit inside the axes.

Defaults: labels 12 pt; tick labels 10 pt; annotations and legends 12 pt;
export at 300 dpi with Type 42 fonts.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt

TEXTWIDTH_IN = 16.0 / 2.54


@dataclass(frozen=True)
class FigureStyle:
    fs_label: int = 12
    fs_tick: int = 10
    fs_annot: int = 12
    fs_legend: int = 12
    dpi: int = 300
    text: str = "#222222"
    individual: str = "#0072B2"
    tactical: str = "#D55E00"
    team: str = "#009E73"
    mark: str = "#111111"
    muted: str = "#9E9E9E"


STYLE = FigureStyle()

# Axes-fraction box reserved for a northwest panel letter.
# Keep other annotations and data labels outside this pad.
LETTER_PAD_NW = (0.00, 0.82, 0.22, 1.00)

_LOC = {
    "northwest": ((0.05, 0.92), "left", "top"),
    "northeast": ((0.95, 0.92), "right", "top"),
    "southwest": ((0.05, 0.06), "left", "bottom"),
    "southeast": ((0.95, 0.06), "right", "bottom"),
    # Above a pitch scale bar; use when NW is occupied by players or hulls.
    "west-lower": ((0.05, 0.20), "left", "bottom"),
}


def apply_rcparams(style: FigureStyle = STYLE) -> None:
    """Set Matplotlib defaults used by every published panel."""
    plt.rcParams.update(
        {
            "font.size": style.fs_tick,
            "axes.labelsize": style.fs_label,
            "xtick.labelsize": style.fs_tick,
            "ytick.labelsize": style.fs_tick,
            "legend.fontsize": style.fs_legend,
            "axes.edgecolor": style.text,
            "axes.labelcolor": style.text,
            "xtick.color": style.text,
            "ytick.color": style.text,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.linewidth": 0.8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def new_figure(
    width: float | None = None,
    height: float = 5.5,
    style: FigureStyle = STYLE,
):
    """Return a new figure with house-style rcParams applied."""
    apply_rcparams(style)
    if width is None:
        width = TEXTWIDTH_IN
    return plt.figure(figsize=(width, height), facecolor="white")


def add_panel_letter(
    ax,
    letter: str,
    loc: str = "northwest",
    note: str = "",
    style: FigureStyle = STYLE,
    xy: tuple[float, float] | None = None,
    ha: str | None = None,
    va: str | None = None,
    fontsize: int | None = None,
    bbox: bool = False,
) -> None:
    """Draw a panel identifier inside the axes, never as a title.

    Default northwest occupies ``LETTER_PAD_NW``. Pass ``xy`` when that
    corner already holds a data label, or pick another ``loc``.
    No white patch unless ``bbox=True``.
    """
    raw = str(letter).strip()
    if not raw.startswith("("):
        raw = f"({raw})"
    txt = raw if not note else f"{raw}  {note}"
    default_xy, default_ha, default_va = _LOC.get(loc.lower(), _LOC["northwest"])
    if xy is None:
        xy = default_xy
    if ha is None:
        ha = default_ha
    if va is None:
        va = default_va
    kw: dict = {}
    if bbox:
        kw["bbox"] = {
            "facecolor": "white",
            "edgecolor": "none",
            "pad": 1.0,
            "alpha": 0.92,
        }
    ax.text(
        xy[0],
        xy[1],
        txt,
        transform=ax.transAxes,
        fontsize=style.fs_annot if fontsize is None else fontsize,
        fontweight="bold",
        color=style.text,
        ha=ha,
        va=va,
        zorder=20,
        clip_on=False,
        **kw,
    )


def style_axes(ax, style: FigureStyle = STYLE) -> None:
    """Tick and spine colour. Does not add a title."""
    ax.tick_params(colors=style.text, labelsize=style.fs_tick)
    for spine in ax.spines.values():
        spine.set_color(style.text)


def ylim_bars_from_zero(ax, y_hi: float) -> None:
    """Non-negative bar summaries start at zero."""
    hi = float(y_hi) if y_hi is not None and y_hi == y_hi and y_hi > 0 else 1.0
    ax.set_ylim(0.0, hi * 1.18)


def export_figure(
    fig,
    pdf_path: Path,
    png_path: Path | None = None,
    style: FigureStyle = STYLE,
    bbox_inches: str | None = None,
) -> None:
    """Write PDF and optional PNG, then close the figure."""
    kw: dict = {"dpi": style.dpi}
    if bbox_inches is not None:
        kw["bbox_inches"] = bbox_inches
    fig.savefig(pdf_path, **kw)
    if png_path is not None:
        fig.savefig(png_path, **kw)
    plt.close(fig)
