import pygame

from settings import DISP_WIDTH, DISP_HEIGHT
from map import Map
from entity import Entity
from hud import HUD
from camera import Camera

class Display:
    """Holds all of the game's internals and objects."""
    
    _ent_in_control = None
    
    def __init__(self, surface):
        self.surface = surface
        self.hud = HUD(surface)
        self.surface_scaled = pygame.Surface((surface.get_width()*2, surface.get_height()*2))
    
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
            self.surface.blit(bg.image, self.camera.apply(bg))

        self.surface.blit(Map.current_map.image, self.camera.apply(Map.current_map))

        for object in Map.current_map.objects:
            self.surface.blit(object.image, self.camera.apply(object))
        
        self.hud.elements.draw(self.surface)

        pygame.transform.scale(self.surface, self.surface_scaled.get_size(), self.surface_scaled)
