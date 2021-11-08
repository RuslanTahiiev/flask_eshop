from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment
from flask_login import LoginManager
from flask_session import Session
from flask_security import Security, SQLAlchemyUserDatastore


# Database
db = SQLAlchemy()

# Flask Login
login_manager = LoginManager()

# Flask Session
red_session = Session()

# Flask Security
security = Security()


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    assets = Environment()
    app.config.from_object('config.DevConfig')
    from .models import User, Role
    from .forms import LoginForm, SignupForm
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)

    # Init plugins
    db.init_app(app)
    assets.init_app(app)
    login_manager.init_app(app)
    red_session.init_app(app)
    security.init_app(
        app,
        datastore=user_datastore,
        register_blueprint=False,
        login_form=LoginForm,
        register_form=SignupForm
    )

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
