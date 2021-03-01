from flask import Flask
from flask_restful import Resource, Api
from product import Product, ProductList

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
api.add_resource(Product, '/product', '/product/<string:name>', endpoint='product')
api.add_resource(ProductList, '/products')

if __name__ == '__main__':
    app.run(debug=True) 