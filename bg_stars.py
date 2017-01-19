import pygame
import random

class Stars(pygame.sprite.Sprite):

    density = 150

    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.random = random.Random()

        self.stars = zip((self.random.randint(0, size[0]) for _ in range(self.density)),
                (self.random.randint(0, size[1]) for _ in range(self.density)))

        self.rect = self.image.get_rect()

        self.generate()

    def update(self):
        pass

    def generate(self):
        for pos in self.stars:
            self.image.fill((255, 255, 255), pygame.Rect(pos, (1, 1)))
