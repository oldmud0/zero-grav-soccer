import os, math
from entity import Entity
from map import Map

class Ship(Entity):
	def __init__(self, surface, team):
		path = os.path.join("res", "ship-sprite.png")
		super(Ship, self).__init__(path, surface)
		
		if team == 0:
			# red team faces right
			self.x = Map.current_map.rect.w * 0.4
			self.y = Map.current_map.rect.h / 2
			self.rot = 270
		elif team == 1:
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
	
	def action(self, delta):
		if self.thrust:
			self.vx += -.1*math.sin(math.radians(self.rot))
			self.vy += -.1*math.cos(math.radians(self.rot))
		if self.left:
			self.rot += 2
		if self.right:
			self.rot -= 2
		if self.grabbing:
			pass
		
		self.move(delta)
		self.collision_detect()