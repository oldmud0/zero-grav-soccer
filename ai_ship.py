import pygame
from ship import Ship
from ai.soccer_ai import SoccerAI

class AIShip(Ship):
    """An AI-controlled version of the Ship.
    See the ai/ folder for details on implementation.
    """

    think_interval = 4

    def __init__(self, team, gamemode):
        super(AIShip, self).__init__(team, gamemode)
        self.ai = SoccerAI(self, gamemode)
        self.think_timer = self.think_interval

    def action(self, delta):
        super(AIShip, self).action(delta)
        self.think_timer -= 1
        if self.think_timer == 0:
            self.ai.think()
            self.think_timer = self.think_interval
