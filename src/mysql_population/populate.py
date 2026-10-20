"""Load the Alibaba trace CSV files into the CSC370 MySQL schema.

The trace does not contain geographic placement, model deployment, GPU memory,
or inference-request data. Those values are generated from a local,
reproducible random generator. The script assumes that ``sql/schema.sql`` has
already been applied to the target database.
"""

from __future__ import annotations

import argparse
import os
import random
from pathlib import Path
from typing import Any

import mysql.connector
import pandas as pd

DEFAULT_SEED = 370
DEFAULT_MAX_SERVERS = 500
DEFAULT_MAX_METRICS = 2_000
DEFAULT_MAX_REQUESTS = 1_000
INSERT_BATCH_SIZE = 1_000

REGIONS = [
    (1, "us-west", "United States"),
    (2, "us-east", "United States"),
    (3, "eu-west", "Ireland"),
    (4, "ap-southeast", "Singapore"),
    (5, "sa-east", "Brazil"),
]

GPU_MEMORY_GB = {
    "P100": 16,
    "T4": 16,
    "V100": 16,
    "V100M32": 32,
}


def _csv(data_dir: Path, name: str) -> pd.DataFrame:
    """Read one trace CSV, accepting either data/ or data/raw/ layouts."""
    path = data_dir / name
    if not path.exists() and data_dir.name != "raw":
        path = data_dir / "raw" / name
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")
    return pd.read_csv(path)


def _number(value: Any, fallback: float, rng: random.Random) -> float:
    if pd.notna(value):
        return float(value)
    return fallback * rng.uniform(0.8, 1.2)


def _integer(value: Any, fallback: int, rng: random.Random) -> int:
    if pd.notna(value):
        return int(float(value))
    return max(1, int(round(fallback * rng.uniform(0.8, 1.2))))


def _text(value: Any, fallback: str) -> str:
    return fallback if pd.isna(value) or str(value).strip() == "" else str(value)


def build_rows(
    data_dir: Path,
    rng: random.Random,
    max_servers: int,
    max_metrics: int,
    max_requests: int,
) -> dict[str, list[tuple[Any, ...]]]:
    """Transform CSV data into rows matching the database schema."""
    specs = _csv(data_dir, "pai_machine_spec.csv")
    specs = specs[specs["gpu_type"].fillna("").ne("CPU")]
    specs = specs[specs["cap_gpu"].fillna(0).astype(float).gt(0)]
    specs = specs.drop_duplicates("machine").head(max_servers)
    if specs.empty:
        raise ValueError("No GPU server rows were found in pai_machine_spec.csv")

    gpu_names = sorted(specs["gpu_type"].dropna().astype(str).unique())
    gpu_types = [(name,) for name in gpu_names]
    specific_gpu_types = [
        (name, GPU_MEMORY_GB.get(name, rng.randint(8, 32))) for name in gpu_names
    ]
    servers = [
        (
            str(row.machine),
            _integer(row.cap_cpu, 32, rng),
            _integer(row.cap_mem, 128, rng),
            _integer(row.cap_gpu, 1, rng),
            REGIONS[index % len(REGIONS)][0],
            str(row.gpu_type),
        )
        for index, row in enumerate(specs.itertuples(index=False))
    ]

    tags = _csv(data_dir, "pai_group_tag_table.csv")
    model_names = sorted(
        value for value in tags["workload"].dropna().astype(str).str.strip().unique()
        if value
    )
    if not model_names:
        model_names = ["default-model"]
    models = [(index, name) for index, name in enumerate(model_names, start=1)]
    model_ids = {name: model_id for model_id, name in models}

    hosts = [
        (model_id, machine_id)
        for model_id, _ in models
        for machine_id, *_ in servers
        if rng.random() < 0.25
    ]
    compatible = [
        (model_id, gpu_name)
        for model_id, _ in models
        for gpu_name in gpu_names
        if rng.random() < 0.7
    ]
    if not compatible:
        compatible = [(models[0][0], gpu_names[0])]

    metrics_source = _csv(data_dir, "pai_machine_metric.csv")
    metrics_source = metrics_source[
        metrics_source["machine"].astype(str).isin({row[0] for row in servers})
    ].head(max_metrics)
    metrics = [
        (
            index,
            _number(row.start_time, 1_000_000, rng),
            _number(row.end_time, _number(row.start_time, 1_000_000, rng) + 300, rng),
            _number(row.machine_num_worker, 10, rng),
            _number(row.machine_gpu, 50, rng),
            _number(row.machine_cpu, 50, rng),
            str(row.machine),
        )
        for index, row in enumerate(metrics_source.itertuples(index=False), start=1)
    ]

    jobs = _csv(data_dir, "pai_job_table.csv").head(max_requests)
    requests = []
    for request_id, row in enumerate(jobs.itertuples(index=False), start=1):
        model_name = model_names[(request_id - 1) % len(model_names)]
        machine_id = servers[(request_id - 1) % len(servers)][0]
        submitted = _number(row.start_time, 1_000_000, rng)
        status = _text(row.status, rng.choice(["Completed", "Failed", "Running"]))
        requests.append(
            (
                request_id,
                submitted,
                _integer(pd.NA, 128, rng),
                status,
                _number(pd.NA, 250, rng),
                REGIONS[(request_id - 1) % len(REGIONS)][0],
                model_ids[model_name],
                machine_id,
            )
        )

    return {
        "regions": REGIONS,
        "gpu_types": gpu_types,
        "specific_gpu_types": specific_gpu_types,
        "models": models,
        "servers": servers,
        "metrics": metrics,
        "hosts": hosts,
        "compatible": compatible,
        "requests": requests,
    }


def insert_rows(connection: Any, rows: dict[str, list[tuple[Any, ...]]]) -> None:
    """Insert all generated rows in foreign-key order as one transaction."""
    statements = [
        ("regions", "INSERT INTO Region (region_id, region_name, country) VALUES (%s, %s, %s)"),
        ("gpu_types", "INSERT INTO GPUType (gpu_type_name) VALUES (%s)"),
        (
            "specific_gpu_types",
            "INSERT INTO SpecificGPUType (gpu_type_name, memory_gb) VALUES (%s, %s)",
        ),
        ("models", "INSERT INTO AIModel (model_id, model_name) VALUES (%s, %s)"),
        (
            "servers",
            "INSERT INTO GPUServer (machine_id, cpu_capacity, memory_capacity, gpu_capacity, region_id, gpu_type_name) VALUES (%s, %s, %s, %s, %s, %s)",
        ),
        (
            "metrics",
            "INSERT INTO MachineMetric (metric_id, start_time, end_time, worker_load, gpu_utilization, cpu_utilization, machine_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        ),
        ("hosts", "INSERT INTO Hosts (model_id, machine_id) VALUES (%s, %s)"),
        (
            "compatible",
            "INSERT INTO CompatibleWith (model_id, gpu_type_name) VALUES (%s, %s)",
        ),
        (
            "requests",
            "INSERT INTO InferenceRequest (request_id, submitted_at, input_size, status, response_time_ms, region_id, model_id, machine_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        ),
    ]
    cursor = connection.cursor()
    try:
        for key, statement in statements:
            for start in range(0, len(rows[key]), INSERT_BATCH_SIZE):
                cursor.executemany(
                    statement,
                    rows[key][start : start + INSERT_BATCH_SIZE],
                )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--max-servers", type=int, default=DEFAULT_MAX_SERVERS)
    parser.add_argument("--max-metrics", type=int, default=DEFAULT_MAX_METRICS)
    parser.add_argument("--max-requests", type=int, default=DEFAULT_MAX_REQUESTS)
    parser.add_argument("--host", default=os.getenv("MYSQL_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("MYSQL_PORT", "3306")))
    parser.add_argument("--user", default=os.getenv("MYSQL_USER", "root"))
    parser.add_argument("--password", default=os.getenv("MYSQL_PASSWORD", ""))
    parser.add_argument("--database", default=os.getenv("MYSQL_DATABASE", "csc370"))
    args = parser.parse_args()

    rows = build_rows(
        args.data_dir,
        random.Random(args.seed),
        args.max_servers,
        args.max_metrics,
        args.max_requests,
    )
    connection = mysql.connector.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database,
    )
    try:
        insert_rows(connection, rows)
    finally:
        connection.close()
    print("Inserted: " + ", ".join(f"{key}={len(value)}" for key, value in rows.items()))


if __name__ == "__main__":
    main()
