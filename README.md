# CSC370

## Project Description

This project will develop an information system for analyzing machine learning workloads in large-scale GPU clusters. The database will contain trace data from Alibaba’s Platform for Artificial Intelligence (PAI), covering training and inference jobs running on over 6,500 GPUs across approximately 1,800 machines during July and August 2020. The system will organize and store information about jobs, machines, GPUs, and workload characteristics to enable efficient querying and analysis of cluster activity.

## Project Links

- [Sprint Goals](./docs/goals.md)
- [Dataset Link](https://www.kaggle.com/datasets/derrickmwiti/cluster-trace-gpu-v2020/data)
- [Dataset-to-Schema Mapping](./docs/data-mapping.md)
- [AI Usage Declaration](./docs/ai-declaration.md)

## Setup

1. Download the [dataset](https://www.kaggle.com/datasets/derrickmwiti/cluster-trace-gpu-v2020/data)
   and extract the CSVs into `data/raw/` (gitignored; not committed due to size).
2. Install MySQL locally, e.g. `brew install mysql && brew services start mysql`.
3. Regenerate the data insertion files (optional — they are already committed),
   from the repo root: `python3 src/data-population/main.py`.
4. Load the database (tables must be loaded in this order because of foreign keys):
    ```
    mysql -u root -e "CREATE DATABASE IF NOT EXISTS csc370"
    mysql -u root csc370 < sql/schema.sql
    for t in region gpu_type ai_model gpu_server machine_metric hosts compatible_with inference_request; do
        mysql -u root csc370 < sql/data-insertion/$t.sql
    done
    mysql -u root csc370 --table < sql/queries.sql
    ```

## How the Data Insertion Files Are Generated

The SQL that inserts data is written by hand. Python only fills in the values.

- **Templates** (`sql/data-insertion/templates/<table>.sql`) are hand-written: one
  `INSERT` statement per table, with a `?` placeholder for each value, e.g.
    ```sql
    INSERT INTO AIModel (model_id, model_name)
    VALUES (?, ?);
    ```
- **Population scripts** (`src/data-population/<table>.py`) read the raw CSVs in
  `data/raw/` and produce the values for each row, in the same order as the
  template's placeholders. Shared lookups (sampled jobs, model IDs, regions) live in
  `common.py`, so all tables are generated from the same data. Values that aren't
  in the dataset (e.g. regions) are simulated with a fixed random seed, so the output
  is reproducible. These scripts (including `common.py`) only read and filter CSV
  data in Python and return plain values. They do not build, generate or run any
  SQL. All SQL comes from the hand-written templates.
- **`main.py`** puts the two together. For each row a population script produces,
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
goes into it, edit its population script. Then rerun `main.py`. Pass table names to
regenerate only those, e.g. `python3 src/data-population/main.py region ai_model`.

## Authors

| Name              | Student Number |
| ----------------- | -------------- |
| Douglas MacGregor | V01008370      |
| Mohammad Awwad    | V01026961      |
| Jarren Morris     | V01043998      |
