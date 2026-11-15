
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

    updated_data = request.get_json()

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

    # Update product information
    product.update(updated_data)

    return jsonify({
        "message": "Product updated successfully",
        "product": product
    }), 200


if __name__ == '__main__':
    app.run(debug=True)