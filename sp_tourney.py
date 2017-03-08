import pygame, os, json

class SinglePlayerTourney:
    """A single-player tournament mode.
    You fight AI until you are the winner.
    """
    
    level_maps = [
        "soccer_arcade1_tilemap.png",
        "soccer_arcade1_tilemap.png",
        "soccer_arcade1_tilemap.png"
    ]

    current_level = 0

    lives_left = 3
    
    wait_timer_max = 240
    wait_timer = 0
    waiting = False

    def __init__(self):
        pass

    def next_level(self):
        self.current_level += 1
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

    def update(self):
        if self.waiting:
            self.wait_timer -= 1
            if self.wait_timer == 0:
                self.waiting = False
                self._start_level()

class Bracket(pygame.surface.Surface):
    """A visualization of a tournament bracket.
    No loser's bracket.
    """
    
    bracket_name = "bracket-16"
    
    transition_progress = 90

    def __init__(self):
        self._parse_transition_data(self.bracket_name)
        
    def _parse_transition_data(self, path):
        transitions_file_path_ext = os.path.splitext(path)
        transitions_file_path = transitions_file_path_ext[0] + ".json"
        transitions_file = open(transitions_file_path).read()
        self.transitions = json.loads(transitions_file)
        
    def render(self):
        

    def transition(self):
        pass

class ContinueScreen(pygame.surface.Surface):
    """Continue?"""

    continue_sound = None # todo: haven't added one, yet

    continue_text_path = None # todo

    def __init__(self):
        pass