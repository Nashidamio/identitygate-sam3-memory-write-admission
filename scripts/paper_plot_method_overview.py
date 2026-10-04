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
    fontsize: float = 10.0,
    linewidth: float = 1.1,
    fontweight: str = "normal",
) -> None:
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.010,rounding_size=0.010",
        facecolor="white",
        edgecolor="black",
        linewidth=linewidth,
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
        linespacing=1.10,
    )


def arrow(
    ax,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
) -> None:
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            mutation_scale=13,
            linewidth=1.2,
            color="black",
        )
    )


def setup_axis(ax) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")


def draw_intervention(ax) -> None:
    setup_axis(ax)

    ax.text(
        0.01,
        0.97,
        "(a) Memory-write intervention",
        ha="left",
        va="top",
        fontsize=12,
        fontweight="bold",
    )

    box(
        ax,
        0.03,
        0.43,
        0.13,
        0.22,
        "Frame $t$\nnon-conditioning",
        fontsize=10.0,
    )

    box(
        ax,
        0.21,
        0.40,
        0.16,
        0.28,
        "Frozen SAM 3\npredict first",
        fontsize=10.8,
        linewidth=1.4,
        fontweight="bold",
    )

    box(
        ax,
        0.42,
        0.43,
        0.14,
        0.22,
        "Candidate\nmemory write",
        fontsize=10.2,
    )

    box(
        ax,
        0.61,
        0.37,
        0.17,
        0.34,
        "ALL-SAFE gate\n\n"
        r"$s^{frame}_v(t)=\min_o s_v(o,t)$"
        "\n"
        r"admit if $\geq\tau_v$",
        fontsize=10.0,
        linewidth=1.4,
        fontweight="bold",
    )

    box(
        ax,
        0.84,
        0.65,
        0.13,
        0.20,
        "ADMIT\nkeep",
        fontsize=10.4,
        fontweight="bold",
    )

    box(
        ax,
        0.84,
        0.22,
        0.13,
        0.20,
        "BLOCK\nevict",
        fontsize=10.4,
        fontweight="bold",
    )

    arrow(ax, 0.16, 0.54, 0.21, 0.54)
    arrow(ax, 0.37, 0.54, 0.42, 0.54)
    arrow(ax, 0.56, 0.54, 0.61, 0.54)

    arrow(ax, 0.78, 0.61, 0.84, 0.75)
    arrow(ax, 0.78, 0.47, 0.84, 0.32)


def draw_signal_ladder(ax) -> None:
    setup_axis(ax)

    ax.text(
        0.01,
        0.97,
        "(b) Signal-family ladder",
        ha="left",
        va="top",
        fontsize=12,
        fontweight="bold",
    )

    box(
        ax,
        0.07,
        0.48,
        0.17,
        0.24,
        "B1\nmanual quality\n+ temporal",
        fontsize=10.0,
    )

    box(
        ax,
        0.30,
        0.44,
        0.17,
        0.32,
        "B2\nquality + temporal\n4,994 params",
        fontsize=10.0,
        linewidth=1.4,
        fontweight="bold",
    )

    box(
        ax,
        0.53,
        0.48,
        0.17,
        0.24,
        "B3-S\n+ self identity",
        fontsize=10.0,
    )

    box(
        ax,
        0.76,
        0.48,
        0.17,
        0.24,
        "B3-R\n+ competitor\nidentity",
        fontsize=10.0,
    )

    arrow(ax, 0.24, 0.60, 0.30, 0.60)
    arrow(ax, 0.47, 0.60, 0.53, 0.60)
    arrow(ax, 0.70, 0.60, 0.76, 0.60)

    box(
        ax,
        0.07,
        0.10,
        0.17,
        0.19,
        "B0\nnative ungated",
        fontsize=10.0,
    )

    box(
        ax,
        0.76,
        0.10,
        0.17,
        0.19,
        "B5\nDMS-lite\ncomparator",
        fontsize=10.0,
    )


def main() -> None:
    fig, (ax1, ax2) = plt.subplots(
        2,
        1,
        figsize=(10.8, 7.6),
    )

    fig.subplots_adjust(
        left=0.04,
        right=0.98,
        top=0.97,
        bottom=0.05,
        hspace=0.22,
    )

    draw_intervention(ax1)
    draw_signal_ladder(ax2)

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
