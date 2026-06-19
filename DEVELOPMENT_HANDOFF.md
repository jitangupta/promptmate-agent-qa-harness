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

## 2026-06-16 - PromptMate Button Hidden While Panel Open

- **Type:** UX
- **Platform:** chatgpt.com
- **Related tests:** TC-008
- **Severity:** P2
- **Observed:** The floating PromptMate button becomes hidden while the panel is open, so users cannot close the panel by clicking the same button again.
- **Expected:** If the product supports toggle behavior, the button should remain visible/clickable or the test expectation should be updated to only support the close button.
- **Evidence:** TR-004 in `promptmate_test_results_2026-06-16.jsonl`.
- **Suggested fix:** Keep a visible active-state PromptMate pill while the panel is open, or update product copy/tests to make the close-button-only behavior explicit.
- **Status:** Open

## 2026-06-16 - Search Clear Button Missing

- **Type:** UX
- **Platform:** chatgpt.com
- **Related tests:** TC-012
- **Severity:** P2
- **Observed:** With a search query active, no visible clear-search X/button was found.
- **Expected:** Users should have a visible one-click affordance to clear search and restore the full library.
- **Evidence:** TR-008 in `promptmate_test_results_2026-06-16.jsonl`.
- **Suggested fix:** Add a visible clear button inside the search input when `query.length > 0`, with an accessible label such as `Clear search`.
- **Status:** Open

## 2026-06-16 - Edit Validation Partially Persists Empty Title Edit

- **Type:** Bug
- **Platform:** chatgpt.com
- **Related tests:** TC-039
- **Severity:** P1
- **Observed:** Editing a prompt with an empty title left the modal open, but the prompt body changed to the attempted edit body.
- **Expected:** Invalid edits should be fully blocked; no title, body, group, history, or sync changes should persist until validation passes.
- **Evidence:** TR-032 in `promptmate_test_results_2026-06-16.jsonl`.
- **Suggested fix:** Run validation before any persistence/update side effects, and add a regression test asserting that failed validation leaves the original prompt object unchanged.
- **Status:** Open

## 2026-06-16 - Copy Action Copies Title Instead of Body

- **Type:** Bug
- **Platform:** chatgpt.com
- **Related tests:** TC-041
- **Severity:** P1
- **Observed:** Copy action on `AutoTest-TC037-edited` placed the prompt title on the clipboard instead of the prompt body.
- **Expected:** Copy should copy the prompt body exactly.
- **Evidence:** TR-034 in `promptmate_test_results_2026-06-16.jsonl`.
- **Suggested fix:** Check the prompt action handler receives the prompt body field, not the title/display label, and add clipboard unit coverage for prompt cards with distinct title/body.
- **Status:** Open

## 2026-06-16 - Chrome Automation Stability Limited Back-Half Coverage

- **Type:** Testability
- **Platform:** chatgpt.com
- **Related tests:** TC-042, TC-043, TC-044, TC-045, TC-046, TC-047, TC-048, TC-049, TC-051, TC-052, TC-053, TC-057, TC-058, TC-059, TC-060, TC-061, TC-062, TC-063, TC-064, TC-065, TC-067, TC-068, TC-069, TC-070, TC-072, TC-074, TC-075, TC-076, TC-077, TC-078, TC-079, TC-080, TC-081, TC-083, TC-084, TC-085, TC-086
- **Severity:** P2
- **Observed:** Chrome automation reset twice while working through the Version History section, preventing reliable completion of the back half of the suite in one session.
- **Expected:** QA harness should support resuming from a known test ID with stable AutoTest fixtures and minimal manual reconstruction.
- **Evidence:** Multiple `unable_to_test` results in `promptmate_test_results_2026-06-16.jsonl`.
- **Suggested fix:** Add a resumable runner checklist or split smoke/regression suites into smaller platform chunks, with fixture setup/cleanup guidance for AutoTest prompts and groups.
- **Status:** Open

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
