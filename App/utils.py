from .models import User, Periods
from . import db
from datetime import datetime
import json

def flip_bit(user_id:int, day:int, period:int):
    user = User.query.get(user_id)
    binary_data = user.schedule_data
    position = day*8 + period
    byte_array = bytearray(binary_data)
    byte_index = position // 8
    bit_index = 7-position % 8
    byte_array[byte_index] ^= (1 << bit_index)
    byte_data = bytes(byte_array)
    user.schedule_data = byte_data
    db.session.commit()
    return 1

def initialize_period_data():
    if not Periods.query.first():
        for _ in range(0,6):
            newThing = Periods()
            db.session.add(newThing)
        db.session.commit()

def temp_function_for_default_user_loading():
    from .models import User, Periods
    if not User.query.first():
        user1 = User(
            username = "Student1",
            name = "Ben",
            last_name = "Lozzano",
            email = "benlozzano@gmail.com",
            email_verification_token=None,
            role = 0
        )
        user1.set_password("s")
        db.session.add(user1)
        db.session.commit()

        user2 = User(
            username = "Admin",
            name = "Ben2",
            last_name = "Lozzano2",
            email = "benloz25@bergen.org",
            email_verification_token=None,
            role = 3
        )
        user2.set_password("s")

        user3 = User(
            username = "Teacher",
            name = "Bean",
            last_name = "Lasanga",
            email = "bean_lasanga@gmail.com",
            email_verification_token=None,
            role = 2
        )
        user3.set_password("s")

        user4 = User(
            username = "NHS Student",
            name = "Bacon",
            last_name = "Burrido",
            email = "america@gmail.com",
            email_verification_token=None,
            volunteer_hours=0,
            role = 1,
            qualification_data = json.loads('{"Math": 1, "Algebra": 0, "Science": 0, "Chemistry": 0, "Gym": 0, "Geometry": 0, "Biomolecular Quantum Physics": 0, "English": 0}')
        )
        user4.set_password("s")
        period1 = Periods.query.first()
        period1.monday = " 4"
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user4)
        db.session.commit()

def temp_admin_loading_delete_later():
    from .models import User
    if not User.query.first():
        user1 = User(
            username = "Ms. Genicoff",
            name = "Sharon",
            last_name = "Genicoff",
            email = "shagen@bergen.org",
            email_verification_token=None,
            role = 1
        )
        user1.set_password("Demo1")
        db.session.add(user1)
        db.session.commit()

        user2 = User(
            username = "Mr. Pena",
            name = "Carlos",
            last_name = "Pena",
            email = "carpen@bergen.org",
            email_verification_token=None,
            role = 3
        )
        user2.set_password("Demo1")

        user3 = User(
            username = "Ms. Kendall",
            name = "Monet",
            last_name = "Kendall",
            email = "monken@bergen.org",
            email_verification_token=None,
            role = 3
        )
        user3.set_password("Demo1")

        user4 = User(
            username = "Ms. Mak",
            name = "Cynthia",
            last_name = "Mak",
            email = "cynmak@bergen.org",
            email_verification_token=None,
            role = 3,
        )
        user4.set_password("Demo1")
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user4)
        db.session.commit()

def add_new_session(tutor_id,student_id,date,period,start_time, end_time,request,repeating):
    from .models import ActiveMessageHistory, Session, SessionRequest
    from .utils import weekday
    year, month, temp_day = (int(i) for i in date.split('-'))
    dayNumber = weekday(year, month, temp_day)
    if request:
        new_session = SessionRequest(
            tutor = tutor_id,
            start_time = start_time,
            end_time = end_time,
            student = student_id,
            period = period,
            start_date = datetime.today(),
            day_of_the_week = dayNumber,
            date = datetime.strptime(date, '%Y-%m-%d').date(),
            time_confirmation_pending = tutor_id
        )
        db.session.add(new_session)
    else:
        conversation = ActiveMessageHistory(
            people = {tutor_id:'',student_id:''},
            missed = {'total':0,tutor_id:0,student_id:0}
        )
        db.session.add(conversation)
        db.session.commit()
        new_session = Session(
            tutor = tutor_id,
            start_time = start_time,
            end_time = end_time,
            student = student_id,
            period = period,
            start_date = datetime.today(),
            day_of_the_week = dayNumber,
            date = datetime.strptime(date, '%Y-%m-%d').date(),
            message_history_id = conversation.id,
            recurring = repeating
        )
        db.session.add(new_session)
    db.session.commit()

def remove_session(session_id):
    from .models import Session, SessionFile, ActiveMessageHistory
    session = Session.query.get(session_id)
    session_files = SessionFile.query.filter_by(session_id = session_id).all()
    message_history = ActiveMessageHistory.query.get(session.message_history_id)
    for files in session_files:
        db.session.delete(files)
    db.session.delete(message_history)
    db.session.delete(session)
    db.session.commit()
