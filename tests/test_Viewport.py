
import unittest 
from Viewport import Viewport 


class TestViewport(unittest.TestCase):

	def test_percentage_to_point(self):

		viewport = Viewport()
		view_port_pixel = viewport.percentage_to_point(50, 50)
		self.assertEqual(view_port_pixel.x, 2.5)
		self.assertEqual(view_port_pixel.y, 2.5)
		self.assertEqual(view_port_pixel.z, 0.0)



if __name__ == "__main__":
	unittest.main()

