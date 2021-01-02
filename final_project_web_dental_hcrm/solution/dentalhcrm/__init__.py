from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dentalhcrm.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from dentalhcrm.public.routes import public
    app.register_blueprint(public)

    from dentalhcrm.user.routes import user
    app.register_blueprint(user)
    
    from dentalhcrm.member.routes import member
    app.register_blueprint(member)
    
    from dentalhcrm.errors.handlers import errors
    app.register_blueprint(errors)

    return app
