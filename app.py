import gevent.monkey, gevent.socket
import socket
gevent.monkey.patch_all()
if socket.socket is gevent.socket.socket:
    print "gevent monkey patch has occurred"
from flask import Flask, render_template, request, json, jsonify
from flask_socketio import SocketIO, emit, send, join_room, leave_room, close_room, rooms, disconnect
from flask_celery import make_celery
from celery import Celery
import urllib2
import re
import base64, time, cStringIO
from Vector import Vector
from Sphere import Sphere
from Triangle import Triangle
from PointLight import PointLight
from Screen2D import Screen2D
from RayTracer import RayTracer


#helper function to use regex in order to read tuple (vector) elements which is given as a string
def vectorElem(vector):
	vectorElements = re.findall("[-+]?\d*\.\d+|[-+]?\d+", vector)
	print "vectorElem", vectorElements
	print len(vectorElements)
	if len(vectorElements) != 0:
		return float(vectorElements[0]), float(vectorElements[1]), float(vectorElements[2])


"""helper function to read JSON data from dynamic Form and returns the primitive
objects which are chosen by the user"""

def readDynamicForm(dynamicFormData):
	primitiveObjs = []
	for item in dynamicFormData:
		for key in item:
			if key == "sphere":
				sphere_position = item[key]['sphere-position']
				pos_x, pos_y, pos_z = vectorElem(sphere_position)
				color = str(item[key]['color'])
				R, G, B = vectorElem(color)
				radius = float(item[key]['radius'])
				material = str(item[key]['material'])
				sphere = Sphere(position=Vector(pos_x, pos_y, pos_z), color=Vector(R, G, B), radius=radius, ka=0, kd=0, material=material) 
				primitiveObjs.append(sphere)

			elif key == "triangle":
				vertexA = item[key]['vertexA']
				verA_x, verA_y, verA_z = vectorElem(vertexA)
				vertexB = item[key]['vertexB']
				verB_x, verB_y, verB_z = vectorElem(vertexB)
				vertexC = item[key]['vertexC']
				verC_x, verC_y, verC_z = vectorElem(vertexC)
				color = str(item[key]['color'])
				R, G, B = vectorElem(color)
				material = str(item[key]['material'])
				triangle = Triangle(a=Vector(verA_x, verA_y, verA_z), b=Vector(verB_x, verB_y, verB_z), c=Vector(verC_x, verC_y, verC_z), color=Vector(R, G, B), ka=0, kd=0, material=material)
				primitiveObjs.append(triangle)
	return primitiveObjs


# create a Flask instance and initialize the flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

app.config.update(
CELERY_BROKER_URL='amqp://localhost//',
CELERY_RESULT_BACKEND='amqp://localhost//'
)

socketio = SocketIO(app, engineio_logger=True, ping_timeout=120, message_queue='amqp://')
celery = make_celery(app)

@app.route('/')
def my_form():
    return render_template("form.html")


# route for handling login page
@app.route('/login', method=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			return redirect(url_for('home'))
	return render_template('login.html', error=error)


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

    
