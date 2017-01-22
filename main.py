import pygame, os

from entity import Entity
from ship import Ship
from player_ship import PlayerShip
from map import Map
from soccer import SoccerGame
from display import Display
from scanlines import Scanlines
from startscreen import StartScreen
import events

from settings import DISP_WIDTH, DISP_HEIGHT, LOCAL_MP

window = None
game_disp = None
game_disp2 = None
clock = None

stop = False

# Game states
MENU = 0
GAME = 1

def init():
    """Initialize pygame and all objects/variables needed to begin the game."""
    global game_disp, game_disp2, clock, gamemode, window, window_unscaled, scanlines, state, startscreen
    
    pygame.init()
    clock = pygame.time.Clock()
    
    # Main surface is here in case there are multiple smaller surfaces for splitscreen
    #window_size = (DISP_WIDTH*2, DISP_HEIGHT*2)
    window_size = (0,0)
    window = pygame.display.set_mode(window_size, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
    window_unscaled = pygame.surface.Surface((DISP_WIDTH, DISP_HEIGHT))

    # Create post-processing filter
    scanlines = Scanlines(window.get_size())
    
    # Set window icon
    pygame.display.set_icon(pygame.image.load(os.path.join("res", "icon.png")).convert_alpha())
    
    # Make screen 1 half-sized instead of full-sized if splitscreen is on
    if LOCAL_MP:
        game_disp = Display((DISP_WIDTH // 2, DISP_HEIGHT))
    else:
        game_disp = Display((DISP_WIDTH, DISP_HEIGHT))
    
    # Set window title
    pygame.display.set_caption("Soccer in space!")
    
    # Create main menu
    startscreen = StartScreen(window_unscaled.get_size())
    state = MENU

    # Create the map
    map_path = os.path.join("res", "le_football.png")
    Map.current_map = Map(map_path)
    
    # Start the gamemode
    gamemode = SoccerGame()
    game_disp.load_game(gamemode)
    
    # Create the ship
    ship = PlayerShip(0, gamemode)
    Map.objects.add(ship)
    game_disp.ent_in_control = ship
    
    # Create player 2 ship and display if splitscreen is on
    if LOCAL_MP:
        game_disp2 = Display((DISP_WIDTH // 2, DISP_HEIGHT))
        game_disp2.load_game(gamemode)

        ship2 = PlayerShip(1, gamemode)
        Map.objects.add(ship2)
        game_disp2.ent_in_control = ship2
    
    pygame.time.set_timer(events.COLLISION_UNSTUCK, 1000)
    
    print("Finished initializing.")
    
    loop()
    
def pollEvents():
    """Process all (key) events passed to pygame."""
    for event in pygame.event.get():
        global stop, state
        if event.type == pygame.QUIT:
            stop = True
        elif event.type == events.QUIT:
            stop = True
        elif event.type == events.COLLISION_UNSTUCK:
            Entity.unstuck_all(Map.objects)
        elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
            if event.key == pygame.K_ESCAPE:
                stop = True
            if state == MENU:
                startscreen.handle_inputs(event)
            elif state == GAME:
                game_disp.ent_in_control.handle_inputs(event, 0)
                if LOCAL_MP:
                    game_disp2.ent_in_control.handle_inputs(event, 1)
        elif event.type == events.START_GAME:
            if state == GAME:
                raise Exception("Game is already in main game state!")
            state = GAME
    
def loop():
    """Primary game loop."""
    genTimer = 100
    while not stop:     
        pollEvents();
        
        delta = clock.tick(60)

        # Simple FPS clock
        genTimer -= 1 
        if genTimer == 0:
            print("[fps]", clock.get_fps())
            genTimer = 100
        
        if state == MENU:
            menu_state_loop(delta)
        elif state == GAME:
            game_state_loop(delta)
        else:
            raise Exception("Unknown game state!")

        # Upscale the game to fit the window
        pygame.transform.scale(window_unscaled, window.get_size(), window)
        scanlines.apply(window)

        pygame.display.flip()
    quit()

def game_state_loop(delta):
    """Game loop specifically during main game state"""
    Map.current_map.action(delta)
    gamemode.update()
    
    game_disp.update()
    game_disp.render()
    
    window_unscaled.blit(game_disp.surface, (0,0))
    
    if LOCAL_MP:
        game_disp2.update()
        game_disp2.render()
        window_unscaled.blit(game_disp2.surface, (DISP_WIDTH // 2 - 1, 0))
        
        # Draw separating line
        pygame.draw.line(window_unscaled, (0,0,0), (DISP_WIDTH // 2 - 1, 0), (DISP_WIDTH // 2 - 1, DISP_HEIGHT - 1), 3)

def menu_state_loop(delta):
    """Game loop specifically during the start screen/main menu"""
    window_unscaled.blit(startscreen, (0,0))

def quit():
    print("Exiting.")
    pygame.quit()

if __name__ == "__main__": # Make sure the game is not being run twice!
    init()
