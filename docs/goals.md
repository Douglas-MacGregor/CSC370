# Table of Contents

- [Sprint One Goals](#sprint-one-goals)
- [Sprint Two Goals](#sprint-two-goals)
- [Future Sprint Goals](#future-sprint-goals)

# Sprint One Goals

## Goal: Select a Project Topic and Define Requirements

### Objective

Select a suitable database-driven information system and define a clear set of functional requirements that will guide the database design.

### Acceptance Criteria

- Project topic and scope are defined.
- Key users/stakeholders are identified.
- Project is approved by the team and TA

## Goal: Complete an Initial Entity-Relationship Diagram

### Objective

Develop an initial conceptual database design based on the project requirements.

### Acceptance Criteria

- All major entities and attributes are identified.
- Primary keys are defined.
- Relationships between entities are represented.
- ER diagram reflects the project requirements.

## Goal: Define Relationship Multiplicity

### Objective

Define/figure out the types of between relationships different entities.

### Acceptance Criteria

- Multiplicity is defined for every relationship.
- One-to-one, one-to-many, and many-to-many relationships are identified.
- Many-to-many relationships have appropriate associative entities.

## Goal: Normalize the Database to BCNF

### Objective

Transform the relational schema into a normalized design that satisfies the normalization concepts covered in the course, up to and including Boyce-Codd Normal Form (BCNF).

### Acceptance Criteria

- Functional dependencies are identified.
- Schema is normalized through 1NF, 2NF, and 3NF.
- Final schema satisfies BCNF.
- Primary and foreign keys are defined.
- Final schema remains consistent with the requirements.

## Goal: Set Up MySQL and Create Tables

### Objective

Get each group members computer's set up and ready for furture work on mySQL. Have each member spend sone time getting familar with create, modifiying and inserting data with mySQL.

### Acceptance Criteria

- MySQL is installed and working for all team members.
- Team members can create, modify, and insert data.
- Normalized schema is implemented as MySQL tables.
- Primary and foreign keys are implemented correctly.
- A subset of the project dataset is successfully inserted into the database.

---

# Sprint Two Goals

## Goal: Define Constraints and Create SQL for Referential Integrity

### Objective

Define database constraints using relational algebra notation and implement referential integrity constraints in SQL to ensure data consistency.

### Acceptance Criteria

- Constraints are expressed using relational algebra notation.
- Primary key and foreign key constraints are implemented.
- SQL constraints prevent invalid or inconsistent data.
- Constraints are demonstrated using SQL queries.

### Scope Note

Three cross-table constraints are expressed in relational algebra and checked
with SQL queries, but they are not enforced in the schema:

- A server only hosts models that are compatible with its GPU type.
- A request runs on a server that hosts the requested model.
- Metric windows for the same machine do not overlap.

A `CHECK` constraint only sees one row, so enforcing these needs triggers. That
was out of scope for this sprint and is planned under
[Enforce Database Consistency Using Advanced SQL](#goal-enforce-database-consistency-using-advanced-sql).
The current simulated data violates the first two: 4 `Hosts` rows and 353 of
400 requests. A unique `(region_name, country)` constraint on `Region` was
also deferred.

## Goal: Incorporate Inheritance and Weak Entity Sets into Database Design

### Objective

Evaluate the existing ER diagram and incorporate inheritance and weak entity sets where appropriate.

### Acceptance Criteria

- The ER diagram is evaluated against established design principles.
- Appropriate opportunities for inheritance and weak entity sets are identified.
- Design changes are consistent with the project requirements.
- The relational schema reflects the updated design.

## Goal: Calculate Minimal Bases and Project Relational Dependencies

### Objective

Simplify functional dependencies by calculating a minimal basis and determine the dependencies that hold when projected onto decomposed relations.

### Acceptance Criteria

- Functional dependencies are identified and simplified into a minimal basis.
- Functional dependencies are projected onto relevant relations.
- Dependency preservation is evaluated for the decomposition.

## Goal: Apply Third and Fourth Normal Forms

### Objective

Evaluate the relational schema for 3NF and 4NF, decomposing relations where necessary to reduce redundancy and prevent update anomalies.

### Acceptance Criteria

- Functional dependencies are evaluated to determine whether relations satisfy 3NF.
- Multivalued dependencies are identified where applicable.
- Relations are decomposed into 3NF or 4NF where necessary.
- Dependency preservation is evaluated for the resulting decomposition.

## Goal: Perform Initial Time Trials

### Objective

Conduct initial performance experiments on the database to establish a baseline for query execution times.

### Acceptance Criteria

- Representative queries are selected for testing.
- Query execution times are measured and recorded.
- The test environment and dataset are documented.
- Initial results are recorded for comparison in future sprints.

---

# Future Sprint Goals

## Goal: Expand the Database Dataset

### Objective

Explore the process of loading a larger portion of the project dataset into the database.

### Acceptance Criteria

- A larger subset of the dataset is loaded successfully.
- Data can be queried after loading.
- Any issues encountered with larger datasets are documented.

## Goal: Further Explore Database Performance

### Objective

Investigate how database size and query complexity affect system performance.

### Acceptance Criteria

- Performance of selected queries is measured.
- Performance issues, if any, are identified and documented.
- Potential improvements are investigated where appropriate.

## Goal: Implement Database Queries

### Objective

Develop queries that demonstrate the functionality and usefulness of the database.

### Acceptance Criteria

- Queries are developed to answer relevant project questions.
- Queries return correct results.
- Query performance is evaluated where appropriate.

## Goal: Improve and Refine the Database

### Objective

Review the database design and implementation based on testing and project needs.

### Acceptance Criteria

- Issues or areas for improvement are identified.
- Appropriate improvements are implemented where feasible.
- Changes remain consistent with the project requirements.

## Goal: Develop and Optimize Complex SQL Queries

### Objective

Develop complex SQL queries using aggregation, subqueries, and data manipulation, and evaluate query performance using indexes.

### Acceptance Criteria

- Aggregation queries use `WHERE`, `HAVING`, and functional dependency attributes where appropriate.
- Subqueries combine aggregations with existential conditions.
- Data is inserted or deleted based on complex query predicates.
- Query performance is evaluated using `EXPLAIN` and non-primary indexes.

## Goal: Evaluate and Simplify Complex Queries

### Objective

Analyze complex SQL queries to understand how subqueries, joins, and aggregation affect query structure and execution.

### Acceptance Criteria

- A complex query is simplified by replacing a subquery with a join where appropriate.
- Alternative query formulations are compared for correctness and readability.
- Query execution plans are examined to understand performance differences.

## Goal: Enforce Database Consistency Using Advanced SQL

### Objective

Explore how triggers and SQL's three-valued logic can enforce data consistency and handle NULL values in database queries.

### Acceptance Criteria

- Triggers are implemented to enforce a relevant database consistency rule.
- The cross-table constraints from Sprint Two (GPU compatibility of hosted
  models, requests running on a server that hosts their model, non-overlapping
  metric windows) are enforced, and the data population is fixed so existing
  data satisfies them.
- Queries involving NULL values are evaluated using three-valued logic.
- The effects of NULL values on query predicates and results are demonstrated.
