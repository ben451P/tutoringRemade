from . import main
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User
from ..decorators import email_verified_required, admin_only, check_for_closed_session
from .. import db

@main.route('/admin_temp_route', methods=['POST', 'GET'])
def admin_temp_route():
    if request.method == "POST":
        from random import randint, sample
        number = int(request.form.get("number"))
        if number <= 0:
            flash("The number has to be above 0","danger")
            return render_template("admin_temp_route.html")
        if int(request.form.get("submit")):
            if len(User.query.filter_by(role=1).all()) == 0 or len(User.query.filter_by(role=0).all()) == 0:
                flash("Insert some students and tutors first","warning")
                return redirect(url_for("main.admin_temp_route"))
            # ...rest of your admin_temp_route logic...
    return render_template('admin_temp_route.html')

@main.route('/user_managing', methods=['POST', 'GET'])
@login_required
@email_verified_required
@admin_only
@check_for_closed_session
def user_managing():
    if request.method == 'POST':
        promoted_user = request.form.get('promoted_user')
        rank = request.form.get('role')
        user = User.query.get(int(promoted_user))
        user.role = int(rank)
        db.session.commit()
    people = User.query.all()
    people = [i for i in people if i.role < 3]
    return render_template('user_handling/user_managing.html',people=people)

@main.route('/tag_managing', methods=['POST', 'GET'])
@login_required
@email_verified_required
@admin_only
@check_for_closed_session
def tag_managing():
    NHS_students = User.query.filter_by(role=1).all()
    return render_template('user_handling/tag_managing.html', NHSs=NHS_students)

@main.route('/approve_hours')
@login_required
@email_verified_required
@admin_only
def approve_hours():
    # ...original approve_hours logic from app.py...
    pass

# Add other admin/management routes here
