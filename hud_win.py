import pygame, os
from hud_element import HUDElement

class HUDWinMessage(HUDElement):
    
    path = os.path.join("res", "winner.png")

    timer = 0
    visible = False

    def __init__(self, position):
        super(HUDWinMessage, self).__init__(position)

        self.sprite_sheet = self.image

    def show(self, team):
        self.image = self.get_image(team)
        self.rect.size = self.image.get_size()
        self.timer = 360
        self.visible = True

    def action(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.visible = False

    def get_image(self, team):
        return self.sprite_sheet.subsurface(pygame.Rect(0, 32*team, 240, 32)).convert_alpha()
