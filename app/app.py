from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.update(
        SECRET_KEY="trocar-em-producao",
        SQLALCHEMY_DATABASE_URI="sqlite:///jogadores.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if config:
        app.config.update(config)

    db.init_app(app)

    with app.app_context():
        from . .app.routes import register_routes

        register_routes(app)
        db.create_all()

    return app
