import pygame, os, math

import collision
from entity import Entity
from map import Map

from settings import SHIP_ACCELERATION, SHIP_BRAKING, DEBUG

class Ship(Entity):
    mass = 300
    
    path_collide_mask = os.path.join("res", "ship-collision.png")

    default_acceleration = SHIP_ACCELERATION
    acceleration = SHIP_ACCELERATION

    collision_sound_cooldown = 30

    def __init__(self, team, gamemode):
        self.team = team
        self.gamemode = gamemode
        gamemode.change_team(self, team)
        
        if self.team == 0:
            # blue team faces right
            self.x = Map.current_map.rect.w * 0.4
            self.y = Map.current_map.rect.h / 2
            self.rot = 270
            path = os.path.join("res", "ship-sprite-blue.png")
            path_firing = os.path.join("res", "ship-sprite-blue-firing.png")
        elif self.team == 1:
            # red team faces left
            self.x = Map.current_map.rect.w * 0.6
            self.y = Map.current_map.rect.h / 2
            self.rot = 90
            path = os.path.join("res", "ship-sprite-red.png")
            path_firing = os.path.join("res", "ship-sprite-red-firing.png")
        else:
            assert(False)
            
        print("Loading", path_firing)
        self.firing_sprite = pygame.image.load(path_firing).convert_alpha()
        
        super(Ship, self).__init__(path)
        
        self.mask = pygame.mask.from_surface(pygame.image.load(self.path_collide_mask).convert_alpha())
        
        self.thrust = False
        self.left = False
        self.right = False
        self.grabbing = False
        self.braking = False
        
        self.invuln_timer = 0
        self.invuln_blink = False
        self.invuln_blink_timer = 0

        self.gamemode = gamemode
        self.team = team
        
        self.collide_sound = pygame.mixer.Sound(os.path.join("res", "ship_bump.wav"))
        self.collide_with_ship_sound = pygame.mixer.Sound(os.path.join("res", "ship_ship_collision.wav"))
        self.collision_last_frame = False
    
    def action(self, delta):
        self.move(delta)

        collision = False
        if self.collision_detect():
            collision = True
            if not self.collision_last_frame:
                self.collide_sound.play()
            self.collision_last_frame = True
        if self.collision_detect_others():
            collision = True
            if not self.collision_last_frame:
                self.collide_with_ship_sound.play()
            self.collision_last_frame = True
        if not collision:
            self.collision_last_frame = False

        if self.thrust:
            self.vx += -self.acceleration*math.sin(math.radians(self.rot))
            self.vy += -self.acceleration*math.cos(math.radians(self.rot))
            if self.current_sprite != self.firing_sprite:
                self.set_sprite(self.firing_sprite)
        else:
            if self.current_sprite != self.main_sprite:
                self.set_sprite(self.main_sprite)

        if self.left:
            self.vrot = self.vrot / 2 + 2
        if self.right:
            self.vrot = self.vrot / 2 - 2
        if not (self.left ^ self.right):
            self.vrot = self.vrot / 4
        if self.grabbing:
            pass
        if self.braking:
            self.vx *= SHIP_BRAKING
            self.vy *= SHIP_BRAKING
        
        if self.x < 0 or self.x > Map.current_map.rect.w:
            self.vx *= -1
        if self.y < 0 or self.y > Map.current_map.rect.h:
            self.vy *= -1

        if self.collision_ignore:
            self.invuln_timer -= 1
            self.invuln_blink_timer -= 1
            if self.invuln_blink_timer == 0:
                if self.invuln_blink:
                    self.set_alpha(30)
                else:
                    self.set_alpha(255)
                self.invuln_blink = not self.invuln_blink
                self.invuln_blink_timer = self.invuln_timer // 30
            if self.invuln_timer <= 0:
                self.set_alpha(255)
                self.make_invulnerable(False)
        if DEBUG: pygame.gfxdraw.box(self.image, self.rect, (35, 45, 220))


    def respawn(self):
        super(Ship, self).respawn()
        self.x, self.y, self.rot = self.gamemode.get_spawn_pos(self)
        self.make_invulnerable(True)

    def make_invulnerable(self, invuln):
        """Make the ship invulnerable"""
        self.collision_ignore = invuln
        if invuln:
            self.invuln_timer = 180
            self.invuln_blink_timer = 4
        else:
            self.invuln_timer = 0
            self.invuln_blink_timer = 0
            self.invuln_blink = False
 
    def collision_detect_others(self):
        if self.collision_ignore: 
            return

        teammates = self.gamemode.get_enemies(self)
        other_objects = [self.gamemode.objective]  # It's a list, just for future-proofing
        
        objects = teammates + other_objects
        
        hit = False
        for obj in objects:
            point = pygame.sprite.collide_mask(obj, self)
            if point:
                # BONK!
                collision.elastic_collision(obj, self, point)
                hit = True
        return hit
        
