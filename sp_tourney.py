import pygame, os, events, json, random

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
    
    wait_timer_max = 360
    wait_timer = 0
    waiting = False

    def __init__(self, size):
        self.size = size
        self.current_scene = self.bracket = Bracket(size)
        self.next_level()

    def next_level(self):
        self.current_level += 1
        if DEBUG: print("Going to level", self.current_level)
        self.bracket.transition(self.current_level, True)
        self._wait()
        
    def redo_level(self):
        """Intended to be called from the Continue screen."""
        self._wait()

    def _wait(self):
        self.wait_timer = self.wait_timer_max
        self.waiting = True

    def _start_level(self):
        if self.current_level == len(self.level_maps):
            self.current_scene = Congratulations()

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
            pass

    def update(self):
        """Returns the current scene being rendered."""
        if self.waiting:
            self.wait_timer -= 1
            if self.wait_timer == 0:
                self.waiting = False
                self._start_level()
        self.current_scene.update()
        self.current_scene.render()
        return self.current_scene

class Bracket(pygame.surface.Surface):
    """A visualization of a tournament bracket.
    No loser's bracket.
    For now, the maximum number of players is
    hardcoded to be 16.
    """
    
    bracket_name = "bracket-16"
    bracket_path = os.path.join("res", "cinematic", bracket_name + ".png")

    player_human_path = os.path.join("res", "cinematic", "bracket-player.png")
    player_ai_path = os.path.join("res", "cinematic", "bracket-ai.png")
    
    transition_progress = 0
    transition_max_progress = 150

    def __init__(self, size):
        pygame.surface.Surface.__init__(self, size)
        self.real_size = size

        self.bracket_image = pygame.image.load(self.bracket_path)
        self.size = self.bracket_image.get_size()
        self.unscaled = pygame.surface.Surface(self.size)
        self._parse_transition_data(self.bracket_path)
        self._generate_bracket()
        self._load_player_icons()
        
    def _parse_transition_data(self, path):
        transitions_file_path_ext = os.path.splitext(path)
        transitions_file_path = transitions_file_path_ext[0] + ".json"
        transitions_file = open(transitions_file_path).read()

        self.transitions = json.loads(transitions_file)
       
    def _generate_bracket(self):
        self.players = []

        n_human = random.randrange(0, 16)

        for n in range(16):
            x, y = self.transitions["level1"][n]
            bp = self.BracketPlayer(n, x, y, "human" if n == n_human else "ai")
            self.players.append(bp)

        self.players_movable = self.players[:]

    def _load_player_icons(self):
        self.player_human = pygame.image.load(self.player_human_path).convert_alpha()
        self.player_ai = pygame.image.load(self.player_ai_path).convert_alpha()

    def update(self):
        if self.transition_progress > 0:
            self.transition_progress -= 1
            if self.transition_progress == self.transition_max_progress // 2:
                self.players_movable = self.players_movable_next
            if self.transition_twopart and self.transition_progress < self.transition_max_progress // 2:
                self.move_players(2)
            else:
                self.move_players(1)

    def move_players(self, part):
        pm = self.players_movable
        for i in range(0, len(pm)):
            player = pm[i]
            t_to_x, t_to_y = 0, 0
            if part == 1:
                t_from_x, t_from_y = self.transition_from[player.oldnum]
                t_to_x, t_to_y = self.transition_part1[player.oldnum]
                progress = (1 - self.transition_progress / self.transition_max_progress) * 2
            elif part == 2:
                t_from_x, t_from_y = self.transition_part1[player.oldnum]
                t_to_x, t_to_y = self.transition_part2[player.num]
                progress = 1 - self.transition_progress / (self.transition_max_progress // 2)
            else:
                raise ValueError("Given transition part is out of bounds")
            player.x = t_from_x + int((t_to_x - t_from_x) * progress)
            player.y = t_from_y + int((t_to_y - t_from_y) * progress)

    def render(self):
       self.unscaled.blit(self.bracket_image, pygame.Rect((0, 0), self.size))
       for player in self.players:
           if player.icon_type == "human":
               icon = self.player_human
           elif player.icon_type == "ai":
               icon = self.player_ai
           else:
               raise ValueError("Bracket player doesn't have a known icon type: " + str(player.icon_type))
           r = pygame.Rect(0, 0, 16, 16)
           r.center = player.x, player.y
           self.unscaled.blit(icon, r)
       pygame.transform.scale(self.unscaled, self.real_size, self)

    def transition(self, from_level, two_part):
        from_level += 1 # Sorry, ugly hack since arrays start from zero.
        self.transition_from = self.transitions["level"+str(from_level)]
        self.transition_twopart = two_part
        self._calculate_movable_players()
        if two_part:
            self.transition_part1 = self.transitions["level"+str(from_level)+"_transition"]
            self.transition_part2 = self.transitions["level"+str(from_level+1)]
        else:
            self.transition_part1 = self.transitions["level"+str(from_level+1)]
        self.transition_progress = self.transition_max_progress

    def _calculate_movable_players(self):
        pm = self.players_movable
        pmn = []
        for i in range(0, len(pm), 2):
            p1, p2 = pm[i], pm[i+1]
            p1.oldnum = p1.num
            p2.oldnum = p2.num
            # We know the human will always win in the animation
            if p1.icon_type == "human":
                pmn.append(p1)
                p1.num = i // 2
            elif p2.icon_type == "human":
                pmn.append(p2)
                p2.num = i // 2
            else:
                # Pick an AI player from random
                if random.randrange(2):
                    pmn.append(p1)
                    p1.num = i // 2
                else:
                    pmn.append(p2)
                    p2.num = i // 2
        self.players_movable_next = pmn

    class BracketPlayer:
        """Tiny representation of a player in the bracket.
        num: The player's number in the bracket.
        x, y: Position of the center of their icons.
        icon_type: The icon rendered for the player.
            Possible values: human, ai
        """
        __slots__ = ("num", "oldnum", "x", "y", "icon_type")
        def __init__(self, num, x, y, icon_type):
            self.num = self.oldnum = num
            self.x = x
            self.y = y
            self.icon_type = icon_type

class ContinueScreen(pygame.surface.Surface):
    """Continue?"""

    continue_sound = None # todo: haven't added one, yet

    continue_image = os.path.join("res", "cinematic", "continue.png")

    continue_timer = 10

    continue_tick_timer = 90

    def __init__(self):
        # Load sound and text
        pass

    def update(self):
        # Countdown timer
        # If timer == 0, game over
        # If keypress found, spend a life and redo level
        pass

    def count_down(self):
        pass

    def render(self):
        pass

class GameOver(pygame.surface.Surface):
    """Game over!"""

    gameover_sound = None

    gameover_image = os.path.join("res", "cinematic", "gameover.png")

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

    congrats_image = os.path.join("res", "cinematic", "congratulations.png")

    congrats_timer = 600

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
