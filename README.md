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

PromptMate is a Chrome extension that helps users compose, organize, personalize, sync, and inject reusable prompts into AI chat interfaces.

Current feature areas covered by the harness include prompt search, tone and format modifiers, grouped prompt libraries, group-specific instructions, variable placeholders, user context, context extraction, preview, version history, trash/restore flows, cloud sync, and platform-specific injection behavior.

Supported PromptMate surfaces:

| Platform | URL | Notes |
|---|---|---|
| Claude | `https://claude.ai/new` | Uses the Claude content script |
| ChatGPT | `https://chatgpt.com` | Input is usually `contenteditable` |
| DeepSeek | `https://chat.deepseek.com` | May require login |
| Kimi | `https://kimi.com` | Wait 3 seconds after navigation |

## Repository Structure

| File | Purpose |
|---|---|
| `AGENTS.md` | Shared runbook for Codex, Claude Code, and other agentic systems |
| `CLAUDE.md` | Claude Code entry point that delegates to `AGENTS.md` |
| `promptmate_test_cases.jsonl` | Master test specification, one JSON object per line |
| `promptmate_test_results_YYYY-MM-DD.jsonl` | Raw result log for a dated run |
| `promptmate_test_report_YYYY-MM-DD.md` | Human-readable report for a dated run |
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
Review the latest report and summarize failures.
```

During testing, discovered product issues should go into `DEVELOPMENT_HANDOFF.md`, not only into the dated test report. The handoff file is meant to be directly usable by Codex, Claude Code, or a human developer.

## Positioning

This repository is also a public case study for the Agent QA Harness pattern: using AI agents as browser-based QA operators with structured specs, evidence-oriented logs, and development-ready handoffs.
