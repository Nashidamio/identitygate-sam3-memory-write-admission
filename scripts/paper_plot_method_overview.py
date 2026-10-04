#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "paper" / "cvpr2027" / "figures"
OUT_PDF = OUT_DIR / "method_overview.pdf"
OUT_PNG = OUT_DIR / "method_overview.png"


def box(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    *,
    fontsize: float = 8.5,
    linewidth: float = 1.1,
    linestyle: str = "-",
) -> None:
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.012",
        facecolor="white",
        edgecolor="black",
        linewidth=linewidth,
        linestyle=linestyle,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
    )


def arrow(
    ax,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    label: str | None = None,
    linestyle: str = "-",
    linewidth: float = 1.1,
    mutation_scale: float = 10.0,
    rad: float = 0.0,
    label_dx: float = 0.0,
    label_dy: float = 0.0,
) -> None:
    patch = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle="-|>",
        mutation_scale=mutation_scale,
        linewidth=linewidth,
        linestyle=linestyle,
        color="black",
        connectionstyle=f"arc3,rad={rad}",
    )
    ax.add_patch(patch)
    if label:
        ax.text(
            (x1 + x2) / 2 + label_dx,
            (y1 + y2) / 2 + label_dy,
            label,
            ha="center",
            va="center",
            fontsize=7.5,
        )


def main() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 5.25))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.01,
        0.975,
        "(a) Closed-loop physical memory-write intervention",
        ha="left",
        va="top",
        fontsize=10,
        fontweight="bold",
    )

    box(
        ax,
        0.025,
        0.735,
        0.12,
        0.105,
        "Frame t\nnon-conditioning",
    )
    box(
        ax,
        0.19,
        0.70,
        0.17,
        0.175,
        "Frozen SAM 3\nVOS/PVS\n\nprediction first",
        fontsize=9,
        linewidth=1.4,
    )
    box(
        ax,
        0.405,
        0.795,
        0.16,
        0.095,
        "Current-frame\nprediction\npreserved",
    )
    box(
        ax,
        0.405,
        0.655,
        0.16,
        0.095,
        "Native candidate\nnon-cond memory",
    )
    box(
        ax,
        0.615,
        0.68,
        0.18,
        0.17,
        "Policy score\n$s_v(o,t)$\n\nALL-SAFE\n"
        "$s^{frame}_v(t)=\\min_o s_v(o,t)$\n"
        "ADMIT iff $\\geq \\tau_v$",
        fontsize=8,
        linewidth=1.4,
    )
    box(
        ax,
        0.845,
        0.785,
        0.125,
        0.09,
        "ADMIT\nleave native\nstate unchanged",
        fontsize=8,
    )
    box(
        ax,
        0.845,
        0.625,
        0.125,
        0.12,
        "BLOCK\npost-yield eviction\n"
        "global + per-object\nnon-cond memory",
        fontsize=7.6,
    )
    box(
        ax,
        0.79,
        0.49,
        0.18,
        0.075,
        "Propagation at t+1\nuses resulting memory",
        fontsize=8,
    )

    arrow(ax, 0.145, 0.787, 0.19, 0.787)
    arrow(ax, 0.36, 0.80, 0.405, 0.842)
    arrow(ax, 0.36, 0.765, 0.405, 0.702)
    arrow(
        ax,
        0.565,
        0.72,
        0.615,
        0.745,
        label="causal signals",
        label_dy=0.025,
    )
    arrow(ax, 0.795, 0.785, 0.845, 0.83, label="ADMIT", label_dy=0.025)
    arrow(ax, 0.795, 0.735, 0.845, 0.685, label="BLOCK", label_dy=-0.025)
    arrow(ax, 0.91, 0.785, 0.90, 0.565)
    arrow(ax, 0.91, 0.625, 0.90, 0.565)

    ax.text(
        0.405,
        0.61,
        "Prompt / conditioning frames are always retained.",
        ha="left",
        va="center",
        fontsize=7.7,
    )
    ax.text(
        0.405,
        0.575,
        "Gate decision changes future memory, not the already-produced prediction.",
        ha="left",
        va="center",
        fontsize=7.7,
    )

    ax.plot([0.015, 0.985], [0.45, 0.45], linewidth=0.8, color="black")

    ax.text(
        0.01,
        0.425,
        "(b) Frozen signal-family comparison",
        ha="left",
        va="top",
        fontsize=10,
        fontweight="bold",
    )

    box(
        ax,
        0.025,
        0.245,
        0.13,
        0.105,
        "B0\nnative reference\nungated writes",
        fontsize=8,
    )
    box(
        ax,
        0.19,
        0.245,
        0.15,
        0.105,
        "B1\nmanual\nquality-temporal\n0 learned params",
        fontsize=7.8,
    )
    box(
        ax,
        0.385,
        0.225,
        0.17,
        0.145,
        "B2\nlearned\nquality-temporal\n5 causal features\n4,994 params",
        fontsize=7.8,
        linewidth=1.4,
    )
    box(
        ax,
        0.605,
        0.225,
        0.15,
        0.145,
        "B3-S\nB2 + self identity\n"
        "ptr similarity\nFP32 cosine",
        fontsize=7.8,
    )
    box(
        ax,
        0.805,
        0.225,
        0.165,
        0.145,
        "B3-R\nB3-S + competitor\n"
        "anchor similarity\nFP32 cosine",
        fontsize=7.7,
    )
    box(
        ax,
        0.385,
        0.055,
        0.17,
        0.10,
        "B5\nDMS-lite comparator\n0 learned params\nsame intervention",
        fontsize=7.7,
        linestyle="--",
    )

    arrow(
        ax,
        0.555,
        0.297,
        0.605,
        0.297,
        label="+ self pointer",
        label_dy=0.032,
    )
    arrow(
        ax,
        0.755,
        0.297,
        0.805,
        0.297,
        label="+ competitor pointer",
        label_dy=0.032,
    )

    arrow(
        ax,
        0.875,
        0.39,
        0.68,
        0.39,
        label="missing competitor identity",
        linestyle="--",
        rad=0.08,
        label_dy=0.028,
    )
    arrow(
        ax,
        0.68,
        0.405,
        0.47,
        0.405,
        label="missing self identity",
        linestyle="--",
        rad=0.06,
        label_dy=0.025,
    )

    ax.text(
        0.785,
        0.095,
        "pointer_valid = availability mask only\n"
        "not a predictive numeric feature",
        ha="center",
        va="center",
        fontsize=7.6,
    )

    ax.text(
        0.19,
        0.18,
        "B1, B2, B3-S, B3-R, and B5 all drive the same frame-level\n"
        "ALL-SAFE physical write intervention shown above.",
        ha="left",
        va="center",
        fontsize=7.7,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PDF, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"PDF={OUT_PDF}")
    print(f"PNG={OUT_PNG}")


if __name__ == "__main__":
    main()
