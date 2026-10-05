import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from etl import load_template, render_template  # noqa: E402

import region  # noqa: E402
import gpu_type
import ai_model
import gpu_server
import machine_metric
import hosts
import compatible_with
import inference_request

# order matters for FK deps, see schema.sql
STEPS = [
    ("region", region),
    ("gpu_type", gpu_type),
    ("ai_model", ai_model),
    ("gpu_server", gpu_server),
    ("machine_metric", machine_metric),
    ("hosts", hosts),
    ("compatible_with", compatible_with),
    ("inference_request", inference_request),
]


def run(name, mod):
    template = load_template(f"sql/data-insertion/templates/{name}.sql")
    with open(f"sql/data-insertion/{name}.sql", "w") as out:
        mod.populate(lambda values: out.write(render_template(template, values) + "\n"))


def main():
    # optionally pass table names to only run some, e.g. `main.py region ai_model`
    only = set(sys.argv[1:])
    for name, mod in STEPS:
        if only and name not in only:
            continue
        print(f"populating {name}...")
        run(name, mod)


if __name__ == "__main__":
    main()
