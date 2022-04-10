import connexion
from itsdangerous import json
from numpy import product
import six

from swagger_server.models.product import Product as Product_model  # noqa: E501
from swagger_server.models.db_model import Product as Product_db, db, ma, ProductSchema
from swagger_server import util
from flask import Flask, jsonify, make_response, request


def delete_product():  # noqa: E501
    '''delete products based on query'''

    brand = request.args.get('brand') #obtem o input do user localhost:8080/v1/products?brand=Nike
    name = request.args.get('name') #localhost:8080/v1/products?name=Reebok+Classic98

    if brand: #se tiver sido usado como query a brand
        products = Product_db.query.filter_by(product_brand = brand).all() #obtem todos os produtos dessa brand

        if not products: #se nao existirem
            return make_response(
                "Products of brand {product_brand} not found".format(product_brand=brand), 404
            )

        Product_db.query.filter_by(product_brand = brand).delete() #se existirem sao apagados
        db.session.commit() #atualiza a bd
        return make_response(
            "Products of brand {product_brand} deleted".format(product_brand=brand), 200
        )
        
    elif name:
        products = Product_db.query.filter_by(product_name = name).all()

        if not products:
            return make_response(
                "Product with name {product_name} not found".format(product_name=name), 404
            )

        Product_db.query.filter_by(product_name = name).delete()
        db.session.commit()
        return make_response(
            "Product with name {product_name} deleted".format(product_name=name), 200
        )

    else:
        Product_db.query.filter().delete()
        return make_response(
            "All products were deleted", 200
        )


def delete_product_by_id(prodID):  # noqa: E501
    '''delete product based on ID'''

    product = Product_db.query.filter_by(product_id = prodID).all() #verifica a existencia de um produto com esse id

    if product: #caso exista
        Product_db.query.filter_by(product_id = prodID).delete()  #apaga-o da bd
        db.session.commit() #atualiza a bd
        return make_response(
            "Product with ID {product_id} deleted".format(product_id=prodID), 200
        )
    else: #caso nao exista
        return make_response(
            "Product ID {product_id} not found".format(product_id=prodID), 404
    )


def get_product_by_id(prodID):  # noqa: E501
    '''get product based on id'''

    product = Product_db.query.filter_by(product_id = prodID).all() #guarda os produtos encontrados

    if product:
        product_schema = ProductSchema(many=True) #criado um objeto do tipo schema
        return product_schema.jsonify(product) #para conseguir converter os dados da bd em json
    else:
        return make_response(
            "Product ID {product_id} not found".format(product_id=prodID), 404
        )


def get_product_by_query():  # noqa: E501
    '''get products based on query'''

    brand = request.args.get('brand')
    name = request.args.get('name')

    if brand:
        products = Product_db.query.filter_by(product_brand = brand).all()
        if not products:
            return make_response(
                "Products of brand {product_brand} not found".format(product_brand=brand), 404
            )
    elif name:
        products = Product_db.query.filter_by(product_name = name).all()
        if not products:
            return make_response(
                "Product with name {product_name} not found".format(product_name=name), 404
            )
    else:
        products = Product_db.query.filter().all()

    product_schema = ProductSchema(many=True)
    return product_schema.jsonify(products)


def post_product():
    #para este caso meter product como param da funcao
    # prodName = product.get('product_name')
    # prodBrand = product.get('product_brand')

    # existing_product = Product_db.query.filter(Product_db.product_name == prodName).filter(Product_db.product_brand == prodBrand).all()

    # if existing_product:
    #     return make_response(
    #         "Product {product_name} {product_brand} already exists".format(product_name=prodName, product_brand=prodBrand), 400
    #     )
    # else:
    #     product_schema = ProductSchema(many=True)
    #     new_product = product_schema.load(product, session=db.session).data
    #     db.session.add(new_product)
    #     db.session.commit()
    #     return product_schema.jsonify(new_product)
    data = request.get_json()
    new_product = Product_db(**data)
    product_schema = ProductSchema()
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)