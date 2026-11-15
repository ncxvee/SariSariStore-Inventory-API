from flask import Flask

from routes.get_products import get_products_bp
from routes.add_product import add_product_bp

app = Flask(__name__)

app.register_blueprint(get_products_bp)
app.register_blueprint(add_product_bp)


if __name__ == '__main__':
    app.run(debug=True)