"""
Obstacle classes demonstrating Inheritance and Polymorphism

This module contains the base Obstacle class and specific obstacle types
that demonstrate inheritance hierarchies and polymorphic behavior.
"""

from abc import abstractmethod
import math
from enum import Enum
from game.entities.game_object import GameObject

class ObstacleType(Enum):
    """Enumeration of obstacle types"""
    CACTUS = "cactus"
    BIRD = "bird"
    ROCK = "rock"

class Obstacle(GameObject):
    """
    Abstract base class for all obstacles
    
    Demonstrates:
    - Inheritance: Extends GameObject
    - Abstraction: Defines common obstacle interface
    - Encapsulation: Protected obstacle properties
    """
    
    def __init__(self, x: int, y: int, sprite: str, speed: int = 1):
        """
        Initialize obstacle
        
        Args:
            x: X position
            y: Y position
            sprite: Obstacle character
            speed: Movement speed
        """
        super().__init__(x, y, sprite)
        self._speed = speed
        self._original_x = x
    
    @property
    def speed(self) -> int:
        """Get obstacle speed"""
        return self._speed
    
    @property
    def original_x(self) -> int:
        """Get original X position"""
        return self._original_x
    
    def set_speed(self, speed: int) -> None:
        """Set obstacle movement speed"""
        self._speed = speed
    
    @abstractmethod
    def move_left(self) -> None:
        """Move obstacle left - must be implemented by subclasses"""
        pass
    
    def update(self) -> None:
        """
        Update obstacle (Polymorphism)
        
        Base implementation handles common movement and boundary checking
        """
        self.move_left()
        
        # Deactivate if moved off screen (left edge)
        if self.x + self.width < 0:
            self.set_active(False)
    
    def render(self) -> str:
        """
        Render obstacle (Polymorphism)
        
        Returns:
            String representation of the obstacle
        """
        if not self.active:
            return " " * self.width
        return self.sprite
    
    def is_off_screen(self) -> bool:
        """Check if obstacle is off screen"""
        return self.x + self.width < 0

class Cactus(Obstacle):
    """
    Enhanced Cactus obstacle - ground-based obstacle with multiple sizes
    
    Demonstrates:
    - Inheritance: Extends Obstacle
    - Polymorphism: Specific implementation of abstract methods
    - Variety: Different cactus sizes and types
    """
    
    # Enhanced cactus sprites with different sizes and types
    SPRITES = {
        'small': ['🌵', '�', '🍃'],
        'medium': ['�🌲', '�', '�🎋'], 
        'large': ['🌳', '🌲', '🏔️'],
        'cluster': ['🌵🌵', '🌲🌲', '🌳🌳']  # Multi-character obstacles
    }
    
    def __init__(self, x: int, ground_y: int, size: str = 'small', cactus_type: int = 0):
        """
        Initialize enhanced cactus
        
        Args:
            x: X position
            ground_y: Ground level
            size: Cactus size (small, medium, large, cluster)
            cactus_type: Type of cactus within size category
        """
        sprites = self.SPRITES.get(size, self.SPRITES['small'])
        sprite = sprites[cactus_type % len(sprites)]
        super().__init__(x, ground_y, sprite, speed=1)
        
        self._size = size
        self._cactus_type = cactus_type
        
        # Set dimensions based on size
        if size == 'cluster':
            self._width = 2
            self._height = 2
        elif size == 'large':
            self._width = 1
            self._height = 3
        elif size == 'medium':
            self._width = 1
            self._height = 2
        else:  # small
            self._width = 1
            self._height = 1
    
    @property
    def size(self) -> str:
        """Get cactus size"""
        return self._size
    
    @property
    def cactus_type(self) -> int:
        """Get cactus type"""
        return self._cactus_type
    
    def move_left(self) -> None:
        """Move cactus left with enhanced speed"""
        self._x -= self._speed
    
    def get_obstacle_type(self) -> ObstacleType:
        """Get obstacle type"""
        return ObstacleType.CACTUS
    
    def get_collision_box(self) -> tuple:
        """Get enhanced collision box"""
        return (self._x, self._y - self._height + 1, self._width, self._height)

class Bird(Obstacle):
    """
    Enhanced Bird obstacle - flying obstacle with realistic flight patterns
    
    Demonstrates:
    - Inheritance: Extends Obstacle  
    - Polymorphism: Unique flying behavior
    - Encapsulation: Private animation state
    - Enhanced Movement: Multiple flight patterns
    """
    
    # Enhanced bird sprites with different types and flight animations
    SPRITES = {
        'eagle': ['🦅', '🦅'],  # Steady soaring
        'sparrow': ['🐦', '�'],  # Quick flapping
        'dove': ['�🕊️', '🕊'],  # Gentle gliding
        'pterodactyl': ['🦕', '🦖']  # Prehistoric (for fun!)
    }
    
    FLIGHT_PATTERNS = {
        'straight': lambda t: 0,
        'bobbing': lambda t: math.sin(t * 0.3) * 2,
        'swooping': lambda t: math.sin(t * 0.1) * 4,
        'erratic': lambda t: math.sin(t * 0.5) * 1 + math.cos(t * 0.7) * 1
    }
    
    def __init__(self, x: int, y: int, bird_type: str = 'sparrow', flight_pattern: str = 'bobbing'):
        """
        Initialize enhanced bird
        
        Args:
            x: X position
            y: Y position (flying height)
            bird_type: Type of bird (eagle, sparrow, dove, pterodactyl)
            flight_pattern: Flight pattern (straight, bobbing, swooping, erratic)
        """
        sprites = self.SPRITES.get(bird_type, self.SPRITES['sparrow'])
        sprite = sprites[0]  # Start with first sprite
        super().__init__(x, y, sprite, speed=1)
        
        self._width = 1
        self._height = 1
        self._original_y = y
        self._bird_type = bird_type
        self._flight_pattern = flight_pattern
        self._animation_time = 0.0
        self._sprite_index = 0
        self._animation_speed = 0.2
        
        # Flight pattern function
        self._pattern_func = self.FLIGHT_PATTERNS.get(flight_pattern, self.FLIGHT_PATTERNS['bobbing'])
    
    @property
    def bird_type(self) -> str:
        """Get bird type"""
        return self._bird_type
    
    @property
    def flight_pattern(self) -> str:
        """Get flight pattern"""
        return self._flight_pattern
    
    def update(self) -> None:
        """Update bird with enhanced flight animation"""
        super().update()
        
        # Move left
        self._x -= self._speed
        
        # Update animation time
        self._animation_time += self._animation_speed
        
        # Apply flight pattern
        y_offset = self._pattern_func(self._animation_time)
        self._y = int(self._original_y + y_offset)
        
        # Animate sprite (wing flapping effect)
        sprites = self.SPRITES[self._bird_type]
        self._sprite_index = int(self._animation_time * 5) % len(sprites)
        self._sprite = sprites[self._sprite_index]
        
        # Deactivate when off screen
        if self._x < -1:
            self._active = False
    
    def move_left(self) -> None:
        """Move bird left with flight pattern"""
        self._x -= self._speed
    
    def get_obstacle_type(self) -> ObstacleType:
        """Get obstacle type"""
        return ObstacleType.BIRD
    
    def get_collision_box(self) -> tuple:
        """Get bird collision box"""
        return (self._x, self._y, self._width, self._height)
    
    @property
    def bird_type(self) -> int:
        """Get bird type"""
        return self._bird_type
    
    @property
    def original_y(self) -> int:
        """Get original Y position"""
        return self._original_y
    
    def move_left(self) -> None:
        """Move bird left with bobbing motion (Polymorphism)"""
        self._x -= self._speed
        
        # Add bobbing motion
        self._bob_offset += self._bob_speed
        bob_y = int(math.sin(self._bob_offset) * self._bob_amplitude)
        self._y = self._original_y + bob_y
    
    def update(self) -> None:
        """
        Update bird with enhanced animation (Polymorphism)
        
        Overrides base update to add flying-specific behavior
        """
        super().update()  # Call parent update
        
        # Additional bird-specific updates could go here
        # (e.g., wing flapping animation, speed changes)
    
    def get_obstacle_type(self) -> ObstacleType:
        """Get obstacle type"""
        return ObstacleType.BIRD

class Rock(Obstacle):
    """
    Rock obstacle - low ground obstacle that must be jumped over
    
    Demonstrates:
    - Inheritance: Another concrete obstacle type
    - Polymorphism: Different behavior from other obstacles
    """
    
    SPRITES = ['🪨', '⛰️', '🗿']  # Different rock types
    
    def __init__(self, x: int, ground_y: int, rock_type: int = 0):
        """
        Initialize rock
        
        Args:
            x: X position
            ground_y: Ground level
            rock_type: Type of rock (index into SPRITES)
        """
        sprite = self.SPRITES[rock_type % len(self.SPRITES)]
        super().__init__(x, ground_y + 1, sprite, speed=1)  # Slightly above ground
        self._width = 1
        self._height = 1
        self._rock_type = rock_type
    
    @property
    def rock_type(self) -> int:
        """Get rock type"""
        return self._rock_type
    
    def move_left(self) -> None:
        """Move rock left (Polymorphism)"""
        self._x -= self._speed
    
    def get_obstacle_type(self) -> ObstacleType:
        """Get obstacle type"""
        return ObstacleType.ROCK
