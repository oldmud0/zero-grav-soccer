import pygame

class HUDElement(pygame.sprite.Sprite):
    """This class is not meant to be used directly."""
    
    path = None
    visible = True

    def __init__(self, position):
        super(HUDElement, self).__init__()
        print("Loading", self.path)
        self.image = pygame.image.load(self.path).convert_alpha()
        
        self.rect = self.image.get_rect()
        self.rect.w /= 10
        self.rect.center = position
    
    def action(self):
        pass
