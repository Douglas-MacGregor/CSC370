# AI Usage Declaration

We used AI tools as development and review aids: an AI coding assistant
(Claude) for environment setup, Python tooling, documentation and review, and
ChatGPT (GPT-5.6 Sol) for SQL syntax verification and dataset review. This
declaration lists what each tool did and what we wrote by hand, so that the
AI's contribution is clearly separated from our own work on the course
competencies.

## What We Did by Hand

**Project design**

- Chose the project topic, defined its scope, and framed it around
  routing inference requests.
- Designed the conceptual ERD: entities, attributes, relationships and
  multiplicity, including which attributes to track.
- Identified functional dependencies and normalized the schema to BCNF.
- Wrote and maintained the sprint goals and acceptance criteria.

**Dataset analysis**

- Reviewed the Alibaba PAI dataset and decided which parts fit our
  requirements.
- Produced the field-by-field mapping from the dataset to the ERD (the source
  table behind `docs/data-mapping.md`). This included deciding which attributes
  come from real data, which must be simulated, and how.

**SQL**

- Wrote the relational schema and DDL (`sql/schema.sql`): tables, primary
  keys, foreign keys, and composite keys for the many-to-many relationship
  tables, all derived from our ERD before any AI syntax check.
- Wrote every SQL insertion template (`sql/data-insertion/templates/`). These
  define the `INSERT` statement for each table: the target table, the column
  list and column order, and the placeholder for each value.
- Wrote the demonstration queries (`sql/queries.sql`).

**Direction and decisions**

- Decided how work was split between ourselves and AI. In particular, we chose
  to write all SQL ourselves and limit AI to Python tooling.
- Decided which suggested improvements to adopt as future goals (staging tables
  to move data transformation into SQL, multi-row inserts, and schema
  constraints), and what each goal should achieve.

## What AI Did

**Coding assistant (Claude):**

- Installed and configured a local MySQL server (via Homebrew) for development
  and testing.
- Moved the raw Kaggle CSVs into `data/raw/` and updated `.gitignore` so the
  multi-GB raw dataset isn't committed.
- Wrote the Python data-population code (`src/etl.py`, `src/data-population/`)
  that follows our dataset mapping. It reads and samples the raw CSVs, joins them
  to derive the `Hosts` and `CompatibleWith` rows, generates the simulated values
  described in `docs/data-mapping.md`, and fills our hand-written SQL templates
  with those values. Claude chose the sample sizes (400 sampled jobs, at most 5
  metrics per machine).
- Reviewed our insertion templates against `sql/schema.sql` and the Python
  output, checking column names, column order and number of placeholders.
  No changes were needed.
- Suggested ways to show more SQL in the project: staging tables with
  `INSERT ... SELECT`, looking up foreign keys inside the templates, and adding
  `NOT NULL`/`CHECK` constraints. Claude described these approaches in words
  only and did not write the SQL. We chose which ones to pursue.
- Drafted `docs/data-mapping.md` from the field-mapping table we had already
  produced.
- Wrote the README section explaining how the insertion files are generated,
  and corrected the setup and load instructions. Claude also tested those
  instructions against a temporary database.

**ChatGPT (GPT-5.6 Sol):**

- Used to review and verify our work, not to design the database. After we
  had derived the tables, keys and relationship tables from our ERD using the
  syntax taught in class, it checked our SQL and helped convert that syntax to
  what MySQL expects. For example, where foreign keys and composite primary
  keys go did not change; only the syntax used to declare them did.
- Helped us read through the large, multi-table Kaggle dataset and its
  documentation to find potentially useful parts (machine information, GPU
  type, resource capacity, utilization, timing data). We reviewed the dataset
  ourselves, decided which parts matched our requirements, and identified what
  was missing and would need to be added or simulated.

## Why This Does Not Undermine Course Competencies

The competencies being assessed are conceptual and relational schema design,
normalization to BCNF, and turning a design into working SQL. We did all of
that by hand: the ERD, the normalization, the DDL with its keys and
constraints, the `INSERT` templates and the queries. Where AI wrote code, it was
Python that reads data and fills our SQL with values. It made no
database-design decisions and wrote no SQL for us. Its other work was setting
up tools, writing documentation, checking syntax, and reviewing SQL we had
already written.

Our future goals move even more of the project into SQL. Data transformation
that the Python currently performs (filtering, joins, deduplication, sampling)
will be reimplemented by us in SQL using staging tables, so that this logic is
also our own work.
