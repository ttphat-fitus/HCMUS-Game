import pygame
import random
from .game_object import GameObject

class Dino(GameObject):
    """Player character - the dinosaur"""
    
    # Constants from original Godot code
    GRAVITY = 4500
    JUMP_SPEED = -1500  # Increased from -1800 for 2x farther jump distance
    
    def __init__(self, x, y):
        super().__init__(x, y)
        
        # Sprite sheet management
        self.current_sprite_sheet = "base"
        self.sprite_sheets = {
            "base": "assets/img/mort-base.png",
            "slow": "assets/img/mort-slow.png", 
            "fast": "assets/img/mort-fast.png"
        }
        
        # Load sprite sheet (576x24 = 24 frames of 24x24) with original 8x scale
        self.load_sprite_sheet("assets/img/mort-base.png", 24, 24, 24, 8.0)  # Original scale
        
        # Animation states and frame ranges (matching original Godot mapping)
        self.state = "idle"  # idle, run, jump, duck
        self.on_ground = True
        
        # Frame ranges for different animations (based on original Godot scene)
        self.animation_frames = {
            "idle": [0, 1, 2, 3],      # Frames 0-3 for idle
            "run": [4, 5, 6, 7, 8, 9], # Frames 4-9 for running  
            "jump": [11],              # Frame 11 for jumping
            "duck": [18, 19, 20, 21, 22, 23]  # Frames 18-23 for ducking
        }
        
        # Animation settings (matching original)
        self.animation_speed = 10.0  # Frames per second (original value)
        self.state_frame_index = 0
        self.animation_timer = 0.0
        
        # Collision rectangles for different states
        self.run_rect = None
        self.duck_rect = None
        
        # Jump sound
        self.jump_sound = None
        try:
            self.jump_sound = pygame.mixer.Sound("assets/sound/jump.wav")
            self.jump_sound.set_volume(0.5)
        except pygame.error:
            pass
            
        # Set up collision rectangles (matching original Godot collision shapes)
        if self.rect:
            # Original: RunCol shape = 10x16 at scale 8 = 80x128
            self.run_rect = pygame.Rect(0, 0, 80, 128)
            # Original: DuckCol shape = 10x14 at scale 8 = 80x112  
            self.duck_rect = pygame.Rect(0, 0, 80, 112)
    
    def change_sprite_sheet(self, sheet_type):
        """Change the sprite sheet based on type (base, slow, fast)"""
        if sheet_type in self.sprite_sheets and sheet_type != self.current_sprite_sheet:
            self.current_sprite_sheet = sheet_type
            # Reload sprite sheet with the new image
            self.load_sprite_sheet(self.sprite_sheets[sheet_type], 24, 24, 24, 8.0)
            # Reset animation to avoid flickering
            self.state_frame_index = 0
            self.animation_timer = 0.0
            print(f"Dino sprite changed to: {sheet_type}")
        
    def update(self, delta_time, game_running, ground_y, active_powerups=None, score=0):
        """Update dinosaur physics and animation"""
        # Check sprite sheet conditions
        if active_powerups and "halfspeed" in active_powerups:
            self.change_sprite_sheet("slow")
        elif score > 4000:
            self.change_sprite_sheet("fast")
        else:
            self.change_sprite_sheet("base")
            
        # Apply gravity
        self.velocity.y += self.GRAVITY * delta_time
        
        # Check if on ground
        ground_surface = ground_y - self.rect.height // 2
        if self.position.y >= ground_surface:
            self.position.y = ground_surface
            self.velocity.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
        # Handle input and set state
        keys = pygame.key.get_pressed()
        
        old_state = self.state
        
        if self.on_ground:
            if not game_running:
                self.state = "idle"
            else:
                if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                    self.velocity.y = self.JUMP_SPEED
                    self.state = "jump"
                    if self.jump_sound:
                        self.jump_sound.play()
                elif keys[pygame.K_DOWN]:
                    self.state = "duck"
                else:
                    self.state = "run"
        else:
            self.state = "jump"
            
        # Reset animation when state changes
        if old_state != self.state:
            self.state_frame_index = 0
            self.animation_timer = 0.0
            
        # Update animation
        self.update_state_animation(delta_time)
        
        # Update position
        super().update(delta_time)
        
    def update_state_animation(self, delta_time):
        """Update animation based on current state"""
        if self.state in self.animation_frames:
            frames = self.animation_frames[self.state]
            
            if len(frames) > 1:  # Only animate if multiple frames
                self.animation_timer += delta_time
                if self.animation_timer >= 1.0 / self.animation_speed:
                    self.state_frame_index = (self.state_frame_index + 1) % len(frames)
                    self.animation_timer = 0.0
                    
            # Get current frame for this state
            current_frame = frames[self.state_frame_index % len(frames)]
            self.sprite = self.get_frame(current_frame)
        
    def get_collision_rect(self):
        """Get the appropriate collision rectangle based on state"""
        if self.state == "duck" and self.duck_rect:
            rect = self.duck_rect.copy()
            # Position duck collision (original had position offset of -1, 1 at scale 8)
            rect.centerx = self.position.x - 8  # -1 * 8 scale
            rect.centery = self.position.y + 8   # +1 * 8 scale
            return rect
        elif self.run_rect:
            rect = self.run_rect.copy()
            # Position run collision (original had position offset of -1, 0 at scale 8)
            rect.centerx = self.position.x - 8  # -1 * 8 scale
            rect.centery = self.position.y       # 0 offset
            return rect
        return self.rect
        
    def draw(self, screen):
        """Draw the dinosaur with proper animation"""
        if self.visible and self.sprite:
            # Update rect position to match current position
            self.rect.center = (self.position.x, self.position.y)
            screen.blit(self.sprite, self.rect)
            
            # Debug: Draw collision rectangles (remove in final version)
            # collision_rect = self.get_collision_rect()
            # if collision_rect:
            #     pygame.draw.rect(screen, (255, 0, 0), collision_rect, 2)
