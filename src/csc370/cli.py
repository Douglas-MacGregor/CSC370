"""`csc370` command-line entry point."""

from __future__ import annotations

import argparse

from . import benchmark, explain, generate, load, plot, populate

# (subcommand, module, help)
COMMANDS = [
    ("generate", generate, "regenerate sql/data-insertion/*.sql from the raw CSVs and templates"),
    ("load", load, "create the database, apply schema.sql and load the insertion files"),
    ("populate", populate, "populate MySQL directly from the CSVs (pandas loader)"),
    ("benchmark", benchmark, "time every query in sql/queries/ and write a CSV"),
    ("plot", plot, "plot benchmark timings, optionally against a baseline"),
    ("explain", explain, "collect and plot EXPLAIN plan comparisons"),
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csc370",
        description="Tools for the CSC370 GPU inference routing database.",
    )
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")
    for name, module, help_text in COMMANDS:
        cmd = sub.add_parser(name, help=help_text, description=help_text)
        module.add_arguments(cmd)
        cmd.set_defaults(_run=module.run)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args._run(args)


if __name__ == "__main__":
    raise SystemExit(main())
