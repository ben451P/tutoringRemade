from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_socketio import SocketIO

# Extensions
socketio = SocketIO()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
    app.config["SQLALCHEMY_BINDS"] = {
        "records_db": "sqlite:///records_library.db"
    }
    app.config['SESSION_COOKIE_NAME'] = 'Session_Cookie'
    app.config['SESSION_COOKIE_PATH'] = '/'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
    app.config['SESSION_PERMANENT'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = "ben_sucks"
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = "oscarjepsen2007@gmail.com"
    app.config['MAIL_PASSWORD'] = "agda kzab akxo blpa"
    app.config['MAIL_DEFAULT_SENDER'] = "oscarjepsen2007@gmail.com"

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)

    # Import models to ensure user_loader is registered
    from App import models

    # Import and register blueprints/routes
    from App.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
