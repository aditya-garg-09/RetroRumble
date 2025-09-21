#!/usr/bin/env python3
"""
Generate placeholder sprite assets for the game
"""

import pygame
import os

def create_placeholder_sprites():
    """Generate placeholder sprite images"""
    pygame.init()

    # Player sprite (32x32 blue square)
    player_surface = pygame.Surface((32, 32))
    player_surface.fill((0, 100, 255))
    pygame.draw.rect(player_surface, (255, 255, 255), (0, 0, 32, 32), 2)
    pygame.image.save(player_surface, "player.png")

    # Enemy slime sprite (24x24 green square)
    slime_surface = pygame.Surface((24, 24))
    slime_surface.fill((100, 255, 100))
    pygame.draw.rect(slime_surface, (255, 255, 255), (0, 0, 24, 24), 2)
    pygame.image.save(slime_surface, "slime.png")

    # Projectile sprite (8x8 yellow circle)
    projectile_surface = pygame.Surface((8, 8))
    projectile_surface.fill((0, 0, 0))  # Transparent background
    projectile_surface.set_colorkey((0, 0, 0))
    pygame.draw.circle(projectile_surface, (255, 255, 0), (4, 4), 4)
    pygame.image.save(projectile_surface, "projectile.png")

    print("Placeholder sprites created: player.png, slime.png, projectile.png")

if __name__ == "__main__":
    # Change to the placeholder directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    create_placeholder_sprites()
    pygame.quit()