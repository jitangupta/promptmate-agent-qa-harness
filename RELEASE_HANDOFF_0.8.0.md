# PromptMate Release Handoff - 0.8.0

## Version Decision

- Previous live release: `0.7.1`
- Next live release: `0.8.0`
- Do not mark this release as `1.0.0`.

## Why This Is 0.8.0

PromptMate has grown beyond simple prompt-list management, but this release should still be positioned as a pre-1.0 iteration. The current release adds and exposes larger composition workflows that need focused QA before a major version label:

- variable placeholders using `{{double_brace}}` syntax
- fill-in variable dialog with required fields and live preview
- prompt grouping
- group-specific instruction controls
- prompt movement between groups
- user context storage and insertion
- context extraction from the current chat
- prompt preview and resolved insertion flows
- version history
- trash restore and delete-forever flows

## QA Scope Update

The master test inventory now extends through `TC-086`.

New feature areas added:

- `TC-065` to `TC-070`: Variables
- `TC-071` to `TC-078`: Groups
- `TC-079` to `TC-084`: User Context
- `TC-085` to `TC-086`: Prompt Preview

Before calling `0.8.0` live, run at least one supported-platform smoke pass on ChatGPT, then repeat cross-platform injection checks on Claude, DeepSeek, and Kimi where authentication allows.

## Exploration Evidence

Chrome exploration on `chatgpt.com` on 2026-06-14 confirmed these installed-extension surfaces:

- global menu items: `Recently deleted`, `Your context`, `User Guide`, `Usage stats: On`
- group headers with counts and group actions
- group action menu: `Rename`, `Edit instruction`, `Delete group`
- group instruction dialog with Use instruction switch and optional instruction textarea
- variable prompt card badge such as `1 variable`
- `Fill in variables` dialog with detected variables, live preview, disabled Insert until required values are filled
- prompt editor with Group selector, `New group...`, and detected variable hints
- `Version history` dialog with 10-revision copy and restore semantics
- Trash view with Restore and Delete forever actions plus expiry labels
