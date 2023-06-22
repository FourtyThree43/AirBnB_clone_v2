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
from sqlalchemy.orm import scoped_session, sessionmaker


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
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query objects on the current database session """

        class_dict = {}
        class_list = []
        if cls:
            class_list += [cls]
        else:
            class_list += [State, City, User, Place, Review]
        for obj in class_list:
            for instance in self.__session.query(obj).all():
                key = instance.__class__.__name__ + "." + instance.id
            #    del instance.__dict__["_sa_instance_state"]
                class_dict[key] = instance

        return class_dict

    def new(self, obj):
        """Add an object to the current database session """
        self.__session.add(obj)
        # self.save()

    def save(self):
        """Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from the current database session if not ``None`` """
        if obj:
            self.__session.delete(obj)
            # self.save()

    def reload(self):
        """Initialise a database session """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
