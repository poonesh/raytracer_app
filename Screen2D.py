

from PIL import Image

class Screen2D():

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.image = Image.new(size=(self.width, self.height), mode="RGB", color = "black")
		self.pixels = self.image.load()


	def set_pixel_color(self, color=(255, 255, 255)):
		for i in range(self.image.size[0]):
			for j in range(self.image.size[1]):
				self.pixels[i,j] = color
		self.image.show()


	def pixel_position_percentage(self, pixel_i, pixel_j):
		percentage_u = (pixel_i/float(self.width))*100 
		percentage_v = (pixel_j/float(self.height))*100
		percentage_pos = (percentage_u, percentage_v)
		return percentage_pos

