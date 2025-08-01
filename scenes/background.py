import pygame

class Background:
    """Manages the parallax scrolling background"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Load background layers
        self.layers = []
        self.layer_speeds = [1.5, 1.6, 1.7, 1.8, 1.9]  # Different scroll speeds for parallax
        
        # Load parallax layers
        for i in range(1, 6):
            try:
                layer_image = pygame.image.load(f"assets/img/background/plx-{i}.png").convert_alpha()
                # Scale to screen height
                scale_factor = screen_height / layer_image.get_height()
                width = int(layer_image.get_width() * scale_factor)
                height = int(layer_image.get_height() * scale_factor)
                layer_image = pygame.transform.scale(layer_image, (width, height))
                self.layers.append(layer_image)
            except pygame.error:
                # Create a fallback colored layer if image doesn't load
                fallback = pygame.Surface((screen_width, screen_height))
                fallback.fill((100 + i * 20, 150 + i * 10, 200 + i * 5))
                self.layers.append(fallback)
        
        # Ground
        self.ground_image = None
        try:
            self.ground_image = pygame.image.load("assets/img/background/ground.png").convert_alpha()
        except pygame.error:
            # Create fallback ground
            self.ground_image = pygame.Surface((screen_width, 100))
            self.ground_image.fill((139, 69, 19))  # Brown color
            
        self.ground_y = screen_height - self.ground_image.get_height()
        
        # Track positions for infinite scrolling
        self.layer_positions = [0] * len(self.layers)
        self.ground_positions = [0, screen_width]
        self.ground_speed = 3.0  # Ground moves faster than other layers
        
    def update(self, delta_time, speed):
        """Update background scrolling"""
        # Update parallax layers
        for i, layer_speed in enumerate(self.layer_speeds):
            self.layer_positions[i] -= speed * layer_speed * delta_time
            # Reset position for infinite scrolling
            if self.layer_positions[i] <= -self.layers[i].get_width():
                self.layer_positions[i] = 0
                
        # Update ground with increased speed
        for i in range(len(self.ground_positions)):
            self.ground_positions[i] -= speed * self.ground_speed * delta_time
            
        # Reset ground positions for infinite scrolling
        if self.ground_positions[0] <= -self.ground_image.get_width():
            self.ground_positions[0] = self.ground_positions[1] + self.ground_image.get_width()
        if self.ground_positions[1] <= -self.ground_image.get_width():
            self.ground_positions[1] = self.ground_positions[0] + self.ground_image.get_width()
            
    def draw(self, screen):
        """Draw the background"""
        # Draw parallax layers
        for i, layer in enumerate(self.layers):
            x = self.layer_positions[i]
            # Draw multiple copies to ensure full coverage
            while x < self.screen_width:
                screen.blit(layer, (x, 0))
                x += layer.get_width()
                
        # Draw ground
        for ground_x in self.ground_positions:
            screen.blit(self.ground_image, (ground_x, self.ground_y))
            
    def get_ground_y(self):
        """Get the Y position of the ground surface"""
        return self.ground_y
