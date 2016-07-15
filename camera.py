import pygame

from settings import DISP_WIDTH, DISP_HEIGHT

class Camera:
	"""The Camera tracks the object being controlled while remaining within
	the bounds of the level/scene.
	
	Thanks to the good friends at Stack Overflow: http://stackoverflow.com/a/14357169/2958458
	"""
	
	def __init__(self, width, height):
		self.rect = pygame.Rect(0, 0, width, height)
	
	def apply(self, target):
		"""Apply the position transformations to an entity/sprite."""
		return target.rect.move(self.rect.topleft)
	
	def update(self, target):
		self.rect = self.follow(target.rect.center)
		
	def follow(self, target):
		x, y = target # Center X and Y of target's rectangle/sprite
		_, _, w, h = self.rect # Width and height of our level
		x, y, _, _ = DISP_WIDTH/2 - x, DISP_HEIGHT/2 - y, w, h # Center to target
		
		# Clamp the rectangle's boundaries to the level's boundaries
		x = min(0, x)
		x = max(DISP_WIDTH - w, x)
		y = max(DISP_HEIGHT - h, y)
		y = min(0, y)
		
		return pygame.Rect(x, y, w, h)
