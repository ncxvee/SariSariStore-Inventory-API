from flask import Flask, jsonify
from products import products

app = Flask(__name__)

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

<<<<<<< Updated upstream
#Mitchie: get product by id
=======
#Mitchie: Get one product by ID
>>>>>>> Stashed changes
@app.route('/products/<int:product_id>', methods=['GET'])
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

<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
if __name__ == '__main__':
    app.run(debug=True)
