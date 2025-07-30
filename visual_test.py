#!/usr/bin/env python3
"""
Visual test script to demonstrate the improved scaling and animations.
This will show the dino in different states and all obstacles with proper scaling.
"""

import pygame
import sys
import os
import time

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scenes.dino import Dino
from scenes.obstacles import Stump, Rock, Barrel, Bird
from scenes.background import Background

def visual_test():
    """Visual test for scaling and animations"""
    print("Starting visual test...")
    
    pygame.init()
    
    # Create a window
    screen_width, screen_height = 1000, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Dino Game - Scaling & Animation Test")
    clock = pygame.time.Clock()
    
    # Create background
    background = Background(screen_width, screen_height)
    ground_y = background.get_ground_y()
    
    # Create dino
    dino = Dino(200, ground_y)
    
    # Create obstacles for testing
    obstacles = [
        Stump(400, ground_y),
        Rock(500, ground_y),
        Barrel(600, ground_y),
        Bird(700, 300),
        Bird(800, 400)
    ]
    
    # Position obstacles properly on ground
    for obs in obstacles:
        if hasattr(obs, 'rect') and obs.rect and obs != obstacles[3] and obs != obstacles[4]:  # Not birds
            obs.position.y = ground_y - obs.rect.height // 2
            obs.rect.centery = obs.position.y
    
    # Test states
    states = ["idle", "run", "jump", "duck"]
    current_state = 0
    state_timer = 0
    
    font = pygame.font.Font(None, 36)
    
    print("Visual test running... Press ESC to exit")
    print("Watch the dino cycle through different animation states")
    print("Observe the scaling of all sprites")
    
    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Cycle through states manually
                    current_state = (current_state + 1) % len(states)
                    dino.state = states[current_state]
                    state_timer = 0
        
        # Auto-cycle through states every 2 seconds
        state_timer += delta_time
        if state_timer >= 2.0:
            current_state = (current_state + 1) % len(states)
            dino.state = states[current_state]
            state_timer = 0
            print(f"Dino state: {dino.state}")
        
        # Update dino animation
        dino.update_state_animation(delta_time)
        
        # Update bird animations
        for obstacle in obstacles:
            if isinstance(obstacle, Bird):
                obstacle.update_animation(delta_time)
        
        # Draw everything
        screen.fill((135, 206, 235))  # Sky blue
        
        # Draw background
        background.draw(screen)
        
        # Draw obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        # Draw dino
        dino.draw(screen)
        
        # Draw info text
        info_texts = [
            f"Current State: {dino.state}",
            f"Dino Size: {dino.rect.width}x{dino.rect.height} (8x scale)",
            f"Original Godot scaling applied",
            "Press SPACE to manually cycle states",
            "Press ESC to exit"
        ]
        
        for i, text in enumerate(info_texts):
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (10, 10 + i * 30))
        
        # Draw collision rectangles for debugging
        dino_collision = dino.get_collision_rect()
        if dino_collision:
            pygame.draw.rect(screen, (255, 0, 0), dino_collision, 2)
        
        for obstacle in obstacles:
            if obstacle.rect:
                pygame.draw.rect(screen, (0, 255, 0), obstacle.rect, 2)
        
        pygame.display.flip()
    
    pygame.quit()
    print("Visual test completed!")

if __name__ == "__main__":
    visual_test()
