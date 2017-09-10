
from Vector import Vector
from Ray import Ray
import sys


class Triangle():

	def __init__(self, a= Vector(1.0, 0.0, 0.0), b= Vector(0.0, 0.0, 1.0), c= Vector(0.0, 1.0, 0.0), color=Vector(0.0, 0.0, 0.0), ka = 0, kd = 0, material="normal"):
		self.a = a
		self.b = b
		self.c = c
		self.color = color
		self.ka = ka  #the surface's coefficient of ambient reflection  (0<= ka <= 1)
		self.kd = kd  #the surface's coefficient of diffuse reflection  (0<= kd <= 1)
		ab_vector = self.b.clone().sub(self.a.clone())
		ac_vector = self.c.clone().sub(self.a.clone())
		self.normal = (ab_vector.clone().cross(ac_vector))
		self.material = material
		
	
	
	def surface_normal(self, point=Vector(0, 0, 0), ray_origin=Vector(0, 0, 0), ray_dir=Vector(0, 0, 0)):
		return self.normal.clone()

	
	def get_intersect(self, ray_origin = Vector(0.0, 0.0, 0.0), ray_dir = Vector(1.0, 1.0, 1.0)):

		"""
		this method retrns True if a ray intersects a triangle.
		following are the procedures for the calculation, there are two major steps: 
		- first, if the ray intersects the plane where the triangle is placed.
		- second, if the ray intersects inside the triangle. 
		(1) to calculate the normal of a triangle, the cross product of the triangle's sides should be calculated. 
		(2) finding the plane(triangle) normal, if the dot product of ray_dir and plane normal is zero, the 
			ray is paralled to the triangle plane and so there is no intersects. 
		(3) if the step number (2) is not valid, it should be checked if the intersection point is inside the triangle 
			or not. (at this point, it can also be checked if the plane is behind the ray, this is optional though for this project)
		(4) the last step is to check if the ray intersects the plane inside the triangle.
		"""

		ray = Ray(ray_origin, ray_dir.clone().normalize())
		

		normal = self.normal.clone()
		plane_normal_ray_vec_dot = ray.ray_dir.clone().dot(normal)  #l(ray_dir).n (normal_plane)
		
		#check if the ray is perpendicular to the normal vector of the plane
		if plane_normal_ray_vec_dot == 0.0: #if ray and normal vector to the plane are perpendicular 
			return False

		plane_normal_ray_vec_dot = ray.ray_dir.clone().dot(normal) 
		

		#D is the distance of the plane from origin (0, 0, 0) which can be calculated as following 
		D = normal.clone().dot(self.a.clone())
		nominator = float(float(ray_origin.clone().dot(normal.clone()) - D))
		t = float(-nominator/(plane_normal_ray_vec_dot))

		if t < 0.0:
			return False


		#check if the intersection point is inside the triangle
		scaled_ray_dir = ray.ray_dir.clone().constant_multiply(t) 	
		intersect_point = ray_origin.clone().add(scaled_ray_dir)
		
		intersect_point_a = self.a.clone().sub(intersect_point.clone())
		intersect_point_b = self.b.clone().sub(intersect_point.clone())
		intersect_point_c = self.c.clone().sub(intersect_point.clone())

		v1 = intersect_point_a.clone().cross(intersect_point_b.clone())
		v2 = intersect_point_b.clone().cross(intersect_point_c.clone())
		v3 = intersect_point_c.clone().cross(intersect_point_a.clone())

		if (v1.dot(v2)) > 0 and \
		   (v2.dot(v3)) > 0 and \
		   (v3.dot(v1)) > 0:
		
		    return t
		return False


