# Dino Run (Python) – Applying Generative AI in Development

> Slide outline emphasizing how GenAI accelerated, structured, and validated the rewrite. Each section ≈ 1 slide.

---
## 1. Title / Context
- Project: Dino Run (Godot → Python / Pygame)
- Theme: AI‑Assisted OOP Refactor & Feature Growth
- Focus: Leveraging GenAI for code synthesis, review, docs

---
## 2. Why Use GenAI Here?
- Rapid translation of engine concepts (Godot nodes → Python classes)
- Continuous design narration (logs, plan evolution)
- Faster iteration on feature ideation (powerups, patterns)
- Reduces boilerplate & documentation burden

---
## 3. AI Collaboration Goals
| Goal | Description | Success Indicator |
|------|-------------|-------------------|
| Fidelity | Preserve original mechanics | Matching speed/difficulty behavior |
| Clarity | Produce explainable architecture | PLAN + pattern docs generated |
| Extensibility | Prepare hooks for future features | Identified strategy/state/event bus points |
| Productivity | Cut manual drafting time | Fewer handwritten stubs |

---
## 4. Workflow Lifecycle (Human ↔ AI)
1. Describe intent / constraints
2. AI proposes structure or patch
3. Human reviews diff & plays game
4. AI updates docs & log (traceability)
5. Iterate until behavior & clarity align

---
## 5. Prompt Engineering Patterns
| Prompt Type | Example | Output |
|-------------|---------|--------|
| Conversion | "Map Godot obstacle spawning to Python" | Factory + manager draft |
| Refactor | "Separate score speed from movement speed" | Introduced `base_speed` vs `speed` |
| Enhancement | "Add halfspeed & doublegold powerups" | Timed dict logic + HUD update |
| Documentation | "Create design pattern table" | DESIGN_PATTERNS.md |

---
## 6. AI Tooling & Artifacts
- `AI_LOG.md`: Immutable chronological trace
- `PLAN.md`: Living roadmap with checkmarks
- Generated docs: patterns, OOP analysis, slide outline
- Diff-based edits → minimal unrelated churn

---
## 7. OOP & Patterns via AI Guidance
Implemented / scaffolded:
- Factory (obstacle instantiation)
- Proto Strategy (speed progression formula abstraction candidate)
- Future hooks: Observer (EventBus), State objects, Command input layer

---
## 8. Powerup Feature Ideation
- Human: need slowdown without score penalty
- AI: propose dual-speed model (`base_speed` vs `speed`)
- Human validated fairness in gameplay
- Extension path: polymorphic `PowerupEffect` classes (future)

---
## 9. Ensuring Correctness
| Risk | Mitigation (AI + Human) |
|------|-------------------------|
| Hallucinated APIs | Always cross-check with Pygame docs / runtime tests |
| Hidden regressions | Small, isolated patches; manual playtest after core changes |
| Drifting docs | AI updates README / pattern docs immediately post-change |
| Over-abstraction | Defer patterns until a second use case appears |

---
## 10. Randomness & Reproducibility
- AI suggested factory wrapper → place to inject seed
- Potential next step: deterministic test harness with fixed RNG
- Facilitates replay-based regression detection

---
## 11. Documentation Automation
- AI-generated: DESIGN_PATTERNS.md, OOP_ANALYSIS.md, Slide.md
- Structured logs enable future fine-tuning or audit
- Reduces onboarding ramp for new contributors

---
## 12. Refactor Roadmap (AI Proposed)
1. Extract `DifficultyStrategy` interface
2. Implement `EventBus` for powerup & score events
3. Introduce `GameState` classes (menu / playing / game over)
4. Formalize `PowerupEffect.apply/expire`
5. Command-based input for remapping & AI bots

---
## 13. Productivity Metrics (Qualitative)
| Aspect | Manual Estimate | AI-Assisted Reality |
|--------|-----------------|---------------------|
| Initial architecture draft | 3–4 hrs | < 45 min |
| Powerup system concept → code | 1 hr | ~10 min |
| Documentation compilation | 2 hrs | < 30 min |

---
## 14. Risk & Ethical Considerations
- Attribution: Preserve original authorship context (Godot base)
- Accuracy: Encourage verification of physics constants
- Maintainability: Avoid cryptic AI one-liners; keep clarity priority
- Data Leakage: No external secret usage (local assets only)

---
## 15. Future AI Enhancements
- Auto test generation for collision & spawning
- Performance profiling suggestions (blit counts, frame timing)
- Procedural obstacle wave designer via prompt
- Automated balancing experiments (vary speed curves)

---
## 16. Replicating This AI Workflow
Minimal checklist:
1. Establish PLAN.md + logging convention
2. Use incremental prompts (one concern each)
3. Demand diffs, not full rewrites
4. Validate in runtime loop frequently
5. Keep AI as reviewer + generator, not unchecked committer

---
## 17. High-Quality Prompt Examples
"Refactor scoring so slowdown powerup doesn’t reduce score; keep difficulty scaling stable."
"Draft EventBus interface; list 5 initial events for this runner."
"Compare pros/cons of Strategy vs simple conditional for difficulty evolution." 

---
## 18. Closing
- GenAI accelerated translation + feature ideation
- Human oversight ensured fidelity & balance
- Foundation ready for deeper automated tooling rounds

---
_End of AI-focused deck._
