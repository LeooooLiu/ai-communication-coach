# v0.2.0 release verification

Verified on 2026-09-27.

## Public release

- Tag commit: `81747c66fec4716b05192bdf5899182a1c1b750b`
- Release: [AI Communication Coach v0.2.0](https://github.com/LeooooLiu/ai-communication-coach/releases/tag/v0.2.0)
- Release assets: portable Plugin ZIP and a separate SHA-256 file
- Private vulnerability reporting: enabled

## Package gates

- Public package validator: 23 general cases, 10 real-conversation cases, 11 theory sources.
- Portable Agent Plugins manifest: valid against the vendored 1.0.0 schema.
- Codex compatibility manifest: passed the bundled `plugin-creator` validator.
- Generated Plugin tree: synchronized with canonical sources, 21 files.
- Release ZIP: all entries decompressed successfully.
- Published ZIP checksum: matched `a491da0351b476163fa502d862da5937f8865b1d05dc1d7bce492dbbed64878d`.

## Distribution gates

- Direct root Skill installation from public `main`: passed in a clean temporary destination; the installed `SKILL.md` matched the release candidate.
- Git-backed remote marketplace installation from public `main`: installed and enabled Plugin version `0.2.0` in an isolated Codex home.
- Published Release ZIP: installed through an isolated local marketplace after download and checksum verification.

## Behavior gates

- GPT-6 Luna real-conversation run and focused regression: [report](../evals/runs/2026-09-27-gpt-6-luna.md).
- GPT-6 Luna and GPT-5.6 Sol context reconstruction: [report](../evals/runs/2026-09-27-cross-model-context.md).
- Three real two-turn disposable workspace tasks: [report](../evals/runs/2026-09-27-multiturn-workspaces.md).
- Published Release asset positive and negative activation: [report](../evals/runs/2026-09-27-release-artifact.md).

The evidence supports the listed model configurations, host, and cases. It does not establish identical behavior for every model, language, or host.
