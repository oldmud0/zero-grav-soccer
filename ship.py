import pygame, os, math

import collision
from entity import Entity
from map import Map

class Ship(Entity):
	mass = 300

	def __init__(self, surface, team, gamemode):
		path = os.path.join("res", "ship-sprite.png")
		super(Ship, self).__init__(path, surface)
		
		self.team = team
		gamemode.change_team(self, team)
		
		if self.team == 0:
			# red team faces right
			self.x = Map.current_map.rect.w * 0.4
			self.y = Map.current_map.rect.h / 2
			self.rot = 270
		elif self.team == 1:
			# blue team faces left
			self.x = Map.current_map.rect.w * 0.6
			self.y = Map.current_map.rect.h / 2
			self.rot = 90
		else:
			assert(False)
		
		self.thrust	= False
		self.left = False
		self.right = False
		self.grabbing = False
		
		self.gamemode = gamemode
		self.team = team
		
		self.collide_sound = pygame.mixer.Sound(os.path.join("res", "ship_bump.wav"))
		self.collide_with_ship_sound = pygame.mixer.Sound(os.path.join("res", "ship_ship_collision.wav"))
	
	def action(self, delta):
		if self.thrust:
			self.vx += -.1*math.sin(math.radians(self.rot))
			self.vy += -.1*math.cos(math.radians(self.rot))
		if self.left:
			self.vrot = self.vrot / 2 + 2
		if self.right:
			self.vrot = self.vrot / 2 - 2
		if not (self.left ^ self.right):
			self.vrot = self.vrot / 4
		if self.grabbing:
			pass
		
		self.move(delta)
		if self.collision_detect():
			self.collide_sound.play()
		if self.collision_detect_others():
			self.collide_with_ship_sound.play()
		
	def collision_detect_others(self):
		teammates = self.gamemode.get_enemies(self)
		other_objects = [self.gamemode.objective] # It's a list, just for future-proofing
		
		objects = teammates + other_objects
		
		for obj in objects:
			if pygame.sprite.collide_mask(self, obj):
				# BONK!
				collision.elastic_collision(obj, self)
	