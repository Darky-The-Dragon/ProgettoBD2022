from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'gianniepinotto'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:gianniepinotto@localhost:5432/progettobd'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # we need to define where the roots are:
    from .views import views
    from .auth import auth
    from .song import song
    from. dashboard import dashboard
    from .add_album import add_album
    from .add_song import add_song
    from .user import user
    from .searched import searched

    # We register the blueprint:
    app.register_blueprint(user, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(song, url_prefix='/')
    app.register_blueprint(dashboard, url_prefix='/')
    app.register_blueprint(add_album, url_prefix='/')
    app.register_blueprint(add_song, url_prefix='/')
    app.register_blueprint(searched, url_prefix='/')
    # Script that checks before we run the server every time if we created the database
    from .models import User, Note

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # This tells flask how to load the user
    @login_manager.user_loader
    def load_user(id):
        # This looks for the primary key
        return User.query.get(int(id))

    db.create_all(app=app)

    return app
