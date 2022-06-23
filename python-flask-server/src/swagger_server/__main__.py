#!/usr/bin/env python3
import connexion
import os
from swagger_server import encoder
from swagger_server.models.db_model import engine, Base
from flask_cors import CORS

def main():
    Base.metadata.create_all(engine)
    basedir = os.path.abspath(os.path.dirname(__file__))
    application = connexion.FlaskApp(__name__, specification_dir='./swagger/')
    application.app.json_encoder = encoder.JSONEncoder
    application.add_api('swagger.yaml', arguments={'title': 'Product'})
    app = application.app
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()
