import pygame
import sys
import json
import os
import random
from .dino import Dino
from .obstacles import ObstacleManager
from .tokens import TokenManager
from .background import Background
from .hud import HUD
from .game_over import GameOver
from .path_utils import get_resource_path, get_save_path

class MainGame:
    """Main game class managing the entire game state"""
    
    # Constants for game settings
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
        pygame.display.set_caption("Dino Run")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_running = False
        
        # Game variables
        self.score = 0
        self.token_score = 0  # Separate score for tokens collected
        self.high_score = self.load_high_score()
        self.speed = self.START_SPEED
        self.base_speed = self.START_SPEED  # Store original speed for powerup calculations
        self.difficulty = 0
        self.camera_x = 0
        
        # Powerup effects
        self.active_powerups = {}  # Dictionary to track active powerups
        self.coin_multiplier = 1  # Multiplier for coin collection (doublegold effect)
        
        # Initialize game objects
        self.background = Background(screen_width, screen_height)
        self.ground_y = self.background.get_ground_y()
        
        # Create dino and position it properly on the ground (a bit lower)
        self.ground_offset = 40
        self.dino = Dino(self.DINO_START_POS[0], self.ground_y - self.ground_offset)
        # Set a ground offset so the dino stays lower
        self.obstacle_manager = ObstacleManager(screen_width, self.ground_y)
        self.token_manager = TokenManager(screen_width, self.ground_y)
        self.hud = HUD(screen_width, screen_height)
        self.game_over_screen = GameOver(screen_width, screen_height)
        
        # Load sounds
        self.bg_music = None
        self.game_over_sounds = []
        self.load_sounds()
        
        # Initialize new game
        self.new_game()
        
    def load_high_score(self):
        """Load high score from file"""
        try:
            score_file = get_save_path("high_score.json")
            if os.path.exists(score_file):
                with open(score_file, "r") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return 0
        
    def save_high_score(self):
        """Save high score to file"""
        try:
            score_file = get_save_path("high_score.json")
            with open(score_file, "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except Exception as e:
            print(f"Error saving high score: {e}")
    
    def load_sounds(self):
        """Load game sounds"""
        try:
            # Load background music
            self.bg_music = get_resource_path("assets/sound/bg.mp3")
            
            # Load game over sounds
            game_over_files = [
                get_resource_path("assets/sound/haha1.mp3"), 
                get_resource_path("assets/sound/haha2.mp3"), 
                get_resource_path("assets/sound/haha3.mp3")
            ]
            for sound_file in game_over_files:
                try:
                    sound = pygame.mixer.Sound(sound_file)
                    self.game_over_sounds.append(sound)
                except pygame.error as e:
                    print(f"Warning: Could not load {sound_file}: {e}")
            
            print(f"Loaded {len(self.game_over_sounds)} game over sounds")
            
        except Exception as e:
            print(f"Error loading sounds: {e}")
    
    def play_background_music(self):
        """Start playing background music in loop"""
        try:
            if self.bg_music:
                pygame.mixer.music.load(self.bg_music)
                pygame.mixer.music.set_volume(0.3)  # Set volume to 30%
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                print("Background music started")
        except pygame.error as e:
            print(f"Error playing background music: {e}")
    
    def stop_background_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
    
    def play_game_over_sound(self):
        """Play a random game over sound in loop"""
        try:
            if self.game_over_sounds:
                # Stop any currently playing game over sound
                pygame.mixer.stop()
                # Choose a random game over sound
                sound = random.choice(self.game_over_sounds)
                sound.set_volume(0.5)  # Set volume to 50%
                sound.play(-1)  # -1 means loop indefinitely
                print("Game over sound started")
        except Exception as e:
            print(f"Error playing game over sound: {e}")
    
    def stop_game_over_sound(self):
        """Stop game over sound"""
        pygame.mixer.stop()
            
    def new_game(self):
        """Reset the game for a new run"""
        # Reset variables
        self.score = 0
        self.token_score = 0
        self.game_running = False
        self.difficulty = 0
        self.speed = self.START_SPEED
        self.base_speed = self.START_SPEED
        self.camera_x = 0
        
        # Reset powerups
        self.active_powerups.clear()
        self.coin_multiplier = 1
        
        # Reset game objects
        self.dino.position.x = self.DINO_START_POS[0]
        self.dino.position.y = self.ground_y + self.ground_offset - self.dino.rect.height // 2  # Use consistent offset
        self.dino.velocity.x = 0
        self.dino.velocity.y = 0
        self.dino.state = "idle"
        
        self.obstacle_manager.clear()
        self.token_manager.clear()
        self.hud.show_start_label_again()
        self.game_over_screen.hide()
        
        # Stop any game over sounds and start background music
        self.stop_game_over_sound()
        self.play_background_music()
        
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
            # Update powerups first
            self.update_powerups(delta_time)
            
            # Calculate base speed for scoring (always normal speed)
            self.base_speed = self.START_SPEED + self.score / self.SPEED_MODIFIER
            if self.base_speed > self.MAX_SPEED:
                self.base_speed = self.MAX_SPEED
                
            # Movement speed (can be affected by halfspeed powerup)
            if "halfspeed" in self.active_powerups:
                self.speed = self.base_speed * 0.7 # Slower movement for obstacles/background
            else:
                self.speed = self.base_speed
                
            self.difficulty = int(self.score / self.SPEED_MODIFIER)
            if self.difficulty > self.MAX_DIFFICULTY:
                self.difficulty = self.MAX_DIFFICULTY
                
            # Update camera position (following dino)
            self.camera_x = self.dino.position.x - 200
            
            # Update score (always use base_speed, not affected by halfspeed powerup)
            self.score += self.base_speed * delta_time
            
            # Update game objects
            self.dino.update(delta_time, self.game_running, self.ground_y + self.ground_offset, self.active_powerups, self.score)
            self.background.update(delta_time, self.speed)
            self.obstacle_manager.update(delta_time, self.speed, self.score, self.difficulty, self.camera_x)
            self.token_manager.update(delta_time, self.speed, self.score, self.difficulty, self.camera_x)
            
            # Check token collisions (collect tokens and powerups)
            coin_value, powerup_effects = self.token_manager.check_collision(self.dino)
            if coin_value > 0:
                # Apply coin multiplier from doublegold powerup
                actual_coins = coin_value * self.coin_multiplier
                self.token_score += actual_coins
                if self.coin_multiplier > 1:
                    print(f"Doublegold active! Collected {coin_value} coin(s) -> {actual_coins} coins!")
                # Play collection sound here if you have one
                # pygame.mixer.Sound("assets/sound/collect.wav").play()
            
            # Handle powerup effects
            for powerup in powerup_effects:
                self.activate_powerup(powerup["effect"], powerup["duration"], powerup["type"])
            
            # Check obstacle collisions (game over)
            if self.obstacle_manager.check_collision(self.dino):
                self.game_over()
        else:
            # Update dino in idle state
            self.dino.update(delta_time, self.game_running, self.ground_y + self.ground_offset, self.active_powerups, self.score)
            
    def game_over(self):
        """Handle game over"""
        self.check_high_score()
        self.game_running = False
        self.game_over_screen.show()
        
        # Stop background music and play game over sound
        self.stop_background_music()
        self.play_game_over_sound()
        
    def check_high_score(self):
        """Check and update high score"""
        if self.score > self.high_score:
            self.high_score = int(self.score)
            self.save_high_score()
    
    def update_powerups(self, delta_time):
        """Update active powerup timers"""
        expired_powerups = []
        
        for powerup_name, remaining_time in self.active_powerups.items():
            remaining_time -= delta_time
            if remaining_time <= 0:
                expired_powerups.append(powerup_name)
            else:
                self.active_powerups[powerup_name] = remaining_time
        
        # Remove expired powerups and reset their effects
        for powerup_name in expired_powerups:
            del self.active_powerups[powerup_name]
            if powerup_name == "doublegold":
                self.coin_multiplier = 1
                print("Doublegold powerup expired!")
            elif powerup_name == "halfspeed":
                print("Halfspeed powerup expired!")
    
    def activate_powerup(self, effect, duration, powerup_type):
        """Activate a powerup effect"""
        if effect == "halfspeed":
            self.active_powerups["halfspeed"] = duration
            print(f"Halfspeed activated for {duration} seconds! (Slower gameplay, same scoring)")
        elif effect == "doublegold":
            self.active_powerups["doublegold"] = duration
            self.coin_multiplier = 2
            print(f"Doublegold activated for {duration} seconds!")
            
    def draw(self):
        """Draw all game elements"""
        self.screen.fill((135, 206, 235))  # Sky blue background
        
        # Draw game objects
        self.background.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.token_manager.draw(self.screen)
        self.dino.draw(self.screen)
        
        # Draw UI
        self.hud.draw(self.screen, int(self.score), self.high_score, self.game_running, self.token_score, self.active_powerups)
        self.game_over_screen.draw(self.screen, int(self.score), self.high_score)
        
        pygame.display.flip()
        
    def run(self):
        """Main game loop"""
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0  # Convert to seconds
            
            self.handle_events()
            self.update(delta_time)
            self.draw()
            
        # Stop all sounds before quitting
        self.stop_background_music()
        self.stop_game_over_sound()
        pygame.quit()
        sys.exit()
