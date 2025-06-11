from flask import Flask
from routes.auth_routes import auth_bp
from routes.delivery_routes import delivery_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(delivery_bp, url_prefix='/trip')

if __name__ == "__main__":
    app.run()
