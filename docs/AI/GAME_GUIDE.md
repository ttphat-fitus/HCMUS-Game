# 🦕 Dino Run - Python Game Setup Guide

## 📋 What You Have

I've successfully rewritten the Godot-based dinosaur running game into Python! Here's what was created:

### 🎮 **Complete Game Recreation**
- **Faithful port**: All mechanics from the original Godot game
- **Same gameplay**: Jump, duck, avoid obstacles, score points
- **Progressive difficulty**: Speed and obstacle frequency increase
- **High score tracking**: Persistent across game sessions
- **Sound effects**: Jump sound included
- **Parallax background**: Multi-layer scrolling background

### 📁 **Project Structure**
```
Game-Python2/
├── 🎯 main.py              # Game entry point
├── 🔧 setup.py             # Automated setup
├── 🪟 setup.bat            # Windows setup (double-click)
├── 🐧 setup.sh             # macOS/Linux setup
├── 🎮 run_game.bat         # Windows game launcher
├── 🎮 run_game.sh          # macOS/Linux game launcher
├── 🧪 test_game.py         # Test script
├── 📄 requirements.txt     # Dependencies
├── 📖 README.md            # Documentation
├── 📝 DEVELOPMENT_NOTES.md # Technical details
├── 🖼️ assets/              # Game assets (copied from original)
└── 🎭 scenes/              # Game logic classes
```

## 🚀 **Quick Start (Windows)**

### Option 1: Super Easy (Recommended)
1. **Double-click** `setup.bat` to set up everything automatically
2. **Double-click** `run_game.bat` to play the game

### Option 2: Command Line
```cmd
# Setup (one time only)
setup.bat

# Run the game
run_game.bat
```

## 🚀 **Quick Start (macOS/Linux)**

```bash
# Make scripts executable
chmod +x setup.sh run_game.sh

# Setup (one time only)
./setup.sh

# Run the game
./run_game.sh
```

## 🕹️ **Game Controls**

| Key | Action |
|-----|--------|
| **SPACE** | Jump / Start Game |
| **DOWN ARROW** | Duck (while running) |
| **ESC** | Quit Game |

## 🎯 **Game Features**

✅ **Gameplay**
- Infinite running with increasing difficulty
- Jump over ground obstacles (stumps, rocks, barrels)
- Duck under flying birds
- Progressive speed increase
- Score tracking with high score persistence
- Token collection system for bonus points
- Three powerup types:
  - **HalfSpeed**: Slows game movement for easier navigation (5 seconds)
  - **DoubleGold**: Doubles token value collection (10 seconds) 
  - **God Mode**: Grants invincibility through obstacles (8 seconds)

✅ **Visual & Audio**
- Parallax scrolling background (5 layers)
- Original game sprites and sounds
- Retro-style font from original game
- Smooth 60 FPS gameplay

✅ **Technical**
- Cross-platform (Windows, macOS, Linux)
- Virtual environment isolation
- Automated setup scripts
- Error handling and recovery

## 🔧 **Manual Setup (If Needed)**

If the automatic setup doesn't work, follow these steps:

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```cmd
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install pygame
```

### 4. Run the Game
```bash
python main.py
```

## 🧪 **Testing**

To verify everything works without running the full game:

```bash
# Windows
venv\Scripts\python test_game.py

# macOS/Linux
venv/bin/python test_game.py
```

### FPS Toggle (Debugging)

For testing and debugging, an FPS counter can be toggled at runtime:

- Press `F` during gameplay to toggle the FPS display on/off.
- When enabled, the HUD shows "FPS: <number>" at the top-right.
- A unit test `test_fps_toggle.py` is included in the project root to verify the toggle behavior programmatically.

## 🎨 **Customization**

The game is built with modularity in mind. You can easily:

- **Add new obstacles**: Create new classes in `scenes/obstacles.py`
- **Modify physics**: Adjust constants in `scenes/dino.py` and `scenes/main_game.py`
- **Change graphics**: Replace images in `assets/img/`
- **Add sounds**: Add new sounds to `assets/sound/`
- **Enhance animations**: Extend the sprite system in `scenes/dino.py`

## 🐛 **Troubleshooting**

### Common Issues:

1. **"pygame not found"**
   - Run the setup script again
   - Manually install: `pip install pygame`

2. **"No module named 'scenes'"**
   - Make sure you're running from the `Game-Python2` directory
   - Check that all `.py` files are present in the `scenes/` folder

3. **Images not loading**
   - Verify assets were copied correctly from the original game
   - Check that `assets/img/` contains all the PNG files

4. **Sound not working**
   - Audio is optional; game will work without it
   - Check that `assets/sound/jump.wav` exists

### Getting Help:

- Check `DEVELOPMENT_NOTES.md` for technical details
- Review error messages in the console
- Test with `test_game.py` for basic functionality

## 🏆 **Achievement Unlocked!**

You now have a complete, working Python version of the dinosaur running game! The recreation includes:

- ✅ All original game mechanics
- ✅ Same difficulty progression  
- ✅ Identical obstacle types and behavior
- ✅ Original graphics and sounds
- ✅ Cross-platform compatibility
- ✅ Easy setup and launch scripts

**Enjoy your Python-powered dinosaur adventure!** 🦕🎮
