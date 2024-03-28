from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS # Importing cors here 
import json
import os

app = Flask(__name__) 
CORS(app) # Here, we enable CORS for all domains on all routes

def load_products():
    with open ('products.json', 'r') as f:
        return json.load(f)['products']
    
@app.route('/products', methods = ['GET'])
@app.route('/products/<int:product_id>', methods = ['GET'])
def get_products(product_id = None):
    products = load_products()
    if product_id is None:
        return jsonify({"products": products})
    else:
        product = next((p for p in products if p['id'] == product_id), None)
        return jsonify(product) if product else ('', 404)
    
@app.route('/products/add', methods = ['POST'])
def add_product():
    new_product = request.json
    products = load_products()
    new_product['id'] = len(products) + 1
    products.append(new_product)
    with open('products.json', 'w') as f:
        json.dump({"products": products}, f)
    return jsonify(new_product), 201

@app.route('/product-images/<path:filename>')
def get_image(filename):
    return send_from_directory('product-images', filename)

@app.route('/products/<int:product_id>', methods = ['PUT'])
def update_product(product_id):
    products = load_products()
    updated_version = request.json
    #if p['id'] == product_id:
    product = next((p for p in products if p['id'] == product_id), None)
    if (product_id == None):
        return jsonify('', 404)
    else:
        product.update(updated_version)
        # open the product.json and write the products
        with open('products.json', 'w') as f:
            json.dump({"products": products}, f)
        return jsonify(updated_version), 201

@app.route('/products/<int:product_id>', methods = ['DELETE'])
def remove_product(product_id):
    products = load_products()
    product_index = next((index for index, p in enumerate(products) if p['id'] == product_id), None)
    if product_index is None:
        return jsonify({'error' : 'Product not found.'}), 404
    
    del products[product_index]

    with open('products.json', 'w') as f:
        json.dump({"products": products}, f)
    
    return jsonify({'message' : 'Product successfully deleted.'}), 200

if __name__ == '__main__':
    app.run(debug = True)
