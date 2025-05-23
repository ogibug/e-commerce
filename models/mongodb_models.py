from flask_pymongo import PyMongo

mongo = PyMongo()

def get_all_products():
    products = mongo.db.products.find()
    return products

def add_product(name, description, price):
    mongo.db.products.insert_one({
        'name': name,
        'description': description,
        'price': price
    })
