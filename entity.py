import pygame

class Entity(pygame.sprite.Sprite):
	def __init__(self, path, surface):
		pygame.sprite.Sprite.__init__(self)
		
		self.surface = surface
		
		print("Loading", path)
		self.image = pygame.image.load(path).convert_alpha()
		self.original_image = self.image
		
		self.rect = self.image.get_rect()
		
		self.rot = 0
		
		self.vx = 0
		self.vy = 0
		self.vrot = 0
	
	def rot_center(self):
		loc = self.rect.center
		self.image = pygame.transform.rotate(self.original_image, self.rot)
		self.rect = self.image.get_rect()
		self.rect.center = loc
	
	def action(self):
		self.move()
	
	def move(self):
		x = self.rect.center[0]
		y = self.rect.center[1]
		self.rect.center = (x + self.vx, y + self.vy)
		
		self.rot = (self.rot + self.vrot) % 360
		self.rot_center()
		print(self.vx, self.vy)
