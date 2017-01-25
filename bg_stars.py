import pygame
import random

class Stars(pygame.surface.Surface):

    density = 150

    def __init__(self, size):
        pygame.surface.Surface.__init__(self, size)

        self.random = random.Random()

        self.stars = zip((self.random.randint(0, size[0]) for _ in range(self.density)),
                (self.random.randint(0, size[1]) for _ in range(self.density)))

        self.generate()

    def update(self):
        pass

    def generate(self):
        for pos in self.stars:
            self.fill((255, 255, 255), pygame.Rect(pos, (1, 1)))
