import pygame

from constants import DISP_WIDTH, DISP_HEIGHT

class Camera:
	"""The Camera tracks the object being controlled while remaining within
	the bounds of the level/scene.
	
	Thanks to the good friends at Stack Overflow: http://stackoverflow.com/q/22872524
	"""
	
	def __init__(self, width, height):
		self.rect = pygame.Rect(0, 0, width, height)
	
	def apply(self, target):
		return target.rect.move(self.rect.topleft)
	
	def update(self, target):
		self.rect = self.follow(target.rect)
		
	def follow(self, target):
		l, t, _, _ = target # Left and top of target's rectangle/sprite
		_, _, w, h = self.rect # Width and height of our level
		l, t       = DISP_WIDTH/2 - l, DISP_HEIGHT/2 - t # Center to target
		
		# Clamp the rectangle's boundaries to the level's boundaries
		l = min(0, l)
		l = max(DISP_WIDTH - w, l)
		t = max(DISP_HEIGHT - l, t)
		t = min(0, t)
		
		return pygame.Rect(l, t, w, h)
