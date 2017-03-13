import math

from settings import DEBUG

class SoccerAI:
    """The embodiment of a simple soccer AI.
    The bot has a difficulty slider and can do
    short-term predictions on the ball's path.
    It is objective-based and will go for the ball,
    catch it, and then shoot it at the goal.
    
    Despite what you think, no, this AI does not
    read the human controller ;)
    """
    
    """Valid difficulty levels:
    1 - very easy
        Just go for the ball, do not try to
        predict the path as it bounces across
        walls
    2 - easy
        Predict path on bounce, but the ball
        and the goal are separate objectives.
        Thus, the bot will not be very accurate
        in getting the ball to the goal.
    3 - normal
        Predict path on bounce and do all tricks.
        Bot will grab the ball and brake when needed.
    4 - hard
        Ships in the other team are also objectives.
        Bot will try to hit and block these ships
        if they are a greater risk than the ball itself.
    """
    
    difficulty = 1
    
    def __init__(self, ship, gamemode):
        self.ship = ship
        self.gamemode = gamemode

    def think(self):
        """Process stimulus and determine the correct
        inputs during this interval."""

        objective = self.gamemode.objective
        obj_x, obj_y = objective.x, objective.y
        pos_x, pos_y = self.ship.x, self.ship.y

        # Get ship to point toward ball within margin of error
        ang_err = .2
        ball_angle = (math.degrees((math.atan2(-(obj_y - pos_y), obj_x - pos_x)) % (2 * math.pi))) % 360
        diff = ((ball_angle - self.ship.rot) + 90) % 360 - 180
        #print("[ship ang]", self.ship.rot)
        #print("[ball ang]", ball_angle)
        #print("[diff]", diff)
        self.ship.vrot = self.ship.vrot / 2 + diff / 6

        accel = self.ship.default_acceleration * math.sqrt( (obj_x - pos_x) ** 2 + (obj_y - pos_y) ** 2 )
        if accel > 1:
            self.ship.thrust = True
            self.ship.acceleration = min(self.ship.default_acceleration, accel)
        else:
            self.ship.thrust = False
