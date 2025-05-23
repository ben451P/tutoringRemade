from functools import wraps
from flask import flash, redirect, url_for, request
from flask_login import current_user

def email_verified_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.email_verification_token:
            return f(*args, **kwargs)
        else:
            flash("You need to verify your email to access this page.", "warning")
            return redirect(url_for('profile'))
    return decorated_function

def check_for_closed_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.marked:
            params = {"id":current_user.marked,"form":"0","cancel_reason":"4"}
            return redirect(url_for("complete_session",**params))
        return f(*args,**kwargs)
    return decorated_function

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role >= 2:
            return f(*args, **kwargs)
        else:
            flash("You do not have the authority to access this page.", "danger")
            return redirect(url_for('index'))
    return decorated_function
