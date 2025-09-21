# Pixel Arena

A top-down arena shooter prototype built with Python and Pygame. Fight waves of enemies, collect coins, and survive as long as possible!

## Features

- **Player Movement**: WASD controls with mouse-aimed projectile shooting
- **Wave-based Enemies**: JSON-configured enemy waves with increasing difficulty
- **Resource Management**: Mana system for shooting with automatic regeneration
- **HUD**: Real-time display of health, mana, coins, and wave progress
- **Shop System**: Placeholder shop modal (Space to open/close)
- **Data-driven Design**: JSON configuration for enemies, waves, and game tuning

## Installation

1. **Install Python 3.10+** if not already installed
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Generate placeholder assets** (optional):
   ```bash
   cd assets/placeholder
   python generate_placeholders.py
   ```

## How to Run

```bash
python main.py
```

## Controls

- **WASD** or **Arrow Keys**: Move player
- **Mouse**: Aim projectiles
- **Left Mouse Button**: Shoot (costs mana)
- **Space**: Open/close shop
- **P**: Pause/unpause game
- **ESC**: Close shop modal

## Game Mechanics

### Player
- Health: 100 HP
- Mana: 50 MP (regenerates over time)
- Shooting cost: 5 mana per projectile
- Movement speed: 300 units/second

### Enemies
- **Slimes**: Basic green enemies that chase the player
- Deal contact damage when they touch the player
- Drop coins when defeated
- Spawn from arena edges in timed waves

### Waves
- Wave 1: 3 slimes, 2-second spawn delay
- Wave 2: 5 slimes, 1.5-second spawn delay
- Wave 3+: Procedurally generated with increasing difficulty

## Project Structure

```
RetroRumble/
├── main.py                 # Game entry point
├── engine/                 # Core game engine
│   ├── entity.py          # Base entity class
│   ├── player.py          # Player implementation
│   ├── enemy.py           # Enemy implementation
│   ├── projectile.py      # Projectile implementation
│   ├── wave_manager.py    # Wave spawning system
│   └── ui.py              # HUD and shop UI
├── scenes/
│   └── arena_scene.py     # Main game scene
├── data/                  # JSON configuration files
│   ├── tuning.json        # Game balance parameters
│   ├── enemies/
│   │   └── slime.json     # Slime enemy configuration
│   └── waves/
│       ├── wave_01.json   # Wave definitions
│       ├── wave_02.json
│       └── wave_03.json
└── assets/
    └── placeholder/       # Generated placeholder sprites
```

## Configuration

### Tuning Parameters
Edit `data/tuning.json` to adjust game balance:
- Player stats (health, mana, speed, damage)
- Game timing (wave delays, regeneration rates)

### Adding Enemies
1. Create a new JSON file in `data/enemies/`
2. Define enemy stats (health, speed, damage, appearance)
3. Reference the enemy type in wave files

### Creating Waves
Add new wave files in `data/waves/` with format `wave_XX.json`:
```json
{
  "wave_number": 4,
  "description": "Custom wave description",
  "enemies": [
    {
      "type": "slime",
      "count": 10,
      "spawn_delay": 0.8
    }
  ]
}
```

## Development Notes

- **Fixed timestep**: 60 FPS target with delta-time movement
- **Modular design**: Separate classes for entities, scenes, and systems
- **Data-driven**: JSON configuration for easy tweaking
- **Placeholder art**: Colored rectangles/circles for rapid prototyping

## Next Steps

See the prioritized task list below for planned improvements and features.

## Troubleshooting

- **ImportError**: Make sure pygame is installed: `pip install pygame`
- **Missing assets**: The game will run with colored shapes if sprite files are missing
- **Performance**: Reduce enemy count in wave files if the game runs slowly