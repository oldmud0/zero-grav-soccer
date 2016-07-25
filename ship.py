import pygame, os, math

import collision
from entity import Entity
from map import Map

from settings import SHIP_ACCELERATION

class Ship(Entity):
	mass = 300

	def __init__(self, team, gamemode):
		self.team = team
		self.gamemode = gamemode
		gamemode.change_team(self, team)
		
		if self.team == 0:
			# blue team faces right
			self.x = Map.current_map.rect.w * 0.4
			self.y = Map.current_map.rect.h / 2
			self.rot = 270
			path = os.path.join("res", "ship-sprite-blue.png")
			path_firing = os.path.join("res", "ship-sprite-blue-firing.png")
		elif self.team == 1:
			# red team faces left
			self.x = Map.current_map.rect.w * 0.6
			self.y = Map.current_map.rect.h / 2
			self.rot = 90
			path = os.path.join("res", "ship-sprite-red.png")
			path_firing = os.path.join("res", "ship-sprite-red-firing.png")
		else:
			assert(False)
			
		print("Loading", path_firing)
		self.firing_sprite = pygame.image.load(path_firing).convert_alpha()
		
		super(Ship, self).__init__(path)
		
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
			self.vx += -SHIP_ACCELERATION*math.sin(math.radians(self.rot))
			self.vy += -SHIP_ACCELERATION*math.cos(math.radians(self.rot))
			self.current_sprite = self.firing_sprite
		else:
			self.current_sprite = self.main_sprite
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
			
		if self.x < 0 or self.x > Map.current_map.rect.w or self.y < 0 or self.y > Map.current_map.rect.h:
			self.vx *= -1
			
	def respawn(self):
		super(Ship, self).respawn()
		self.x, self.y, self.rot = self.gamemode.get_spawn_pos(self)
		
	def collision_detect_others(self):
		teammates = self.gamemode.get_enemies(self)
		other_objects = [self.gamemode.objective] # It's a list, just for future-proofing
		
		objects = teammates + other_objects
		
		hit = False
		for obj in objects:
			point = pygame.sprite.collide_mask(obj, self)
			if point:
				# BONK!
				collision.elastic_collision(obj, self, point)
				hit = True
		return hit
		