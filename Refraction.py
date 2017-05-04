
from Vector import Vector 
from Ray import Ray
from Triangle import Triangle
from Sphere import Sphere
from Triangle import Triangle 
from Screen2D import Screen2D
from Viewport import Viewport
from PointLight import PointLight
import math
import sys

ray = Ray(origin=Vector(0.0, 0.0, 0.0), ray_dir=Vector(1.0, 1.0, 0.5))
sphere = Sphere(position=Vector(2, 2, 2), radius=1.0)
t_min = sphere.get_intersect(ray_origin=Vector(0.0, 0.0, 0.0), ray_dir=Vector(1.0, 1.0, 0.5))
print t_min
intersect_point = ray.origin.clone().add(ray.ray_dir.clone().constant_multiply(t_min))
normal_vector = sphere.surface_normal(point=intersect_point.clone(), ray_origin=ray.origin.clone(),ray_dir=ray.ray_dir.clone()) 
# print "normal_vector", normal_vector 
# print "ray_dir", ray.ray_dir
# print "ray_dir_normalize", ray.ray_dir.normalize()
# print "intersect_point", intersect_point


def Refraction(ray, air_ind, glass_ind, env ="air"):
	sphere = Sphere(position=Vector(2, 2, 2), radius=1.0)
	print "ray.ray_origin", ray.origin
	print "ray.ray_dir", ray.ray_dir
	t_min = sphere.get_intersect(ray_origin=ray.origin, ray_dir=ray.ray_dir.normalize())
	print "t_min", t_min
	intersect_point = ray.origin.clone().add((ray.ray_dir.normalize().clone()).constant_multiply(t_min*0.001))
	print "intersect_point", intersect_point
	normal_vector = sphere.surface_normal(point=intersect_point.clone(), ray_origin=ray.origin.clone(),ray_dir=ray.ray_dir.clone()) 
	print "normal_vector", normal_vector 
	c_1 = normal_vector.normalize().clone().dot(ray.ray_dir.normalize().clone())
	if env == "air":
		n = air_ind/glass_ind
		c_1 = -c_1
		print "n", n
		# print "c_1", c_1
	else:
		n = glass_ind/air_ind
		print "n", n
		normal_vector = normal_vector.normalize().constant_multiply(-1)
	k = (1-(n**2)*(1-(c_1)**2))
	if k < 0:
		return "K is negative"
	c_2 = math.sqrt(k)
	part_1 = ray.ray_dir.normalize().constant_multiply(n)
	part_2 = normal_vector.normalize().clone().constant_multiply((n*c_1 - c_2))	
	ref_ray_dir = (part_1.clone().add(part_2.clone())).normalize()
	# print "ref_ray_dir", ref_ray_dir
	ref_ray = Ray(origin=intersect_point, ray_dir=ref_ray_dir)
	# print "env", env
	# print "n", n
	return ref_ray


	
ref_ray_airtoglass = Refraction(ray, 1, 1.5, env ="air")


print "ref_ray_airtoglass", ref_ray_airtoglass.ray_dir

ref_ray_glasstoair = Refraction(ref_ray_airtoglass, 1, 1.5, env ="glass")
print "ref_ray_glasstoair", ref_ray_glasstoair.ray_dir.normalize()
print "ref_ray_glasstoair", ref_ray_glasstoair.ray_dir


