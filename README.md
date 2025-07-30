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
- **ESC**: Quit Game

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
- Parallax scrolling background with proper scaling
- Sound effects with jump sound
- Game over screen with restart functionality
- Persistent high score tracking

## Project Structure
```
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
    ├── hud.py          # UI elements
    └── game_over.py    # Game over screen
```

## Credits
Ported from the original Godot version to Python using Pygame.
