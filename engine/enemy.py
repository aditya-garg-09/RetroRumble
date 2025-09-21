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

        # Constant movement with random initial direction
        angle = random.uniform(0, 2 * math.pi)
        self.base_velocity_x = math.cos(angle) * self.move_speed
        self.base_velocity_y = math.sin(angle) * self.move_speed

    def update(self, dt: float, player, screen_rect: pygame.Rect):
        """Update enemy with constant movement and wall bouncing"""
        if not player.alive:
            return

        # Calculate distance to player for chase behavior
        distance = self.distance_to(player)

        # Mix base movement with player chasing
        if distance <= self.chase_range:
            # Add slight attraction to player (30% influence)
            player_influence = 0.3
            dx = player.center_x - self.center_x
            dy = player.center_y - self.center_y
            player_distance = math.sqrt(dx * dx + dy * dy)

            if player_distance > 0:
                player_vel_x = (dx / player_distance) * self.move_speed * player_influence
                player_vel_y = (dy / player_distance) * self.move_speed * player_influence

                # Blend with base movement
                self.velocity_x = self.base_velocity_x * (1 - player_influence) + player_vel_x
                self.velocity_y = self.base_velocity_y * (1 - player_influence) + player_vel_y
            else:
                self.velocity_x = self.base_velocity_x
                self.velocity_y = self.base_velocity_y
        else:
            # Use base constant movement
            self.velocity_x = self.base_velocity_x
            self.velocity_y = self.base_velocity_y

        # Update position
        super().update(dt)

        # Wall bouncing - bounce off screen edges
        margin = 10
        bounced = False

        if self.x <= margin or self.x >= screen_rect.width - self.width - margin:
            self.base_velocity_x = -self.base_velocity_x
            self.velocity_x = -self.velocity_x
            # Keep enemy inside bounds
            self.x = max(margin, min(self.x, screen_rect.width - self.width - margin))
            bounced = True

        if self.y <= margin or self.y >= screen_rect.height - self.height - margin:
            self.base_velocity_y = -self.base_velocity_y
            self.velocity_y = -self.velocity_y
            # Keep enemy inside bounds
            self.y = max(margin, min(self.y, screen_rect.height - self.height - margin))
            bounced = True

        # Add slight randomness to prevent predictable bouncing patterns
        if bounced:
            angle_variation = random.uniform(-0.3, 0.3)  # Small angle change
            current_angle = math.atan2(self.base_velocity_y, self.base_velocity_x)
            new_angle = current_angle + angle_variation
            speed = math.sqrt(self.base_velocity_x**2 + self.base_velocity_y**2)
            self.base_velocity_x = math.cos(new_angle) * speed
            self.base_velocity_y = math.sin(new_angle) * speed

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