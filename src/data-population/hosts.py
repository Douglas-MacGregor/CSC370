from common import get_instances, get_inst_workload, get_model_id_of


def populate(insert):
    inst_workload = get_inst_workload()
    model_id_of = get_model_id_of()
    seen = set()
    for job_name, task_name, inst_id, machine, start_time, end_time in get_instances():
        workload = inst_workload.get(inst_id)
        if not workload:
            continue
        key = (model_id_of[workload], machine)
        if key not in seen:
            seen.add(key)
            insert(list(key))
