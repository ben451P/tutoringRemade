from . import main
from flask import render_template, request, redirect, url_for, flash, jsonify, Response, send_file
from flask_login import login_required, current_user
from ..models import Session, SessionRequest, ActiveMessageHistory, SessionFile, User
from ..decorators import email_verified_required, check_for_closed_session
from ..utils import add_new_session, remove_session
from .. import db
import base64
import io
from sqlalchemy.orm.attributes import flag_modified
from datetime import datetime

@main.route('/appointment_messages')
@login_required
@email_verified_required
@check_for_closed_session
def user_messages():
    ID = request.args.get('identification')
    open_session = Session.query.get(ID)
    message_history = ActiveMessageHistory.query.get(open_session.message_history_id)
    message_history.missed[str(current_user.id)] = message_history.missed['total']
    flag_modified(message_history,'missed')
    db.session.commit()
    other = open_session.tutor if open_session.tutor != current_user.id else open_session.student
    other = User.query.get(other)
    my_image = base64.b64encode(current_user.image_data).decode('utf-8') if current_user.image_data else None
    other_image = base64.b64encode(other.image_data).decode('utf-8') if other.image_data else None
    other = other.username
    messages = message_history.messages['list']
    messages = [{'mine': True if i['sender'] == current_user.id else False,'message':i['message'],'sender':User.query.get(i['sender']).username}  for i in messages]
    return render_template('user_messages.html',
                           recipient = other,
                           my_image=my_image,
                           other_image = other_image,
                           session=open_session,
                           thiss=current_user,
                           messages=messages)

@main.route('/appointment_overview', methods=['POST', 'GET'])
@login_required
@email_verified_required
@check_for_closed_session
def user_overview():
    ID = request.args.get("identification")
    if request.method == "POST":
        id = request.form["id"]
        return redirect(f'/terminate_session?identification={id}')
    open_session = Session.query.get(ID)
    other_user = User.query.get(open_session.tutor) if current_user.role == 0 else User.query.get(open_session.student)
    other_user_image = base64.b64encode(other_user.image_data).decode('utf-8') if other_user.image_data else None
    return render_template("user_overview.html",session=open_session,other=other_user,other_image = other_user_image,role=current_user.role)

@main.route('/appointment_preview', methods=['POST', 'GET'])
@login_required
@email_verified_required
@check_for_closed_session
def user_preview():
    ID = request.args.get("identification")
    open_session = SessionRequest.query.get(ID)
    other_user = User.query.get(open_session.tutor) if current_user.role == 0 else User.query.get(open_session.student)
    other_user_image = base64.b64encode(other_user.image_data).decode('utf-8') if other_user.image_data else None
    period = None # period_converter[open_session.period] # You may need to import period_converter
    if request.method == "POST":
        id = request.form["id"]
        submit = int(request.form["submit"])
        if submit == 1:
            return redirect(url_for("main.confirm_appointment",id=id))
        if submit == 0:
            return redirect(f'/delete_session/{id}?pre=1')
        start_time = request.form.get("start_time").split(":")
        end_time = request.form.get("end_time").split(':')
        start_time = f"{start_time[0]}:{start_time[1]}"
        end_time = f"{end_time[0]}:{end_time[1]}"
        # start_time = string_to_time(start_time)
        # end_time = string_to_time(end_time)
        if open_session.start_time == start_time and open_session.end_time == end_time:
            open_session.time_confirmation_pending = -1
        else:
            open_session.time_confirmation_pending = other_user.id
            open_session.start_time = start_time
            open_session.end_time = end_time
        db.session.commit()
    return render_template("user_preview.html",session=open_session,other=other_user,other_image = other_user_image,type=current_user.role,period=period, confirm = open_session.time_confirmation_pending == current_user.id,confirmed = open_session.time_confirmation_pending == -1)

@main.route('/create_request')
def create_request():
    return render_template('create_request.html')

@main.route('/session_hindsight', methods=['GET', 'POST'])
def session_hindsight():
    id = request.args.get("identification")
    if request.method == "POST":
        feedback = request.form.get("feedback_text")
        repeating = int(request.form.get("repeating_session"))
        session = Session.query.get(id)
        session.session_history['sessions'] += 1
        session.session_history['descriptions'].append(feedback)
        flag_modified(session, 'session_history')
        if repeating:
            pass
        else:
            pass
    return render_template("session_hindsight.html",id=id)
