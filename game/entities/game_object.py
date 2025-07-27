"""
Abstract base class for all game objects

This module demonstrates the Abstraction principle of OOP by defining
a common interface that all game entities must implement.
"""

from abc import ABC, abstractmethod
from typing import Tuple

class GameObject(ABC):
    """
    Abstract base class for all game objects
    
    Demonstrates:
    - Abstraction: Defines common interface for all game entities
    - Encapsulation: Protects internal state with properties
    """
    
    def __init__(self, x: int, y: int, sprite: str = ' '):
        """
        Initialize a game object
        
        Args:
            x: X coordinate
            y: Y coordinate 
            sprite: Character representation
        """
        self._x = x              # Protected member (Encapsulation)
        self._y = y              # Protected member (Encapsulation)
        self._sprite = sprite    # Protected member (Encapsulation)
        self._active = True      # Protected member (Encapsulation)
        self._width = 1          # Protected member (Encapsulation)
        self._height = 1         # Protected member (Encapsulation)
    
    # Properties for Encapsulation
    @property
    def x(self) -> int:
        """Get X coordinate"""
        return self._x
    
    @property
    def y(self) -> int:
        """Get Y coordinate"""
        return self._y
    
    @property
    def sprite(self) -> str:
        """Get sprite character"""
        return self._sprite
    
    @property
    def active(self) -> bool:
        """Get active status"""
        return self._active
    
    @property
    def width(self) -> int:
        """Get object width"""
        return self._width
    
    @property
    def height(self) -> int:
        """Get object height"""
        return self._height
    
    @property
    def position(self) -> Tuple[int, int]:
        """Get position as tuple"""
        return (self._x, self._y)
    
    # Controlled setters for Encapsulation
    def set_position(self, x: int, y: int) -> None:
        """Set object position"""
        self._x = x
        self._y = y
    
    def set_active(self, active: bool) -> None:
        """Set active status"""
        self._active = active
    
    def move(self, dx: int, dy: int) -> None:
        """Move object by offset"""
        self._x += dx
        self._y += dy
    
    # Abstract methods - forces subclasses to implement (Abstraction)
    @abstractmethod
    def update(self) -> None:
        """Update object state - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def render(self) -> str:
        """Render object as string - must be implemented by subclasses"""
        pass
    
    def check_collision(self, other: 'GameObject') -> bool:
        """
        Check collision with another game object
        
        Uses bounding box collision detection
        
        Args:
            other: Another GameObject to check collision with
            
        Returns:
            True if objects are colliding
        """
        if not (self.active and other.active):
            return False
        
        # Bounding box collision detection
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)
    
    def get_bounds(self) -> Tuple[int, int, int, int]:
        """
        Get object boundaries
        
        Returns:
            Tuple of (left, top, right, bottom)
        """
        return (self.x, self.y, self.x + self.width, self.y + self.height)
    
    def __repr__(self) -> str:
        """String representation for debugging"""
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, active={self.active})"
