from flask import Blueprint, jsonify, request
from products import products

manage_product_bp = Blueprint("manage_product", __name__)


@manage_product_bp.route('/products/<int:product_id>', methods=['PATCH'])
def update_product(product_id):
    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )

    if product is None:
        return jsonify({
            "error": f"Product with ID {product_id} not found."
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data."
        }), 400

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return jsonify({
                "error": "Product name must not be empty."
            }), 400

    if "price" in data:
        price = data["price"]

        if (isinstance(price, bool) or
            not isinstance(price, (int, float)) or price < 0):
            return jsonify({
                "error": "Price must be a non-negative number."
            }), 400

    if "stock" in data:
        stock = data["stock"]

        if (isinstance(stock, bool) or
            not isinstance(stock, int) or stock < 0):
            return jsonify({
                "error": "Stock must be a non-negative integer."
            }), 400

    if "name" in data:
        product["name"] = data["name"].strip()

    if "price" in data:
        product["price"] = float(data["price"])

    if "stock" in data:
        product["stock"] = data["stock"]

    return jsonify(product), 200


@manage_product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )

    if product is None:
        return jsonify({
            "error": f"Product with ID {product_id} not found."
        }), 404

    products.remove(product)

    return jsonify({
        "message": f"Product with ID {product_id} deleted successfully."
    }), 200
