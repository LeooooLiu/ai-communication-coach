# Behavioral evaluation

`behavioral-cases.json` defines realistic cases for release review. The cases test behavior rather than exact wording.

## Release rule

- No critical failure in clear, inferable, branching, missing-dependency, action-boundary, attribution, preference, conflict, or AI-owned-repair cases.
- Minor wording differences are acceptable when the expected action and interaction cost remain correct.
- Evaluate with at least one model configuration before a public release; use multiple models when claiming broad portability.

Structural validation of the JSON does not prove model behavior. Record model, date, outcome, and observed failure separately when an evaluation is run.
