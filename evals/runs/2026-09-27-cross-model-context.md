# Cross-model context reconstruction run — 2026-09-27

## Scope

This run tests whether the Skill can recover likely intent from incomplete everyday speech while keeping facts, hypotheses, unknowns, and authorization separate. It also reruns the existing real-conversation suite on a second model family.

The evaluation grades the response the user would see. It does not use a model's self-reported state label as the pass criterion.

## Configurations

| Model | Reasoning effort | Suite | Fresh responses |
| --- | --- | --- | ---: |
| `gpt-6-luna` | `low` | six new context-reconstruction cases, two runs each | 12 |
| `gpt-5.6-sol` | `low` | six new context-reconstruction cases | 6 |
| `gpt-5.6-sol` | `low` | ten anonymized real-conversation cases | 10 |

Each response came from an isolated Codex CLI session with explicit Skill invocation. Side effects were disabled; the run captured the first response before execution.

## Context-reconstruction result

Both models passed every tested response:

- `gpt-6-luna`: **12/12**
- `gpt-5.6-sol`: **6/6**

The passing behavior included:

- resolving an omitted reference from one clearly active prior direction;
- treating “能不能先看看” as a request to inspect rather than a capability question;
- asking once when two earlier versions were equally plausible referents;
- retaining a causal explanation as a hypothesis rather than turning it into fact;
- declining to invent a hidden motive from a delayed reply;
- carrying forward local performance work without inventing permission to deploy.

## Second-model real-conversation result

The first pass produced **9/10** acceptable responses. The one failure involved this fixture text:

> “这个最近发布的模型我可以在本地部署吗？”

The fixture had replaced the public model name during anonymization. Asking for the missing model was therefore correct for the text the evaluator supplied, but it no longer represented the original conversation. The fixture was repaired to retain “MiniMax H3,” a public, decision-relevant referent, and the focused rerun passed.

After correcting the fixture, `gpt-5.6-sol` passed **10/10** real-conversation cases.

This exposed an evaluation design rule: privacy editing should remove personal information while preserving referents that determine the correct action.

## Timing

The isolated CLI calls took roughly 120–132 seconds end to end in this environment. The run did not separate model latency, process startup, and evaluation harness overhead, so timing is recorded as an observation and excluded from the behavior score.

## Conclusion

The tested behavior is consistent across these two model configurations for the covered cases. This is evidence for context reconstruction, question discipline, epistemic boundaries, and authorization boundaries. It is not a claim that every model, host, language, or untested conversation will behave identically.
