import sqlalchemy
from os import times
from pyexpat import model
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Text, Boolean, Float

#db = SQLAlchemy()
#ma = Marshmallow()

engine = sqlalchemy.create_engine('mysql+pymysql://root:secret@productmariadb:3306/productdb?charset=utf8mb4')
Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    brand = Column(String(80))
    name = Column(String(120))
    stock = Column(Integer)
    price = Column(Float)

    def __init__(self, brand, name, stock, price):
        self.brand = brand
        self.name = name
        self.stock = stock
        self.price = price

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

