from sqlite3 import connect
from unittest import result
from sqlalchemy import create_engine
from sqlalchemy import text

connection_string="sqlite:///Northwind_small.sqlite"
engine = create_engine(connection_string,echo=False)

with engine.connect() as conn:
    result = conn.execute(text("SELECT LastName, FirstName,Title,BirthDate FROM Employee"))
    for row in result :
        print(f"{row['LastName']}{row['FirstName']}{row['BirthDate']}: \t {row['Title']}")