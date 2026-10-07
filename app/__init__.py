from flask import Flask
from flask_cors import CORS
from config import Config
from .extensions import db, jwt, migrate


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from . import models
    from .routes.missoes_routes import missao_bp
    from .routes.auth_routes import auth_bp
    from .routes.herois_routes import herois_bp

    app.register_blueprint(missao_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(herois_bp)


    @app.get("/health")
    def health_check():
        return {
            "status": "online",
            "message": "Hero Management API funcionando",
        }, 200

    return app