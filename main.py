#!/usr/bin/env python3
"""
Dino Run Game - Python Version
A faithful recreation of the classic dinosaur running game using Pygame.

Controls:
- SPACE: Jump / Start Game
- DOWN ARROW: Duck (while running)
- ESC: Quit Game

This is a Python remake of the original Godot version.
"""

import pygame
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scenes.main_game import MainGame

def main():
    """Main entry point for the game"""
    try:
        # Check if pygame is available
        pygame.init()
        
        # Create and run the game
        game = MainGame()
        game.run()
        
    except ImportError:
        print("Error: Pygame is not installed!")
        print("Please install pygame using: pip install pygame")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting game: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
