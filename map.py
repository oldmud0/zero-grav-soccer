import pygame, os, json, pygame.gfxdraw
from bg_stars import Stars
from settings import DEBUG

class Map(pygame.sprite.Sprite):
    current_map = None
    background = None

    def __init__(self, path, collision_path = None):
        pygame.sprite.Sprite.__init__(self)
                
        print("Loading", path) # Debugging purposes only
        self.image = pygame.image.load(path).convert()
        self.objects = pygame.sprite.Group()
        
        # Find or generate a collision map.
        if collision_path == None:
            print("Collision map path for", os.path.basename(path), "wasn't explicitly provided.")
            collision_path_ext = os.path.splitext(path)
            collision_path = collision_path_ext[0] + "-collision" + collision_path_ext[1]
            print("Loading", collision_path)
        
        try: # "Don't ask for permission. Ask for forgiveness instead"
            self.collision_map = pygame.image.load(collision_path).convert_alpha()
            self.mask = pygame.mask.from_surface(self.collision_map)
        except pygame.error:
            print("Couldn't find a collision map. Generating one instead.")
            self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()

        self.background = Stars(self.rect.size, False)

        self.collision_rects = []
        rects_file_path_ext = os.path.splitext(path)
        rects_file_path = rects_file_path_ext[0] + "-collision.txt"
        rects_file = open(rects_file_path).read()
        rects = json.loads(rects_file)
        for rect in rects:
            self.collision_rects.append(pygame.rect.Rect(rect[0], rect[1], rect[2], rect[3]))
            if DEBUG: pygame.gfxdraw.rectangle(self.image, rect, (35, 20, 220))
    
    def action(self, delta):
        for object in self.objects:
            object.action(delta)
        #self.background.update()
