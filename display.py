import pygame

from settings import DISP_WIDTH, DISP_HEIGHT
from map import Map
from entity import Entity
from hud import HUD
from camera import Camera

class Display:
    """Holds all of the game's internals and objects."""
    
    _ent_in_control = None
    
    def __init__(self, size):
        self.surface = pygame.surface.Surface(size)
        self.hud = HUD(self.surface)
    
    def load_game(self, gamemode):
        self.camera = Camera(Map.current_map.rect.w, Map.current_map.rect.h, self.surface.get_width(), self.surface.get_height())
        self.hud.acquire_gamemode_hud(gamemode, self.camera)
        
    def update(self):
        self.camera.update()
        self.hud.action()
    
    @property
    def ent_in_control(self):
        return self._ent_in_control
        
    @ent_in_control.setter
    def ent_in_control(self, ent):
        self._ent_in_control = ent
        self.camera.target = ent
        
    def render(self):
        self.surface.fill((0xff, 0xff, 0xff))
        
        bg = Map.current_map.background
        if bg is not None:
            self.surface.blit(bg, (0,0))

        self.surface.blit(Map.current_map.image, self.camera.apply(Map.current_map))

        for object in Map.current_map.objects:
            self.surface.blit(object.image, self.camera.apply(object))

        for element in self.hud.elements:
            if element.visible:
                self.surface.blit(element.image, element.rect)
