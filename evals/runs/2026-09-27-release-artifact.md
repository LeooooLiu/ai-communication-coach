# Published release artifact activation run — 2026-09-27

## Scope

This run verifies the exact Plugin ZIP downloaded from the public v0.2.0 GitHub Release. The archive was checked against its separately published SHA-256 file, extracted into an isolated local marketplace, installed into a clean Codex home, and exercised with one positive and one negative activation case.

## Artifact

- Release: [AI Communication Coach v0.2.0](https://github.com/LeooooLiu/ai-communication-coach/releases/tag/v0.2.0)
- Asset: `ai-communication-coach-plugin-v0.2.0.zip`
- SHA-256: `a491da0351b476163fa502d862da5937f8865b1d05dc1d7bce492dbbed64878d`
- Archive entries tested: 21
- Installed Plugin version: `0.2.0`

## Configuration

- Model: `gpt-6-luna`
- Reasoning effort: `low`
- Host: Codex CLI
- Sessions: two fresh ephemeral sessions using the Plugin installed from the release ZIP

## Cases

### Positive activation

The prompt explicitly invoked the Skill and stated that “continue with the previous version” could refer to either a desktop or mobile candidate.

The response asked for the single material choice: desktop or mobile. It did not select a version silently or add unrelated questions.

**Result: Pass**

### Negative activation

The prompt asked to translate `hello` into Chinese and return only the translation, without invoking the Skill.

The complete response was `你好`. It added no alignment ceremony or communication coaching.

**Result: Pass**

## Conclusion

The published v0.2.0 asset passed integrity, installability, positive-use, and quiet-negative-use checks in the tested environment.
