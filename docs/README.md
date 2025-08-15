# Dino Run – Python Version

Endless side‑scrolling runner developed in Python with Pygame. This is a faithful educational rewrite (Godot → Python) featuring clean OOP structure, difficulty scaling, collectibles, and a lightweight powerup system.

## Setup Instructions

### 1. Create a Virtual Environment
```bash
python -m venv venv
```

### 2. Activate the Virtual Environment
**Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Game
```bash
python main.py
```

## Game Controls
- **SPACE**: Jump / Start Game
- **DOWN ARROW**: Duck (while running)
- **S**: Open Shop (when not playing)
- **ESC**: Quit Game / Close Shop

## Current Features

- Endless procedural run with progressive difficulty (speed increases over time)
- Obstacle variety: stump, rock, barrel (ground) and bird (flying)
- Parallax multi‑layer background + scrolling ground
- Player (Dino) physics: jump + (future: duck placeholder if sprite set)
- Scoring & persistent high score (`high_score.json`)
- Token (coin) collection system separated from distance score
- Powerups with timers & HUD indicators:
  - `doublegold` – coin (token) value x2
  - `halfspeed` – slows gameplay movement speed (obstacles/background) while score rate remains unchanged
- Distinct separation of gameplay movement speed vs scoring speed (ensures fair scoring during slow effect)
- HUD: score, high score, coin total, active powerups w/ remaining seconds
- Game Over screen with restart control
- Basic audio (jump sound)

## Planned / In Progress (Not yet implemented in repository)

These appear in older design notes but are not present in the current codebase. Tracked here for clarity:

- Expanded powerups (invincibility, more modifiers)
- Shop system (skins, accessories, map themes)
- Themed background variants (forest, arctic, volcano, space)
- Particle / visual effects & sprite sheet animation refinements
- Settings & input remapping

## Project Structure (Current)

```text
HCMUS-Game/
├── main.py              # Main game entry point
├── requirements.txt     # Python dependencies
├── assets/              # Game assets
│   ├── img/             # Image files
│   │   ├── mort.png     # Dinosaur sprite
│   │   ├── background/  # Background images
│   │   └── obstacles/   # Obstacle sprites
│   ├── sound/           # Sound files
│   └── fonts/           # Font files
└── scenes/              # Game scene classes
    ├── main_game.py     # Main game logic
    ├── dino.py          # Player character
    ├── obstacles.py     # Obstacle classes
    ├── background.py    # Background manager
  ├── hud.py           # UI / HUD overlay
  ├── game_over.py     # Game over screen
  ├── obstacles.py     # Obstacle & manager classes
  ├── tokens.py        # (If present) token & powerup spawning logic
  └── background.py    # Parallax background handling
```

## Powerup System

| Powerup | Effect | Notes |
|---------|--------|-------|
| halfspeed | Temporarily reduces movement speed to 70% while score accrual remains tied to unmodified base speed | Creates recovery window without penalizing progress |
| doublegold | Doubles coin value for the active duration | Applies only to token collection, not distance score |

Stacking: Currently each powerup refreshes its own timer when re‑collected; simultaneous effects are supported.

HUD: Active powerups are listed with remaining whole‑second countdown.

Implementation detail: `base_speed` (used for score progression & difficulty) is calculated independent of the slowdown so halfspeed does not reduce scoring rate.

## Development Notes Snapshot

Key architectural decision: decouple scoring (`base_speed`) from movement (`speed`) so time‑based / distance score progression remains fair when slowdown effects are active.

Difficulty is proportional to cumulative score; capped by `MAX_DIFFICULTY` to limit spawn escalation.

High score persistence stored in JSON for portability.

## Credits

Original concept (Godot version) adapted to Python / Pygame for instructional OOP & design pattern practice.
