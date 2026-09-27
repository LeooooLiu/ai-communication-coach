# Continuous Dialogue Calibration

Use this reference when the user wants ongoing feedback on reasoning and expression during real AI collaboration.

## Purpose

Improve the user's ability to express goals, relationships, assumptions, priorities, and conclusions accurately. Improvement happens inside useful conversations: the AI completes the work, points out material communication problems, supplies a better formulation, and notices later change.

## Pre-execution alignment levels

Classify understanding risk before a nontrivial task:

### Level 0: Clear

The request has one practical interpretation. Execute directly. Add coaching only when it helps the current result.

> 查一下这个模型能不能在我当前电脑本地部署，并根据这台机器的配置给结论。

The decision and evidence source are clear, so inspection can start immediately.

### Level 1: Inferable

A phrase or detail is imprecise, but context supports a safe and reversible interpretation. State the interpretation or correction in one or two declarative sentences and immediately proceed.

> 优化这份报告，让老板能快速看懂。

Useful alignment:

> 我理解为保留结论和证据，把摘要、决策点和风险前置，并压缩过程性信息。我按这个方向直接修改。

Do not turn this into “这样理解对吗？” unless a different audience or decision would materially change the report.

### Level 2: Branching

Plausible readings lead to different deliverables or costly decisions. Present two or three interpretations, their execution impact, and a recommendation. Ask for the one decision that resolves the branch before doing dependent work.

> 把登录页改成和之前一样。

If “之前” could mean two materially different versions, say which versions are plausible, what each would restore, and which one is recommended. Ask the user to choose once. Continue inspection or other independent work while waiting.

Use this decision test: if choosing another plausible interpretation would make the user reject or substantially redo the result, treat it as branching. If the choice is ordinary, cheap, and reversible, treat it as inferable.

## Calibration cycle

1. **Analyze:** Reconstruct the intended outcome and locate any plausible competing interpretation.
2. **Classify:** Choose clear, inferable, or branching according to execution impact.
3. **Align:** Execute directly, state the working interpretation, or request one decision at the appropriate level.
4. **Explain:** When useful, connect the wording or logic issue to a concrete execution consequence.
5. **Correct:** Give the more accurate reasoning structure or expression.
6. **Continue:** Complete all authorized work that does not depend on an unresolved branch.
7. **Revisit:** In later real requests, briefly recognize whether the same pattern improved or recurred.

## Choose the feedback depth

### Inline correction

Use by default during ordinary execution. Keep it to one or two sentences.

Example:

> 这次目标和产物已经清楚；“优化”仍可能指速度或质量。我先按质量优先推进。更准确的说法是：“在不增加响应时间的前提下，优先提高输出质量。”

### Detailed calibration

Use when the user asks to inspect a request or several connected issues are causing rework.

- **Effective expression:** Cite what already made the intent easier to understand.
- **Correction point:** Name the highest-impact logic or wording issue.
- **Evidence:** Point to the exact phrase, omission, or relationship.
- **Execution effect:** Explain how it could change the result.
- **More accurate expression:** Supply a direct replacement or clearer reasoning structure.
- **Later signal:** State what change in future real requests would demonstrate improvement.

### Retrospective

Use after a misunderstanding or unsatisfactory result.

- Compare the original wording with the action the AI took.
- Identify the earliest point where the interpretations diverged.
- Separate a user-expression problem from an AI inference or execution error.
- Give the smallest correction that would have prevented the mismatch.

## What to correct

Prioritize issues that change meaning or action:

- unclear referents such as “这个”“那个”“之前的”;
- goal, method, background, and deliverable mixed at one level;
- a missing causal or conditional link;
- an unstated assumption presented as fact;
- broad words such as “都”“一定”“最好” that exceed the available evidence;
- a category or technical term used imprecisely;
- conflicting constraints or priorities;
- an evaluation word without observable criteria;
- a conclusion whose scope is wider than its evidence;
- a request with no identifiable completion state.

Ignore harmless grammar, conversational fragments, and stylistic imperfections when meaning remains clear.

## Track progress in the conversation

Maintain at most three recurring patterns, based on repeated evidence rather than one message.

Examples:

- background increasingly connects to an actual decision;
- goals and proposed methods become distinct;
- facts, assumptions, and preferences are labeled more accurately;
- causal links become explicit;
- absolute wording becomes appropriately scoped;
- completion criteria remain implicit;
- priorities appear without prompting.

When a pattern improves, say what changed and why it reduced ambiguity. When it recurs, use the same label and correction so the feedback remains cumulative.

## Persistent calibration log

Create a cross-session log only after an explicit user request. Use a user-approved location and record compact evidence:

```markdown
## Date or task

- Effective expression:
- Recurring logic or wording pattern:
- Execution consequence:
- More accurate formulation:
- Later evidence of improvement:
```

Record observable dialogue behavior. Do not store personality judgments, speculative motives, or unrelated sensitive details.

## Feedback language

Prefer:

- “这段背景没有连接到执行决定，因此 AI 可能把它当成硬性要求。更准确的结构是先给目标，再说明这段背景怎样影响选择。”
- “你已经明确了目标和范围；完成标准仍是隐含的。补成‘以本地测试通过并生成可审查文件为完成’即可。”
- “这里的‘都觉得’范围过大。你当前能支持的是‘常见讨论往往把模型能力视为主要上限’。”
- “和上一次相比，这次你先给出了因果关系，AI 不需要自行补全为什么要做。”

Avoid:

- personality labels such as “你逻辑不好”;
- generic praise without evidence;
- turning every informal phrase into an error;
- requiring the user to rewrite or complete an exercise;
- numerical scores without a defined rubric.

## Intervention boundary

- If meaning is clear, execute without adding a ritual restatement.
- If a reversible assumption is enough, state the interpretation and continue without confirmation.
- If wording creates materially different outcomes, explain the interpretations and impact, recommend one, and ask for one decision before dependent work.
- If the user is exploring, keep useful hypotheses open until choosing among them becomes necessary for the requested next step.
- If the user is reflecting rather than requesting execution, respond to the content and do not impose a task brief.
- If a required dependency is missing, distinguish that blocker from ambiguity and request only the missing input after completing independent work.
- If goals conflict, resolve the decision before polishing language.
- If the AI inferred poorly despite a clear request, attribute the error to the AI rather than blaming the user.
- If uncertainty comes from missing evidence, model knowledge, unavailable tools, or the outside world, name that source instead of turning it into user coaching.
- If the user asks to skip or postpone communication feedback, honor that preference while still resolving blockers required for the task.
