import pygame
import sys
import json
import os
from .dino import Dino
from .obstacles import ObstacleManager
from .background import Background
from .hud import HUD
from .game_over import GameOver

class MainGame:
    """Main game class managing the entire game state"""
    
    # Constants from original Godot code
    DINO_START_POS = (150, 485)
    START_SPEED = 200.0  # Higher starting speed
    MAX_SPEED = 1000.0  # Much higher max speed
    SPEED_MODIFIER = 50  # Lower modifier means faster speed gain
    SCORE_MODIFIER = 10
    MAX_DIFFICULTY = 2
    
    def __init__(self, screen_width=1152, screen_height=648):
        pygame.init()
        pygame.mixer.init()
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Dino Run - Python Version")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_running = False
        
        # Game variables
        self.score = 0
        self.high_score = self.load_high_score()
        self.speed = self.START_SPEED
        self.difficulty = 0
        self.camera_x = 0
        
        # Initialize game objects
        self.background = Background(screen_width, screen_height)
        self.ground_y = self.background.get_ground_y()
        
        # Create dino and position it properly on the ground (a bit lower)
        self.ground_offset = 40
        self.dino = Dino(self.DINO_START_POS[0], self.ground_y - self.ground_offset)
        # Set a ground offset so the dino stays lower
        self.obstacle_manager = ObstacleManager(screen_width, self.ground_y)
        self.hud = HUD(screen_width, screen_height)
        self.game_over_screen = GameOver(screen_width, screen_height)
        
        # Initialize new game
        self.new_game()
        
    def load_high_score(self):
        """Load high score from file"""
        try:
            if os.path.exists("high_score.json"):
                with open("high_score.json", "r") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return 0
        
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open("high_score.json", "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except Exception as e:
            print(f"Error saving high score: {e}")
            
    def new_game(self):
        """Reset the game for a new run"""
        # Reset variables
        self.score = 0
        self.game_running = False
        self.difficulty = 0
        self.speed = self.START_SPEED
        self.camera_x = 0
        
        # Reset game objects
        self.dino.position.x = self.DINO_START_POS[0]
        self.dino.position.y = self.ground_y + self.ground_offset - self.dino.rect.height // 2  # Use consistent offset
        self.dino.velocity.x = 0
        self.dino.velocity.y = 0
        self.dino.state = "idle"
        
        self.obstacle_manager.clear()
        self.hud.show_start_label_again()
        self.game_over_screen.hide()
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if not self.game_running and not self.game_over_screen.visible:
                        self.game_running = True
                        self.hud.hide_start_label()
                    elif self.game_over_screen.visible:
                        self.new_game()
                        
    def update(self, delta_time):
        """Update game logic"""
        if self.game_running:
            # Update speed and difficulty (matching original logic)
            self.speed = self.START_SPEED + self.score / self.SPEED_MODIFIER
            if self.speed > self.MAX_SPEED:
                self.speed = self.MAX_SPEED
                
            self.difficulty = int(self.score / self.SPEED_MODIFIER)
            if self.difficulty > self.MAX_DIFFICULTY:
                self.difficulty = self.MAX_DIFFICULTY
                
            # Update camera position (following dino)
            self.camera_x = self.dino.position.x - 200
            
            # Update score
            self.score += self.speed * delta_time
            
            # Update game objects
            self.dino.update(delta_time, self.game_running, self.ground_y + self.ground_offset)
            self.background.update(delta_time, self.speed)
            self.obstacle_manager.update(delta_time, self.speed, self.score, self.difficulty, self.camera_x)
            
            # Check collisions
            if self.obstacle_manager.check_collision(self.dino):
                self.game_over()
        else:
            # Update dino in idle state
            self.dino.update(delta_time, self.game_running, self.ground_y + self.ground_offset)
            
    def game_over(self):
        """Handle game over"""
        self.check_high_score()
        self.game_running = False
        self.game_over_screen.show()
        
    def check_high_score(self):
        """Check and update high score"""
        if self.score > self.high_score:
            self.high_score = int(self.score)
            self.save_high_score()
            
    def draw(self):
        """Draw all game elements"""
        self.screen.fill((135, 206, 235))  # Sky blue background
        
        # Draw game objects
        self.background.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.dino.draw(self.screen)
        
        # Draw UI
        self.hud.draw(self.screen, int(self.score), self.high_score, self.game_running)
        self.game_over_screen.draw(self.screen, int(self.score), self.high_score)
        
        pygame.display.flip()
        
    def run(self):
        """Main game loop"""
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0  # Convert to seconds
            
            self.handle_events()
            self.update(delta_time)
            self.draw()
            
        pygame.quit()
        sys.exit()
