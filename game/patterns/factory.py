"""
Factory Pattern Implementation for Obstacle Creation

This module demonstrates the Factory Pattern, which is ideal for creating
different types of obstacles dynamically based on game requirements.

DESIGN PATTERN JUSTIFICATION:
The Factory Pattern is perfect for this T-Rex Runner game because:

1. **Multiple Product Types**: We have different obstacle types (Cactus, Bird, Rock)
   that share a common interface but have different creation parameters.

2. **Dynamic Creation**: Obstacles need to be created randomly during gameplay
   with varying types, positions, and properties.

3. **Encapsulation of Creation Logic**: The factory hides the complexity of
   determining which obstacle type to create based on game state.

4. **Easy Extensibility**: Adding new obstacle types requires minimal changes
   to existing code - just add the new class and update the factory.

5. **Parameter Management**: Different obstacles need different initialization
   parameters (ground position for cacti, flying height for birds).
"""

import random
from typing import List, Type, Optional
from enum import Enum
from game.entities.obstacle import Obstacle, Cactus, Bird, Rock, ObstacleType

class DifficultyLevel(Enum):
    """Game difficulty levels affecting obstacle creation"""
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXTREME = 4

class ObstacleFactory:
    """
    Factory class for creating obstacles
    
    Demonstrates the Factory Pattern by providing a centralized way to create
    different types of obstacles based on game parameters.
    
    The factory encapsulates:
    - Obstacle type selection logic
    - Parameter calculation for different obstacle types
    - Difficulty-based creation probabilities
    - Random variation in obstacle properties
    """
    
    # Obstacle type probabilities for different difficulty levels
    _DIFFICULTY_PROBABILITIES = {
        DifficultyLevel.EASY: {
            ObstacleType.CACTUS: 0.7,
            ObstacleType.BIRD: 0.2,
            ObstacleType.ROCK: 0.1
        },
        DifficultyLevel.MEDIUM: {
            ObstacleType.CACTUS: 0.5,
            ObstacleType.BIRD: 0.3,
            ObstacleType.ROCK: 0.2
        },
        DifficultyLevel.HARD: {
            ObstacleType.CACTUS: 0.4,
            ObstacleType.BIRD: 0.4,
            ObstacleType.ROCK: 0.2
        },
        DifficultyLevel.EXTREME: {
            ObstacleType.CACTUS: 0.3,
            ObstacleType.BIRD: 0.5,
            ObstacleType.ROCK: 0.2
        }
    }
    
    # Flying heights for birds at different difficulties
    _BIRD_HEIGHTS = {
        DifficultyLevel.EASY: [3, 4],
        DifficultyLevel.MEDIUM: [2, 3, 4],
        DifficultyLevel.HARD: [2, 3, 4, 5],
        DifficultyLevel.EXTREME: [1, 2, 3, 4, 5]
    }
    
    @classmethod
    def create_obstacle(cls, 
                       obstacle_type: ObstacleType, 
                       x: int, 
                       ground_y: int, 
                       difficulty: DifficultyLevel = DifficultyLevel.EASY,
                       **kwargs) -> Obstacle:
        """
        Create a specific type of obstacle
        
        Args:
            obstacle_type: Type of obstacle to create
            x: X position for the obstacle
            ground_y: Ground level Y coordinate
            difficulty: Current game difficulty
            **kwargs: Additional parameters for specific obstacle types
            
        Returns:
            Created obstacle instance
            
        Raises:
            ValueError: If obstacle_type is not supported
        """
        if obstacle_type == ObstacleType.CACTUS:
            return cls._create_cactus(x, ground_y, difficulty, **kwargs)
        elif obstacle_type == ObstacleType.BIRD:
            return cls._create_bird(x, ground_y, difficulty, **kwargs)
        elif obstacle_type == ObstacleType.ROCK:
            return cls._create_rock(x, ground_y, difficulty, **kwargs)
        else:
            raise ValueError(f"Unsupported obstacle type: {obstacle_type}")
    
    @classmethod
    def create_random_obstacle(cls, 
                              x: int, 
                              ground_y: int, 
                              difficulty: DifficultyLevel = DifficultyLevel.EASY) -> Obstacle:
        """
        Create a random obstacle based on difficulty probabilities
        
        Args:
            x: X position for the obstacle
            ground_y: Ground level Y coordinate
            difficulty: Current game difficulty level
            
        Returns:
            Randomly created obstacle
        """
        # Get probability distribution for current difficulty
        probabilities = cls._DIFFICULTY_PROBABILITIES[difficulty]
        
        # Select obstacle type based on probabilities
        obstacle_type = cls._weighted_random_choice(probabilities)
        
        # Create the selected obstacle type
        return cls.create_obstacle(obstacle_type, x, ground_y, difficulty)
    
    @classmethod
    def create_obstacle_sequence(cls, 
                                x: int, 
                                ground_y: int, 
                                difficulty: DifficultyLevel,
                                count: int = 3) -> List[Obstacle]:
        """
        Create a sequence of obstacles for challenging patterns
        
        Args:
            x: Starting X position
            ground_y: Ground level Y coordinate
            difficulty: Current difficulty level
            count: Number of obstacles in sequence
            
        Returns:
            List of obstacles forming a challenging pattern
        """
        obstacles = []
        spacing = 3  # Spacing between obstacles in sequence
        
        for i in range(count):
            obstacle_x = x + (i * spacing)
            
            # Create varied obstacles in sequence
            if i == 0:
                # Start with ground obstacle
                obstacle = cls.create_obstacle(ObstacleType.CACTUS, obstacle_x, ground_y, difficulty)
            elif i == 1:
                # Follow with flying obstacle
                obstacle = cls.create_obstacle(ObstacleType.BIRD, obstacle_x, ground_y, difficulty)
            else:
                # Random for remaining
                obstacle = cls.create_random_obstacle(obstacle_x, ground_y, difficulty)
            
            obstacles.append(obstacle)
        
        return obstacles
    
    @classmethod
    def _create_cactus(cls, 
                      x: int, 
                      ground_y: int, 
                      difficulty: DifficultyLevel,
                      **kwargs) -> Cactus:
        """Create a cactus obstacle with random variation"""
        cactus_type = kwargs.get('cactus_type', random.randint(0, 2))
        cactus = Cactus(x, ground_y - 1, cactus_type)  # Position above ground
        
        # Adjust speed based on difficulty
        speed = 1 + (difficulty.value - 1) * 0.5
        cactus.set_speed(int(speed))
        
        return cactus
    
    @classmethod
    def _create_bird(cls, 
                    x: int, 
                    ground_y: int, 
                    difficulty: DifficultyLevel,
                    **kwargs) -> Bird:
        """Create a bird obstacle with random flying height"""
        # Select random flying height based on difficulty
        heights = cls._BIRD_HEIGHTS[difficulty]
        flying_height = random.choice(heights)
        bird_y = ground_y - flying_height
        
        bird_type = kwargs.get('bird_type', random.randint(0, 2))
        bird = Bird(x, bird_y, bird_type)
        
        # Adjust speed based on difficulty
        speed = 1 + (difficulty.value - 1) * 0.3
        bird.set_speed(int(speed))
        
        return bird
    
    @classmethod
    def _create_rock(cls, 
                    x: int, 
                    ground_y: int, 
                    difficulty: DifficultyLevel,
                    **kwargs) -> Rock:
        """Create a rock obstacle"""
        rock_type = kwargs.get('rock_type', random.randint(0, 2))
        rock = Rock(x, ground_y, rock_type)
        
        # Adjust speed based on difficulty
        speed = 1 + (difficulty.value - 1) * 0.4
        rock.set_speed(int(speed))
        
        return rock
    
    @classmethod
    def _weighted_random_choice(cls, probabilities: dict) -> ObstacleType:
        """
        Select a random obstacle type based on weighted probabilities
        
        Args:
            probabilities: Dictionary mapping obstacle types to probabilities
            
        Returns:
            Selected obstacle type
        """
        choices = list(probabilities.keys())
        weights = list(probabilities.values())
        
        return random.choices(choices, weights=weights)[0]
    
    @classmethod
    def get_obstacle_info(cls, obstacle_type: ObstacleType) -> dict:
        """
        Get information about a specific obstacle type
        
        Args:
            obstacle_type: The obstacle type to get info for
            
        Returns:
            Dictionary with obstacle information
        """
        info = {
            ObstacleType.CACTUS: {
                "name": "Cactus",
                "description": "Ground-based obstacle that must be jumped over",
                "difficulty": "Easy to Medium",
                "strategy": "Jump to avoid"
            },
            ObstacleType.BIRD: {
                "name": "Bird",
                "description": "Flying obstacle at various heights",
                "difficulty": "Medium to Hard",
                "strategy": "Duck under or jump over depending on height"
            },
            ObstacleType.ROCK: {
                "name": "Rock",
                "description": "Low ground obstacle",
                "difficulty": "Easy",
                "strategy": "Jump to clear"
            }
        }
        
        return info.get(obstacle_type, {"name": "Unknown", "description": "Unknown obstacle"})

# Factory Pattern Benefits:
# 1. Encapsulation: Creation logic is centralized and hidden
# 2. Flexibility: Easy to add new obstacle types without changing client code
# 3. Configuration: Difficulty-based creation with different parameters
# 4. Consistency: Ensures all obstacles are created properly
# 5. Testability: Easy to test creation logic in isolation
