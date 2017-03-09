import pygame, os, events, json

from settings import DEBUG

class SinglePlayerTourney:
    """A single-player tournament mode.
    You fight AI until you are the winner.
    """
    
    level_maps = [
        "soccer_arcade1_tilemap.png",
        "soccer_arcade1_tilemap.png",
        "soccer_arcade1_tilemap.png"
    ]

    current_level = -1

    lives_left = 3
    
    wait_timer_max = 240
    wait_timer = 0
    waiting = False

    def __init__(self, size):
        self.size = size
        self.current_scene = self.bracket = Bracket(size)
        self.next_level()

    def next_level(self):
        self.current_level += 1
        if DEBUG: print("Going to level", self.current_level)
        self._wait()
        
    def redo_level(self):
        """Intended to be called from the Continue screen."""
        self._wait()

    def _wait(self):
        self.wait_timer = self.wait_timer_max
        self.waiting = True

    def _start_level(self):
        pygame.event.post(pygame.event.Event(events.START_GAME, {
            "called_by": self,
            "map": self.level_maps[self.current_level],
            "mode": "vs_ai"
        }))

    def handover(self, outcome):
        """Main loop to singleplayer manager handover."""
        if outcome == 0:
            # P1's team won. Go to the next level!
            self.next_level()
        else:
            # todo You lost. Continue??
            pass
    
    def update(self):
        """Returns the current scene being rendered."""
        if self.waiting:
            self.wait_timer -= 1
            if self.wait_timer == 0:
                self.waiting = False
                self._start_level()
        self.current_scene.render()
        return self.current_scene

class Bracket(pygame.surface.Surface):
    """A visualization of a tournament bracket.
    No loser's bracket.
    """
    
    bracket_name = "bracket-16"
    bracket_path = os.path.join("res", "cinematic", bracket_name + ".png")
    
    transition_progress = 90

    def __init__(self, size):
        pygame.surface.Surface.__init__(self, size)
        self.real_size = size

        self.bracket_image = pygame.image.load(self.bracket_path)
        self.size = self.bracket_image.get_size()
        self.unscaled = pygame.surface.Surface(self.size)
        self._parse_transition_data(self.bracket_path)
        
    def _parse_transition_data(self, path):
        transitions_file_path_ext = os.path.splitext(path)
        transitions_file_path = transitions_file_path_ext[0] + ".json"
        transitions_file = open(transitions_file_path).read()
        self.transitions = json.loads(transitions_file)
        
    def render(self):
       self.unscaled.blit(self.bracket_image, pygame.Rect((0, 0), self.size))
       pygame.transform.scale(self.unscaled, self.real_size, self)
    def transition(self):
        pass

class ContinueScreen(pygame.surface.Surface):
    """Continue?"""

    continue_sound = None # todo: haven't added one, yet

    continue_text_path = None # todo

    continue_timer = 10

    def __init__(self):
        # Load sound and text
        pass

    def update(self):
        # Countdown timer
        # If timer == 0, game over
        # If keypress found, spend a life and redo level
        pass

    def render(self):
        pass

class GameOver(pygame.surface.Surface):
    """Game over!"""

    gameover_sound = None

    gameover_image = None

    gameover_timer = 240

    def __init__(self):
        # Load sound and text
        pass

    def update(self):
        # Countdown timer
        # Fade in image
        # Then go back to menu
        pass

    def render(self):
        pass

class Congratulations(pygame.surface.Surface):
    """Congratulations!"""

    congrats_sound = None

    congrats_image = None

    congrats_timer = 240

    def __init__(self):
        # Load sound and text
        pass

    def update(self):
        # Countdown timer
        # Fade in image
        # Then go back to menu
        pass

    def render(self):
        pass
