# Diagnostic Framework

Use this reference for complex requests, repeated misunderstandings, or a detailed coaching session. Select the relevant checks instead of treating the list as a required form.

## Understanding risk

Choose the interaction level by execution impact:

- **Clear:** There is one practical reading. Start.
- **Inferable:** Context supports a safe, reversible reading. State it briefly and start without asking.
- **Branching:** Plausible readings would change the deliverable, architecture, scope, cost, evaluation standard, or external or difficult-to-reverse action. Present the alternatives, impact, and recommendation, then ask for one decision.

Use a counterfactual check: “If the user intended the other plausible reading, would they reject or substantially redo the result?” A yes indicates branching. Ordinary implementation details and cheap reversible choices are inferable.

## Conversational state

Do not diagnose every message as a specification problem:

- **Execution:** A result or action is expected; use the full diagnostic framework.
- **Exploration:** The useful output may be alternatives, questions, or a provisional model. Ambiguity about the final choice is allowed when selecting that choice is not yet the task.
- **Reflection:** The message may seek understanding rather than correction or action. Respond to its content before offering any calibration.
- **Repair:** Establish whether the user is correcting an AI inference, adding missing evidence, or changing a previous decision. These have different causes even when the new instruction is identical.

## 1. Intent

- What change does the user want in the world, product, document, or decision?
- Is the stated method the real goal, or one possible route?
- Why does the result matter now?

Common failure: the AI optimizes the proposed method while missing the desired outcome.

## 2. Deliverable

- Does the user want analysis, a plan, implementation, revision, a file, a decision, or an external action?
- What form should the result take?
- Who will use it?

Common failure: words such as “看看”“处理一下”“设计一下” permit several completion levels.

## 3. Context and evidence

- What has already happened?
- Which files, messages, examples, or facts are authoritative?
- Which statements are verified facts, working assumptions, preferences, or ideas?

Common failure: background is mistaken for a requirement, or an idea is treated as a confirmed decision.

## 4. Scope and constraints

- Which project, time range, audience, platform, or artifact is in scope?
- Which constraints materially shape the solution?
- Are exclusions real requirements or only anticipated concerns?

Common failure: the AI expands a local request into a broad redesign, or obeys an incidental example as a universal rule.

## 5. Priorities and tradeoffs

- What matters most: speed, accuracy, cost, polish, reversibility, learning, or coverage?
- Which quality can be reduced when priorities conflict?
- Is the user asking for exploration or convergence?

Common failure: the AI chooses a reasonable tradeoff that differs from the user's unstated priority.

## 6. Authority and action boundary

- Is the AI authorized to inspect, edit, commit, publish, purchase, message, deploy, or delete?
- Which actions require a user decision because they create external or difficult-to-reverse state?

Common failure: review is interpreted as implementation, or implementation is stopped at advice.

## 7. Completion and feedback

- What observable result counts as done?
- What evidence should support the conclusion?
- Who reviews the result, and what would cause another iteration?

Common failure: the AI stops after a plausible first pass because completion was never defined.

## Selecting questions

Rank missing information by decision impact:

- Ask once about choices that create materially different deliverables, architectures, costs, evaluation standards, or external consequences. Show plausible interpretations and recommend one first.
- Ask once for a required input, dependency, or authority that cannot be discovered and without which dependent work cannot continue.
- State the working interpretation for choices that are reversible and easy to revise, then proceed without confirmation.
- Discover information directly when the user has already placed the relevant source in scope.
- Ignore wording imperfections that do not change the work.

## Multi-turn continuity

- Treat earlier user decisions as active context until the user changes them or new evidence creates a conflict.
- Distinguish refinement from reversal: adding detail narrows a decision; choosing a different outcome replaces it.
- When the user corrects the AI, repair the inference and continue instead of converting the correction into coaching feedback about the user.
- Surface only conflicts that still affect the next action.

## Attribution before coaching

Locate the source of the difficulty before giving feedback:

- **User expression:** the wording or reasoning permits materially different actions. Calibrate the specific expression.
- **Missing shared context:** the intent may be clear, but a file, destination, credential, or prior decision is unavailable. Request or discover the dependency.
- **AI error:** the request was sufficient and the AI inferred or executed incorrectly. Own and repair the error.
- **Model or tool limit:** the requested judgment requires knowledge, access, or capability the AI does not currently have. Retrieve, inspect, or state the concrete boundary.
- **External uncertainty:** the evidence itself is incomplete or disputed. Preserve the uncertainty and explain what evidence would resolve it.

Only the first category is evidence of a communication pattern in the user's request. The same visible failure can have different causes, so diagnose from the conversation record rather than the outcome alone.

## Reasoning patterns to correct

Choose the pattern tied to the observed problem:

- outcome before method;
- fact, assumption, preference, and decision are different categories;
- dependencies determine task order;
- constraints matter only when they change a choice;
- priorities resolve tradeoffs;
- completion needs observable evidence;
- feedback should update the next request, not merely judge the previous result.

## Feedback dimensions

Use these dimensions to explain the user's current strengths and highest-impact correction. Assess only dimensions visible in the request.

- **Goal formation:** The intended change is distinct from the proposed method.
- **Information hierarchy:** Necessary context is separated from motivating background and incidental detail.
- **Epistemic clarity:** Facts, assumptions, preferences, hypotheses, and decisions are labeled by their function.
- **Decomposition:** Subtasks follow real dependencies and can be verified independently.
- **Priority:** Tradeoffs have an explicit ordering or decision rule.
- **Completion:** Success is observable and tied to evidence.
- **Iteration:** Feedback from the last result changes the next request.

Describe what is effective, what remains implicit, and the more accurate reasoning or wording. Avoid global judgments about intelligence, competence, or communication ability.
