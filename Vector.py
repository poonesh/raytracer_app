

class Vector():
	"""
	this class creates a vector object which obviously has a direction (x, y, z) and magnitude.
	the methods also provide the operations on a vector including adding, subtraction, dot and cross product as well as magnitude 
	and normalization. Through clone method, the vector object can be copied. 
	"""

	def __init__(self, x=0.0, y=0.0, z=0.0):
		self.x = x
		self.y = y
		self.z = z


	def mag(self):
		return ((self.x)**2 + (self.y)**2 + (self.z)**2)**(0.5)
		

	def add(self, v):
		self.x = v.x + self.x
		self.y = v.y + self.y
		self.z = v.z + self.z
		return self


	def sub(self, v):
		self.x = self.x - v.x 
		self.y = self.y - v.y 
		self.z = self.z - v.z 
		return self


	def dot(self, v):
		return v.x * self.x + v.y * self.y + v.z * self.z


	def cross(self, v):
		temp_x = self.y * v.z - self.z * v.y
		temp_y = self.z * v.x - self.x * v.z
		temp_z = self.x * v.y - self.y * v.x
		self.x, self.y, self.z = temp_x, temp_y, temp_z
		return self


	def normalize(self):
		magnitude = float(self.mag())
		self.x = self.x / magnitude
		self.y = self.y / magnitude
		self.z = self.z / magnitude
		return self


	def clone(self):
		return Vector(self.x, self.y, self.z)


	def div(self, cons):
		self.x = self.x/cons
		self.y = self.y/cons
		self.z = self.z/cons
		return self


	def constant_multiply(self, cons):
		self.x = self.x*cons
		self.y = self.y*cons
		self.z = self.z*cons
		return self


	def reflected_ray_dir(self, normal_vector):
		"""this function calculates the reflected ray 
		of a mirror surface primitive in a ray tracer 
		scene."""

		N = normal_vector.normalize()
		N_dot_self = N.dot(self.normalize())
		R_r = (N.constant_multiply(N_dot_self)).constant_multiply(2).sub(self.normalize())
		ref_ray_dir = R_r.normalize()
		return ref_ray_dir
		

	def __str__(self):
		return '({}, {}, {})'.format(self.x, self.y, self.z)


	


	
