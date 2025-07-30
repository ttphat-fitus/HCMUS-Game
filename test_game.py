#!/usr/bin/env python3
"""
Simple test script to verify the game can start without errors.
This will initialize the game and run for a few seconds, then exit.
"""

import pygame
import sys
import os
import time

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scenes.main_game import MainGame

def test_game():
    """Test game initialization and basic functionality"""
    print("Testing game initialization...")
    
    try:
        # Initialize pygame
        pygame.init()
        
        # Create game instance
        game = MainGame(800, 600)  # Smaller window for testing
        print("✓ Game created successfully")
        
        # Test basic game loop for a few frames
        print("Testing game loop...")
        for i in range(60):  # Test 60 frames (1 second at 60 FPS)
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                    
            # Update game
            game.update(1/60.0)  # Simulate 60 FPS
            
            # Draw game
            game.draw()
            
            if i % 30 == 0:  # Print progress every half second
                print(f"Frame {i}/60...")
                
        print("✓ Game loop test completed")
        
        # Test starting the game
        print("Testing game start...")
        game.game_running = True
        game.hud.hide_start_label()
        
        # Run a few more frames with game running
        for i in range(30):
            game.update(1/60.0)
            game.draw()
            
        print("✓ Game start test completed")
        
        pygame.quit()
        print("\n🎮 All tests passed! Game is ready to run.")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_game()
    if not success:
        print("\n❌ Tests failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("\nTo run the full game, use: python main.py")
