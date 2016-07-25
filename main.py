import pygame, os

from entity import Entity
from ship import Ship
from player_ship import PlayerShip
from map import Map
from soccer import SoccerGame
from display import Display

from settings import DISP_WIDTH, DISP_HEIGHT, COLLISION_UNSTUCK_EVENT_ID, LOCAL_MP

window = None
game_disp = None
game_disp2 = None
clock = None

stop = False

def init():
	"""Initialize pygame and all objects/variables needed to begin the game."""
	global game_disp, game_disp2, clock, gamemode, window
	
	pygame.init()
	clock = pygame.time.Clock()
	
	# Main surface is here in case there are multiple smaller surfaces for splitscreen
	window = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
	
	if LOCAL_MP:
		surface_player1 = pygame.surface.Surface((DISP_WIDTH // 2, DISP_HEIGHT))
		game_disp = Display(surface_player1)
	else:
		game_disp = Display(window)
	
	pygame.display.set_caption("Soccer in space!")
	
	# Create the map
	map_path = os.path.join("res", "le_football.png")
	Map.current_map = Map(map_path)
	
	# Start the gamemode
	gamemode = SoccerGame()
	game_disp.load_game(gamemode)
	
	# Create the ship
	ship = PlayerShip(0, gamemode)
	Map.objects.add(ship)
	game_disp.ent_in_control = ship
	
	if LOCAL_MP:
		surface_player2 = pygame.surface.Surface((DISP_WIDTH // 2, DISP_HEIGHT))
		game_disp2 = Display(surface_player2)
		game_disp2.load_game(gamemode)
		
		ship2 = PlayerShip(1, gamemode)
		Map.objects.add(ship2)
		game_disp2.ent_in_control = ship2
	
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
			Entity.unstuck_all(Map.objects)
		elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
			if event.key == pygame.K_ESCAPE:
				stop = True
			game_disp.ent_in_control.handleInputs(event, 0)
			if LOCAL_MP:
				game_disp2.ent_in_control.handleInputs(event, 1)
	
def loop():
	"""Primary game loop."""
	while not stop:		
		pollEvents();
		
		delta = clock.tick(60)
		
		Map.current_map.action(delta)
		gamemode.update()
		
		game_disp.update()
		game_disp.render()
		
		window.blit(game_disp.surface, (0, 0))
		
		if LOCAL_MP:
			game_disp2.update()
			game_disp2.render()
			window.blit(game_disp2.surface, (DISP_WIDTH // 2 - 1, 0))
			
			# Draw separating line
			pygame.draw.line(window, (0,0,0), (DISP_WIDTH // 2 - 1, 0), (DISP_WIDTH // 2 - 1, DISP_HEIGHT - 1), 3)
		
		pygame.display.update()
	quit()
	
def quit():
	print("Exiting.")
	pygame.quit()

if __name__ == "__main__": # Make sure the game is not being run twice!
	init()