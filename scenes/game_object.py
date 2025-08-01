import pygame
import math

class GameObject:
    """Base class for all game objects"""
    
    def __init__(self, x=0, y=0):
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.sprite = None
        self.rect = None
        self.visible = True
        
        # Animation support
        self.sprite_sheet = None
        self.current_frame = 0
        self.frame_count = 1
        self.frame_width = 0
        self.frame_height = 0
        self.animation_speed = 10.0  # frames per second
        self.animation_timer = 0.0
        self.scale = 1.0
        
    def load_sprite(self, image_path, scale=1.0):
        """Load and scale a sprite"""
        try:
            self.sprite = pygame.image.load(image_path).convert_alpha()
            self.scale = scale
            if scale != 1.0:
                width = int(self.sprite.get_width() * scale)
                height = int(self.sprite.get_height() * scale)
                self.sprite = pygame.transform.scale(self.sprite, (width, height))
            self.rect = self.sprite.get_rect()
            self.rect.center = (self.position.x, self.position.y)
        except pygame.error as e:
            print(f"Error loading sprite {image_path}: {e}")
            
    def load_sprite_sheet(self, image_path, frame_width, frame_height, frame_count, scale=1.0):
        """Load a sprite sheet for animation"""
        try:
            self.sprite_sheet = pygame.image.load(image_path).convert_alpha()
            self.frame_width = frame_width
            self.frame_height = frame_height
            self.frame_count = frame_count
            self.scale = scale
            self.current_frame = 0
            
            # Extract and scale the first frame as default sprite
            frame_rect = pygame.Rect(0, 0, frame_width, frame_height)
            self.sprite = self.sprite_sheet.subsurface(frame_rect).copy()
            
            if scale != 1.0:
                scaled_width = int(frame_width * scale)
                scaled_height = int(frame_height * scale)
                self.sprite = pygame.transform.scale(self.sprite, (scaled_width, scaled_height))
                
            self.rect = self.sprite.get_rect()
            self.rect.center = (self.position.x, self.position.y)
        except pygame.error as e:
            print(f"Error loading sprite sheet {image_path}: {e}")
            
    def get_frame(self, frame_index):
        """Get a specific frame from the sprite sheet"""
        if not self.sprite_sheet or frame_index >= self.frame_count:
            return self.sprite
            
        frame_x = (frame_index * self.frame_width) % self.sprite_sheet.get_width()
        frame_y = ((frame_index * self.frame_width) // self.sprite_sheet.get_width()) * self.frame_height
        
        frame_rect = pygame.Rect(frame_x, frame_y, self.frame_width, self.frame_height)
        frame = self.sprite_sheet.subsurface(frame_rect).copy()
        
        if self.scale != 1.0:
            scaled_width = int(self.frame_width * self.scale)
            scaled_height = int(self.frame_height * self.scale)
            frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
            
        return frame
        
    def update_animation(self, delta_time):
        """Update animation frame"""
        if self.sprite_sheet and self.frame_count > 1:
            self.animation_timer += delta_time
            if self.animation_timer >= 1.0 / self.animation_speed:
                self.current_frame = (self.current_frame + 1) % self.frame_count
                self.sprite = self.get_frame(self.current_frame)
                self.animation_timer = 0.0
            
    def update(self, delta_time):
        """Update the game object"""
        self.position += self.velocity * delta_time
        if self.rect:
            self.rect.center = (self.position.x, self.position.y)
            
    def draw(self, screen):
        """Draw the game object"""
        if self.visible and self.sprite:
            screen.blit(self.sprite, self.rect)
            
    def get_rect(self):
        """Get the collision rectangle"""
        return self.rect if self.rect else pygame.Rect(self.position.x, self.position.y, 0, 0)
        
    def collides_with(self, other):
        """Check collision with another game object"""
        return self.get_rect().colliderect(other.get_rect())
