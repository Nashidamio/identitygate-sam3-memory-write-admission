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
    fontsize: float = 9.0,
    linewidth: float = 1.1,
    linestyle: str = "-",
    fontweight: str = "normal",
) -> None:
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.010",
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
        fontweight=fontweight,
        linespacing=1.15,
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
    mutation_scale: float = 11.0,
    rad: float = 0.0,
    label_y: float | None = None,
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

    if label is not None:
        y = (y1 + y2) / 2 if label_y is None else label_y
        ax.text(
            (x1 + x2) / 2,
            y,
            label,
            ha="center",
            va="center",
            fontsize=8.3,
        )


def main() -> None:
    fig, ax = plt.subplots(figsize=(11.0, 7.0))
    fig.subplots_adjust(
        left=0.02,
        right=0.98,
        top=0.98,
        bottom=0.03,
    )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # ------------------------------------------------------------------
    # Panel (a): physical closed-loop intervention.
    # ------------------------------------------------------------------
    ax.text(
        0.015,
        0.975,
        "(a) Closed-loop physical memory-write intervention",
        ha="left",
        va="top",
        fontsize=12,
        fontweight="bold",
    )

    box(
        ax,
        0.025,
        0.735,
        0.105,
        0.095,
        "Frame t\nnon-conditioning",
        fontsize=9.3,
    )

    box(
        ax,
        0.165,
        0.700,
        0.145,
        0.165,
        "Frozen SAM 3\nVOS/PVS\n\nprediction first",
        fontsize=10,
        linewidth=1.4,
        fontweight="bold",
    )

    box(
        ax,
        0.355,
        0.785,
        0.145,
        0.085,
        "Current prediction\nalready produced",
        fontsize=9.3,
    )

    box(
        ax,
        0.355,
        0.655,
        0.145,
        0.085,
        "Candidate\nnon-cond write",
        fontsize=9.3,
    )

    box(
        ax,
        0.545,
        0.675,
        0.185,
        0.190,
        "Policy score\n"
        r"$s_v(o,t)$"
        "\n\nALL-SAFE\n"
        r"$s^{frame}_v(t)=\min_o s_v(o,t)$"
        "\n"
        r"ADMIT iff $s^{frame}_v(t)\geq\tau_v$",
        fontsize=9.0,
        linewidth=1.4,
    )

    box(
        ax,
        0.775,
        0.800,
        0.095,
        0.075,
        "ADMIT\nkeep write",
        fontsize=9.0,
        fontweight="bold",
    )

    box(
        ax,
        0.890,
        0.775,
        0.090,
        0.100,
        "BLOCK\npost-yield\neviction",
        fontsize=8.7,
        fontweight="bold",
    )

    box(
        ax,
        0.805,
        0.605,
        0.155,
        0.085,
        "Propagation at t+1\nuses resulting memory",
        fontsize=9.0,
    )

    arrow(ax, 0.130, 0.782, 0.165, 0.782)

    arrow(
        ax,
        0.310,
        0.805,
        0.355,
        0.827,
    )

    arrow(
        ax,
        0.310,
        0.755,
        0.355,
        0.697,
    )

    arrow(
        ax,
        0.500,
        0.697,
        0.545,
        0.735,
        label="causal signals",
        label_y=0.750,
    )

    arrow(
        ax,
        0.730,
        0.800,
        0.775,
        0.837,
    )

    arrow(
        ax,
        0.730,
        0.730,
        0.890,
        0.825,
    )

    arrow(
        ax,
        0.822,
        0.800,
        0.850,
        0.690,
    )

    arrow(
        ax,
        0.935,
        0.775,
        0.915,
        0.690,
    )

    box(
        ax,
        0.175,
        0.505,
        0.565,
        0.080,
        "Current-frame prediction is preserved; admission changes only future memory.\n"
        "Prompt and conditioning frames are always retained.",
        fontsize=9.2,
        linewidth=0.9,
    )

    ax.plot(
        [0.015, 0.985],
        [0.445, 0.445],
        linewidth=0.9,
        color="black",
    )

    # ------------------------------------------------------------------
    # Panel (b): frozen signal-family comparison.
    # ------------------------------------------------------------------
    ax.text(
        0.015,
        0.420,
        "(b) Frozen signal-family comparison",
        ha="left",
        va="top",
        fontsize=12,
        fontweight="bold",
    )

    box(
        ax,
        0.030,
        0.245,
        0.190,
        0.125,
        "B1\nmanual quality-temporal\n0 learned params",
        fontsize=9.2,
    )

    box(
        ax,
        0.265,
        0.235,
        0.190,
        0.145,
        "B2\nlearned quality-temporal\n5 causal features\n4,994 learned params",
        fontsize=9.2,
        linewidth=1.4,
        fontweight="bold",
    )

    box(
        ax,
        0.500,
        0.235,
        0.190,
        0.145,
        "B3-S\nB2 + self identity\n"
        r"$ptr\_sim\_anchor\_fp32$",
        fontsize=9.2,
    )

    box(
        ax,
        0.735,
        0.235,
        0.220,
        0.145,
        "B3-R\nB3-S + competitor identity\n"
        r"$max\_comp\_anchor\_cos\_fp32$",
        fontsize=8.9,
    )

    arrow(
        ax,
        0.455,
        0.307,
        0.500,
        0.307,
        label="+ self identity",
        label_y=0.393,
    )

    arrow(
        ax,
        0.690,
        0.307,
        0.735,
        0.307,
        label="+ competitor identity",
        label_y=0.393,
    )

    arrow(
        ax,
        0.845,
        0.215,
        0.595,
        0.215,
        linestyle="--",
        rad=-0.04,
    )

    arrow(
        ax,
        0.595,
        0.190,
        0.360,
        0.190,
        linestyle="--",
        rad=-0.04,
    )

    ax.text(
        0.605,
        0.165,
        "Missing identity fallback: B3-R -> B3-S -> B2",
        ha="center",
        va="center",
        fontsize=9.1,
        fontweight="bold",
    )

    box(
        ax,
        0.035,
        0.045,
        0.190,
        0.085,
        "B0\nnative reference\nungated writes",
        fontsize=9.0,
    )

    box(
        ax,
        0.765,
        0.035,
        0.205,
        0.105,
        "B5\nDMS-lite comparator\n0 learned params\nnot exact SAM3-DMS",
        fontsize=8.7,
        linestyle="--",
    )

    box(
        ax,
        0.270,
        0.040,
        0.450,
        0.095,
        "pointer_valid: availability mask only, never a predictive numeric feature.\n"
        "All gated variants use the same ALL-SAFE physical write intervention.",
        fontsize=8.9,
        linewidth=0.9,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    fig.savefig(
        OUT_PDF,
        bbox_inches="tight",
        pad_inches=0.08,
    )
    fig.savefig(
        OUT_PNG,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.08,
    )

    plt.close(fig)

    print(f"PDF={OUT_PDF}")
    print(f"PNG={OUT_PNG}")


if __name__ == "__main__":
    main()
