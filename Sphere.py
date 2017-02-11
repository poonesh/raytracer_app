
from Vector import Vector
from Ray import Ray


def solve_quadratic(a, b, c):
	delta = b**2 - 4*a*c
	if delta < 0:
		return None
	x1 = (-b + (delta**0.5))/float(2*a)
	x2 = (-b - (delta**0.5))/float(2*a)

	return x1, x2


class Sphere():

	def __init__(self, position= Vector(0, 0, 0), radius = 1.0, color=Vector(0, 0, 255), ka = 0, kd = 0):
		self.position = position
		self.radius = radius
		self.color = color
		self.ka = ka  # the surface's coefficient of ambient reflection  (0<= ka <= 1)
		self.kd = kd  # the surface's coefficient of diffuse reflection  (0<= ka <= 1)


	def surface_normal(self, point = Vector(1, 1, 1), ray_origin=Vector(0, 0, 0), ray_dir=Vector(0, 0, 0)):

		center_point_vector = point.clone().sub(self.position.clone())
		return center_point_vector.clone().normalize()


	
	def get_intersect(self, ray_origin= Vector(0, 0, 0), ray_dir = Vector(1, 1, 1)):
		
		"""
		this method returns the point where a Ray and a sphere intersects.
		if the Ray does not intersect with the sphere the function returns False

		following are the calculation steps:

		(1) the equation of a sphere x^2 + y^2 + z^2 = R^2
		
		(2) the equation of a ray P = O + tD 
			(O is the origin of the ray and D is the normalized vector which corresponds to the ray direction and P 
			is a point at the end of the ray based on the scaling factor t. t is in fact the parametric distance from the origin of the ray 
			to the point of interest along the ray) 
		
		(3) if x, y, and z in equation 1 are the coordinates of point P in equation 2: P^2 - R^2 = 0
			(when the sphere is not centered at the origin, equation 2 is equal to  |P - C|^2 - R^2 = 0 (equation 3) 
		
		(4) equation 3 can be rewritten as |O + tD - C|^2 - R^2 = 0 (equation 4), where C is the center of the sphere in space
		
		(5) equation 4 is a quadratic function where a = 1 (dot product of a normalized vector with itself) and 
			b = 2D(O-C) and c = |O-C|^2 - R^2.
		(6) delta = b^2 - 4*a*c   t1, t2 = (-b +- sqrt(delta)/2a
			if delta > 0, the ray intersects the sphere in two points (t1 and t2)
			if delta = 0, the ray intersects the sphere in one point only (t1=t2)
			if delta < 0, the ray does not intersect with the sphere.    
		"""
		ray = Ray(ray_origin, ray_dir)

		a = ray.ray_dir.dot(ray.ray_dir)  #a = D^2 = 1 (D is a normalized vector for ray direction)
		vector_O_C = ray.origin.clone().sub(self.position.clone()) #the vector between origin of the ray and the center of the circle
		
		scaled_ray_direction = ray.ray_dir.clone().constant_multiply(2)  # 2*D 
		b = scaled_ray_direction.dot(vector_O_C)
		
		mag_vector_O_C = vector_O_C.mag()

		c = (mag_vector_O_C)**2 - (self.radius)**2
		
		if solve_quadratic(a, b, c) is None:
			return False

		t1, t2 = solve_quadratic(a, b, c)


		if t1>0 and t2>0:
			if t1<t2:
				return t1
			return t2

		elif t1==t2:
			return t1

		else:
			return False




