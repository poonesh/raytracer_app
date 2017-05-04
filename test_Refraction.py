
import unittest 
from Vector import Vector
from Ray import Ray
import math


class TestRefraction(unittest.TestCase):

	# def test_refraction(self):

	# 	r1 = Ray(origin=Vector(0, 0, 0), ray_dir=Vector(1, 1, 1))

	# 	intersection_point = Vector(2, 2, 2)
	# 	surface_normal = Vector(-1, -1, -1)

	# 	nFrom = 1
	# 	nTo = 1.5

	# 	r2 = r1.refract(nFrom, nTo, intersection_point, surface_normal)
		
	# 	self.assertEqual(r2.origin.x, 2)
	# 	self.assertEqual(r2.origin.y, 2)
	# 	self.assertEqual(r2.origin.z, 2)

	# 	val = Vector(1,1,1).normalize()

	# 	self.assertAlmostEqual(r2.ray_dir.x, val.x)
	# 	self.assertAlmostEqual(r2.ray_dir.y, val.y)
	# 	self.assertAlmostEqual(r2.ray_dir.z, val.z)

	def test_refraction_2(self):

		r1 = Ray(origin=Vector(0, 0, 0), ray_dir=Vector(1, 0, 0))

		intersection_point = Vector(1, 0, 0)
		surface_normal = Vector(-1, 1, 0)

		nFrom = 1
		nTo = 1.5

		r2 = r1.refract(nFrom, nTo, intersection_point, surface_normal)
		
		self.assertEqual(r2.origin.x, intersection_point.x)
		self.assertEqual(r2.origin.y, intersection_point.y)
		self.assertEqual(r2.origin.z, intersection_point.z)

		self.assertAlmostEqual(r2.ray_dir.x, 0.3763991)
		self.assertAlmostEqual(r2.ray_dir.y, 0.2902675)
		self.assertAlmostEqual(r2.ray_dir.z, 0)


if __name__ == "__main__":
	unittest.main()

