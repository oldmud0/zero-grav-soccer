import pygame, os

from entity import Entity
from ship import Ship
from map import Map
from soccer import SoccerGame
from display import Display

from settings import COLLISION_UNSTUCK_EVENT_ID

game_disp = None

stop = False

def init():
	"""Initialize pygame and all objects/variables needed to begin the game."""
	global game_disp, camera, gamemode
	
	pygame.init()
	
	game_disp = Display()
	pygame.display.set_caption("Soccer in space!")
	
	# Create the map
	map_path = os.path.join("res", "le_football.png")
	Map.current_map = Map(map_path, game_disp)
	
	# Start the gamemode
	gamemode = SoccerGame(game_disp)
	game_disp.hud.acquire_gamemode_hud(gamemode)
	
	# Create the ship
	from player_ship import PlayerShip
	ship = PlayerShip(game_disp, 0, gamemode)
	game_disp.objects.add(ship)
	Entity.ent_in_control = ship
	
	# Create another ship!
	ship2 = Ship(game_disp, 1, gamemode)
	game_disp.objects.add(ship2)
	
	from camera import Camera
	game_disp.camera = Camera(Map.current_map.rect.w, Map.current_map.rect.h) # This should be the size of the map.
	
	pygame.time.set_timer(COLLISION_UNSTUCK_EVENT_ID, 1000)
	
	print("Finished initializing.")
	
	loop()

def pollEvents():
	"""Process all (key) events passed to pygame."""
	for event in pygame.event.get():
		global stop
		if event.type == pygame.QUIT:
			stop = True
		elif event.type == COLLISION_UNSTUCK_EVENT_ID:
			Entity.unstuck_all(game_disp.objects)
		elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
			if event.key == pygame.K_ESCAPE:
				stop = True
			Entity.ent_in_control.handleInputs(event)
		
def loop():
	"""Primary game loop."""
	while not stop:		
		pollEvents();
		
		game_disp.update()
		game_disp.render()
	quit()
	
def quit():
	print("Exiting.")
	pygame.quit()

if __name__ == "__main__": # Make sure the game is not being run twice!
	init()