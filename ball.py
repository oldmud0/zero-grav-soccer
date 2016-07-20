import pygame, os

import collision
from entity import Entity
from map import Map

class Ball(Entity):
	
	mass = 200

	def __init__(self, surface):
		path = os.path.join("res", "ball.png")
		super(Ball, self).__init__(path, surface)
		self.collide_sound = pygame.mixer.Sound(os.path.join("res", "bounce.wav"))
		
		self.x, self.y = Map.current_map.rect.w / 2, Map.current_map.rect.h / 2
		
	def action(self, delta):
		self.move(delta)
		if self.collision_detect():
			self.collide_sound.play()
		if self.collision_detect_others():
			self.collide_sound.play()
	
	def collision_detect_others(self):
		objects = list(self.surface.objects)
		objects.remove(self)
		for obj in objects:
			point = pygame.sprite.collide_mask(obj, self)
			if point:
				# BONK!
				collision.elastic_collision(obj, self, point)