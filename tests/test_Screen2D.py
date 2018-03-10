
import unittest
from Screen2D import Screen2D


class TestScreen2D(unittest.TestCase):

	def test_initialize(self):
		screen_2D = Screen2D(500, 500)
		screen_2D.image.size[0]
		screen_2D.image.size[1]
		screen_2D.pixels = screen_2D.image.load()

		self.assertEqual(screen_2D.image.size[0], 500)
		self.assertEqual(screen_2D.image.size[1], 500)
		self.assertEqual(screen_2D.pixels[0, 0], (0.0, 0.0, 0.0))


	def test_set_pixel_color(self):
		screen_2D = Screen2D(500, 500)
		screen_2D.set_pixel_color((34, 139, 34))
		screen_2D.pixels = screen_2D.image.load()
		self.assertEqual(screen_2D.pixels[0, 0], (34, 139, 34))


	def test_pixel_position_percentage(self):
		screen_2D = Screen2D(500, 500)
		percentage_pos = screen_2D.pixel_position_percentage(250, 250)
		self.assertEqual(percentage_pos[0], 50)
		self.assertEqual(percentage_pos[1], 50)

		screen_2D = Screen2D(500, 500)
		percentage_pos = screen_2D.pixel_position_percentage(375, 375)
		self.assertEqual(percentage_pos[0], 75)
		self.assertEqual(percentage_pos[1], 75)



if __name__ == "__main__":
	unittest.main()

	