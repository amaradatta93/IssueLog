import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate

from server.config import UPLOAD_FOLDER
from server.config import mail_username, mail_password, mail_server, mail_port, mail_use_ssl
from server.config import username, password, host, db_name
from server.db import db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_FOLDER=UPLOAD_FOLDER,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    app.config.update(
        MAIL_USERNAME=mail_username,
        MAIL_PASSWORD=mail_password,
        MAIL_SERVER=mail_server,
        MAIL_PORT=mail_port,
        MAIL_USE_SSL=mail_use_ssl,
        SQLALCHEMY_DATABASE_URI=f'mysql://{username}:{password}@{host}/{db_name}'
    )

    CORS(app, resources={r"/*": {"origins": "localhost:4200"}})
    JWTManager(app)
    mail = Mail()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate = Migrate(app, db)

    mail.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import views
    app.register_blueprint(views.dashboard)
    app.register_blueprint(views.support_engineers)

    return app
