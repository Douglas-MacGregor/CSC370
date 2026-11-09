"""Load sql/schema.sql and the generated sql/data-insertion files with the mysql client."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path

from .db import add_mysql_args
from .generate import TABLES
from .paths import INSERTION_DIR, SCHEMA


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--fresh", action="store_true",
        help="drop and recreate the database first (schema.sql has no DROP TABLE)",
    )
    parser.add_argument(
        "--schema-only", action="store_true",
        help="apply schema.sql but skip the data-insertion files",
    )
    add_mysql_args(parser)


def _mysql(args: argparse.Namespace, database: str | None, sql_file: Path | None = None,
           execute: str | None = None) -> None:
    cmd = ["mysql", f"--host={args.host}", f"--port={args.port}", f"--user={args.user}"]
    if database:
        cmd.append(database)
    if execute:
        cmd += ["-e", execute]
    env = dict(os.environ)
    if args.password:
        env["MYSQL_PWD"] = args.password  # keep the password out of the process list
    stdin = sql_file.open("rb") if sql_file else None
    try:
        subprocess.run(cmd, stdin=stdin, env=env, check=True)
    finally:
        if stdin:
            stdin.close()


def run(args: argparse.Namespace) -> int:
    if shutil.which("mysql") is None:
        raise SystemExit("error: the `mysql` client was not found on PATH (brew install mysql)")
    if not re.fullmatch(r"\w+", args.database):
        raise SystemExit(f"error: invalid database name {args.database!r}")

    db = args.database
    try:
        if args.fresh:
            print(f"dropping database {db}...")
            _mysql(args, None, execute=f"DROP DATABASE IF EXISTS `{db}`")
        _mysql(args, None, execute=f"CREATE DATABASE IF NOT EXISTS `{db}`")

        print(f"applying {SCHEMA.relative_to(SCHEMA.parents[1])}...")
        _mysql(args, db, SCHEMA)

        if not args.schema_only:
            for table in TABLES:  # FK order, same as `csc370 generate`
                path = INSERTION_DIR / f"{table}.sql"
                print(f"loading {table}...")
                _mysql(args, db, path)
    except subprocess.CalledProcessError as error:
        raise SystemExit(
            f"error: mysql exited with status {error.returncode}"
            " (if the tables already exist, rerun with --fresh)"
        ) from error
    print("done")
    return 0
