# AI Development Log

## 2025-07-30 Game Rewrite in Python — Initial analysis & plan
### User's prompt
````

# Game Rewrite in Python

## Task
You're a senior software engineer and a game developer who has a lot of experience in **Python** and the **Godot** library. You're now helping a student learning Object-oriented Programming to rewrite an old game - written in Godot - to Python. 

## Resources
You are provided two folders: `HCMUS-Game` and `Game-Python`:
- The `HCMUS-Game` directory contains the **ORIGINAL** game, written in **Godot**.
- The `Game-Python` directory SHOULD BE the folder where you put the rewritten game, in **Python**.

## Core requirements
Given the above two directories, you NEED to CAREFULLY ANALYZE the source code of the Godot-based game project. Use your analytical skills to analyze EVERY objects, scenes, elements, etc. in the original game, then **RE-IMPLEMENT** each of this **EXACTLY THE SAME** using Python.

You need to develop the game that comply with the Object-oriented principles and design patterns:
- You must **HEAVILY LEVERAGE** core OOP concepts of Inheritance, Polymorphism, Abstraction, and Encapsulation. Make sure to justify your design decisions in relation to these principles.
- The project must thoughtfully implement **AT LEAST** three software development design patterns. Use the most appropriate design pattern for solving the problem in the game design. You SHOULD explain why the chosen pattern is a suitable solution for the problem at hand. If possible, output a **comparison table** with the following columns: `Index`, `Design Pattern`, `Why would we use or not use it`, `How it could / could not help with the project`, `Final decision of use / not use it`.
- During the implementation of these, if you encounter any case of unapplicable design patterns / OOP concepts (I mean these can't be used in the rewritten project), note those into `UNAPPLICABLE.md` file. Then explain your decision in a comprehensive manner.

## Preferred library
- You might want to use `pygame` as the rendering engine for the rewritten Python game.
- Before using any library, make sure you search the internet first for the appropriate documentation accordingly.
- Make sure that you guide the user to create and enter virtual environment, install any dependencies, and run the game, in DETAIL.

## Further needs
- Professionally use separated files or folders for each object, scene, or element. 
- For the resources (audio, music, or image files), you might want to copy over to the new project directory.
- Before starting, you should create a file called `PLAN.md`. This file contains what you are planning to do, using bulleted list. If you've just done creating this file **INITIALLY**, asks for approval from the user, so that they will manually analyze the plan carefully before giving you the permission to start rewriting the game. **Yes, REMEMBER, ask the user for permission before STARTING your work!!!!**

## Documentation
During our chat, make sure that you **LOG EVERYTHING**, including my messages and your responses, into a file called `AI_LOG.md`, using the following format:

```
----------
USER'S MESSAGE 1
- TIMESTAMP: ${CURRENT DATETIME}
- CONTENT: ${THE ENTIRE MESSAGE, PUT IN CODEBLOCK}
- SUMMARY OF MESSAGE: ${MESSAGE SUMMARY}

----------
COPILOT RESPONSE 1
- TIMESTAMP: ${CURRENT DATETIME}
- YOUR RESPONSE: ${YOUR ENTIRE RESPONSE, PUT IN CODEBLOCK}
- FILES CHANGED: ${Bulleted list of changed files directory}
- SUMMARY OF RESPONSE: ${RESPONSE SUMMARY}
- USER'S FEEDBACK: JUST LEAVE THIS FIELD BLANK

----------
```
... and continue for every single other messages/responses.

````
- SUMMARY OF MESSAGE: User requesting to rewrite a Godot-based game to Python with heavy OOP principles, design patterns, and professional documentation. Must create PLAN.md first and get approval before starting.

### Summary of AI response
- Logged the conversation and created an initial `AI_LOG.md` entry for this interaction.
- Began analysis of the Godot project by reading `project.godot`, key scene scripts (`scenes/main.gd`, `scenes/dino.gd`, `scenes/bird.gd`) and scene files (`scenes/*.tscn`).
- Scanned asset directories to inventory images, sounds, and fonts used by the original Godot project.
- Checked the existing `Game-Python/` directory to see what (if anything) is already implemented in Python.
- Researched `pygame` documentation to confirm it is a suitable rendering option for the rewrite.
- Prepared to create a PLAN.md and requested user approval before starting the rewrite.

### Files changed
- Added/updated `AI_LOG.md` to record this interaction.
- Read (no changes) `HCMUS-Game/project.godot` and scripts: `scenes/main.gd`, `scenes/dino.gd`, `scenes/bird.gd`.
- Read (no changes) scene files: `scenes/main.tscn`, `scenes/dino.tscn`, `scenes/bird.tscn`, `scenes/barrel.tscn`, `scenes/bg.tscn`, `scenes/game_over.tscn`, `scenes/ground.tscn`, `scenes/hud.tscn`, `scenes/rock.tscn`, `scenes/stump.tscn`.
- Scanned asset metadata under `HCMUS-Game/assets/` (images, fonts, sounds) including `assets/img/*` and `assets/sound/*` (no files were modified).
- Inspected `Game-Python/` directory (found empty / no relevant files).

### User's opinion
Copilot created the game following the prompt by the user, but it resulted in a lot of errors although it was structurally correct. The cause might be that the prompt contains too many requirements.

## 2025-07-30 Game Rewrite in Python — Analysis & plan (conversation 2)
### User's prompt
````

# Game Rewrite in Python

## Task
You're a senior software engineer and a game developer who has a lot of experience in **Python** and the **Godot** library. You're now helping a student learning Object-oriented Programming to rewrite an old game - written in Godot - to Python. 

## Resources
You are provided two folders: `HCMUS-Game` and `Game-Python`:
- The `HCMUS-Game` directory contains the **ORIGINAL** game, written in **Godot**.
- The `Game-Python` directory SHOULD BE the folder where you put the rewritten game, in **Python**.

## Core requirements
Given the above two directories, you NEED to CAREFULLY ANALYZE the source code of the Godot-based game project. Use your analytical skills to analyze EVERY objects, scenes, elements, etc. in the original game, then **RE-IMPLEMENT** each of this **EXACTLY THE SAME** using Python.

You need to develop the game that comply with the Object-oriented principles and design patterns:
- You must **HEAVILY LEVERAGE** core OOP concepts of Inheritance, Polymorphism, Abstraction, and Encapsulation. Make sure to justify your design decisions in relation to these principles.
- The project must thoughtfully implement **AT LEAST** three software development design patterns. Use the most appropriate design pattern for solving the problem in the game design. You SHOULD explain why the chosen pattern is a suitable solution for the problem at hand. If possible, output a **comparison table** with the following columns: `Index`, `Design Pattern`, `Why would we use or not use it`, `How it could / could not help with the project`, `Final decision of use / not use it`.
- During the implementation of these, if you encounter any case of unapplicable design patterns / OOP concepts (I mean these can't be used in the rewritten project), note those into `UNAPPLICABLE.md` file. Then explain your decision in a comprehensive manner.

## Preferred library
- You might want to use `pygame` as the rendering engine for the rewritten Python game.
- Before using any library, make sure you search the internet first for the appropriate documentation accordingly.
- Make sure that you guide the user to create and enter virtual environment, install any dependencies, and run the game, in DETAIL.

## Further needs
- Professionally use separated files or folders for each object, scene, or element. 
- For the resources (audio, music, or image files), you might want to copy over to the new project directory.
- Before starting, you should create a file called `PLAN.md`. This file contains what you are planning to do, using bulleted list. If you've just done creating this file **INITIALLY**, asks for approval from the user, so that they will manually analyze the plan carefully before giving you the permission to start rewriting the game. **Yes, REMEMBER, ask the user for permission before STARTING your work!!!!**

## Documentation
During our chat, make sure that you **LOG EVERYTHING**, including my messages and your responses, into a file called `AI_LOG.md`, using the following format:

```
----------
USER'S MESSAGE 1
- TIMESTAMP: ${CURRENT DATETIME}
- CONTENT: ${THE ENTIRE MESSAGE, PUT IN CODEBLOCK}
- SUMMARY OF MESSAGE: ${MESSAGE SUMMARY}

----------
COPILOT RESPONSE 1
- TIMESTAMP: ${CURRENT DATETIME}
- YOUR RESPONSE: ${YOUR ENTIRE RESPONSE, PUT IN CODEBLOCK}
- FILES CHANGED: ${Bulleted list of changed files directory}
- SUMMARY OF RESPONSE: ${RESPONSE SUMMARY}
- USER'S FEEDBACK: JUST LEAVE THIS FIELD BLANK

----------
```
... and continue for every single other messages/responses.
````
### Summary of AI response
- Confirmed intention to rewrite the Godot game to Python using OOP principles and design patterns; will start by analyzing the original game structure and creating a PLAN.md.
- Read key game scripts and scene files (examples: `scenes/main.gd`, `scenes/dino.gd`, `scenes/bird.gd`) to extract game logic and variables.
- Enumerated assets under `HCMUS-Game/assets/` (images and sounds) to determine resources to copy into the Python project.
- Checked `Game-Python` directory to see what (if anything) exists to receive the rewritten code.
- Began creating `PLAN.md` and prepared to update `AI_LOG.md` with findings.
- Performed read-only inspections of Godot project files; no modifications to original game source were made.

### Files changed
- Updated `AI_LOG.md` (this file) to append the current analysis.
- Read (no changes): `HCMUS-Game/project.godot`, `scenes/main.gd`, `scenes/dino.gd`, `scenes/bird.gd`, and scene files: `scenes/main.tscn`, `scenes/dino.tscn`, `scenes/bird.tscn`, `scenes/barrel.tscn`, `scenes/bg.tscn`, `scenes/game_over.tscn`, `scenes/ground.tscn`, `scenes/hud.tscn`, `scenes/rock.tscn`, `scenes/stump.tscn`.
- Scanned assets (no changes): `assets/img/*`, `assets/img/background/*`, `assets/img/obstacles/*`, `assets/sound/jump.wav`.

### User's opinion
Copilot created the game following the prompt by the user, but it resulted in a lot of errors although it was structurally correct. The cause might be that the prompt contains too many requirements.


## 2025-07-30 Game Rewrite in Python — Phase 1 start
### User's prompt
````

Let's proceed with rewritting the project. I've attached my original prompt and your plan here, accordingly. Carefully follow the plan and implement the source code!

````
- SUMMARY OF MESSAGE: User approved the plan and gave permission to start implementing the Python game rewrite.

### Summary of AI response
- Started Phase 1 setup: project structure, requirements, README, configuration constants, and package skeleton.
- Prepared asset folders and created many package __init__ files so the codebase is import-ready.
- Set up virtual environment instructions in README, added pygame to requirements, created config/settings.py with game constants.
- Created package layout under src/ (game, objects, ui, utils, managers).
- Prepared to copy game assets (images, sounds, fonts) into the new project structure.
- Awaiting confirmation to continue with Phase 1 implementation details (creating base GameObject, AssetManager, and main game loop).

### Files changed
- PLAN.md (created/updated)
- Game-Python/
  - requirements.txt (created: includes pygame)
  - README.md (created: setup & run instructions)
  - config/settings.py (created: screen, physics, asset paths, constants)
  - src/__init__.py
  - src/game/__init__.py
  - src/objects/__init__.py
  - src/objects/base/__init__.py
  - src/objects/player/__init__.py
  - src/objects/obstacles/__init__.py
  - src/objects/background/__init__.py
  - src/ui/__init__.py
  - src/utils/__init__.py
  - src/managers/__init__.py
  - (many package directories created matching planned file structure)
  - assets/images/ (asset folder prepared)
  - assets/sounds/ (asset folder prepared)
  - assets/fonts/ (asset folder prepared)
- AI_LOG.md (appended earlier entries)

### User's opinion
Copilot followed as expected. However the game resulted in a lot of library errors and functionality issues.

## 2025-07-30 Game Rewrite in Python — Collision utilities implementation
### User's prompt
````
(Continuation of Python rewrite: Implement collision detection utilities for game objects)
````
- SUMMARY OF MESSAGE: User requested implementation of collision detection utilities for the Python game rewrite.

### Summary of AI response
- Created and implemented `src/utils/collision.py` containing:
  - A static `CollisionDetector` class with methods for rectangle, circle, point-in-rect, rect-circle, and pixel-perfect collision detection.
  - Each method is documented with docstrings and demonstrates OOP principles, especially abstraction (hiding complex math behind simple interfaces).
  - Implemented a `CollisionBox` class to encapsulate collision data for game objects, with properties and methods for collision checking, demonstrating encapsulation.
- All code is well-documented and structured to support OOP best practices.

### Files changed
- Created/updated: `src/utils/collision.py`

### User's opinion
Copilot followed as expected. However the game resulted in a lot of library errors and functionality issues.

## 2025-07-30 Game Rewrite in Python — Animation system implementation
### User's prompt
````
(Continuation of Python rewrite: Implement animation system for sprite-based game objects)
````
- SUMMARY OF MESSAGE: User requested implementation of animation system for sprite-based game objects in the Python rewrite.

### Summary of AI response
- Created and implemented `src/utils/animation.py` containing:
  - `AnimationFrame` class: Represents a single frame in an animation, encapsulates frame data.
  - `Animation` class: Manages a sequence of frames, handles timing, looping, and playback state. Demonstrates abstraction and encapsulation.
  - `AnimationController` class: Manages multiple animations for a game object, supports adding, playing, and switching animations. Demonstrates polymorphism and encapsulation.
- All classes are documented with docstrings and designed to support OOP principles (abstraction, encapsulation, polymorphism).
- The animation system is modular and ready for integration with game objects.

### Files changed
- Created/updated: `src/utils/animation.py`

### User's opinion
Copilot followed as expected. However the game resulted in a lot of library errors and functionality issues.

## 2025-07-30 Game Rewrite in Python — Base GameObject implementation
### User's prompt
````
(Continuation of Python rewrite: Implement base GameObject class for core architecture)
````
- SUMMARY OF MESSAGE: User requested implementation of a base GameObject class for the Python game rewrite's core architecture.

### Summary of AI response
- Created and implemented `src/objects/base/game_object.py` containing:
  - `GameObject` abstract base class, serving as the foundation for all game objects.
  - Demonstrates all core OOP principles:
    - Abstraction: Defines a common interface and abstract methods.
    - Encapsulation: Uses protected/private attributes with property accessors.
    - Inheritance: Designed to be inherited by all game objects.
    - Polymorphism: Virtual methods for subclass overrides.
  - Includes properties for position, velocity, size, active/visible state, surface, and collision box.
  - Provides abstract methods for update and other game logic, enforcing subclass implementation.
- Code is modular, documented, and ready for extension by specific game object types.

### Files changed
- Created/updated: `src/objects/base/game_object.py`

### User's opinion
Copilot followed as expected. However the game resulted in a lot of library errors and functionality issues.

## 2025-07-30 Game Rewrite in Python — MovableGameObject implementation
### User's prompt
````
(Continuation of Python rewrite: Implement MovableGameObject class for physics and movement)
````
- SUMMARY OF MESSAGE: User requested implementation of a MovableGameObject class for physics and movement in the Python game rewrite.

### Summary of AI response
- Extended the base GameObject architecture by creating `src/objects/base/game_object.py` (continued):
  - Added `MovableGameObject` class, inheriting from `GameObject`.
  - Implements physics and movement capabilities:
    - Properties for acceleration, max speed, friction.
    - Methods for applying force, updating physics, and movement.
    - Demonstrates inheritance (extends GameObject), encapsulation (property accessors), and extensibility for future game objects.
  - All code is documented and designed for OOP best practices.

### Files changed
- Updated: `src/objects/base/game_object.py` (added MovableGameObject class and physics methods)

### User's opinion
Copilot followed as expected. However the game resulted in a lot of library errors and functionality issues.

## 2025-07-30 Game Rewrite in Python — AssetManager (Singleton) implementation
### User's prompt
````
(Continuation of Python rewrite: Implement AssetManager using Singleton pattern for asset loading and caching)
````
- SUMMARY OF MESSAGE: User requested implementation of an AssetManager using the Singleton pattern for managing game assets.

### Summary of AI response
- Created and implemented `src/managers/asset_manager.py` containing:
  - `AssetManager` class, implementing the Singleton pattern to ensure only one instance manages all assets.
  - Manages loading and caching of images, sounds, fonts, and music.
  - Demonstrates Singleton pattern and encapsulation (private asset storage, controlled access).
  - Provides methods for loading images, sounds, fonts, and music with caching and error handling.
- Code is modular, documented, and ready for integration with other game systems.

### Files changed
- Created/updated: `src/managers/asset_manager.py`

### User's opinion
Copilot followed as expected. However the game resulted in a lot of library errors and functionality issues.

## 2025-07-30 Game Rewrite in Python — Debugging & refactor
### User's prompt
- SUMMARY OF MESSAGE: User requested a detailed debugging and refactoring the infinite running dino game, emphasizing input handling, animation state, and game state transitions.

### Summary of AI response
- Objective: Debug and refactor the infinite running dino game (Python, pygame) to fix jump action, animation state, and game flow issues.
- Key issues addressed:
  - Jump action not triggering on space bar: Refactored input handling in `dino.py`, consolidated logic, and fixed jump trigger.
  - Animation state not updating correctly: Removed redundant `_update_animation_state`, centralized animation logic.
  - Game flow mismatch: Introduced `PRE_START` state in `states.py` and updated `game_manager.py` to match original game flow.
- Major code changes:
  - `dino.py`: Refactored input handling, removed redundant animation state logic, fixed jump trigger.
  - `game_manager.py`: Added `PRE_START` state support, revised game start flow, ensured background/obstacle spawning matches original game.
  - `states.py`: Added `PRE_START` state to game state management.
  - Other files referenced: `events.py`, `obstacle_factory.py`, `ground.py`, `HUD`, `GameOverScreen`.
- Design patterns & OOP principles:
  - State, Singleton, Observer, Factory, Facade, Composition patterns referenced and/or implemented.
  - Emphasis on OOP principles: abstraction, encapsulation, inheritance, polymorphism.
- Debugging & verification:
  - Copilot analyzed code, proposed and performed file edits, verified changes, and ensured game logic matched original Godot version.
  - Lessons learned: Importance of consolidating input logic, managing animation state transitions, and matching original game flow.
- Progress tracking:
  - Completed: Parsed and summarized all major debugging steps and code changes.
  - Pending: None (all relevant implementation steps captured and logged).

### Files changed
- `game_manager.py`
### User's opinion
Copilot followed the workflow and implemented the requested changes. The refactored code improved input handling and game flow, but some minor issues may remain for further review.

## 2025-07-30 Game Flow Revision: Static Start, Fast Background, Obstacles
### User's prompt
```
After pressing SPACE, it changes to the game state where background is static at first. Then, after the player jump by using the space bar, the dino starts the running animation while the background moves at a much faster speed. Obstacles are then spawned. Revise the source code and fix this
```
### Summary of AI response
- Reviewed and modified state management in `game_manager.py`, `states.py`, and related files to match the described flow.
- Updated event types, state transitions, and UI messages for correct game progression.
- Ensured code changes in `events.py`, `settings.py`, and `states.py` to support the new flow.
- Verified the revised structure ensures the game follows the classic pattern of starting the action after the player's first move.
- Implemented static background and idle dino at start, with fast background and obstacle spawning after first jump.
- Maintained consistency with previous entries and template formatting.
- All changes logged and summarized per workflow.
- Ready for further review or next steps.

### User's opinion
Copilot followed the requirements of the prompt successfully. Changes have been approved.

## 2025-07-30 Scaling and Animation Fixes for Dino & Obstacles
### User's prompt
```
Analyze all scenes files so that the dino are at scale, render its animation correctly. Do the same for obstacles.
```
### Summary of AI response
- Analyzed all scene files and assets to ensure dino and obstacles are at correct scale and render animations accurately.
- Enhanced game logic in `game_object.py`, `dino.py`, `obstacles.py`, and `main_game.py` for proper scaling, sprite sheet animation, and collision detection.
- Created `visual_test.py` to visually verify scaling and animation of dino and obstacles.
- Updated documentation (`README.md`, `SCALING_ANALYSIS.md`) to reflect technical improvements and testing procedures.
- Verified changes with automated and visual tests; confirmed all tests pass and game logic matches requirements.
- Ensured all code changes are logged and summarized per workflow.
- Maintained consistency with previous entries and template formatting.
- Ready for further review or next steps.

### User's opinion
Copilot attempted to refactor the entire game, which helped to run the game successfully. All scaling issues are fixed as the original game.

## 2025-07-30 Ground & Obstacle Speed Synchronization
### User's prompt
```
Make the GROUND scroll faster
Make the obstable scroll faster with the ground as well
```
### Summary of AI response
- Searched the codebase for ground scrolling logic and identified the relevant section in `background.py`.
- Added a `ground_speed` multiplier to the ground update logic, making the ground scroll twice as fast as the base speed.
- Searched for obstacle movement logic in `obstacles.py` and updated the `Obstacle` class to use a matching speed multiplier.
- Modified the Bird class to maintain its half-speed behavior while scaling with the new ground speed.
- Ensured all ground obstacles now move at the same speed as the ground, with birds maintaining their relative speed.
- Summarized the changes and explained how to further adjust the speed if needed.
- All changes were logged and summarized per workflow.
- Ready for further review or next steps.

### User's opinion
- Copilot successfully followed the requirements in the prompt and implemented the requested changes.

## 2025-08-15 Bird Obstacle Not Appearing — Debug & Fix
### User's prompt
```
Why is the bird not appearing in the game
The function is triggering correctly, however the bird is not appearing in the gamre
```
### Summary of AI response
- Analyzed the obstacle generation logic and identified a misleading comment and missing difficulty check for bird spawning.
- Noted that the random chance for bird spawning was incorrectly described and the actual probability was 50%, not 67%.
- Searched for references to `ObstacleManager` and confirmed how difficulty and score affect bird spawning.
- Updated the bird generation logic to require max difficulty and a 50% chance for spawning, matching the original game.
- Explained that birds will only appear when the score reaches 100 (difficulty level 2) and the random chance triggers.
- Added debug prints and checked sprite loading, position, and drawing logic for the Bird class.
- Summarized the fix and provided instructions for verifying bird appearance in-game.
- All changes were logged and summarized per workflow.

### User's opinion
- Copilot successfully followed the requirements in the prompt and implemented the requested changes.


## 2025-08-15 Dino Sprite Sheet Switching — Implementation & Debug
### User's prompt
```
I want you to do the following things:
- Change the default sprite sheet from `mort.png` to `mort-base.png`.
- Use the sprite sheet `mort-slow.png` when the dino collected the `halfspeed` token.
- Use the sprite sheet `mort-fast.png` when the score of the player reaches above 400.
```
### Summary of AI response
- Analyzed the dino character code and the powerup/token system to determine where sprite sheet switching should occur.
- Searched for relevant logic in `main_game.py` and `tokens.py` to understand how powerups and score are tracked.
- Implemented dynamic sprite sheet switching in the dino class: default to `mort-base.png`, switch to `mort-slow.png` for halfspeed token, and to `mort-fast.png` for score > 400.
- Added a method to change sprite sheets and ensured animation resets to avoid flickering.
- Detected and resolved file corruption in `dino.py` by recreating the file and restoring correct logic.
- Verified the new logic by reading and updating the file, confirming correct sprite switching and error handling.
- Highlighted the importance of robust asset management and dynamic state handling in game development.
- All changes and debugging steps were logged and summarized per workflow.

### User's opinion
- Copilot successfully followed the requirements in the prompt and implemented the requested changes.

## 2025-08-15 Prepare Game for .exe Packaging — Dependency & Environment Analysis
### User's prompt
```
Prepare this game for packaging as a standalone .exe file
```
### Summary of AI response
- Analyzed the main game file to identify all dependencies and required modules for packaging.
- Searched for a `requirements.txt` file and other .txt files to list dependencies, but found none in the project.
- Examined imports in `main.py` and `main_game.py`, confirming dependencies: pygame, sys, os, json, random, and local modules.
- Configured the Python environment and confirmed Python version 3.11.4.
- Noted the absence of a requirements.txt and recommended creating one for packaging.
- Provided guidance for packaging the game as a .exe, suggesting tools like PyInstaller and steps for bundling assets.
- Highlighted the importance of dependency management and environment setup for successful distribution.
- All steps and findings were logged and summarized per workflow.

### User's opinion
- Copilot guided the user to package the game into a standalone .exe file that can be used to distribute to other Windows machines.

## 2025-08-23 Coin spawn inside obstacle bug — detection & fix

- Issue: Coins (tokens) and powerups occasionally spawned overlapping obstacles, making them uncollectable. This was reported during playtesting and reproduced reliably in scenarios with clustered obstacles.
- Cause: Token spawning logic did not consider obstacle positions when choosing a random spawn x/y within the camera view. Random placement occasionally coincided with obstacle rects.
- Fix implemented: TokenManager now validates proposed spawn positions against `ObstacleManager` active obstacles. It uses an inflated obstacle rectangle (safety buffer) to check collisions and performs up to 10 placement attempts before falling back to a predetermined safe position.
- Files changed: `scenes/tokens.py`, minor update in `scenes/main_game.py` to forward `obstacle_manager` to token updates, HUD tweaks to show FPS toggle.
- Adjustable tuning knobs: `min_distance_from_obstacles` (horizontal buffer, default 150 px) and `vertical_safe_zone` (vertical buffer, default 80 px) inside `TokenManager`.
- Validation: Manual playtesting recommended. Use the `F` key during gameplay to enable FPS display and monitor performance while testing spawning behavior.

Next steps: Gather playtesting feedback and tune buffer values. If spawn density becomes an issue, consider more sophisticated placement policies that account for obstacle clusters and preferred token lanes.
