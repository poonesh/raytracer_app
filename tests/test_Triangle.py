
import unittest
from Triangle import Triangle 
from Vector import Vector


class TestTriangle(unittest.TestCase):

	def test_get_intersect(self):
		
		T = Triangle()
		result = T.get_intersect(Vector(0.0, 0.0, 0.0), Vector(1.0, 1.0, -0.5))
		self.assertEqual(result, False)

		result = T.get_intersect(Vector(0.0, 0.0, 0.0), Vector(-1.0, -1.0, 1.0))
		self.assertEqual(result, False)

		result = T.get_intersect(Vector(2.0, 0.0, 0.0), Vector(-2.0, 2.0, 0.0))
		self.assertEqual(result, False)

		T = Triangle(Vector(1.0, 0.0, 0.0), Vector(0.0, 0.0, 1.0), Vector(0.0, 1.0, 0.0))
		result = T.get_intersect(Vector(0.0, 0.0, 0.0), Vector(1.0, 1.0, 1.0))
		self.assertEqual(result, True)



if __name__ == "__main__": 
	unittest.main() 