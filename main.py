import pygame, os

from entity import Entity
from map import Map

from settings import DISP_WIDTH, DISP_HEIGHT

game_disp = None
game_clock = None

stop = False

objects = pygame.sprite.Group()

def init():
	"""Initialize pygame and all objects/variables needed to begin the game."""
	global game_disp, game_clock, camera
	
	pygame.init()
	
	game_disp = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
	
	pygame.display.set_caption("Soccer in space!")
	game_clock = pygame.time.Clock()
	
	# Create the map
	map_path = os.path.join("res", "le_football_small.png")
	Map.current_map = Map(map_path, game_disp)
	
	# Create the ship
	from player_ship import PlayerShip
	ship = PlayerShip(game_disp, 0)
	objects.add(ship)
	Entity.ent_in_control = ship
	
	from camera import Camera
	camera = Camera(Map.current_map.rect.w, Map.current_map.rect.h) # This should be the size of the map.
	
	print(" -- Finished initializing --")
	
	loop()

def pollEvents():
	"""Process all (key) events passed to pygame."""
	for event in pygame.event.get():
		global stop
		if event.type == pygame.QUIT:
			stop = True
		elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
			if event.key == pygame.K_ESCAPE:
				stop = True
			Entity.ent_in_control.handleInputs(event)
		
def loop():
	"""Primary game loop."""
	while not stop:
		delta = game_clock.tick(60)
		
		pollEvents();
		game_disp.fill((0xff, 0xff, 0xff))
		
		game_disp.blit(Map.current_map.image, camera.apply(Map.current_map))
		
		# Render and update all objects
		for object in objects:
			object.action(delta)
			game_disp.blit(object.image, camera.apply(object))
		
		camera.update(Entity.ent_in_control)
		
		pygame.display.update()
	quit()
	
def quit():
	pygame.quit()

if __name__ == "__main__": # Make sure the game is not being run twice!
	init()