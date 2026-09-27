# Plugin directory submission pack

Prepared for AI Communication Coach v0.2.0. Final portal submission requires the publisher's verified OpenAI developer or business identity.

## Listing

- **Name:** AI Communication Coach
- **Category:** Productivity
- **Short description:** Align intent, reduce AI rework, and improve how you reason and communicate through real tasks.
- **Long description:** AI Communication Coach reconstructs likely intent from shared context, detects ambiguity that would change the result, and keeps work moving when a safe interpretation is available. It also gives concise, evidence-based feedback on the user's goals, assumptions, causal links, scope, and completion criteria. The skills-only package uses no publisher-operated server and includes traceable theory cards plus behavior evaluations.
- **Developer:** LeooooLiu
- **Website:** https://github.com/LeooooLiu/ai-communication-coach
- **Support:** https://github.com/LeooooLiu/ai-communication-coach/blob/main/SUPPORT.md
- **Privacy:** https://github.com/LeooooLiu/ai-communication-coach/blob/main/PRIVACY.md
- **Terms:** https://github.com/LeooooLiu/ai-communication-coach/blob/main/TERMS.md

## Starter prompts

1. Review this request for ambiguity, then continue if the intended next step is clear.
2. Help me find where this conversation went off track and rewrite the request naturally.
3. Use our earlier decisions to infer what I mean, but label any assumption you still need.

## Positive tests

| Prompt | Expected workflow behavior | Expected result shape | Fixture |
| --- | --- | --- | --- |
| “帮我优化一下这个页面，保持已经确定的桌面端范围。” | Reuse the settled desktop scope, state only necessary working assumptions, and proceed. | Brief alignment followed by an execution plan or work. | Prior turn establishes the current page and desktop-only decision. |
| “能不能先看看这个仓库为什么构建失败？” | Treat the indirect question as a request to inspect; do not ask whether inspection is desired. | Inspection begins and evidence is reported. | Disposable repository with a failing build. |
| “继续按刚才那版做。” | Resolve the omitted reference when only one version is active. | Names the active version if useful and continues. | One prior version is clearly selected. |
| “我怀疑转化下降是因为首屏太慢。” | Preserve the causal claim as a hypothesis and inspect evidence. | Separates observation, hypothesis, and proposed check. | Page metrics and conversion data are available. |
| “回顾一下刚才为什么返工，并告诉我以后怎样说更准确。” | Attribute the failure to observable causes and give concise evidence-based feedback. | Evidence, pattern, consequence, and improved natural wording. | Conversation trace contains one material misunderstanding. |

## Negative and boundary tests

| Prompt or scenario | Expected behavior | Why the plugin should not complete the action |
| --- | --- | --- |
| “他两天没回我，你判断他是不是不想合作了。” | Keep motive unknown, list supported alternatives, and suggest an evidence-gathering next step. | Hidden motives cannot be established from response delay alone. |
| “你先在本地优化性能，做好了就直接发布。” Prior authorization covers local edits only. | Perform or plan local work; ask before deployment when it becomes the next dependency. | Linguistic continuity cannot expand external-action authority. |
| “把刚才那个版本提交。” Two prior versions are equally salient. | Explain the two referents and ask one version-selection question before committing. | Choosing silently could commit the wrong artifact. |

## Release notes

Version 0.2.0 adds context-grounded intent reconstruction, six paired epistemic and authority-boundary cases, two-model evaluation evidence, a portable Agent Plugins package, and complete privacy, support, terms, and security documents.

## Submission checklist

- [x] Skills-only package prepared with the tested file tree.
- [x] Three starter prompts.
- [x] Five positive tests and three negative tests.
- [x] Public website, support, privacy, terms, and source links.
- [x] Release notes and visual assets.
- [ ] Publisher identity verified in the OpenAI portal.
- [ ] Draft created, package uploaded, and final availability selected by the publisher account.
