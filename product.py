from flask_restful import Resource, reqparse
import sqlite3

class Product(Resource):
    TABLE_NAME = 'products'

    parser = reqparse.RequestParser()
    parser.add_argument('product_name', type=str, required=True, help="This field cannot be left blank!" )
    parser.add_argument('product_description', type=str, required=True, help="This field cannot be left blank!" )
    parser.add_argument('product_price', type=int, required=True, help="This field cannot be left blank!" )
    
    def get(self, name):
        product = self.find_by_name(name)
        if product:
            return product
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE product_name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'product': {'product_name': row[1], 'product_description': row[2], 'product_price': row[3]}}

    def post(self):
        data = Product.parser.parse_args()
        product = {
            'product_name': data['product_name'], 
            'product_description': data['product_description'],
            'product_price': data['product_price']
        }
        if self.find_by_name(product['product_name']):
            return {'message': "An product with name '{}' already exists.".format(product['product_name'])}      

        try:
            Product.insert(product)
        except:
            return {"message": "An error occurred inserting the product."}

        return product

    @classmethod
    def insert(cls, product):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(NULL, ?, ?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (product['product_name'], product['product_description'], product['product_price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE product_name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Product deleted'}

    def put(self, name):
        data = Product.parser.parse_args()
        product = self.find_by_name(name)
        updated_product = { 
            'product_name': name,
            'product_description': data['product_description'],
            'product_price': data['product_price']
        }
        if product is None:
            try:
                Product.insert(updated_product)
            except:
                return {"message": "An error occurred updating the product."}
        else:
            try:
                Product.update(updated_product)
            except:
                return {"message": "An error occurred updating the product."}
        return updated_product

    @classmethod
    def update(cls, product):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE {table} SET product_description=?, product_price=? WHERE product_name=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (product['product_description'], product['product_price'], product['product_name']))

        connection.commit()
        connection.close()


class ProductList(Resource):
    TABLE_NAME = 'products'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        products = []
        for row in result:
            products.append({'product_name': row[1], 'product_description': row[2], 'product_price': row[3]})
        connection.close()

        return {'products': products}
