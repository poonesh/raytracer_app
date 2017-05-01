
from Vector import Vector 
from PointLight import PointLight
from Screen2D import Screen2D
from RayTracer import RayTracer
from flask import Flask, render_template, request, jsonify, Response, send_file, json
from flask_celery import make_celery
import re 
import base64, time


# create a Flask instance and initialize the flask application
app = Flask(__name__)

app.config.update(
CELERY_BROKER_URL = 'amqp://localhost//',
CELERY_RESULT_BACKEND='amqp://localhost//'
)

celery = make_celery(app)


@app.route('/')
def my_form():
    return render_template("form.html")



@app.route('/result')
def result():
	light_position = request.args.get("light_position", "(0, 0, 0)", type=str)
	image_size = request.args.get('image_size', 128, type=int)
	ambient_illumination = request.args.get('ambient_illumination', 0.5, type=float)
	final_result.delay(light_position, image_size, ambient_illumination)


@celery.task(name='app.result')
def final_result(light_position, image_size, ambient_illumination):
	light_position_coor = re.findall("[-+]?\d*\.\d+|[-+]?\d+", light_position)
	x = float(light_position_coor[0])
	y = float(light_position_coor[1])
	z = float(light_position_coor[2])

	pointlight = PointLight(position=Vector(x, y, z), color=Vector(255, 255, 255), Ka=ambient_illumination) 
	raytracer = RayTracer(screen2D=[image_size, image_size], lights=[pointlight], camerapos=Vector(7.5, 5, 10), O=Vector(0, 0, 0), U=Vector(10, 0, 0), V=Vector(0, 10, 0)) 
	raytracer.render_image()

	# the image is encoded to base64 which returns a string (encoded_string)
	encoded_string = base64.b64encode(open("/Users/Pooneh/projects/applications/ray_tracer_app_flask/static/ray_pic.png", "rb").read())
	with open ('result.json', 'w') as f:
		json.dump({'image': encoded_string}, f) # write the string in a file 'result.json'
	
	
    
if __name__ == '__main__':
    app.run(debug=True, port=4000)



    
