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
		
		self.respawn()
		
	def action(self, delta):
		self.move(delta)
		if self.collision_detect():
			self.collide_sound.play()
		if self.collision_detect_others():
			self.collide_sound.play()
		
		# Based on which side the ball went, we can figure out who scored the goal.
		# However, it's the gamemode's responsibility to decide whether or not respawn the ball
		if self.x < 0:
			self.team_scored = 0
		if self.x > Map.current_map.rect.w:
			self.team_scored = 1
			
		# Loop over? Might be an interesting concept to try.
		if self.y < 0:
			self.y = Map.current_map.rect.h
		if self.y > Map.current_map.rect.h:
			self.y = 0
	
	def collision_detect_others(self):
		objects = list(self.surface.objects)
		objects.remove(self)
		for obj in objects:
			point = pygame.sprite.collide_mask(obj, self)
			if point:
				# BONK!
				collision.elastic_collision(obj, self, point)
				
	def respawn(self):
		super(Ball, self).respawn()
		self.x, self.y = Map.current_map.rect.w / 2, Map.current_map.rect.h / 2
		self.team_scored = -1