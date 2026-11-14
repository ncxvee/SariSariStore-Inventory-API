from flask import Flask, jsonify, request
from products import products

app = Flask(__name__)

# GET: Retrieve all products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)


# POST: Add a new product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must contain valid JSON"}), 400

    required_fields = ["name", "price", "stock"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    name = data["name"]

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Product name must not be empty"}), 400

    price = data["price"]

    if isinstance(price, bool) or not isinstance(price, (int, float)):
        return jsonify({"error": "Price must be a number"}), 400

    import math

    if not math.isfinite(price) or price <= 0:
        return jsonify({"error": "Price must be greater than zero"}), 400

    stock = data["stock"]

    if isinstance(stock, bool) or not isinstance(stock, int) or stock < 0:
        return jsonify({"error": "Stock must be a non-negative integer"}), 400

    new_id = max((product["id"] for product in products), default=0) + 1

    new_product = {
        "id": new_id,
        "name": name.strip(),
        "price": price,
        "stock": stock
    }

    products.append(new_product)

    return jsonify({
        "message": "Product added successfully",
        "product": new_product
    }), 201


if __name__ == '__main__':
    app.run(debug=True)