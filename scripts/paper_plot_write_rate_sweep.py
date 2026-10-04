#!/usr/bin/env python3

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

# Use embedded TrueType fonts in PDF output; avoid Type 3 fonts.
plt.rcParams["pdf.fonttype"] = 42


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "experiments" / "EXP053_final_test" / "curve_summary.csv"
OUT_DIR = ROOT / "paper" / "cvpr2027" / "figures"
OUT_PDF = OUT_DIR / "write_rate_sweep.pdf"
OUT_PNG = OUT_DIR / "write_rate_sweep.png"

EXPECTED_ROWS = 19
VARIANT_ORDER = ["B1", "B2", "B3_S", "B3_R", "B5"]
DISPLAY_NAME = {
    "B1": "B1",
    "B2": "B2",
    "B3_S": "B3-S",
    "B3_R": "B3-R",
    "B5": "B5",
}


def load_rows() -> list[dict[str, str]]:
    with INPUT.open(newline="", encoding="utf-8") as f:
        rows = [
            row
            for row in csv.DictReader(f)
            if row["scope"] == "HARD_TEST80"
        ]

    assert len(rows) == EXPECTED_ROWS, (
        f"Expected {EXPECTED_ROWS} HARD_TEST80 curve rows, got {len(rows)}"
    )

    for row in rows:
        assert row["variant"] in VARIANT_ORDER, row["variant"]
        assert row["signal_neutral_exact_budget_match"] == "True", row

    return rows


def main() -> None:
    rows = load_rows()
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["variant"]].append(row)

    fig, ax = plt.subplots(figsize=(6.9, 4.15))

    markers = ["o", "s", "^", "D", "v"]

    for marker, variant in zip(markers, VARIANT_ORDER):
        points = sorted(
            grouped[variant],
            key=lambda r: float(r["test_realized_write_rate"]),
        )
        x = [float(r["test_realized_write_rate"]) for r in points]
        y = [float(r["signal_por30"]) for r in points]

        ax.plot(
            x,
            y,
            marker=marker,
            linewidth=1.6,
            markersize=5.2,
            label=DISPLAY_NAME[variant],
        )

        headline = [r for r in points if float(r["target_rate"]) == 0.3]
        assert len(headline) == 1, (variant, headline)
        hx = float(headline[0]["test_realized_write_rate"])
        hy = float(headline[0]["signal_por30"])
        ax.scatter(
            [hx],
            [hy],
            marker=marker,
            s=78,
            facecolors="none",
            edgecolors="black",
            linewidths=1.0,
            zorder=5,
        )

    ax.set_xlabel("Realized TEST physical write rate")
    ax.set_ylabel("POR@30")
    ax.set_xlim(0.03, 0.45)
    ax.set_ylim(0.715, 0.772)
    ax.grid(True, linewidth=0.4, alpha=0.35)
    ax.legend(
        frameon=False,
        ncol=5,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.01),
        columnspacing=1.1,
        handletextpad=0.4,
    )

    ax.text(
        0.99,
        0.03,
        "Open markers: frozen headline operating points",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=8,
    )

    fig.tight_layout()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PDF, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"INPUT={INPUT}")
    print(f"ROWS={len(rows)}")
    print(f"PDF={OUT_PDF}")
    print(f"PNG={OUT_PNG}")


if __name__ == "__main__":
    main()
