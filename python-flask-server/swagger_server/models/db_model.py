from os import times
from pyexpat import model
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    product_brand = db.Column(db.String(80))
    product_name = db.Column(db.String(120))
    product_stock = db.Column(db.Integer)
    product_price = db.Column(db.Float)

class ProductSchema(ma.Schema):
    class Meta:
        fields = (
            'product_id',
            'product_brand',
            'product_name',
            'product_stock',
            'product_price'
        )



