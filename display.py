import pygame

from settings import DISP_WIDTH, DISP_HEIGHT
from map import Map
from entity import Entity
from hud import HUD
from camera import Camera

class Display:
	"""Holds all of the game's internals and objects."""
	
	clock = None
	
	_ent_in_control = None
	
	def __init__(self):
		self.surface = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
		
		self.clock = pygame.time.Clock()
		self.objects = pygame.sprite.Group()
		self.hud = HUD(self)
	
	def load_game(self, gamemode):
		self.camera = Camera(Map.current_map.rect.w, Map.current_map.rect.h)
		self.hud.acquire_gamemode_hud(gamemode, self.camera)
		
	def update(self):
		delta = self.clock.tick(60)
		for object in self.objects:
			object.action(delta)
		self.camera.update()
		self.hud.action()
	
	@property
	def ent_in_control(self):
		return self._ent_in_control
		
	@ent_in_control.setter
	def ent_in_control(self, ent):
		self._ent_in_control = ent
		self.camera.target = ent
		
	def render(self):
		self.surface.fill((0xff, 0xff, 0xff))
		
		self.surface.blit(Map.current_map.image, self.camera.apply(Map.current_map))
		for object in self.objects:
			self.surface.blit(object.image, self.camera.apply(object))
			
		self.hud.elements.draw(self.surface)
			
		self.surface.blit
		
		pygame.display.update()