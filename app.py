import gevent.monkey, gevent.socket
import socket
gevent.monkey.patch_all()
if socket.socket is gevent.socket.socket:
    print "gevent monkey patch has occurred"

from flask import Flask, session, render_template, flash, redirect, url_for, request, json, jsonify
import urllib2, base64, time, cStringIO, re

from config import set_config
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

# set homepage to form.htm
@app.route('/')
def my_form():
    return render_template("form.html")


# route for handling login page
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			if check_password_hash(user.password, form.password.data):
				return redirect(url_for('my_form'))
			return '<h1>Invalid username or password</h1>'
		# return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
	return render_template('login.html', form=form)


@app.route('/signup', methods=['GET','POST'])
def signup():
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method="sha256")
		new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		return '<h1>New User Has Been Created!</h1>'
		# return '<h1>' + form.username.data + ' ' +form.email.data + ' ' + form.password.data + '</h1>'
	return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('my_form'))


@app.route('/result', methods=['POST'])
def result():
	light_position = request.json["lightPosition"]
	image_size = int(request.json["imageSize"])
	ambient_illumination = float(request.json["ambIllumination"])
	dynamicFormData = request.json["dynamicForm"]
	final_result.delay(light_position, image_size, ambient_illumination, dynamicFormData)
	return jsonify({"status": 200})
	

@celery.task(name='app.result')
def final_result(light_position, image_size, ambient_illumination, dynamicFormData):
	x, y, z = vectorElem(light_position)
	primitiveObjs = readDynamicForm(dynamicFormData)
	pointlight = PointLight(position=Vector(x, y, z), color=Vector(255, 255, 255), Ka=ambient_illumination) 
	raytracer = RayTracer(screen2D=[image_size, image_size], primitives=primitiveObjs, lights=[pointlight], camerapos=Vector(7.5, 5, 10), O=Vector(0, 0, 0), U=Vector(10, 0, 0), V=Vector(0, 10, 0))
	socketio = SocketIO(engineio_logger=True, ping_timeout=120, message_queue='amqp://')
	
	def call_back_func1(perc):
		socketio.emit('send_prog_perc', {'data':perc})
	
	def call_back_func2(image):
		my_buffer = cStringIO.StringIO()
		image.save(my_buffer, format="JPEG")
		encoded_string = base64.b64encode(my_buffer.getvalue())
		socketio.emit('send_image', {'data':encoded_string})

	raytracer.render_image(call_back_func1, call_back_func2)


if __name__ == '__main__':
    app.debug = True
    socketio.run(app, port=5000) 

