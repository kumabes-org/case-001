from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
import os
from decimal import Decimal


DB_USERNAME=os.getenv("DB_USERNAME")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_HOSTNAME=os.getenv("DB_HOSTNAME")
DB_NAME=os.getenv("DB_NAME")


banco = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}?charset=utf8mb4&collation=utf8mb4_unicode_ci'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
    

class ProductModel(banco.Model):
    __tablename__ = 'products'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_collate": "utf8_unicode_ci",
        "mysql_charset": "utf8",
    }
    
    id = banco.Column(banco.Integer, primary_key=True)
    name = banco.Column(banco.String(160,collation='utf8_unicode_ci'))
    description = banco.Column(banco.String(160,collation='utf8_unicode_ci'))
    price = banco.Column(banco.Numeric(18,2))
    quantity = banco.Column(banco.Integer)

    def __init__(self, id, name, description, price, quantity):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": json.dumps(self.price, cls=JSONEncoder),
            "quantity": self.quantity
        }

    @classmethod
    def retrieve(cls, id):
        product = cls.query.filter_by(id=id).first()
        if product:
            return product
        else:
            return None    

class Product(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('id')
    argumentos.add_argument('name')
    argumentos.add_argument('description')
    argumentos.add_argument('price')
    argumentos.add_argument('quantity')

    def get(self, id):
        product = ProductModel.retrieve(id)
        if product:
            return product.json()
        return {'message': 'Product not found!'}, 404    

class Products(Resource):
    def get(self):
        products = []
        products_from_db = ProductModel.query.all()
        for product in products_from_db:            
            products.append(product.json())
            
        return products

api.add_resource(Products, "/api/v1/products")
api.add_resource(Product, "/api/v1/products/<int:id>")

if __name__ == '__main__':
  banco.init_app(app)
  app.run(debug=True)