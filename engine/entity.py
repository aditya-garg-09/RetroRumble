"""
Base entity class for all game objects
"""

import pygame
import math
from typing import Tuple

class Entity:
    """Base class for all game entities (players, enemies, projectiles)"""

    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.alive = True
        self.color = (255, 255, 255)  # Default white

    @property
    def center_x(self) -> float:
        """Center X coordinate"""
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        """Center Y coordinate"""
        return self.y + self.height / 2

    @property
    def rect(self) -> pygame.Rect:
        """Pygame rectangle for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def distance_to(self, other: 'Entity') -> float:
        """Calculate distance to another entity"""
        dx = self.center_x - other.center_x
        dy = self.center_y - other.center_y
        return math.sqrt(dx * dx + dy * dy)

    def angle_to(self, other: 'Entity') -> float:
        """Calculate angle to another entity in radians"""
        dx = other.center_x - self.center_x
        dy = other.center_y - self.center_y
        return math.atan2(dy, dx)

    def move_towards(self, target_x: float, target_y: float, speed: float, dt: float):
        """Move towards a target position at given speed"""
        dx = target_x - self.center_x
        dy = target_y - self.center_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            # Normalize direction and apply speed
            self.velocity_x = (dx / distance) * speed
            self.velocity_y = (dy / distance) * speed

    def update(self, dt: float):
        """Update entity position based on velocity and delta time"""
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def render(self, screen: pygame.Surface):
        """Render the entity (override in subclasses)"""
        pygame.draw.rect(screen, self.color, self.rect)

    def collides_with(self, other: 'Entity') -> bool:
        """Check collision with another entity"""
        return self.rect.colliderect(other.rect)