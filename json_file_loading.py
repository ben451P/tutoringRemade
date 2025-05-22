import json
from datetime import time, datetime, timedelta
from calendar import weekday
from PIL import Image



user_type_key = {0:'student', 1:'teacher', 2:'administrator', 3:'developer'}

def load_session_history_JSON():
    with open('static/assets/session_history_JSON.json', 'r') as file:
        form = json.load(file)
    return form

def load_basic_json_file():
    with open('static/assets/basic_json_file.json', 'r') as file:
        basic = json.load(file)
    return basic

def load_default_schedule():
    with open('static/assets/default_schedule.json', 'r') as file:
        default_schedule = json.load(file)
    return default_schedule

def load_default_notifactions():
    with open('static/assets/default_notifactions.json', 'r') as file:
        default_notifactions = json.load(file)
    return default_notifactions

def load_non_basic_json_file():
    with open('static/assets/messages.json', 'r') as file:
        default_schedule = json.load(file)
    return default_schedule

def string_to_time(time_str):
    hour, minute = map(int, time_str.split(':'))
    # Create a time object with the provided hour and minute
    result_time = time(hour=hour, minute=minute)
    return result_time

lower_days = ['monday','tuesday','wednesday','thursday','friday']
def find_next_day_of_week(day_of_week : str):
    day_index = lower_days.index(day_of_week.lower())
    today = datetime.now().weekday()
    days_ahead = (day_index - today) % 7
    if days_ahead == 0:
        days_ahead = 7
    next_day = datetime.now() + timedelta(days=days_ahead)
    # returns the date of the next time a day of the week would occur
    return next_day.strftime("%Y-%m-%d")


def time_to_min(time):
    return sum(i*j for i, j in zip(map(int, time.split(':')), (60, 1, 1/60)))

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
def date_to_day(date):
    year, month, day = (int(i) for i in date.split('-'))
    dayNumber = weekday(year, month, day)
    day = days[dayNumber].lower()
    return day

def load_available_classes():
    with open('static/assets/store_classlist.json', 'r') as file:
        form = json.load(file)
    return form["class_list"]

def write_available_classes(classList):
    with open('static/assets/store_classlist.json', 'r') as file:
        classList = json.dumps(classList,indent=2)
        file.write(classList)
    return

UNIVERSAL_CLASSLIST = load_available_classes()

def current_classlist():
    return {i:0 for i in UNIVERSAL_CLASSLIST}

def make_square(image, size):
    width, height = image.size
    new_dim = min(width, height)

    left = (width - new_dim) / 2
    top = (height - new_dim) / 2
    right = (width + new_dim) / 2
    bottom = (height + new_dim) / 2

    img_cropped = image.crop((left, top, right, bottom))
    img_resized = img_cropped.resize((size, size), Image.Resampling.LANCZOS)

    return img_resized

def count_weekdays_between(start_date: datetime, end_date: datetime, weekday: int) -> int:

    end_date = end_date.date()

    current_date = start_date
    weekday_count = 0
    
    while current_date <= end_date:
        if current_date.weekday() == weekday:
            weekday_count += 1
        current_date += timedelta(days=1)
    
    return weekday_count

def load_student_teacher_JSON():
    with open('static/assets/student_teacher.json', 'r') as file:
        student_teacher_file = json.load(file)
    return student_teacher_file