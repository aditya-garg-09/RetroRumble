"""
Modern UI elements for RetroRumble including HUD and shop
"""

import pygame
import math

class HUD:
    """Modern heads-up display with gradients and improved styling"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Modern fonts
        self.title_font = pygame.font.Font(None, 32)
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

        # Modern color scheme
        self.bg_color = (15, 15, 25)  # Dark blue-gray
        self.accent_color = (100, 200, 255)  # Bright cyan
        self.text_color = (240, 240, 240)  # Light gray
        self.health_color = (255, 80, 80)  # Bright red
        self.mana_color = (80, 150, 255)  # Bright blue
        self.coins_color = (255, 215, 0)  # Gold
        self.border_color = (60, 60, 80)  # Gray border

    def render(self, screen: pygame.Surface, player, wave_manager, coins: int):
        """Render the modern HUD with gradients and styling"""
        # Modern HUD panel
        hud_height = 100
        self._render_modern_panel(screen, 0, 0, self.screen_width, hud_height)

        # Left side - Player stats
        self._render_modern_stat_bar(screen, 30, 25, 250, 18, player.health, player.max_health,
                                   self.health_color, "HEALTH", show_numbers=True)

        self._render_modern_stat_bar(screen, 30, 55, 250, 12, player.mana, player.max_mana,
                                   self.mana_color, "MANA", show_numbers=True)

        # Center - Game info with modern styling
        center_x = self.screen_width // 2

        # Wave display with glow effect
        wave_text = self.title_font.render(f"WAVE {wave_manager.current_wave}", True, self.accent_color)
        wave_rect = wave_text.get_rect(centerx=center_x, y=20)
        self._render_text_with_glow(screen, wave_text, wave_rect, self.accent_color)

        # Enemies counter
        enemies_text = self.font.render(f"Enemies: {wave_manager.enemies_remaining}", True, self.text_color)
        enemies_rect = enemies_text.get_rect(centerx=center_x, y=50)
        screen.blit(enemies_text, enemies_rect)

        # Right side - Coins with icon effect
        coins_x = self.screen_width - 200
        coins_bg = pygame.Surface((180, 60))
        coins_bg.set_alpha(150)
        coins_bg.fill(self.bg_color)
        screen.blit(coins_bg, (coins_x, 20))

        # Coin icon (circle)
        pygame.draw.circle(screen, self.coins_color, (coins_x + 20, 35), 8)
        pygame.draw.circle(screen, (200, 160, 0), (coins_x + 20, 35), 8, 2)

        coins_text = self.font.render(f"{coins}", True, self.coins_color)
        screen.blit(coins_text, (coins_x + 35, 25))

        coins_label = self.small_font.render("COINS", True, self.text_color)
        screen.blit(coins_label, (coins_x + 35, 50))

        # Wave status indicator
        if wave_manager.wave_complete and wave_manager.enemies_remaining == 0:
            status_text = self.font.render("WAVE COMPLETE", True, (0, 255, 100))
            status_rect = status_text.get_rect(centerx=center_x, y=75)
            self._render_text_with_glow(screen, status_text, status_rect, (0, 255, 100))

        # Controls hint in bottom right
        controls_text = self.small_font.render("Shift+Space: Fullscreen | TAB: Shop | Space: Pause", True, (150, 150, 150))
        controls_rect = controls_text.get_rect(right=self.screen_width - 10, bottom=self.screen_height - 10)
        screen.blit(controls_text, controls_rect)

    def _render_modern_panel(self, screen: pygame.Surface, x: int, y: int, width: int, height: int):
        """Render a modern panel with gradient background"""
        # Create gradient surface
        gradient_surface = pygame.Surface((width, height))

        for i in range(height):
            alpha = int(200 * (1 - i / height))
            color = (*self.bg_color, alpha)
            gradient_surface.set_at((0, i), color)

        # Fill the rest
        gradient_surface.set_alpha(220)
        gradient_surface.fill(self.bg_color)
        screen.blit(gradient_surface, (x, y))

        # Border
        pygame.draw.rect(screen, self.border_color, (x, y, width, height), 2)

    def _render_modern_stat_bar(self, screen: pygame.Surface, x: int, y: int, width: int, height: int,
                               current: float, maximum: float, color: tuple, label: str, show_numbers: bool = False):
        """Render a modern stat bar with styling"""
        # Background with inner shadow effect
        bg_color = (30, 30, 40)
        pygame.draw.rect(screen, bg_color, (x, y, width, height))
        pygame.draw.rect(screen, (10, 10, 15), (x, y, width, height), 2)

        # Fill with gradient
        if maximum > 0:
            fill_width = int((current / maximum) * width)
            if fill_width > 0:
                # Create gradient fill
                for i in range(fill_width):
                    alpha = 0.7 + 0.3 * (i / width)
                    fill_color = tuple(int(c * alpha) for c in color)
                    pygame.draw.line(screen, fill_color, (x + i, y), (x + i, y + height))

        # Glossy highlight
        highlight_height = height // 3
        highlight_surface = pygame.Surface((width, highlight_height))
        highlight_surface.set_alpha(80)
        highlight_surface.fill((255, 255, 255))
        screen.blit(highlight_surface, (x, y))

        # Border
        pygame.draw.rect(screen, self.border_color, (x, y, width, height), 1)

        # Label
        label_text = self.small_font.render(label, True, self.text_color)
        screen.blit(label_text, (x, y - 18))

        # Numbers
        if show_numbers:
            numbers_text = self.small_font.render(f"{int(current)}/{int(maximum)}", True, self.text_color)
            numbers_rect = numbers_text.get_rect(right=x + width, y=y - 18)
            screen.blit(numbers_text, numbers_rect)

    def _render_text_with_glow(self, screen: pygame.Surface, text_surface: pygame.Surface,
                              rect: pygame.Rect, glow_color: tuple):
        """Render text with a glow effect"""
        # Create glow by rendering offset copies
        glow_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for offset_x, offset_y in glow_offsets:
            glow_rect = rect.copy()
            glow_rect.x += offset_x
            glow_rect.y += offset_y
            screen.blit(text_surface, glow_rect)

        # Render main text
        screen.blit(text_surface, rect)


class ShopModal:
    """Modern shop interface with improved styling"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)
        self.visible = False

        # Modern styling
        self.bg_color = (20, 25, 35)
        self.accent_color = (100, 200, 255)
        self.text_color = (240, 240, 240)
        self.border_color = (80, 120, 160)
        self.button_color = (60, 80, 120)
        self.hover_color = (80, 100, 140)

        # Modal dimensions
        self.width = 500
        self.height = 400
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2

        # Shop items
        self.shop_items = [
            {"name": "Health Upgrade", "price": 50, "description": "Increase max health by 25"},
            {"name": "Damage Boost", "price": 75, "description": "Increase projectile damage by 10"},
            {"name": "Speed Enhancement", "price": 60, "description": "Increase movement speed by 50"},
            {"name": "Mana Expansion", "price": 40, "description": "Increase max mana by 20"},
            {"name": "Rapid Fire", "price": 100, "description": "Reduce mana cost by 2"}
        ]

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
        """Render modern shop modal"""
        if not self.visible:
            return

        # Dark overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Modern shop window with gradient
        self._render_gradient_rect(screen, self.x, self.y, self.width, self.height,
                                 self.bg_color, (40, 50, 70))

        # Border with glow
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), 3)
        pygame.draw.rect(screen, self.accent_color, (self.x-1, self.y-1, self.width+2, self.height+2), 1)

        # Title with modern styling
        title_text = self.title_font.render("RETRO SHOP", True, self.accent_color)
        title_rect = title_text.get_rect(centerx=self.x + self.width // 2, y=self.y + 20)
        screen.blit(title_text, title_rect)

        # Coins display with icon
        coins_y = self.y + 70
        pygame.draw.circle(screen, (255, 215, 0), (self.x + 30, coins_y + 10), 8)
        coins_text = self.font.render(f"Coins: {coins}", True, (255, 215, 0))
        screen.blit(coins_text, (self.x + 50, coins_y))

        # Shop items with modern buttons
        item_start_y = self.y + 110
        for i, item in enumerate(self.shop_items):
            item_y = item_start_y + i * 50

            # Item background
            can_afford = coins >= item["price"]
            bg_color = self.button_color if can_afford else (40, 40, 50)
            text_color = self.text_color if can_afford else (120, 120, 120)

            pygame.draw.rect(screen, bg_color, (self.x + 20, item_y, self.width - 40, 40))
            pygame.draw.rect(screen, self.border_color, (self.x + 20, item_y, self.width - 40, 40), 1)

            # Item text
            name_text = self.font.render(item["name"], True, text_color)
            screen.blit(name_text, (self.x + 30, item_y + 5))

            desc_text = self.small_font.render(item["description"], True, (180, 180, 180))
            screen.blit(desc_text, (self.x + 30, item_y + 25))

            # Price
            price_text = self.font.render(f"{item['price']} coins", True, (255, 215, 0))
            price_rect = price_text.get_rect(right=self.x + self.width - 30, centery=item_y + 20)
            screen.blit(price_text, price_rect)

        # Instructions
        instructions = [
            "Click items to purchase (Coming Soon!)",
            "ESC or TAB to close"
        ]

        for i, instruction in enumerate(instructions):
            inst_text = self.small_font.render(instruction, True, (150, 150, 150))
            inst_rect = inst_text.get_rect(centerx=self.x + self.width // 2,
                                         y=self.y + self.height - 50 + i * 20)
            screen.blit(inst_text, inst_rect)

    def _render_gradient_rect(self, screen: pygame.Surface, x: int, y: int, width: int, height: int,
                            start_color: tuple, end_color: tuple):
        """Render a rectangle with vertical gradient"""
        for i in range(height):
            ratio = i / height
            color = tuple(int(start_color[j] + (end_color[j] - start_color[j]) * ratio) for j in range(3))
            pygame.draw.line(screen, color, (x, y + i), (x + width, y + i))