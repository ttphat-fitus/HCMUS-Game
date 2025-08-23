(# AI / Development Log)

## [2025-08-23] Coin spawn inside obstacle bug — detection & fix

- Issue: Coins (tokens) and powerups occasionally spawned overlapping obstacles, making them uncollectable. This was reported during playtesting and reproduced reliably in scenarios with clustered obstacles.
- Cause: Token spawning logic did not consider obstacle positions when choosing a random spawn x/y within the camera view. Random placement occasionally coincided with obstacle rects.
- Fix implemented: TokenManager now validates proposed spawn positions against `ObstacleManager` active obstacles. It uses an inflated obstacle rectangle (safety buffer) to check collisions and performs up to 10 placement attempts before falling back to a predetermined safe position.
- Files changed: `scenes/tokens.py`, minor update in `scenes/main_game.py` to forward `obstacle_manager` to token updates, HUD tweaks to show FPS toggle.
- Adjustable tuning knobs: `min_distance_from_obstacles` (horizontal buffer, default 150 px) and `vertical_safe_zone` (vertical buffer, default 80 px) inside `TokenManager`.
- Validation: Manual playtesting recommended. Use the `F` key during gameplay to enable FPS display and monitor performance while testing spawning behavior.

Next steps: Gather playtesting feedback and tune buffer values. If spawn density becomes an issue, consider more sophisticated placement policies that account for obstacle clusters and preferred token lanes.

