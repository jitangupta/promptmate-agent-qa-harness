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
| `runs/YYYY-MM-DD/test_results.jsonl` | Raw result log for a dated run |
| `runs/YYYY-MM-DD/test_report.md` | Markdown report for a dated run |
| `runs/YYYY-MM-DD/dashboard.html` | Token and cost dashboard (when a Codex rollout log is present) |
| `DEVELOPMENT_HANDOFF.md` | Product bugs, enhancements, and UX notes discovered during testing |
| `RELEASE_HANDOFF_0.8.0.md` | Release-specific handoff for the 0.8.0 live release decision and expanded QA scope |
| `fixtures/` | localStorage state fixtures for tests that require specific extension internal state |

## Fixtures

Some test scenarios depend on internal extension state stored in `localStorage` that cannot be reached purely through UI navigation. The `fixtures/` directory contains JSON files documenting these states and the DevTools console snippet to inject them.

### How to inject a fixture

**URL param method (preferred — agent-friendly, no DevTools needed):**

Requires the `pm_test_key` / `pm_test_value` hook to be implemented in the PromptMate content script (see `DEVELOPMENT_HANDOFF.md` entry 2026-06-19). Once shipped, navigate to the platform URL with the params and the content script writes the value into `chrome.storage.local` then reloads once.

```
https://chatgpt.com?pm_test_key=<storageKey>&pm_test_value=<urlEncodedJSON>
```

The same two params work for any `chrome.storage.local` key — rating prompt, onboarding state, feature flags, or any future storage-backed banner.

**Manual DevTools fallback (works today, not usable by agents):**

1. Open Chrome DevTools on the target platform page (F12).
2. Go to the **Application** tab.
3. Expand **Extension Storage → Local**, find the PromptMate entry.
4. Double-click the value cell for the target key and paste the desired state JSON.
5. Press Enter, then reload the page.

### Available fixtures

| File | Key | Purpose |
|---|---|---|
| `fixtures/rating_prompt.json` | `promptmate.ratingPrompt` | Controls visibility of the "A quick favor" Chrome Web Store rating dialog |

## Testing State-Dependent UI

Some UI components — banners, onboarding prompts, rating dialogs, feature gates — only appear when specific conditions are met in internal storage. Because `chrome.storage.local` lives in the extension process rather than the page, agents cannot reach it through DOM manipulation or script injection. DevTools can write to it, but agents cannot open DevTools panels.

This creates a class of tests that are structurally blocked without help from the product itself.

### The testability hook pattern

The fix is a **testability seam**: a thin, controlled entry point into internal state that is accessible through a channel agents already have — URL navigation — and stripped from production builds.

PromptMate implements this as two URL parameters read by the content script on load:

| Parameter | Role |
|---|---|
| `pm_test_key` | The `chrome.storage.local` key to write |
| `pm_test_value` | The JSON value to write at that key |

When both params are present, the content script writes the value, removes the params from the URL, and reloads once. The next load behaves exactly as if the user had reached that storage state naturally. The `pm_test_key` / `pm_test_value` pair is generic — it works for any `chrome.storage.local` key, not only `promptmate.ratingPrompt`.

### Why chrome.storage.local is different from localStorage

| | `localStorage` | `chrome.storage.local` |
|---|---|---|
| Lives in | Page context | Extension process |
| Writable by page JS | Yes | No |
| Writable by DevTools console | Yes (`localStorage.setItem(...)`) | Only via Application tab |
| Writable by agents | Via script injection | Not directly — blocked |

If a banner uses `localStorage`, an agent can seed it via script injection. If it uses `chrome.storage.local`, the agent is blocked unless the extension exposes a hook. This distinction is easy to miss when first designing the harness.

### The production gating requirement

The URL param hook must never reach production users. A page on any domain could craft a URL with `?pm_test_key=...&pm_test_value=...` and overwrite extension state for any user who clicks it.

PromptMate gates the hook on `process.env.BUILD !== 'production'`, stripped at bundle time by `@rollup/plugin-replace`. The hook is compiled out of production builds entirely — not a runtime conditional. Any testability hook of this kind requires the same treatment.

### Where this pattern applies beyond the rating prompt

The same problem and the same fix apply to any UI element gated on opaque browser storage:

- `localStorage` feature flags or A/B cohort assignments
- `sessionStorage`-backed onboarding progress
- `IndexedDB`-backed state (usage thresholds, upgrade prompts)
- Cookies that gate paywalls or trial expiry banners

### If you are adapting this harness for a different product

Before writing test cases for any state-dependent UI component, ask: *can an agent reach this state through normal navigation?*

If the answer is no:

1. Document the blocked state in your `DEVELOPMENT_HANDOFF.md` equivalent.
2. Spec a testability hook in the product — pick the agent-accessible channel (URL param, test API endpoint, dev-mode keyboard shortcut).
3. Gate it from production.
4. Add a fixture file describing the states and how to inject them.
5. Update your agent runbook with the injection method **before** writing the test cases.

Discovering the injection gap during a live run wastes a run. Document the gap first, then close it, then write the test cases.

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

## Resuming a Partial Run

If Chrome automation resets mid-run or you need to restart:

1. Check the existing `runs/YYYY-MM-DD/test_results.jsonl` to find the last logged result ID.
2. The user may specify a resume point: **"Resume from TC-XXX"** means skip all test cases with ID ≤ TC-XXX and continue from the next one.
3. When resuming, do not re-run completed tests. Append new results to the same `runs/YYYY-MM-DD/test_results.jsonl` file using sequential TR-IDs continuing from the last logged result.
4. If AutoTest fixture prompts or groups from a previous session are missing, re-create them before continuing — do not mark tests as `unable_to_test` solely because fixtures need to be re-established.

## Suite Chunks

For long runs or targeted testing, the suite can be split into themed chunks. Run one or more chunks rather than the full suite when time or session stability is limited.

| Chunk | Test IDs | Focus |
|---|---|---|
| `smoke` | TC-001 – TC-020 | Extension presence, panel UI, search, tone/format |
| `compose` | TC-021 – TC-060 | Prompt library, injection, pin, CRUD, version history, trash, sync, account |
| `personalize` | TC-061 – TC-078 | Edge cases, variables, groups |
| `context` | TC-079 – TC-088 | User context, prompt preview, rating prompt |

When the user specifies a chunk name (e.g. "Run the smoke chunk on ChatGPT"), execute only those test IDs.

## Usability Review Rule

During every test run, evaluate whether a real user would understand and complete the workflow smoothly, not only whether the expected UI state appears.

Flag friction when any step feels confusing, hidden, slow, fragile, repetitive, easy to mis-click, unclear in copy, hard to recover from, or surprising in sequence. A test can still be logged as `pass` for functional behavior while also producing a UX handoff item.

Capture usability notes in result `notes` when they are test-specific. Add a `UX` entry to `DEVELOPMENT_HANDOFF.md` when the friction suggests a product improvement, especially for variables, grouping, group instructions, user context, context extraction, history, restore, or destructive actions.

## Result Logging

Append each result to `runs/YYYY-MM-DD/test_results.jsonl` using today's date. Create the `runs/YYYY-MM-DD/` directory if it does not exist.

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

After a run, create or update `runs/YYYY-MM-DD/test_report.md`. Include one platform column per platform tested; the example below shows a ChatGPT-only run:

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
| Rating Prompt | TC-087 to TC-088 |
