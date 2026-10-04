import random

from common import (
    get_sampled_jobs, get_instances, get_inst_workload,
    get_model_id_of, get_regions, get_gpu_server_ids,
)


def populate(insert):
    inst_workload = get_inst_workload()
    model_id_of = get_model_id_of()
    model_names = list(model_id_of)
    region_ids = [r[0] for r in get_regions()]
    server_ids = sorted(get_gpu_server_ids())

    job_instances = {}
    for job_name, task_name, inst_id, machine, start_time, end_time in get_instances():
        job_instances.setdefault(job_name, []).append((inst_id, machine, start_time, end_time))

    for request_id, (job_name, status, start_time) in enumerate(get_sampled_jobs(), start=1):
        insts = job_instances.get(job_name, [])

        # real model if any instance has a workload tag, otherwise made up
        model_name = next((inst_workload[i[0]] for i in insts if i[0] in inst_workload), None)
        if model_name is None:
            model_name = random.choice(model_names)

        # real machine + duration if we have an instance, otherwise made up
        if insts:
            _, machine, s, e = insts[0]
            response_time_ms = (float(e) - float(s)) * 1000 if s and e else random.uniform(50, 500)
        else:
            machine = random.choice(server_ids)
            response_time_ms = random.uniform(50, 500)

        insert([
            request_id, start_time, random.randint(16, 4096), status, response_time_ms,
            random.choice(region_ids), model_id_of[model_name], machine,
        ])
