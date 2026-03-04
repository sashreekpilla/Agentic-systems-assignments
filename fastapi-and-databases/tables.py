from db import engine
from sqlalchemy import MetaData, Table, Column, Integer, String, CheckConstraint

metadata = MetaData() # metadata object stores the schema/structure of the table.


students = Table(
    "students", # name of the table.
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False), 
    Column("age", Integer, CheckConstraint('age >= 18', name='age_check')),
    Column("city", String, nullable=True)
)


def create_tables():
    metadata.create_all(engine)
