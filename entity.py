import pygame

import collision
from map import Map

from settings import COLLISION_DAMPING, COLLISION_ALGORITHM_EXPERIMENTAL

class Entity(pygame.sprite.Sprite):
	ent_in_control = None

	def __init__(self, path, surface):
		pygame.sprite.Sprite.__init__(self)
		
		self.surface = surface
		
		print("Loading", path) # Debugging purposes only
		self.image = pygame.image.load(path).convert_alpha()
		self.original_image = self.image
		
		self.mask = pygame.mask.from_surface(self.image)
		
		self.rect = self.image.get_rect()
		
		self.x = 0
		self.y = 0
		self.rot = 0
		
		self.vx = 0
		self.vy = 0
		self.vrot = 0
	
	def rot_center(self):
		"""Rotate the entity's sprite while preserving the center.
		This is done by taking the original sprite's center, rotating the sprite,
		and then giving the rotated sprite the old center.
		"""
		loc = self.rect.center
		self.image = pygame.transform.rotate(self.original_image, self.rot)
		self.rect = self.image.get_rect()
		self.rect.center = loc
	
	def action(self, delta):
		self.move()
		self.collision_detect()
	
	def move(self, delta):
		"""Move a sprite using time-based movement."""
		ideal_frame_time = 60 # FPS
		displacement_factor = delta / ideal_frame_time
				
		self.x += self.vx * displacement_factor
		self.y += self.vy * displacement_factor
		
		# If we do not round our floats, pygame will floor it for us (bad)
		self.rect.center = (round(self.x), round(self.y))
		
		self.rot = (self.rot + self.vrot) % 360
		self.rot_center()
	
	def collision_detect(self):
		"""Check for collisions against other entities or the map.
		Collision detection is very tricky.
		"""
		point = pygame.sprite.collide_mask(Map.current_map, self)
		if point:
			# First, check if the collision was with a map or entity
			if COLLISION_ALGORITHM_EXPERIMENTAL:
				self.vx, self.vy = collision.calculate_reflection_angle(Map.current_map.mask, point, (self.vx, self.vy))
			else 
				self.vx, self.vy = collision.simple_collision(Map.current_map.mask, point, (self.vx, self.vy))
			self.vx, self.vy = self.vx * COLLISION_DAMPING, self.vy * COLLISION_DAMPING