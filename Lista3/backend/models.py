from sqlalchemy import Column, Integer

from .database.database import Base



class Test(Base):
    __tablename__ = "test"

    id: int = Column(Integer, primary_key=True)

