#!/usr/bin/python3
"""Defines ``DBStorage`` class """

from models.base_model import Base
import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+mysqldb://hbnb_dev:hbnb_dev_pwd@localhost"
                       + "/hbnb_dev_db", pool_pre_ping=True)

