"""Run each SQL query repeatedly and record its elapsed time."""

from __future__ import annotations

import argparse
import os
import time
from pathlib import Path

import mysql.connector
from mysql.connector import Error

DEFAULT_QUERY_DIR = Path(__file__).resolve().parents[1] / "sql" / "queries"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "query_timings.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark every .sql file in a query directory."
    )
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
        help=f"timing output file (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="number of timed executions per query (default: 3)",
    )
    parser.add_argument("--host", default=os.getenv("MYSQL_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("MYSQL_PORT", "3306")))
    parser.add_argument("--user", default=os.getenv("MYSQL_USER", "root"))
    parser.add_argument("--password", default=os.getenv("MYSQL_PASSWORD", ""))
    parser.add_argument("--database", default=os.getenv("MYSQL_DATABASE", "csc370"))
    return parser.parse_args()


def load_queries(query_dir: Path) -> list[tuple[str, str]]:
    if not query_dir.is_dir():
        raise FileNotFoundError(f"Query directory not found: {query_dir}")

    queries = []
    for path in sorted(query_dir.glob("*.sql")):
        sql = path.read_text(encoding="utf-8").strip()
        if sql:
            queries.append((path.stem, sql))

    if not queries:
        raise FileNotFoundError(f"No non-empty .sql files found in {query_dir}")
    return queries


def benchmark(
    queries: list[tuple[str, str]], connection: mysql.connector.MySQLConnection, runs: int
) -> list[tuple[str, list[float]]]:
    timings = []
    cursor = connection.cursor()
    try:
        for name, sql in queries:
            query_times = []
            for _ in range(runs):
                start = time.perf_counter_ns()
                cursor.execute(sql)
                cursor.fetchall()
                elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
                query_times.append(elapsed_ms)
            timings.append((name, query_times))
    finally:
        cursor.close()
    return timings


def write_results(output: Path, timings: list[tuple[str, list[float]]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as file:
        file.write("# Wall-clock query time in milliseconds (one value per run)\n")
        for name, query_times in timings:
            values = " ".join(f"{elapsed:.3f}" for elapsed in query_times)
            file.write(f"{name}: {values}\n")


def main() -> int:
    args = parse_args()
    if args.runs < 1:
        raise ValueError("--runs must be at least 1")

    queries = load_queries(args.query_dir)
    connection = None
    try:
        connection = mysql.connector.connect(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password,
            database=args.database,
        )
        timings = benchmark(queries, connection, args.runs)
        write_results(args.output, timings)
    except Error as error:
        raise RuntimeError(f"MySQL benchmark failed: {error}") from error
    finally:
        if connection is not None and connection.is_connected():
            connection.close()

    print(f"Wrote {len(timings)} query timings to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
