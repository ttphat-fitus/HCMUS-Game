import pygame
import random
from .game_object import GameObject
from .path_utils import get_resource_path

class Obstacle(GameObject):
    """Base obstacle class"""
    
    def __init__(self, x, y, image_path, scale=1.0):
        super().__init__(x, y)
        if image_path:  # Only load if image path is provided
            self.load_sprite(image_path, scale)
        self.speed_multiplier = 3.0  # Match ground speed
        
    def update(self, delta_time, speed):
        """Move obstacle left based on game speed"""
        self.velocity.x = -speed * self.speed_multiplier  # Apply same multiplier as ground
        super().update(delta_time)

class Stump(Obstacle):
    """Tree stump obstacle"""
    
    def __init__(self, x, y):
        super().__init__(x, y, get_resource_path("assets/img/obstacles/stump.png"), 3.0)  # Original 4x scale

class Rock(Obstacle):
    """Rock obstacle"""
    
    def __init__(self, x, y):
        super().__init__(x, y, get_resource_path("assets/img/obstacles/rock.png"), 3.0)  # Original 4x scale

class Barrel(Obstacle):
    """Barrel obstacle"""
    
    def __init__(self, x, y):
        super().__init__(x, y, get_resource_path("assets/img/obstacles/barrel.png"), 3.0)  # Original 4x scale

class Bird(Obstacle):
    """Flying bird obstacle"""
    
    def __init__(self, x, y):
        # Pass None as image_path since we'll load sprite sheet manually
        super().__init__(x, y, None, 3.0)
        
        # Load bird sprite sheet (288x32 = 9 frames of 32x32) with original 4x scale
        try:
            self.load_sprite_sheet(get_resource_path("assets/img/obstacles/Bird.png"), 32, 32, 9, 3.0)
            self.animation_speed = 10.0  # Match original Godot speed
            self.speed_multiplier = 3.0  # Set speed multiplier here
            print(f"Bird created at position ({x}, {y})")
        except Exception as e:
            print(f"ERROR initializing bird: {e}")
        
    def update(self, delta_time, speed):
        """Birds move at half speed like in original and animate"""
        # Set velocity
        self.velocity.x = -(speed * self.speed_multiplier) / 2  # Apply multiplier but keep half speed for birds
        
        # Update animation first
        self.update_animation(delta_time)
        
        # Update position using the base class update
        super().update(delta_time, speed)  # Need to pass speed to base class

class ObstacleFactory:
    """Factory for creating obstacles"""
    
    # Bird heights from original code
    BIRD_HEIGHTS = [200, 390]
    
    @staticmethod
    def create_ground_obstacle(x, y, obstacle_type=None):
        """Create a random ground obstacle"""
        if obstacle_type is None:
            obstacle_type = random.choice(['stump', 'rock', 'barrel'])
            
        if obstacle_type == 'stump':
            return Stump(x, y)
        elif obstacle_type == 'rock':
            return Rock(x, y)
        elif obstacle_type == 'barrel':
            return Barrel(x, y)
        else:
            return Stump(x, y)  # Default
            
    @staticmethod
    def create_bird(x):
        """Create a bird at random height"""
        # y = random.choice(ObstacleFactory.BIRD_HEIGHTS)
        return Bird(x, 400)

class ObstacleManager:
    """Manages all obstacles in the game"""
    
    def __init__(self, screen_width, ground_y):
        self.obstacles = []
        self.screen_width = screen_width
        self.ground_y = ground_y
        self.last_obstacle_x = 0
        
    def clear(self):
        """Remove all obstacles"""
        self.obstacles.clear()
        self.last_obstacle_x = 0
        
    def update(self, delta_time, speed, score, difficulty, camera_x):
        """Update all obstacles"""
        # Update existing obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update(delta_time, speed)
            
            # Remove obstacles that are off screen
            if obstacle.position.x < camera_x - self.screen_width:
                self.obstacles.remove(obstacle)
                
        # Generate new obstacles
        self._generate_obstacles(score, difficulty, camera_x)
        
    def _generate_obstacles(self, score, difficulty, camera_x):
        """Generate new obstacles based on original logic"""
        if not self.obstacles or self.last_obstacle_x < self.screen_width + score:  # Check if we need more obstacles
            # Generate ground obstacles
            # max_obstacles = difficulty + 3  # More obstacles per group
            num_obstacles = 1  # At least 2 obstacles
            
            group_spacing = random.randint(175, 350)  # Space between groups
            
            # Calculate next obstacle position based on last obstacle
            if self.last_obstacle_x == 0:
                obs_x = self.screen_width + score + (group_spacing * 0.75)
            else:
                obs_x = self.last_obstacle_x + group_spacing

            if random.random() >= 0.5:
                print("Creating ground obstacle at", obs_x)
                obstacle = ObstacleFactory.create_ground_obstacle(obs_x, 0)  # Temp Y position
                if obstacle.rect:
                    # Position obstacle properly on ground
                    obs_y = self.ground_y - obstacle.rect.height // 2
                    obstacle.position.y = obs_y
                    obstacle.rect.centery = obs_y
                    
                self.obstacles.append(obstacle)
                self.last_obstacle_x = obs_x
            else:
                print("Creating bird at", obs_x)
                bird = ObstacleFactory.create_bird(obs_x)
                self.obstacles.append(bird)
                self.last_obstacle_x = obs_x
                    
    def draw(self, screen):
        """Draw all obstacles"""
        for obstacle in self.obstacles:
            obstacle.draw(screen)
            
    def check_collision(self, dino):
        """Check collision with dinosaur"""
        dino_rect = dino.get_collision_rect()
        if not dino_rect:
            return False
            
        for obstacle in self.obstacles:
            if obstacle.rect and dino_rect.colliderect(obstacle.rect):
                return True
        return False
