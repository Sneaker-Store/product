from os import times
from pyexpat import model
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(80))
    name = db.Column(db.String(120))
    stock = db.Column(db.Integer)
    price = db.Column(db.Float)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self, brand, name, stock, price):
        self.brand = brand
        self.name = name
        self.stock = stock
        self.price = price

class ProductSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'brand',
            'name',
            'stock',
            'price'
        )



