import pygame, os

from hud_element import HUDElement

class HUDScoreElement(HUDElement):
    
    path = os.path.join("res", "numbers.png")
    
    def __init__(self, position, get_value):
        super(HUDScoreElement, self).__init__(position)
        
        self.get_value = get_value # lambda, hope closure works all right
        self.value = self.get_value()
        
        self.sprite_sheet = self.image
        
        self.image = self.get_image()
    
    def action(self):
        new_value = self.get_value()
        if self.value != new_value:
            if new_value > 9:
                raise ValueError("Double digits for score not implemented yet")
            self.value = new_value
            self.image = self.get_image()
            
    def get_image(self):
        """Get the right number from the sprite sheet."""
        #image = pygame.Surface((32, 64), pygame.SRCALPHA).convert_alpha()
        #image.blit(self.sprite_sheet, self.rect.center, (32*self.value, 0, 32, 64))
        return self.sprite_sheet.subsurface(pygame.Rect(32*self.value, 0, 32, 64))
