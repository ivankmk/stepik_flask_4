from flask import Flask, render_template, abort, redirect, url_for
import itertools
import json
import random
from config import Config
from forms import userForm, RequestForm
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, Teacher, Timetable, Student, Request, Booking, \
     Goal
from sqlalchemy import func


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)


GOALS = {'travel': '⛱ Для путешествий',
         'study': '🏫 Для учебы',
         'work': '🏢 Для работы',
         'relocate': '🚜 Для переезда',
         'programming': '💻 Для программирования'}

DAYS = {'mon': 'Понедельник',
        'tue': 'Вторник',
        'wed': 'Среда',
        'thu': 'Четверг',
        'fri': 'Пятница',
        'sat': 'Суббота',
        'sun': 'Воскресенье'}



@app.route('/')
def index():
    all_profiles = Teacher.query.order_by(func.random()).limit(6).all()
    goals = Goal.query.all()
    return render_template('index.html',
                            all_profiles=all_profiles,
                            goals=goals)

@app.route('/all/')
def index_all():
    all_profiles = Teacher.query.order_by(func.random()).all()
    return render_template('index.html',
                           all_profiles=all_profiles,
                           goals=GOALS)


@app.route('/request/')
def render_request():
    form = RequestForm()
    return render_template('request.html',
                           form=form)


# @app.route('/request_done/', methods=["POST"])
# def render_request_done():
#     form = RequestForm()

#     with open("requests.json", "r",  encoding='utf8') as f:
#         requests = json.load(f)

#     request = {
#         'name': form.name.data,
#         'phone': form.phone.data,
#         'hours': form.hours_available.data,
#         'goal': form.goal.data
#     }

#     requests.append(request)

#     with open("requests.json", "w", encoding='utf8') as f:
#         json.dump(requests, f, ensure_ascii=False)

#     return render_template(
#         'request_done.html',
#         form=form,
#     )


# @app.route('/booking/<int:id>/<day>/<time>/')
# def booking(id, day, time):

#     all_profiles = json.load(open('data.json'))
#     profile_data = [
#         profile for profile in all_profiles if profile['id'] == id][0]


#     day = DAYS[day]

#     form = userForm()
#     return render_template('booking.html',
#                            profile_data=profile_data,
#                            profile_id=id,
#                            day=day,
#                            time=time,
#                            form=form)


# @app.route('/booking_done/', methods=['POST'])
# def render_booking_done():
#     form = userForm()
#     name = form.name.data
#     phone = form.phone.data
#     day = form.day.data
#     time = form.time.data
#     teacher_id = form.teacher_id.data
#     teacher_name = form.teacher_name.data

#     with open('bookings.json', 'r', encoding='utf8') as f:
#         bookings = json.load(f)

#     booking = {
#         'id': teacher_id,
#         'name': name,
#         'phone': phone,
#         'date': '{},{}:00'.format(day, time)
#     }

#     bookings.append(booking)

#     with open('bookings.json', 'w', encoding='utf8') as f:
#         json.dump(bookings, f, ensure_ascii=False)

#     return render_template('booking_done.html',
#                            name=name,
#                            phone=phone,
#                            time=time,
#                            day=day)


@app.route('/goals/<goal>')
def goals(goal):
    goal_render = Goal.query.filter(Goal.goal_slug == goal).first()
    profiles_data = goal_render.teacher
    return render_template('goal.html',
                           profiles_data=profiles_data,
                           goal=goal_render.goal_text)


@app.route('/profile/<int:id>')
def profile(id):
    profile_data = Teacher.query.get(id)
    time_slots = []
    for slug, weekday in DAYS.items():
        times = []
        for slot in profile_data.timetables:
            if slot.weekday == slug:
                times.append(slot.time)
            slot = {slug: times}
            time_slots.append(slot)
    print(time_slots)
    if not profile_data:
        abort(404)

    return render_template('profile.html',
                           profile_data=profile_data,
                           goals=GOALS,
                           days=DAYS,
                           time_slots=time_slots)


if __name__ == '__main__':
    app.run()
