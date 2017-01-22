import pygame

class Button(pygame.sprite.Sprite):
    """Represents a button that can be used in UI."""

    def __init__(self, off_path, on_path, action, pos):
        pygame.sprite.Sprite.__init__(self)

        self.image_on = pygame.image.load(on_path).convert()
        self.image_off = pygame.image.load(off_path).convert()

        self.image = self.image_off

        self.action = action

        self.rect = self.image.get_rect()
        self.rect.center = pos

    def select(self):
        self.image = self.image_on

    def deselect(self):
        self.image = self.image_off
