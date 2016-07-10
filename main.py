import pygame

from player_ship import PlayerShip
from camera import Camera
from constants import DISP_WIDTH, DISP_HEIGHT

game_disp = None
game_clock = None

stop = False

objects = pygame.sprite.Group()

object_in_control = None
scene = None
camera = None

def init():
	global game_disp, game_clock, object_in_control, camera
	
	pygame.init()
	
	game_disp = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
	
	pygame.display.set_caption("Soccer in space!")
	game_clock = pygame.time.Clock()
	
	ship = PlayerShip(game_disp, 0)
	objects.add(ship)
	object_in_control = ship
	
	camera = Camera(1280, 720) # This should be the size of the map.
	
	loop()

def pollEvents():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			global stop
			stop = True
		elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
			object_in_control.handleInputs(event)
		
def loop():
	while not stop:
		pollEvents();
		game_disp.fill((0xff, 0xff, 0xff))
		
		for object in objects:
			object.action()
			game_disp.blit(object.image, camera.apply(object))
		
		pygame.display.update()
		game_clock.tick(60)
	quit()

def quit():
	pygame.quit()

init()
