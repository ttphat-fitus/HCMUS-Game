"""
Singleton Pattern Implementation for Game Engine

This module demonstrates the Singleton Pattern, which ensures that only one
instance of the game engine exists throughout the application lifecycle.

DESIGN PATTERN JUSTIFICATION:
The Singleton Pattern is perfect for the GameEngine because:

1. **Single Game Instance**: Only one game should run at a time to prevent
   conflicts in game state, input handling, and resource management.

2. **Global Access Point**: Various game components need access to the game
   engine (player, obstacles, UI) without passing references everywhere.

3. **Resource Management**: Centralized control over game resources like
   the display, input handler, and game state prevents conflicts.

4. **State Consistency**: Ensures all game components share the same game
   state and prevents synchronization issues.

5. **Lifecycle Management**: Single point of control for game initialization,
   running, and cleanup.
"""

import threading
from typing import Optional, List, Any
from game.entities.game_object import GameObject

class SingletonMeta(type):
    """
    Thread-safe Singleton metaclass
    
    This metaclass ensures that only one instance of the GameEngine
    can exist, even in multi-threaded environments.
    """
    
    _instances = {}
    _lock: threading.Lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        """
        Control instance creation
        
        Uses double-checked locking pattern for thread safety
        """
        if cls not in cls._instances:
            with cls._lock:
                # Double-check in case another thread created the instance
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]

class GameEngine(metaclass=SingletonMeta):
    """
    Singleton Game Engine managing the entire game state and lifecycle
    
    Demonstrates the Singleton Pattern by ensuring only one game instance
    exists and providing global access to game functionality.
    
    Responsibilities:
    - Game state management (running, paused, game over)
    - Game loop coordination (update, render cycle)
    - Component coordination (player, obstacles, score)
    - Input handling coordination
    - Display management
    """
    
    def __init__(self):
        """
        Initialize game engine
        
        Note: This should only be called once due to Singleton pattern
        """
        # Prevent multiple initialization
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        
        # Game state
        self._running = False
        self._paused = False
        self._game_over = False
        self._score = 0
        self._high_score = 0
        self._game_speed = 1.0
        self._difficulty_level = 1
        self._difficulty = "normal"  # easy, normal, hard
        
        # Game dimensions
        self._screen_width = 80
        self._screen_height = 20
        self._ground_y = 15
        
        # Enhanced statistics tracking
        self._game_start_time = 0
        self._obstacles_dodged = 0
        self._achievements = []
        self._level = 1
        self._speed_multiplier = 1.0
        
        # Game objects
        self._player: Optional['Player'] = None
        self._obstacles: List['Obstacle'] = []
        self._game_objects: List[GameObject] = []
        
        # Game components (will be injected)
        self._input_handler: Optional[Any] = None
        self._display: Optional[Any] = None
        self._observers: List[Any] = []
        
        # Timing
        self._frame_count = 0
        self._target_fps = 20
        self._frame_time = 1.0 / self._target_fps
        
        # Obstacle spawning
        self._last_obstacle_spawn = 0
        self._obstacle_spawn_interval = 60  # frames
        
        # Load high score
        self._load_high_score()
    
    @classmethod
    def get_instance(cls) -> 'GameEngine':
        """
        Get the singleton instance of GameEngine
        
        Returns:
            The unique GameEngine instance
        """
        return cls()
    
    @classmethod
    def destroy_instance(cls) -> None:
        """
        Destroy the singleton instance (for cleanup)
        """
        if cls in cls._instances:
            instance = cls._instances[cls]
            instance._cleanup()
            del cls._instances[cls]
    
    # Properties for controlled access (Encapsulation)
    @property
    def running(self) -> bool:
        """Check if game is running"""
        return self._running
    
    @property
    def paused(self) -> bool:
        """Check if game is paused"""
        return self._paused
    
    @property
    def game_over(self) -> bool:
        """Check if game is over"""
        return self._game_over
    
    @property
    def score(self) -> int:
        """Get current score"""
        return self._score
    
    @property
    def high_score(self) -> int:
        """Get high score"""
        return self._high_score
    
    @property
    def screen_width(self) -> int:
        """Get screen width"""
        return self._screen_width
    
    @property
    def screen_height(self) -> int:
        """Get screen height"""
        return self._screen_height
    
    @property
    def ground_y(self) -> int:
        """Get ground level"""
        return self._ground_y
    
    @property
    def player(self) -> Optional['Player']:
        """Get player object"""
        return self._player
    
    @property
    def obstacles(self) -> List['Obstacle']:
        """Get list of obstacles"""
        return self._obstacles.copy()  # Return copy to prevent external modification
    
    @property
    def game_speed(self) -> float:
        """Get current game speed"""
        return self._game_speed
    
    @property
    def difficulty_level(self) -> int:
        """Get current difficulty level"""
        return self._difficulty_level
    
    # Game lifecycle methods
    def initialize(self) -> bool:
        """
        Initialize game components
        
        Returns:
            True if initialization successful
        """
        try:
            # Import here to avoid circular imports
            from game.entities.player import Player
            from game.utils.input_handler import InputHandler
            from game.utils.display import Display
            
            # Create game components
            self._player = Player(10, self._ground_y)
            self._input_handler = InputHandler()
            self._display = Display(self._screen_width, self._screen_height)
            
            # Initialize game state
            self._obstacles.clear()
            self._game_objects.clear()
            self._score = 0
            self._game_speed = 1.0
            self._difficulty_level = 1
            self._frame_count = 0
            self._last_obstacle_spawn = 0
            
            # Add player to game objects
            if self._player:
                self._game_objects.append(self._player)
            
            # Notify observers of game start
            self._notify_observers("game_start", 0)
            
            return True
            
        except Exception as e:
            print(f"Failed to initialize game: {e}")
            return False
    
    def run(self) -> None:
        """
        Main game loop
        
        Coordinates the entire game execution cycle
        """
        if not self._running:
            self._running = True
            self._game_over = False
            
            try:
                import time
                
                while self._running and not self._game_over:
                    frame_start = time.time()
                    
                    # Handle input
                    self._handle_input()
                    
                    # Update game state (if not paused)
                    if not self._paused:
                        self._update()
                    
                    # Render game
                    self._render()
                    
                    # Frame rate limiting
                    frame_elapsed = time.time() - frame_start
                    sleep_time = max(0, self._frame_time - frame_elapsed)
                    time.sleep(sleep_time)
                    
                    self._frame_count += 1
                
            except KeyboardInterrupt:
                print("\nGame interrupted by user")
            except Exception as e:
                print(f"Game error: {e}")
            finally:
                self._running = False
    
    def stop(self) -> None:
        """Stop the game"""
        self._running = False
    
    def pause(self) -> None:
        """Pause the game"""
        self._paused = True
        self._notify_observers("game_paused", 0)
    
    def resume(self) -> None:
        """Resume the game"""
        self._paused = False
        self._notify_observers("game_resumed", 0)
    
    def restart(self) -> None:
        """Restart the game"""
        self._game_over = False
        self.initialize()
    
    def end_game(self) -> None:
        """End the current game"""
        self._game_over = True
        self._running = False
        
        # Update high score
        if self._score > self._high_score:
            self._high_score = self._score
            self._save_high_score()
        
        self._notify_observers("game_over", self._score)
    
    # Component management
    def set_player(self, player: 'Player') -> None:
        """Set the player object"""
        self._player = player
        if player not in self._game_objects:
            self._game_objects.append(player)
    
    def add_obstacle(self, obstacle: 'Obstacle') -> None:
        """Add an obstacle to the game"""
        self._obstacles.append(obstacle)
        self._game_objects.append(obstacle)
    
    def remove_obstacle(self, obstacle: 'Obstacle') -> None:
        """Remove an obstacle from the game"""
        if obstacle in self._obstacles:
            self._obstacles.remove(obstacle)
        if obstacle in self._game_objects:
            self._game_objects.remove(obstacle)
    
    def clear_obstacles(self) -> None:
        """Clear all obstacles"""
        for obstacle in self._obstacles[:]:
            self.remove_obstacle(obstacle)
    
    # Observer pattern support
    def add_observer(self, observer: Any) -> None:
        """Add an observer for game events"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer: Any) -> None:
        """Remove an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self, event: str, data: Any) -> None:
        """Notify all observers of an event"""
        for observer in self._observers:
            if hasattr(observer, 'on_notify'):
                try:
                    observer.on_notify(event, data)
                except Exception as e:
                    print(f"Observer notification error: {e}")
    
    # Score management
    def add_score(self, points: int) -> None:
        """Add points to the score"""
        self._score += points
        self._notify_observers("score_changed", self._score)
    
    def increase_difficulty(self) -> None:
        """Increase game difficulty"""
        self._difficulty_level += 1
        self._game_speed += 0.1
        self._obstacle_spawn_interval = max(30, self._obstacle_spawn_interval - 5)
        self._notify_observers("difficulty_increased", self._difficulty_level)
    
    # Component setters for simplified main
    def set_input_handler(self, input_handler: Any) -> None:
        """Set the input handler"""
        self._input_handler = input_handler
    
    def set_display(self, display: Any) -> None:
        """Set the display"""
        self._display = display
    
    def start(self) -> None:
        """Start the game"""
        self._running = True
        self._game_over = False
        self._paused = False
        self._notify_observers("game_start", 0)
    
    def update(self) -> None:
        """Public update method for simplified main"""
        if not self._paused and not self._game_over:
            self._update()
    
    def render(self) -> None:
        """Public render method for simplified main"""
        if self._display:
            self._render()
    
    def toggle_pause(self) -> None:
        """Toggle pause state"""
        if self._paused:
            self.resume()
        else:
            self.pause()
    
    # Private methods
    def _handle_input(self) -> None:
        """Handle user input"""
        if self._input_handler and self._player:
            key = self._input_handler.get_key()
            
            if key in ['space', 'up']:
                self._player.jump()
            elif key in ['down', 's']:
                self._player.duck()
            elif key in ['escape', 'q']:
                self.stop()
            elif key == 'p':
                if self._paused:
                    self.resume()
                else:
                    self.pause()
    
    def _update(self) -> None:
        """Update game state"""
        # Update all game objects
        for game_object in self._game_objects[:]:
            game_object.update()
            
            # Remove inactive objects
            if not game_object.active:
                if game_object in self._game_objects:
                    self._game_objects.remove(game_object)
                if hasattr(game_object, 'get_obstacle_type'):  # It's an obstacle
                    if game_object in self._obstacles:
                        self._obstacles.remove(game_object)
        
        # Spawn new obstacles
        self._spawn_obstacles()
        
        # Check collisions
        self._check_collisions()
        
        # Update score (distance-based)
        if self._frame_count % 10 == 0:  # Every 10 frames
            self.add_score(1)
        
        # Increase difficulty periodically
        if self._score > 0 and self._score % 100 == 0:
            if self._score // 100 > self._difficulty_level - 1:
                self.increase_difficulty()
    
    def _render(self) -> None:
        """Render the game with modern visuals"""
        if not self._display:
            return
            
        # Clear the display
        self._display.clear()
        
        # Render background elements
        if hasattr(self._display, 'draw_clouds'):
            self._display.draw_clouds()
        
        # Render ground with modern styling
        if hasattr(self._display, 'draw_ground'):
            self._display.draw_ground(self._ground_y)
        else:
            # Fallback ground rendering
            ground_char = "▔"
            for x in range(self._screen_width):
                self._display.draw_char(x, self._ground_y, ground_char)
        
        # Render player with enhanced visuals
        if self._player and self._player.active:
            if hasattr(self._player, 'render_to_display'):
                self._player.render_to_display(self._display)
            else:
                # Fallback rendering
                sprite = self._player.render()
                x, y = int(self._player.x), int(self._player.y)
                self._display.draw_char(x, y, sprite)
        
        # Render obstacles with enhanced visuals
        for obstacle in self._obstacles:
            if obstacle.active:
                if hasattr(obstacle, 'render_to_display'):
                    obstacle.render_to_display(self._display)
                elif hasattr(self._display, 'draw_object'):
                    self._display.draw_object(obstacle)
                else:
                    # Fallback rendering
                    sprite = obstacle.render()
                    x, y = int(obstacle.x), int(obstacle.y)
                    if hasattr(self._display, 'draw_char'):
                        self._display.draw_char(x, y, sprite)
        
        # Render modern HUD
        if hasattr(self._display, 'draw_enhanced_score'):
            level = self._difficulty_level
            speed_multiplier = self._game_speed / 1.0  # Normalize speed
            self._display.draw_enhanced_score(self._score, self._high_score, level, speed_multiplier)
        else:
            # Fallback HUD
            if hasattr(self._display, 'draw_score'):
                self._display.draw_score(self._score, self._high_score)
            if hasattr(self._display, 'draw_speed'):
                self._display.draw_speed(self._game_speed)
        
        # Handle special screens
        if self._paused and not self._game_over:
            if hasattr(self._display, 'draw_pause_screen'):
                self._display.draw_pause_screen()
            else:
                # Fallback pause screen
                pause_text = "PAUSED - Press P to Resume"
                self._display.draw_text(self._screen_width // 2 - len(pause_text) // 2, 
                                      self._screen_height // 2, pause_text)
        
        # Game over screen handled in main loop
        
        # Present the final frame
        self._display.present()
    
    def _spawn_obstacles(self) -> None:
        """Spawn new obstacles"""
        from game.patterns.factory import ObstacleFactory, DifficultyLevel
        
        if self._frame_count - self._last_obstacle_spawn >= self._obstacle_spawn_interval:
            # Determine difficulty level
            difficulty = DifficultyLevel(min(4, max(1, self._difficulty_level)))
            
            # Create obstacle at right edge of screen
            obstacle = ObstacleFactory.create_random_obstacle(
                self._screen_width, 
                self._ground_y, 
                difficulty
            )
            
            self.add_obstacle(obstacle)
            self._last_obstacle_spawn = self._frame_count
            self._notify_observers("obstacle_spawned", obstacle)
    
    def _check_collisions(self) -> None:
        """Check for collisions between player and obstacles"""
        if not self._player or not self._player.active:
            return
        
        for obstacle in self._obstacles:
            if obstacle.active and self._player.check_collision(obstacle):
                self.end_game()
                break
    
    def _load_high_score(self) -> None:
        """Load high score from file"""
        try:
            with open("high_score.txt", "r") as f:
                self._high_score = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            self._high_score = 0
    
    def _save_high_score(self) -> None:
        """Save high score to file"""
        try:
            with open("high_score.txt", "w") as f:
                f.write(str(self._high_score))
        except Exception as e:
            print(f"Failed to save high score: {e}")
    
    def _cleanup(self) -> None:
        """Clean up resources"""
        if self._input_handler and hasattr(self._input_handler, 'disable_raw_mode'):
            self._input_handler.disable_raw_mode()
        
        if self._display and hasattr(self._display, 'cleanup'):
            self._display.cleanup()
    
    # Enhanced UI Support Methods
    def set_difficulty(self, difficulty: str) -> None:
        """Set game difficulty level"""
        self._difficulty = difficulty
        
        # Adjust game parameters based on difficulty
        if difficulty == "easy":
            self._obstacle_spawn_interval = 80  # Slower spawning
            self._target_fps = 15  # Slower game speed
        elif difficulty == "normal":
            self._obstacle_spawn_interval = 60  # Normal spawning
            self._target_fps = 20  # Normal game speed
        elif difficulty == "hard":
            self._obstacle_spawn_interval = 40  # Faster spawning
            self._target_fps = 25  # Faster game speed
    
    def get_game_stats(self) -> dict:
        """Get comprehensive game statistics"""
        import time
        current_time = time.time()
        time_played = current_time - self._game_start_time if self._game_start_time > 0 else 0
        
        return {
            'score': self._score,
            'high_score': self._high_score,
            'level': self._level,
            'speed_multiplier': self._speed_multiplier,
            'obstacles_dodged': self._obstacles_dodged,
            'time_played': time_played,
            'achievements': self._achievements.copy(),
            'difficulty': self._difficulty,
            'frame_count': self._frame_count
        }
    
    def is_running(self) -> bool:
        """Check if game is running"""
        return self._running
    
    def is_paused(self) -> bool:
        """Check if game is paused"""
        return self._paused
    
    def is_game_over(self) -> bool:
        """Check if game is over"""
        return self._game_over
    
    def toggle_pause(self) -> None:
        """Toggle game pause state"""
        if not self._game_over:
            self._paused = not self._paused
            self._notify_observers("game_paused" if self._paused else "game_resumed", self._paused)
    
    def restart(self) -> None:
        """Restart the game"""
        import time
        
        # Reset game state
        self._running = True
        self._paused = False
        self._game_over = False
        self._score = 0
        self._level = 1
        self._speed_multiplier = 1.0
        self._obstacles_dodged = 0
        self._achievements = []
        self._frame_count = 0
        self._last_obstacle_spawn = 0
        self._game_start_time = time.time()
        
        # Clear obstacles
        self._obstacles.clear()
        self._game_objects.clear()
        
        # Reset player
        if self._player:
            self._player.reset()
            self._game_objects.append(self._player)
        
        self._notify_observers("game_restarted", None)
    
    def get_player(self):
        """Get the player object"""
        return self._player
    
    def get_display(self):
        """Get the display object"""
        return self._display
    
    def add_achievement(self, achievement: str) -> None:
        """Add an achievement"""
        if achievement not in self._achievements:
            self._achievements.append(achievement)
            self._notify_observers("achievement_unlocked", achievement)
    
    def check_achievements(self) -> None:
        """Check for new achievements"""
        # Score-based achievements
        if self._score >= 1000 and "First Thousand" not in self._achievements:
            self.add_achievement("First Thousand")
        
        if self._score >= 5000 and "Five Thousand Club" not in self._achievements:
            self.add_achievement("Five Thousand Club")
        
        if self._score >= 10000 and "Perfect Ten" not in self._achievements:
            self.add_achievement("Perfect Ten")
        
        # Obstacle-based achievements
        if self._obstacles_dodged >= 10 and "Dodge Master" not in self._achievements:
            self.add_achievement("Dodge Master")
        
        if self._obstacles_dodged >= 50 and "Obstacle Legend" not in self._achievements:
            self.add_achievement("Obstacle Legend")
        
        if self._obstacles_dodged >= 100 and "Untouchable" not in self._achievements:
            self.add_achievement("Untouchable")
        
        # Level-based achievements
        if self._level >= 5 and "Level 5 Reached" not in self._achievements:
            self.add_achievement("Level 5 Reached")
        
        if self._level >= 10 and "Double Digits" not in self._achievements:
            self.add_achievement("Double Digits")
        
        # Speed-based achievements
        if self._speed_multiplier >= 2.0 and "Speed Demon" not in self._achievements:
            self.add_achievement("Speed Demon")
        
        if self._speed_multiplier >= 3.0 and "Lightning Fast" not in self._achievements:
            self.add_achievement("Lightning Fast")
    
    def increment_obstacles_dodged(self) -> None:
        """Increment obstacles dodged counter"""
        self._obstacles_dodged += 1
        self._notify_observers("obstacle_dodged", self._obstacles_dodged)

# Singleton Pattern Benefits:
# 1. Single Instance: Ensures only one game runs at a time
# 2. Global Access: Easy access from any game component
# 3. Resource Control: Centralized management of game resources
# 4. State Consistency: All components share the same game state
# 5. Thread Safety: Prevents race conditions in multi-threaded scenarios
