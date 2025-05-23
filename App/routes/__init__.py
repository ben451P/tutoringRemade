# This file initializes the routes package and registers all blueprints.
from flask import Blueprint
import os

main = Blueprint('main', __name__, template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../templates')))

# Import and register all route modules here
from . import user_routes, session_routes, admin_routes, file_routes, notification_routes, misc_routes
