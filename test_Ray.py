
import unittest
import math
from Ray import Ray
from Vector import Vector


class TestRay(unittest.TestCase):

	def test_initialize(self):

		R = Ray(Vector(0.0, 0.0, 0.0), Vector(1.0, 1.0, 1.0))
		self.assertEqual(R.origin.x, 0.0)
		self.assertEqual(R.ray_dir.y, 1.0/math.sqrt(3))


	def test_defaults(self):

		R = Ray()
		self.assertEqual(R.origin.x, 0.0)
		self.assertEqual(R.origin.y, 0.0)
		self.assertEqual(R.origin.z, 0.0)


	def test_check_point(self):
		R = Ray(Vector(0.0, 0.0, 0.0), Vector(0.0, 2.0, 0.0))
		self.assertEqual(R.get_point(10).x, 0)
		self.assertEqual(R.get_point(10).y, 10)
		self.assertEqual(R.get_point(10).z, 0)


		R = Ray(Vector(1.0, 1.0, 1.0), Vector(0.0, 2.0, 0.0))
		self.assertEqual(R.get_point(10).x, 1)
		self.assertEqual(R.get_point(10).y, 11)
		self.assertEqual(R.get_point(10).z, 1)





if __name__ == "__main__":
	unittest.main()

