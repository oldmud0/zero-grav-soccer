import pygame

class Map(pygame.sprite.Sprite):
	def __init__(self, path, surface):
		pygame.sprite.Sprite.__init__(self)
		self.surface = surface
		self.image = pygame.image.load(path).convert()
		self.rect = self.image.get_rect()
		