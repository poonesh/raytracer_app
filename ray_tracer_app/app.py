import sys
sys.path.append('/Users/Pooneh/projects/applications/RayTracer_app/ray_tracer_app_flask/render_primitives')

import gevent.monkey, gevent.socket
import socket
gevent.monkey.patch_all()
if socket.socket is gevent.socket.socket:
    print "gevent monkey patch has occurred"

from flask import Flask, session, render_template, flash, redirect, url_for, request, json, jsonify, g
from flask_socketio import SocketIO
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,login_user, login_required, logout_user, current_user
from flask.ext.login import AnonymousUserMixin
from flask_bootstrap import Bootstrap
import urllib2, base64, time, cStringIO, re

from app_config import set_config
from database import get_database
from app_helper_functions import vectorElem, readDynamicForm
from forms import *

from Vector import Vector
from Sphere import Sphere
from Triangle import Triangle
from PointLight import PointLight
from Screen2D import Screen2D
from RayTracer import RayTracer


# create a Flask instance and initialize the flask application
app = Flask(__name__)
socketio, celery = set_config(app)
db, User, UserImage = get_database(app)
Bootstrap(app)

class Anonymous(AnonymousUserMixin):
	"""
	Anonymous class inherits from AnonymousUserMixin. When no user is logged_in,
	the current user will be an instance of Ananymous class which has a username property with the value 'Guest'.
	"""
	def __init__(self):
		self.username = 'Guest'

#LoginManager contains the code which lets the application and Flask-Login work together(like how 
#to load a user from an ID)
login_manager = LoginManager()
login_manager.init_app(app) #passing app to login_manager for configuration
login_manager.anonymous_user = Anonymous
#login_manager.login_view = 'login' #if I want to use a @login_required decorator, login_manager.login_view 
# is also required. Not in this app though.

@login_manager.user_loader
def load_user(user_id): # the load_user model connects the abstract user of flask-login to the user model database behind the scene
	return User.query.get(int(user_id)) # note that the user_id is saved as unicode which needs to be converted to an integer 

@app.before_request
def before_request():
	g.user = current_user

# set homepage to form.htm
@app.route('/')
def my_form():
    return render_template("form.html")

# route for handling login page
@app.route('/login', methods=['GET', 'POST'])
def login():
	"""
	In this function we use a class to represent and validate the client-side form data. For example, 
	WTForms is a library that will handle this and use a custom LoginForm to validate.
	"""
	form = LoginForm()
	if form.validate_on_submit():
		# Login and validate the user.
		# user should be an instance of the user class
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			login_user(user)
			if check_password_hash(user.password, form.password.data):
				# user.password is the hashed password
				# form.password.data is the plaintext password
				# return True if the password matches and Flase otherwis
				if login_user(user):
					flash('You just logged in!')
					return redirect(url_for('my_form'))
		else:
			flash('Error logging in!')
			return redirect(url_for('login'))
	return render_template('login.html', form=form) # how we are redirect to the login form again????????


@app.route('/signup', methods=['GET','POST'])
def signup():
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method="sha256")
		new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		flash('You just signed up!')
		return redirect(url_for('my_form'))
	return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
	logout_user()
	flash('You just logged out!')
	return redirect(url_for('my_form'))


@celery.task(name='task.result')
def final_result(light_position, image_size, ambient_illumination, dynamicFormData, username):
	"""A set of parameters are passed to final_result function to create an instance of RayTracer class(raytracer). Then the method 
	render_image() from this class is used to calculate the precentage progress of the rendered_image. call_back_func_send_image()
	also save the image as URI data and pass it to front end through socketio. This call_back function also save the URI data of the 
	rendred image in SQLAlchemy."""

	owner = User.query.filter_by(username=username).first()
	x, y, z = vectorElem(light_position)
	primitiveObjs = readDynamicForm(dynamicFormData)
	pointlight = PointLight(position=Vector(x, y, z), color=Vector(255, 255, 255), Ka=ambient_illumination) 
	raytracer = RayTracer(screen2D=[image_size, image_size], primitives=primitiveObjs, lights=[pointlight], camerapos=Vector(7.5, 5, 10), O=Vector(0, 0, 0), U=Vector(10, 0, 0), V=Vector(0, 10, 0))
	socketio = SocketIO(engineio_logger=True, ping_timeout=120, message_queue='amqp://')
	
	def call_back_func_progress_percentage(perc):
		socketio.emit('send_prog_perc', {'data':perc})
	
	def call_back_func_send_image(image):
		my_buffer = cStringIO.StringIO() # using cStringIO in order to be able to save the image as an string
		image.save(my_buffer, format="JPEG")
		encoded_string = base64.b64encode(my_buffer.getvalue())
		image = UserImage(image=encoded_string, drawer=owner)
		db.session.add(image)
		db.session.commit()
		socketio.emit('send_image', {'data':encoded_string})

	raytracer.render_image(call_back_func_progress_percentage, call_back_func_send_image)


"""
jQuery sending data to the ('/result') endpoint and function result pass this data(if these data are valid) to final_result function 
and pass it to message broker(rabbitmq) to annonce that I have a new task for celery worker (which is supposed to be done asynchronously). 
Then the result function will return a dictionary {"status":200} to confirm that the task has been passed to celery and nothing has broken.
"""
@app.route('/result', methods=['POST'])
def result():
	light_position = request.json["lightPosition"]
	# if vectorElem(light_position) is None:
	# 	return jsonify({"status": 500, "message": "Light Position Format Incorrect"})
	image_size = int(request.json["imageSize"])
	ambient_illumination = float(request.json["ambIllumination"])
	dynamicFormData = request.json["dynamicForm"]
	final_result.delay(light_position, image_size, ambient_illumination, dynamicFormData, current_user.username)
	return jsonify({"status": 200})


if __name__ == '__main__':
    app.debug = True
    socketio.run(app, port=5000)
