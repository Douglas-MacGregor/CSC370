# Sprint Three Query Analysis

## Goal: Develop and Optimize Complex SQL Queries

- `18_region_request_aggregation.sql` uses `WHERE`, `GROUP BY`, `HAVING`, and functional-dependency attributes (`region_id -> region_name, country`).
- `19_models_with_high_gpu_utilization.sql` combines a correlated `EXISTS` subquery with `GROUP BY` and `HAVING`.
- `01_complex_predicates.sql` demonstrates `INSERT` and `DELETE` using complex query predicates.
- `01_explain_index.sql` compares the aggregation query before and after creating the non-primary index `idx_inference_response_time`.

### EXPLAIN result

Before the new index, MySQL only considered `region_id`.

After creating `idx_inference_response_time`, both `region_id` and `idx_inference_response_time` appeared under `possible_keys`, but MySQL still chose `region_id`.

This shows that adding an index does not guarantee the optimizer will use it for a particular query.

## Goal: Evaluate and Simplify Complex Queries

Query 13 uses an `IN` subquery to find machines hosting both model 1 and model 2.

`20_machines_hosting_both_models_join.sql` rewrites the same query using a self-join on `Hosts`.

Both queries return the same result, so the join formulation preserves correctness. The join version also makes the relationship between the two `Hosts` rows more explicit.

### EXPLAIN result

The subquery and join versions produced essentially the same execution plan.

Both used the `PRIMARY` key with a `ref` lookup followed by an `eq_ref` lookup, with one estimated row for each access.

Therefore, for the current schema and dataset, there was no meaningful execution-plan performance difference between the two formulations.
