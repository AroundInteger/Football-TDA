#!/usr/bin/env python3
"""Interactive layout editor for Figure~1 panels (a) and (b).

Drag coloured handles to place $P(t)$ clusters, $\\tilde P(t)$ centroids,
and text annotations.  Panel~(b) updates live from the left-slot positions.

Usage:
    python3 pipeline/steps/00_pipeline_figure_layout_editor.py

Keys:
    s  — save layout to pipeline/config/fig1_layout.yaml
    e  — export full four-panel figure (PDF/PNG)
    q  — quit

Requires an interactive Matplotlib backend (the default on macOS is fine).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from fig1_layout import CLUSTER_NAMES, LAYOUT_PATH, load_layout  # noqa: E402

_FIG_MOD_PATH = Path(__file__).resolve().parent / "00_pipeline_figure.py"
_spec = importlib.util.spec_from_file_location("pipeline_figure1", _FIG_MOD_PATH)
_fig1 = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_fig1)

HANDLE_COLOURS = _fig1.CLUSTER_PALETTE[:4]
FONT_PT = _fig1.FONT_PT


class _DragTarget:
    __slots__ = ("kind", "index", "artist")

    def __init__(self, kind: str, index: int | None, artist):
        self.kind = kind
        self.index = index
        self.artist = artist


class Fig1LayoutEditor:
    """Two-panel preview with draggable layout handles."""

    PANEL_A_KINDS = frozenset({
        "left", "right", "label_pt", "label_pt_tilde", "label_delta", "label_lt_delta",
    })
    PANEL_B_KINDS = frozenset({"label_pt_tilde_b", "eps_label"})

    def __init__(self) -> None:
        self.layout = load_layout()
        self._pts, self._labels, self._cents, _, _ = _fig1._schematic_clustering_layout(self.layout)
        self._colours = _fig1._cluster_colours(len(np.unique(self._labels)))
        d = np.linalg.norm(self._cents[:, None, :] - self._cents[None, :, :], axis=2)
        iu = np.triu_indices(len(self._cents), k=1)
        self._eps = float(np.percentile(d[iu], 60)) if len(self._cents) > 1 else 8.0

        self.fig = plt.figure(figsize=(11.5, 6.2))
        try:
            self.fig.canvas.manager.set_window_title("Figure 1 layout editor")
        except AttributeError:
            pass
        self.ax_a = self.fig.add_axes([0.06, 0.22, 0.40, 0.68])
        self.ax_b = self.fig.add_axes([0.54, 0.22, 0.40, 0.68])

        self._targets: list[_DragTarget] = []
        self._active: _DragTarget | None = None
        self._overlay_artists: list = []

        self._build_widgets()
        self._redraw()
        self._connect()

    def _build_widgets(self) -> None:
        ax_dr = self.fig.add_axes([0.12, 0.10, 0.30, 0.03])
        ax_ls = self.fig.add_axes([0.12, 0.05, 0.30, 0.03])
        ax_save = self.fig.add_axes([0.58, 0.06, 0.12, 0.05])
        ax_export = self.fig.add_axes([0.72, 0.06, 0.12, 0.05])

        self._slider_delta_r = Slider(
            ax_dr, r"$\delta$ radius", 0.04, 0.14,
            valinit=self.layout.delta_r, valstep=0.002,
        )
        self._slider_local = Slider(
            ax_ls, "point spread", 0.010, 0.060,
            valinit=self.layout.local_scale, valstep=0.002,
        )
        self._slider_delta_r.on_changed(self._on_slider)
        self._slider_local.on_changed(self._on_slider)

        Button(ax_save, "Save YAML").on_clicked(lambda _evt: self._save())
        Button(ax_export, "Export PDF").on_clicked(lambda _evt: self._export())

        self.fig.text(
            0.06, 0.16,
            "Drag coloured squares = $P(t)$ clusters (panel b follows).  "
            "Diamonds = $\\tilde P(t)$.  Gold = text labels.",
            fontsize=9, color="#444444",
        )
        self.fig.text(
            0.06, 0.01,
            f"Layout file: {LAYOUT_PATH}   |   Keys: s save, e export, q quit",
            fontsize=8, color="#666666",
        )

    def _connect(self) -> None:
        canvas = self.fig.canvas
        canvas.mpl_connect("button_press_event", self._on_press)
        canvas.mpl_connect("motion_notify_event", self._on_motion)
        canvas.mpl_connect("button_release_event", self._on_release)
        canvas.mpl_connect("key_press_event", self._on_key)

    def _on_slider(self, _val) -> None:
        self.layout.delta_r = float(self._slider_delta_r.val)
        self.layout.local_scale = float(self._slider_local.val)
        self._redraw()

    def _on_key(self, event) -> None:
        if event.key == "s":
            self._save()
        elif event.key == "e":
            self._export()
        elif event.key == "q":
            plt.close(self.fig)

    def _save(self) -> None:
        path = self.layout.save()
        print(f"Saved layout → {path}")

    def _export(self) -> None:
        self.layout.save()
        out = _fig1.render_figure(self.layout)
        print(f"Exported full figure → {out}")

    def _clear_overlays(self) -> None:
        for art in self._overlay_artists:
            art.remove()
        self._overlay_artists.clear()
        self._targets.clear()

    def _axis_for(self, kind: str):
        return self.ax_b if kind in self.PANEL_B_KINDS else self.ax_a

    def _add_handle(
        self,
        kind: str,
        xy: list[float],
        *,
        index: int | None = None,
        marker: str = "s",
        size: float = 90,
        colour: str = "#FFD600",
        label: str | None = None,
    ) -> None:
        ax = self._axis_for(kind)

        if kind.startswith("label") or kind == "eps_label":
            txt = ax.text(
                xy[0], xy[1], label or kind,
                fontsize=FONT_PT - 1, color=colour,
                ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFDE7", edgecolor=colour, alpha=0.9),
                picker=True, zorder=20,
            )
            self._overlay_artists.append(txt)
            self._targets.append(_DragTarget(kind, index, txt))
            return

        sc = ax.scatter(
            [xy[0]], [xy[1]], s=size, marker=marker,
            facecolors=colour, edgecolors="white", linewidths=1.2,
            picker=5, zorder=20, alpha=0.85,
        )
        self._overlay_artists.append(sc)
        self._targets.append(_DragTarget(kind, index, sc))
        if label:
            ann = ax.text(
                xy[0], xy[1] + 0.055, label,
                fontsize=7, ha="center", va="bottom", color=colour, zorder=21,
            )
            self._overlay_artists.append(ann)

    def _bracket_label_xy(self) -> list[float]:
        i, j = self.layout.delta_bracket
        mid = (np.array(self.layout.left_slots[i]) + np.array(self.layout.left_slots[j])) / 2
        off = np.array(self.layout.delta_bracket_label_offset)
        return (mid + off).tolist()

    def _eps_label_xy(self) -> list[float]:
        mapped, shift = _fig1._filtration_positions(self.layout)
        if self.layout.eps_label_pos is not None:
            return (np.asarray(self.layout.eps_label_pos) + shift).tolist()
        return mapped[self.layout.eps_label_index].tolist()

    def _redraw(self) -> None:
        self.ax_a.clear()
        self.ax_b.clear()
        _fig1._panel_clustering(self.ax_a, self._pts, self._labels, self._colours, self.layout)
        _fig1._panel_filtration(
            self.ax_b, self._cents, self._labels, self._colours, self._eps, self.layout,
        )
        self.ax_a.set_title(r"(a) Clustering — drag handles to edit", fontsize=FONT_PT)
        self.ax_b.set_title(r"(b) Filtration — auto from left slots", fontsize=FONT_PT)

        self._clear_overlays()

        for i, (name, colour) in enumerate(zip(CLUSTER_NAMES, HANDLE_COLOURS)):
            self._add_handle(
                "left", self.layout.left_slots[i], index=i,
                marker="s", colour=colour, label=f"{name[0].upper()} $P(t)$",
            )
            self._add_handle(
                "right", self.layout.right_slots[i], index=i,
                marker="D", colour=colour, size=70, label=f"{name[0].upper()} $\\tilde P$",
            )

        self._add_handle("label_pt", self.layout.label_pt, label=r"$P(\tilde{t})$", colour="#F9A825")
        self._add_handle(
            "label_pt_tilde", self.layout.label_pt_tilde, label=r"$\tilde{P}(\tilde{t})$", colour="#F9A825",
        )
        self._add_handle(
            "label_lt_delta", self._bracket_label_xy(), label=r"$<\delta$", colour="#757575",
        )
        self._add_handle(
            "label_pt_tilde_b", self.layout.label_pt_tilde_b,
            label=r"$\tilde{P}(\tilde{t})$ b", colour="#F9A825",
        )
        self._add_handle(
            "eps_label", self._eps_label_xy(), label=r"$\varepsilon_{\max}$", colour="#E65100",
        )

        self.fig.canvas.draw_idle()

    def _pick_target(self, event) -> _DragTarget | None:
        if event.inaxes not in (self.ax_a, self.ax_b):
            return None
        for target in reversed(self._targets):
            if target.artist.contains(event)[0]:
                return target
        return None

    def _set_xy(self, target: _DragTarget, x: float, y: float) -> None:
        x = float(np.clip(x, 0.02, 0.98))
        y = float(np.clip(y, 0.02, 0.98))
        kind, idx = target.kind, target.index

        if kind == "left" and idx is not None:
            self.layout.left_slots[idx] = [x, y]
        elif kind == "right" and idx is not None:
            self.layout.right_slots[idx] = [x, y]
        elif kind == "label_pt":
            self.layout.label_pt = [x, y]
        elif kind == "label_pt_tilde":
            self.layout.label_pt_tilde = [x, y]
        elif kind == "label_pt_tilde_b":
            self.layout.label_pt_tilde_b = [x, y]
        elif kind == "eps_label":
            self.layout.eps_label_pos = [x, y]
        elif kind == "label_lt_delta":
            i, j = self.layout.delta_bracket
            mid = (np.array(self.layout.left_slots[i]) + np.array(self.layout.left_slots[j])) / 2
            self.layout.delta_bracket_label_offset = (np.array([x, y]) - mid).tolist()

    def _on_press(self, event) -> None:
        self._active = self._pick_target(event)

    def _on_motion(self, event) -> None:
        if self._active is None or event.xdata is None or event.ydata is None:
            return
        if event.inaxes not in (self.ax_a, self.ax_b):
            return
        self._set_xy(self._active, event.xdata, event.ydata)
        self._redraw()

    def _on_release(self, _event) -> None:
        self._active = None

    def run(self) -> None:
        plt.show()


def main() -> None:
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": FONT_PT,
        "mathtext.fontset": "dejavuserif",
    })
    Fig1LayoutEditor().run()


if __name__ == "__main__":
    main()
