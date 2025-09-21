"""
Wave management system for spawning enemies in timed waves
"""

import json
import random
import pygame
from typing import List, Dict
from engine.enemy import Enemy

class WaveManager:
    """Manages enemy waves based on JSON configuration"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_wave = 1
        self.wave_complete = False
        self.wave_data = None
        self.enemy_templates = {}

        # Spawn timing
        self.spawn_queue = []
        self.spawn_timer = 0.0
        self.enemies_spawned = 0
        self.enemies_remaining = 0

        # Load enemy templates
        self._load_enemy_templates()

    def _load_enemy_templates(self):
        """Load enemy configuration from JSON files"""
        try:
            with open("data/enemies/slime.json", "r") as f:
                self.enemy_templates["slime"] = json.load(f)
        except FileNotFoundError:
            # Fallback if file doesn't exist
            self.enemy_templates["slime"] = {
                "health": 50,
                "speed": 80,
                "damage": 20,
                "size": 24,
                "color": [100, 255, 100],
                "coins": 5,
                "chase_range": 300,
                "attack_cooldown": 1.5
            }

    def load_wave(self, wave_number: int) -> bool:
        """Load wave data from JSON file"""
        try:
            filename = f"data/waves/wave_{wave_number:02d}.json"
            with open(filename, "r") as f:
                self.wave_data = json.load(f)
                self._prepare_spawn_queue()
                return True
        except FileNotFoundError:
            # Generate a procedural wave if file doesn't exist
            self._generate_procedural_wave(wave_number)
            return True

    def _generate_procedural_wave(self, wave_number: int):
        """Generate a procedural wave if JSON doesn't exist"""
        enemy_count = min(3 + wave_number * 2, 15)  # Scale with wave number
        spawn_delay = max(1.0, 3.0 - wave_number * 0.2)  # Faster spawning on later waves

        self.wave_data = {
            "enemies": [
                {
                    "type": "slime",
                    "count": enemy_count,
                    "spawn_delay": spawn_delay
                }
            ]
        }
        self._prepare_spawn_queue()

    def _prepare_spawn_queue(self):
        """Prepare the spawn queue from wave data"""
        self.spawn_queue = []
        self.spawn_timer = 0.0
        self.enemies_spawned = 0
        self.wave_complete = False

        total_enemies = 0
        for enemy_group in self.wave_data["enemies"]:
            enemy_type = enemy_group["type"]
            count = enemy_group["count"]
            spawn_delay = enemy_group.get("spawn_delay", 2.0)

            for i in range(count):
                spawn_time = i * spawn_delay
                self.spawn_queue.append({
                    "type": enemy_type,
                    "spawn_time": spawn_time
                })
                total_enemies += 1

        self.enemies_remaining = total_enemies
        # Sort by spawn time
        self.spawn_queue.sort(key=lambda x: x["spawn_time"])

    def update(self, dt: float, enemies: List[Enemy]) -> List[Enemy]:
        """Update wave spawning and return new enemies to add"""
        new_enemies = []

        if not self.wave_data:
            return new_enemies

        self.spawn_timer += dt

        # Spawn enemies from queue
        while (self.spawn_queue and
               self.spawn_timer >= self.spawn_queue[0]["spawn_time"]):

            spawn_info = self.spawn_queue.pop(0)
            enemy = self._spawn_enemy(spawn_info["type"])
            if enemy:
                new_enemies.append(enemy)
                self.enemies_spawned += 1

        # Update enemies remaining count
        alive_enemies = len([e for e in enemies if e.alive])
        self.enemies_remaining = alive_enemies + len(self.spawn_queue)

        # Check if wave is complete
        if not self.spawn_queue and alive_enemies == 0 and not self.wave_complete:
            self.wave_complete = True

        return new_enemies

    def _spawn_enemy(self, enemy_type: str) -> Enemy:
        """Spawn a single enemy at arena edge"""
        if enemy_type not in self.enemy_templates:
            return None

        # Choose random edge of screen
        edge = random.randint(0, 3)
        margin = 50

        if edge == 0:  # Top
            x = random.randint(0, self.screen_width)
            y = -margin
        elif edge == 1:  # Right
            x = self.screen_width + margin
            y = random.randint(0, self.screen_height)
        elif edge == 2:  # Bottom
            x = random.randint(0, self.screen_width)
            y = self.screen_height + margin
        else:  # Left
            x = -margin
            y = random.randint(0, self.screen_height)

        enemy_data = self.enemy_templates[enemy_type].copy()
        return Enemy(x, y, enemy_data)

    def next_wave(self):
        """Advance to the next wave"""
        self.current_wave += 1
        self.wave_complete = False
        self.load_wave(self.current_wave)

    def is_wave_complete(self) -> bool:
        """Check if current wave is complete"""
        return self.wave_complete