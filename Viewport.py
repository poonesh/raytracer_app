

from PIL import Image
from Vector import Vector 

class Viewport():

	def __init__(self, O=Vector(0, 0, 0), U=Vector(5, 0, 0), V=Vector(0, 5, 0)):
		self.O = O
		self.U = U
		self.V = V
		

	def percentage_to_point(self, u_percentage, v_percentage):
		U_vector = self.U.clone().constant_multiply(u_percentage/100.0)
		V_vector = self.V.clone().constant_multiply(v_percentage/100.0)
		view_port_pixel = self.O.clone().add(U_vector).add(V_vector)
		return view_port_pixel




  