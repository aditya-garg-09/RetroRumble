"""
Main arena scene containing the game loop and entity management
"""

import pygame
import json
from typing import List
from engine.player import Player
from engine.enemy import Enemy
from engine.projectile import Projectile
from engine.wave_manager import WaveManager
from engine.ui import HUD, ShopModal

class ArenaScene:
    """Main game scene with player, enemies, and wave management"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Load tuning data
        self.tuning_data = self._load_tuning_data()

        # Initialize game entities
        self.player = Player(
            self.screen_rect.centerx - 16,
            self.screen_rect.centery - 16,
            self.tuning_data
        )

        self.enemies: List[Enemy] = []
        self.projectiles: List[Projectile] = []

        # Game systems
        self.wave_manager = WaveManager(self.screen_rect.width, self.screen_rect.height)
        self.hud = HUD(self.screen_rect.width, self.screen_rect.height)
        self.shop = ShopModal(self.screen_rect.width, self.screen_rect.height)

        # Game state
        self.coins = 0
        self.game_paused = False
        self.wave_start_delay = 0.0
        self.wave_delay_duration = 3.0  # Seconds between waves

        # Start first wave
        self.wave_manager.load_wave(1)

        # Input state
        self.mouse_pressed = False

        print(f"OK: ArenaScene initialized - starting wave {self.wave_manager.current_wave}")

    def _load_tuning_data(self) -> dict:
        """Load game tuning data from JSON"""
        try:
            with open("data/tuning.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default tuning if file doesn't exist
            return {
                "player": {
                    "max_health": 100,
                    "max_mana": 50,
                    "move_speed": 300,
                    "mana_regen": 20,
                    "projectile_cost": 5,
                    "projectile_speed": 500,
                    "projectile_damage": 25
                }
            }

    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.shop.toggle_visibility()
            elif event.key == pygame.K_p:
                self.game_paused = not self.game_paused

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.mouse_pressed = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_pressed = False

        # Pass events to shop
        self.shop.handle_event(event)

    def update(self, dt: float):
        """Update all game entities and systems"""
        if self.game_paused or self.shop.visible:
            return

        # Handle wave completion and delays
        if self.wave_manager.is_wave_complete():
            self.wave_start_delay += dt
            if self.wave_start_delay >= self.wave_delay_duration:
                self.wave_manager.next_wave()
                self.wave_start_delay = 0.0
                print(f"OK: Starting wave {self.wave_manager.current_wave}")

        # Update player
        if self.player.alive:
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            self.player.handle_input(keys, mouse_pos, self.mouse_pressed,
                                   self.projectiles, self.screen_rect)
            self.player.update(dt, self.screen_rect)

        # Update wave manager and spawn enemies
        new_enemies = self.wave_manager.update(dt, self.enemies)
        self.enemies.extend(new_enemies)

        # Update enemies
        for enemy in self.enemies[:]:
            if enemy.alive:
                enemy.update(dt, self.player, self.screen_rect)
                # Check enemy attacks on player
                if enemy.attack(self.player):
                    pass  # Attack handled in enemy.attack()
            else:
                self.enemies.remove(enemy)
                self.coins += enemy.coins_value

        # Update projectiles
        for projectile in self.projectiles[:]:
            if projectile.alive:
                projectile.update(dt, self.screen_rect)
            else:
                self.projectiles.remove(projectile)

        # Handle projectile collisions
        self._handle_projectile_collisions()

    def _handle_projectile_collisions(self):
        """Handle collisions between projectiles and targets"""
        for projectile in self.projectiles[:]:
            if not projectile.alive:
                continue

            if projectile.friendly:
                # Player projectiles hit enemies
                for enemy in self.enemies:
                    if enemy.alive and projectile.collides_with(enemy):
                        enemy.take_damage(projectile.damage)
                        projectile.alive = False
                        break
            else:
                # Enemy projectiles hit player
                if self.player.alive and projectile.collides_with(self.player):
                    self.player.take_damage(projectile.damage)
                    projectile.alive = False

    def render(self):
        """Render all game entities and UI"""
        # Clear screen
        self.screen.fill((32, 32, 64))  # Dark blue background

        # Draw arena border
        border_color = (100, 100, 100)
        pygame.draw.rect(self.screen, border_color, self.screen_rect, 3)

        # Render entities
        if self.player.alive:
            self.player.render(self.screen)

        for enemy in self.enemies:
            if enemy.alive:
                enemy.render(self.screen)

        for projectile in self.projectiles:
            if projectile.alive:
                projectile.render(self.screen)

        # Render UI
        self.hud.render(self.screen, self.player, self.wave_manager, self.coins)
        self.shop.render(self.screen, self.coins)

        # Game over screen
        if not self.player.alive:
            self._render_game_over()

        # Pause indicator
        if self.game_paused:
            font = pygame.font.Font(None, 48)
            pause_text = font.render("PAUSED - Press P to continue", True, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=self.screen_rect.center)
            self.screen.blit(pause_text, pause_rect)

    def _render_game_over(self):
        """Render game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Game over text
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("GAME OVER", True, (255, 100, 100))
        game_over_rect = game_over_text.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery - 50))
        self.screen.blit(game_over_text, game_over_rect)

        # Stats
        stats_font = pygame.font.Font(None, 32)
        wave_text = stats_font.render(f"Reached Wave: {self.wave_manager.current_wave}", True, (255, 255, 255))
        coins_text = stats_font.render(f"Coins Collected: {self.coins}", True, (255, 215, 0))

        wave_rect = wave_text.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + 20))
        coins_rect = coins_text.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + 60))

        self.screen.blit(wave_text, wave_rect)
        self.screen.blit(coins_text, coins_rect)