"""
Projectile entity for player and enemy attacks
"""

import pygame
from engine.entity import Entity

class Projectile(Entity):
    """Projectile fired by players or enemies"""

    def __init__(self, x: float, y: float, vel_x: float, vel_y: float, damage: int, friendly: bool = True):
        super().__init__(x, y, 8, 8)  # Small 8x8 projectile
        self.velocity_x = vel_x
        self.velocity_y = vel_y
        self.damage = damage
        self.friendly = friendly  # True for player projectiles, False for enemy
        self.lifetime = 3.0  # Seconds before auto-destroy
        self.age = 0.0

        # Visual appearance
        self.color = (255, 255, 0) if friendly else (255, 100, 100)  # Yellow for player, red for enemy

    def update(self, dt: float, screen_rect: pygame.Rect):
        """Update projectile movement and lifetime"""
        super().update(dt)
        self.age += dt

        # Remove if too old or off screen
        if self.age >= self.lifetime:
            self.alive = False

        if (self.x < -50 or self.x > screen_rect.width + 50 or
            self.y < -50 or self.y > screen_rect.height + 50):
            self.alive = False

    def render(self, screen: pygame.Surface):
        """Render projectile as a small circle"""
        center_x = int(self.center_x)
        center_y = int(self.center_y)
        pygame.draw.circle(screen, self.color, (center_x, center_y), 4)