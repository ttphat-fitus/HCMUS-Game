# Game Development Analysis

## Original Game Analysis (Godot)

The original HCMUS-Game is a classic endless runner game similar to Chrome's T-Rex game. Here's the complete analysis:

### Game Structure
```
HCMUS-Game/
├── project.godot          # Godot project configuration
├── assets/
│   ├── fonts/retro.ttf    # Retro-style font
│   ├── img/
│   │   ├── mort.png       # Dinosaur character sprite
│   │   ├── background/    # Parallax scrolling layers (plx-1 to plx-5, ground)
│   │   └── obstacles/     # Obstacle sprites (barrel, bird, rock, stump)
│   └── sound/jump.wav     # Jump sound effect
└── scenes/
    ├── main.gd/.tscn      # Main game logic and scene
    ├── dino.gd/.tscn      # Player character
    ├── bird.gd/.tscn      # Flying obstacle
    ├── hud.tscn           # User interface
    ├── game_over.tscn     # Game over screen
    ├── bg.tscn            # Background
    ├── ground.tscn        # Ground element
    └── obstacle scenes    # Individual obstacle scenes
```

### Core Game Mechanics

1. **Player Character (Dino)**
   - Can jump (SPACE/UP key)
   - Can duck (DOWN key) 
   - Has collision detection
   - Animated states: idle, run, jump, duck

2. **Obstacle System**
   - Ground obstacles: stump, rock, barrel
   - Flying obstacles: bird (at two different heights)
   - Procedural generation based on score/difficulty
   - Multiple obstacles can spawn in groups

3. **Scrolling System**
   - Fixed camera following player
   - Infinite ground scrolling
   - Parallax background layers

4. **Game Logic**
   - Speed increases with score
   - Difficulty progression (more obstacles)
   - Score tracking and high score persistence
   - Game over on collision

### Key Constants from Original Code
- `DINO_START_POS`: (150, 485)
- `GRAVITY`: 4200
- `JUMP_SPEED`: -1800
- `START_SPEED`: 10.0
- `MAX_SPEED`: 25
- `SPEED_MODIFIER`: 5000
- `SCORE_MODIFIER`: 10
- `MAX_DIFFICULTY`: 2
- `BIRD_HEIGHTS`: [200, 390]

## Python Implementation

### Architecture Design

The Python version follows the same structure as the original but uses object-oriented principles:

1. **GameObject Base Class**: Common functionality for all game entities
2. **MainGame Class**: Core game loop and state management
3. **Specialized Classes**: Dino, Obstacles, Background, HUD, GameOver
4. **Manager Classes**: ObstacleManager for handling multiple obstacles

### Key Differences from Original

1. **Physics**: Adapted from Godot's built-in physics to custom implementation
2. **Coordinates**: Godot uses different coordinate system than Pygame
3. **Animation**: Simplified animation system (extensible for sprite sheets)
4. **Audio**: Pygame mixer instead of Godot's audio system
5. **Input**: Pygame event system instead of Godot's input actions

### File Structure
```
Game-Python2/
├── main.py                # Entry point
├── setup.py              # Automated setup script
├── setup.bat             # Windows setup batch file
├── run_game.bat          # Windows game launcher
├── test_game.py          # Testing script
├── requirements.txt      # Python dependencies
├── README.md             # User documentation
├── high_score.json       # Persistent high score storage
├── assets/               # Copied from original (images, sounds, fonts)
└── scenes/               # Game logic classes
    ├── __init__.py
    ├── main_game.py      # Main game controller
    ├── game_object.py    # Base class for all game entities
    ├── dino.py           # Player character
    ├── obstacles.py      # Obstacle classes and management
    ├── background.py     # Parallax scrolling background
    ├── hud.py            # User interface
    └── game_over.py      # Game over screen
```

### Implementation Features

✅ **Completed Features (Current Repository)**:

- Endless running gameplay & progressive difficulty
- Obstacle set: stump, rock, barrel, bird
- Token (coin) spawning & collection tracking (separate `token_score`)
- Powerups (timed): `halfspeed`, `doublegold`, `godmode`
   - Movement slowdown decoupled from score progression via `base_speed` vs `speed`
   - Invincibility allows passage through obstacles without collision
- Parallax scrolling background (multi-layer)
- Jump mechanic (duck placeholder pending art)
- Persistent high score (`high_score.json`)
- HUD: score, high score, coins, active powerups with countdown
- Game over screen & restart flow
- Basic audio (jump sound)

🔄 **Planned / Potential Enhancements**:

- Additional powerups (shield, score multiplier, jump enhancement)
- Duck state sprite & hitbox adjustments
- Particle / dust effects on land & collision
- Expanded obstacle library + pattern groups
- Animated sprite sheets (current dino placeholder single frame sequences)
- Biome / themed backgrounds (forest, arctic, volcano, space)
- Shop system (skins, cosmetics, map themes)
- Achievements & session analytics

### Performance Considerations

- Uses Pygame's hardware acceleration when available
- Efficient collision detection using pygame.Rect
- Memory management through proper object cleanup
- 60 FPS target with delta time calculations

### Debugging / Testing Helpers

- Runtime FPS toggle: Press `F` during gameplay to toggle an FPS counter shown in the HUD (top-right). This is useful when profiling performance or validating frame stability.
- Automated test: `test_fps_toggle.py` verifies the toggle behavior programmatically.

### Error Report & Fix — Coin / Token Spawning Overlapping Obstacles

- Symptom: During playtesting, coins and some powerups sometimes spawned directly inside obstacles (stump/rock/barrel/bird), making them uncollectable.
- Root cause: Token spawn logic did not check active obstacle positions before placing a token. Random placement occasionally overlapped obstacle bounding rectangles.
- Fix summary: Implemented collision-aware spawning in `TokenManager`:
   - `is_safe_spawn_position()` checks proposed token rects against inflated obstacle rects (safety buffer).
   - Spawn methods retry placement (default 10 attempts) before falling back to a safe position.
   - Parameters to tune: `min_distance_from_obstacles` (default 150 px), `vertical_safe_zone` (default 80 px).

   Notes on validation:
      - Run the game and observe token placement in crowded obstacle areas. Adjust the two parameters above in `scenes/tokens.py` if tokens are still too close or too sparse.
      - If spawning frequency drops noticeably, consider decreasing `min_distance_from_obstacles` or adding lane-based spawn logic to guarantee valid lanes.

### Platform Compatibility

- **Windows**: Full support with .bat files for easy setup
- **macOS/Linux**: Full support with shell scripts
- **Python 3.6+**: Required for modern Python features
- **Pygame 2.0+**: Latest version for best performance

## Distribution & Packaging

### macOS Application Bundle
- **Build System**: PyInstaller with custom spec file
- **Compatibility**: macOS 10.12 (Sierra) and later
- **Output**: Standalone .app bundle + optional DMG
- **Build Process**: Automated via `build_macos.sh` script

### Packaging Features:
- All assets automatically bundled
- No Python installation required for end users
- Professional app metadata and bundle identifier
- Retina display optimization
- Universal architecture support (Intel + Apple Silicon)

### Build Commands:
```bash
# Quick build
./build_macos.sh

# Create distribution DMG
./create_dmg.sh

# Manual PyInstaller
pyinstaller build_macos.spec --clean --noconfirm
```

### Distribution Files:
- `build_macos.spec` - PyInstaller configuration
- `build_macos.sh` - Automated build script
- `create_dmg.sh` - DMG creation script
- `requirements.txt` - Python dependencies
