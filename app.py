from flask import Flask, jsonify
from products import products

app = Flask(__name__)

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)