from flask import Blueprint, jsonify
from products import products

get_products_bp = Blueprint("get_products", __name__)


@get_products_bp.route('/products', methods=['GET'])
def get_products():
    return jsonify(products), 200