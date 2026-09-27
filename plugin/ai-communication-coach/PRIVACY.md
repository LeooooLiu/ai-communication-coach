# Privacy

AI Communication Coach is a skills-only package. It does not run a publisher-operated server, create user accounts, collect analytics, or send conversation content to the project author.

## Data handling

- The Skill instructions are read and executed by the AI host where the user installs them.
- Conversation content, files, model requests, logs, and telemetry are processed according to that host's settings and policies.
- The optional theory corpus builder downloads only the public sources declared in `research/corpus-manifest.json`. It stores retrieved files, extracted text, chunks, and the SQLite search index under the local Git-ignored `research/.local-corpus/` directory.
- The model evaluation runner stores local results under the Git-ignored `.local-evals/` directory.
- The package contains no analytics SDK, tracking pixel, advertising code, or publisher-controlled network endpoint.

## User-submitted reports

GitHub issues and discussions contain only the information a contributor chooses to post and are governed by GitHub's privacy terms. Remove personal, confidential, and proprietary information before sharing a conversation example.

## Contact

For a privacy question, open a [private security report](https://github.com/LeooooLiu/ai-communication-coach/security/advisories/new) when disclosure itself is sensitive. For ordinary questions, use [GitHub Discussions](https://github.com/LeooooLiu/ai-communication-coach/discussions).

Last updated: 2026-09-27.
