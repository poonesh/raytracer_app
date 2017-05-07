
from Vector import Vector
from Sphere import Sphere
from Triangle import Triangle 
from PointLight import PointLight
from Screen2D import Screen2D
from RayTracer import RayTracer
from flask import Flask, render_template, request, jsonify, Response, send_file, json
from flask_celery import make_celery
import re 
import base64, time


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
				radius = float(item[key]['radius'])
				print(str(item[key]['color']))
				color = str(item[key]['color'])
				print "color", color
				R, G, B = vectorElem(color)
				print "R", R, G, B

				material = str(item[key]['material'])
				print material

				sphere = Sphere(position=Vector(pos_x, pos_y, pos_z), radius=radius, ka=0, kd=0, material=material) #color=Vector(R, G, B)
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
				triangle = Triangle(a= Vector(verA_x, verA_y, verA_z), b= Vector(verB_x, verB_y, verB_z), c= Vector(verC_x, verC_y, verC_z), color=Vector(R, G, B), ka = 0, kd = 0, material=material)
				primitiveObjs.append(triangle)
	return primitiveObjs


# create a Flask instance and initialize the flask application
app = Flask(__name__)

# app.config.update(
# CELERY_BROKER_URL = 'amqp://localhost//',
# CELERY_RESULT_BACKEND='amqp://localhost//'
# )

# celery = make_celery(app)


@app.route('/')
def my_form():
    return render_template("form.html")



@app.route('/result', methods=['POST'])
def result():
	
	# light_position = request.args.get('light_position',"(0, 0, 0)", type=str)  
	# image_size = request.args.get('image_size', 128,  type=int) 
	# ambient_illumination = request.args.get('ambient_illumination', 0.5, type=float) 
	# primitive_selector = request.args.get('primitive_selector', "sphere" , type=str)
	# primitive_selector0 = request.args.get('primitive_selector0', "sphere" , type=str)

	
	light_position = request.json["lightPosition"]
	image_size = int(request.json["imageSize"])
	ambient_illumination = float(request.json["ambIllumination"])

	dynamicFormData = request.json["dynamicForm"]
	print "dynamicFormData", dynamicFormData
	primitiveObjs = readDynamicForm(dynamicFormData)
	# print "objects", primitiveObjs
	# print type(primitiveObjs)
	# print len(primitiveObjs)

	
	x, y, z = vectorElem(light_position)

	pointlight = PointLight(position=Vector(x, y, z), color=Vector(255, 255, 255), Ka=ambient_illumination) 
	raytracer = RayTracer(screen2D=[image_size, image_size], primitives=primitiveObjs, lights=[pointlight], camerapos=Vector(7.5, 5, 10), O=Vector(0, 0, 0), U=Vector(10, 0, 0), V=Vector(0, 10, 0)) 
	raytracer.render_image()

	# the image is encoded to base64 which returns a string (encoded_string)
	encoded_string = base64.b64encode(open("/Users/Pooneh/projects/applications/ray_tracer_app_flask/static/ray_pic.png", "rb").read())
	return jsonify(data=encoded_string)
	# with open ('result.json', 'w') as f:
	# 	json.dump({'image': encoded_string}, f) # write the string in a file 'result.json'


# @celery.task(name='app.result')
# def final_result(light_position, image_size, ambient_illumination, primitive_selector):
# 	light_position_coor = re.findall("[-+]?\d*\.\d+|[-+]?\d+", light_position)
# 	x = float(light_position_coor[0])
# 	y = float(light_position_coor[1])
# 	z = float(light_position_coor[2])

# 	pointlight = PointLight(position=Vector(x, y, z), color=Vector(255, 255, 255), Ka=ambient_illumination) 
# 	raytracer = RayTracer(screen2D=[image_size, image_size], lights=[pointlight], camerapos=Vector(7.5, 5, 10), O=Vector(0, 0, 0), U=Vector(10, 0, 0), V=Vector(0, 10, 0)) 
# 	raytracer.render_image()

# 	# the image is encoded to base64 which returns a string (encoded_string)
# 	encoded_string = base64.b64encode(open("/Users/Pooneh/projects/applications/ray_tracer_app_flask/static/ray_pic.png", "rb").read())
# 	with open ('result.json', 'w') as f:
# 		json.dump({'image': encoded_string}, f) # write the string in a file 'result.json'
	
	
    
if __name__ == '__main__':
    app.run(debug=True, port=4000)

    
