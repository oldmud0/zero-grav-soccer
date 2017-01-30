import pygame
from button import Button
import events
from bg_stars import Stars

class StartScreen(pygame.surface.Surface):
    """Main menu of the game"""

    button_group = pygame.sprite.Group()
    _button_selected = 0

    instructions_visible = False

    def __init__(self, size):
        pygame.surface.Surface.__init__(self, size)

        self.button_list = [
            Button(
                "res/menu/btn_play_off.png",
                "res/menu/btn_play_on.png",
                self.show_instructions, (size[0] // 2, size[1] // 2 + 30)),
            Button(
                "res/menu/btn_quit_off.png",
                "res/menu/btn_quit_on.png",
                self.quit_game, (size[0] // 2, size[1] // 2 + 80))
        ]

        for button in self.button_list:
            self.button_group.add(button)

        self.button_selected.select()
        self.logo = pygame.image.load("res/menu/logo.png").convert_alpha()
        self.background = Stars(size)
        self.instructions = pygame.image.load("res/menu/instructions.png").convert()
        self.text_font = pygame.font.Font("res/gohufont-11.ttf", 11)
        self.text_copyright = self.text_font.render("Copyright (c) 2016-2017 Bennett Ramirez", False, (255, 255, 255))
        self.text_version = self.text_font.render("Pre-alpha 0.1.2", False, (255, 255, 255))
        self.render()

    def handle_inputs(self, event):
        if event.type == pygame.KEYDOWN:
            if self.instructions_visible:
                if event.key == pygame.K_RETURN:
                    self.start_game()
            else:
                # Select buttons
                inc = False
                if event.key == pygame.K_UP: inc = 1
                elif event.key == pygame.K_DOWN: inc = -1
                if inc:
                    self.button_selected.deselect()
                    self._button_selected = (self._button_selected + inc) % len(self.button_list)
                    self.button_selected.select()
                    self.render()
                if event.key == pygame.K_RETURN:
                    self.button_selected.action()

    def render(self):
        """Redraw start screen whenever it changes."""
        self.fill((0,0,0))
        if self.instructions_visible:
            self.blit(self.instructions, (0,0))
        else:
            self.blit(self.background, (0,0))
            self.button_group.draw(self)
            self.blit(self.logo, ((self.get_width() - self.logo.get_width()) // 2, round(self.get_height() * .2)))
            self.blit(self.text_copyright, ((self.get_width() - self.text_copyright.get_width(), \
                    self.get_height() - self.text_copyright.get_height())))
            self.blit(self.text_version, ((0, \
                    self.get_height() - self.text_version.get_height())))

    def show_instructions(self):
        self.instructions_visible = True
        self.render()

    def start_game(self):
        pygame.event.post(pygame.event.Event(events.START_GAME, {"called_by": self}))

    def quit_game(self):
        pygame.event.post(pygame.event.Event(events.QUIT, {"called_by": self}))

    def reset(self):
        """Prepare menu for redisplay due to a change in game state"""
        self._button_selected = 0
        self.instructions_visible = False
        self.render()

    @property
    def button_selected(self):
        return self.button_list[self._button_selected]
