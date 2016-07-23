import pygame, os

from entity import Entity
from ship import Ship
from player_ship import PlayerShip
from map import Map
from soccer import SoccerGame
from display import Display
from camera import Camera

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
	Map.current_map = Map(map_path)
	
	# Start the gamemode
	gamemode = SoccerGame(game_disp)
	game_disp.load_game(gamemode)
	
	# Create the ship
	ship = PlayerShip(game_disp, 0, gamemode)
	game_disp.objects.add(ship)
	game_disp.ent_in_control = ship
	
	# Create another ship!
	#ship2 = Ship(game_disp, 1, gamemode)
	#game_disp.objects.add(ship2)
	
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
			game_disp.ent_in_control.handleInputs(event)
	
def loop():
	"""Primary game loop."""
	while not stop:		
		pollEvents();
		
		game_disp.update()
		gamemode.update()
		game_disp.render()
	quit()
	
def quit():
	print("Exiting.")
	pygame.quit()

if __name__ == "__main__": # Make sure the game is not being run twice!
	init()