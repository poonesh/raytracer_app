
import unittest
from Vector import Vector


class TestVector(unittest.TestCase):

    def test_initialize(self):

        v = Vector(1, 2, 3)

        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
        self.assertEqual(v.z, 3)

    def test_defaults(self):

        v = Vector()

        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)
        self.assertEqual(v.z, 0)

    def test_add(self):

        v = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)

        v.add(v2)

        self.assertEqual(v.x, 5)
        self.assertEqual(v.y, 7)
        self.assertEqual(v.z, 9)


    # TODO: Implement test_sub, test_dot, test_cross

    def test_mag(self):
        v = Vector(0, 0, 0)
        self.assertEqual(v.mag(), 0)


    def test_dot(self):
        v1 = Vector(6, 2, 1)
        v2 = Vector(2, 1, 2)
        self.assertEqual(v1.dot(v2), 16)


    def test_cross(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(-1, 0, -2)
        v1.cross(v2)
        self.assertEqual(v1.x, -4)
        self.assertEqual(v1.y, -1)
        self.assertEqual(v1.z, 2)

    # # lookup class method chaining
    def test_chain(self):

        v = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)

        v.add(v2).add(v2)

        self.assertEqual(v.x, 9)
        self.assertEqual(v.y, 12)
        self.assertEqual(v.z, 15)


    def test_normalize(self):

        v = Vector(0, 5, 0)
        v.normalize()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 1)
        self.assertEqual(v.z, 0)


    def test_constant_multiply(self):
        v = Vector(0, 5, 0)
        result_vector = v.constant_multiply(3)
        self.assertEqual(result_vector.x, 0)
        self.assertEqual(result_vector.y, 15)
        self.assertEqual(result_vector.z, 0)




if __name__ == "__main__":
    unittest.main()

