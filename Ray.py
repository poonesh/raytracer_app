
from Vector import Vector

class Ray():
	"""
	this class provide a ray object with origin and ray direction.
	""" 

	def __init__(self, origin = Vector(0.0, 0.0, 0.0), ray_dir = Vector(1.0, 1.0, 1.0)):
		self.origin =  origin
		self.ray_dir = ray_dir
		if abs(1.0-self.ray_dir.mag()) >= 1e-5:  #check if ray_dir is normalized or not 
			self.ray_dir.normalize()

	 
	def get_point(self, t):
		scaled_ray_direction = Vector(t*self.ray_dir.x, t*self.ray_dir.y, t*self.ray_dir.z)
		point_on_the_ray_direction = self.origin.clone().add(scaled_ray_direction)
		return point_on_the_ray_direction 





