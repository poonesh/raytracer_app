import gevent.monkey, gevent.socket
import socket
gevent.monkey.patch_all()
if socket.socket is gevent.socket.socket:
    print "gevent monkey patch has occurred"

from flask import Flask, session, render_template, flash, redirect, url_for, request, json, jsonify, g
from flask_socketio import SocketIO, join_room
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,login_user, login_required, logout_user, current_user
from flask.ext.login import AnonymousUserMixin
from flask_bootstrap import Bootstrap
from sqlalchemy import text
import urllib2, base64, time, cStringIO

from app_config import set_config
from database import get_database
from app_helper_functions import vectorElem, readDynamicForm
from forms import *

from render_primitives.Vector import Vector
from render_primitives.Sphere import Sphere
from render_primitives.Triangle import Triangle
from render_primitives.PointLight import PointLight
from render_primitives.Screen2D import Screen2D
from render_primitives.RayTracer import RayTracer


# create a Flask instance and initialize the flask application
app = Flask(__name__)
socketio, celery = set_config(app)
db, Users, UserImage = get_database(app)
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
login_manager.login_view = 'login' #if I want to use a @login_required decorator, login_manager.login_view is also required. 


# we use user_loader callback. This callback is used to reload the user object from the user ID stored in the session. 
@login_manager.user_loader
def load_user(user_id): 
	return Users.query.get(int(user_id)) # note that the user_id is saved as unicode which needs to be converted to an integer 

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
		user = Users.query.filter_by(username=form.username.data).first()
		if user:
			if check_password_hash(user.password, form.password.data):
				# user.password is the hashed password
				# form.password.data is the plaintext password
				# return True if the password matches and Flase otherwis
				if login_user(user):
					flash('You just logged in!')
					return redirect(url_for('profile_page'))
		else:
			flash('Error logging in!')
			return redirect(url_for('login'))
	return render_template('login.html', form=form)


@app.route('/signup', methods=['GET','POST'])
def signup():
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method="sha256")
		new_user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(new_user) #adding new python object to the session
		db.session.commit()		 #commiting the session to the database
		flash('You just signed up!')
		return redirect(url_for('my_form'))
	return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
	logout_user()
	flash('You just logged out!')
	return redirect(url_for('my_form'))


@app.route('/profile')
@login_required
def profile_page():
	username = current_user.username
	flash('Welcome, %s' %username)
	id = current_user.id
	#writing SQL query in SQLAlchemy
	sql = text('select image from "user_image" where user_id='+str(id))
	user_images = db.engine.execute(sql)
	images = []
	for image in user_images:
		images.append(image[0])
	return render_template('profile.html', images=images)


@celery.task(name='task.result')
def final_result(light_position, image_size, ambient_illumination, dynamicFormData, username, room):
	"""A set of parameters are passed to final_result function to create an instance of RayTracer class(raytracer). Then the method 
	render_image() from this class is used to calculate the precentage progress of the rendered_image. call_back_func_send_image()
	also save the image as URI data and pass it to front end through socketio. This call_back function also save the URI data of the 
	rendred image in SQLAlchemy."""

	image_owner = Users.query.filter_by(username=username).first()
	x, y, z = vectorElem(light_position)
	primitiveObjs = readDynamicForm(dynamicFormData)
	pointlight = PointLight(position=Vector(x, y, z), color=Vector(255, 255, 255), Ka=ambient_illumination) 
	raytracer = RayTracer(screen2D=[image_size, image_size], primitives=primitiveObjs, lights=[pointlight], camerapos=Vector(5, 5, -10), O=Vector(0, 0, 0), U=Vector(10, 0, 0), V=Vector(0, 10, 0))
	socketio = SocketIO(engineio_logger=True, ping_timeout=120, message_queue='amqp://')
	
	def call_back_func_progress_percentage(perc):
		socketio.emit('send_prog_perc', {'data':perc}, namespace='/result', room=room)
	
	def call_back_func_send_image(image):
		my_buffer = cStringIO.StringIO() # using cStringIO in order to be able to save the image as an string
		image.save(my_buffer, format="JPEG")
		encoded_string = base64.b64encode(my_buffer.getvalue())
		image = UserImage(image=encoded_string, drawer=image_owner)
		db.session.add(image)
		db.session.commit()
		socketio.emit('send_image' ,{'data':encoded_string}, namespace='/result', room=room)

	raytracer.render_image(call_back_func_progress_percentage, call_back_func_send_image)


"""
jQuery sending data to the ('/result') endpoint and function result pass this data(if these data are valid) to final_result function 
and pass it to message broker(rabbitmq) to annonce that I have a new task for celery worker (which is supposed to be done asynchronously). 
Then the result function will return a dictionary {"status":200} to confirm that the task has been passed to celery and nothing has broken.
"""
# @app.route('/result', methods=['POST'])
# def result():
# 	light_position = request.json["lightPosition"]
# 	image_size = int(request.json["imageSize"])
# 	ambient_illumination = float(request.json["ambIllumination"])
# 	dynamicFormData = request.json["dynamicForm"]
# 	session_id = request.sid
# 	room = session_id
# 	join_room(room)
# 	final_result.delay(light_position, image_size, ambient_illumination, dynamicFormData, current_user.username, room)
# 	return jsonify({"status": 200})


@socketio.on('submit_data', namespace='/result')
def result_handler(data):
	light_position = data['lightPosition']
	image_size = int(data['imageSize'])
	ambient_illumination = float(data['ambIllumination'])
	dynamicFormData = data['dynamicForm']
	session_id = request.sid
	room = session_id
	join_room(room)
	final_result.delay(light_position, image_size, ambient_illumination, dynamicFormData, current_user.username, room)


if __name__ == '__main__':
	app.debug = True
	socketio.run(app, host='0.0.0.0' ,port=5000)
