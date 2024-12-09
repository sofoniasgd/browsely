# coding: utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(20), nullable=False)
    location = Column(String(20), nullable=False)
    file_path = Column(String(255), nullable=False)
    root_directory = Column(String(255), nullable=False)
