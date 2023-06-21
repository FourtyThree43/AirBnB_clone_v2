#!/usr/bin/python3
"""Defines ``DBStorage`` class """

from models.base_model import Base
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBStorage:
    """Storage class that connects the application to a database """
    __engine = None
    __session = None

    def __init__(self):
        """Constructor method """
        user = getenv('HBNB_MYSQL_USER')
        passwad = getenv('HBNB_MYSQL_PWD')
        host_name = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwad, host_name, db))
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query objects on the current database session """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker()
        self.__session = Session(self.__engine)
        if cls:
            query_rows = self.__session.query(cls)
