from flask import Flask
from application.extensions import db
from application.routes import blue_prints

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    for print in blue_prints:
        app.register_blueprint(print)

    with app.app_context():
        db.create_all()

    return app
