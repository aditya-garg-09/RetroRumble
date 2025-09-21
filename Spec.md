# RetroRumble — Spec.md

> A crisp, developer-facing specification for the Pixel Arena 2D survival arena game (Pygame).

---

## 1. Project Vision

Retro Rumble is a fast-paced, addictive 2D arena survival game focused on short rounds, tight controls, and escalating waves of AI opponents. It targets low-spec hardware and emphasizes smooth animations, responsive input, and modern UI polish.

**Design goals**

* Fun, repeatable runs with short sessions (3–10 minutes average).
* Retro pixel art aesthetic with modern UI overlays and fluid animations.
* Highly tunable data-driven systems (JSON/YAML configs).
* Clean, modular codebase suitable for portfolio and iterative expansion.

---

## 2. Platform & Tech

* Language: **Python 3.10+**
* Engine: **Pygame (2.x)**
* Optional: `pygame_gui` for UI overlays or custom UI system using sprite sheets.
* Data: JSON for configs, SQLite for local high-scores (optional).

**Target platforms**: Desktop (Windows, Linux, macOS). Minimum CPU: any dual-core laptop (2012+), RAM: 2GB, GPU: integrated.

---

## 3. Minimum Viable Product (MVP) Scope

Deliver a working prototype with:

* One playable arena with obstacles.
* Player character (move, melee, ranged, one spell, dodge).
* 3 enemy types (Slime, Bat, Skeleton Archer) with simple AI.
* Wave progression system (10+ waves culminate in a simple miniboss).
* Loot: coins + one weapon drop.
* In-between-wave shop overlay (buy health/mana/potion/upgrades).
* Local high-score table.

---

## 4. Core Systems

### 4.1 Input & Controls

* Movement: W/A/S/D or Arrow keys (8-direction support via normalized vectors).
* Aim & Fire: Mouse to aim, LMB to primary attack (projectile or melee depending on weapon range).
* Spell: RMB or keyboard key (e.g., Space/Q/E) consumes mana.
* Dodge/roll: Shift (short invulnerability, cooldown).
* Pause/Shop: Esc key.

### 4.2 Entity System (OOP)

* `Entity` base class: position, velocity, sprite, AABB hitbox, update(), draw(), take\_damage().
* `Player(Entity)` extends with: health, mana, inventory, input handler, abilities.
* `Enemy(Entity)` extends with: state machine (idle, chase, attack, flee), AI parameters.
* `Projectile` class: owner, velocity, damage, lifetime.
* `Pickup` class: coins, mana orbs, health potions.

### 4.3 Combat & Damage

* Damage types: `physical`, `magic`, `pierce`, `aoe`.
* Armor/Resistance system (simple multiplier). Example: `final_damage = base_damage * (1 - resistance)`.
* Friendly fire: off by default; configurable.

### 4.4 Wave Manager

* Waves defined in JSON with: `wave_number`, `spawns: [{enemy_type, count, delay, spawn_point}]`, `modifiers` (e.g., fog, fast\_enemies).
* Wave scaling algorithm: base\_count + floor(wave\_number \* scale\_factor).
* Spawn scheduler: queue events with timers.

### 4.5 Shop & Upgrades

* In-between waves UI overlay (modal) shows: coins, items, one-time upgrades.
* Items: Health Potion, Mana Potion, Weapon Upgrade (increases damage or adds effect), Passive (increase max mana).

### 4.6 Loot System

* Drop tables per enemy type (JSON): `common`, `uncommon`, `rare`, `legendary` probabilities.
* Loot roll on death; instantiate `Pickup` item at enemy position.

### 4.7 Save & High-scores

* Local `scores.db` (SQLite) or plain JSON `scores.json`.
* Save: player name, wave reached, score, timestamp.

---

## 5. Data Formats (examples)

### `enemies/slime.json`

```json
{
  "id": "slime",
  "health": 20,
  "speed": 60,
  "damage": 4,
  "loot_table": {"coins": [1,3], "mana_orb": 0.2}
}
```

### `waves/wave_01.json`

```json
{
  "wave": 1,
  "spawn_groups": [
    {"enemy_id": "slime", "count": 6, "spawn_delay": 0.5}
  ],
  "modifiers": []
}
```

### `weapons/bow.json`

```json
{
  "id": "shortbow",
  "type": "ranged",
  "damage": 7,
  "proj_speed": 420,
  "cooldown": 0.4,
  "properties": ["piercing"]
}
```

---

## 6. UI / UX Guidelines

* **Art direction**: pixel sprites (16–32px) with crisp palette; UI uses smooth vector-ish panels and subtle translucency.
* **HUD**: Top-left: health + mana bars (animated gradients). Top-right: coins and current wave. Bottom-center: quickbar for spells/items.
* **Shop modal**: slide-up panel animation with easing (cubic-in-out). Items show icon, name, stat changes, and price.
* **Feedback**: damage numbers (floating text), hit sparks, screen shake on heavy hits, particle bursts for explosions.
* **Menus**: simple animated transitions (fade + slight slide) to feel modern.

Animation notes: Use delta-time based interpolation. Implement an `Animator` helper that drives sprite offsets, alpha, scale with easing functions (linear, cubic, elastic).

---

## 7. Art & Audio

* **Sprites**: 16×16–48×48 PNGs, sprite sheets for animations (idle, run, attack, hit, death).
* **Particles**: simple procedural particles using Pygame surfaces (small circles/squares with fade).
* **Audio**: short SFX for hits, pickups, spells. Looping background music (OGG) kept low.
* **Asset pipeline**: `assets/sprites/`, `assets/sfx/`, `assets/music/`.

---

## 8. Animation & Smoothness

* Use fixed timestep game loop (e.g., 60 FPS target) with interpolation for rendering.
* Movement & physics: update using `dt` to keep behavior frame-rate independent.
* Tween system for UI: `Tween(target, property, start, end, duration, easing)` to handle slide/fade/scale.
* Particle pooling to avoid GC overhead.

---

## 9. Performance & Optimization

* Sprite batching: group draws when possible.
* Limit particles per explosion (configurable cap).
* Use simple AABB collision for most checks; reserve pixel-perfect collisions for special cases.
* Cap enemy AI updates (e.g., update pathing every N frames) to reduce CPU.

---

## 10. Testing & QA

* Unit-test data loaders and wave-scaler logic (pure Python functions).
* Integration: run automated smoke-run script that boots game headless to validate no runtime exceptions in core loop.
* Manual: playtesting checklist for input latency, perceived fairness, and difficulty curve.

---

## 11. File Structure (Recommended)

```
pixel-arena/
├─ assets/
│  ├─ sprites/
│  ├─ sfx/
│  └─ music/
├─ data/
│  ├─ enemies/
│  ├─ waves/
│  └─ weapons/
├─ engine/
│  ├─ entity.py
│  ├─ player.py
│  ├─ enemy.py
│  ├─ projectile.py
│  ├─ ui.py
│  └─ animator.py
├─ scenes/
│  ├─ arena_scene.py
│  └─ menu_scene.py
├─ main.py
├─ requirements.txt
├─ README.md
└─ Spec.md
```

---

## 12. Build, Run & Developer Workflow

1. Create Python virtualenv: `python -m venv venv && source venv/bin/activate` (Windows: `venv\Scripts\activate`).
2. Install: `pip install -r requirements.txt` (minimal: `pygame`, `pygame_gui` optional).
3. Run: `python main.py`.
4. Tuning: tweak JSON in `data/` then restart or implement a simple hot-reload watcher for configs.

---

## 13. Tuning Variables (for designers)

* `WAVE_SCALE_FACTOR` (float) — growth in enemy count per wave.
* `BASE_ENEMY_HEALTH_MULTIPLIER` — multiplies enemy health by wave tiers.
* `MANA_REGEN_PER_SECOND` — baseline regen.
* `DODGE_COOLDOWN` — seconds.
* `LOOT_RARITY_WEIGHTS` — array of four floats.

Keep all tunables in `data/tuning.json` for easy balancing.

---

## 14. Roadmap & Milestones

**Week 1 (MVP)**

* Project scaffolding, basic player, simple enemy, wave manager, HUD.

**Week 2 (Content & Polish)**

* Multiple enemy behaviors, shop, loot, basic audio, particle effects.

**Week 3 (Polish & Extras)**

* Add 2 weapon classes, 3 spells, boss wave, local highscores, UI polish.

**Stretch goals**

* Co-op local play, additional arenas, daily challenges, platform packaging.

---

## 15. Notes for Contributors

* Keep systems data-driven.
* Respect single responsibility — avoid giant monolithic files.
* Add docstrings and small unit tests for pure logic functions.

---

*End of Spec.md*
