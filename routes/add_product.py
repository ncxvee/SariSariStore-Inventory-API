from flask import Blueprint, jsonify, request
from products import products

add_product_bp = Blueprint("add_product", __name__)


@add_product_bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data."
        }), 400

    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock")

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            "error": "Product name is required."
        }), 400

    if (isinstance(price, bool) or
        not isinstance(price, (int, float)) or price < 0):
        return jsonify({
            "error": "Price must be a non-negative number."
        }), 400

    if (isinstance(stock, bool) or
        not isinstance(stock, int) or stock < 0):
        return jsonify({
            "error": "Stock must be a non-negative integer."
        }), 400

    new_id = max(
        (p["id"] for p in products),
        default=0
    ) + 1

    new_product = {
        "id": new_id,
        "name": name.strip(),
        "price": float(price),
        "stock": stock
    }

    products.append(new_product)

    return jsonify(new_product), 201