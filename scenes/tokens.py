import pygame
import random
import math
from .game_object import GameObject
from .path_utils import get_resource_path

class Token(GameObject):
    """Collectible token class"""
    
    def __init__(self, x, y, token_type="coin", scale=1):  # Much smaller scale for large sprites
        super().__init__(x, y)
        self.token_type = token_type
        
        # Set value and effect based on token type
        if token_type == "coin":
            self.value = 1
            self.effect = None
        elif token_type == "halfspeed":
            self.value = 0  # No coin value
            self.effect = "halfspeed"
            self.effect_duration = 10.0  # 10 seconds
        elif token_type == "doublegold":
            self.value = 0  # No coin value
            self.effect = "doublegold"
            self.effect_duration = 10.0  # 10 seconds
        elif token_type == "godmode":
            self.value = 0  # No coin value
            self.effect = "godmode"
            self.effect_duration = 8.0  # 8 seconds
            
        self.speed_multiplier = 3.0  # Match ground speed like obstacles
        self.collected = False
        
        # Animation properties for visual appeal
        self.bob_speed = 3.0  # Speed of up/down movement
        self.bob_amplitude = 5  # Amplitude of bobbing motion
        self.bob_offset = random.uniform(0, 2 * math.pi)  # Random start phase
        self.initial_y = y
        
        # Load token sprite based on type
        self.load_token_sprite(token_type, scale)
        
    def load_token_sprite(self, token_type, scale):
        """Load the appropriate sprite for the token type"""
        sprite_paths = {
            "coin": get_resource_path("assets/img/rewards/coin.png"),
            "halfspeed": get_resource_path("assets/img/rewards/halfspeed.png"),
            "doublegold": get_resource_path("assets/img/rewards/doublegold.png"),
            "godmode": get_resource_path("assets/img/rewards/godmode.png")
        }
        
        sprite_path = sprite_paths.get(token_type, sprite_paths["coin"])
        
        try:
            self.load_sprite(sprite_path, scale)
            print(f"{token_type.capitalize()} loaded successfully at position ({self.position.x}, {self.position.y}), scale: {scale}")
        except Exception as e:
            # Create a simple colored rectangle as fallback
            self.create_fallback_sprite(scale)
            
    def create_fallback_sprite(self, scale):
        """Create a simple colored shape if sprite loading fails"""
        size = int(24 * scale)  # Base size scaled
        print(f"Creating fallback {self.token_type} sprite with size: {size}x{size}")
        
        # Different colors for different token types
        colors = {
            "coin": (255, 215, 0),      # Gold
            "halfspeed": (128, 0, 128), # Purple
            "doublegold": (255, 165, 0), # Orange
            "godmode": (0, 255, 0)      # Green
        }
        
        color = colors.get(self.token_type, colors["coin"])
        
        # Create different shapes for different powerups
        self.sprite = pygame.Surface((size, size), pygame.SRCALPHA)
        
        if self.token_type == "coin":
            # Circle for coin
            pygame.draw.circle(self.sprite, color, (size // 2, size // 2), size // 2)
            pygame.draw.circle(self.sprite, (255, 255, 255), (size // 2, size // 2), size // 2, 2)
        elif self.token_type == "halfspeed":
            # Diamond for halfspeed
            points = [(size // 2, 2), (size - 2, size // 2), (size // 2, size - 2), (2, size // 2)]
            pygame.draw.polygon(self.sprite, color, points)
            pygame.draw.polygon(self.sprite, (255, 255, 255), points, 2)
        elif self.token_type == "doublegold":
            # Star-like shape for doublegold
            pygame.draw.rect(self.sprite, color, (size // 4, size // 4, size // 2, size // 2))
            pygame.draw.rect(self.sprite, (255, 255, 255), (size // 4, size // 4, size // 2, size // 2), 2)
        elif self.token_type == "godmode":
            # Shield-like shape for godmode (cross/plus pattern)
            center = size // 2
            thickness = size // 6
            # Vertical bar
            pygame.draw.rect(self.sprite, color, (center - thickness//2, thickness, thickness, size - 2*thickness))
            # Horizontal bar
            pygame.draw.rect(self.sprite, color, (thickness, center - thickness//2, size - 2*thickness, thickness))
            # Border
            pygame.draw.rect(self.sprite, (200, 200, 200), (center - thickness//2, thickness, thickness, size - 2*thickness), 2)
            pygame.draw.rect(self.sprite, (200, 200, 200), (thickness, center - thickness//2, size - 2*thickness, thickness), 2)
        
        self.rect = self.sprite.get_rect()
        self.rect.center = (self.position.x, self.position.y)
        print(f"Fallback {self.token_type} rect: {self.rect}")
        
    def update(self, delta_time, speed):
        """Update token position and animation"""
        if self.collected:
            return
            
        # Move left with game speed
        self.velocity.x = -speed * self.speed_multiplier
        
        # Add bobbing animation
        self.bob_offset += self.bob_speed * delta_time
        bob_y = math.sin(self.bob_offset) * self.bob_amplitude
        self.position.y = self.initial_y + bob_y
        
        # Update position
        super().update(delta_time)
        
    def collect(self):
        """Mark token as collected and return value and effect"""
        self.collected = True
        self.visible = False
        
        # Return both value and effect information
        return {
            "value": self.value,
            "effect": getattr(self, "effect", None),
            "duration": getattr(self, "effect_duration", 0),
            "type": self.token_type
        }
        
    def is_off_screen(self, camera_x, screen_width):
        """Check if token is off screen and can be removed"""
        return self.position.x < camera_x - 100

class TokenManager:
    """Manages all tokens in the game"""
    
    def __init__(self, screen_width, ground_y):
        self.screen_width = screen_width
        self.ground_y = ground_y
        self.tokens = []
        
        # Spawn timing
        self.spawn_timer = 0.0
        self.min_spawn_interval = 3.0  # Minimum seconds between token spawns
        self.max_spawn_interval = 8.0  # Maximum seconds between token spawns
        self.next_spawn_time = random.uniform(self.min_spawn_interval, self.max_spawn_interval)
        
        # Powerup spawn timing (separate from regular tokens)
        self.powerup_spawn_timer = 0.0
        self.min_powerup_interval = 15.0  # Minimum seconds between powerup spawns
        self.max_powerup_interval = 30.0  # Maximum seconds between powerup spawns
        self.next_powerup_time = random.uniform(self.min_powerup_interval, self.max_powerup_interval)
        
        # Token heights (different levels for variety)
        self.token_heights = [
            self.ground_y - 50,   # Just above ground
            self.ground_y - 150,  # Mid-air
            self.ground_y - 250,  # High up
        ]
        
        # Token spawn probabilities
        self.coin_probability = 1.0  # Coins always spawn when timer triggers
        self.doublegold_probability = 0.5 # chance for doublegold
        self.halfspeed_min_score = 400  # Minimum score needed for halfspeed powerup
        self.godmode_min_score = 1000  # Minimum score needed for godmode powerup
        self.godmode_probability = 0.3 # chance for godmode 
        
        # Safe spawning parameters
        self.min_distance_from_obstacles = 150  # Minimum horizontal distance from obstacles
        self.vertical_safe_zone = 80  # Vertical buffer zone around obstacles
        
    def update(self, delta_time, speed, score, difficulty, camera_x, obstacle_manager=None):
        """Update all tokens and spawn new ones"""
        # Update spawn timer for regular coins
        self.spawn_timer += delta_time
        
        # Spawn new coin if it's time
        if self.spawn_timer >= self.next_spawn_time:
            self.spawn_coin(camera_x, obstacle_manager)
            self.spawn_timer = 0.0
            
            # Adjust spawn rate based on difficulty
            base_min = self.min_spawn_interval
            base_max = self.max_spawn_interval
            difficulty_factor = max(0.5, 1.0 - (difficulty * 0.2))
            
            self.next_spawn_time = random.uniform(
                base_min * difficulty_factor,
                base_max * difficulty_factor
            )
        
        # Update powerup spawn timer
        self.powerup_spawn_timer += delta_time
        
        # Spawn powerups if it's time
        if self.powerup_spawn_timer >= self.next_powerup_time:
            self.spawn_powerup(camera_x, score, obstacle_manager)
            self.powerup_spawn_timer = 0.0
            self.next_powerup_time = random.uniform(self.min_powerup_interval, self.max_powerup_interval)
        
        # Update existing tokens
        for token in self.tokens[:]:  # Use slice copy to allow removal during iteration
            token.update(delta_time, speed)
            
            # Remove tokens that are off screen
            if token.is_off_screen(camera_x, self.screen_width):
                self.tokens.remove(token)
                
    def is_safe_spawn_position(self, x, y, obstacle_manager):
        """Check if a position is safe to spawn a token (not overlapping with obstacles)"""
        if not obstacle_manager:
            return True
            
        # Create a temporary rect for the proposed token position
        token_rect = pygame.Rect(x - 20, y - 20, 40, 40)  # Token size approximation
        
        # Check against all existing obstacles
        for obstacle in obstacle_manager.obstacles:
            if obstacle.rect:
                # Expand obstacle rect with safety buffer
                safe_rect = obstacle.rect.inflate(
                    self.min_distance_from_obstacles * 2, 
                    self.vertical_safe_zone * 2
                )
                
                # Check if token would overlap with the safe zone
                if token_rect.colliderect(safe_rect):
                    return False
                    
        return True
                
    def spawn_coin(self, camera_x, obstacle_manager=None):
        """Spawn a new coin in a safe location"""
        max_attempts = 10  # Prevent infinite loops
        attempts = 0
        
        while attempts < max_attempts:
            # Position token ahead of camera
            x = camera_x + self.screen_width + random.randint(100, 300)
            y = random.choice(self.token_heights)
            
            # Check if position is safe
            if obstacle_manager is None or self.is_safe_spawn_position(x, y, obstacle_manager):
                # Create coin
                token = Token(x, y, "coin")
                self.tokens.append(token)
                return
                
            attempts += 1
        
        # If we couldn't find a safe position, spawn anyway but further ahead
        x = camera_x + self.screen_width + random.randint(400, 600)
        y = random.choice(self.token_heights)
        token = Token(x, y, "coin")
        self.tokens.append(token)
        
    def spawn_powerup(self, camera_x, score, obstacle_manager=None):
        """Spawn a powerup in a safe location based on conditions"""
        max_attempts = 10  # Prevent infinite loops
        attempts = 0
        
        # Determine which powerup to spawn first
        available_powerups = []
        
        # Doublegold can always spawn (but with probability)
        if random.random() < self.doublegold_probability:
            available_powerups.append("doublegold")
            
        # Halfspeed only spawns if score is high enough
        if score >= self.halfspeed_min_score:
            available_powerups.append("halfspeed")
            
        # Godmode only spawns if score is very high and with low probability
        if score >= self.godmode_min_score and random.random() < self.godmode_probability:
            available_powerups.append("godmode")
        
        # Return early if no powerups are available
        if not available_powerups:
            return
            
        powerup_type = random.choice(available_powerups)
        
        while attempts < max_attempts:
            # Position powerup ahead of camera
            x = camera_x + self.screen_width + random.randint(200, 500)
            y = random.choice(self.token_heights)
            
            # Check if position is safe
            if obstacle_manager is None or self.is_safe_spawn_position(x, y, obstacle_manager):
                powerup = Token(x, y, powerup_type)
                self.tokens.append(powerup)
                print(f"Spawned {powerup_type} powerup at score {int(score)} at safe position")
                return
                
            attempts += 1
        
        # If we couldn't find a safe position, spawn anyway but much further ahead
        x = camera_x + self.screen_width + random.randint(600, 800)
        y = random.choice(self.token_heights)
        powerup = Token(x, y, powerup_type)
        self.tokens.append(powerup)
        print(f"Spawned {powerup_type} powerup at score {int(score)} at fallback position")
        
    def choose_token_type(self):
        """Choose a token type based on rarity weights"""
        total_weight = sum(self.token_types.values())
        random_value = random.randint(1, total_weight)
        
        cumulative_weight = 0
        for token_type, weight in self.token_types.items():
            cumulative_weight += weight
            if random_value <= cumulative_weight:
                return token_type
                
        return "coin"  # Fallback
        
    def check_collision(self, dino):
        """Check collision between dino and tokens"""
        collected_items = []
        total_coin_value = 0
        powerup_effects = []
        
        for token in self.tokens[:]:
            if not token.collected and token.collides_with(dino):
                collected_data = token.collect()
                collected_items.append(collected_data)
                
                if collected_data["type"] == "coin":
                    total_coin_value += collected_data["value"]
                else:
                    # It's a powerup
                    powerup_effects.append({
                        "effect": collected_data["effect"],
                        "duration": collected_data["duration"],
                        "type": collected_data["type"]
                    })
                
                self.tokens.remove(token)
                
        return total_coin_value, powerup_effects
        
    def draw(self, screen):
        """Draw all tokens"""
        active_items = 0
        for token in self.tokens:
            if not token.collected:
                active_items += 1
                if token.sprite and token.rect:
                    token.draw(screen)
                
    def clear(self):
        """Clear all tokens (for game restart)"""
        self.tokens.clear()
        self.spawn_timer = 0.0
        self.powerup_spawn_timer = 0.0
        self.next_spawn_time = random.uniform(self.min_spawn_interval, self.max_spawn_interval)
        self.next_powerup_time = random.uniform(self.min_powerup_interval, self.max_powerup_interval)
