# PromptMate Agent QA Harness

A lightweight, agent-operated QA harness for testing the PromptMate Chrome extension in real browser sessions.

This repository is not the PromptMate extension source code. It is a public, reusable example of an Agent QA Harness: structured instructions, JSONL test cases, result logs, reports, and development handoff notes that AI agents can use to perform browser-based product QA.

## Why This Exists

PromptMate runs inside several third-party AI chat products. Those products change often, use different input implementations, and may depend on logged-in browser state. Traditional brittle selectors are not always enough.

This harness treats an AI agent as a supervised QA operator:

- read a structured test spec
- use Chrome with the installed PromptMate extension
- interact with the UI like a user
- log every result immediately
- generate a readable report
- separate product bugs and UX opportunities into a development handoff file

## Target Product

**[PromptMate](https://github.com/jitangupta/PromptMate)** is a Chrome extension that helps users compose, organize, personalize, sync, and inject reusable prompts into AI chat interfaces.

Current feature areas covered by the harness include prompt search, tone and format modifiers, grouped prompt libraries, group-specific instructions, variable placeholders, user context, context extraction, preview, version history, trash/restore flows, cloud sync, and platform-specific injection behavior.

Supported PromptMate surfaces:

| Platform | URL | Notes |
|---|---|---|
| Claude | `https://claude.ai/new` | Uses the Claude content script |
| ChatGPT | `https://chatgpt.com` | Input is usually `contenteditable` |
| DeepSeek | `https://chat.deepseek.com` | May require login |
| Kimi | `https://kimi.com` | Wait 3 seconds after navigation |

## Repository Structure

| File / Directory | Purpose |
|---|---|
| `AGENTS.md` | Shared runbook for Codex, Claude Code, and other agentic systems |
| `CLAUDE.md` | Claude Code entry point that delegates to `AGENTS.md` |
| `promptmate_test_cases.jsonl` | Master test specification, one JSON object per line |
| `runs/YYYY-MM-DD/test_results.jsonl` | Raw result log for a dated run |
| `runs/YYYY-MM-DD/test_report.md` | Human-readable report for a dated run |
| `runs/YYYY-MM-DD/dashboard.html` | Token and cost dashboard (when a Codex rollout log is present) |
| `fixtures/` | Extension storage state fixtures for state-dependent tests |
| `eval.py` | Consistency eval script — measures cross-run verdict reliability |
| `CASE_STUDY.md` | In-depth write-up of harness architecture, the chrome.storage.local gap, and token economics |
| `DEVELOPMENT_HANDOFF.md` | Bugs, usability issues, and enhancement ideas found during testing |
| `RELEASE_HANDOFF_0.8.0.md` | Release-specific handoff for the 0.8.0 live release decision and expanded QA scope |

## Test Case Format

Each line in `promptmate_test_cases.jsonl` is a JSON object:

```json
{
  "id": "TC-001",
  "category": "Extension Presence",
  "name": "Button visible on chatgpt.com",
  "description": "PromptMate button appears on chatgpt.com after page load",
  "preconditions": ["Extension installed", "Logged into PromptMate"],
  "steps": ["Navigate to https://chatgpt.com", "Look for PromptMate button"],
  "expected": "PromptMate button is visible at bottom-right corner",
  "platforms": ["chatgpt.com"]
}
```

## Result Format

Each result is appended immediately as JSONL:

```json
{
  "id": "TR-001",
  "test_id": "TC-001",
  "platform": "chatgpt.com",
  "status": "pass",
  "timestamp": "2026-06-14",
  "notes": "PromptMate button was visible and opened the panel."
}
```

Valid statuses: `pass`, `fail`, `unable_to_test`, `skip`.

## How To Use

For agentic systems, start with `AGENTS.md`.

Common prompts:

```text
Start the ChatGPT test.
Start the full test.
Run TC-031 through TC-041 on chatgpt.com.
Run the smoke chunk on ChatGPT.
Review the latest report and summarize failures.
```

The suite is split into named chunks for targeted or partial runs:

| Chunk | Test IDs | Focus |
|---|---|---|
| `smoke` | TC-001 – TC-020 | Extension presence, panel UI, search, tone/format |
| `compose` | TC-021 – TC-060 | Prompt library, injection, pin, CRUD, version history, trash, sync |
| `personalize` | TC-061 – TC-078 | Edge cases, variables, groups |
| `context` | TC-079 – TC-088 | User context, prompt preview, rating prompt |

During testing, discovered product issues should go into `DEVELOPMENT_HANDOFF.md`, not only into the dated test report. The handoff file is meant to be directly usable by Codex, Claude Code, or a human developer.

To measure cross-run verdict consistency after accumulating multiple runs:

```bash
python eval.py          # human-readable report
python eval.py --json   # machine-readable output
```

## Testing State-Dependent UI

When a UI component only appears based on internal storage state (`chrome.storage.local`, `localStorage`, `sessionStorage`, cookies), agents are typically blocked — they can navigate URLs and click elements but cannot open DevTools to seed that state directly.

The fix is a **testability hook** built into the product: a URL parameter pair (`pm_test_key` / `pm_test_value`) that the content script reads on load, writes to `chrome.storage.local`, and then reloads. Any agent that can navigate a URL can seed any storage-backed state without DevTools access.

Key requirements for this pattern to work safely:
- The hook must be gated from production builds (not a runtime flag — stripped at bundle time)
- The hook should be generic, covering any storage key, not just the one that triggered the need
- Fixture files should document each injectable state and how to use the hook

See `AGENTS.md → Testing State-Dependent UI` for the full pattern, including the `chrome.storage.local` vs. `localStorage` distinction, production gating details, and guidance for adapting this to other products.

## Agent QA Harness Pattern

This repository is a worked example of the **[Agent QA Harness](https://github.com/jitangupta/agent-qa-harness)** pattern — a generalized, file-based template for using AI agents as browser-based QA operators on any project.

If you want to use this pattern for your own product, start there. It includes an onboarding flow where the agent asks about your project, checks your tooling, and generates an initial test spec — no code required.
