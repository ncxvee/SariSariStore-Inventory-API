
from flask import Flask, jsonify, request
from products import products

app = Flask(__name__)


# GET ALL PRODUCTS
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)
from flask import Flask

from routes.get_products import get_products_bp
from routes.get_product_by_id import get_product_by_id_bp
from routes.add_product import add_product_bp
from routes.manage_product import manage_product_bp

app = Flask(__name__)

app.register_blueprint(get_products_bp)
app.register_blueprint(get_product_by_id_bp)
app.register_blueprint(add_product_bp)
app.register_blueprint(manage_product_bp)



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