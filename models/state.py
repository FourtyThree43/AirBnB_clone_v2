#!/usr/bin/python3
""" State Module for HBNB project """

import models
from models.base_model import Base, BaseModel
# from models.city import City
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", back_populates="state",
                          cascade="all, delete, delete-orphan")

    @property
    def cities(self):
        """
        Return the list of ``City`` instances with ``state_id`` equal to
        the current ``State.id``
        """
        return [value for key, value in models.storage.all().items()
                if key.split(".")[0] == "City" and value.state_id == self.id]
