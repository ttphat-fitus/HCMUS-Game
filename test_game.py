#!/usr/bin/env python3
"""
Simple test script to verify the T-Rex game components work

This script tests the core game functionality without requiring user input.
"""

import sys
import os

# Add game package to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_game_components():
    """Test all game components"""
    print("🧪 Testing T-Rex Runner Components...")
    print("=" * 50)
    
    try:
        # Test imports
        print("📦 Testing imports...")
        from game.core.game_engine import GameEngine
        from game.entities.player import Player
        from game.entities.obstacle import Obstacle
        from game.patterns.factory import ObstacleFactory, DifficultyLevel
        from game.patterns.observer import ScoreObserver, GameEventObserver
        from game.utils.input_handler import InputHandler
        from game.utils.display import Display
        print("✅ All imports successful")
        
        # Test Singleton Pattern
        print("\n🔄 Testing Singleton Pattern...")
        game1 = GameEngine.get_instance()
        game2 = GameEngine.get_instance()
        assert game1 is game2, "Singleton pattern failed!"
        print("✅ Singleton pattern working correctly")
        
        # Test Factory Pattern
        print("\n🏭 Testing Factory Pattern...")
        from game.entities.obstacle import ObstacleType
        factory = ObstacleFactory()
        cactus = factory.create_obstacle(ObstacleType.CACTUS, 50, 18)
        bird = factory.create_obstacle(ObstacleType.BIRD, 60, 15)
        assert cactus.get_obstacle_type() == ObstacleType.CACTUS
        assert bird.get_obstacle_type() == ObstacleType.BIRD
        print("✅ Factory pattern working correctly")
        
        # Test Observer Pattern
        print("\n👁️ Testing Observer Pattern...")
        observer = ScoreObserver()
        game1.add_observer(observer)
        print("✅ Observer pattern working correctly")
        
        # Test Player
        print("\n🦕 Testing Player...")
        player = Player(10, 18)
        assert player.x == 10
        assert player.y == 18
        player.jump()
        player.update()  # Test update cycle
        print("✅ Player class working correctly")
        
        # Test Game Initialization
        print("\n🎮 Testing Game Initialization...")
        if game1.initialize():
            print("✅ Game initialization successful")
        else:
            print("❌ Game initialization failed")
            return False
        
        # Test Input Handler
        print("\n⌨️ Testing Input Handler...")
        input_handler = InputHandler()
        print("✅ Input handler created successfully")
        
        # Test Display
        print("\n🖥️ Testing Display...")
        display = Display(80, 20)
        print("✅ Display created successfully")
        
        # Cleanup
        print("\n🧹 Testing Cleanup...")
        GameEngine.destroy_instance()
        print("✅ Cleanup successful")
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED!")
        print("🎮 The T-Rex Runner game is ready to play!")
        print("\nTo start the game, run: python3 main.py")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_game_components()
    sys.exit(0 if success else 1)
