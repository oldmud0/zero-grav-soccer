import pygame

from constants import DISP_WIDTH, DISP_HEIGHT

game_disp = None
game_clock = None

stop = False

objects = pygame.sprite.Group()

object_in_control = None
scene = None
camera = None

def init():
	"""Initialize pygame and all objects/variables needed to begin the game."""
	global game_disp, game_clock, object_in_control, camera, scene
	
	pygame.init()
	
	game_disp = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
	
	pygame.display.set_caption("Soccer in space!")
	game_clock = pygame.time.Clock()
	
	from player_ship import PlayerShip
	ship = PlayerShip(game_disp, 0)
	objects.add(ship)
	object_in_control = ship
	
	from map import Map
	scene = Map("res/le_football_small.png", game_disp)
	
	from camera import Camera
	camera = Camera(scene.rect.w, scene.rect.h) # This should be the size of the map.
	
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
			object_in_control.handleInputs(event)
		
def loop():
	"""Primary game loop."""
	while not stop:
		delta = game_clock.tick(60)
		
		pollEvents();
		game_disp.fill((0xff, 0xff, 0xff))
		
		game_disp.blit(scene.image, camera.apply(scene))
		
		# Render and update all objects
		for object in objects:
			object.action(delta)
			game_disp.blit(object.image, camera.apply(object))
		
		camera.update(object_in_control)
		
		pygame.display.update()
	quit()
	
def quit():
	pygame.quit()

if __name__ == "__main__": # Make sure the game is not being run twice!
	init()