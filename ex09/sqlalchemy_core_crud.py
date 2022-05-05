from django.db import connection
from sqlalchemy import MetaData, Table, Column, String, Integer, create_engine
from sqlalchemy import Text, DateTime, Boolean,select,insert,update,delete,or_,and_

connection_string ="sqlite:///Northwind_small.sqlite"
engine = create_engine(connection_string, echo=False)

metadata= MetaData()
employees = Table('Employee', metadata,
                Column('Id', Integer(), primary_key=True),
                Column('LastName', String(8000)),
                Column('FirstName', String(8000)),
                Column('BirthDate', String(8000)),
                )

def show_metadata():
    for t in metadata.sorted_tables:
        print (f"Table {t.name}:")
        for c in t.column:
            print(f"{c}({c.type})")

def do_insert():
    stmt = employees.insert().values(
        LastName = 'Collins',
        FirstName = 'Arnold',
        BirthDate ='2000-01-31'     
    )
    new_id=0