#!/usr/bin/env python3
"""
T-Rex Runner Game - Simplified Working Version

A console-based implementation of Chrome's T-Rex Runner game demonstrating
Object-Oriented Programming principles and design patterns.

Author: AI Collaboration Project
Date: July 25, 2025
Language: Python 3.8+
"""

import sys
import os
import time

# Add game package to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from game.core.game_engine import GameEngine
from game.patterns.observer import ScoreObserver, GameEventObserver
from game.utils.input_handler import InputHandler
from game.utils.display import Display

def main():
    """Main game entry point with modern UI"""
    # Initialize modern display system
    display = Display(80, 24)
    input_handler = InputHandler()
    
    try:
        input_handler.enable_raw_mode()
        
        # Show modern welcome screen
        show_modern_welcome(display, input_handler)
        
        # Get game engine instance (Singleton Pattern)
        game = GameEngine.get_instance()
        
        # Create and register observers (Observer Pattern)
        score_observer = ScoreObserver()
        event_observer = GameEventObserver()
        
        game.add_observer(score_observer)
        game.add_observer(event_observer)
        
        # Initialize and run the game
        if game.initialize():
            display.clear()
            run_game_loop(game, input_handler, display)
        else:
            show_error_screen(display, "Failed to initialize game!")
            
    except KeyboardInterrupt:
        show_exit_screen(display, "Game interrupted by user")
    except Exception as e:
        show_error_screen(display, f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        input_handler.disable_raw_mode()
        display.cleanup()
        GameEngine.destroy_instance()

def show_modern_welcome(display: Display, input_handler: InputHandler):
    """Show modern animated welcome screen"""
    from game.utils.display import Colors
    
    for frame in range(60):  # 3 second animation at 20fps
        display.clear()
        
        center_x = display.width // 2
        center_y = display.height // 2
        
        # Animated title with color gradient
        title_frames = [
            "🦕 T-REX RUNNER 🦖",
            "🦖 T-REX RUNNER 🦕", 
            "🦴 T-REX RUNNER 🦴"
        ]
        title = title_frames[frame // 20]
        
        # Draw animated border
        for y in range(center_y - 8, center_y + 9):
            for x in range(center_x - 30, center_x + 31):
                if (0 <= x < display.width and 0 <= y < display.height and
                    (x == center_x - 30 or x == center_x + 30 or 
                     y == center_y - 8 or y == center_y + 8)):
                    border_char = "█" if (x + y + frame) % 3 == 0 else "▓"
                    color = Colors.BRIGHT_CYAN if frame % 10 < 5 else Colors.CYAN
                    display.draw_char(x, y, border_char, color)
        
        # Title with rainbow effect
        title_color = Colors.BOLD + Colors.BRIGHT_MAGENTA
        display.draw_text(center_x, center_y - 5, title, True, title_color)
        
        # Subtitle
        subtitle = "Modern Console Gaming Experience"
        display.draw_text(center_x, center_y - 3, subtitle, True, Colors.BRIGHT_YELLOW)
        
        # Feature highlights
        features = [
            "🎮 Enhanced Graphics & Animations",
            "🌈 Modern Color System", 
            "🏆 Progressive Difficulty",
            "⚡ Smooth 20 FPS Gameplay"
        ]
        
        for i, feature in enumerate(features):
            if frame > 15 + i * 5:  # Staggered appearance
                color = Colors.BRIGHT_WHITE if (frame + i) % 20 < 10 else Colors.WHITE
                display.draw_text(center_x, center_y - 1 + i, feature, True, color)
        
        # Controls section
        if frame > 40:
            controls_title = "🎯 CONTROLS:"
            display.draw_text(center_x, center_y + 5, controls_title, True, Colors.BOLD + Colors.BRIGHT_GREEN)
            
            controls = [
                "SPACE/↑ - Jump over obstacles",
                "DOWN/S - Duck under birds", 
                "P - Pause game",
                "ESC/Q - Quit"
            ]
            
            for i, control in enumerate(controls):
                display.draw_text(center_x, center_y + 6 + i, control, True, Colors.GREEN)
        
        # Start prompt with blinking effect
        if frame > 50 and frame % 10 < 7:
            prompt = "Press SPACE to start or ESC to quit..."
            display.draw_text(center_x, center_y + 11, prompt, True, 
                            Colors.BOLD + Colors.BRIGHT_WHITE)
        
        display.present()
        time.sleep(1/20)  # 20 FPS
        
        # Check for input
        key = input_handler.get_key()
        if key in ['space', 'up']:
            break
        elif key in ['escape', 'q']:
            display.cleanup()
            input_handler.disable_raw_mode()
            show_exit_screen(display, "Thanks for checking out T-Rex Runner!")
            sys.exit(0)

def show_error_screen(display: Display, message: str):
    """Show modern error screen"""
    from game.utils.display import Colors
    
    display.clear()
    center_x = display.width // 2
    center_y = display.height // 2
    
    # Error border
    for y in range(center_y - 3, center_y + 4):
        for x in range(center_x - 25, center_x + 26):
            if (0 <= x < display.width and 0 <= y < display.height and
                (x == center_x - 25 or x == center_x + 25 or 
                 y == center_y - 3 or y == center_y + 3)):
                display.draw_char(x, y, "█", Colors.BRIGHT_RED)
    
    # Error message
    display.draw_text(center_x, center_y - 1, "❌ ERROR", True, Colors.BOLD + Colors.BRIGHT_RED)
    display.draw_text(center_x, center_y, message, True, Colors.WHITE)
    display.draw_text(center_x, center_y + 2, "Press any key to exit...", True, Colors.BRIGHT_YELLOW)
    
    display.present()
    input("") # Wait for any key

def show_exit_screen(display: Display, message: str):
    """Show modern exit screen"""
    from game.utils.display import Colors
    
    display.clear()
    center_x = display.width // 2
    center_y = display.height // 2
    
    # Exit message
    display.draw_text(center_x, center_y - 1, "👋 GOODBYE!", True, Colors.BOLD + Colors.BRIGHT_CYAN)
    display.draw_text(center_x, center_y, message, True, Colors.WHITE)
    display.draw_text(center_x, center_y + 2, "🦕 Thanks for playing! 🦖", True, Colors.BRIGHT_GREEN)
    
    display.present()
    time.sleep(2)

def run_game_loop(game: GameEngine, input_handler: InputHandler, display: Display):
    """
    Enhanced game loop with modern UI and smooth animations
    
    Args:
        game: Game engine instance
        input_handler: Input handler
        display: Modern display system
    """
    from game.utils.display import Colors
    
    # Initialize game components
    game.set_input_handler(input_handler)
    game.set_display(display)
    
    # Game timing for smooth 20 FPS
    target_fps = 20
    frame_time = 1.0 / target_fps
    
    try:
        # Start the game with modern intro
        game.start()
        show_game_start_animation(display)
        
        while game.running:
            frame_start = time.time()
            
            # Handle input with enhanced feedback
            key = input_handler.get_key()
            if key:
                if key in ['escape', 'q']:
                    if show_quit_confirmation(display, input_handler):
                        game.stop()
                        break
                elif key == 'p':
                    game.toggle_pause()
                elif key in ['space', 'up']:
                    if game.game_over:
                        game.restart()
                        show_restart_animation(display)
                    else:
                        player = game.player
                        if player and player.jump():
                            # Visual feedback for successful jump
                            pass
                elif key in ['down', 's']:
                    player = game.player
                    if player:
                        player.duck()
            
            # Update game state
            if not game.paused:
                game.update()
            
            # Modern rendering pipeline
            display.clear()
            
            # Draw layered background
            display.draw_clouds()
            
            # Draw modern ground
            ground_y = 18
            display.draw_ground(ground_y)
            
            # Draw game objects with enhanced visuals
            game.render()
            
            # Modern HUD with stats
            render_modern_hud(display, game)
            
            # Handle special screens
            if game.paused and not game.game_over:
                display.draw_pause_screen()
            elif game.game_over:
                render_game_over_screen(display, game)
            
            display.present()
            
            # Precise frame timing
            frame_end = time.time()
            elapsed = frame_end - frame_start
            sleep_time = max(0, frame_time - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    except KeyboardInterrupt:
        game.stop()

def show_game_start_animation(display: Display):
    """Show modern game start animation"""
    from game.utils.display import Colors
    
    for frame in range(30):  # 1.5 second animation
        display.clear()
        
        center_x = display.width // 2
        center_y = display.height // 2
        
        # Countdown effect
        countdown = ["🎮", "3", "2", "1", "GO!"]
        if frame < len(countdown) * 6:
            current_text = countdown[frame // 6]
            size_effect = "█" if frame % 6 < 3 else ""
            
            # Color progression
            colors = [Colors.BRIGHT_RED, Colors.BRIGHT_YELLOW, Colors.BRIGHT_GREEN, Colors.BRIGHT_CYAN, Colors.BRIGHT_MAGENTA]
            color = colors[frame // 6] if frame // 6 < len(colors) else Colors.BRIGHT_WHITE
            
            display.draw_text(center_x, center_y, f"{size_effect}{current_text}{size_effect}", True, Colors.BOLD + color)
        
        display.present()
        time.sleep(1/20)

def show_restart_animation(display: Display):
    """Show quick restart animation"""
    from game.utils.display import Colors
    
    # Quick flash effect
    display.draw_text(display.width // 2, display.height // 2, "🔄 RESTARTING...", True, Colors.BOLD + Colors.BRIGHT_CYAN)
    display.present()
    time.sleep(0.3)

def show_quit_confirmation(display: Display, input_handler: InputHandler) -> bool:
    """Show modern quit confirmation dialog"""
    from game.utils.display import Colors
    
    # Save current screen
    original_buffer = [row[:] for row in display._buffer]
    original_color_buffer = [row[:] for row in display._color_buffer]
    
    center_x = display.width // 2
    center_y = display.height // 2
    
    # Draw confirmation dialog
    for y in range(center_y - 3, center_y + 4):
        for x in range(center_x - 15, center_x + 16):
            if 0 <= x < display.width and 0 <= y < display.height:
                if (x == center_x - 15 or x == center_x + 15 or 
                    y == center_y - 3 or y == center_y + 3):
                    display.draw_char(x, y, "█", Colors.BRIGHT_YELLOW)
                else:
                    display.draw_char(x, y, " ", Colors.BG_BLACK)
    
    display.draw_text(center_x, center_y - 1, "⚠️  QUIT GAME?", True, Colors.BOLD + Colors.BRIGHT_RED)
    display.draw_text(center_x, center_y + 1, "Y = Yes    N = No", True, Colors.BRIGHT_WHITE)
    display.present()
    
    # Wait for confirmation
    while True:
        key = input_handler.get_key()
        if key in ['y', 'Y']:
            return True
        elif key in ['n', 'N', 'escape']:
            # Restore screen
            display._buffer = original_buffer
            display._color_buffer = original_color_buffer
            display.present()
            return False
        time.sleep(0.05)

def render_modern_hud(display: Display, game: GameEngine):
    """Render modern HUD with enhanced visuals"""
    stats = game.get_game_stats() if hasattr(game, 'get_game_stats') else {}
    score = getattr(game, 'score', 0)
    high_score = getattr(game, 'high_score', 0)
    level = stats.get('level', 1)
    speed = stats.get('speed_multiplier', 1.0)
    
    display.draw_enhanced_score(score, high_score, level, speed)

def render_game_over_screen(display: Display, game: GameEngine):
    """Render modern game over screen"""
    stats = game.get_game_stats() if hasattr(game, 'get_game_stats') else {}
    score = getattr(game, 'score', 0)
    high_score = getattr(game, 'high_score', 0)
    level = stats.get('level', 1)
    
    display.draw_game_over_screen(score, high_score, level)

if __name__ == "__main__":
    main()
