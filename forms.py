from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, RadioField
from wtforms.validators import InputRequired, Email

class userForm(FlaskForm):
    name = StringField(
        'Вас зовут', [InputRequired(), InputRequired(message='Введите имя')])
    phone = StringField(
        'Ваш телефон', [InputRequired(), InputRequired(message='Введите телефон')])
    day = HiddenField()
    time = HiddenField()
    teacher_id = HiddenField()
    timetable_id = HiddenField()
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