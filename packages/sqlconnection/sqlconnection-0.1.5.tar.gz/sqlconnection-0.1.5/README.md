SQL Adapter for Connection and Query Handling


## System Dependency

* Python 3.6.8
* pipenv


## Development Setup

1) Clone the repo 
2) cd sqlconnection
3) pipenv install
4) pipenv shell

Start developing

# Package sqlconnection
python version must be 3.6.8
### Build
python setup.py build

### Distribute
python setup.py sdist

### Dependency
* psycopg2-binary>=2.8.4

### Use 
```
from sqlconnection import postgresql
from sqlconection import postgresql_queries

psql = postgresql.Postgres()

psql.create_connection()

conn = psql.get_connection()

postgresql_queries.execute_query(conn, query)

conn.close_connection()

```




