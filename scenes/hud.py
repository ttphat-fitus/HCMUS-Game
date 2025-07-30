import pygame

class HUD:
    """Heads-up display for showing score and UI elements"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Load font
        self.font = None
        self.large_font = None
        try:
            self.font = pygame.font.Font("assets/fonts/retro.ttf", 24)
            self.large_font = pygame.font.Font("assets/fonts/retro.ttf", 48)
        except (pygame.error, FileNotFoundError):
            self.font = pygame.font.Font(None, 24)
            self.large_font = pygame.font.Font(None, 48)
            
        # Colors
        self.text_color = (255, 255, 255)  # White
        self.shadow_color = (0, 0, 0)     # Black shadow
        
        # UI state
        self.show_start_label = True
        
    def draw_text_with_shadow(self, screen, text, font, x, y, color=None, shadow_offset=2):
        """Draw text with a shadow effect"""
        if color is None:
            color = self.text_color
            
        # Draw shadow
        shadow_surface = font.render(text, True, self.shadow_color)
        screen.blit(shadow_surface, (x + shadow_offset, y + shadow_offset))
        
        # Draw main text
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
        
        return text_surface.get_width(), text_surface.get_height()
        
    def draw(self, screen, score, high_score, game_running):
        """Draw the HUD elements"""
        # Score
        score_text = f"SCORE: {score // 10}"  # Match original SCORE_MODIFIER
        self.draw_text_with_shadow(screen, score_text, self.font, 20, 20)
        
        # High Score
        high_score_text = f"HIGH SCORE: {high_score // 10}"
        self.draw_text_with_shadow(screen, high_score_text, self.font, 20, 50)
        
        # Start label
        if self.show_start_label and not game_running:
            start_text = "PRESS SPACE TO START"
            text_width, text_height = self.font.size(start_text)
            x = (self.screen_width - text_width) // 2
            y = (self.screen_height - text_height) // 2
            self.draw_text_with_shadow(screen, start_text, self.large_font, x, y)
            
            # Instructions
            instructions = [
                "SPACE - Jump",
                "DOWN ARROW - Duck",
                "ESC - Quit"
            ]
            for i, instruction in enumerate(instructions):
                inst_width, inst_height = self.font.size(instruction)
                inst_x = (self.screen_width - inst_width) // 2
                inst_y = y + text_height + 40 + (i * 30)
                self.draw_text_with_shadow(screen, instruction, self.font, inst_x, inst_y)
                
    def hide_start_label(self):
        """Hide the start label when game begins"""
        self.show_start_label = False
        
    def show_start_label_again(self):
        """Show start label again for new game"""
        self.show_start_label = True
