
from Vector import Vector 
from RayTracer import RayTracer
from flask import Flask, render_template, request, jsonify, Response, send_file
import base64, time

# from image import data_uri
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("form.html")
    

@app.route('/result')
def result():
	x = request.args.get('x', 0.0, type=float)
	y = request.args.get('y', 0.0, type=float)
	z = request.args.get('z', 0.0, type=float)
	raytracer = RayTracer(lightpos=Vector(x ,y ,z), camerapos=Vector(7.5, 5, 10), O=Vector(0, 0, 0), U=Vector(10, 0, 0), V=Vector(0, 10, 0)) 
	raytracer.render_image() 
	encoded = base64.b64encode(open("/Users/Pooneh/projects/applications/ray_tracer_app_flask/static/ray_pic.png", "rb").read())
	return jsonify(data=encoded)

    
if __name__ == '__main__':
    app.run(debug=True, port=4000)
    
