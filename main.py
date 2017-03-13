import pygame, os, events

from entity import Entity
from ship import Ship
from player_ship import PlayerShip
from map import Map
from soccer import SoccerGame
from display import Display
from scanlines import Scanlines
from startscreen import StartScreen
from sp_tourney import SinglePlayerTourney
from hud_global import GlobalHUD
import events

from settings import DISP_WIDTH, DISP_HEIGHT, DEBUG, WINDOWED

# Game states
MENU = 0
GAME = 1
SINGLEPLAYER = 2

class ZeroGravitySoccer():

    stop = False
    sp_manager = None

    def __init__(self):
        """Initialize pygame and all objects/variables needed to begin the game."""
        pygame.init()
        self.clock = pygame.time.Clock()

        # small hack: if windowed is not comfortable at max res,
        # then override option and go straight to full-screen mode
        res_x, res_y = pygame.display.list_modes()[0]
        if res_x < DISP_WIDTH*1.6 or res_y < DISP_HEIGHT*1.6:
            print("Windowed mode would barely fit in this monitor. Forcing full screen.")
            global WINDOWED
            WINDOWED = False

        # Main surface is here in case there are multiple smaller surfaces for splitscreen
        if WINDOWED:
            window_size = (DISP_WIDTH*2, DISP_HEIGHT*2)
            self.window = pygame.display.set_mode(window_size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        else:
            window_size = (0,0)
            self.window = pygame.display.set_mode(window_size, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.window_unscaled = pygame.surface.Surface((DISP_WIDTH, DISP_HEIGHT))

        # Create post-processing filter
        self.scanlines = Scanlines(self.window.get_size())

        # Set window icon
        pygame.display.set_icon(pygame.image.load(os.path.join("res", "icon.png")).convert_alpha())


        # Set window title
        pygame.display.set_caption("Zero-Gravity Soccer")

        # Create main menu
        self.startscreen = StartScreen(self.window_unscaled.get_size())
        self.state = MENU

        print("Finished initializing.")

        self.loop()

    def pollEvents(self):
        """Process all (key) events passed to pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                       # Quit
                self.stop = True
            elif event.type == events.QUIT:                     # Quit
                self.stop = True

            elif event.type == events.COLLISION_UNSTUCK:        # Unstuck
                Entity.unstuck_all(Map.current_map.objects)

            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):  # Keypresses
                if event.key == pygame.K_ESCAPE:                # Quit
                    self.stop = True
                if self.state == MENU:                          # Menu inputs
                    self.startscreen.handle_inputs(event)
                elif self.state == SINGLEPLAYER:
                    self.sp_manager.handle_inputs(event)        # Singleplayer manager inputs
                elif self.state == GAME:                        # In-game inputs
                    self.game_disp.ent_in_control.handle_inputs(event, 0)
                    if self.splitscreen:                        # Player 2 as well
                        self.game_disp2.ent_in_control.handle_inputs(event, 1)
                    # Sinful debugging tactics
                    if DEBUG:
                        if event.key == pygame.K_MINUS:
                            pygame.event.post(pygame.event.Event(events.END_GAME, {
                                "called_by": "debug", "outcome": 0}))
                        elif event.key == pygame.K_EQUALS:
                            pygame.event.post(pygame.event.Event(events.END_GAME, {
                                "called_by": "debug", "outcome": 1}))
            
            elif event.type == events.START_GAME:               # Start a game
                if self.state == GAME:
                    raise Exception("Game is already in main game state!")
                if event.mode == "sp_tourney":
                    self.sp_manager = SinglePlayerTourney(self.window_unscaled.get_size())
                    self.state = SINGLEPLAYER
                elif event.mode == "vs_ai":
                    self.start_game(event.map, vs_ai = True)
                    self.state = GAME
                elif event.mode == "vs_local":
                    self.start_game(event.map)
                    self.state = GAME
                else:
                    self.start_game(event.map)
                    self.state = GAME

            elif event.type == events.END_GAME:                 # End a game
                if self.state != GAME:
                    raise Exception("Can't end game, because we aren't in the game state!")
                self.end_game()
                # Check if we're supposed to go to singleplayer
                if self.sp_manager is not None:
                    self.sp_manager.handover(event.outcome)
                    self.state = SINGLEPLAYER
                else:
                   self.to_menu()

            elif event.type == events.TO_MENU:                  # Go to menu
                if self.state == MENU:
                    raise Exception("Game is already in main menu state!")
                self.to_menu()

    def to_menu(self):
        try:
            del self.sp_manager
        except AttributeError:
            pass

        self.startscreen.reset()
        self.state = MENU

    def start_game(self, map, vs_ai = False):
        self.splitscreen = not vs_ai
        # Create the map
        map_path = os.path.join("res", map)
        curr_map = Map.current_map = Map(map_path)

        # Start the gamemode
        self.gamemode = SoccerGame()

        # Make screen 1 half-sized instead of full-sized if splitscreen is on
        if self.splitscreen:
            self.game_disp = Display((DISP_WIDTH // 2, DISP_HEIGHT))
        else:
            self.game_disp = Display((DISP_WIDTH, DISP_HEIGHT))

        self.game_disp.load_game(self.gamemode)

        # Create the ship
        ship = PlayerShip(0, self.gamemode)
        curr_map.objects.add(ship)
        self.game_disp.ent_in_control = ship

        # Create player 2 ship and display if splitscreen is on
        if self.splitscreen:
            self.game_disp2 = Display((DISP_WIDTH // 2, DISP_HEIGHT))
            self.game_disp2.load_game(self.gamemode)

            ship2 = PlayerShip(1, self.gamemode)
            curr_map.objects.add(ship2)
            self.game_disp2.ent_in_control = ship2

        # Create global HUD
        self.global_hud = GlobalHUD(self.window_unscaled.get_size(), self.gamemode)

        pygame.time.set_timer(events.COLLISION_UNSTUCK, 1000)

    def end_game(self):
        """Gracefully end the game."""
        # Turn off the auto-unstuck
        pygame.time.set_timer(events.COLLISION_UNSTUCK, 0)

        # Dereference all the game variables so they can be GC'd
        # (free memory!)
        del self.gamemode
        del Map.current_map

    def loop(self):
        """Primary game loop."""
        genTimer = 100
        while not self.stop:
            self.pollEvents();

            delta = self.clock.tick(60)

            # Simple FPS clock
            genTimer -= 1
            if genTimer == 0:
                if DEBUG: print("[fps]", self.clock.get_fps())
                genTimer = 100

            if self.state == MENU:
                self.menu_state_loop(delta)
            elif self.state == GAME:
                self.game_state_loop(delta)
            elif self.state == SINGLEPLAYER:
                self.sp_state_loop(delta)
            else:
                raise Exception("Unknown game state!")

            # Upscale the game to fit the window
            pygame.transform.scale(self.window_unscaled, self.window.get_size(), self.window)
            self.scanlines.apply(self.window)

            pygame.display.flip()
        self.quit()

    def game_state_loop(self, delta):
        """Game loop specifically during main game state"""
        Map.current_map.action(delta)
        self.gamemode.update()

        self.game_disp.update()
        self.game_disp.render()

        self.window_unscaled.blit(self.game_disp.surface, (0,0))

        if self.splitscreen:
            self.game_disp2.update()
            self.game_disp2.render()
            self.window_unscaled.blit(self.game_disp2.surface, (DISP_WIDTH // 2 - 1, 0))

            # Draw separating line
            pygame.draw.line(self.window_unscaled, (0,0,0), (DISP_WIDTH // 2 - 1, 0), (DISP_WIDTH // 2 - 1, DISP_HEIGHT - 1), 3)

        self.global_hud.update()
        self.global_hud.render()
        self.window_unscaled.blit(self.global_hud, (0,0))

    def sp_state_loop(self, delta):
        """Game loop specifically during the (cinematic) scenes handled by the
        singleplayer manager (tourney mode, etc.)
        """
        scene = self.sp_manager.update()
        self.window_unscaled.blit(scene, (0,0))

    def menu_state_loop(self, delta):
        """Game loop specifically during the start screen/main menu"""
        self.startscreen.update()
        self.window_unscaled.blit(self.startscreen, (0,0))

    def quit(self):
        print("Exiting.")
        pygame.quit()

if __name__ == "__main__": # Make sure the game is not being run twice!
    game = ZeroGravitySoccer()
