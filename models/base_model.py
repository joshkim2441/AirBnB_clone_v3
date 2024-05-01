#!/usr/bin/python3
"""
Contains class BaseModel
"""
import os
import uuid
import json
import models
import sqlalchemy
from os import getenv
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

time = "%Y-%m-%dT%H:%M:%S.%f"
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')
if STORAGE_TYPE == "db":
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if STORAGE_TYPE == "db":
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __set_attributes(self, attr_dict):
        """Converts attr_dict values to python attributes"""
        if 'id' not in attr_dict:
            attr_dict['id'] = str(uuid.uuid4())
        if 'created_at' not in attr_dict:
            attr_dict['created_at'] = datetime.utcnow()
        elif not isinstance(attr_dict['created_at'], datetime):
            attr_dict['created_at'] = datetime.strptime(
                attr_dict['created_at'], "%Y-%m-%d %H:%M:%S.%f"
            )
        if 'updated_at' not in attr_dict:
            attr_dict['updated_at'] = datetime.utcnow()
        elif not isinstance(attr_dict['updated_at'], datetime):
            attr_dict['updated_at'] = datetime.strptime(
                attr_dict['updated_at'], "%Y-%m-%d %H:%M:%S.%f"
            )
        if STORAGE_TYPE != 'db':
            attr_dict.pop('__class__', None)
        for attr, val in attr_dict.items():
            setattr(self, attr, val)

        def __is_serializable(self, obj_v):
            """Checks if object is serializable: private """
            try:
                obj_to_string = json.dumps(obj_v)
                return obj_to_string is not None and isinstance(
                    obj_to_string, str)
            except Exception:
                return False

        def bm_update(self, attr_dict=None):
            """Updates basemodel, sets correct attributes"""
            IGNORE = [
                'id', 'created_at', 'updated_at', 'email',
                'state_id', 'user_id', 'city_id', 'place_id'
            ]
            if attr_dict:
                updated_dict = {
                    k: v for k, v in attr_dict.items() if k not in IGNORE
                }
                for key, value in updated_dict.items():
                    setattr(self, key, value)
                self.save()

    def __str__(self):
        """String representation of the BaseModel class"""
        class_name = type(self).__name__
        return "[{}] ({}) {}".format(class_name, self.id,
                                     self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_fs=None):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if save_fs is None:
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict

    def to_json(self, saving_file_storage=False):
        """returns a json representation of self"""
        obj_class = self.__class__.__name__
        bm_dict = {
            k: v if self.__is_serializable(v) else str(v)
            for k, v in self.__dict__.items()
        }
        bm_dict.pop('_sa_instance_state', None)
        bm_dict.update({
            '__class__': obj_class
            })
        if not saving_file_storage and obj_class == 'User':
            bm_dict.pop('password', None)
        return (bm_dict)

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
