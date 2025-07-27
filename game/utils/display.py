"""
Modern Display Manager with Advanced UI Graphics

This module provides a sophisticated console display system with modern
visual effects, colors, and animations for the T-Rex Runner game.
"""

import os
import sys
import time
import math
from typing import List, Optional, Tuple
from game.entities.game_object import GameObject

class Colors:
    """ANSI color codes for modern terminal graphics"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Basic colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

class Display:
    """
    Modern Display Manager with Advanced Graphics
    
    Features:
    - ANSI color support for modern terminals
    - Smooth animations and transitions
    - Progressive UI elements
    - Professional visual effects
    - Optimized rendering pipeline
    """
    
    def __init__(self, width: int = 80, height: int = 24):
        """
        Initialize modern display system
        
        Args:
            width: Screen width in characters
            height: Screen height in characters
        """
        self.width = width
        self.height = height
        self._buffer: List[List[str]] = []
        self._color_buffer: List[List[str]] = []
        self._frame_count = 0
        self._animation_time = 0.0
        
        # Modern UI settings
        self._use_colors = self._detect_color_support()
        self._use_unicode = True
        
        # Initialize buffers
        self._init_buffers()
        
        # Platform detection
        self._is_windows = sys.platform.startswith('win')
        
        # Initialize console for modern display
        self._init_modern_console()
    
    def _detect_color_support(self) -> bool:
        """Detect if terminal supports colors"""
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    
    def _init_buffers(self) -> None:
        """Initialize display buffers"""
        self._buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self._color_buffer = [[Colors.RESET for _ in range(self.width)] for _ in range(self.height)]
    
    def _init_modern_console(self) -> None:
        """Initialize console for modern display"""
        if not self._is_windows and self._use_colors:
            # Enable cursor hiding and alternate screen
            sys.stdout.write('\033[?25l')  # Hide cursor
            sys.stdout.write('\033[?1049h')  # Alternate screen
            sys.stdout.flush()
    
    def clear(self) -> None:
        """Clear display with modern effect"""
        self._init_buffers()
        self._frame_count += 1
        self._animation_time = self._frame_count * 0.05
    
    def draw_char(self, x: int, y: int, char: str, color: str = Colors.RESET) -> None:
        """Draw character with color support"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self._buffer[y][x] = char
            if self._use_colors:
                self._color_buffer[y][x] = color
    
    def draw_string(self, x: int, y: int, text: str, color: str = Colors.RESET) -> None:
        """Draw colored string"""
        for i, char in enumerate(text):
            if x + i < self.width:
                self.draw_char(x + i, y, char, color)
            else:
                break
    
    def draw_text(self, x: int, y: int, text: str, center: bool = False, color: str = Colors.RESET) -> None:
        """Draw text with centering support"""
        if center:
            x = max(0, x - len(text) // 2)
        self.draw_string(x, y, text, color)
    
    def draw_object(self, game_object: GameObject) -> None:
        """Draw game object with enhanced visuals"""
        if not game_object.active:
            return
        
        sprite = game_object.render()
        x, y = game_object.position
        
        # Add color based on object type
        color = Colors.RESET
        if hasattr(game_object, 'get_obstacle_type'):
            # It's an obstacle
            color = Colors.BRIGHT_RED
        elif hasattr(game_object, 'state'):
            # It's the player
            color = Colors.BRIGHT_GREEN
        
        self.draw_string(x, y, sprite, color)
    
    def draw_modern_ground(self, ground_y: int) -> None:
        """Draw modern animated ground with depth"""
        # Main ground line with color gradient
        ground_chars = ['▬', '═', '━', '▬']
        for x in range(self.width):
            char_index = (x + self._frame_count // 4) % len(ground_chars)
            char = ground_chars[char_index]
            
            # Color gradient for depth
            if x % 3 == 0:
                color = Colors.BRIGHT_YELLOW
            elif x % 2 == 0:
                color = Colors.YELLOW
            else:
                color = Colors.DIM + Colors.YELLOW
            
            self.draw_char(x, ground_y + 1, char, color)
        
        # Ground details with colors
        for x in range(0, self.width, 8):
            detail_x = (x + self._frame_count // 3) % self.width
            if detail_x < self.width - 1 and ground_y + 2 < self.height:
                # Rocks and grass with colors
                if (detail_x + self._frame_count // 8) % 20 == 0:
                    self.draw_char(detail_x, ground_y + 2, "∘", Colors.BRIGHT_BLACK)
                elif (detail_x + self._frame_count // 6) % 15 == 0:
                    self.draw_char(detail_x, ground_y + 2, "'", Colors.GREEN)
    
    def draw_ground(self, ground_y: int) -> None:
        """Public ground drawing method"""
        self.draw_modern_ground(ground_y)
    
    def draw_modern_clouds(self) -> None:
        """Draw modern animated clouds with depth"""
        cloud_patterns = [
            ("☁", Colors.BRIGHT_WHITE),
            ("⛅", Colors.WHITE),
            ("☁", Colors.DIM + Colors.WHITE)
        ]
        
        cloud_positions = [
            (20 + (self._frame_count // 12) % (self.width + 15), 2, 0),
            (50 + (self._frame_count // 10) % (self.width + 15), 4, 1),
            (75 + (self._frame_count // 15) % (self.width + 15), 1, 2)
        ]
        
        for x, y, pattern_idx in cloud_positions:
            wrapped_x = x % self.width
            if wrapped_x < self.width - 2 and y < self.height - 2:
                cloud, color = cloud_patterns[pattern_idx % len(cloud_patterns)]
                self.draw_string(wrapped_x, y, cloud, color)
    
    def draw_clouds(self) -> None:
        """Public cloud drawing method"""
        self.draw_modern_clouds()
    
    def draw_enhanced_score(self, score: int, high_score: int, level: int = 1, speed: float = 1.0) -> None:
        """Draw modern score display with colors and effects"""
        # Modern score display with gradients
        score_text = f"SCORE {score:05d}"
        self.draw_string(2, 1, score_text, Colors.BOLD + Colors.BRIGHT_CYAN)
        
        # High score with trophy effect
        if high_score > 0:
            hi_text = f"HIGH  {high_score:05d}"
            color = Colors.BOLD + Colors.BRIGHT_YELLOW if score >= high_score else Colors.YELLOW
            self.draw_string(2, 2, hi_text, color)
        
        # Level with progression color
        level_text = f"LEV {level:02d}"
        level_color = Colors.BRIGHT_GREEN if level >= 5 else Colors.GREEN
        self.draw_string(self.width - 8, 1, level_text, level_color)
        
        # Speed with dynamic color based on speed
        speed_text = f"{speed:.1f}×"
        if speed >= 3.0:
            speed_color = Colors.BOLD + Colors.BRIGHT_RED
        elif speed >= 2.0:
            speed_color = Colors.BRIGHT_YELLOW
        else:
            speed_color = Colors.WHITE
        self.draw_string(self.width - 5, 2, speed_text, speed_color)
        
        # Milestone celebration effect
        if score > 0 and score % 500 == 0 and (self._frame_count // 3) % 4 < 2:
            milestone_text = "★ MILESTONE REACHED! ★"
            center_x = self.width // 2 - len(milestone_text) // 2
            self.draw_string(center_x, 4, milestone_text, Colors.BOLD + Colors.BRIGHT_MAGENTA)
    
    def draw_modern_pause_screen(self) -> None:
        """Draw modern pause screen with visual effects"""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Create a modern border
        for y in range(center_y - 5, center_y + 6):
            for x in range(center_x - 20, center_x + 21):
                if 0 <= x < self.width and 0 <= y < self.height:
                    if (x == center_x - 20 or x == center_x + 20 or 
                        y == center_y - 5 or y == center_y + 5):
                        border_char = "█" if (x + y + self._frame_count) % 3 == 0 else "▓"
                        self.draw_char(x, y, border_char, Colors.BRIGHT_BLUE)
                    elif abs(x - center_x) < 19 and abs(y - center_y) < 4:
                        # Semi-transparent background
                        if (x + y) % 2 == 0:
                            self.draw_char(x, y, "░", Colors.DIM + Colors.BLUE)
        
        # Animated pause text
        pause_icon = "⏸" if (self._frame_count // 8) % 2 == 0 else "⏯"
        pause_text = f"{pause_icon} GAME PAUSED {pause_icon}"
        self.draw_text(center_x, center_y - 1, pause_text, True, Colors.BOLD + Colors.BRIGHT_WHITE)
        
        self.draw_text(center_x, center_y + 1, "Press P to continue", True, Colors.BRIGHT_CYAN)
        self.draw_text(center_x, center_y + 2, "Press ESC to quit", True, Colors.BRIGHT_RED)
    
    def draw_pause_screen(self) -> None:
        """Public pause screen method"""
        self.draw_modern_pause_screen()
    
    def draw_modern_game_over(self, score: int, high_score: int, level: int = 1) -> None:
        """Draw modern game over screen with spectacular effects"""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Animated border with multiple layers
        for layer in range(3):
            border_char = ["█", "▓", "░"][layer]
            color = [Colors.BRIGHT_RED, Colors.RED, Colors.DIM + Colors.RED][layer]
            
            for y in range(center_y - 7 + layer, center_y + 8 - layer):
                for x in range(center_x - 25 + layer, center_x + 26 - layer):
                    if (0 <= x < self.width and 0 <= y < self.height and
                        (x == center_x - 25 + layer or x == center_x + 25 - layer or
                         y == center_y - 7 + layer or y == center_y + 7 - layer)):
                        if (x + y + self._frame_count + layer) % 4 == 0:
                            self.draw_char(x, y, border_char, color)
        
        # Animated game over title
        skull_frames = ["💀", "☠", "💀", "👻"]
        skull = skull_frames[(self._frame_count // 10) % len(skull_frames)]
        title = f"{skull} GAME OVER {skull}"
        self.draw_text(center_x, center_y - 4, title, True, Colors.BOLD + Colors.BRIGHT_RED)
        
        # Score with celebration effects
        final_score = f"FINAL SCORE: {score:05d}"
        score_color = Colors.BOLD + Colors.BRIGHT_YELLOW
        self.draw_text(center_x, center_y - 2, final_score, True, score_color)
        
        level_text = f"LEVEL REACHED: {level}"
        self.draw_text(center_x, center_y - 1, level_text, True, Colors.BRIGHT_CYAN)
        
        # High score handling with effects
        if high_score > 0:
            if score >= high_score:
                if (self._frame_count // 5) % 3 < 2:
                    record_text = "🏆 NEW HIGH SCORE! 🏆"
                    self.draw_text(center_x, center_y, record_text, True, 
                                 Colors.BOLD + Colors.BRIGHT_MAGENTA)
            else:
                high_text = f"HIGH SCORE: {high_score:05d}"
                self.draw_text(center_x, center_y, high_text, True, Colors.YELLOW)
        
        # Achievement categories with colors
        if score >= 1000:
            if score >= 5000:
                achievement = "🥇 GOLD CHAMPION!"
                color = Colors.BOLD + Colors.BRIGHT_YELLOW
            elif score >= 2500:
                achievement = "🥈 SILVER MASTER!"
                color = Colors.BOLD + Colors.BRIGHT_WHITE
            else:
                achievement = "🥉 BRONZE RUNNER!"
                color = Colors.BOLD + Colors.YELLOW
            self.draw_text(center_x, center_y + 1, achievement, True, color)
        
        # Blinking restart instructions
        if (self._frame_count // 20) % 2 == 0:
            restart_text = "Press SPACE to restart • ESC to quit"
            self.draw_text(center_x, center_y + 3, restart_text, True, Colors.BRIGHT_GREEN)
    
    def draw_game_over_screen(self, score: int, high_score: int, level: int = 1) -> None:
        """Public game over screen method"""
        self.draw_modern_game_over(score, high_score, level)
    
    def present(self) -> None:
        """Present buffer with modern rendering"""
        # Move cursor to top-left
        if not self._is_windows:
            sys.stdout.write('\033[H')
        
        # Render with colors
        output_lines = []
        for y in range(self.height):
            line_chars = []
            current_color = Colors.RESET
            
            for x in range(self.width):
                char = self._buffer[y][x]
                color = self._color_buffer[y][x] if self._use_colors else Colors.RESET
                
                if color != current_color:
                    line_chars.append(color)
                    current_color = color
                
                line_chars.append(char)
            
            # Reset color at end of line
            if current_color != Colors.RESET:
                line_chars.append(Colors.RESET)
            
            output_lines.append(''.join(line_chars))
        
        # Output everything at once for smooth rendering
        sys.stdout.write('\n'.join(output_lines))
        sys.stdout.flush()
    
    def cleanup(self) -> None:
        """Cleanup modern display"""
        if not self._is_windows and self._use_colors:
            # Restore normal screen and cursor
            sys.stdout.write('\033[?1049l')  # Exit alternate screen
            sys.stdout.write('\033[?25h')    # Show cursor
            sys.stdout.write(Colors.RESET)   # Reset colors
            sys.stdout.flush()

