# UML Class Diagrams

This document contains the UML class diagrams for the T-Rex Runner game, showcasing the object-oriented design and design pattern implementations.

## Overall System Architecture

```mermaid
classDiagram
    %% Core Entity Hierarchy
    class GameObject {
        <<abstract>>
        -x: float
        -y: float
        -width: float
        -height: float
        -symbol: str
        +__init__(x, y, width, height, symbol)
        +update()* abstract
        +render()* abstract
        +get_bounds() Tuple
        +check_collision(other) bool
        +get_x() float
        +get_y() float
        +set_position(x, y) void
    }

    class Player {
        -ground_y: float
        -jump_velocity: float
        -gravity: float
        -is_jumping: bool
        -is_ducking: bool
        -max_jump_height: float
        +__init__(x, ground_y)
        +update() void
        +render() str
        +jump() void
        +duck() void
        +stop_ducking() void
        +is_on_ground() bool
        +reset() void
    }

    class Obstacle {
        <<abstract>>
        -speed: float
        +__init__(x, y, width, height, symbol, speed)
        +update() void
        +render() str
        +move() void
        +is_off_screen() bool
    }

    class Cactus {
        +__init__(x, ground_y, speed)
        +render() str
    }

    class Bird {
        -flight_height: float
        +__init__(x, ground_y, speed, flight_height)
        +render() str
    }

    class Rock {
        +__init__(x, ground_y, speed)
        +render() str
    }

    %% Inheritance relationships
    GameObject <|-- Player
    GameObject <|-- Obstacle
    Obstacle <|-- Cactus
    Obstacle <|-- Bird
    Obstacle <|-- Rock
```

## Design Pattern Implementations

### 1. Singleton Pattern - GameEngine

```mermaid
classDiagram
    class SingletonMeta {
        <<metaclass>>
        -_instances: Dict
        -_lock: Lock
        +__call__(*args, **kwargs) instance
    }

    class GameEngine {
        <<singleton>>
        -running: bool
        -score: int
        -high_score: int
        -game_speed: float
        -obstacles: List[Obstacle]
        -player: Player
        -observers: List[Observer]
        -obstacle_spawn_timer: float
        -obstacle_spawn_interval: float
        -difficulty_level: int
        -achievements: Dict
        +get_instance() GameEngine
        +start_game() void
        +stop_game() void
        +update() void
        +render() void
        +add_observer(observer) void
        +remove_observer(observer) void
        +notify_observers(event, data) void
        -spawn_obstacle() void
        -check_collisions() bool
        -update_score() void
        -increase_difficulty() void
        -handle_achievement(score) void
        -save_high_score() void
        -load_high_score() void
    }

    SingletonMeta ||-- GameEngine : metaclass
```

### 2. Factory Pattern - ObstacleFactory

```mermaid
classDiagram
    class ObstacleFactory {
        <<factory>>
        +create_cactus(x, ground_y, speed) Cactus
        +create_bird(x, ground_y, speed) Bird  
        +create_rock(x, ground_y, speed) Rock
        +create_random_obstacle(x, ground_y, difficulty) Obstacle
        -get_obstacle_probabilities(difficulty) Dict
    }

    class Obstacle {
        <<abstract>>
    }

    class Cactus
    class Bird  
    class Rock

    ObstacleFactory ..> Obstacle : creates
    ObstacleFactory ..> Cactus : creates
    ObstacleFactory ..> Bird : creates
    ObstacleFactory ..> Rock : creates
    
    Obstacle <|-- Cactus
    Obstacle <|-- Bird
    Obstacle <|-- Rock
```

### 3. Observer Pattern - Event System

```mermaid
classDiagram
    class Observer {
        <<interface>>
        +update(event: str, data: Any)* abstract
    }

    class ScoreObserver {
        -display: Display
        +__init__(display)
        +update(event, data) void
        -handle_score_change(score) void
        -handle_game_over(final_score) void
        -handle_achievement(achievement) void
    }

    class GameEngine {
        -observers: List[WeakRef[Observer]]
        +add_observer(observer) void
        +remove_observer(observer) void  
        +notify_observers(event, data) void
    }

    Observer <|.. ScoreObserver
    GameEngine o-- Observer : observes
```

## Utility Classes

```mermaid
classDiagram
    class InputHandler {
        -input_queue: Queue
        -running: bool
        -input_thread: Thread
        +__init__()
        +start() void
        +stop() void
        +get_key() str|None
        +has_key() bool
        -_input_worker() void
        -_get_key_press() str|None
    }

    class Display {
        -width: int
        -height: int
        -buffer: List[List[str]]
        -previous_buffer: List[List[str]]
        +__init__(width, height)
        +clear() void
        +put_char(x, y, char) void
        +put_string(x, y, text) void
        +render() void
        +get_size() Tuple[int, int]
        -_clear_screen() void
        -_move_cursor(x, y) void
        -_hide_cursor() void
        -_show_cursor() void
    }

    class PlatformUtils {
        <<utility>>
        +get_platform() str
        +is_windows() bool
        +is_unix() bool
        +setup_terminal() void
        +restore_terminal() void
    }
```

## Complete System Integration

```mermaid
classDiagram
    %% Main Application
    class Main {
        +main() void
        -setup_game() GameEngine
        -setup_observers(game, display) void
        -game_loop(game, input_handler) void
        -cleanup(input_handler, display) void
    }

    %% Core Game Components
    class GameEngine {
        <<singleton>>
    }
    
    class Player
    class ObstacleFactory {
        <<factory>>
    }
    
    class ScoreObserver {
        <<observer>>
    }

    %% Utilities
    class InputHandler
    class Display

    %% Relationships
    Main ..> GameEngine : uses
    Main ..> InputHandler : uses
    Main ..> Display : uses
    Main ..> ScoreObserver : creates
    
    GameEngine --> Player : contains
    GameEngine --> ObstacleFactory : uses
    GameEngine --> ScoreObserver : notifies
    
    ScoreObserver --> Display : uses
    
    GameEngine ..> InputHandler : reads from
```

## Key Design Principles Demonstrated

### SOLID Principles

1. **Single Responsibility Principle (SRP)**
   - `GameObject`: Manages basic entity properties and behavior
   - `Player`: Handles only player-specific logic (jumping, ducking)
   - `ObstacleFactory`: Responsible only for creating obstacles
   - `InputHandler`: Manages only input collection and processing
   - `Display`: Handles only rendering and screen management

2. **Open/Closed Principle (OCP)**
   - `GameObject` abstract class is closed for modification but open for extension
   - New obstacle types can be added by extending `Obstacle` class
   - New observers can be added without modifying existing code

3. **Liskov Substitution Principle (LSP)**
   - All `Obstacle` subclasses can be used interchangeably
   - `Player` can be used anywhere `GameObject` is expected
   - Factory pattern ensures proper substitutability

4. **Interface Segregation Principle (ISP)**
   - `Observer` interface contains only the methods observers need
   - `GameObject` abstract class defines minimal required interface
   - Utility classes have focused, specific interfaces

5. **Dependency Inversion Principle (DIP)**
   - `GameEngine` depends on `Observer` abstraction, not concrete implementations
   - `ObstacleFactory` returns `Obstacle` interface, not specific types
   - High-level modules don't depend on low-level implementation details

### Design Pattern Benefits

1. **Singleton Pattern**

   - Ensures single game instance and centralized state management
   - Thread-safe implementation prevents race conditions
   - Global access point for game state

2. **Factory Pattern**

   - Encapsulates complex obstacle creation logic
   - Easy to add new obstacle types without changing existing code
   - Centralizes creation parameters and difficulty balancing

3. **Observer Pattern**

   - Loose coupling between game events and UI updates
   - Easy to add new event listeners (achievements, analytics, etc.)
   - Real-time notifications without tight dependencies

## Class Relationship Summary

| Pattern | Classes Involved | Relationship Type | Purpose |
|---------|------------------|-------------------|---------|
| Inheritance | `GameObject` → `Player`, `Obstacle` | Is-a | Code reuse and polymorphism |
| Inheritance | `Obstacle` → `Cactus`, `Bird`, `Rock` | Is-a | Specialized obstacle behaviors |
| Composition | `GameEngine` → `Player`, `obstacles[]` | Has-a | Game state management |
| Aggregation | `GameEngine` → `observers[]` | Uses | Event notification system |
| Dependency | `GameEngine` → `ObstacleFactory` | Uses | Obstacle creation |
| Association | `ScoreObserver` → `Display` | Uses | Score display updates |

This architecture demonstrates a well-structured, maintainable, and extensible object-oriented design that effectively implements multiple design patterns while adhering to SOLID principles and OOP best practices.
    │     Cactus      │   │      Bird       │
    │ <<ConcreteProduct>>│ │ <<ConcreteProduct>>│
    └─────────────────┘   └─────────────────┘
```

### Observer Pattern - Event System

```
    ┌─────────────────────────────────────┐
    │           Observer                  │
    │         <<Interface>>               │
    │─────────────────────────────────────│
    │ + onNotify(string, int): void       │
    └─────────────────────────────────────┘
                        △
                        │
              ┌─────────┴─────────┐
              │                   │
    ┌─────────────────┐   ┌─────────────────┐
    │ ScoreObserver   │   │GameEventObserver│
    │ <<Concrete      │   │ <<Concrete      │
    │  Observer>>     │   │  Observer>>     │
    │─────────────────│   │─────────────────│
    │ - currentScore  │   │                 │
    │ - highScore     │   │─────────────────│
    │─────────────────│   │ + onNotify()    │
    │ + onNotify()    │   │   : void        │
    │   : void        │   └─────────────────┘
    │ + resetScore()  │
    │   : void        │
    └─────────────────┘

    ┌─────────────────────────────────────┐
    │           GameEngine                │
    │          <<Subject>>                │
    │─────────────────────────────────────│
    │ - observers: vector<Observer*>      │
    │─────────────────────────────────────│
    │ + addObserver(Observer*): void      │
    │ + removeObserver(Observer*): void   │
    │ + notifyObservers(string, int): void│
    └─────────────────────────────────────┘
                        │
                        │ notifies
                        ▼
    ┌─────────────────────────────────────┐
    │           Observer                  │
    └─────────────────────────────────────┘
```

## Component Interaction Diagram

```
    ┌─────────────┐    creates    ┌─────────────────┐
    │    main()   │──────────────►│   GameEngine    │
    └─────────────┘               │   (Singleton)   │
                                  └─────────────────┘
                                           │
                                           │ manages
                                           ▼
    ┌─────────────┐                ┌─────────────────┐
    │ ScoreObserver│◄──────────────│     Player      │
    │GameEventObs.│   observes     └─────────────────┘
    └─────────────┘                         │
                                           │ interacts with
                                           ▼
                                  ┌─────────────────┐
                                  │   Obstacles     │
                                  │   (Collection)  │
                                  └─────────────────┘
                                           ▲
                                           │ creates
                                  ┌─────────────────┐
                                  │ObstacleFactory  │
                                  │   (Factory)     │
                                  └─────────────────┘
```

## Sequence Diagram - Game Loop

```
main() → GameEngine → Player → ObstacleFactory → Observer

  │         │          │            │              │
  │ getInstance()      │            │              │
  │────────►│          │            │              │
  │         │          │            │              │
  │ run()   │          │            │              │
  │────────►│          │            │              │
  │         │          │            │              │
  │         │ handleInput()         │              │
  │         │────────► │            │              │
  │         │          │            │              │
  │         │ update() │            │              │
  │         │────────► │            │              │
  │         │          │            │              │
  │         │ shouldSpawnObstacle() │              │
  │         │─────────────────────► │              │
  │         │          │            │              │
  │         │ createRandomObstacle()│              │
  │         │─────────────────────► │              │
  │         │          │            │              │
  │         │ checkCollisions()     │              │
  │         │────────► │            │              │
  │         │          │            │              │
  │         │ notifyObservers()     │              │
  │         │─────────────────────────────────────►│
  │         │          │            │              │
```

## Design Pattern Benefits Summary

### Singleton Pattern Benefits
- **Single Instance**: Ensures only one game engine exists
- **Global Access**: Easy access from any part of the program
- **Resource Management**: Centralized control of game resources
- **State Consistency**: Prevents conflicting game states

### Factory Pattern Benefits
- **Flexibility**: Easy to add new obstacle types
- **Encapsulation**: Creation logic is centralized
- **Abstraction**: Client code doesn't need to know concrete types
- **Maintainability**: Changes to creation logic affect only factory

### Observer Pattern Benefits
- **Loose Coupling**: Game engine doesn't depend on specific observers
- **Extensibility**: Easy to add new event handlers
- **Separation of Concerns**: Event handling is separate from game logic
- **Reusability**: Observers can be used in different contexts

This UML documentation provides a clear visual representation of the object-oriented design and design pattern implementations used in the T-Rex Runner game.
