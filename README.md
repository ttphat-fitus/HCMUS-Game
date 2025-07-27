# T-Rex Runner Game 🦕

A console-based implementation of Chrome's T-Rex Runner game, built in **Python** with exemplary Object-Oriented Programming principles and design patterns.

## 🎮 Game Features

- **Classic T-Rex Runner Gameplay**: Jump and duck to avoid obstacles
- **Progressive Difficulty**: Game speed increases over time  
- **Multiple Obstacle Types**: Cacti, birds, and rocks with unique behaviors
- **Score System**: Track your current score and high score with achievements
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Real-Time Input**: Responsive keyboard controls without requiring Enter
- **Unicode Graphics**: Beautiful emoji-based visual representation
- **Smart AI Design**: Developed using AI collaboration for optimal architecture

## 🐍 Why Python? 

After comprehensive analysis, **Python was selected** as the optimal language because:

- **🎯 Perfect OOP Support**: Natural inheritance, polymorphism, and encapsulation
- **⚡ Superior Input Handling**: Excellent cross-platform real-time input libraries  
- **🌍 Cross-Platform Excellence**: Built-in platform detection and handling
- **🚀 Rapid Development**: Minimal boilerplate code with rich standard library
- **📚 Educational Value**: Clear syntax ideal for learning OOP concepts
- **🤖 AI-Friendly**: Optimal for AI-assisted development and code generation

## 🏗️ Object-Oriented Design Excellence

This project demonstrates mastery of all four OOP principles:

### **Encapsulation** 🔒
- Private member variables with property decorators
- Controlled access through getter/setter methods
- Internal state protection with clear interfaces

### **Inheritance** 🌳
- `GameObject` abstract base class for all game entities
- `Obstacle` hierarchy with `Cactus`, `Bird`, and `Rock` subclasses  
- `Player` class extending `GameObject` with specific behaviors

### **Polymorphism** 🎭
- Method overriding in subclasses for different behaviors
- Runtime behavior changes based on object type
- Common interfaces with type-specific implementations

### **Abstraction** 🎨
- Abstract base classes defining common contracts
- Complex implementation details hidden behind simple interfaces
- Clear separation between interface and implementation

## 🎨 Design Patterns Implementation

### 1. **Singleton Pattern** - GameEngine 🏛️
**Perfect Justification**: 
- ✅ Only one game instance should exist at any time
- ✅ Global access point for centralized game state management
- ✅ Prevents multiple game loops causing resource conflicts
- ✅ Thread-safe implementation with proper cleanup

```python
class GameEngine(metaclass=SingletonMeta):
    @classmethod
    def get_instance(cls):
        return cls()  # Guaranteed single instance
```

### 2. **Factory Pattern** - ObstacleFactory 🏭
**Perfect Justification**:
- ✅ Multiple obstacle types with different creation parameters
- ✅ Dynamic obstacle generation based on difficulty level
- ✅ Encapsulates complex creation logic in one place
- ✅ Easy extensibility for new obstacle types

```python
obstacle = ObstacleFactory.create_random_obstacle(x, ground_y, difficulty)
```

### 3. **Observer Pattern** - Event System 👁️
**Perfect Justification**:
- ✅ Decouples game events from UI and scoring systems
- ✅ Multiple components can react to events independently
- ✅ Real-time score updates and game state notifications
- ✅ Easy to add new observers (sound, achievements, analytics)

```python
game.add_observer(score_observer)
game.notify_observers("score_changed", new_score)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ (recommended: Python 3.9+)
- No additional dependencies required (uses only standard library)

### Quick Start

```bash
# Clone or download the project
cd T-Rex

# Run the game (no installation needed!)
python3 main.py
```

### Alternative Python Commands
```bash
# If python3 is not available, try:
python main.py

# On Windows:
py main.py
```

## 🎮 How to Play

### Controls
- **SPACE** or **UP ARROW**: Jump over ground obstacles (cacti, rocks)
- **DOWN ARROW** or **S**: Duck under flying obstacles (birds)
- **P**: Pause/Resume game
- **ESC** or **Q**: Quit the game

### Gameplay
1. 🦕 The T-Rex automatically runs forward
2. 🌵 Jump over cacti and rocks on the ground
3. 🦅 Duck under birds flying at different heights  
4. 📈 Game speed increases as your score gets higher
5. 💥 Game ends if you hit any obstacle
6. 🏆 Try to beat your high score and unlock achievements!

### Scoring & Achievements
- **Distance Points**: Earn points for distance survived
- **Milestone Achievements**: Unlock achievements at score milestones
- **Level Progression**: Reach higher difficulty levels
- **High Score Tracking**: Persistent high score storage

## 📁 Project Structure

```
T-Rex/
├── main.py                 # Game entry point
├── game/                   # Main game package  
│   ├── core/              # Core game engine
│   │   └── game_engine.py # Singleton GameEngine
│   ├── entities/          # Game objects
│   │   ├── game_object.py # Abstract base class
│   │   ├── player.py      # T-Rex player class
│   │   └── obstacle.py    # Obstacle hierarchy
│   ├── patterns/          # Design pattern implementations
│   │   ├── factory.py     # Factory pattern for obstacles
│   │   └── observer.py    # Observer pattern for events
│   └── utils/             # Utility classes
│       ├── input_handler.py # Cross-platform input
│       └── display.py     # Console rendering
├── docs/                  # Comprehensive documentation
│   ├── AI_COLLABORATION_LOG.md # AI development log
│   ├── LANGUAGE_ANALYSIS.md    # Language selection analysis
│   └── UML_DIAGRAMS.md         # Visual architecture diagrams
└── README.md              # This file
```

## 🔧 Technical Implementation Highlights

### Cross-Platform Input Handling
- **Windows**: `msvcrt` module for immediate key detection
- **Unix/Linux/macOS**: `termios`/`tty` for raw terminal mode
- **Thread-Safe**: Background input monitoring with proper buffering
- **Key Normalization**: Consistent key naming across platforms

### Advanced Game Engine
- **Singleton Architecture**: Thread-safe single instance management
- **Observer Events**: Real-time notifications for score, collisions, achievements
- **Factory Creation**: Dynamic obstacle generation with difficulty scaling
- **Resource Management**: Proper cleanup and context management

### Smart Display System  
- **Efficient Rendering**: Only updates changed screen characters
- **Unicode Support**: Beautiful emoji graphics work cross-platform
- **Console Control**: Platform-specific screen manipulation
- **Frame Rate Control**: Smooth 20 FPS gameplay with timing control

## 🏆 Educational Achievements

### Advanced Python Features Demonstrated
- ✅ **Abstract Base Classes** with `@abstractmethod` decorators
- ✅ **Property Decorators** for elegant encapsulation
- ✅ **Type Hints** for better code documentation and IDE support
- ✅ **Context Managers** with `__enter__`/`__exit__` methods
- ✅ **Threading** for responsive input handling
- ✅ **Weak References** to prevent memory leaks in observers
- ✅ **Enums** for type-safe constants and state management

### Software Engineering Best Practices
- ✅ **SOLID Principles**: Single Responsibility, Open/Closed, etc.
- ✅ **Clean Architecture**: Clear separation of concerns
- ✅ **Design Patterns**: Real-world implementation with justification
- ✅ **Error Handling**: Graceful exception handling throughout
- ✅ **Documentation**: Comprehensive docstrings and comments
- ✅ **Cross-Platform**: Works seamlessly on all major operating systems

## 🤖 AI Collaboration Excellence

This project showcases optimal AI collaboration for software development:

### AI-Assisted Development Process
1. **Architecture Planning**: AI provided comprehensive system design
2. **Pattern Selection**: AI justified optimal design patterns for requirements
3. **Code Generation**: AI generated high-quality, documented code
4. **Cross-Platform Solutions**: AI provided platform-specific implementations  
5. **Debugging**: AI helped resolve import and structure issues
6. **Documentation**: AI created comprehensive technical documentation

### Educational Benefits of AI Collaboration
- **Accelerated Learning**: Rapid exposure to advanced concepts
- **Best Practices**: AI suggested modern Python patterns and techniques
- **Real-World Application**: Practical implementation of theoretical concepts
- **Professional Quality**: Industry-standard code structure and documentation

## 🐛 Troubleshooting

### Common Issues

**Game Won't Start**:
- Ensure Python 3.8+ is installed: `python3 --version`
- Try alternative Python commands: `python main.py` or `py main.py`

**Input Not Responsive**:  
- Make sure terminal window has focus
- Some terminals may not support all key combinations
- Try running in a different terminal emulator

**Display Issues**:
- Ensure terminal supports Unicode/emoji characters
- Try resizing terminal window if display appears corrupted
- Some older terminals may not render emoji correctly

**Permission Issues**:
- No special permissions required - uses only standard library
- If issues persist, try running from a different directory

## 📚 Extension Ideas

Want to enhance the game further? Try implementing:

### Gameplay Extensions
- 🎵 **Sound Effects**: Add audio feedback using `pygame` or `playsound`
- 🌈 **Visual Effects**: Particle effects for collisions and achievements
- 🏃 **Power-ups**: Speed boosts, invincibility, double points
- 🎯 **Game Modes**: Timed challenges, endless mode, obstacle course
- 👥 **Multiplayer**: Local or network multiplayer support

### Technical Extensions  
- 🖼️ **Graphical Version**: Port to `pygame`, `tkinter`, or `pyglet`
- 💾 **Save System**: Save/load game progress and settings
- 📊 **Analytics**: Detailed statistics and performance tracking
- 🏆 **Achievement System**: Comprehensive achievement framework
- 🌐 **Online Features**: Leaderboards and social sharing

### Learning Extensions
- 🧪 **Unit Testing**: Add comprehensive test suite with `pytest`
- 📈 **Performance Profiling**: Optimize with `cProfile` and `line_profiler`
- 🔄 **Additional Patterns**: Implement Strategy, State, or Command patterns
- 📱 **Mobile Port**: Adapt for mobile platforms using `kivy`

## 📝 Academic Usage

This project is designed for educational purposes and demonstrates:

- **University-Level OOP**: Advanced object-oriented programming concepts
- **Design Pattern Mastery**: Real-world application of software design patterns
- **Professional Development**: Industry-standard coding practices and architecture
- **AI Collaboration**: Modern development techniques using AI assistance

Perfect for:
- Computer Science coursework and final projects
- Object-Oriented Programming class demonstrations  
- Software Engineering portfolio pieces
- Design Pattern learning and teaching

## 🙏 Acknowledgments

- **Chrome T-Rex Game**: Original inspiration from Google's offline dinosaur game
- **AI Collaboration**: Advanced development techniques using AI assistance
- **Python Community**: Excellent standard library enabling cross-platform development
- **Open Source**: Built with standard library - no external dependencies

---

**🎮 Ready to Play? Run `python3 main.py` and start jumping! 🦕**

*Developed with ❤️ using AI collaboration for optimal learning and professional quality*
