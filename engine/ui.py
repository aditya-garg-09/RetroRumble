"""
UI elements for the game including HUD and shop
"""

import pygame

class HUD:
    """Heads-up display showing player stats and game state"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

        # Colors
        self.bg_color = (0, 0, 0, 128)  # Semi-transparent black
        self.text_color = (255, 255, 255)
        self.health_color = (255, 0, 0)
        self.mana_color = (0, 100, 255)
        self.coins_color = (255, 215, 0)

    def render(self, screen: pygame.Surface, player, wave_manager, coins: int):
        """Render the complete HUD"""
        # Create HUD background
        hud_height = 80
        hud_surface = pygame.Surface((self.screen_width, hud_height))
        hud_surface.set_alpha(200)
        hud_surface.fill((0, 0, 0))
        screen.blit(hud_surface, (0, 0))

        # Health bar
        self._render_stat_bar(screen, 20, 20, 200, 20, player.health, player.max_health,
                            self.health_color, "Health")

        # Mana bar
        self._render_stat_bar(screen, 20, 45, 200, 15, player.mana, player.max_mana,
                            self.mana_color, "Mana")

        # Coins
        coins_text = self.font.render(f"Coins: {coins}", True, self.coins_color)
        screen.blit(coins_text, (250, 20))

        # Wave info
        wave_text = self.font.render(f"Wave: {wave_manager.current_wave}", True, self.text_color)
        screen.blit(wave_text, (250, 45))

        # Enemies remaining
        enemies_text = self.small_font.render(f"Enemies: {wave_manager.enemies_remaining}", True, self.text_color)
        screen.blit(enemies_text, (350, 45))

        # Game status
        if wave_manager.wave_complete and wave_manager.enemies_remaining == 0:
            status_text = self.font.render("WAVE COMPLETE - Next wave starting...", True, (0, 255, 0))
            screen.blit(status_text, (400, 20))

    def _render_stat_bar(self, screen: pygame.Surface, x: int, y: int, width: int, height: int,
                        current: float, maximum: float, color: tuple, label: str):
        """Render a stat bar with background and label"""
        # Background
        pygame.draw.rect(screen, (64, 64, 64), (x, y, width, height))

        # Fill
        if maximum > 0:
            fill_width = int((current / maximum) * width)
            pygame.draw.rect(screen, color, (x, y, fill_width, height))

        # Border
        pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2)

        # Label
        label_text = self.small_font.render(f"{label}: {int(current)}/{int(maximum)}", True, self.text_color)
        screen.blit(label_text, (x, y - 15))


class ShopModal:
    """Shop interface for purchasing upgrades (placeholder implementation)"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 32)
        self.visible = False

        # Modal dimensions
        self.width = 400
        self.height = 300
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2

    def toggle_visibility(self):
        """Show/hide the shop modal"""
        self.visible = not self.visible

    def handle_event(self, event):
        """Handle shop input events"""
        if not self.visible:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.visible = False

    def render(self, screen: pygame.Surface, coins: int):
        """Render shop modal if visible"""
        if not self.visible:
            return

        # Background overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Shop window
        pygame.draw.rect(screen, (64, 64, 64), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 3)

        # Title
        title_text = self.font.render("SHOP", True, (255, 255, 255))
        title_rect = title_text.get_rect(centerx=self.x + self.width // 2, y=self.y + 20)
        screen.blit(title_text, title_rect)

        # Coins display
        coins_text = self.font.render(f"Coins: {coins}", True, (255, 215, 0))
        screen.blit(coins_text, (self.x + 20, self.y + 60))

        # Placeholder items
        items = [
            "Health Upgrade - 50 coins",
            "Damage Upgrade - 75 coins",
            "Speed Upgrade - 60 coins"
        ]

        for i, item in enumerate(items):
            item_text = self.font.render(item, True, (200, 200, 200))
            screen.blit(item_text, (self.x + 20, self.y + 100 + i * 40))

        # Instructions
        esc_text = self.font.render("Press ESC to close", True, (150, 150, 150))
        screen.blit(esc_text, (self.x + 20, self.y + self.height - 40))