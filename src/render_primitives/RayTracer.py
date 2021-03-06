# import numba
# from numba import jit
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



class RayTracer():
	def __init__(self, screen2D=[256, 256], primitives=[] , lights=[] , camerapos=Vector(0, 0, 0), O=Vector(0, 0, 0), U=Vector(0, 0, 0), V=Vector(0, 0, 0)):
		self.lights = lights
		self.camerapos = camerapos
		self.viewportpos = Viewport(O=O, U=U, V=V)
		self.list_of_primitives = []
		self.primitives = primitives 
		self.screen2D = Screen2D(screen2D[0], screen2D[1])
		self.size = self.screen2D.image.size

		
		# cornell box components
		triangle_back_1 = Triangle(a= Vector(0, 0, 10), b= Vector(20, 0, 10), c= Vector(0, 20, 10), color= Vector(247, 195, 49))
		triangle_right_1 = Triangle(a= Vector(10, 20, 0), b= Vector(10, 0, 20), c= Vector(10, 0, 0), color= Vector(70, 130, 180))
		triangle_top_1 = Triangle(a= Vector(0, 10, 0), b= Vector(20, 10, 0), c= Vector(0, 10, 20), color= Vector(176, 224, 230))
		triangle_left_1 = Triangle(a= Vector(0, 0, 0), b= Vector(0, 0, 20), c= Vector(0, 20, 0), color= Vector(215, 57, 37))
		triangle_bottom_1 = Triangle(a= Vector(0, 0, 0), b= Vector(20, 0, 0), c= Vector(0, 0, 20), color= Vector(205, 205, 201))
		


		for prim in self.primitives:
			print "prim", prim
			self.list_of_primitives.append(prim)


		# appending cornell box componenet to the list_of_primitives  
		self.list_of_primitives.append(triangle_back_1)
		self.list_of_primitives.append(triangle_right_1)
		self.list_of_primitives.append(triangle_top_1)
		self.list_of_primitives.append(triangle_left_1)
		self.list_of_primitives.append(triangle_bottom_1)
	
		#calculate ambient illumination for the point_light
		self.ambient = self.lights[0].ambient_illumination()


	def set_light_pos(self, position=Vector(0, 0, 0)):
		self.lights = self.lights[0](position=position)
		return self.lightpos


	def set_camera_pos(self, position=Vector(0, 0, 0)):
		self.camerapos = position
		return self.camerapos


	def is_in_shadow(self, intersect_point, obj):
		"""
		"""
		#1. calculate ray from intersect point to light source
		light_intersect_vector = self.lights[0].position.clone().sub(intersect_point)
		t_ray_light = light_intersect_vector.mag()
		light_intersect_ray = Ray(origin =intersect_point.clone(), ray_dir= light_intersect_vector.normalize())
		#2. determine if ray intersects any OTHER primitives
		is_intersected = False
		for test_obj in self.list_of_primitives:
			if obj != test_obj and test_obj.material != "glass":
				t = test_obj.get_intersect(light_intersect_ray.origin.clone(), light_intersect_ray.ray_dir.clone())
				if t and t < t_ray_light:
					is_intersected = True
					break
				else:
					is_intersected = False
			else:
				continue
		return is_intersected


	def illumination(self, ray, normal_vector, intersect_point, surface_color):
		plane_normal_ray_vec_dot = ray.ray_dir.clone().dot(normal_vector)  #l(ray_dir).n (normal_plane)
		
		if plane_normal_ray_vec_dot > 1e-6: #if ray and normal vector to the plane are in the same direction (the angle between them is 0)
			normal_vector.constant_multiply(-1) #change the direction of the ray
		else:
			normal_vector.constant_multiply(1)

		plane_normal_ray_vec_dot = ray.ray_dir.clone().dot(normal_vector) 

		diffuse = self.lights[0].diffuse_illumination(Normal_vector=normal_vector.clone() , point=intersect_point) #calculate diffuse illumination for the point_light 
		add_diffuse_ambient = diffuse.clone().add(self.ambient.clone()) #add diffuse and ambient illumination 
		 
		#rescaling the surface color between 0 and 1, multiplying with diffuse and ambient illumination """
		final_color_R = (surface_color.clone().div(255.0)).x * add_diffuse_ambient.x
		final_color_G = (surface_color.clone().div(255.0)).y * add_diffuse_ambient.y
		final_color_B = (surface_color.clone().div(255.0)).z * add_diffuse_ambient.z

		#converting the color scale between 0 and 255 
		final_color_R = int(math.floor(final_color_R*255))
		final_color_G = int(math.floor(final_color_G*255))
		final_color_B = int(math.floor(final_color_B*255))

		final_color = (final_color_R, final_color_G, final_color_B)
		return final_color


	def scene_intersect(self, ray, n_current):
		intersect_scale_dic = {}
		num_of_bounces_glass = 0
		num_of_bounces_mirror = 0
		for obj in self.list_of_primitives:
			t = obj.get_intersect(ray.origin.clone(), ray.ray_dir.normalize().clone()) 
			if t:
				intersect_scale_dic[obj] = t
		if len(intersect_scale_dic) != 0:
			t_min = min(intersect_scale_dic.itervalues())
			intersected_obj = (min(intersect_scale_dic, key=intersect_scale_dic.get))
			surface_color = intersected_obj.color
			intersect_point = ray.origin.clone().add(ray.ray_dir.normalize().clone().constant_multiply(t_min))
			normal_vector = intersected_obj.surface_normal(point=intersect_point.clone(), ray_origin=self.camerapos.clone(), ray_dir=ray.ray_dir.normalize().clone())	
			
			if intersected_obj.material == "glass" and num_of_bounces_glass <= 200:
				num_of_bounces_glass += 1
				if n_current == "air":
					nFrom = 1
					nTo = 1.5
				else:
					nFrom = 1.5
					nTo = 1
				ray = ray.refract(nFrom, nTo, intersect_point, normal_vector)
				ray.origin = ray.origin.clone().add(ray.ray_dir.normalize().clone().constant_multiply(0.001))
				
				if ray.reflect_called == False:
					if n_current == "air":
						n_current = "glass"
					else:
						n_current = "air"

				return self.scene_intersect(ray, n_current)
			
		
			if intersected_obj.material == "mirror" and num_of_bounces_mirror <= 200:
				num_of_bounces_mirror += 1
				ray = ray.reflect(intersect_point, normal_vector)
				ray.origin = ray.origin.clone().add(ray.ray_dir.normalize().clone().constant_multiply(0.001))
				return self.scene_intersect(ray, "air")

			else:
				# calling is_in_shadow function to check if the intersect point is in shadow or not
				is_intersected = self.is_in_shadow(intersect_point.clone(), intersected_obj)
				if is_intersected:
					return (0, 0, 0)
				else:
				# calling illumination function if the intersect_point light_position Ray does not intersects with any other primitives 
					final_color = self.illumination(ray, normal_vector, intersect_point, surface_color)
					return final_color
		else:
			return (0, 0, 0)

	# @jit
	def render_image(self, call_back_func_progress_percentage, call_back_func_send_image):
		""" 
		Two call_back_function is passed to the render_image function where the first one send the percentage progress of rendering image to the front end
		and the second one send the rendered image to the front end. In order to render image, this function converts the position of pixels in a screen 2D 
		to the correlate pixel positions in the viewport and claculates the ray direction and also color of the picture.
		 """
		#looping over the size of the width of screen2D
		for i in range(self.size[0]):
			#calculate the percentage of the pixel position corresponding to the width of the screen2D image
			perc = (float(i+1)/(self.size[0]))*100
			if perc == 25 or perc == 50 or perc == 75 or perc == 100:
				#call back function to send the percentage of the calculation progress to the front end in app.py file
				call_back_func_progress_percentage(perc)
			#looping over the height of the image
			for j in range(self.size[1]):
				#finding pixel position percentage in the screen2D
				percentage_pos = self.screen2D.pixel_position_percentage(i, j)
				 #converting pixel position percentage in the screen2D to the correlate pixel position in the viewport 
				view_port_pixel = self.viewportpos.percentage_to_point(percentage_pos[0], percentage_pos[1])
				ray_dir = view_port_pixel.sub(self.camerapos.clone())
				ray = Ray(self.camerapos.clone(), ray_dir.clone()) #defining a ray
				color = self.scene_intersect(ray, "air")
				""" assign the color to the screen2D pixels
					(x,y) === (0,0) is defined at the bottom left corner of the viewport but at the top left corner or the screen2D.
					so to avoid rendering the image upside down we need to convert the pixels by having self.size[1] - j - 1 unless we
					define the viewport as U= vector(-5, 0, 0) and V= vector(0, -5, 0) where we can assign the color to the screen2D.pixels[i, j] = color.
				"""
				self.screen2D.pixels[i,self.size[1] - j - 1] = color
		image = self.screen2D.image
		call_back_func_send_image(image)



