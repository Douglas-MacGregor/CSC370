"""Run each SQL query repeatedly and record its elapsed time as CSV."""

from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

import mysql.connector
from mysql.connector import Error

from .db import add_mysql_args, connect
from .paths import QUERIES_DIR, RESULTS_DIR

DEFAULT_QUERY_DIR = QUERIES_DIR
DEFAULT_OUTPUT = RESULTS_DIR / "query_timings.csv"


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--query-dir",
        type=Path,
        default=DEFAULT_QUERY_DIR,
        help=f"directory containing .sql files (default: {DEFAULT_QUERY_DIR})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"CSV timing output file (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="number of timed executions per query (default: 3)",
    )
    add_mysql_args(parser)


def load_queries(query_dir: Path) -> list[tuple[str, str]]:
    if not query_dir.is_dir():
        raise FileNotFoundError(f"Query directory not found: {query_dir}")

    queries = []
    for path in sorted(query_dir.glob("*.sql")):
        sql = "\n".join(
            line
            for line in path.read_text(encoding="utf-8").splitlines()
            if not line.lstrip().startswith("--")
        ).strip().rstrip(";").strip()
        if sql:
            queries.append((path.stem, sql))

    if not queries:
        raise FileNotFoundError(f"No non-empty .sql files found in {query_dir}")
    return queries


def benchmark(
    queries: list[tuple[str, str]], connection: mysql.connector.MySQLConnection, runs: int
) -> list[tuple[str, list[float]]]:
    timings = []
    cursor = connection.cursor(buffered=True)
    try:
        for name, sql in queries:
            query_times = []
            for run in range(1, runs + 1):
                start = time.perf_counter_ns()
                try:
                    cursor.execute(sql)
                    cursor.fetchall()
                except Error as error:
                    raise RuntimeError(
                        f"Query {name!r} failed on run {run}: {error}"
                    ) from error
                elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
                query_times.append(elapsed_ms)
            timings.append((name, query_times))
    finally:
        cursor.close()
    return timings


def write_results(output: Path, timings: list[tuple[str, list[float]]]) -> None:
    """Write one CSV row per query execution for analysis and visualization."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(("query", "run", "elapsed_ms"))
        for name, query_times in timings:
            for run, elapsed_ms in enumerate(query_times, start=1):
                writer.writerow((name, run, f"{elapsed_ms:.3f}"))


def run(args: argparse.Namespace) -> int:
    if args.runs < 1:
        raise ValueError("--runs must be at least 1")

    queries = load_queries(args.query_dir)
    connection = None
    try:
        connection = connect(args, use_pure=True)
        timings = benchmark(queries, connection, args.runs)
        write_results(args.output, timings)
    except Error as error:
        raise RuntimeError(f"MySQL benchmark failed: {error}") from error
    finally:
        if connection is not None and connection.is_connected():
            connection.close()

    print(f"Wrote {len(timings)} query timings to {args.output}")
    return 0

