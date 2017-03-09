import pygame
import random

class Stars(pygame.surface.Surface):

    density = 150

    def __init__(self, size, animated):
        pygame.surface.Surface.__init__(self, size)
        self.size = size

        self.random = random.Random()

        self.generate(animated)
        self._animated = animated

    def animate(self):
        if self._animated:
            max_x, max_y = self.size
            self.fill((0, 0, 0), pygame.Rect(0, 0, max_x, max_y))
            for star in self.stars:
                x, y, speed, size = star.x, star.y, star.speed, star.size
                self.fill((255, 255, 255), pygame.Rect(int(x), int(y), size, size))
                if y - speed < 0:
                    star.x = self.random.randint(0, max_x)
                    star.y = (y - speed) % max_y
                else:
                    star.y -= speed
        else:
            raise Exception("An attempt was made to animate a non-animated star field.")

    def generate(self, animated):
        max_x, max_y = self.size
        if animated:
            self.stars = []
            for _ in range(self.density):
                x = self.random.randint(0, max_x) 
                y = self.random.randint(0, max_y)
                speed = self.random.uniform(.4, 2)
                size = self.random.randint(1, 2)
                self.stars.append(Star(x, y, speed, size))
        else:
            self.stars = zip((self.random.randint(0, max_x) for _ in range(self.density)),
                    (self.random.randint(0, max_y) for _ in range(self.density)))
            for pos in self.stars:
                self.fill((255, 255, 255), pygame.Rect(pos, (1, 1)))

class Star:
    """Represents a single star.
    (Okay, don't start calling me crazy now...)
    """
    # Using __slots__ saves on memory,
    # as Python doesn't expect any more attributes to be added
    __slots__ = ("x", "y", "speed", "size")
    def __init__(self, x, y, speed, size):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
