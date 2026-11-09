# Documentation Index

## Project

- [Sprint Goals](./goals.md): goals and acceptance criteria for every sprint
- [AI Usage Declaration](./ai-declaration.md)
- [References](./references.md)

## Design (`design/`)

- [ERD](./design/erd.pdf): initial entity-relationship diagram
- [ERD v2](./design/erd-2.pdf): revised ERD (Sprint 2)
- [Dataset-to-Schema Mapping](./design/data-mapping.md): which attributes come from the trace and which are simulated

## Normalization (`normalization/`)

- [BCNF](./normalization/bcnf.pdf) ([source](./normalization/bcnf.tex))
- [FD Analysis](./normalization/fd-analysis.pdf) ([source](./normalization/fd-analysis.tex)): functional dependency analysis
- [FD Projection](./normalization/fd-projection.pdf) ([source](./normalization/fd-projection.tex)): projected functional dependencies

## Constraints (`constraints/`)

- [Constraints](./constraints/G48_Constraints.pdf): Sprint 2 constraints

## Performance (`performance/`)

- [Timing Notes](./performance/timing-notes.md): how to reproduce the timing experiments and the query optimizations made
- [Sprint 3 Query Analysis](./performance/sprint3-query-analysis.md): complex queries and `EXPLAIN` results

### Results (`performance/results/`)

Output of `csc370 benchmark`, `csc370 plot` and `csc370 explain`.

| File | Contents |
| --- | --- |
| [query_timings_results.txt](./performance/results/query_timings_results.txt) | Sprint 2 baseline timings (legacy text format) |
| [query_timings_baseline.csv](./performance/results/query_timings_baseline.csv) | Baseline timings as CSV |
| [query_timings_new_7.csv](./performance/results/query_timings_new_7.csv) | Sprint 3 timings, 7 runs per query |
| [query_timings.csv](./performance/results/query_timings.csv) | Latest `csc370 benchmark` run (default output) |
| [query_timings_comparison.png](./performance/results/query_timings_comparison.png) | Baseline vs. Sprint 3 chart |
| [query_plan_explain.csv](./performance/results/query_plan_explain.csv), [.png](./performance/results/query_plan_explain.png) | `EXPLAIN` plan comparison data and chart |
