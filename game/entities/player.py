"""
Player class implementing the T-Rex character

Demonstrates Inheritance and Polymorphism by extending GameObject
and implementing State pattern for player behaviors.
"""

from enum import Enum
from typing import List
from game.entities.game_object import GameObject

class PlayerState(Enum):
    """Player state enumeration for State pattern"""
    RUNNING = "running"
    JUMPING = "jumping"
    DUCKING = "ducking"

class Player(GameObject):
    """
    Enhanced Player class representing the T-Rex dinosaur
    
    Demonstrates:
    - Inheritance: Extends GameObject
    - Polymorphism: Overrides abstract methods with player-specific behavior
    - Encapsulation: Private state management
    - State Pattern: Different behaviors based on current state
    - Enhanced Animation: Improved visual feedback
    """
    
    # Enhanced class constants
    JUMP_HEIGHT = 6
    GRAVITY = 1
    JUMP_VELOCITY = -6
    
    # Enhanced animation sprites with more variety
    RUN_SPRITES = ['🦕', '🦖', '🦴']  # Running animation with bone kick
    JUMP_SPRITES = ['🦅', '✈️']      # Jumping animation
    DUCK_SPRITES = ['🐊', '🐍']      # Ducking animation  
    CELEBRATION_SPRITES = ['🎉', '🏆', '⭐']  # Milestone celebrations
    
    def __init__(self, x: int, ground_y: int):
        """
        Initialize enhanced player
        
        Args:
            x: Starting X position
            ground_y: Ground level Y coordinate
        """
        super().__init__(x, ground_y, self.RUN_SPRITES[0])
        
        # Enhanced state management
        self._state = PlayerState.RUNNING
        self._ground_y = ground_y
        self._velocity_y = 0
        self._jump_count = 0  # For double jump feature
        self._max_jumps = 1   # Can be upgraded
        
        # Enhanced animation system
        self._animation_time = 0.0
        self._animation_speed = 0.3
        self._sprite_index = 0
        self._celebration_timer = 0
        
        # Player stats for enhanced gameplay
        self._jumps_performed = 0
        self._ducks_performed = 0
        self._distance_traveled = 0.0
        self._ground_y = ground_y
        self._velocity_y = 0
        self._animation_frame = 0
        self._animation_timer = 0
        self._animation_speed = 10  # Frames between animation changes
        
        # Adjust size based on state
        self._width = 2
        self._height = 2
    
    @property
    def state(self) -> PlayerState:
        """Get current player state"""
        return self._state
    
    @property
    def ground_y(self) -> int:
        """Get ground level"""
        return self._ground_y
    
    @property
    def is_on_ground(self) -> bool:
        """Check if player is on ground"""
        return self._y >= self._ground_y
    
    def jump(self) -> bool:
        """
        Make player jump (only if on ground and running)
        
        Returns:
            True if jump was successful
        """
        if self._state == PlayerState.RUNNING and self.is_on_ground:
            self._state = PlayerState.JUMPING
            self._velocity_y = self.JUMP_VELOCITY
            self._sprite = self.JUMP_SPRITES[0]
            return True
        return False
    
    def duck(self) -> bool:
        """
        Make player duck
        
        Returns:
            True if duck was successful
        """
        if self._state in [PlayerState.RUNNING, PlayerState.JUMPING]:
            self._state = PlayerState.DUCKING
            self._sprite = self.DUCK_SPRITE
            self._height = 1  # Smaller hitbox when ducking
            if self.is_on_ground:
                self._y = self._ground_y  # Adjust position
            return True
        return False
    
    def stop_ducking(self) -> bool:
        """
        Stop ducking and return to running
        
        Returns:
            True if successful
        """
        if self._state == PlayerState.DUCKING and self.is_on_ground:
            self._state = PlayerState.RUNNING
            self._height = 2  # Restore normal height
            self._y = self._ground_y - 1  # Adjust position
            return True
        return False
    
    def update(self) -> None:
        """
        Enhanced update with better animations and physics
        
        This method demonstrates polymorphism by providing player-specific
        implementation with enhanced visual feedback.
        """
        self._update_physics()
        self._update_enhanced_animation()
        self._update_sprite()
        self._update_stats()
    
    def _update_physics(self) -> None:
        """Enhanced physics with better jump mechanics"""
        if self._state == PlayerState.JUMPING:
            # Apply gravity
            self._velocity_y += self.GRAVITY
            self._y += self._velocity_y
            
            # Check for landing
            if self._y >= self._ground_y:
                self._y = self._ground_y
                self._velocity_y = 0
                self._state = PlayerState.RUNNING
                self._jump_count = 0  # Reset jump count on landing
    
    def _update_enhanced_animation(self) -> None:
        """Enhanced animation system with more fluid transitions"""
        self._animation_time += self._animation_speed
        
        # Handle celebration animation
        if self._celebration_timer > 0:
            self._celebration_timer -= 1
            celebration_index = int(self._animation_time * 3) % len(self.CELEBRATION_SPRITES)
            self._sprite = self.CELEBRATION_SPRITES[celebration_index]
            return
        
        # State-based animation
        if self._state == PlayerState.RUNNING:
            self._sprite_index = int(self._animation_time * 2) % len(self.RUN_SPRITES)
            self._sprite = self.RUN_SPRITES[self._sprite_index]
        elif self._state == PlayerState.JUMPING:
            # Animate jump based on velocity
            if self._velocity_y < 0:  # Going up
                self._sprite = self.JUMP_SPRITES[0]
            else:  # Coming down
                self._sprite = self.JUMP_SPRITES[1] if len(self.JUMP_SPRITES) > 1 else self.JUMP_SPRITES[0]
        elif self._state == PlayerState.DUCKING:
            self._sprite_index = int(self._animation_time * 4) % len(self.DUCK_SPRITES)
            self._sprite = self.DUCK_SPRITES[self._sprite_index]
    
    def _update_sprite(self) -> None:
        """Update sprite (legacy method for compatibility)"""
        pass  # Animation is handled in _update_enhanced_animation
    
    def _update_stats(self) -> None:
        """Update player statistics"""
        if self._state == PlayerState.RUNNING:
            self._distance_traveled += 0.1
    
    def trigger_celebration(self, duration: int = 30) -> None:
        """Trigger celebration animation for milestones"""
        self._celebration_timer = duration
    
    def get_stats(self) -> dict:
        """Get player statistics"""
        return {
            'jumps': self._jumps_performed,
            'ducks': self._ducks_performed,
            'distance': self._distance_traveled
        }
    
    def get_collision_box(self) -> tuple:
        """
        Get player collision box
        
        Returns:
            Tuple of (x, y, width, height)
        """
        return (self._x, self._y, self._width, self._height)
    
    def render(self) -> str:
        """
        Render player sprite (Polymorphism)
        
        Returns:
            Current sprite character
        """
        return self._sprite
    
    def render_to_display(self, display) -> None:
        """
        Render the player with enhanced animations and effects to display
        
        Args:
            display: Display system for rendering
        """
        if not display:
            return
            
        try:
            from game.utils.display import Colors
        except ImportError:
            # Fallback if colors not available
            Colors = None
        
        # Get current sprite
        sprite = self._sprite
        
        # Calculate render position
        x = int(self._x)
        y = int(self._y)
        
        # Add visual effects based on state
        color = ""
        effect = ""
        
        if Colors:
            if self._state == PlayerState.DUCKING:
                color = Colors.BRIGHT_YELLOW + Colors.BOLD
                effect = "💨"  # Speed effect while ducking
            elif self._state == PlayerState.JUMPING:
                color = Colors.BRIGHT_CYAN + Colors.BOLD
                effect = "✨"  # Sparkle effect while jumping
            elif hasattr(self, '_invulnerable_timer') and self._invulnerable_timer > 0:
                # Flashing effect during invulnerability
                import time
                flash_interval = 0.1
                if (time.time() % (flash_interval * 2)) < flash_interval:
                    color = Colors.BRIGHT_RED + Colors.BOLD
                else:
                    color = Colors.BRIGHT_WHITE + Colors.BOLD
                effect = "🛡️"
            elif self._velocity_y > 0:
                color = Colors.BRIGHT_MAGENTA + Colors.BOLD
                effect = "⬆️"
            else:
                # Running state with frame-based coloring
                if self._sprite_index % 2 == 0:
                    color = Colors.BRIGHT_GREEN + Colors.BOLD
                else:
                    color = Colors.GREEN + Colors.BOLD
        
        # Draw the T-Rex sprite with color
        if hasattr(display, 'draw_text') and Colors:
            display.draw_text(x, y, sprite, False, color)
        elif hasattr(display, 'draw_char'):
            display.draw_char(x, y, sprite, color or "")
        else:
            # Fallback for basic display
            if hasattr(display, 'buffer') and hasattr(display, 'width') and hasattr(display, 'height'):
                if 0 <= x < display.width and 0 <= y < display.height:
                    display.buffer[y][x] = sprite
        
        # Add visual effects
        if effect and Colors and hasattr(display, 'draw_text'):
            import time
            if time.time() % 0.5 < 0.25:  # Blinking effect
                effect_x = x + 2
                effect_y = y
                if 0 <= effect_x < display.width and 0 <= effect_y < display.height:
                    display.draw_text(effect_x, effect_y, effect, False, Colors.BRIGHT_WHITE)
        
        # Draw movement trail for extra visual appeal
        if self._state == PlayerState.RUNNING and Colors and hasattr(display, 'draw_char'):
            trail_char = "·"
            trail_color = Colors.DIM
            for i in range(1, 3):
                trail_x = x - i
                trail_y = y
                if trail_x >= 0 and 0 <= trail_y < display.height:
                    display.draw_char(trail_x, trail_y, trail_char, trail_color)
        
        # Celebration effect when achieving milestones
        if hasattr(self, '_celebration_timer') and self._celebration_timer > 0 and Colors:
            import time
            celebration_effects = ["🎉", "⭐", "🌟", "✨", "🎊"]
            effect_idx = int(time.time() * 5) % len(celebration_effects)
            celebration_x = x + 1
            celebration_y = y - 1
            if (0 <= celebration_x < display.width and 0 <= celebration_y < display.height and 
                hasattr(display, 'draw_text')):
                display.draw_text(celebration_x, celebration_y, celebration_effects[effect_idx], 
                                False, Colors.BRIGHT_YELLOW + Colors.BOLD)
            self._celebration_timer -= 1
