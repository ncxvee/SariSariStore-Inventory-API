
from flask import Flask, jsonify, request
from products import products

app = Flask(__name__)


# GET ALL PRODUCTS
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)


# PUT UPDATE PRODUCT
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):

    updated_data = request.get_json(silent=True)

    # Check if request contains JSON data
    if not isinstance(updated_data, dict) or not updated_data:
        return jsonify({
            "error": "Please provide product information"
        }), 400

    # Find product using its ID
    product = next(
        (item for item in products
         if item["id"] == product_id),
        None
    )

    # Check if product exists
    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    # Allowed fields to update
    allowed_fields = ["name", "price", "stock"]

    # Check for invalid fields
    invalid_fields = [
        field for field in updated_data
        if field not in allowed_fields
    ]

    if invalid_fields:
        return jsonify({
            "error": "Invalid fields",
            "invalid_fields": invalid_fields
        }), 400

    # Validate updated values
    for field, value in updated_data.items():

        if field == "name":
            if not isinstance(value, str) or not value.strip():
                return jsonify({
                    "error": "Invalid product name"
                }), 400

        elif field == "price":
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
                return jsonify({
                    "error": "Price must be a non-negative number"
                }), 400

        elif field == "stock":
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                return jsonify({
                    "error": "Stock must be a non-negative integer"
                }), 400

    # Update product information
    product.update(updated_data)

    return jsonify({
        "message": "Product updated successfully",
        "product": product
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
