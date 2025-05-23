from . import main
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from ..decorators import email_verified_required, check_for_closed_session

@main.route('/welcome')
def welcome():
    return render_template('welcome.html')

@main.route('/index.html')
def reroute_user():
    return redirect(url_for('main.index'))

@main.route('/')
def index():
    if not current_user or not getattr(current_user, 'is_authenticated', False):
        return redirect(url_for('main.login'))
    # You may want to add your homepage logic here, e.g.:
    # if current_user.role == 0:
    #     return render_template('homepages/student.html')
    # elif current_user.role == 1:
    #     return render_template('homepages/nhs.html')
    # elif current_user.role == 2:
    #     return render_template('homepages/teacher.html')
    # elif current_user.role == 3:
    #     return render_template('homepages/admin.html')
    return render_template('homepages/old.html')

# Add error handlers and other miscellaneous routes here
