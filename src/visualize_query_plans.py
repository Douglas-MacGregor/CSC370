"""Collect and visualize the EXPLAIN plans described by the analysis SQL files."""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path

import matplotlib.pyplot as plt
import mysql.connector
from mysql.connector import Error

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "docs" / "query_plan_explain.csv"
DEFAULT_PNG = ROOT / "docs" / "query_plan_explain.png"

SUBQUERY_SQL = """
SELECT machine_id
FROM Hosts
WHERE model_id = 1
    AND machine_id IN (
        SELECT machine_id
        FROM Hosts
        WHERE model_id = 2
    )
"""

JOIN_SQL = """
SELECT h1.machine_id
FROM Hosts AS h1
JOIN Hosts AS h2 ON h1.machine_id = h2.machine_id
WHERE h1.model_id = 1
    AND h2.model_id = 2
"""

INDEX_SQL = """
SELECT
    r.region_id,
    r.region_name,
    r.country,
    COUNT(*) AS request_count,
    AVG(ir.response_time_ms) AS average_response_time_ms
FROM Region AS r
JOIN InferenceRequest AS ir ON r.region_id = ir.region_id
WHERE ir.response_time_ms > 1000000
GROUP BY r.region_id
HAVING COUNT(*) >= 5
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Visualize EXPLAIN plan comparisons from the data-analysis SQL files."
    )
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--output", type=Path, default=DEFAULT_PNG)
    parser.add_argument(
        "--runs",
        type=int,
        default=7,
        help="number of EXPLAIN executions per plan variant (default: 7)",
    )
    parser.add_argument("--host", default=os.getenv("MYSQL_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("MYSQL_PORT", "3306")))
    parser.add_argument("--user", default=os.getenv("MYSQL_USER", "root"))
    parser.add_argument("--password", default=os.getenv("MYSQL_PASSWORD", ""))
    parser.add_argument("--database", default=os.getenv("MYSQL_DATABASE", "csc370"))
    return parser.parse_args()


def explain(
    cursor: mysql.connector.cursor.MySQLCursor,
    variant: str,
    sql: str,
    run: int,
) -> list[dict[str, object]]:
    cursor.execute(f"EXPLAIN {sql}")
    columns = [column[0] for column in cursor.description]
    rows = []
    for step, values in enumerate(cursor.fetchall(), start=1):
        plan = dict(zip(columns, values))
        rows.append(
            {
                "analysis": "subquery_vs_join" if variant in {"subquery", "join"} else "index",
                "variant": variant,
                "run": run,
                "step": step,
                "select_id": plan.get("select_id", ""),
                "table": plan.get("table", ""),
                "access_type": plan.get("type", ""),
                "possible_keys": plan.get("possible_keys", "") or "",
                "key": plan.get("key", "") or "",
                "rows": float(plan.get("rows") or 0),
                "filtered": float(plan.get("filtered") or 0),
            }
        )
    return rows


def collect_plans(
    connection: mysql.connector.MySQLConnection, runs: int
) -> list[dict[str, object]]:
    cursor = connection.cursor()
    try:
        plans = []
        for run in range(1, runs + 1):
            plans.extend(explain(cursor, "subquery", SUBQUERY_SQL, run))
            plans.extend(explain(cursor, "join", JOIN_SQL, run))
        cursor.execute(
            "SELECT COUNT(*) FROM information_schema.statistics "
            "WHERE table_schema = DATABASE() "
            "AND table_name = 'InferenceRequest' "
            "AND index_name = 'idx_inference_response_time'"
        )
        if cursor.fetchone()[0] > 0:
            raise RuntimeError(
                "Index idx_inference_response_time already exists; remove it "
                "before running this comparison."
            )
        try:
            for run in range(1, runs + 1):
                plans.extend(explain(cursor, "without_index", INDEX_SQL, run))
            cursor.execute(
                "CREATE INDEX idx_inference_response_time "
                "ON InferenceRequest(response_time_ms)"
            )
            for run in range(1, runs + 1):
                plans.extend(explain(cursor, "with_index", INDEX_SQL, run))
        finally:
            cursor.execute("DROP INDEX idx_inference_response_time ON InferenceRequest")
        return plans
    finally:
        cursor.close()


def write_csv(path: Path, plans: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "analysis",
        "variant",
        "run",
        "step",
        "select_id",
        "table",
        "access_type",
        "possible_keys",
        "key",
        "rows",
        "filtered",
    ]
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(plans)


def plot_plans(path: Path, plans: list[dict[str, object]]) -> None:
    panels = [
        (
            [("subquery", "Subquery"), ("join", "Join")],
            "Subquery vs. join",
        ),
        (
            [
                ("without_index", "Without index"),
                ("with_index", "With response-time index"),
            ],
            "Aggregation before vs. after index",
        ),
    ]
    figure, axes = plt.subplots(2, 1, figsize=(14, 10), squeeze=False)
    colors = ["#4c72b0", "#dd8452"]

    for axis, (variants, title) in zip(axes.flat, panels):
        values: list[float] = []
        labels: list[str] = []
        for variant, label in variants:
            variant_rows = [plan for plan in plans if plan["variant"] == variant]
            if not variant_rows:
                continue
            run_maxima = [
                max(plan["rows"] for plan in variant_rows if plan["run"] == run)
                for run in {plan["run"] for plan in variant_rows}
            ]
            values.append(sum(run_maxima) / len(run_maxima))
            labels.append(label)

        axis.bar(labels, values, color=colors[: len(values)])
        axis.set_title(title)
        axis.set_ylabel("Highest estimated rows (log scale)")
        axis.set_yscale("log")
        axis.grid(axis="y", alpha=0.25)

    figure.suptitle("MySQL EXPLAIN plan comparisons")
    figure.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=180)


def main() -> int:
    args = parse_args()
    if args.runs < 1:
        raise ValueError("--runs must be at least 1")
    connection = None
    try:
        connection = mysql.connector.connect(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password,
            database=args.database,
            use_pure=True,
        )
        plans = collect_plans(connection, args.runs)
        write_csv(args.csv, plans)
        plot_plans(args.output, plans)
    except Error as error:
        raise RuntimeError(f"Unable to collect EXPLAIN plans: {error}") from error
    finally:
        if connection is not None and connection.is_connected():
            connection.close()

    print(f"Wrote {len(plans)} EXPLAIN steps to {args.csv}")
    print(f"Wrote visualization to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

