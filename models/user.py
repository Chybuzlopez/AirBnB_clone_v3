#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, username, password, *args, **kwargs):
        """initializes user"""
	self.username = username
        self.password = self._hash_password(password)
        super().__init__(*args, **kwargs)

    def update_password(self, new_password):
        self.password = self._hash_password(new_password)
    
    def _hash_password(self, password):
        return hashlib.md5(password.encode()).hexdigest()

