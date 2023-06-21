#!/usr/bin/python3
"""Defines ``DBStorage`` class """

from models.base_model import Base
import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBStorage:
    """Storage class that connects the application to a database """
    __engine = None
    __session = None

    def __init__(self):
        """Constructor method """
        self.__engine = create_engine(f"mysql+mysqldb://"
                                      + f"{os.getenv('HBNB_MYSQL_USER')}:"
                                      + f"{os.getenv('HBNB_MYSQL_PWD')}"
                                      + f"@{os.getenv('HBNB_MYSQL_HOST')}/"
                                      + f"{os.getenv('HBNB_MYSQL_DB')}"
                                      , pool_pre_ping=True)

        if os.getenv("HBNB_MYSQL_USER") == "test":
            # drop all tables
            pass

    def all(self, cls=None):
        """Query objects on the current database session """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker()
        self.__session = Session(self.__engine)
        if cls:
            query_rows = self.__session.query(cls)
