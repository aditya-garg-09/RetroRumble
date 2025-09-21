"""
Enemy entities with AI behavior
"""

import pygame
import random
import math
from engine.entity import Entity

class Enemy(Entity):
    """Base enemy class with chase AI and contact damage"""

    def __init__(self, x: float, y: float, enemy_data: dict):
        size = enemy_data.get("size", 24)
        super().__init__(x, y, size, size)

        # Enemy stats from data
        self.max_health = enemy_data.get("health", 50)
        self.health = self.max_health
        self.move_speed = enemy_data.get("speed", 100)
        self.damage = enemy_data.get("damage", 20)
        self.coins_value = enemy_data.get("coins", 5)

        # Visual
        color_data = enemy_data.get("color", [100, 255, 100])
        self.color = tuple(color_data)

        # AI behavior
        self.chase_range = enemy_data.get("chase_range", 300)
        self.attack_cooldown = enemy_data.get("attack_cooldown", 1.0)
        self.last_attack_time = 0.0

        # Movement variation to prevent stacking
        self.movement_offset_x = random.uniform(-20, 20)
        self.movement_offset_y = random.uniform(-20, 20)

    def update(self, dt: float, player, screen_rect: pygame.Rect):
        """Update enemy AI and movement"""
        if not player.alive:
            return

        # Calculate distance to player
        distance = self.distance_to(player)

        # Chase player if in range
        if distance <= self.chase_range:
            # Add slight offset to prevent enemies from overlapping perfectly
            target_x = player.center_x + self.movement_offset_x
            target_y = player.center_y + self.movement_offset_y
            self.move_towards(target_x, target_y, self.move_speed, dt)

        # Update position
        super().update(dt)

        # Update attack cooldown
        self.last_attack_time += dt

    def can_attack(self) -> bool:
        """Check if enemy can attack (cooldown finished)"""
        return self.last_attack_time >= self.attack_cooldown

    def attack(self, player):
        """Attack the player (contact damage)"""
        if self.can_attack() and self.collides_with(player):
            player.take_damage(self.damage)
            self.last_attack_time = 0.0
            return True
        return False

    def take_damage(self, damage: int):
        """Apply damage to enemy"""
        self.health -= damage
        if self.health <= 0:
            self.alive = False

    def render(self, screen: pygame.Surface):
        """Render enemy with health bar"""
        # Draw enemy body
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw health bar if damaged
        if self.health < self.max_health:
            bar_width = self.width
            bar_height = 4
            bar_x = self.x
            bar_y = self.y - 8

            # Background (red)
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

            # Health (green)
            health_ratio = self.health / self.max_health
            health_width = bar_width * health_ratio
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))