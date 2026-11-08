"""Plot benchmark timings and optionally compare them with a previous sprint."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "query_timings.png"


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot query benchmark timings.")
    parser.add_argument("current", type=Path, help="current benchmark CSV or text output")
    parser.add_argument("--baseline", type=Path, help="previous sprint CSV or text output")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    current = read_timings(args.current)
    baseline = read_timings(args.baseline) if args.baseline else {}
    names = sorted(set(current) | set(baseline))
    positions = range(len(names))
    width = 0.8 if not baseline else 0.38

    figure, axis = plt.subplots(figsize=(max(12, len(names) * 0.55), 7))
    if baseline:
        axis.bar([position - width / 2 for position in positions],
                 [baseline.get(name, 0) for name in names], width, label="Baseline")
        axis.bar([position + width / 2 for position in positions],
                 [current.get(name, 0) for name in names], width, label="Current")
    else:
        axis.bar(positions, [current.get(name, 0) for name in names], width, label="Current")
    axis.set_title("Query execution time by implementation")
    axis.set_ylabel("Average wall-clock time (ms)")
    axis.set_xlabel("Query")
    axis.set_xticks(list(positions), names, rotation=70, ha="right")
    axis.grid(axis="y", alpha=0.25)
    axis.legend()
    figure.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(args.output, dpi=180)
    print(f"Wrote visualization to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
