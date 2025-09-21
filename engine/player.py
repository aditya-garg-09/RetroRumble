"""
Player entity with movement and shooting capabilities
"""

import pygame
import math
from engine.entity import Entity
from engine.projectile import Projectile
from typing import List

class Player(Entity):
    """Player character with WASD movement and mouse shooting"""

    def __init__(self, x: float, y: float, tuning_data: dict):
        super().__init__(x, y, 32, 32)  # 32x32 player
        self.color = (0, 100, 255)  # Blue player

        # Player stats from tuning data
        config = tuning_data.get("player", {})
        self.max_health = config.get("max_health", 100)
        self.max_mana = config.get("max_mana", 50)
        self.move_speed = config.get("move_speed", 300)
        self.mana_regen = config.get("mana_regen", 20)  # per second
        self.projectile_cost = config.get("projectile_cost", 5)
        self.projectile_speed = config.get("projectile_speed", 500)
        self.projectile_damage = config.get("projectile_damage", 25)

        # Current stats
        self.health = self.max_health
        self.mana = self.max_mana

        # Input state
        self.keys_pressed = set()

    def handle_input(self, keys: pygame.key.ScancodeWrapper, mouse_pos: tuple, mouse_pressed: bool,
                    projectiles: List[Projectile], screen_rect: pygame.Rect):
        """Handle player input for movement and shooting"""

        # Movement input
        self.velocity_x = 0
        self.velocity_y = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity_y -= self.move_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity_y += self.move_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x -= self.move_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x += self.move_speed

        # Normalize diagonal movement
        if self.velocity_x != 0 and self.velocity_y != 0:
            factor = 1.0 / math.sqrt(2)
            self.velocity_x *= factor
            self.velocity_y *= factor

        # Shooting input
        if mouse_pressed and self.mana >= self.projectile_cost:
            self.shoot(mouse_pos, projectiles)

    def shoot(self, target_pos: tuple, projectiles: List[Projectile]):
        """Create a projectile towards the target position"""
        if self.mana < self.projectile_cost:
            return

        # Calculate direction
        dx = target_pos[0] - self.center_x
        dy = target_pos[1] - self.center_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            # Normalize and apply speed
            vel_x = (dx / distance) * self.projectile_speed
            vel_y = (dy / distance) * self.projectile_speed

            # Create projectile
            projectile = Projectile(
                self.center_x - 4, self.center_y - 4,  # Center on player
                vel_x, vel_y,
                self.projectile_damage,
                friendly=True
            )
            projectiles.append(projectile)

            # Consume mana
            self.mana -= self.projectile_cost

    def update(self, dt: float, screen_rect: pygame.Rect):
        """Update player position and stats"""
        # Move
        super().update(dt)

        # Keep player on screen
        self.x = max(0, min(self.x, screen_rect.width - self.width))
        self.y = max(0, min(self.y, screen_rect.height - self.height))

        # Regenerate mana
        self.mana = min(self.max_mana, self.mana + self.mana_regen * dt)

    def take_damage(self, damage: int):
        """Apply damage to player"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def render(self, screen: pygame.Surface):
        """Render player with health indicator"""
        # Draw player body
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw health bar above player
        bar_width = self.width
        bar_height = 6
        bar_x = self.x
        bar_y = self.y - 10

        # Background (red)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Health (green)
        health_ratio = self.health / self.max_health
        health_width = bar_width * health_ratio
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))