# Security Policy

## Supported versions

Security fixes target the latest GitHub release. Reproduce a report against that version when possible.

## Report a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/LeooooLiu/ai-communication-coach/security/advisories/new). Include the affected version, impact, reproduction steps, and any suggested mitigation.

Do not put unpatched vulnerabilities, credentials, private conversations, or proprietary files in a public issue.

## Package boundary

The core package is instruction text plus local Python utilities. It has no publisher-operated service. The optional corpus builder performs outbound downloads only for URLs declared in `research/corpus-manifest.json`; the evaluation runner invokes the locally installed Codex CLI.
