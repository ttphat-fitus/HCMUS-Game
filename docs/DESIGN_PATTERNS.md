# Design Patterns in HCMUS Dino Run (Python Version)

This document explains which software design patterns are PRESENTLY applied (even in lightweight form), which are PLANNED, and which were CONSIDERED but deferred. The current codebase is intentionally minimal, so some patterns appear in *proto / implicit* form awaiting future expansion.

## Legend
- Implemented: ✅ (actively in code now)
- Partial: 🟡 (lightweight / implicit usage; can be formalized later)
- Planned: 🟦 (design placeholder; not coded yet)
- Not Using: ❌ (rejected for scope/complexity reasons)

## Summary Table
| # | Pattern | Status | Where / How | Benefit | Next Action |
|---|---------|--------|-------------|---------|-------------|
| 1 | Factory | ✅ | `ObstacleFactory.create_ground_obstacle/create_bird` | Centralizes creation + easy to add new obstacle subclasses | Extend to tokens/powerups if diversity grows |
| 2 | Strategy | 🟡 | Speed & difficulty derived from `score / SPEED_MODIFIER` (simple embedded formula) | Isolates progression logic conceptually | Extract DifficultyStrategy interface when alternative curves needed |
| 3 | Observer | 🟦 | Planned event bus for decoupling (e.g., score, powerup pickup, game over) | Reduces direct coupling between systems | Introduce `EventBus` class emitting typed events |
| 4 | State | 🟦 | Menu vs Playing vs GameOver handled via booleans now (`game_running`, `game_over_screen.visible`) | Clearer transitions & testability | Introduce `IGameState` with concrete states managing update/draw |
| 5 | Singleton | 🟡 | Pygame modules (& planned managers) act process‑wide; implicit for high score persistence | Avoid duplicate heavy managers | Formalize only if new managers (AudioManager, AssetCache) added |
| 6 | Prototype | ❌ | Not required: assets are static & cheap | Would add unnecessary complexity | None |
| 7 | Command | 🟦 | Input directly polled (`pygame.key.get_pressed`) | Enables remapping, replay, AI scripting | Wrap inputs in command objects / mapping table |
| 8 | Decorator | ❌ | Powerups use simple state dictionary; layering behaviors not yet needed | Keeps logic simpler at current scale | Reassess if >5 simultaneous effects |
| 9 | Builder | ❌ | Game objects have simple constructors | No complex staged construction | None |
|10 | Flyweight | ❌ | Sprite count small; Pygame caching sufficient | Would prematurely optimize | None |

## Implemented Patterns Detail
### 1. Factory Pattern (Obstacle Creation)
**Location:** `obstacles.py` → `ObstacleFactory`

**Intent:** Encapsulate obstacle instantiation logic and randomization behind a simple API. This prevents `MainGame` from containing branching creation code.

**Benefits:**
- Central point to add new obstacle classes (e.g., Cactus, Pit, RollingBoulder)
- Supports probability tuning & grouping later
- Facilitates unit tests by injecting a deterministic factory

**Future Enhancements:** Add parameter object (spawn context) or dependency injection for difficulty-aware selection.

### 2. (Proto) Strategy Pattern (Difficulty / Speed Progression)
Currently progression is an inline formula:
```
base_speed = START_SPEED + score / SPEED_MODIFIER
```
This is effectively a simple *LinearDifficultyStrategy*. Extracting it into:
```
class DifficultyStrategy:
    def compute_speed(self, score: float) -> float: ...
```
would allow alternate curves (exponential, stepped, adaptive). Powerups (like slowdown) already rely on separation of `base_speed` vs modified `speed`, making externalization straightforward.

## Planned Patterns Detail
### Observer Pattern (Event Bus)
**Motivation:** Avoid direct coupling where `MainGame` manually triggers side effects (sound, UI flash, analytics) on powerup pickup or collision.

**Planned API Sketch:**
```
class EventBus:
    def subscribe(event_type, handler): ...
    def emit(event_type, **data): ...
```
**Example Events:** `POWERUP_ACTIVATED`, `POWERUP_EXPIRED`, `OBSTACLE_HIT`, `COIN_COLLECTED`, `NEW_HIGH_SCORE`.

### State Pattern (Game Flow)
Replace boolean flags with state objects:
```
class GameState:    
    def handle_input(self, game): ...
    def update(self, game, dt): ...
    def draw(self, game): ...
```
Concrete states: `MenuState`, `PlayingState`, `GameOverState`, `PausedState`.

### Command Pattern (Input Abstraction)
Wrap inputs for remapping & automation: 
```
class Command: 
    def execute(self, game): ...
```
Mapping example: `{ JUMP: JumpCommand(), DUCK: DuckCommand() }`

## Deferred / Rejected Patterns Rationale
| Pattern | Reason Not Used Now | When to Reconsider |
|---------|---------------------|--------------------|
| Prototype | No cloning requirement; objects are cheap | If object graphs (e.g., scripted obstacle packs) become complex |
| Decorator | Powerups simple; stacking rules minimal | If multiple concurrent layered buffs require dynamic composition |
| Builder | Straightforward constructors (no optional explosion) | If complex multi-step asset assembly emerges |
| Flyweight | Memory footprint negligible | If dozens of large animated entities appear simultaneously |

## Roadmap to Formalization
1. Extract `DifficultyStrategy` once ≥2 alternate curves are prototyped.
2. Add `EventBus` to decouple HUD, audio, analytics from core logic.
3. Introduce `GameState` classes; migrate `if self.game_running` branching.
4. Wrap input handling in commands enabling replay/AI.
5. Expand powerup system; consider Decorator or Strategy per powerup if complexity rises.

## Quick Win Suggestions
| Ref | Effort | Value | Action |
|-----|--------|-------|--------|
| A | Low | Testability | Introduce `DifficultyStrategy` class now (linear) |
| B | Medium | Extensibility | Implement `EventBus` & emit on powerup pickup/expiry |
| C | Medium | Clarity | Refactor game states into separate classes |
| D | Low | Future Proof | Define `ICommand` and map jump/duck |

## Sample Refactor Snippets
**Difficulty Strategy Extraction:**
```python
class LinearDifficultyStrategy:
    def __init__(self, start_speed, speed_modifier, max_speed):
        self.start = start_speed
        self.mod = speed_modifier
        self.max = max_speed
    def compute(self, score):
        speed = self.start + score / self.mod
        return min(speed, self.max)
```
Used in `MainGame.update`: 
```python
self.base_speed = self.difficulty_strategy.compute(self.score)
```

**Event Emission Example (future):**
```python
self.event_bus.emit('POWERUP_ACTIVATED', name=effect, duration=duration)
```

---
This document will evolve as planned abstractions are implemented.
