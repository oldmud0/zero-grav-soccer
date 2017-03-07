import pygame, os, events

from settings import DISP_WIDTH, DISP_HEIGHT

from map import Map
from ball import Ball

from hud_score import HUDScoreElement
from hud_arrow import HUDArrowElement
from hud_win import HUDWinMessage

class SoccerGame:
    """Define game behavior for the soccer gamemode.
    Red team is 0, and blue team is 1.
    """

    blue_team_score = 0
    blue_team_ships = []

    red_team_score = 0
    red_team_ships = []

    win_score = 3

    _ball = None

    announce_win_timer = -1

    self.winner = -1

    def __init__(self):
        self._ball = Ball()
        Map.current_map.objects.add(self._ball)
        self.goal_sound = pygame.mixer.Sound(os.path.join("res", "goal.wav"))

    def get_spawn_pos(self, ship):
        """Return x, y, angle of the spawn position for a ship given their team."""
        if ship.team == 0:
            return Map.current_map.rect.w / 2 - 50, \
                    Map.current_map.rect.h / 3 * (1 + self.blue_team_ships.index(ship)), \
                    270
        elif ship.team == 1:
            return Map.current_map.rect.w / 2 + 50, \
                    Map.current_map.rect.h / 3 * (1 + self.red_team_ships.index(ship)), \
                    90
        else:
            raise Exception("Couldn't determine ship team to spawn ship!")

    def update(self):
        team_scored = self._ball.team_scored
        if team_scored > -1:
            if team_scored == 0:
                self.blue_team_score += 1
            elif team_scored == 1:
                self.red_team_score += 1
            self.goal_sound.play()
            self._ball.respawn()
            if self.blue_team_score == self.win_score:
                self.announce_win(0)
                self.winner = 0
            elif self.red_team_score == self.win_score:
                self.announce_win(1)
                self.winner = 1

        if self.announce_win_timer > 0:
            self.announce_win_timer -= 1
        elif self.announce_win_timer == 0:
            pygame.event.post(pygame.event.Event(events.END_GAME, {
                "called_by": self, "outcome": self.winner}))
            self.announce_win_timer -= 1

    @property
    def objective(self):
        """Return the main objective of the game (the ball)."""
        return self._ball

    def new_hud(self, width, height, camera):
        """Return the HUD elements suggested for the gamemode."""
        elements = pygame.sprite.Group()
        elements.add(HUDScoreElement((round(width * .33), 35), lambda: self.blue_team_score))
        elements.add(HUDScoreElement((round(width * .66), 35), lambda: self.red_team_score))
        
        self.hud_win = HUDWinMessage((width // 2 - 100, height // 2))
        elements.add(self.hud_win)
        #elements.add(HUDArrowElement(camera, lambda: self._ball.rect.center, False))
        return elements

    def respawn_all(self):
        for ship in self.red_team_ships + self.blue_team_ships:
            ship.respawn()
        self._ball.respawn()

    def request_change_team(self, ship, requested):
        """Check for team balance, then assign a team to the ship."""

        if len(self.red_team_ships) - 1 > len(self.blue_team_ships):
            # Too many people in red team. Assign to blue instead.
            requested = 0
        elif len(self.blue_team_ships) - 1 > len(self.red_team_ships):
            # and vice versa.
            requested = 1
        else:
            # If no problems, just fulfill the request.
            pass

        if ship.team == requested or 0 > requested > 1:
            # Ignore if it's already the same team, or if invalid
            return

        self.change_team(ship, requested)
        return requested

    def change_team(self, ship, team):
        try:
            self.blue_team_ships.remove(ship)
            self.red_team_ships.remove(ship)
        except:
            pass

        if ship.team == 0:
            self.blue_team_ships.append(ship)
        elif ship.team == 1:
            self.red_team_ships.append(ship)

    def get_teammates(self, ship):
        """Get the list of a ship's teammates."""
        if ship.team == 0:
            teammates = list(self.blue_team_ships)
        if ship.team == 1:
            teammates = list(self.red_team_ships)
        teammates.remove(ship)
        return teammates

    def get_enemies(self, ship):
        """Get the list of a ship's enemies. Useful for collision checks."""
        if ship.team == 0:
            enemies = list(self.red_team_ships)
        if ship.team == 1:
            enemies = list(self.blue_team_ships)
        return enemies

    def announce_win(self, team):
        """Announce the winning team."""
        self.hud_win.show(team)
        self.announce_win_timer = 360
