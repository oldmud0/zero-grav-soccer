import pygame, os

class HUD:
    """Heads-up display"""
    
    def __init__(self, surface):
        self.surface = surface
        self.elements = pygame.sprite.Group()
        
    def reset_hud(self):
        self.elements.clear()
        
    def acquire_gamemode_hud(self, gamemode, camera):
        self.elements.add(gamemode.new_hud(self.surface.get_width(), \
                self.surface.get_height(), camera))

    def acquire_global_gamemode_hud(self, gamemode):
        self.elements.add(gamemode.new_global_hud(self.surface.get_width(), \
            self.surface.get_height()))

    def action(self):
        for element in self.elements:
            element.action()
