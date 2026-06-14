# PromptMate Agent QA Harness - Agent Runbook

This repository is a lightweight QA harness for testing the PromptMate Chrome extension with AI agents such as Codex, Claude Code, and Claude Desktop.

It is not the PromptMate extension source code. It contains the test specification, execution rules, result logs, reports, and development handoff notes.

When a user asks to run tests, follow this file unless they give a narrower scope.

## Product Under Test

PromptMate is a Chrome extension that helps users compose, organize, personalize, sync, and inject reusable prompts into AI chat interfaces.

The extension renders a floating PromptMate button and panel inside supported AI chat products. The panel includes:

- searchable prompt library
- prompt grouping with group headers and group-specific actions
- group-specific instructions that can be applied during prompt insertion
- variable placeholders using `{{double_brace}}` syntax, with a fill-in dialog and live preview before insertion
- user context that can be attached to inserted prompts
- context extraction from the current chat
- Tone and Format settings
- prompt actions: Use, Pin, Copy, Preview, Edit, History, Move to group, Delete
- cloud sync
- version history
- trash and restore flows

## Supported Platforms

| Platform | URL | Notes |
|---|---|---|
| Claude | `https://claude.ai/new` | Use the real Chrome session with the extension installed |
| ChatGPT | `https://chatgpt.com` | Input is usually a `contenteditable` element |
| DeepSeek | `https://chat.deepseek.com` | May require login |
| Kimi | `https://kimi.com` | Wait 3 seconds after navigation; try `www.kimi.com` only if needed |

## Important Scope Rule

If the user specifies a platform, run only that platform.

Examples:

- "Start the ChatGPT test" means run applicable tests on `chatgpt.com` only.
- "Start the full test" means run all supported platforms.
- "Start the test" without a platform means ask one concise clarification unless prior conversation clearly established the platform.

## Files

| File | Purpose |
|---|---|
| `AGENTS.md` | Shared instructions for all AI agents |
| `CLAUDE.md` | Claude Code pointer to this runbook |
| `promptmate_test_cases.jsonl` | Master test cases, one JSON object per line |
| `promptmate_test_results_YYYY-MM-DD.jsonl` | Raw result log for a dated run |
| `promptmate_test_report_YYYY-MM-DD.md` | Markdown report for a dated run |
| `DEVELOPMENT_HANDOFF.md` | Product bugs, enhancements, and UX notes discovered during testing |
| `RELEASE_HANDOFF_0.8.0.md` | Release-specific handoff for the 0.8.0 live release decision and expanded QA scope |

## How To Open PromptMate

1. Use Chrome with the installed PromptMate extension.
2. Navigate to the target platform URL.
3. Wait for the page to load. For Kimi, wait 3 extra seconds.
4. Locate the PromptMate button by accessible text, DOM text, or visual search. Prefer stable UI evidence over fixed coordinates.
5. Click the button to open the panel.
6. Use visible labels and DOM state for interactions. Avoid hard-coded pixel coordinates except as a last resort.

Useful UI targets:

| Element | Search text or cue |
|---|---|
| Open panel button | `PromptMate`, `Open PromptMate`, `PromptMate button` |
| Close panel | `Close`, `X`, `close PromptMate` |
| Search bar | `Search prompts` |
| Tone dropdown | `TONE`, `Tone` |
| Format dropdown | `FORMAT`, `Format` |
| New prompt button | `New prompt`, `+ New prompt` |
| Global menu | `...`, `more options`, `ellipsis menu` |
| Prompt card menu | prompt-specific options menu |
| Save button | `Save` |
| Cancel button | `Cancel` |

## Test Execution Flow

1. Read `promptmate_test_cases.jsonl`.
2. Filter test cases by the requested platform.
3. Navigate to the platform and open PromptMate.
4. Execute each applicable test case in order.
5. Append a result immediately after every test.
6. Watch for usability friction while testing, even when the functional expectation passes.
7. Add product bugs, enhancements, and usability ideas to `DEVELOPMENT_HANDOFF.md`.
8. Generate or update the markdown report after the run.

## Usability Review Rule

During every test run, evaluate whether a real user would understand and complete the workflow smoothly, not only whether the expected UI state appears.

Flag friction when any step feels confusing, hidden, slow, fragile, repetitive, easy to mis-click, unclear in copy, hard to recover from, or surprising in sequence. A test can still be logged as `pass` for functional behavior while also producing a UX handoff item.

Capture usability notes in result `notes` when they are test-specific. Add a `UX` entry to `DEVELOPMENT_HANDOFF.md` when the friction suggests a product improvement, especially for variables, grouping, group instructions, user context, context extraction, history, restore, or destructive actions.

## Result Logging

Append each result to `promptmate_test_results_YYYY-MM-DD.jsonl` using today's date.

Use sequential result IDs for the run:

```json
{
  "id": "TR-001",
  "test_id": "TC-001",
  "platform": "chatgpt.com",
  "status": "pass",
  "timestamp": "YYYY-MM-DD",
  "notes": "Observed behavior and relevant evidence."
}
```

Statuses:

| Status | Use when |
|---|---|
| `pass` | Expected outcome was confirmed |
| `fail` | Test ran but actual behavior differed from expected behavior |
| `unable_to_test` | Test could not be executed; explain why |
| `skip` | Test was intentionally skipped; explain why |

## Authentication Rule

Do not sign in, sign out, or complete authentication flows.

If a platform shows a login wall, mark applicable tests as `unable_to_test` with a note such as:

```text
not logged in - user handles auth manually
```

For sign-out tests, verify button presence only. Do not click sign out.

## Data Safety Rules

This is a test account, but keep test data easy to identify and clean up.

- Prefix created prompts with `AutoTest-`.
- Delete or restore `AutoTest-` prompts after the test that created them when safe.
- Do not click destructive account/auth actions.
- Treat irreversible delete-forever flows as `skip` unless the item was created during the same run and the user has approved that scope.

Default skip guidance:

- `TC-050`: Delete forever - skip unless the item was created during the same run and the user approved irreversible deletion.
- `TC-056`: Sign out button - verify presence only; do not click sign out.

## Development Handoff Rule

Whenever testing reveals a bug, usability issue, missing state, unclear copy, flaky behavior, or enhancement idea, add it to `DEVELOPMENT_HANDOFF.md`.

Use this format:

```markdown
## YYYY-MM-DD - Short Title

- **Type:** Bug | Enhancement | UX | Testability | Docs
- **Platform:** chatgpt.com | claude.ai | chat.deepseek.com | kimi.com | all
- **Related tests:** TC-XXX, TC-YYY
- **Severity:** P0 | P1 | P2 | P3
- **Observed:** What happened.
- **Expected:** What should happen.
- **Evidence:** Result ID, report section, or short reproduction note.
- **Suggested fix:** Concrete implementation or product suggestion.
- **Status:** Open
```

## Markdown Report Format

After a run, create or update `promptmate_test_report_YYYY-MM-DD.md`. Include one platform column per platform tested; the example below shows a ChatGPT-only run:

```markdown
# PromptMate Test Report - YYYY-MM-DD

## Summary

| Platform | Pass | Fail | Skip | Unable | Total |
|---|---|---|---|---|---|
| chatgpt.com | N | N | N | N | N |
| **TOTAL** | **N** | **N** | **N** | **N** | **N** |

## Results Matrix

| ID | Category | Test Name | chatgpt.com |
|---|---|---|---|
| TC-001 | Extension Presence | Button visible | pass |

Legend: pass | fail | skip | unable_to_test | n/a not applicable

## Failures & Issues

### [TC-XXX] Test name - platform

**Expected:** ...
**Actual:** ...
**Notes:** ...

## Development Handoff Additions

List any entries added to `DEVELOPMENT_HANDOFF.md`.

## Observations & Recommendations

Patterns, risks, and follow-up testing suggestions.
```

## Current Test Categories

| Category | Test IDs |
|---|---|
| Extension Presence | TC-001 to TC-005 |
| Panel UI | TC-006 to TC-008 |
| Search | TC-009 to TC-013 |
| Tone & Format | TC-014 to TC-018 |
| Prompt Library | TC-019 to TC-022 |
| Prompt Injection | TC-023 to TC-027 |
| Pin / Unpin | TC-028 to TC-030 |
| Prompt CRUD | TC-031 to TC-041 |
| Version History | TC-042 to TC-046 |
| Trash | TC-047 to TC-051 |
| Cloud Sync | TC-052 to TC-054 |
| Account | TC-055 to TC-056 |
| Help & Feedback | TC-057 to TC-059 |
| Edge Cases | TC-060 to TC-064 |
| Variables | TC-065 to TC-070 |
| Groups | TC-071 to TC-078 |
| User Context | TC-079 to TC-084 |
| Prompt Preview | TC-085 to TC-086 |
