"""Repo locations, so commands work from any directory."""

from pathlib import Path

# src/csc370/paths.py -> repo root (requires an editable install: pip install -e .)
ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"

SQL_DIR = ROOT / "sql"
SCHEMA = SQL_DIR / "schema.sql"
QUERIES_DIR = SQL_DIR / "queries"
INSERTION_DIR = SQL_DIR / "data-insertion"
TEMPLATES_DIR = INSERTION_DIR / "templates"

DOCS_DIR = ROOT / "docs"
RESULTS_DIR = DOCS_DIR / "performance" / "results"
