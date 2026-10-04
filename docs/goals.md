# Sprint One Goals

## Goal 1: Select a Project Topic and Define Requirements

### Objective

Select a suitable database-driven information system and define a clear set of functional requirements that will guide the database design.

### Acceptance Criteria

- Project topic and scope are defined.
- Key users/stakeholders are identified.
- Project is approved by the team and TA

## Goal 2: Complete an Initial Entity-Relationship Diagram

### Objective

Develop an initial conceptual database design based on the project requirements.

### Acceptance Criteria

- All major entities and attributes are identified.
- Primary keys are defined.
- Relationships between entities are represented.
- ER diagram reflects the project requirements.

## Goal 3: Define Relationship Multiplicity

### Objective

Define/figure out the types of between relationships different entities.

### Acceptance Criteria

- Multiplicity is defined for every relationship.
- One-to-one, one-to-many, and many-to-many relationships are identified.
- Many-to-many relationships have appropriate associative entities.

## Goal 4: Normalize the Database to BCNF

### Objective

Transform the relational schema into a normalized design that satisfies the normalization concepts covered in the course, up to and including Boyce-Codd Normal Form (BCNF).

### Acceptance Criteria

- Functional dependencies are identified.
- Schema is normalized through 1NF, 2NF, and 3NF.
- Final schema satisfies BCNF.
- Primary and foreign keys are defined.
- Final schema remains consistent with the requirements.

## Goal 5: Set Up MySQL and Create Tables

### Objective

Get each group members computer's set up and ready for furture work on mySQL. Have each member spend sone time getting familar with create, modifiying and inserting data with mySQL.

### Acceptance Criteria

- MySQL is installed and working for all team members.
- Team members can create, modify, and insert data.
- Normalized schema is implemented as MySQL tables.
- Primary and foreign keys are implemented correctly.
- A subset of the project dataset is successfully inserted into the database.

---

# Future Sprint Goals

## Goal 6: Expand the Database Dataset

### Objective

Explore the process of loading a larger portion of the project dataset into the database.

### Acceptance Criteria

- A larger subset of the dataset is loaded successfully.
- Data can be queried after loading.
- Any issues encountered with larger datasets are documented.

## Goal 7: Explore Database Performance

### Objective

Investigate how database size and query complexity affect system performance.

### Acceptance Criteria

- Performance of selected queries is measured.
- Performance issues, if any, are identified and documented.
- Potential improvements are investigated where appropriate.

## Goal 8: Implement Database Queries

### Objective

Develop queries that demonstrate the functionality and usefulness of the database.

### Acceptance Criteria

- Queries are developed to answer relevant project questions.
- Queries return correct results.
- Query performance is evaluated where appropriate.

## Goal 9: Improve and Refine the Database

### Objective

Review the database design and implementation based on testing and project needs.

### Acceptance Criteria

- Issues or areas for improvement are identified.
- Appropriate improvements are implemented where feasible.
- Changes remain consistent with the project requirements.

## Goal 10: Apply Additional Database Design Concepts

### Objective

Continue applying new database design concepts introduced in future lectures to further review and refine the ERD and database design where appropriate. For example, concepts such as inheritance, generalisation, subsets, or weak entity sets could be explored if they fit the project requirements.

### Acceptance Criteria

- New database design concepts taught in future lectures are reviewed for relevance to the project.
- Potential improvements to the ERD or relational schema are identified.
- Concepts such as inheritance or generalisation are explored where appropriate.
- Relevant changes are implemented where they improve the database design.
- Any changes remain consistent with the project requirements and existing database structure.
- Major design changes and the reasoning behind them are documented.

## Goal 11: Move Data Transformation into SQL Using Staging Tables

### Objective

Shift the data transformation work currently done in Python over to SQL. Raw dataset files are loaded as-is into staging tables, and the final tables are then populated from the staging tables using SQL, so that filtering, joining, deduplicating and sampling the data are all demonstrated in SQL.

### Acceptance Criteria

- Staging tables are created for the raw dataset files used by the project.
- Python's role is limited to loading raw data and running SQL files.
- Final tables are populated from staging tables using SQL.
- Transformation logic (filtering, joins, deduplication, sampling, ID assignment) is implemented in SQL rather than Python.
- Loaded data matches the data produced by the previous Python-based approach, or any differences are documented.
- Staging tables are cleaned up once the final tables are populated.

## Goal 12: Improve Data Insertion Efficiency

### Objective

Insert data more efficiently by inserting many rows per statement instead of repeating a separate `INSERT INTO` statement for every row, while keeping the insertion SQL readable and maintainable.

### Acceptance Criteria

- Each table is populated without a separate `INSERT INTO` statement per row.
- Large tables load successfully within MySQL's limits.
- Insertion SQL remains written in separate SQL files that are easy to read.
- Load times before and after the change are compared.

## Goal 13: Strengthen the Schema with Constraints

### Objective

Improve data integrity by adding constraints to the schema so that the database itself rejects invalid data.

### Acceptance Criteria

- `NOT NULL` is applied to attributes that must always have a value.
- `CHECK` constraints enforce valid ranges and relationships between attributes (e.g. non-negative values, end times after start times).
- Attributes with a fixed set of values (e.g. request status) are restricted to those values.
- Foreign key behaviour on delete and update is defined.
- Constraints are tested by attempting to insert invalid data.
- Any constraint that conflicts with the real dataset is documented along with how it was handled.
