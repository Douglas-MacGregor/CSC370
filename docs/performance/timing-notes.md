# Running the Timing Experiment

## Steps to reproduce

Set up a Python virtual env and install the project (adds the `csc370` command)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Set up the database and schema

```bash
csc370 load --fresh --schema-only
```

Set up a user on the database so the script can access it

```mysql
CREATE USER 'csc370user'@'localhost'
IDENTIFIED BY 'YourPassword123!';

GRANT ALL PRIVILEGES ON csc370.*
TO 'csc370user'@'localhost';
```

Fill the database

```bash
csc370 populate --database csc370 --user csc370user --password 'YourPassword123!' --max-servers 1000000 --max-metrics 1000000 --max-requests 1000000
```

Run the script to execute the queries

```bash
# Used default seed; run each query 7 times to reduce timing spikes
csc370 benchmark --runs 7 --database csc370 --user csc370user --password 'YourPassword123!'
```

## Query optimizations

The following changes were made after reviewing the queries in
`sql/queries/`:

- Query 02 now filters with `WHERE ir.status = 'Failed'`, matching its
  description instead of returning every inference request.
- Queries 04 and 05 no longer join `GPUType` when no `GPUType` columns are
  selected. `GPUServer.gpu_type_name` already references that table.
- Query 19 now joins and groups model/server metrics once, then uses
  `DISTINCT` to return each qualifying model once instead of running a
  correlated aggregation for every model.
- `sql/schema.sql` adds indexes for request status, request machine/region
  lookups, response-time filtering plus region grouping, and machine metric
  lookups by machine and GPU utilization.

Recreate the database from `sql/schema.sql` or apply the indexes manually
before benchmarking the optimized queries. Compare the plans and timings with:

```bash
csc370 load --fresh --schema-only --user csc370user --password 'YourPassword123!'
csc370 populate --database csc370 --user csc370user --password 'YourPassword123!' \
    --max-servers 1000000 --max-metrics 1000000 --max-requests 1000000
csc370 benchmark \
    --runs 7 \
    --database csc370 \
    --user csc370user \
    --password 'YourPassword123!'
```

Use `EXPLAIN` or `EXPLAIN ANALYZE` on queries 02, 09, 18, and 19 to confirm
that the optimizer uses the new indexes. The indexes improve possible access
paths but do not guarantee that MySQL will choose them for every data
distribution.
