# AI 沟通教练 Plugin directory submission pack

Prepared for AI 沟通教练 (AI Communication Coach) v0.2.1. Final portal submission requires the publisher's verified OpenAI developer or business identity.

## Listing

- **Name:** AI 沟通教练｜AI Communication Coach
- **Category:** Productivity
- **Short description:** 优化提示词与需求表达，让 AI 更准确理解并减少返工。
- **Long description:** AI 沟通教练面向中文用户的提示词优化、需求澄清和人机协作场景。它从共享上下文重建最可能的意图，识别会改变结果的歧义，并在可以安全推断时继续工作；同时基于真实任务反馈目标、假设、因果、范围和完成标准中的表达问题。Skill-only 包不使用发布者服务器，并附有可追溯理论卡片与行为评测。
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

Version 0.2.1 makes “AI 沟通教练” the primary public name and adds Chinese discovery language for AI communication, prompt optimization, requirement clarification, human-AI collaboration, and reasoning clarity. It preserves the tested behavior and stable `ai-communication-coach` technical identifier from v0.2.0.

## Submission checklist

- [x] Skills-only package prepared with the tested file tree.
- [x] Three starter prompts.
- [x] Five positive tests and three negative tests.
- [x] Public website, support, privacy, terms, and source links.
- [x] Release notes and visual assets.
- [ ] Publisher identity verified in the OpenAI portal.
- [ ] Draft created, package uploaded, and final availability selected by the publisher account.
