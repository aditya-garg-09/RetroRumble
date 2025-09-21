#!/usr/bin/env python3
"""
RetroRumble - Main entry point
A top-down arena shooter with wave-based enemies
"""

import pygame
import sys
from scenes.arena_scene import ArenaScene
from engine.ui import HUD, ShopModal

def main():
    """Main game entry point"""
    pygame.init()
    pygame.mixer.init()

    # Screen setup
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    fullscreen = False
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RetroRumble")

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
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if event.key == pygame.K_SPACE and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                    # Toggle fullscreen
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        # Update arena scene with new screen size
                        arena.screen = screen
                        arena.screen_rect = screen.get_rect()
                        arena.hud = HUD(screen.get_width(), screen.get_height())
                        arena.shop = ShopModal(screen.get_width(), screen.get_height())
                        arena.wave_manager.screen_width = screen.get_width()
                        arena.wave_manager.screen_height = screen.get_height()
                    else:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                        # Update arena scene with original screen size
                        arena.screen = screen
                        arena.screen_rect = screen.get_rect()
                        arena.hud = HUD(SCREEN_WIDTH, SCREEN_HEIGHT)
                        arena.shop = ShopModal(SCREEN_WIDTH, SCREEN_HEIGHT)
                        arena.wave_manager.screen_width = SCREEN_WIDTH
                        arena.wave_manager.screen_height = SCREEN_HEIGHT
            arena.handle_event(event)

        # Update and render
        arena.update(dt)
        arena.render()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()