from flask import Flask

from config import Config

from .extensions import db, jwt, migrate


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from . import models

    @app.get("/health")
    def health_check():
        return {
            "status": "online",
            "message": "Hero Management API funcionando",
        }, 200

    return app