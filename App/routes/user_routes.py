from . import main
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from ..models import User
from ..decorators import email_verified_required, check_for_closed_session
from .. import db
import base64
from datetime import datetime
from PIL import Image
from io import BytesIO

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", "success")
            if not current_user.email_verification_token:
                return redirect(url_for('main.index'))
            return redirect(url_for('main.profile'))
        else:
            flash("Invalid credentials!","danger")
    return render_template("user_handling/login.html")

@main.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Logged out!','success')
    return redirect(url_for('main.login'))

@main.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        username = request.form.get("username")
        if not (name and last_name and email and password and confirm_password and username):
            flash("Please fill in all fields.", "danger")
            return render_template("user_handling/register.html")
        user = User.query.filter_by(username=username).first()
        if user is not None:
            flash("User already exist! Try a different username", "danger")
            return render_template("user_handling/register.html")
        user = User.query.filter_by(email=email).first()
        if user is not None:
            flash("User already exist! Try a different email", "danger")
            return render_template("user_handling/register.html")
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("user_handling/register.html")
        new_user = User(
            name=name,
            last_name=last_name,
            email=email,
            username=username,
            email_verification_token=1
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for('main.login'))
    return render_template("user_handling/register.html")

@main.route('/profile', methods=['POST', 'GET'])
@login_required
@check_for_closed_session
def profile():
    if request.method == 'POST':
        user = User.query.get(current_user.id)
        if 'submit1' in request.form:
            email = request.form.get('email') if user.email_verification_token else user.email
            name = request.form.get('name')
            username = request.form.get('username')
            last_name = request.form.get('last_name')
            user.email = email
            user.username = username
            user.name = name
            user.last_name = last_name
            flash('Account information updated','success')
        elif 'submit2' in request.form:
            password = request.form.get('old_pass')
            if user.check_password(password):
                new_pass = request.form.get('new_pass')
                user.set_password(new_pass)
                flash('Your password has been updated!','success')
            else:
                flash('Current password is not correct', 'warning')
        else:
            data = request.files.get('image')
            img = Image.open(data.stream)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img_square = make_square(img, size=300)
            buffered = BytesIO()
            img_square.save(buffered, format="JPEG")
            image_data = buffered.getvalue()
            user.image_data = image_data
            flash('Profile image changed!','success')
        db.session.commit()
    badges = [i if current_user.qualification_data[i] else None for i in current_user.qualification_data]
    return render_template('profile.html',
                           image_data=base64.b64encode(current_user.image_data).decode('utf-8') if current_user.image_data else None,
                           is_verified=current_user.email_verification_token != None,
                           badges=badges,
                           verified = current_user.email_verification_token == None
                           )

@main.route('/forgot_password')
def forgot_password():
    return render_template('user_handling/forgot_password.html')
