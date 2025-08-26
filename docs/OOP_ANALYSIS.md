# OOP Analysis – HCMUS Dino Run (Python Version)

This document maps concrete code in the repository to the four core object‑oriented principles and highlights extension points.

## 1. Abstraction
Abstracts hide implementation detail behind clear responsibilities.

| Abstraction | File / Class | Responsibility | Notes |
|-------------|--------------|----------------|-------|
| GameObject base | `scenes/game_object.py` | Unified position, sprite, animation handling | Other entities build on this common contract |
| Obstacle hierarchy | `scenes/obstacles.py` (`Obstacle`, `Stump`, `Rock`, `Barrel`, `Bird`) | Shared movement logic + polymorphic sprite setup | Bird overrides animation & speed logic |
| Token abstraction | `scenes/tokens.py` (`Token`) | Encapsulates value + optional powerup metadata | Could split into `CoinToken` & `PowerupToken` later |
| Manager abstractions | `ObstacleManager`, `TokenManager` | Collection lifecycle, spawning, cleanup | Externalize spawn policies via strategies later |
| MainGame façade | `scenes/main_game.py` | Coordinates subsystems; provides high-level API (`run`, `update`, `draw`) | Candidate for further decomposition (states, event bus) |

## 2. Encapsulation
Protect internal state and expose only what is needed.

| Example | Encapsulated Data | Access Method |
|---------|-------------------|--------------|
| `GameObject` | Raw sprite sheet, frame counters | Public methods `load_sprite_sheet`, `update_animation` – no external mutation of frame index |
| `Dino` | Collision rectangles (`run_rect`, `duck_rect`) | Accessed via `get_collision_rect()` so layout logic stays internal |
| `Token` | Effect duration & type | Returned via `collect()` – prevents external partial state mutation |
| `MainGame` | Powerup timers (`active_powerups`), score logic separation | Manipulated internally; external systems only see HUD output |
| `ObstacleManager` | Obstacle list & spawn timing | Only exposed through `update`, `draw`, `check_collision` |

_Current code uses public attributes for brevity (Pythonic). Formal encapsulation could be increased with `@property` if invariants tighten._

## 3. Inheritance
Hierarchies share behavior; overrides refine specifics.

```
GameObject
 ├─ Obstacle
 │   ├─ Stump
 │   ├─ Rock
 │   ├─ Barrel
 │   └─ Bird (adds animation specifics)
 ├─ Token (adds collect + effect semantics)
 └─ Dino (adds physics + state machine for animation)
```

Benefits already realized:
- One animation + drawing pipeline in `GameObject`
- Consistent vector math and rect alignment

## 4. Polymorphism
Different concrete classes are used through a shared interface.

| Context | Polymorphic Call Site | Behavior Variation |
|---------|-----------------------|--------------------|
| Update loop | `ObstacleManager.update` iterates obstacles calling `obstacle.update(...)` | Bird vs ground obstacles adjust velocity & animation |
| Drawing | `for obstacle in obstacles: obstacle.draw(screen)` | Each obstacle draws its sprite (bird animates) |
| Token processing | `token.collect()` | Returns either coin value or powerup effect payload |
| Dino animation | State-based frame selection | Same method chooses correct frames for idle/run/jump/duck |

## 5. Composition over Inheritance (Where Applied)
Managers *compose* lists of objects instead of subclassing them (e.g., `ObstacleManager`, `TokenManager`). `MainGame` composes all systems instead of inheriting from them.

## 6. Responsibility Distribution (SRP)
| Component | Single Responsibility | Avoided Leakage |
|-----------|-----------------------|-----------------|
| `Dino` | Player physics + animation state | No spawning, scoring, or UI logic |
| `TokenManager` | Token & powerup lifecycle | Does not apply scoring multiplier – leaves to `MainGame` |
| `MainGame` | Orchestrates timing, scoring, difficulty | Does not render individual sprites directly (delegates) |
| `HUD` | Presentation of runtime metrics | No game state mutation |

## 7. Potential Refactors to Strengthen OOP
| Area | Current State | Improvement | Pattern |
|------|---------------|------------|---------|
| Game States | Boolean flags | Introduce state classes | State |
| Difficulty Formula | Inline arithmetic | Strategy objects (linear, exponential) | Strategy |
| Powerup Effects | If/elif in `activate_powerup` | Polymorphic effect classes | Command / Strategy / Decorator |
| Event Handling | Direct method calls | Event bus decoupling | Observer |
| Input | Direct polling | Command mapping & replay | Command |

## 8. Extensibility Hooks
- Add new obstacle: subclass `Obstacle`, register in `ObstacleFactory`.
- Add new powerup: extend Token logic (or future `PowerupEffect` class) and handle in `MainGame.activate_powerup`.
- Replace difficulty curve: swap in future `DifficultyStrategy` instance.
- Add audio/analytics: listen to future emitted events (after Observer introduction).

## 9. Testability Considerations
| Concern | Current Support | Enhancement |
|---------|-----------------|------------|
| Deterministic obstacle spawning | Random choices inline | Inject RNG / factory seed |
| Powerup timing | Timers in dict | Wrap in class for easier mocking |
| Speed progression | Formula | Strategy stub in tests |
| Collision logic | Rect-based; pure | Add unit tests with synthetic rects |

## 10. Anti-Patterns Avoided
| Anti-Pattern | Avoidance Mechanism |
|-------------|---------------------|
| God Object | Responsibilities split among managers & entities |
| Tight Coupling | (Partially) Minimal cross-dependency, future event bus planned |
| Premature Optimization | Kept simple; patterns only where payoff exists |

## 11. Future Migration Path
1. Introduce `DifficultyStrategy` + tests.
2. Add `EventBus` and emit structured events (JSON-like payloads).
3. Extract `PowerupEffect` classes with `apply(game)` / `expire(game)` methods.
4. Replace boolean game state flags with polymorphic state objects.
5. Wrap input mapping in a `CommandRegistry` for AI/replay.

---
This analysis will be revised as architectural upgrades land.
