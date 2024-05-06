#!/usr/bin/python3
""" Place Module for HBNB project """
from models.amenity import Amenity
from models.base_model import BaseModel, Base

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from os import getenv
from sqlalchemy.orm import relationship

storage_type = getenv("HBNB_TYPE_STORAGE")
place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey("places.id"),
           primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    if storage_type == "db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenities = relationship("Amenity", secondary="place_amenity",
                                 viewonly=False)
        amenity_ids = []
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def amenities(self):
            """ Get amenities """
            from models import storage
            amenity_objs = []
            for amenity_id in self.amenity_ids:
                amenity_obj = storage.get("Amenity", amenity_id)
                if amenity_obj is not None:
                    amenity_objs.append(amenity_obj)
            return amenity_objs

        @amenities.setter
        def amenities(self, obj):
            """ Set amenities """
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
