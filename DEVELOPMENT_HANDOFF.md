# Development Handoff

Use this file to capture product changes discovered while running the PromptMate Agent QA Harness.

This file is separate from dated test reports. Reports answer "what happened in this run." This handoff answers "what should the development agent or human developer do next?"

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

_No open items recorded yet for the current harness cleanup._
