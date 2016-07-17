import pygame

import collision
from map import Map

from settings import COLLISION_DAMPING, COLLISION_ALGORITHM_EXPERIMENTAL, COLLISION_STUCK_THRESHOLD, COLLISION_UNSTUCK_AGGRESSION

class Entity(pygame.sprite.Sprite):
	ent_in_control = None
	
	mass = 100
	
	collision_counter = 0
	collision_threshold = COLLISION_STUCK_THRESHOLD

	def __init__(self, path, surface):
		pygame.sprite.Sprite.__init__(self)
		
		self.surface = surface
		
		print("Loading", path) # Debugging purposes only
		self.image = pygame.image.load(path).convert_alpha()
		self.original_image = self.image
		
		self.mask = pygame.mask.from_surface(self.image)
		
		self.rect = self.image.get_rect()
		
		self.respawn()
	
	def respawn(self):
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
		# Check if the collision was with a map
		point = pygame.sprite.collide_mask(Map.current_map, self)
		if point:
			if COLLISION_ALGORITHM_EXPERIMENTAL:
				self.vx, self.vy = collision.calculate_reflection_angle(Map.current_map.mask, point, (self.vx, self.vy))
			else: 
				self.vx, self.vy = collision.simple_collision(Map.current_map.mask, point, (self.vx, self.vy))
			self.vx, self.vy = self.vx * COLLISION_DAMPING, self.vy * COLLISION_DAMPING
			
			self.collision_counter += 1
			return True
		return False
	
	def unstuck_all(objects):
		"""Fix all entities that appears to be stuck.
		If their collision counter is above a certain threshold, they're probably stuck.
		"""
		for obj in objects:
			if obj.collision_counter > obj.collision_threshold:
				print("Object at", (obj.x, obj.y), "is stuck. Trying to unstuck...")
				obj.unstuck()
			obj.collision_counter = 0
	
	def unstuck(self):
		"""Unstuck an entity by checking for any open spots we could put it on."""
		mask = Map.current_map.mask
		
		x_max, y_max = mask.get_size()
		orig_x, orig_y = round(self.x), round(self.y)
		x, y = orig_x , orig_y
		unstuck_aggr = COLLISION_UNSTUCK_AGGRESSION
		
		# Vertical check for any open spots we could put the entity on...
		while y > 0:
			if not mask.get_at((x, y)):
				self.y = y
				self.vy = -unstuck_aggr
				return
			y -= unstuck_aggr
		y = orig_y
		while y < y_max:
			if not mask.get_at((x, y)):
				self.y = y
				self.vy = unstuck_aggr
				return
			y += unstuck_aggr
		y = orig_y
		
		# Horizontal spots?
		while x > 0:
			if not mask.get_at((x, y)):
				self.x = x
				self.vx = -unstuck_aggr
				return
			x -= unstuck_aggr
		x = orig_x
		while x < x_max:
			if not mask.get_at((x, y)):
				self.x = x
				self.vx = unstuck_aggr
				return
			x += unstuck_aggr
		x = orig_x
		
		# Diagonal spots
		while x > 0 and y > 0:
			if not mask.get_at((x, y)):
				self.x, self.y = x, y
				self.vx, self.vy = -unstuck_aggr, -unstuck_aggr
				return
			x, y = x - unstuck_aggr, y - unstuck_aggr
		x, y = orig_x, orig_y
		while x < x_max and y < y_max:
			if not mask.get_at((x, y)):
				self.x, self.y = x, y
				self.vx, self.vy = unstuck_aggr, unstuck_aggr
				return
			x, y = x + unstuck_aggr, y + unstuck_aggr
		x, y = orig_x, orig_y
		while x > 0 and y < y_max:
			if not mask.get_at((x, y)):
				self.x, self.y = x, y
				return
			x, y = x - unstuck_aggr, y + unstuck_aggr
		x, y = orig_x, orig_y
		while x < x_max and y > 0:
			if not mask.get_at((x, y)):
				self.x, self.y = x, y
				return
			x, y = x + unstuck_aggr, y - unstuck_aggr
		x, y = orig_x, orig_y
		
		# All right, I officially give up now.
		print("Couldn't unstuck object!")
	