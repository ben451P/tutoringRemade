from . import db, login_manager
from flask_login import UserMixin
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm.attributes import flag_modified
from .defaults import load_default_notifactions, current_classlist, load_student_teacher_JSON, load_basic_json_file, load_non_basic_json_file, load_session_history_JSON
from werkzeug.security import generate_password_hash, check_password_hash
import json

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255),unique=True)
    name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email_verification_token = db.Column(db.String(255))
    schedule_data = db.Column(db.LargeBinary(8), default=b'\x00' * 8)
    notifaction_data = db.Column(JSON, default=load_default_notifactions)
    hours_of_service = db.Column(db.Float, default = 0.0)
    status = db.Column(db.String, default='')
    image_data = db.Column(db.LargeBinary)
    qualification_data = db.Column(JSON,default=current_classlist)
    volunteer_hours = db.Column(db.Integer,default=0)
    student_teacher_data = db.Column(JSON, default = load_student_teacher_JSON)
    role = db.Column(db.Integer, default = 0)
    marked = db.Column(db.Integer, default = 0)
    sessions = db.relationship('Session', backref='user', lazy = True)
    feedbacks = db.relationship('Feedback', backref='user', lazy = True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class ActiveMessageHistory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    people = db.Column(JSON, default=load_basic_json_file)
    messages = db.Column(JSON, default=load_non_basic_json_file)
    missed = db.Column(JSON, default=load_basic_json_file)
    session = db.relationship('Session', backref='active_message_history', lazy = True)

class MessageLogs(db.Model):
    __bind_key__ = "records_db"
    id = db.Column(db.Integer, primary_key = True)
    people = db.Column(JSON, default=load_basic_json_file)
    messages = db.Column(JSON, default=load_non_basic_json_file)
    session = db.Column(db.Integer,nullable=False)

class SessionLog(db.Model):
    __bind_key__ = "records_db"
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    day_of_the_week = db.Column(db.Integer)
    date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    subject = db.Column(db.String(255))
    tutor = db.Column(db.Integer, nullable = False) 
    student = db.Column(db.Integer, nullable = False)
    period = db.Column(db.Integer)
    cancel_reason = db.Column(db.Integer)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    day_of_the_week = db.Column(db.Integer)
    date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    subject = db.Column(db.String(255))
    tutor = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    student = db.Column(db.Integer, nullable = False)
    period = db.Column(db.Integer)
    session_history = db.Column(JSON, default = load_session_history_JSON)
    message_history_id = db.Column(db.Integer, db.ForeignKey('active_message_history.id'))
    closed = db.Column(db.Boolean, default = False)
    recurring = db.Column(db.Boolean, default = False)
    
    files = db.relationship('SessionFile', back_populates='session', cascade='all, delete-orphan')

class SessionRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    day_of_the_week = db.Column(db.Integer)
    date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    subject = db.Column(db.String(255))
    tutor = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    student = db.Column(db.Integer, nullable = False)
    period = db.Column(db.Integer)
    time_confirmation_pending = db.Column(db.Integer, nullable=False)

class SessionFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    file_data = db.Column(db.LargeBinary)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)

    session = db.relationship('Session', back_populates='files')

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exists = db.Column(db.Boolean, nullable=False)
    on_time = db.Column(db.Integer, nullable=True)
    understanding = db.Column(db.Integer, nullable=True)
    date = db.Column(db.String(255), nullable=True)
    review_text = db.Column(db.String(255), nullable=True)
    subject = db.Column(db.String(255), nullable=True)
    tutoring = db.Column(db.Boolean, nullable=True)
    review_for = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    review_from = db.Column(db.String(255), nullable = False)

class Periods(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    monday = db.Column(db.String(256), default = '')
    tuesday = db.Column(db.String(256), default = '')
    wednesday = db.Column(db.String(256), default = '')
    thursday = db.Column(db.String(256), default = '')
    friday = db.Column(db.String(256), default = '')
