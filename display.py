import pygame

from settings import DISP_WIDTH, DISP_HEIGHT
from map import Map
from entity import Entity
from hud import HUD

class Display:
	"""Holds all of the game's internals and objects."""
	
	clock = None
	
	def __init__(self):
		self.surface = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
		
		self.clock = pygame.time.Clock()
		self.objects = pygame.sprite.Group()
		self.camera = None
		self.hud = HUD(self)
		
	def update(self):
		delta = self.clock.tick(60)
		for object in self.objects:
			object.action(delta)
		self.camera.update(Entity.ent_in_control)
		self.hud.action()
		
	def render(self):
		self.surface.fill((0xff, 0xff, 0xff))
		
		self.surface.blit(Map.current_map.image, self.camera.apply(Map.current_map))
		for object in self.objects:
			self.surface.blit(object.image, self.camera.apply(object))
			
		self.hud.elements.draw(self.surface)
			
		self.surface.blit
		
		pygame.display.update()