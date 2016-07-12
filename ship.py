import os, math
from entity import Entity

class Ship(Entity):
	def __init__(self, surface, team):
		"""
		if team == 0:
			# red team
		elif team == 1:
			# blue team
		else:
			assert(False)
		"""
		path = os.path.join("res", "ship-sprite.png")
		super(Ship, self).__init__(path, surface)
		
		self.thrust	= False
		self.left = False
		self.right = False
		self.grabbing = False
	
	def action(self):
		if self.thrust:
			self.vx += -.1*math.sin(math.radians(self.rot))
			self.vy += -.1*math.cos(math.radians(self.rot))
		if self.left:
			self.rot += 2
		if self.right:
			self.rot -= 2
		if self.grabbing:
			pass
		
		self.move()