# Behavioral evaluation

`behavioral-cases.json` defines general release cases. `real-conversation-cases.json` contains anonymized cases derived from actual project conversations. The cases test behavior rather than exact wording.

## Release rule

- No critical failure in clear, inferable, branching, missing-dependency, action-boundary, attribution, preference, conflict, or AI-owned-repair cases.
- Minor wording differences are acceptable when the expected action and interaction cost remain correct.
- Evaluate with at least one model configuration before a public release; use multiple models when claiming broad portability.
- Grade the response the user actually sees. Internal state labels and self-reported metadata are diagnostic evidence, not pass criteria when the visible action is correct.

Structural validation of the JSON does not prove model behavior. Record model, date, outcome, and observed failure separately when an evaluation is run.

## Recorded runs

- [GPT-6 Luna, 2026-09-27](runs/2026-09-27-gpt-6-luna.md): ten real-conversation cases, focused regression, and an implicit-routing simulation.
- [Cross-model context reconstruction, 2026-09-27](runs/2026-09-27-cross-model-context.md): six paired context cases on GPT-6 Luna and GPT-5.6 Sol, plus the real-conversation suite on a second model family.
- [Multi-turn disposable workspaces, 2026-09-27](runs/2026-09-27-multiturn-workspaces.md): three two-turn tool-using tasks covering staged discovery, scope continuity, and review-before-edit boundaries.
