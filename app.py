from flask import Flask, render_template, abort, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, RadioField
from wtforms.validators import InputRequired, Email
import itertools
import json
import random

app = Flask(__name__)
app.secret_key = 'my-super-secret-phrase-I-dont-tell-this-to-nobody'

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


class userForm(FlaskForm):
    name = StringField(
        'Вас зовут', [InputRequired(), InputRequired(message='Введите имя')])
    phone = StringField(
        'Ваш телефон', [InputRequired(), InputRequired(message='Введите телефон')])
    day = HiddenField()
    time = HiddenField()
    teacher_id = HiddenField()
    teacher_name = HiddenField()
    submit = SubmitField('Записаться на пробный урок')


class RequestForm(FlaskForm):
    name = StringField('Ваше имя', [InputRequired(message='Введите имя')])
    phone = StringField(
        'Ваш телефон', [InputRequired(message='Введите телефон')])
    goal = RadioField('Какая цель занятий?', choices=[
        ('⛱ Для путешествий', '⛱ Для путешествий'),
        ('🏫 Для учебы', '🏫 Для учебы'),
        ('🏢 Для работы', '🏢 Для работы'),
        ('🚜 Для переезда', '🚜 Для переезда'),
        ('💻 Для программирования', '💻 Для программирования')])

    hours_available = RadioField('Сколько времени есть?', choices=[
        ('1-2 часа в неделю', '1-2 часа в неделю'),
        ('3-5 часов в неделю', '3-5 часов в неделю'),
        ('5-7 часов в неделю', '5-7 часов в неделю'),
        ('7-10 часов в неделю', '7-10 часов в неделю')])
    submit = SubmitField('Найдите мне преподавателя')


def create_json():
    with open('bookings.json', 'w', encoding='utf8') as f:
        json.dump([{}], f, ensure_ascii=False)

    with open('requests.json', 'w', encoding='utf8') as f:
        json.dump([{}], f, ensure_ascii=False)

@app.route('/')
def index():
    all_profiles = json.load(open('data.json'))
    return render_template('index.html',
                           all_profiles=random.sample(all_profiles, 6),
                           goals=GOALS)

@app.route('/all/')
def index_all():
    all_profiles = json.load(open('data.json'))
    return render_template('index.html',
                           all_profiles=all_profiles,
                           goals=GOALS)


@app.route('/request/')
def render_request():
    form = RequestForm()
    return render_template('request.html',
                           form=form)


@app.route('/request_done/', methods=["POST"])
def render_request_done():
    form = RequestForm()

    with open("requests.json", "r", encoding='utf8') as f:
        requests = json.load(f)

    request = {
        'name': form.name.data,
        'phone': form.phone.data,
        'hours': form.hours_available.data,
        'goal': form.goal.data
    }

    requests.append(request)

    with open("requests.json", "w", encoding='utf8') as f:
        json.dump(requests, f, ensure_ascii=False)

    return render_template(
        'request_done.html',
        form=form,
    )


@app.route('/booking/<int:id>/<day>/<time>/')
def booking(id, day, time):

    all_profiles = json.load(open('data.json'))
    profile_data = [
        profile for profile in all_profiles if profile['id'] == id][0]


    day = DAYS[day]

    form = userForm()
    return render_template('booking.html',
                           profile_data=profile_data,
                           profile_id=id,
                           day=day,
                           time=time,
                           form=form)


@app.route('/booking_done/', methods=['POST'])
def render_booking_done():
    form = userForm()
    name = form.name.data
    phone = form.phone.data
    day = form.day.data
    time = form.time.data
    teacher_id = form.teacher_id.data
    teacher_name = form.teacher_name.data

    with open('bookings.json', 'r', encoding='utf8') as f:
        bookings = json.load(f)

    booking = {
        'id': teacher_id,
        'name': name,
        'phone': phone,
        'date': '{},{}:00'.format(day, time)
    }

    bookings.append(booking)

    with open('bookings.json', 'w', encoding='utf8') as f:
        json.dump(bookings, f, ensure_ascii=False)

    return render_template('booking_done.html',
                           name=name,
                           phone=phone,
                           time=time,
                           day=day)


@app.route('/goals/<goal>')
def goals(goal):
    all_profiles = json.load(open('data.json'))
    try:
        profiles_data = [
            profile for profile in all_profiles if goal in profile['goals']]
    except IndexError:
        abort(404)
    return render_template('goal.html',
                           profiles_data=profiles_data,
                           goal=GOALS[goal])


@app.route('/profile/<int:id>')
def profile(id):
    all_profiles = json.load(open('data.json'))
    try:
        profile_data = [
            profile for profile in all_profiles if profile['id'] == id][0]
    except IndexError:
        abort(404)

    return render_template('profile.html',
                           profile_data=profile_data,
                           goals=GOALS,
                           days=DAYS)


if __name__ == '__main__':
    app.run()
