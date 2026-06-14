# PromptMate Test Suite — Codex Context

This folder is the test suite for **PromptMate**, a Chrome extension (v0.7.1) that lets users save, organize, and inject prompts into AI chat interfaces.

When a user says **"Start the test"**, follow the instructions in this file exactly.

---

## What PromptMate Is

A Chrome extension injected via content scripts into 4 AI chat platforms. It renders a floating panel (bottom-right corner) with:
- A searchable prompt library
- Tone & Format settings (appended to injected prompts)
- Per-prompt actions: Use, Pin, Copy, Edit, History, Delete
- Cloud sync across platforms
- A trash/restore system (30-day soft delete)

Each platform has its own dedicated content script bundle — injection behavior may differ.

---

## Supported Platforms (from manifest.json)

| Platform | URL to navigate to | Content script |
|---|---|---|
| Codex | `https://Codex.ai/new` | `Codex-content.bundle.js` |
| ChatGPT | `https://chatgpt.com` | `gpt-content.bundle.js` |
| DeepSeek | `https://chat.deepseek.com` | `deepseek-content.bundle.js` |
| Kimi | `https://kimi.com` | `kimi-content.bundle.js` (loads at document_idle — wait 3s after navigation) |

---

## Files in This Folder

| File | Purpose |
|---|---|
| `AGENTS.md` | This file — read first, every session |
| `manifest.json` | Extension manifest — reference for supported URLs |
| `promptmate_test_cases.jsonl` | Master test spec — 64 test cases, one JSON per line |
| `promptmate_test_results_YYYY-MM-DD.jsonl` | Raw results written after each run |
| `promptmate_test_report_YYYY-MM-DD.md` | Markdown report generated after each run |

---

## How to Open PromptMate on Any Platform

1. Navigate to the platform URL above
2. Wait for the page to fully load (extra 3s for Kimi)
3. Use `find` tool with query `"PromptMate button"` to locate the button — do NOT rely on pixel coordinates as window size varies
4. Click it to open the panel
5. Use `find` tool throughout for all panel interactions (search bar, dropdowns, buttons) rather than fixed coordinates

---

## How to Run the Tests

### Step 1 — Read the spec
Read `promptmate_test_cases.jsonl`. Each line is one test case with fields: `id`, `category`, `name`, `description`, `preconditions`, `steps`, `expected`, `platforms`.

### Step 2 — Run platform by platform
For each platform in this order: **Codex.ai → chatgpt.com → chat.deepseek.com → kimi.com**:
- Navigate to the URL
- Open PromptMate
- Execute every test case whose `platforms` array includes this platform
- Log each result immediately

### Step 3 — Write raw results
Append every result to `promptmate_test_results_YYYY-MM-DD.jsonl` (use today's date).
Each line:
```json
{
  "id": "TR-001",
  "test_id": "TC-001",
  "platform": "Codex.ai",
  "status": "pass",
  "timestamp": "YYYY-MM-DD",
  "notes": "Observed behaviour and any detail."
}
```
Use sequential TR-NNN IDs across all platforms in the run.

### Step 4 — Generate the markdown report
After all 4 platforms are done, write `promptmate_test_report_YYYY-MM-DD.md` (see format below).

---

## Result Statuses

| Status | When to use |
|---|---|
| `pass` | Expected outcome confirmed by observation |
| `fail` | Test ran but outcome did NOT match expected |
| `unable_to_test` | Could not execute — explain why in notes |
| `skip` | Explicitly skipped (only for truly destructive ops, noted below) |

---

## Authentication

Authentication (Google Sign-In) is **tested manually by the user** — do not attempt to sign in, sign out, or handle any auth flow. If a platform shows a login wall, log `unable_to_test` for all cases on that platform with note "not logged in — user handles auth manually".

---

## Test Categories

| Category | Test IDs | Description |
|---|---|---|
| Extension Presence | TC-001 – TC-005 | Button visibility per platform and on unsupported sites |
| Panel UI | TC-006 – TC-008 | Open/close panel |
| Search | TC-009 – TC-013 | Search filtering, empty state, case-insensitivity |
| Tone & Format | TC-014 – TC-018 | Dropdowns, persistence, appended modifier |
| Prompt Library | TC-019 – TC-022 | RECENT/PINNED sections, ordering |
| Prompt Injection | TC-023 – TC-027 | Use action per platform, counter increment |
| Pin / Unpin | TC-028 – TC-030 | Pin/unpin behavior, multiple pins |
| Prompt CRUD | TC-031 – TC-041 | Create, Edit, Copy, Cancel, validation |
| Version History | TC-042 – TC-046 | History modal, diff, restore, 10-item cap |
| Trash | TC-047 – TC-051 | Delete, restore, delete forever, navigation |
| Cloud Sync | TC-052 – TC-054 | Sync indicator, persistence, cross-platform |
| Account | TC-055 – TC-056 | Email display, sign-out button presence |
| Help & Feedback | TC-057 – TC-059 | User Guide, Rate, Request feature |
| Edge Cases | TC-060 – TC-064 | Long title/body, special chars, duplicates, Escape |

---

## Data Safety Rules

This is a **test account** — you have full freedom to create, edit, and delete data.

- Always prefix created prompts with `AutoTest-` (e.g. `AutoTest-TC032`)
- Always delete `AutoTest-` prompts after the test that created them
- The only tests to treat as `skip` by default are:
  - **TC-050** (Delete forever) — irreversible; only run if you created the item yourself in this session
  - **TC-056** (Sign out button) — verify presence only, do NOT click it

---

## Platform-Specific Notes

### Codex (Codex.ai)
- Panel opens reliably; all features confirmed working in prior sessions
- Chat input selector: the main textarea

### ChatGPT (chatgpt.com)
- May show a login wall — if not logged in, log `unable_to_test` for all ChatGPT cases with note "not logged in"
- ChatGPT input is a `contenteditable` div, not a textarea — verify Use injection works

### DeepSeek (chat.deepseek.com)
- May require login — same rule as ChatGPT
- Input may be a textarea or contenteditable

### Kimi (kimi.com)
- Content script runs at `document_idle` — **always wait 3 seconds** after navigation before looking for the PromptMate button
- Try both `kimi.com` and `www.kimi.com` if button not found on first try
- May require login

---

## Markdown Report Format

```markdown
# PromptMate Test Report — YYYY-MM-DD

## Summary

| Platform | Pass | Fail | Skip | Unable | Total |
|---|---|---|---|---|---|
| Codex.ai | N | N | N | N | 64 |
| chatgpt.com | N | N | N | N | 64 |
| chat.deepseek.com | N | N | N | N | 64 |
| kimi.com | N | N | N | N | 64 |
| **TOTAL** | **N** | **N** | **N** | **N** | **256** |

## Results Matrix

| ID | Category | Test Name | Codex.ai | chatgpt.com | deepseek | kimi |
|---|---|---|---|---|---|---|
| TC-001 | Extension Visibility | Panel toggle open | ✅ | ✅ | ✅ | ✅ |
| TC-002 | ... | ... | ... | ... | ... | ... |

Legend: ✅ pass · ❌ fail · ⏭️ skip · ❓ unable_to_test

## Failures & Issues

### [TC-XXX] Test name — platform
**Expected:** ...
**Actual:** ...
**Notes:** ...

## Observations & Recommendations

(Any patterns, regressions, or suggestions noted during the run)
```

---

## Quick Reference — Key UI Elements to Find

Use the `find` tool with these queries:

| Element | Query string |
|---|---|
| Open panel button | `"PromptMate button"` |
| Close panel (×) | `"close panel button X"` or `"close PromptMate"` |
| Search bar | `"Search prompts"` |
| Tone dropdown | `"TONE dropdown"` |
| Format dropdown | `"FORMAT dropdown None"` |
| New prompt button | `"New prompt button"` |
| Global menu (···) | `"more options menu"` or `"ellipsis menu"` |
| Prompt card menu (···) | `"prompt options"` on a specific card |
| Save button in modal | `"Save"` |
| Cancel button in modal | `"Cancel"` |
