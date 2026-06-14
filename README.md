# PromptMate Test Suite

Automated test suite for the **PromptMate** Chrome extension (v0.7.1).  
Powered by Claude + Claude-in-Chrome MCP. No Playwright, no Puppeteer.

---

## Supported Platforms

Derived from `manifest.json` `content_scripts`:

| Platform | URL | Content Script |
|---|---|---|
| Claude | `claude.ai` | `claude-content.bundle.js` |
| ChatGPT | `chatgpt.com` | `gpt-content.bundle.js` |
| DeepSeek | `chat.deepseek.com` | `deepseek-content.bundle.js` |
| Kimi | `kimi.com` / `www.kimi.com` | `kimi-content.bundle.js` (document_idle) |

---

## Folder Structure

```
PromptMateTestSuite/
├── README.md                          ← this file
├── manifest.json                      ← extension manifest (reference)
├── promptmate_test_cases.jsonl        ← master test spec (64 test cases)
├── promptmate_test_results_YYYY-MM-DD.jsonl   ← raw results per run
└── promptmate_test_report_YYYY-MM-DD.md       ← markdown report per run
```

---

## How to Run Tests

Open a Claude (Cowork) session, point it to this folder, and say:

> **"Start the test"**

Claude will:
1. Read `promptmate_test_cases.jsonl`
2. Navigate to each of the 4 platforms in Chrome
3. Execute each applicable test case
4. Write raw results to `promptmate_test_results_YYYY-MM-DD.jsonl`
5. Generate a full markdown report `promptmate_test_report_YYYY-MM-DD.md`

Results from previous runs are preserved — each run creates new dated files.

---

## Test Result Statuses

| Status | Meaning |
|---|---|
| `pass` | Test executed and expected outcome confirmed |
| `fail` | Test executed but outcome did not match expected |
| `unable_to_test` | Could not execute — reason logged in `notes` |
| `skip` | Intentionally skipped for this run (e.g. destructive tests) |

---

## Test Case Format (JSONL)

Each line in `promptmate_test_cases.jsonl` is a JSON object:

```json
{
  "id": "TC-001",
  "category": "Extension Visibility",
  "name": "Panel toggle open",
  "description": "...",
  "preconditions": ["..."],
  "steps": ["..."],
  "expected": "...",
  "platforms": ["claude.ai", "chatgpt.com", "chat.deepseek.com", "kimi.com"]
}
```

---

## Test Result Format (JSONL)

Each line in `promptmate_test_results_YYYY-MM-DD.jsonl`:

```json
{
  "id": "TR-001",
  "test_id": "TC-001",
  "platform": "claude.ai",
  "status": "pass",
  "timestamp": "2026-06-07",
  "notes": "Button visible at bottom-right, panel opened correctly."
}
```

---

## Categories

Authentication (Google Sign-In) is **tested manually by the user** and is not included in this suite.

| # | Category | Test IDs |
|---|---|---|
| 1 | Extension Presence | TC-001 – TC-005 |
| 2 | Panel UI | TC-006 – TC-008 |
| 3 | Search | TC-009 – TC-013 |
| 4 | Tone & Format | TC-014 – TC-018 |
| 5 | Prompt Library | TC-019 – TC-022 |
| 6 | Prompt Injection | TC-023 – TC-027 |
| 7 | Pin / Unpin | TC-028 – TC-030 |
| 8 | Prompt CRUD | TC-031 – TC-041 |
| 9 | Version History | TC-042 – TC-046 |
| 10 | Trash | TC-047 – TC-051 |
| 11 | Cloud Sync | TC-052 – TC-054 |
| 12 | Account | TC-055 – TC-056 |
| 13 | Help & Feedback | TC-057 – TC-059 |
| 14 | Edge Cases | TC-060 – TC-064 |

---

## Notes for Claude (Test Runner Instructions)

- Run tests **platform by platform** — navigate to each URL, open PromptMate, run all applicable tests, then move to the next platform.
- For Kimi, wait for `document_idle` — the content script loads after the page fully renders, so wait 2–3s after navigation before interacting.
- **Do not** execute destructive tests (TC-042 Delete forever, TC-049 Sign out) without explicit user confirmation.
- Tests that require creating prompts (TC-030, TC-055–TC-058) should use the prefix `AutoTest-` in the title so they are easy to clean up after.
- After all platforms are tested, generate the markdown report using the template in this README.

---

## Markdown Report Template

The generated report (`promptmate_test_report_YYYY-MM-DD.md`) uses this format:

```
# PromptMate Test Report — YYYY-MM-DD

## Summary
| Platform | Pass | Fail | Unable | Total |
| claude.ai | X | X | X | 60 |
| chatgpt.com | X | X | X | 60 |
| chat.deepseek.com | X | X | X | 60 |
| kimi.com | X | X | X | 60 |

## Results Matrix
| ID | Test Name | claude.ai | chatgpt.com | chat.deepseek.com | kimi.com |
|---|---|---|---|---|---|
| TC-001 | Panel toggle open | ✅ | ✅ | ✅ | ✅ |
...

## Failures & Issues
(detail any failures or unexpected behaviors)
```
