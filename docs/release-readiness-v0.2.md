# v0.2 public release readiness

Baseline recorded on 2026-09-27 before release work began.

## Product behavior

- [x] Add context-grounded intent reconstruction without hidden-fact inference.
- [x] Add paired cases for recoverable omission, real ambiguity, hypotheses, motives, and authority boundaries.
- [x] Run the real-conversation suite on a second model family.
- [x] Run multi-turn tasks that inspect and modify disposable workspaces.

## Distribution

- [x] Build a portable skills-only plugin with root `plugin.json` and `skills/ai-communication-coach/`.
- [x] Validate the portable manifest, bundled Skill, assets, and archive layout.
- [x] Verify direct Skill installation from the public repository in a clean environment.
- [x] Verify plugin installation from a Git-backed local marketplace.

## Public repository

- [x] Add privacy, terms, security, and support documents required by public plugin listings.
- [x] Add full English documentation and keep Chinese as the primary README.
- [x] Update badges, source counts, evaluation counts, installation paths, and release notes.
- [x] Extend CI to validate and build the release bundle.
- [ ] Apply and verify the GitHub social preview image.

## Release

- [x] Commit the release candidate and pass local validation.
- [x] Pass GitHub Actions from the release commit.
- [x] Create a semantic version tag and GitHub Release with the portable plugin ZIP.
- [x] Install the published release artifact and verify one positive and one negative activation case.

## External directory submission

- [x] Prepare listing copy, starter prompts, five positive cases, three negative cases, policy URLs, and release notes.
- [x] Document that identity verification and final submission remain with the publisher account because the portal requires a verified developer or business identity.
