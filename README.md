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
pip install -r requirements.txt
python main.py
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## 🎯 Pre-built Releases

**🎉 New! Ready-to-play releases are now available!**

We've added pre-built executables for easy installation without needing Python:

- **🍎 macOS**: `Dino Run (MacOS).zip` - Compatible with macOS 26 (Tahoe) and later
- **🪟 Windows**: `Dino Run (Window).zip` - Compatible with Windows 10 and later

**Download from the [Releases](./Releases/) folder** - Just download, extract, and play! No Python installation required.


## 🎮 Game Features

### Current Features
- **3 Powerups**: HalfSpeed, DoubleGold, God Mode
- **Dynamic Sprites**: Dinosaur changes appearance based on active powerups
- **Enhanced Audio**: Coin collection sounds and fixed game over audio
- **Cross-platform**: Windows, MacOS

### Controls

| Key | Action |
|-----|--------|
| SPACE / UP | Jump / Start Game |
| DOWN | Duck (while running) |
| ESC | Quit Game |
| F | Toggle FPS display |

## 🛠️ Development

### Project Structure
```
HCMUS-Game/
├── main.py              # Entry point
├── scenes/              # Game modules
├── assets/              # Images, sounds, fonts
├── docs/                # Documentation
└── requirements.txt     # Python dependencies
```

### Building from Source

1. **Clone the repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run the game**: `python3 main.py`
4. **Package for distribution**: `./build_macos.sh` (macOS)

## 📈 Performance Tips
- Use the FPS toggle (F key) to monitor performance
- Close other applications while playing
- Lower system graphics settings if needed

## 📚 Documentation

- [Design Patterns](docs/DESIGN_PATTERNS.md)
- [OOP Analysis](docs/OOP_ANALYSIS.md)
- [AI Development Log](docs/AI_LOG.md)
- [Game Guide](docs/AI/GAME_GUIDE.md)

---

**Developed using Python & Pygame | Enhanced with AI assistance**
