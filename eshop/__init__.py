from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment
from flask_login import LoginManager
from flask_session import Session

db = SQLAlchemy()
login_manager = LoginManager()
red_session = Session()


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    assets = Environment()
    app.config.from_object('config.DevConfig')

    # Init plugins
    db.init_app(app)
    assets.init_app(app)
    login_manager.init_app(app)
    red_session.init_app(app)

    with app.app_context():
        #
        from .auth import routes
        from . import routes

        # Blueprints
        app.register_blueprint(auth.routes.auth_bp)

        from .assets import compile_assets

        # Assets
        compile_assets(assets)

        # Database
        db.create_all()

        return app
