"""Plot benchmark timings and optionally compare them with a previous sprint."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import matplotlib.pyplot as plt

from .paths import RESULTS_DIR

DEFAULT_CURRENT = RESULTS_DIR / "query_timings.csv"
DEFAULT_OUTPUT = RESULTS_DIR / "query_timings.png"


def read_timings(path: Path) -> dict[str, float]:
    """Read structured CSV timings or the legacy ``name: values`` text format."""
    if path.suffix.lower() == ".csv":
        values: dict[str, list[float]] = {}
        with path.open(newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                values.setdefault(row["query"], []).append(float(row["elapsed_ms"]))
        return {name: sum(times) / len(times) for name, times in values.items()}

    pattern = re.compile(r"^([^:#]+):\s+(.+?)(?:\s+Average:\s+([\d.]+))?$")
    timings = {}
    with path.open(encoding="utf-8") as file:
        for line in file:
            match = pattern.match(line.strip())
            if not match:
                continue
            name, raw_values, average = match.groups()
            numbers = []
            for value in raw_values.split():
                if not re.fullmatch(r"\d+(?:\.\d+)?", value):
                    continue
                numbers.append(float(value))
            if numbers:
                timings[name.strip()] = float(average) if average else sum(numbers) / len(numbers)
    if not timings:
        raise ValueError(f"No timing rows found in {path}")
    return timings


def query_sort_key(name: str) -> tuple[int, str]:
    """Keep numbered queries in numeric order."""
    match = re.match(r"^(\d+)", name)
    return (int(match.group(1)) if match else float("inf"), name)


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "current", type=Path, nargs="?", default=DEFAULT_CURRENT,
        help=f"current benchmark CSV (default: {DEFAULT_CURRENT})",
    )
    parser.add_argument("--baseline", type=Path, help="previous sprint benchmark CSV")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)


def run(args: argparse.Namespace) -> int:
    current = read_timings(args.current)
    baseline = read_timings(args.baseline) if args.baseline else {}
    if baseline:
        names = sorted(set(current) | set(baseline), key=query_sort_key)
        columns = min(4, max(1, len(names)))
        rows = (len(names) + columns - 1) // columns
        figure, axes = plt.subplots(
            rows,
            columns,
            figsize=(columns * 4, rows * 3.5),
            squeeze=False,
            sharey=False,
        )
        for index, name in enumerate(names):
            axis = axes[index // columns, index % columns]
            values = [baseline.get(name), current.get(name)]
            labels = ["Baseline", "Current"]
            available_values = [value for value in values if value is not None]
            available_labels = [
                label for label, value in zip(labels, values) if value is not None
            ]
            available_colors = [
                color
                for color, value in zip(["#4c72b0", "#dd8452"], values)
                if value is not None
            ]
            axis.bar(available_labels, available_values, color=available_colors)
            axis.set_title(name)
            axis.set_ylabel("Time (ms)")
            axis.tick_params(axis="x", labelrotation=25)
            axis.grid(axis="y", alpha=0.25)

        for index in range(len(names), rows * columns):
            axes[index // columns, index % columns].set_visible(False)
    else:
        names = sorted(current, key=query_sort_key)
        columns = min(4, max(1, len(names)))
        rows = (len(names) + columns - 1) // columns
        figure, axes = plt.subplots(
            rows,
            columns,
            figsize=(columns * 4, rows * 3.5),
            squeeze=False,
            sharey=False,
        )
        for index, name in enumerate(names):
            axis = axes[index // columns, index % columns]
            axis.bar(["Current"], [current[name]], color="#dd8452")
            axis.set_title(name)
            axis.set_ylabel("Time (ms)")
            axis.grid(axis="y", alpha=0.25)

        for index in range(len(names), rows * columns):
            axes[index // columns, index % columns].set_visible(False)

    figure.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(args.output, dpi=180)
    print(f"Wrote visualization to {args.output}")
    return 0

