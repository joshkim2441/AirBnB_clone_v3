#!/usr/bin/python
""" holds class Amenity"""
import os
import models
import sqlalchemy
from os import getenv
from sqlalchemy import Column, String
from models.place import place_amenity
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class Amenity(BaseModel, Base):
    """Representation of Amenity """
    if STORAGE_TYPE == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary=place_amenity,
                                       back_populates="amenities")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)
