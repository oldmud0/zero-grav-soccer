import pygame, os

class HUD(pygame.sprite.Sprite):
	"""Heads-up display"""
	
	arrow_path = os.path.join("res", "arrow.png")
	
	def __init__(self, surface):
		self.surface = surface
		self.elements = []
		
		print("Loading", path)
		self.image = pygame.image.load(path).convert_alpha()
		
	def action(self):