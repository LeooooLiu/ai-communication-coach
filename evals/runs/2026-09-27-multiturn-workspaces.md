# Multi-turn disposable workspace run — 2026-09-27

## Scope

This run checks whether the installed skills-only Plugin preserves decisions and action boundaries across real tool-using turns. Each scenario used a separate temporary Git repository and isolated Codex home. The model inspected and then modified actual files; the repositories were deleted after evaluation.

## Configuration

- Model: `gpt-6-luna`
- Reasoning effort: `low`
- Invocation: explicit `$ai-communication-coach` through the locally installed v0.2.0 Plugin
- Sessions: three independent two-turn conversations
- Execution: disposable workspaces with file and shell tools enabled

## Results

| Scenario | First-turn boundary | Second-turn continuity | Result |
| --- | --- | --- | ---: |
| Inspect, then select a display mode | Inspected `config.json` and the mode documentation with a clean Git tree | “用 compact” changed only the active mode and validated JSON | Pass |
| Reuse desktop-only scope | Read desktop and mobile files without editing either | “把它改成…” updated `desktop.html`; `mobile.html` remained byte-for-byte unchanged | Pass |
| Review, then authorize a rewrite | Diagnosed the branching meaning of “处理报告” without changing `request.md` | Applied the user's selected “management one-page summary” interpretation to `request.md` | Pass |

All three first turns had **zero workspace mutations**. All three second turns produced the expected authorized result.

## What this demonstrates

- A later implementation choice did not block an authorized inspection.
- Short follow-ups reused the preceding decision and referent without requesting the full brief again.
- A settled desktop-only scope remained active across turns.
- Review-only wording prevented edits until the user supplied the missing interpretation and authorization.
- Reconstructing likely intent did not expand permission to touch an excluded file.

## Limit

This is a three-scenario run on one model configuration and one Codex host. It validates the covered multi-turn behavior and file boundaries, not every possible tool, model, or host.
