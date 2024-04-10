from sqlalchemy import create_engine, Column, Integer, String

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    romantic_step = Column(Integer, nullable=True)
