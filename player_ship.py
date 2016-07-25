import pygame
from ship import Ship
from ship_controls import ship_controls

class PlayerShip(Ship):
	"""A player-controllable version of the Ship."""
	
	def __init__(self, surface, team, gamemode):
		self.team = None
		self.team = gamemode.request_change_team(self, team)
		super(PlayerShip, self).__init__(surface, team, gamemode)
	
	def handleInputs(self, event, player):
		assert(event.type in (pygame.KEYDOWN, pygame.KEYUP))
		
		if event.type == pygame.KEYDOWN:
			on = 1
		if event.type == pygame.KEYUP:
			on = 0
		
		controls = ship_controls[player]
		
		if event.key in controls["thrust"]:
			self.thrust = on
		elif event.key in controls["left"]:
			self.left = on
		elif event.key in controls["right"]:
			self.right = on
		elif event.key in controls["grabbing"]:
			self.grabbing = on
		elif event.key in controls["respawn"]:
			self.respawn()
