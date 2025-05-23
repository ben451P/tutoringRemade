from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response, send_file
from flask_login import login_required, current_user
from .models import User, Session, SessionRequest, ActiveMessageHistory, SessionFile, Feedback, Periods
from .decorators import email_verified_required, check_for_closed_session, admin_only
from .utils import flip_bit, initialize_period_data, temp_function_for_default_user_loading, temp_admin_loading_delete_later, add_new_session, remove_session
from .email_utils import send_verification_email_to
from sqlalchemy.orm.attributes import flag_modified
import base64
import io

main = Blueprint("main", __name__)

@main.app_context_processor
def inject_profile_image():
    included_endpoints = ['index','find_session','user_messages','scheduler','profile','admin_temp_route','tag_managing','user_managing','approve_hours','view','user_uploads']
    current_endpoint = request.endpoint
    if current_endpoint not in included_endpoints:
        return {}
    profile_image = base64.b64encode(current_user.image_data).decode('utf-8') if current_user.image_data else None
    return {'profile_image':profile_image}

# This file is now obsolete. All routes are organized in the App/routes/ package as per the project structure PDF.
