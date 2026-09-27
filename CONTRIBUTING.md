# Contributing

Thanks for helping make AI Communication Coach more accurate and less intrusive.

## What makes a useful contribution

The project values changes that improve observable dialogue behavior:

- a real ambiguity or reasoning pattern that changes execution;
- a case where the Skill asks too much, asks too little, or attributes the problem incorrectly;
- a tighter operational rule that models can follow;
- a traceable source that changes an existing judgment;
- a behavioral case that exposes a concrete failure.

General advice without an execution consequence is unlikely to belong in the core Skill.

## Before opening a pull request

1. Keep `SKILL.md` focused on rules needed during ordinary use.
2. Put detailed explanation, examples, or theory in the matching `references/` file.
3. Add or update a case in `evals/behavioral-cases.json` when behavior changes.
4. Do not commit `research/.local-corpus/`, downloaded source documents, credentials, or private conversations.
5. Run:

```bash
uv run --with pyyaml --with jsonschema python scripts/validate_package.py
python3 scripts/build_plugin.py --check
```

## Behavioral case shape

Each case should include:

- a stable `id`;
- the conversational `state`;
- a realistic `prompt`;
- optional context needed to reproduce the decision;
- observable expected behavior;
- one critical failure that would reject the behavior.

Test actions and interaction cost rather than exact prose.

## Source contributions

Add primary or authoritative sources when possible. Record access level and redistribution status in `research/corpus-manifest.json`. A citation supports a particular rule; source count alone is not evidence that the Skill works.

## Privacy

Remove names, credentials, private repository details, and sensitive personal information from dialogue examples before submitting them.
