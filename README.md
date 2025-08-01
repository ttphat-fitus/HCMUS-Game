# Dino Run Game - Python Version

A Python remake of the classic dinosaur running game using Pygame.

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

## Game Features

- Infinite running gameplay with proper sprite sheet animations
- Progressive difficulty system matching the original
- Multiple obstacle types with proper scaling:
  - **Ground obstacles**: Stumps, rocks, barrels (2.0-2.5x scale)
  - **Flying obstacles**: Animated birds with wing-flapping (2.0x scale)
- **Dino character**: Full sprite sheet animation (2.5x scale)
  - Idle animation (static)
  - Running animation (4-frame cycle)
  - Jumping animation (static)
  - Ducking animation (2-frame cycle)
- **New Reward System**:
  - Collectible coins that appear during gameplay
  - Power-up items with special effects:
    - **x2 Coin Multiplier**: Doubles coin collection for 15 seconds
    - **Speed Reduction Potion**: Slows game speed for 10 seconds
    - **Invincibility**: Makes player immune to obstacles for 8 seconds
- **Shop System**:
  - Purchase dinosaur skins with collected coins
  - Buy character accessories (hats, sunglasses, capes, etc.)
  - Unlock new maps with different themes:
    - Desert (default)
    - Forest
    - Arctic
    - Volcano
    - Space
- **Enhanced Backgrounds**: Multiple themed maps with parallax scrolling
- Sound effects with jump sound
- Game over screen with restart functionality
- Persistent high score tracking
- **Player Progress**: Coins and purchases saved between sessions

## Project Structure

```text
Game-Python2/
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
    ├── enhanced_background.py  # Multi-theme backgrounds
    ├── rewards.py       # Coin and power-up system
    ├── shop.py          # Shop and player progress
    ├── hud.py          # UI elements
    └── game_over.py    # Game over screen
```

## New Features Overview

### 🪙 Rewards System
- **Coins**: Collect golden coins during gameplay to earn currency
- **Power-ups**: Special items with temporary effects:
  - 💰 **x2 Coin Multiplier**: Double coin rewards for 15 seconds
  - 🧪 **Speed Reduction**: Slow down the game for easier navigation
  - 🛡️ **Invincibility**: Phase through obstacles safely

### 🛒 Shop System
- **Skins**: Customize your dinosaur's appearance
  - Classic, Fire, Ice, Golden, Shadow themes
- **Accessories**: Add personality with hats, sunglasses, capes, crowns, and wings
- **Maps**: Purchase new environments to change the game's scenery

### 🗺️ Map Themes
- **Desert**: Classic sandy environment with cacti and dunes
- **Forest**: Lush green landscape with trees and mountains
- **Arctic**: Icy terrain with snow-covered formations
- **Volcano**: Dangerous volcanic environment with lava flows
- **Space**: Cosmic adventure with stars, planets, and space platforms

### 💾 Persistent Progress
- Coins and purchases are saved between game sessions
- High scores and player preferences are maintained
- Shop purchases unlock content permanently

## Credits
Ported from the original Godot version to Python using Pygame.
