from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='sqlalchemy_cloudsqlite',
      version='0.1.0dev0',
      description='SQLite for Serverless Computing',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/njannasch/SQLAlchemy-CloudSQLite',
      author='Nils Jannasch',
      author_email='nils@njann.de',
      license='MIT',
      packages=['sqlalchemy_cloudsqlite'],
      install_requires=['sqlalchemy', 'boto3'],
      entry_points={
          "sqlalchemy.dialects": [
              "cloudsqlite = sqlalchemy_cloudsqlite.dialect:CloudSQLiteDialect",
          ],
      },
      python_requires='>=3.6',
      )
