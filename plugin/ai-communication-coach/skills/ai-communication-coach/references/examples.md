# Examples

Use these examples to calibrate coaching depth. Preserve the user's natural voice rather than copying the formats mechanically.

## Example 1: Designing a reusable skill

### Rough request

> 帮我设计一个教我和 AI 好好说话的 Skill。我很多需求说得不到位，你要看哪里容易误解，教我怎么表达，提高我的思维逻辑和沟通效率。这个方向也适合分享，因为 AI 可以帮助人提升基础能力。

### Likely intent

Create a reusable coaching Skill that diagnoses ambiguity, rewrites requests, and teaches transferable reasoning habits.

### Material ambiguity

- “设计” may mean a concept document, a finished local Skill, or a publishable repository.
- The invocation policy is unstated: every request, automatic selection for coaching requests, or explicit invocation only.
- “提升思维逻辑” needs observable coaching behavior rather than a broad aspiration.

### Useful working interpretation

Create a finished local Codex Skill with automatic discovery for communication-calibration requests. Make its source self-contained and suitable for later sharing. Improve goal definition, decomposition, evidence, priorities, and completion criteria through concise feedback on real requests.

### Improved request

> 请创建一个可复用、以后可以公开分享的 Codex Skill，暂名 `ai-communication-coach`。它用于审视我发给 AI 的需求，指出会导致不同执行结果的歧义，解释 AI 可能怎样理解，并给出更准确、可直接执行的说法。它还要在真实对话中持续指出影响理解的思维结构和措辞问题，例如混淆目标与手段、事实与假设、优先级与完成标准。普通任务继续推进，不设置练习或额外教学流程。请交付完整 Skill 文件并用我这段需求做一次验证。

### Transferable lesson

Separate the product's purpose, activation condition, observable behavior, and deliverable. A motivating belief becomes useful to execution only after it changes one of those decisions.

### Feedback to the person

- **What worked:** The user identified a recurring pain, the desired capability, and a broader reason the product matters.
- **Growth edge:** The request mixed product philosophy, behavior, and delivery level without ranking them.
- **Execution effect:** The AI could produce a concept note, a local Skill, or a public package and still believe it had completed the task.
- **More accurate pattern:** End an exploratory request with one sentence naming the immediate deliverable and what can wait.

## Example 2: A vague implementation request

### Rough request

> 帮我把这个页面优化一下，感觉还不够高级。

### Competing interpretations

- Improve visual taste while preserving the current information architecture.
- Redesign the page structure, copy, interaction, and visual system.

These readings produce different scope and review criteria.

### Focused coaching

This is branching because the two readings change both scope and review criteria. Explain the two directions, recommend preserving the information architecture unless a broader redesign is intended, and ask for that single scope decision before dependent design work.

### Improved request

> 保留当前信息结构，优化这个桌面页面的视觉层级、字体、留白和色彩，让它更接近克制、编辑感强的工具界面。先指出三个最影响质感的问题，再直接修改并给我浏览器截图。交互逻辑和文案内容不在本次范围内。

### Transferable lesson

Convert an adjective into observable design dimensions and define which layers may change.

### Feedback to the person

- **What worked:** The user identified dissatisfaction and the artifact to improve.
- **Growth edge:** “高级” expresses a judgment but provides no observable comparison rule.
- **More accurate pattern:** Translate evaluative words into two or three visible properties or references.

## Example 3: A request that is already sufficient

### Request

> 查一下这个模型能不能在我当前电脑本地部署，并根据这台机器的配置给结论。

### Coaching response

This is actionable. The AI can inspect the machine, check current official model information, and report feasibility. Output depth is a reversible presentation choice, so it does not justify a clarification question.

### Transferable lesson

A useful request does not need to specify every step. State the outcome, place the evidence source in scope, and let the AI choose ordinary execution details.

### Feedback to the person

- **What worked:** The request names the decision, the machine-specific context, and the evidence needed for the conclusion.
- **Correction needed:** None for execution; add constraints only if time, storage, or acceptable performance matters to the decision.

## Example 4: Closing a one-way coaching loop

### User feedback

> 现在只是让 AI 更好地理解人，还没有反过来让人理解和提升。需要增加对人的反馈，才能不断改善逻辑和对话方式。

### What the user reasoned effectively

The user identified the system's missing feedback direction, explained why the omission matters, and connected the proposed feature to a longer-term capability outcome. This is enough to justify a revision.

### Remaining design choices

- Feedback could target wording, task structure, reasoning habits, or all three.
- “不断优化” could mean progress within one conversation or persistent tracking across sessions.
- Frequent feedback could become disruptive unless its depth adapts to the task.

### Useful working interpretation

Give evidence-based feedback on observable reasoning habits, provide the corrected formulation inside the real conversation, recognize change later, and require explicit authorization before writing a persistent learning log.

### Improved request

> 请把 Skill 从单向的需求澄清升级为持续对话校准系统。除了帮助 AI 准确理解和执行，它还要基于我原始表达中的具体证据，反馈有效的思考动作、最需要纠正的逻辑或措辞、它对执行造成的影响，以及更准确的表达。在后续真实对话中识别这些模式是否改善；跨会话记录只在我明确要求时启用。反馈深度要与任务匹配，不设置练习或额外教学流程。

### Feedback to the person

- **What worked:** The critique moved from a feature observation to a causal model: one-way understanding cannot produce sustained human improvement.
- **Growth edge:** The desired feedback mechanism and progression evidence remained implicit.
- **More accurate pattern:** When proposing a feedback loop, specify the observed behavior, correction, later behavior, and evidence that improvement occurred.

## Example 5: Aligning before execution without creating approval friction

### Rough request

> 我给你需求后，你先说说自己的理解。严重歧义就让我选，不严重就纠偏后继续做，帮助我以后说得更清楚。

### Likely intent

Move communication feedback before execution and scale the interaction according to whether ambiguity would actually change the result.

### Understanding risk

This request is inferable. “严重”和“不严重” are not yet operational terms, but the surrounding explanation supplies a workable distinction: whether plausible readings create materially different execution paths.

### Useful pre-execution alignment

> 我理解为把开工前对齐分成三级：信息明确时直接执行；细节可合理推断时，陈述理解和假设后立即开工；不同理解会让交付方向分叉时，列出解释、影响和推荐项，请你选择一次。我会按这个机制更新 Skill 和全局规则。

Then start the edit. Do not ask the user to approve this restatement.

### Feedback to the person

- **What worked:** The request distinguishes an alignment statement from a confirmation request and connects the distinction to reducing rework.
- **Precision gain:** “轻重等级” becomes easier to apply when named “理解风险等级,” with severity defined by execution impact.
- **More accurate pattern:** State the trigger, the AI behavior, and whether work waits for a user decision.

## Example 6: Exploration should not be forced into a decision

### Request

> 我在想这个 Skill 是更适合做成一个日常助手，还是专门用来复盘失败的对话，你帮我一起想想。

### Correct handling

The requested deliverable is exploration. Keep both product directions visible, compare their users and tradeoffs, and identify what evidence would distinguish them. Do not ask the user to choose one before the comparison has been produced.

### Communication feedback

None is required. The open alternatives are intentional and useful to the task.

## Example 7: A missing dependency is not an interpretation branch

### Request

> 把整理好的公告发给项目群。

### Context

The announcement exists, but the target group cannot be identified from available context.

### Correct handling

Finish the announcement and any other independent checks. Then state that the destination is the remaining required input and ask for the exact group once. Do not invent several meanings for the content request, and do not repeatedly ask whether the user wants the message sent.

### Transferable lesson

An ambiguity permits different meanings. A missing dependency leaves the intended action understandable but impossible to complete.

## Example 8: A changed decision is not faulty reasoning

### Earlier decision

> 这次只改桌面端。

### Later instruction

> 我看完桌面效果了，移动端也一起改吧。

### Correct handling

Treat the later instruction as an explicit scope expansion. Update the active scope, state the added work when useful, and continue. Do not criticize the user for inconsistency or ask them to reconfirm the earlier desktop decision.
