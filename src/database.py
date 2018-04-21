import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import UserMixin



def get_database(app):
	db = SQLAlchemy(app)
	password = os.environ['POSTGRES_PWD']
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:'+ password + '@localhost/user_data'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# create table
	class Users(UserMixin, db.Model):
	    id = db.Column(db.Integer, primary_key=True)
	    username = db.Column(db.String(15), unique=True)
	    email = db.Column(db.String(50), unique=True)
	    password = db.Column(db.String(80))
	    images = db.relationship('UserImage', backref='drawer', lazy='dynamic')

	class UserImage(db.Model):
		id = db.Column(db.Integer, primary_key=True)
		image = db.Column(db.LargeBinary)
		user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


	return (db, Users, UserImage)
