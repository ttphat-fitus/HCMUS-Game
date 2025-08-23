# 🦕 HCMUS Dinosaur Game

A modern Python implementation of the classic Chrome Dinosaur endless runner, featuring enhanced powerups, dynamic difficulty scaling, and advanced OOP architecture.

## 🚀 Quick Start

### Prerequisites
- Python 3.7+ (Python 3.8+ recommended)
- pip (Python package installer)

### Installation

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
pip install pygame
python main.py
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install pygame
python3 main.py
```

### Alternative One-Line Setup
**Windows:**
```cmd
python -m venv venv && venv\Scripts\activate && pip install pygame && python main.py
```

**macOS/Linux:**
```bash
python3 -m venv venv && source venv/bin/activate && pip install pygame && python3 main.py
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| **SPACE** / **UP** | Jump / Start Game |
| **DOWN** | Duck (while running) |
| **ESC** | Quit Game |
| **F** | Toggle FPS display (for testing/debug) |

| **F** | Toggle FPS display (for testing/debug) |

## ✨ Features

### Gameplay
- **Endless Running**: Infinite procedural generation with progressive difficulty
- **Obstacle Variety**: Ground obstacles (stump, rock, barrel) and flying obstacles (bird)
- **Physics System**: Realistic gravity, jumping mechanics, and collision detection
- **Scoring**: Distance-based scoring with persistent high scores

### Powerup System (3 Active Powerups)
- **🐌 HalfSpeed**: Reduces game speed by 50% for 5 seconds (purple dino sprite)
- **💰 DoubleGold**: Doubles coin value for 10 seconds (golden dino sprite)
- **⚡ Unstoppable**: 8-second invincibility through obstacles (green dino sprite)

### Visual & Audio
- **Dynamic Sprites**: Dinosaur appearance changes based on active powerups
- **Sound Effects**: Coin collection, jump sounds, and game over audio
- **Parallax Background**: Multi-layer scrolling with depth effect
- **Visual Feedback**: HUD powerup display with countdown timers

### Technical
- **OOP Architecture**: Inheritance, Polymorphism, Abstraction, Encapsulation
- **Design Patterns**: Factory, Observer, State, Singleton, Strategy patterns
- **Cross-Platform**: Windows, macOS, and Linux support
- **Performance**: 60 FPS target with efficient collision detection

## 🔧 Troubleshooting

**"python: command not found"**
```bash
# Try python3 instead
python3 main.py
```

**"pygame not found"**
```bash
# Ensure virtual environment is activated first
pip install pygame
```

**No sound/images**
- Check that `assets/` folder contains all files
- Audio is optional - game works without sound

## 📁 Project Structure

```
HCMUS-Game/
├── main.py                # 🎯 Game entry point
├── assets/               # 🎨 Game assets
│   ├── img/dino/        # 🦕 Dinosaur sprites (base, slow, gold, god)
│   ├── img/background/  # 🌄 Background layers
│   ├── img/obstacles/   # 🚧 Obstacle sprites
│   ├── sound/           # 🔊 Audio files
│   └── fonts/           # 📝 Font files
├── scenes/              # 🎭 Game logic
│   ├── main_game.py     # Core game orchestration
│   ├── dino.py          # Player character
│   ├── obstacles.py     # Obstacle management
│   ├── tokens.py        # Powerup system
│   └── [other scenes]   # Background, HUD, etc.
└── docs/                # 📖 Documentation
    ├── AI_LOG.md        # Development history
    ├── DESIGN_PATTERNS.md # Pattern analysis
    └── OOP_ANALYSIS.md   # Architecture details
```

## 📖 Documentation

- **[AI Development Log](docs/AI_LOG.md)** - Complete development history and feature implementation
- **[Design Patterns](docs/DESIGN_PATTERNS.md)** - Software design pattern implementations
- **[OOP Analysis](docs/OOP_ANALYSIS.md)** - Object-oriented architecture breakdown

## 🎓 Educational Value

This project demonstrates:
- **Advanced Python Programming**: OOP principles and best practices
- **Game Development**: Physics, collision detection, animation systems
- **Software Architecture**: Clean code, modular design, design patterns
- **Cross-Platform Development**: Multi-OS compatibility

## 🏗️ Architecture Highlights

### OOP Principles
- **Inheritance**: GameObject → Dino, Obstacle, Token hierarchy
- **Polymorphism**: Different obstacle types with shared interfaces
- **Encapsulation**: Private methods and controlled property access
- **Abstraction**: Clean interfaces hiding implementation complexity

### Design Patterns
- **Factory**: Dynamic obstacle creation
- **Observer**: Event-driven game state management
- **State**: Game state transitions (menu, playing, game over)
- **Singleton**: Resource and asset management
- **Strategy**: Difficulty progression algorithms

## 📝 Credits

**Educational Project**: HCMUS Computer Science Program  
**Purpose**: Object-Oriented Programming coursework demonstration  
**Framework**: Python 3.8+ with Pygame library  
**Platform**: Cross-platform compatibility  

---

**🎮 Enjoy the game and happy coding! 🦕**
