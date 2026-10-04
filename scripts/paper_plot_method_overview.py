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
        boxstyle="round,pad=0.008,rounding_size=0.008",
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
            mutation_scale=12,
            linewidth=1.2,
            color="black",
        )
    )


def main() -> None:
    fig, ax = plt.subplots(figsize=(12.0, 5.4))

    fig.subplots_adjust(
        left=0.02,
        right=0.98,
        top=0.97,
        bottom=0.04,
    )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Panel (a)
    ax.text(
        0.02,
        0.96,
        "(a) Memory-write intervention",
        ha="left",
        va="top",
        fontsize=12,
        fontweight="bold",
    )

    box(
        ax,
        0.04,
        0.69,
        0.13,
        0.11,
        "Frame $t$\nnon-conditioning",
    )

    box(
        ax,
        0.22,
        0.67,
        0.16,
        0.15,
        "Frozen SAM 3\npredict first",
        fontsize=10.5,
        linewidth=1.4,
        fontweight="bold",
    )

    box(
        ax,
        0.43,
        0.69,
        0.14,
        0.11,
        "Candidate\nmemory write",
    )

    box(
        ax,
        0.62,
        0.66,
        0.17,
        0.17,
        "ALL-SAFE gate\n"
        r"$s^{frame}_v(t)=\min_o s_v(o,t)$"
        "\n"
        r"admit if $\geq \tau_v$",
        fontsize=9.8,
        linewidth=1.4,
        fontweight="bold",
    )

    box(
        ax,
        0.84,
        0.77,
        0.12,
        0.09,
        "ADMIT\nkeep",
        fontsize=10.0,
        fontweight="bold",
    )

    box(
        ax,
        0.84,
        0.58,
        0.12,
        0.09,
        "BLOCK\npost-yield evict",
        fontsize=9.3,
        fontweight="bold",
    )

    arrow(ax, 0.17, 0.745, 0.22, 0.745)
    arrow(ax, 0.38, 0.745, 0.43, 0.745)
    arrow(ax, 0.57, 0.745, 0.62, 0.745)

    arrow(ax, 0.79, 0.775, 0.84, 0.815)
    arrow(ax, 0.79, 0.705, 0.84, 0.625)

    ax.plot(
        [0.02, 0.98],
        [0.49, 0.49],
        linewidth=0.8,
        color="black",
    )

    # Panel (b)
    ax.text(
        0.02,
        0.455,
        "(b) Signal-family ladder",
        ha="left",
        va="top",
        fontsize=12,
        fontweight="bold",
    )

    box(
        ax,
        0.08,
        0.25,
        0.16,
        0.11,
        "B1\nmanual quality + temporal",
        fontsize=9.5,
    )

    box(
        ax,
        0.30,
        0.23,
        0.17,
        0.15,
        "B2\nquality + temporal\n4,994 params",
        fontsize=9.5,
        linewidth=1.4,
        fontweight="bold",
    )

    box(
        ax,
        0.53,
        0.25,
        0.16,
        0.11,
        "B3-S\n+ self identity",
        fontsize=9.5,
    )

    box(
        ax,
        0.75,
        0.25,
        0.17,
        0.11,
        "B3-R\n+ competitor identity",
        fontsize=9.5,
    )

    arrow(ax, 0.24, 0.305, 0.30, 0.305)
    arrow(ax, 0.47, 0.305, 0.53, 0.305)
    arrow(ax, 0.69, 0.305, 0.75, 0.305)

    box(
        ax,
        0.08,
        0.07,
        0.16,
        0.09,
        "B0\nnative ungated",
        fontsize=9.5,
    )

    box(
        ax,
        0.75,
        0.07,
        0.17,
        0.09,
        "B5\nDMS-lite comparator",
        fontsize=9.3,
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
