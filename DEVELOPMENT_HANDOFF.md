# Development Handoff

Use this file to capture product changes discovered while running the PromptMate Agent QA Harness.

This file is separate from dated test reports. Reports answer "what happened in this run." This handoff answers "what should the development agent or human developer do next?"

Usability friction should be captured here even when the underlying test passes. If a workflow is technically correct but feels confusing, hidden, slow, overly risky, or hard to recover from, add a `UX` entry so the team can review it from the user's perspective.

## Entry Template

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

## Severity Guide

- **P0:** Blocks core extension use or risks data loss/security.
- **P1:** Breaks an important workflow on a supported platform.
- **P2:** Noticeable UX, reliability, or compatibility issue with workaround.
- **P3:** Polish, copy, docs, or testability improvement.

## Open Items

## 2026-06-14 - Release Version and QA Scope Handoff

- **Type:** Docs
- **Platform:** all
- **Related tests:** TC-065, TC-066, TC-067, TC-068, TC-069, TC-070, TC-071, TC-072, TC-073, TC-074, TC-075, TC-076, TC-077, TC-078, TC-079, TC-080, TC-081, TC-082, TC-083, TC-084, TC-085, TC-086
- **Severity:** P2
- **Observed:** Live Chrome exploration on chatgpt.com showed PromptMate now includes variable prompts, grouped prompt sections, group-specific instructions, user context, context extraction, prompt preview/fill flows, version history, and trash restore. The old harness language under-described the product as prompt-list management.
- **Expected:** Treat the next live release as `0.8.0`, not `1.0.0`; the previous release was `0.7.1`. QA scope should cover the expanded composition/personalization workflows before release.
- **Evidence:** Chrome exploration on 2026-06-14 observed `Fill in variables`, `Group instruction`, `Your context`, `Recently deleted`, group actions, and `Version history` surfaces in the installed extension.
- **Suggested fix:** Keep release metadata, changelog, store copy, and QA reports aligned to `0.8.0`; use the expanded `promptmate_test_cases.jsonl` inventory through TC-086 for release validation.
- **Status:** Open
