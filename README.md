# parsesql
A small python based sql parser focusing on finding table dependencies within database views. Currently only working with Snowflake ANSI Sql

The current implementation handles the parser as an seperate app that can be used to parse sql files. This is not a stable version. Within the 
next month the goal is to translate that app in a pip package. 

## How to use the parser:
1. Download the repository
2. Intialize the pipenv or generate a requirement.text and intialize it
3. Create a json configuration file under parser/config/configuration.json (There is an example configuration available)
4. Configure the SQLAlchemy engine
5. Create the target database table (Sqllite or Snowflake engine) with SQLAlchemy. Therefore run: 
```
cd parser/
python -m main.database.init_db
```
6. Configure the Runner class (multiprocessing, parsing vs. dataloading)
7. Run the main module with:
```
python parser/app.py
```
