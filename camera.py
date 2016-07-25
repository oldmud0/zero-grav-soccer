import pygame

class Camera:
	"""The Camera tracks the object being controlled while remaining within
	the bounds of the level/scene.
	
	Thanks to the good friends at Stack Overflow: http://stackoverflow.com/a/14357169/2958458
	"""
	
	def __init__(self, map_width, map_height, disp_width, disp_height):
		self.rect = pygame.Rect(0, 0, map_width, map_height)
		self.disp_width, self.disp_height = disp_width, disp_height
	
	def apply(self, target):
		"""Apply the position transformations to an entity/sprite."""
		return target.rect.move(self.rect.topleft)
	
	def update(self):
		self.rect = self.follow(self.target.rect.center)
		
	def follow(self, target):
		dp_w, dp_h = self.disp_width, self.disp_height # Width and height of surface
		x, y = target                                  # Center X and Y of target's rectangle/sprite
		_, _, w, h = self.rect                         # Width and height of our level
		x, y, _, _ = dp_w/2 - x, dp_h/2 - y, w, h      # Center to target
		
		# Clamp the rectangle's boundaries to the level's boundaries
		x = min(0, x)
		x = max(dp_w - w, x)
		y = max(dp_h - h, y)
		y = min(0, y)
		
		return pygame.Rect(x, y, w, h)
