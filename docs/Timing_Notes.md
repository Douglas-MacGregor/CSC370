# Running the Timing Experiment

## Setup

set up python virtual env

```bash
python3 -m venv myenv
source myenv/bin/activate
```

Set up the database and scheme

```bash
   mysql -u root -e "CREATE DATABASE IF NOT EXISTS csc370"
   mysql -u root csc370 < sql/schema.sql
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
python3 src/mysql_population/populate.py --database csc370 --user csc370user --password 'YourPassword123!' --max-servers 1000000 --max-metrics 1000000 --max-requests 1000000
```

Run the script to execute the queries

```bash
# Used default seed
python3 src/benchmark_queries.py --runs 3 --database csc370 --user csc370user --password 'YourPassword123!'
```
