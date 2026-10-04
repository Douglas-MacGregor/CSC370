# CSC370

## Project Description

This project will develop an information system for analyzing machine learning workloads in large-scale GPU clusters. The database will contain trace data from Alibaba’s Platform for Artificial Intelligence (PAI), covering training and inference jobs running on over 6,500 GPUs across approximately 1,800 machines during July and August 2020. The system will organize and store information about jobs, machines, GPUs, and workload characteristics to enable efficient querying and analysis of cluster activity.

## Project Links

- [Sprint Goals](./docs/Goals.md)
- [Dataset Link](https://www.kaggle.com/datasets/derrickmwiti/cluster-trace-gpu-v2020/data)
- [Dataset-to-Schema Mapping](./docs/data-mapping.md)
- [AI Usage Declaration](./docs/ai-declaration.md)

## Setup

1. Download the [dataset](https://www.kaggle.com/datasets/derrickmwiti/cluster-trace-gpu-v2020/data)
   and extract the CSVs into `data/raw/` (gitignored; not committed due to size).
2. Install MySQL locally, e.g. `brew install mysql && brew services start mysql`.
3. Regenerate the sample data load (optional — `sql/data.sql` is already
   committed): `python3 src/etl.py`.
4. Load the database:
    ```
    mysql -u root < sql/schema.sql
    mysql -u root < sql/data.sql
    mysql -u root --table < sql/queries.sql
    ```

## Authors

| Name              | Student Number |
| ----------------- | -------------- |
| Douglas MacGregor | V01008370      |
| Mohammad Awwad    | V01026961      |
| Jarren Morris     | V01043998      |
