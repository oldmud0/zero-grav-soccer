import pygame

import collision
from map import Map

from settings import COLLISION_DAMPING, COLLISION_ALGORITHM_EXPERIMENTAL, COLLISION_STUCK_THRESHOLD, COLLISION_UNSTUCK_AGGRESSION

class Entity(pygame.sprite.Sprite):
    mass = 100
    
    collision_counter = 0
    collision_threshold = COLLISION_STUCK_THRESHOLD
    collision_ignore = False

    x = 0
    y = 0
    rot = 0
    
    vx = 0
    vy = 0
    vrot = 0

    alpha = 255

    def __init__(self, path):
        pygame.sprite.Sprite.__init__(self)
        
        print("Loading", path) # Debugging purposes only
        self.image = pygame.image.load(path).convert_alpha()
        self.current_sprite = self.main_sprite = self.image
        self.current_sprite_alpha = self.current_sprite.copy()

        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        
    def respawn(self):
        self.x = 0
        self.y = 0
        self.rot = 0
        
        self.vx = 0
        self.vy = 0
        self.vrot = 0
        
        self.collision_counter = 0
    
    def rot_center(self):
        """Rotate the entity's sprite while preserving the center.
        This is done by taking the original sprite's center, rotating the sprite,
        and then giving the rotated sprite the old center.
        """
        loc = self.rect.center
        self.image = pygame.transform.rotate(self.current_sprite_alpha, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = loc
    
    def set_alpha(self, alpha):
        """Set the effective alpha of an entity.
        We need to override the pygame's own set_alpha
        method because it does not work on sprites with
        a per-pixel alpha.
        """
        if alpha < 0 or alpha > 255:
            raise ValueError("alpha must be betweeen 0 and 255")

        self.alpha = alpha
        self.draw_alpha()

    def draw_alpha(self):
        """Apply the current effective alpha to the sprite."""
        if self.alpha == 255:
            self.current_sprite_alpha = self.current_sprite
        else:
            mask = pygame.Surface(self.current_sprite.get_size(), flags=pygame.SRCALPHA)
            mask.fill((255, 255, 255, self.alpha))
            self.current_sprite_alpha = self.current_sprite.copy()
            self.current_sprite_alpha.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def set_sprite(self, image):
        """Set a new image as the current sprite."""
        self.current_sprite = image
        self.draw_alpha()

    def action(self, delta):
        self.move()
        self.collision_detect()
    
    def move(self, delta):
        """Move a sprite using time-based movement."""
        ideal_frame_time = 60 # FPS
        displacement_factor = delta / ideal_frame_time
                
        self.x += self.vx * displacement_factor
        self.y += self.vy * displacement_factor
        
        # If we do not round our floats, pygame will floor it for us (bad)
        self.rect.center = (round(self.x), round(self.y))
        
        self.rot = (self.rot + self.vrot) % 360
        self.rot_center()
    
    def collision_detect(self):
        """Check for collisions against other entities or the map.
        Collision detection is very tricky.
        """
        # Check if the collision was with a map
        self.mask = pygame.mask.from_surface(self.image)
        point = pygame.sprite.collide_mask(Map.current_map, self)
        if point:
            if COLLISION_ALGORITHM_EXPERIMENTAL:
                self.vx, self.vy = collision.calculate_reflection_angle(Map.current_map.mask, point, (self.vx, self.vy))
            else: 
                self.vx, self.vy = collision.simple_collision(Map.current_map.mask, point, (self.vx, self.vy))
            self.vx, self.vy = self.vx * COLLISION_DAMPING, self.vy * COLLISION_DAMPING
            
            self.collision_counter += 1
            return True
        return False
    
    def unstuck_all(objects):
        """Fix all entities that appears to be stuck.
        If their collision counter is above a certain threshold, they're probably stuck.
        """
        for obj in objects:
            if obj.collision_counter > obj.collision_threshold:
                print("Object at", (round(obj.x), round(obj.y)), "is stuck. Trying to unstuck...")
                obj.unstuck()
            obj.collision_counter = 0
    
    def unstuck(self):
        """Unstuck an entity by checking for any open spots we could put it on."""
        mask = Map.current_map.mask
        
        x_max, y_max = mask.get_size()
        orig_x, orig_y = round(self.x), round(self.y)
        x, y = orig_x , orig_y
        unstuck_aggr = COLLISION_UNSTUCK_AGGRESSION
        
        # Vertical check for any open spots we could put the entity on...
        while y > 0:
            if not mask.get_at((x, y)):
                self.y = y
                self.vy = -unstuck_aggr
                return
            y -= unstuck_aggr
        y = orig_y
        while y < y_max:
            if not mask.get_at((x, y)):
                self.y = y
                self.vy = unstuck_aggr
                return
            y += unstuck_aggr
        y = orig_y
        
        # Horizontal spots?
        while x > 0:
            if not mask.get_at((x, y)):
                self.x = x
                self.vx = -unstuck_aggr
                return
            x -= unstuck_aggr
        x = orig_x
        while x < x_max:
            if not mask.get_at((x, y)):
                self.x = x
                self.vx = unstuck_aggr
                return
            x += unstuck_aggr
        x = orig_x
        
        # Diagonal spots
        while x > 0 and y > 0:
            if not mask.get_at((x, y)):
                self.x, self.y = x, y
                self.vx, self.vy = -unstuck_aggr, -unstuck_aggr
                return
            x, y = x - unstuck_aggr, y - unstuck_aggr
        x, y = orig_x, orig_y
        while x < x_max and y < y_max:
            if not mask.get_at((x, y)):
                self.x, self.y = x, y
                self.vx, self.vy = unstuck_aggr, unstuck_aggr
                return
            x, y = x + unstuck_aggr, y + unstuck_aggr
        x, y = orig_x, orig_y
        while x > 0 and y < y_max:
            if not mask.get_at((x, y)):
                self.x, self.y = x, y
                return
            x, y = x - unstuck_aggr, y + unstuck_aggr
        x, y = orig_x, orig_y
        while x < x_max and y > 0:
            if not mask.get_at((x, y)):
                self.x, self.y = x, y
                return
            x, y = x + unstuck_aggr, y - unstuck_aggr
        x, y = orig_x, orig_y
        
        # All right, I officially give up now.
        print("Couldn't unstuck object!")
    
