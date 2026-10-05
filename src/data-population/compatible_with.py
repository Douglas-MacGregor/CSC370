from common import get_instances, get_inst_workload, get_task_gpu_type, get_model_id_of


def populate(insert):
    inst_workload = get_inst_workload()
    task_gpu_type = get_task_gpu_type()
    model_id_of = get_model_id_of()
    seen = set()
    for job_name, task_name, inst_id, machine, start_time, end_time in get_instances():
        workload = inst_workload.get(inst_id)
        gpu_type = task_gpu_type.get((job_name, task_name))
        if not workload or not gpu_type:
            continue
        key = (model_id_of[workload], gpu_type)
        if key not in seen:
            seen.add(key)
            insert(list(key))
