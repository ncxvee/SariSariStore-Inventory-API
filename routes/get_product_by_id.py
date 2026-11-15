from flask import Blueprint, jsonify
from products import products

get_product_by_id_bp = Blueprint("get_product_by_id", _name_)

@get_product_by_id_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )

    if product is None:
        return jsonify({
            "error": f"Product with ID {product_id} not found."
        }), 404

    return jsonify(product), 200
