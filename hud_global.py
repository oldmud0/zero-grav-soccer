import pygame
from hud import HUD

class GlobalHUD(pygame.surface.Surface):

    def __init__(self, size, gamemode):
        pygame.surface.Surface.__init__(self, size, pygame.SRCALPHA, 32)
        self.hud = HUD(self)
        self.hud.acquire_global_gamemode_hud(gamemode)

    def update(self):
        self.hud.action()
    
    def render(self):
        self.fill((0,0,0,0))
        for element in self.hud.elements:
            if element.visible:
                self.blit(element.image, element.rect)
