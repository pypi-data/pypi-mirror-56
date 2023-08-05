# SQLAlchemy-CloudSQLite
Reuse your SQLite database in serverless applications and reduce prototyping costs.

With this package, you can synchronize your local SQLite database across multiple instances.
Different storage vendors can be used and easily added.
Commits result in a direct upload of your database.
To reduce API calls when reading a database, a cache_duration can be configured.


##### Info:  
Multiple write accesses in parallel can lead to data loss. Ideal for read-only applications.
Because the database is transferred as a whole file, large databases can cause latency problems.

## Available Integrations
- AWS S3

## Example
### Install
```bash
pip install sqlalchemy_cloudsqlite
```
### Usage
````python
import sqlalchemy_cloudsqlite
SQLALCHEMY_DATABASE_URI = "cloudsqlite:///quickstart.sqlite"
...
engine = create_engine(SQLALCHEMY_DATABASE_URI)

````
#### Configuration
```
import json
os.environ['config'] = json.dumps(
    {
        'cache_duration': 60,
        'storage': {
            'S3': {'bucket_name': '<BUCKET_NAME>'}
        }
    }
)
```
and provide your credentials for S3 access via environment variables or a policy. 

## About
This project is based on the following research:
- [S3SQLite - A Serverless Relational Database](https://blog.zappa.io/posts/s3sqlite-a-serverless-relational-database)
- [zappa-django-utils](https://github.com/Miserlou/zappa-django-utils)
