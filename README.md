# CSC370

## Project Description

This project will develop an information system for analyzing machine learning workloads in large-scale GPU clusters. The database will contain trace data from Alibaba’s Platform for Artificial Intelligence (PAI), covering training and inference jobs running on over 6,500 GPUs across approximately 1,800 machines during July and August 2020. The system will organize and store information about jobs, machines, GPUs, and workload characteristics to enable efficient querying and analysis of cluster activity.

## Project Links

- [Sprint Goals](./docs/goals.md)
- [Documentation Index](./docs/README.md)
- [Dataset Link](https://www.kaggle.com/datasets/derrickmwiti/cluster-trace-gpu-v2020/data)
- [Dataset-to-Schema Mapping](./docs/design/data-mapping.md)
- [AI Usage Declaration](./docs/ai-declaration.md)

## Repository Layout

| Path          | Contents                                                                                                                                                 |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docs/`       | Goals, AI declaration and references, with subfolders `design/`, `normalization/`, `constraints/` and `performance/` (see the [index](./docs/README.md)) |
| `sql/`        | Schema, queries, data-insertion templates and generated insertion files                                                                                  |
| `src/csc370/` | Python package behind the `csc370` command                                                                                                               |
| `data/raw/`   | Raw Kaggle CSVs (gitignored)                                                                                                                             |

## Setup

1. Download the [dataset](https://www.kaggle.com/datasets/derrickmwiti/cluster-trace-gpu-v2020/data)
   and extract the CSVs into `data/raw/` (gitignored; not committed due to size).
2. Install MySQL locally, e.g. `brew install mysql && brew services start mysql`.
3. Install the project (Python 3.10+). This installs the dependencies from
   `pyproject.toml` and adds the `csc370` command:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e .
    ```
    Keep the install editable (`-e`): the commands find `sql/`, `data/` and
    `docs/` relative to the repository, so they work from any directory.
4. Load the database:
    ```bash
    csc370 load --fresh
    ```

## The `csc370` Command

Run `csc370 --help`, or `csc370 <command> --help`, for every option.

| Command                                 | What it does                                                                                        |
| --------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `csc370 generate [TABLE ...]`           | Regenerate `sql/data-insertion/<table>.sql` from the raw CSVs and templates (all tables by default) |
| `csc370 load [--fresh] [--schema-only]` | Create the database, apply `sql/schema.sql`, then load the insertion files in foreign-key order     |
| `csc370 populate`                       | Populate MySQL directly from the CSVs with Pandas (alternative to `load`)                           |
| `csc370 benchmark [--runs N]`           | Time every query in `sql/queries/` and write a CSV                                                  |
| `csc370 plot [CSV] [--baseline CSV]`    | Plot benchmark timings, optionally against a previous sprint                                        |
| `csc370 explain`                        | Collect and plot the `EXPLAIN` plan comparisons                                                     |

Commands that connect to MySQL accept `--host`, `--port`, `--user`,
`--password` and `--database`, or the matching `MYSQL_HOST`, `MYSQL_PORT`,
`MYSQL_USER`, `MYSQL_PASSWORD` and `MYSQL_DATABASE` environment variables.
The defaults are `root` with no password on `127.0.0.1:3306`, database
`csc370`.

A typical end-to-end run:

```bash
csc370 generate            # optional: the insertion files are already committed
csc370 load --fresh        # drop + recreate csc370, apply schema, insert data
csc370 benchmark --runs 7
csc370 plot --baseline docs/performance/results/query_timings_baseline.csv
```

### Loading the database (`load`)

`load` runs `CREATE DATABASE IF NOT EXISTS`, then sends `sql/schema.sql` and
each `sql/data-insertion/<table>.sql` to the `mysql` client in the order
`region, gpu_type, ai_model, gpu_server, machine_metric, hosts,
compatible_with, inference_request`, which foreign keys require. Because
`schema.sql` has no `DROP TABLE`, use `--fresh` to drop and recreate the
database when it already has tables. `--schema-only` creates empty tables,
for example before running `populate`. The password goes to `mysql` through
`MYSQL_PWD`, not the command line.

### Populate MySQL directly from CSVs (`populate`)

After `csc370 load --fresh --schema-only`, the direct loader can populate the
database with Pandas and `mysql-connector-python`:

```bash
csc370 populate --database csc370
```

The loader reads CSVs from `data/` (or `data/raw/`), uses parameterized
inserts, and commits all tables in foreign-key order as one transaction.
Missing values and fields not present in the trace are generated with a
reproducible random seed (`--seed 370`). Defaults are capped at 500 GPU
servers, 2,000 metrics, and 1,000 inference requests; adjust those limits
with `--max-servers`, `--max-metrics`, and `--max-requests`. Source request
statuses are normalized to the schema values; for example, `Completed` is
stored as `Terminated` and `Waiting` is stored as `Running`.

### Benchmark queries (`benchmark`)

Run every SQL file in `sql/queries/` three times and write the elapsed
wall-clock time for each run to
`docs/performance/results/query_timings.csv`:

```bash
csc370 benchmark
```

The benchmark reuses one MySQL connection, measures with Python's
high-resolution monotonic clock, and fetches all result rows before stopping
each timer. Times are written in milliseconds. The query directory includes
the baseline queries and the newer complex queries (18–20), so one run covers
both implementations. Use `--runs N` to change the number of repetitions or
`--output PATH` to choose another CSV output file.

### Visualize query performance (`plot`, `explain`)

Create a bar chart of average query times from the latest benchmark
(`docs/performance/results/query_timings.png`):

```bash
csc370 plot
```

To compare a run with a previous sprint, pass that sprint's CSV as
`--baseline`:

```bash
csc370 plot docs/performance/results/query_timings_new_7.csv \
    --baseline docs/performance/results/query_timings_baseline.csv \
    --output docs/performance/results/query_timings_comparison.png
```

The chart uses the same average wall-clock metric for both inputs. Missing
queries are shown as zero-height bars, making additions such as the complex
queries visible without changing the historical results.

`csc370 explain` runs the subquery-vs-join and index `EXPLAIN` comparisons
and writes `docs/performance/results/query_plan_explain.csv` and `.png`.

## How the Data Insertion Files Are Generated

The SQL that inserts data is written by hand. Python only fills in the values.

- **Templates** (`sql/data-insertion/templates/<table>.sql`) are hand-written: one
  `INSERT` statement per table, with a `?` placeholder for each value, e.g.
    ```sql
    INSERT INTO AIModel (model_id, model_name)
    VALUES (?, ?);
    ```
- **Population scripts** (`src/csc370/generate/<table>.py`) read the raw CSVs in
  `data/raw/` and produce the values for each row, in the same order as the
  template's placeholders. Shared lookups (sampled jobs, model IDs, regions) live in
  `common.py`, so all tables are generated from the same data. Values that aren't
  in the dataset (e.g. regions) are simulated with a fixed random seed, so the output
  is reproducible. These scripts (including `common.py`) only read and filter CSV
  data in Python and return plain values. They do not build, generate or run any
  SQL. All SQL comes from the hand-written templates.
- **`csc370 generate`** (`src/csc370/generate/__init__.py`) puts the two together. For each row a population script produces,
  it fills that table's template with the row's values, quoting strings, leaving
  numbers unquoted and writing empty values as `NULL`. Each filled-in statement is
  written to `sql/data-insertion/<table>.sql`.

The output is one `INSERT` per row:

```sql
INSERT INTO AIModel (model_id, model_name)
VALUES (1, 'bert');
INSERT INTO AIModel (model_id, model_name)
VALUES (2, 'ctr');
...
```

Replacing these with multi-row inserts is planned as a future goal (see
[Sprint Goals](./docs/goals.md)).

To change what gets inserted into a table, edit its template. To change which data
goes into it, edit its population script. Then rerun `csc370 generate`. Pass table names to
regenerate only those, e.g. `csc370 generate region ai_model`.

## Authors

| Name              | Student Number |
| ----------------- | -------------- |
| Douglas MacGregor | V01008370      |
| Mohammad Awwad    | V01026961      |
| Jarren Morris     | V01043998      |
