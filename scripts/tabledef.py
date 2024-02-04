# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Local
SQLALCHEMY_DATABASE_URI = 'sqlite:///everything.db'

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(SQLALCHEMY_DATABASE_URI)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    password = Column(String(512))
    email = Column(String(50))

    def __repr__(self):
        return '<User %r>' % self.username

class Comments(Base):
    __tablename__ = "Comments"

    id = Column(Integer, primary_key=True)
    activeFile = Column(String(500))
    selectedText = Column(String(500))
    comment = Column(String(500))
    tag = Column(String(500))
    username = Column(String(500))

    def __repr__(self):
        return '<selectedText %r>' % self.selectedText


engine = db_connect()  # Connect to database
Base.metadata.create_all(engine)  # Create models
