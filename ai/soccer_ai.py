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
    
    def __init__(self):
        pass
        
    def think(self):
        pass