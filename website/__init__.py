from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Darky12092000!'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Darky12092000!@localhost/ProgettoBD'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # we need to define where the roots are:
    from .views import views
    from .auth import auth
    from .user import user

    # We register the blueprint:
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')

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
