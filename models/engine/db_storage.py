#!/usr/bin/python3
"""Defines ``DBStorage`` class """

from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
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
                                      + f"{os.getenv('HBNB_MYSQL_DB')}",
                                      pool_pre_ping=True)

        if os.getenv("HBNB_MYSQL_USER") == "test":
            # drop all tables
            pass

    def all(self, cls=None):
        """Query objects on the current database session """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

        class_list = [User, State, City, Amenity, Place, Review]
        class_dict = {}
        if cls:
            for instance in self.__session.query(cls).all():
                key = instance.__class__.__name__ + "." + instance.id
                class_dict[key] = instance
        else:
            for obj in class_list:
                for instance in self.__session.query(obj).all():
                    key = instance.__class__.__name__ + "." + instance.id
                    class_dict[key] = instance

        return class_dict
