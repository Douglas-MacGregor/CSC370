from common import get_gpu_types, GPU_MEMORY_GB


def populate(insert):
    for gpu_type in get_gpu_types():
        insert([gpu_type, GPU_MEMORY_GB.get(gpu_type)])
