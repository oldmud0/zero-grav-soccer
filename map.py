import pygame

class Map(pygame.sprite.Sprite):
	current_map = None

	def __init__(self, path, surface):
		pygame.sprite.Sprite.__init__(self)
		
		self.surface = surface
		
		print("Loading", path) # Debugging purposes only
		self.image = pygame.image.load(path).convert()
		
		self.rect = self.image.get_rect()
		