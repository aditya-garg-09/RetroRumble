#!/usr/bin/env python3
"""
Pixel Arena - Main entry point
A top-down arena shooter with wave-based enemies
"""

import pygame
import sys
from scenes.arena_scene import ArenaScene

def main():
    """Main game entry point"""
    pygame.init()
    pygame.mixer.init()

    # Screen setup
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Arena")

    # Game clock for fixed timestep
    clock = pygame.time.Clock()
    FPS = 60

    # Initialize arena scene
    arena = ArenaScene(screen)

    print("OK: Game starting - main loop initialized")

    # Main game loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            arena.handle_event(event)

        # Update and render
        arena.update(dt)
        arena.render()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()