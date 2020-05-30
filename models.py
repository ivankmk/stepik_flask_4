from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


teacher_goals_association = db.Table(
	'teacher_goals',
	db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
	db.Column('goal_id', db.Integer, db.ForeignKey('goals.id')),
)


class Teacher(db.Model):
	__tablename__ = 'teachers'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False, unique=True)
	about = db.Column(db.Text)
	rating = db.Column(db.Float)
	picture = db.Column(db.String)
	price = db.Column(db.Float)
	timetables = db.relationship('Timetable', back_populates='teacher')
	bookings = db.relationship('Booking', back_populates='teacher')
	goals = db.relationship('Goal', secondary=teacher_goals_association, back_populates='teacher')	
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,  nullable=False)

	def __repr__(self):
		return '<Teacher {}>'.format(self.name)

class Timetable(db.Model):
	__tablename__ = 'timetables'
	id = db.Column(db.Integer, primary_key=True)
	teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
	teacher = db.relationship('Teacher', back_populates='timetables')
	weekday = db.Column(db.String)
	time = db.Column(db.Time)
	bookings = db.relationship('Booking', back_populates='timetables')
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,  nullable=False)    

	def __repr__(self):
		return '<Timetable {}>'.format(self.id)


class Goal(db.Model):
	__tablename__ = 'goals'
	id = db.Column(db.Integer, primary_key=True)
	goal_slug = db.Column(db.String, unique=True)
	goal_text = db.Column(db.String, unique=True)
	teacher = db.relationship(
		'Teacher', secondary=teacher_goals_association, back_populates='goals')
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(),  nullable=False)

	def __repr__(self):
		return '<Goal {}>'.format(self.goal_text)

class Student(db.Model):
	__tablename__ = 'students'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	email = db.Column(db.String, nullable=True, unique=True)
	phone = db.Column(db.String, unique=True)
	bookings = db.relationship('Booking', back_populates='student')
	requests = db.relationship('Request', back_populates='student')
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

	def __repr__(self):
		return '<Student {}>'.format(self.name)

class Request(db.Model):
	__tablename__ = 'requests'
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
	student = db.relationship('Student', back_populates='requests')
	goal = db.Column(db.String)
	have_time = db.Column(db.String)
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,  nullable=False)

	def __repr__(self):
		return '<Request {}>'.format(self.student)


class Booking(db.Model):
	__tablename__ = 'bookings'
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
	student = db.relationship('Student', back_populates='bookings')
	teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
	teacher = db.relationship('Teacher', back_populates='bookings')
	timetable_id = db.Column(db.Integer, db.ForeignKey('timetables.id'))
	timetables = db.relationship('Timetable', back_populates='bookings')
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,  nullable=False)    

	def __repr__(self):
		return '<Booking {}>'.format(self.student)	

class Other(db.Model):
	__tablename__ = 'other'
	id = db.Column(db.Integer, primary_key=True)
	data_reference_type = db.Column(db.String)
	data_key = db.Column(db.String)
	data_value = db.Column(db.String)

	def __repr__(self):
		return '<Other data {}>'.format(self.data_key)
