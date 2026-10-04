import random

from etl import read_rows
from common import get_regions


def populate(insert):
    region_ids = [r[0] for r in get_regions()]
    for row in read_rows("data/raw/pai_machine_spec.csv"):
        if row["gpu_type"] == "CPU":
            continue
        insert([
            row["machine"], row["cap_cpu"], row["cap_mem"], row["cap_gpu"],
            random.choice(region_ids), row["gpu_type"],
        ])
