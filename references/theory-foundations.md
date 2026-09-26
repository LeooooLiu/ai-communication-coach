# Theory Foundations

This reference connects established work on communication, language, argumentation, requirements, and information design to concrete Skill behavior. It is a designed synthesis: the sources support individual diagnostic lenses, while the combined workflow and three-level understanding-risk model are this Skill's operational design.

Research snapshot: 2026-09-27.

## Retrieval order

Use the lightest source layer that can support the judgment:

1. Apply the core rules in `SKILL.md` for ordinary requests.
2. Read this local reference for theory-grounded diagnosis and source mapping.
3. Search the private local corpus with `scripts/search_corpus.py` when exact source detail would change the judgment.
4. Browse the original site only for a source that is unavailable locally, a precise citation or quotation, a theory dispute, or a version update.

The private corpus is defined in [`research/corpus-manifest.json`](../research/corpus-manifest.json) and built with [`scripts/build_corpus.py`](../scripts/build_corpus.py). It uses SQLite FTS5 rather than embeddings at the current scale. Downloaded originals and extracted text remain in a Git-ignored local cache; the public Skill contains the manifest, scripts, and derived theory cards.

## Use the evidence base

Select one primary lens for the observed problem and add a second only when it changes the action. Diagnose observable language and task consequences rather than personality. In normal execution, apply the rule without naming its academic source. Name and link sources when the user asks why, requests a detailed review, or needs material for publication.

| Observed problem | Primary foundation | Operational test | Skill action |
| --- | --- | --- | --- |
| Too little, too much, irrelevant, unclear, or weakly supported information | Grice; Miehling et al. | Is the contribution sufficient for the current purpose, relevant, clear, and evidence-bounded? | Request or supply only the information that changes execution; state real uncertainty once. |
| Unclear referent, missing shared context, or excessive confirmation | Clark and Brennan | Is mutual understanding already sufficient for the current task, and what interaction minimizes combined effort? | Use clear, inferable, or branching alignment; do not ask when a reversible interpretation is enough. |
| An action verb hides the intended act or authority | Austin | Is the user asking the AI to inspect, explain, draft, edit, commit, publish, purchase, or decide? | Name the actual deliverable and action boundary before execution when they differ materially. |
| A misunderstanding has already occurred | Schegloff, Jefferson, and Sacks | Where was the earliest repairable trouble source, and who can repair it with least friction? | Locate the divergence, offer a precise repair, and attribute an AI inference error to the AI when appropriate. |
| A conclusion lacks support or jumps over an assumption | Toulmin | What are the claim, grounds, warrant, qualifier, and relevant exception? | Expose the missing inferential bridge, distinguish evidence from assumption, and narrow the conclusion to its support. |
| A task lacks a precise need, constraint, condition, or completion state | ISO/IEC/IEEE 29148 | Could two implementers produce materially different results while both claiming compliance? Can completion be examined? | Clarify outcome-changing branches; turn completion into observable evidence. |
| The user or audience cannot quickly find, understand, or use the message | ISO 24495-1 | Is the content relevant, findable, understandable, and usable for the intended audience and context? | Put the needed decision first, group related information, and remove content that does not help the reader act. |
| The message contains useful ideas in a flat or indirect order | Minto | Is there one governing point, and do supporting ideas answer the reader's question in a coherent order? | State the conclusion first and organize support beneath it. Do not treat presentation structure as proof that a claim is true. |

## Why the three alignment levels follow from these sources

The model combines three ideas:

1. **Grounding is purpose-relative.** Clark and Brennan define successful grounding by whether people understand one another well enough for the current purpose. Perfect mutual certainty is unnecessary.
2. **Conversation should minimize combined effort.** Their principle of least collaborative effort supports proceeding with safe, reversible interpretations instead of adding confirmation turns by default.
3. **Consequences determine precision.** Requirements engineering distinguishes well-formed, precise needs from statements that permit incompatible implementations. The Skill therefore asks only when plausible readings would materially change the result.

This produces the operational levels:

- **Clear:** one practical reading; execute.
- **Inferable:** a safe, reversible reading exists; state it and execute.
- **Branching:** readings create materially different outcomes; explain them, recommend one, and request one decision before dependent work.

## Source-by-source adoption and limits

### 1. H. P. Grice — “Logic and Conversation” (1975)

- **Adopted:** quantity, quality, relation, and manner as tests for sufficient, evidence-aware, relevant, and clear contributions.
- **Used for:** detecting missing context, irrelevant background, unsupported certainty, and ambiguous wording.
- **Limit:** conversational maxims describe how meaning and implication work; they are not a rigid prompt checklist.
- **Primary text:** [Stanford-hosted paper](https://web.stanford.edu/class/psych205/papers/Grice-1975.pdf).

### 2. Herbert H. Clark and Susan E. Brennan — “Grounding in Communication” (1991)

- **Adopted:** common ground, a grounding criterion sufficient for the current purpose, and least collaborative effort.
- **Used for:** the three alignment levels and the rule that inferable details should not create approval friction.
- **Limit:** the chapter studies human communication across media; applying it to AI dialogue is a design inference.
- **Primary text:** [author-hosted chapter](https://web.stanford.edu/~clark/1990s/Clark,%20H.H.%20_%20Brennan,%20S.E.%20_Grounding%20in%20communication_%201991.pdf).

### 3. J. L. Austin — *How to Do Things with Words* (1962; OUP edition 1975)

- **Adopted:** an utterance performs an act, and its force matters beyond its literal wording.
- **Used for:** distinguishing requests to inspect, advise, create, edit, authorize, publish, or commit.
- **Limit:** speech-act categories identify intended action; they do not supply project-specific authorization.
- **Publisher record:** [Oxford Academic](https://academic.oup.com/book/5162).

### 4. Emanuel A. Schegloff, Gail Jefferson, and Harvey Sacks — “The Preference for Self-Correction in the Organization of Repair in Conversation” (1977)

- **Adopted:** conversational trouble can be located and repaired, with strong preferences for self-initiated and self-produced correction.
- **Used for:** repairing the earliest divergence and letting the AI correct its own inference before burdening the user.
- **Limit:** conversation analysis describes interactional organization; it does not imply that every informal phrase requires correction.
- **Article:** [DOI 10.2307/413107](https://doi.org/10.2307/413107).

### 5. Stephen E. Toulmin — *The Uses of Argument* (1958; updated edition 2003)

- **Adopted:** claims depend on grounds and warrants; qualifiers and rebuttals define the force and limits of a conclusion.
- **Used for:** finding hidden assumptions, missing causal links, overgeneralization, and conclusions broader than their evidence.
- **Limit:** a complete argument structure does not make its premises true; evidence still needs verification.
- **Publisher record:** [Cambridge University Press](https://doi.org/10.1017/CBO9780511840005).

### 6. ISO/IEC/IEEE 29148:2018 — Requirements engineering

- **Adopted:** needs should be expressed with their constraints and conditions in a precise, unambiguous form; validation asks whether the intended system is being defined, while verification examines whether requirements are well formed.
- **Used for:** outcome, scope, constraints, completion criteria, and the branching test.
- **Limit:** the standard targets systems and software engineering. Everyday requests use its principles proportionally rather than becoming full specifications.
- **Standard record:** [ISO Online Browsing Platform](https://www.iso.org/obp/ui/en/#iso:std:iso-iec-ieee:29148:ed-2:v1:en).

### 7. ISO 24495-1:2023 — Plain language

- **Adopted:** communication should help intended readers get relevant information, find it, understand it, and use it.
- **Used for:** audience-aware rewrites, information order, headings, and action-ready outputs.
- **Limit:** the standard primarily governs documents, so conversational use focuses on audience, structure, and usability.
- **Standard record:** [ISO 24495-1:2023](https://www.iso.org/standard/78907.html).

### 8. Barbara Minto — *The Pyramid Principle*

- **Adopted:** lead with the governing point and organize supporting ideas into a coherent hierarchy.
- **Used for:** concise alignment statements, decision-first feedback, and publication-ready explanations.
- **Limit:** this is a communication structure, not a test of factual accuracy or logical validity.
- **Current publisher record:** [Pearson, third edition](https://www.pearson.com/en-gb/subject-catalog/p/the-pyramid-principle/P200000015259/9781292763255).

### 9. Erik Miehling et al. — “Language Models in Dialogue: Conversational Maxims for Human-AI Interactions” (2024)

- **Adopted:** direct application of quantity, quality, relevance, and manner to human-AI dialogue, plus explicit attention to transparency about knowledge and operating limits.
- **Used for:** adapting classical pragmatics to AI responses and keeping evidence boundaries visible without defensive padding.
- **Limit:** the paper proposes and evaluates a framework; it does not establish one universally optimal conversational policy.
- **Paper:** [Findings of EMNLP 2024, ACL Anthology](https://aclanthology.org/2024.findings-emnlp.843/).

## Bibliographic count for public descriptions

The current foundation contains **9 traceable sources**:

- 3 books: Austin, Toulmin, and Minto;
- 2 foundational book chapters: Grice, and Clark and Brennan;
- 2 research papers: Schegloff, Jefferson, and Sacks; Miehling et al.;
- 2 international standards: ISO 24495-1 and ISO/IEC/IEEE 29148.

Describe this as a theory-informed synthesis. Do not claim that the nine sources jointly validated this Skill or that source count alone proves its quality.
