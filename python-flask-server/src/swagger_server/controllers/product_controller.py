import requests
import connexion
import sqlalchemy
from swagger_server.models.db_model import Product as Product_db, engine
from flask import jsonify, make_response, request

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

def delete_product():  # noqa: E501
    '''delete products based on query'''
    headers = {'token': request.headers['token'], 'email': request.headers['email']}
    r = requests.get('http://localhost:5000/auth', headers=headers)
    if r.status_code != 200:
        return make_response(
            "Not authenticated", r.status_code
        )

    brand = request.args.get('brand') #obtem o input do user localhost:8080/v1/products?brand=Nike
    name = request.args.get('name') #localhost:8080/v1/products?name=Reebok+Classic98

    if brand: #se tiver sido usado como query a brand
        products = Product_db.query.filter_by(product_brand = brand).all() #obtem todos os produtos dessa brand

        if not products: #se nao existirem
            return make_response(
                "Products of brand {product_brand} not found".format(product_brand=brand), 404
            )

        Product_db.query.filter_by(product_brand = brand).delete() #se existirem sao apagados
        session.commit() #atualiza a bd
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
        session.commit()
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
    headers = {'token': request.headers['token'], 'email': request.headers['email']}
    r = requests.get('http://localhost:5000/auth', headers=headers)
    if r.status_code != 200:
        return make_response(
            "Not authenticated", r.status_code
        )

    product = Product_db.query.filter_by(product_id = prodID).all() #verifica a existencia de um produto com esse id

    if product: #caso exista
        Product_db.query.filter_by(product_id = prodID).delete()  #apaga-o da bd
        session.commit() #atualiza a bd
        return make_response(
            "Product with ID {product_id} deleted".format(product_id=prodID), 200
        )
    else: #caso nao exista
        return make_response(
            "Product ID {product_id} not found".format(product_id=prodID), 404
    )


def get_product_by_id(prodID):  # noqa: E501
    '''get product based on id'''
    headers = {'token': request.headers['token'], 'email': request.headers['email']}
    r = requests.get('http://localhost:5000/auth', headers=headers)
    if r.status_code != 200:
        return make_response(
            "Not authenticated", r.status_code
        )

    product = Product_db.query.filter_by(product_id = prodID).all() #guarda os produtos encontrados

    if product:
        return product.as_dict()
        # product_schema = ProductSchema(many=True) #criado um objeto do tipo schema
        # return product_schema.jsonify(product) #para conseguir converter os dados da bd em json
    else:
        return make_response(
            "Product ID {product_id} not found".format(product_id=prodID), 404
        )


def get_product_by_query():  # noqa: E501
    '''get products based on query'''
    headers = {'token': request.headers['token'], 'email': request.headers['email']}
    r = requests.get('http://auth.k3s/auth', headers=headers)
    if r.status_code != 200:
        return make_response(
            "Not authenticated", r.status_code
        )

    brand = request.args.get('brand')
    name = request.args.get('name')

    if brand:
        products = session.query(Product_db).filter_by(product_brand = brand).all()
        if not products:
            return make_response(
                "Products of brand {product_brand} not found".format(product_brand=brand), 404
            )
    elif name:
        products = session.query(Product_db).filter_by(product_name = name).all()
        if not products:
            return make_response(
                "Product with name {product_name} not found".format(product_name=name), 404
            )
    else:
        products = session.query(Product_db).filter().all()

    return jsonify([ prod.as_dict() for prod in products])
    #product_schema = ProductSchema(many=True)
    #return product_schema.jsonify(products)


def post_product():
    # headers = {'token': request.headers.get('token'), 'email': request.headers.get('email')}
    # r = requests.get('http://localhost:5000/auth', headers=headers)
    # if r.status_code != 200:
    #     return make_response(
    #         "Not authenticated", r.status_code
    #     )
    data = request.get_json(force=True)
    print(data)
    print("--------")
    new_product = Product_db(brand=data['brand'], name=data['name'], price=data['price'], stock=data['stock'])
    #product_schema = ProductSchema()
    session.add(new_product)
    session.commit()
    return make_response("done", 201)
    #return product_schema.jsonify(new_product)
