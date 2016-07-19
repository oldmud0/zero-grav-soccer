import pygame

from map import Map
from ball import Ball
from soccer_hud import SoccerHUD

class SoccerGame:
	"""Define game behavior for the soccer gamemode.
	Red team is 0, and blue team is 1.
	"""
	
	red_team_score = 0
	red_team_ships = []
	
	blue_team_score = 0
	blue_team_ships = []
	
	_ball = None
	
	def __init__(self, surface):
		self._ball = Ball(surface)
		surface.objects.add(self._ball)
		
	def get_spawn_pos(self, ship):
		if ship.team == 0:
			return map.current_map.rect.w / 2 - 50, map.current_map.rect.h / 3 * (1 + self.red_team_ships.index(ship))
		elif ship.team == 1:
			return map.current_map.rect.w / 2 + 50, map.current_map.rect.h / 3 * (1 + self.blue_team_ships.index(ship))
		else:
			assert(False)
	
	@property
	def objective(self):
		"""Return the main objective of the game (the ball)."""
		return self._ball
		
	@property
	def hud(self):
		"""Return the HUD elements suggested for the gamemode."""
		return SoccerHUD
	
	def respawn_all(self):
		for ship in self.red_team_ships + self.blue_team_ships:
			ship.respawn()
		self._ball.respawn()
	
	def request_change_team(self, ship, requested):
		"""Check for team balance, then assign a team to the ship."""
		
		if len(self.red_team_ships) - 1 > len(self.blue_team_ships):
			# Too many people in red team. Assign to blue instead.
			requested = 1
		elif len(self.blue_team_ships) - 1 > len(self.red_team_ships):
			# and vice versa.
			requested = 0
		else:
			# If no problems, just fulfill the request.
			pass
		
		if ship.team == requested or 0 > requested > 1:
			# Ignore if it's already the same team, or if invalid
			return
		
		self.change_team(ship, requested)
		return requested
	
	def change_team(self, ship, team):
		try:
			self.blue_team_ships.remove(ship)
			self.red_team_ships.remove(ship)
		except:
			pass
		
		if ship.team == 0:
			self.red_team_ships.append(ship)
		elif ship.team == 1:
			self.blue_team_ships.append(ship)
	
	def get_teammates(self, ship):
		"""Get the list of a ship's teammates."""
		if ship.team == 0:
			teammates = list(self.red_team_ships)
		if ship.team == 1:
			teammates = list(self.blue_team_ships)
		teammates.remove(ship)
		return teammates
		
	def get_enemies(self, ship):
		"""Get the list of a ship's enemies. Useful for collision checks."""
		if ship.team == 0:
			enemies = list(self.blue_team_ships)
		if ship.team == 1:
			enemies = list(self.red_team_ships)
		return enemies
	