#!/usr/bin/python3
"""Defines ``DBStorage`` class """

from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
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
                                      .format(user, passwad, host_name, db),
                                      pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query objects on the current database session """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

        new_dict = {}
        classes = {"Amenity": Amenity, "City": City, "Place": Place,
                   "Review": Review, "State": State, "User": User}

        for class_name in classes:
            if cls is None or cls is classes[class_name]:
                objs = self.__session.query(classes[class_name]).all()
                for obj in objs:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    new_dict[key] = obj

        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)
