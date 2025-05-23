from . import main
from flask import render_template, request, redirect, url_for, flash, send_file, Response
from flask_login import login_required, current_user
from ..models import Session, SessionFile, User, ActiveMessageHistory
from ..decorators import email_verified_required, check_for_closed_session
from .. import db
import io
import base64

@main.route('/appointment_uploads')
@login_required
@email_verified_required
@check_for_closed_session
def user_uploads():
    ID = request.args.get("identification")
    open_session = Session.query.get(ID)
    other = open_session.tutor if open_session.tutor != current_user.id else open_session.student
    other = User.query.get(other)
    my_image = base64.b64encode(current_user.image_data).decode('utf-8') if current_user.image_data else None
    other_image = base64.b64encode(other.image_data).decode('utf-8') if other.image_data else None
    other = other.username
    return render_template("user_uploads.html",
                           len = len,
                           recipient = other,
                           my_image=my_image,
                           other_image = other_image,
                           session=open_session,
                           thiss=current_user)

@main.route('/material_upload/<session_id>', methods=['POST'])
def material_upload(session_id):
    session = Session.query.get(session_id)
    data = request.files.get('image')
    if not data:
        flash("Attatch a file first!","danger")
        return redirect(url_for('main.user_uploads',identification=session_id))
    file_data = data.read()
    filename = data.filename
    new_file = SessionFile(filename=filename, file_data=file_data, session=session)
    db.session.add(new_file)
    db.session.commit()
    flash("File added successfully","success")
    return redirect(url_for('main.user_uploads',identification=session_id))

@main.route('/display_file/<int:file_id>')
def display_file(file_id):
    file = SessionFile.query.get(file_id)
    if file.filename.endswith('.png'):
        return Response(file.file_data, mimetype='image/png')
    elif file.filename.endswith('.pdf'):
        return Response(file.file_data, mimetype='application/pdf')
    return redirect(url_for('main.user_uploads'))

@main.route('/download_file/<int:file_id>')
def download_file(file_id):
    file = SessionFile.query.get(file_id)
    return send_file(
        io.BytesIO(file.file_data),
        download_name=file.filename,
        as_attachment=True
    )
