import pygame
from .path_utils import get_resource_path

class GameOver:
    """Game over screen"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = False
        
        # Load font
        self.font = None
        self.large_font = None
        try:
            self.font = pygame.font.Font(get_resource_path("assets/fonts/retro.ttf"), 24)
            self.large_font = pygame.font.Font(get_resource_path("assets/fonts/retro.ttf"), 64)
        except (pygame.error, FileNotFoundError):
            self.font = pygame.font.Font(None, 24)
            self.large_font = pygame.font.Font(None, 64)
            
        # Colors
        self.text_color = (255, 255, 255)
        self.shadow_color = (0, 0, 0)
        self.background_color = (0, 0, 0, 128)  # Semi-transparent black
        
        # Create semi-transparent overlay
        self.overlay = pygame.Surface((screen_width, screen_height))
        self.overlay.set_alpha(128)
        self.overlay.fill((0, 0, 0))
        
    def show(self):
        """Show the game over screen"""
        self.visible = True
        
    def hide(self):
        """Hide the game over screen"""
        self.visible = False
        
    def draw_text_with_shadow(self, screen, text, font, x, y, color=None, shadow_offset=3):
        """Draw text with shadow effect"""
        if color is None:
            color = self.text_color
            
        # Draw shadow
        shadow_surface = font.render(text, True, self.shadow_color)
        screen.blit(shadow_surface, (x + shadow_offset, y + shadow_offset))
        
        # Draw main text
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
        
        return text_surface.get_width(), text_surface.get_height()
        
    def draw(self, screen, final_score, high_score):
        """Draw the game over screen"""
        if not self.visible:
            return
            
        # Draw overlay
        screen.blit(self.overlay, (0, 0))
        
        # Game Over text
        game_over_text = "GAME OVER"
        text_width, text_height = self.large_font.size(game_over_text)
        x = (self.screen_width - text_width) // 2
        y = self.screen_height // 2 - 100
        self.draw_text_with_shadow(screen, game_over_text, self.large_font, x, y)
        
        # Final score
        score_text = f"FINAL SCORE: {final_score // 10}"
        score_width, score_height = self.font.size(score_text)
        score_x = (self.screen_width - score_width) // 2
        score_y = y + text_height + 30
        self.draw_text_with_shadow(screen, score_text, self.font, score_x, score_y)
        
        # High score
        if final_score > high_score:
            high_score_text = "NEW HIGH SCORE!"
            hs_color = (255, 255, 0)  # Yellow for new high score
        else:
            high_score_text = f"HIGH SCORE: {high_score // 10}"
            hs_color = self.text_color
            
        hs_width, hs_height = self.font.size(high_score_text)
        hs_x = (self.screen_width - hs_width) // 2
        hs_y = score_y + score_height + 20
        self.draw_text_with_shadow(screen, high_score_text, self.font, hs_x, hs_y, hs_color)
        
        # Restart instruction
        restart_text = "PRESS SPACE TO RESTART"
        restart_width, restart_height = self.font.size(restart_text)
        restart_x = (self.screen_width - restart_width) // 2
        restart_y = hs_y + hs_height + 40
        self.draw_text_with_shadow(screen, restart_text, self.font, restart_x, restart_y)
        
        # Quit instruction
        quit_text = "PRESS ESC TO QUIT"
        quit_width, quit_height = self.font.size(quit_text)
        quit_x = (self.screen_width - quit_width) // 2
        quit_y = restart_y + restart_height + 20
        self.draw_text_with_shadow(screen, quit_text, self.font, quit_x, quit_y)
