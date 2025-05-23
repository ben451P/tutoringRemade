from flask import request, url_for, flash, redirect
from flask_mail import Message
from . import mail, db
import secrets

def generate_verification_token():
    return secrets.token_urlsafe(16)

def send_verification_email_to(user):
    token = generate_verification_token()
    user.email_verification_token = token
    db.session.commit()
    verification_link = request.url_root + f"/verify_email/{token}"
    msg = Message("Verify Your Email!", recipients=[user.email])
    msg.body = f"Click the following link to verify your email: {verification_link}"
    mail.send(msg)
