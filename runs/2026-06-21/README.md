# Run: 2026-06-21

Full QA suite run against PromptMate Chrome extension using Codex Desktop (GPT-5.5).

## Files

| File | Status | Notes |
|---|---|---|
| `dashboard.html` | Public | Token usage and cost analysis — open in browser |
| `rollout-*-019ee93f-*.jsonl` | **Gitignored** | Main agent session log (2.9 MB) |
| `rollout-*-019ee993-*.jsonl` | **Gitignored** | Guardian subagent log (725 KB) |

## Run Summary

| | |
|---|---|
| Date | 2026-06-21 |
| Model | GPT-5.5 (Codex Desktop) |
| Sessions | 2 (main + guardian subagent) |
| Total API requests | 351 |
| Total turns | 18 |
| Total input tokens | ~55.85M (98% cache hit) |
| Total output tokens | ~95.8K |
| Estimated API cost | $35.34 |

## Why JSONL files are excluded

The raw Codex rollout logs capture the full agent context window for every API
request. They contain Windows file paths, email addresses, and API key material
embedded in the context that was sent to the model. The `dashboard.html` file
contains all the analytical data without any of that content.
