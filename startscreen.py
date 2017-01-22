import pygame
from button import Button
import events

class StartScreen(pygame.surface.Surface):
    """Main menu of the game"""

    button_group = pygame.sprite.Group()

    _button_selected = 0

    def __init__(self, size):
        pygame.surface.Surface.__init__(self, size)

        self.button_list = [
            Button(
                "res/menu/btn_play_off.png",
                "res/menu/btn_play_on.png",
                self.start_game, (size[0] // 2, size[1] // 2 + 30)),
            Button(
                "res/menu/btn_quit_off.png",
                "res/menu/btn_quit_on.png",
                self.quit_game, (size[0] // 2, size[1] // 2 + 80))
        ]

        for button in self.button_list:
            self.button_group.add(button)
        
        self.button_selected.select()
        self.render()

    def handle_inputs(self, event):
        if event.type == pygame.KEYDOWN:
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
        self.button_group.draw(self)

    def start_game(self):
        pygame.event.post(pygame.event.Event(events.START_GAME, {"called_by": self}))

    def quit_game(self):
        pygame.event.post(pygame.event.Event(events.QUIT, {"called_by": self}))

    @property
    def button_selected(self):
        return self.button_list[self._button_selected]
