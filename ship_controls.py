import pygame
from settings import SHIP_CONTROL_PRESET

"""Various configurations for ship controls.

Preset 0: Player 1 takes WASD or arrow keys. Player 2 takes numpad.
Preset 1: Player 1 takes WASD. Player 2 takes arrow keys.
"""

presets = [
	# Preset 0
	({
		"thrust":   (pygame.K_w, pygame.K_UP),
		"left":     (pygame.K_a, pygame.K_LEFT),
		"right":    (pygame.K_d, pygame.K_RIGHT),
		"grabbing": (pygame.K_SPACE,),
		"respawn":  (pygame.K_r,)
	},
	{
		"thrust":   (pygame.K_KP8,),
		"left":     (pygame.K_KP4,),
		"right":    (pygame.K_KP6,),
		"grabbing": (pygame.K_KP_ENTER,),
		"respawn":  (pygame.K_KP_PLUS,)
	}),
	
	# Preset 1
	({
		"thrust":   (pygame.K_w,),
		"left":     (pygame.K_a,),
		"right":    (pygame.K_d,),
		"grabbing": (pygame.K_SPACE,),
		"respawn":  (pygame.K_r,)
	},
	{
		"thrust":   (pygame.K_UP,),
		"left":     (pygame.K_LEFT,),
		"right":    (pygame.K_RIGHT,),
		"grabbing": (pygame.K_RETURN,),
		"respawn":  (pygame.K_SLASH,)
	})	
]

ship_controls = None

if SHIP_CONTROL_PRESET == 0:
	ship_controls = presets[0]
elif SHIP_CONTROL_PRESET == 1:
	ship_controls = presets[1]
else:
	raise ValueError("Invalid SHIP_CONTROL_PRESET value")