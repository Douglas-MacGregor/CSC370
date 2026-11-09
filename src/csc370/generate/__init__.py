"""Generate sql/data-insertion/<table>.sql by filling the hand-written templates."""

import argparse

from ..etl import load_template, render_template
from ..paths import INSERTION_DIR, TEMPLATES_DIR

# import order matches the old main.py so the seeded random output is unchanged
from . import region
from . import gpu_type
from . import ai_model
from . import gpu_server
from . import machine_metric
from . import hosts
from . import compatible_with
from . import inference_request

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
TABLES = [name for name, _ in STEPS]


def run_table(name, mod):
    template = load_template(TEMPLATES_DIR / f"{name}.sql")
    with open(INSERTION_DIR / f"{name}.sql", "w") as out:
        mod.populate(lambda values: out.write(render_template(template, values) + "\n"))


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "tables", nargs="*", choices=TABLES, metavar="TABLE",
        help=f"only regenerate these tables (default: all). Choices: {', '.join(TABLES)}",
    )


def run(args: argparse.Namespace) -> int:
    only = set(args.tables)
    for name, mod in STEPS:
        if only and name not in only:
            continue
        print(f"populating {name}...")
        run_table(name, mod)
    return 0
