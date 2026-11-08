"""Shared MySQL connection options for the commands that talk to the database."""

from __future__ import annotations

import argparse
import os

import mysql.connector


def add_mysql_args(parser: argparse.ArgumentParser) -> None:
    group = parser.add_argument_group("MySQL connection (defaults from MYSQL_* env vars)")
    group.add_argument("--host", default=os.getenv("MYSQL_HOST", "127.0.0.1"))
    group.add_argument("--port", type=int, default=int(os.getenv("MYSQL_PORT", "3306")))
    group.add_argument("--user", default=os.getenv("MYSQL_USER", "root"))
    group.add_argument("--password", default=os.getenv("MYSQL_PASSWORD", ""))
    group.add_argument("--database", default=os.getenv("MYSQL_DATABASE", "csc370"))


def connect(args: argparse.Namespace, **kwargs) -> mysql.connector.MySQLConnection:
    return mysql.connector.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database,
        **kwargs,
    )
