# This file (db.py) will help to connect with Database.

from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./students.db"

engine = create_engine(DATABASE_URL, echo=True)