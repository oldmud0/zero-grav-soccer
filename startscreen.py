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

        self.logo = StartScreenLogo()
        self.logo.static = True

        self.logo_animation = True
        self.logo_animation_progress = 0
        self.shake = False

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

    def update(self):
        """Update anything that needs updating,
        including re-rendering the start screen if needed.
        """
        if self.instructions_visible:
            pass
        else:
            if self.logo_animation:
                self.logo_animation_progress += 1/60
                if self.logo_animation_progress >= 1:
                    self.logo_animation = False
                    
                    self.shake = True
                    self.shake_progress = 0
                    self.shake_alternator = 1
                    self.scroll(-2)
                    
                    self.logo.static = True
                self.render()
            if self.shake:
                self.shake_progress += 1
                if 0 <= self.shake_progress <= 20:
                    if not self.shake_progress % 4:
                        self.scroll(4 * self.shake_alternator)
                        self.shake_alternator = -self.shake_alternator
                elif 20 < self.shake_progress < 30:
                    if not self.shake_progress % 2:
                        self.scroll(3 * self.shake_alternator)
                        self.shake_alternator = -self.shake_alternator
                elif 30 < self.shake_progress < 40:
                    if not self.shake_progress % 2:
                        self.scroll(2 * self.shake_alternator)
                        self.shake_alternator = -self.shake_alternator
                elif self.shake_progress >= 40:
                    self.shake = False
            # Animate logo if applicable
            if self.logo.update(): self.render()

    def render(self):
        """Redraw start screen whenever it changes."""
        self.fill((0,0,0))
        if self.instructions_visible:
            self.blit(self.instructions, (0,0))
        else:
            self.blit(self.background, (0,0))
            self.button_group.draw(self)

            if self.logo_animation:
                # Calculate the new scaled logo dimensions
                new_w = round(self.logo.get_width() * (10 - self.logo_animation_progress * 9))
                new_h = round(self.logo.get_height() * (10 - self.logo_animation_progress * 9))
                new_surf = pygame.transform.scale(self.logo.image, (new_w, new_h))
                new_rect = new_surf.get_rect()
                new_rect.midtop = (self.get_width() // 2, round(self.get_height() * .2 * self.logo_animation_progress))
                self.blit(new_surf, new_rect)
            else:
                self.blit(self.logo.image, ((self.get_width() - self.logo.get_width()) // 2, round(self.get_height() * .2)),
                        self.logo.rect)
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

class StartScreenLogo(pygame.sprite.Sprite):

    _static = True
    frame_current = 0
    frame_max = 4

    update_timer = 60/5
    update_timer_max = 60/5

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.image_static = pygame.image.load("res/menu/logo.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.image_animated = pygame.image.load("res/menu/logo_anim.png").convert_alpha()

    def update(self):
        """Returns True if there was a change in the image."""
        if not self.static:
            return self.animate()

    def animate(self):
        """Animates the electricity effect of logo.
        Returns True if there was an actual change in the image.
        """
        self.update_timer -= 1
        if self.update_timer == 0:
            self.rect.y = self.frame_current * self.rect.h
            self.frame_current = (self.frame_current + 1) % self.frame_max
            self.update_timer = self.update_timer_max
            return True

    @property
    def static(self):
        return self._static

    @static.setter
    def static(self, val):
        self._static = val
        if self._static:
            self.image = self.image_static
        else:
            self.image = self.image_animated

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height
