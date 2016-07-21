from pygame.locals import USEREVENT

"""Game constants to tweak portions of the game"""

DISP_WIDTH = 640
DISP_HEIGHT = 480

SHIP_ACCELERATION = 0.15

COLLISION_ALGORITHM_EXPERIMENTAL = 0
COLLISION_ACCURACY = 2
COLLISION_DAMPING = .9

COLLISION_UNSTUCK_EVENT_ID = USEREVENT + 1
COLLISION_UNSTUCK_AGGRESSION = 10

COLLISION_STUCK_THRESHOLD = 35