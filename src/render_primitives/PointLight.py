
from Vector import Vector


class PointLight():
	def __init__(self, position=Vector(1, 1, 1), color=Vector(255, 255, 255), Ka= 0.05, Kd= 0.8):
		self.position = position
		self.color = color
		self.Ka = Ka  # ambient intensity  AI = Ka(0<= Ka <=1) * La(color)
		self.Kd = Kd  # diffuse intensity  DI = Ka max(0, n.l) Ld


	def ambient_illumination(self):
		color = self.color.clone().div(255.0)
		return color.constant_multiply(self.Ka)


	def diffuse_illumination(self, Normal_vector= Vector(0, 0, 0), point= Vector(0, 0, 0)):
		color = self.color.clone().div(255.0)
		vector_point_to_light = (self.position.clone().sub(point.clone())).normalize()
		dot_N_L = Normal_vector.clone().normalize().dot(vector_point_to_light)

		max_value = max(dot_N_L, 0.0) 

		ret = color.constant_multiply(self.Kd*max_value)

		return ret

