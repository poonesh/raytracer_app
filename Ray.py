
from Vector import Vector
import math

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

	def refract(self, nFrom, nTo, intersect_point, surface_normal):
		c_1 = surface_normal.normalize().clone().dot(self.ray_dir.normalize().clone())

		n = nFrom / nTo

		k = (1-(n**2)*(1-(c_1)**2))


		if k < 0:
			return "K is negative"

		c_2 = math.sqrt(k)


		part_1 = self.ray_dir.normalize().constant_multiply(n)
		part_2 = surface_normal.normalize().clone().constant_multiply((n*c_1 - c_2))

		ref_ray_dir = (part_1.clone().add(part_2.clone())).normalize()
	 	ref_ray = Ray(origin=intersect_point, ray_dir=ref_ray_dir)

		return ref_ray

		