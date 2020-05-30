import json
from models import db, Teacher, Timetable, Goal
from datetime import datetime

def get_teachers_data():
	with open("data.json", "r") as f:
		teachers = json.load(f)
	return teachers


def load_teachers_data_to_db():
	teachers = get_teachers_data()

	for teacher in teachers:
		teacher_data = Teacher(
			name=teacher['name'],
			email='{}@school.com'.format(teacher['name'].replace(' ', '_')),
			about=teacher['about'],
			rating=teacher['rating'],
			picture=teacher['picture'],
			price=teacher['price'],
			)
		db.session.add(teacher_data)


	db.session.commit()    


def load_teachers_timetable():

	teachers = get_teachers_data()
	for teacher in teachers:
		teacher_data = db.session.query(Teacher).filter(
			Teacher.name == teacher['name']).first()
		for weekday, time in teacher['free'].items():
			for key, value in time.items():
				if value:
					timetables = Timetable(
						teacher_id = teacher_data.id,
						weekday = weekday,
						time = datetime.strptime(key, '%H:%M').time()
						)
					db.session.add(timetables)
	db.session.commit()


def load_goals():

	goals = {'travel': '⛱ Для путешествий',
			'study': '🏫 Для учебы',
			'work': '🏢 Для работы',
			'relocate': '🚜 Для переезда',
			'programming': '💻 Для программирования'}

	for key, value in goals.items():
		goal = Goal(
			goal_slug=key,
			goal_text=value
		)
		db.session.add(goal)
	db.session.commit()



def load_teachers_goals():
	teachers = get_teachers_data()

	for teacher in teachers:
		teacher_db = db.session.query(Teacher).filter(Teacher.name == teacher['name']).first()
		for goal in teacher['goals']:
			goal_db = db.session.query(Goal).filter(Goal.goal_slug == goal).first()
			teacher_db.goals.append(goal_db)
		db.session.commit()	