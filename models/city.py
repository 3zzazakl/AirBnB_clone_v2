#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


storage_type = getenv("HBNB_TYPE_STORAGE")


class City(BaseModel, Base):
    """ The city class, contains state ID and name """

    __tablename__ = "cities"
    __table_args__ = ({
        'mysql_default_charset': 'latin1'})
    if storage_type == "db":
        id = Column(String(60), primary_key=True)
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
        places = relationship("Place", cascade="all, delete", backref="cities")

    else:
        state_id = ""
        name = ""
