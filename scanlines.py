import pygame

class Scanlines(pygame.Surface):
    """Adds scanlines in post-processing."""

    color = (66, 134, 244)
    scanline_height = 1 
    interval = 2

    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.fill((0xff, 0xff, 0xff))
        self.render()

    def render(self):
        w, h = self.get_size()
        for i in range(0, h, self.interval):
            self.fill(self.color, pygame.rect.Rect(0, i, w, self.scanline_height))

    def apply(self, surface):
        surface.blit(self, (0, 0), special_flags=pygame.BLEND_MULT)
