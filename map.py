import pygame, os

class Map(pygame.sprite.Sprite):
	current_map = None
	objects = pygame.sprite.Group()

	def __init__(self, path, collision_path = None):
		pygame.sprite.Sprite.__init__(self)
				
		print("Loading", path) # Debugging purposes only
		self.image = pygame.image.load(path).convert()
		
		# Find or generate a collision map.
		if collision_path == None:
			print("Collision map path for", os.path.basename(path), "wasn't explicitly provided.")
			collision_path_ext = os.path.splitext(path)
			collision_path = collision_path_ext[0] + "-collision" + collision_path_ext[1]
			print("Loading", collision_path)
		
		try:
			self.collision_map = pygame.image.load(collision_path).convert_alpha() # "Don't ask for permission. Ask for forgiveness instead"
			self.mask = pygame.mask.from_surface(self.collision_map)
		except pygame.error:
			print("Couldn't find a collision map. Generating one instead.")
			self.mask = pygame.mask.from_surface(self.image)
		
		self.rect = self.image.get_rect()
	
	def action(self, delta):
		for object in self.objects:
			object.action(delta)