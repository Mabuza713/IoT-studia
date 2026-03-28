import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


class DatabaseManager:
    def __init__(self):
        database_url = os.getenv("DATABASE_URL")
        print(database_url)
        self.engine = create_engine(database_url)

        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

db_manager = DatabaseManager()
Base = declarative_base()