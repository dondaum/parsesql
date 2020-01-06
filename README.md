# parsesql ![badge](https://github.com/dondaum/parsesql/workflows/parsesql/badge.svg)
A small python based sql parser focusing on finding table dependencies within database views. Currently only working with Snowflake ANSI Sql

The current implementation handles the parser as an seperate app that can be used to parse sql files. This is not a stable version. Within the 
next month the goal is to translate that app in a pip package.

The parser works currently only if no AS or as is used in FROM or JOIN conditions, e.g.

```
SELECT
*
FROM a AS oop
```
-> This won't work

However this syntax will work:
```
SELECT
*
FROM a oop
```

## How to use the parser:
1. Download the repository
2. Intialize the pipenv or generate a requirement.text and intialize it
3. Create a json configuration file under parser/config/configuration.json (There is an example configuration available)
4. Configure the SQLAlchemy engine
5. Create the target database table (Sqllite or Snowflake engine) with SQLAlchemy. Therefore run: 
```
python -m parsesql.main.database.init_db
```
Note: A sqlite file will be placed in the db directory of the package

6. Configure the Runner class (multiprocessing, parsing vs. dataloading)
7. Run the main module with:
```
python -m parsesql.app
```

For running test use:
```
python -m tests.run_all
```