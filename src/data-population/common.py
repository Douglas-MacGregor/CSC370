# shared lookups so the per-table scripts stay consistent with each other
# (same regions, same model ids, same sampled jobs) without each one
# re-scanning the big CSVs from scratch
#
# note: this is plain python over the raw CSV files. it doesn't build, run or
# talk to SQL at all; every SQL statement comes from the hand-written
# templates in sql/data-insertion/templates/

import random

from etl import read_rows

random.seed(370)

RAW = "data/raw"

REGIONS = [
    (1, "us-west", "United States"),
    (2, "us-east", "United States"),
    (3, "eu-west", "Ireland"),
    (4, "ap-southeast", "Singapore"),
    (5, "sa-east", "Brazil"),
]

GPU_MEMORY_GB = {"P100": 16, "T4": 16, "V100": 16, "V100M32": 32, "MISC": None}

SAMPLE_JOB_COUNT = 400
MAX_METRICS_PER_MACHINE = 5

_cache = {}


def get_regions():
    return REGIONS


def get_gpu_types():
    if "gpu_types" not in _cache:
        _cache["gpu_types"] = sorted(
            {row["gpu_type"] for row in read_rows(f"{RAW}/pai_machine_spec.csv")} - {"CPU"}
        )
    return _cache["gpu_types"]


def get_gpu_server_ids():
    if "gpu_server_ids" not in _cache:
        _cache["gpu_server_ids"] = {
            row["machine"] for row in read_rows(f"{RAW}/pai_machine_spec.csv")
            if row["gpu_type"] != "CPU"
        }
    return _cache["gpu_server_ids"]


def get_model_id_of():
    if "model_id_of" not in _cache:
        names = sorted({
            row["workload"].strip() for row in read_rows(f"{RAW}/pai_group_tag_table.csv")
            if row["workload"].strip()
        })
        _cache["model_id_of"] = {name: i + 1 for i, name in enumerate(names)}
    return _cache["model_id_of"]


def get_sampled_jobs():
    if "sampled_jobs" not in _cache:
        jobs = [
            (row["job_name"], row["status"], row["start_time"])
            for row in read_rows(f"{RAW}/pai_job_table.csv")
            if row["start_time"]
        ]
        random.shuffle(jobs)
        _cache["sampled_jobs"] = jobs[:SAMPLE_JOB_COUNT]
    return _cache["sampled_jobs"]


def get_sampled_job_names():
    return {j[0] for j in get_sampled_jobs()}


def get_instances():
    """(job_name, task_name, inst_id, machine, start_time, end_time) for sampled jobs,
    restricted to machines that are real GPU servers."""
    if "instances" not in _cache:
        job_names = get_sampled_job_names()
        server_ids = get_gpu_server_ids()
        _cache["instances"] = [
            (row["job_name"], row["task_name"], row["inst_id"], row["machine"],
             row["start_time"], row["end_time"])
            for row in read_rows(f"{RAW}/pai_instance_table.csv")
            if row["job_name"] in job_names and row["machine"] in server_ids
        ]
    return _cache["instances"]


def get_task_gpu_type():
    """(job_name, task_name) -> gpu_type, for sampled jobs only."""
    if "task_gpu_type" not in _cache:
        job_names = get_sampled_job_names()
        result = {}
        for row in read_rows(f"{RAW}/pai_task_table.csv"):
            if row["job_name"] in job_names and row["gpu_type"]:
                result[(row["job_name"], row["task_name"])] = row["gpu_type"]
        _cache["task_gpu_type"] = result
    return _cache["task_gpu_type"]


def get_inst_workload():
    """inst_id -> workload, restricted to instances we actually sampled."""
    if "inst_workload" not in _cache:
        inst_ids = {i[2] for i in get_instances()}
        result = {}
        for row in read_rows(f"{RAW}/pai_group_tag_table.csv"):
            if row["inst_id"] in inst_ids and row["workload"].strip():
                result[row["inst_id"]] = row["workload"].strip()
        _cache["inst_workload"] = result
    return _cache["inst_workload"]
