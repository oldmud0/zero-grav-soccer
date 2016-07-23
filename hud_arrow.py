import pygame
import math, os

from hud_element import HUDElement

from settings import DISP_WIDTH, DISP_HEIGHT

class HUDArrowElement(HUDElement):
	"""HUD element for pointing at entities or positions"""
	
	path = os.path.join("res", "arrow.png")
	
	rot = 0
	
	def __init__(self, camera, get_pos, onscreen):
		super(HUDArrowElement, self).__init__(get_pos())
		self.original_image = self.image
		self.get_pos = get_pos
		self.onscreen = onscreen # If true, then arrow will also draw when object is on screen.
		self.camera = camera
		
	def rot_center(self):
		loc = self.rect.center
		self.image = pygame.transform.rotate(self.original_image, self.rot)
		self.rect = self.image.get_rect()
		self.rect.center = loc
		
	def action(self):
		self.image = self.original_image.copy()
		self.point()
		self.rot_center()
		
	def point(self):
		"""Point the arrow to the given position."""
		target_pos = self.get_pos()
		print(self.camera.rect.left)
		# If off screen...
		if target_pos[0] < -self.camera.rect.left: # Object is left of camera's view
			self.rot = math.degrees(math.atan2(target_pos[0] - self.camera.rect.centerx, target_pos[1] - self.camera.rect.centery))
			self.rect.midleft = (0, self.camera.rect.bottomleft[1] - target_pos[1])
		elif target_pos[0] > self.camera.rect.right: # Object is right
			self.rot = math.degrees(math.atan2(self.camera.rect.centerx - target_pos[0], target_pos[1] - self.camera.rect.centery))
			self.rect.midright = (DISP_WIDTH - 1, self.camera.rect.bottomright[1] - target_pos[1])
			print("working?")
		elif self.onscreen:
			pass
		else:
			self.image.fill((0,0,0,0)) # transparent