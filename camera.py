import pygame

from constants import DISP_WIDTH, DISP_HEIGHT

class Camera:
	def __init__(self, width, height):
		self.rect = pygame.Rect(0, 0, width, height)
	
	def apply(self, target):
		return target.rect.move(self.rect.topleft)
	
	def update(self, target):
		self.rect = self.follow(self.rect, target.rect)
		
	def follow(self, target):
		l, t, _, _ = target
		_, _, w, h = self.rect
		l, t       = DISP_WIDTH/2 - l, DISP_HEIGHT/2 - t # Center to target
		
		l = min(0, l)
		l = max(DISP_WIDTH - w, l)
		t = max(DISP_HEIGHT - l, t)
		t = min(0, t)
		
		return pygame.Rect(l, t, w, h)
