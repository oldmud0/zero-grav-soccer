import pygame

class Entity(pygame.sprite.Sprite):
	def __init__(self, path, surface):
		pygame.sprite.Sprite.__init__(self)
		
		self.surface = surface
		
		print("Loading", path)
		self.image = pygame.image.load(path).convert_alpha()
		self.original_image = self.image
		
		self.rect = self.image.get_rect()
		
		self.x = 0
		self.y = 0
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
		from main import frame_time
		ideal_frame_time = 60 # FPS
		displacement_factor = frame_time / ideal_frame_time
		
		self.x += self.vx * displacement_factor
		self.y += self.vy * displacement_factor
		
		self.rect.center = (round(self.x), round(self.y))
		
		self.rot = (self.rot + self.vrot) % 360
		self.rot_center()
