
from Vector import Vector 
# from Ray import Ray
# from Triangle import Triangle
# from Sphere import Sphere
# from Triangle import Triangle 
# from Screen2D import Screen2D
# from Viewport import Viewport
# from PointLight import PointLight
# import math
# import sys

from RayTracer import RayTracer
from flask import Flask, render_template, request
import base64

# from image import data_uri
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("form.html")

@app.route('/result', methods=['POST'])
def my_form_post():
	if request.method == 'POST':
		x = float(request.form['X'])
		y = float(request.form['Y'])
		z = float(request.form['Z'])
		raytracer = RayTracer(lightpos=Vector(x ,y ,z), camerapos=Vector(7.5, 5, 10), O=Vector(0, 0, 0), U=Vector(10, 0, 0), V=Vector(0, 10, 0))  
		raytracer.render_image()
		# encoded = base64.b64encode(open("ray_pic.png", "rb").read())
		return render_template("result.html", path = "/static/ray_pic.png")


		

if __name__ == '__main__':
    app.run()








