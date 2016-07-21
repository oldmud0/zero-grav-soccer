import pygame
from ship import Ship

class PlayerShip(Ship):
	"""A player-controllable version of the Ship."""
	
	def __init__(self, surface, team, gamemode):
		self.team = None
		self.team = gamemode.request_change_team(self, team)
		self.gamemode = gamemode
		super(PlayerShip, self).__init__(surface, team, gamemode)
	
	def handleInputs(self, event):
		assert(event.type in (pygame.KEYDOWN, pygame.KEYUP))
		
		if event.type == pygame.KEYDOWN:
			on = 1
		if event.type == pygame.KEYUP:
			on = 0
		
		if event.key in (pygame.K_w, pygame.K_UP):
			self.thrust = on
		elif event.key in (pygame.K_a, pygame.K_LEFT):
			self.left = on
		elif event.key in (pygame.K_d, pygame.K_RIGHT):
			self.right = on
		elif event.key == pygame.K_SPACE:
			self.grabbing = on
		elif event.key == pygame.K_r:
			self.respawn()
			
	def respawn(self):
		super(PlayerShip, self).respawn()
		self.x, self.y, self.rot = self.gamemode.get_spawn_pos(self)
		