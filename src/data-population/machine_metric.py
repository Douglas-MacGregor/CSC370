from etl import read_rows
from common import get_gpu_server_ids, MAX_METRICS_PER_MACHINE


def populate(insert):
    server_ids = get_gpu_server_ids()
    counts = {}
    metric_id = 1
    for row in read_rows("data/raw/pai_machine_metric.csv"):
        machine = row["machine"]
        if machine not in server_ids or counts.get(machine, 0) >= MAX_METRICS_PER_MACHINE:
            continue
        counts[machine] = counts.get(machine, 0) + 1
        insert([
            metric_id, row["start_time"], row["end_time"], row["machine_num_worker"],
            row["machine_gpu"], row["machine_cpu"], machine,
        ])
        metric_id += 1
