import re
from render_primitives.Vector import Vector
from render_primitives.Sphere import Sphere
from render_primitives.Triangle import Triangle
from render_primitives.PointLight import PointLight
from render_primitives.Screen2D import Screen2D
from render_primitives.RayTracer import RayTracer


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


