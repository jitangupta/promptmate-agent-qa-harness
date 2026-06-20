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

## 2026-06-19 - Rating Prompt Tests Blocked by chrome.storage.local Injection Gap

- **Type:** Testability
- **Platform:** all
- **Related tests:** TC-087, TC-088
- **Severity:** P2
- **Observed:** Codex ran TC-087 and TC-088 on chatgpt.com. The Chrome automation surface cannot navigate to `chrome://extensions` or open the DevTools Application panel, so the `promptmate.ratingPrompt` fixture cannot be injected into `chrome.storage.local`. Both tests were logged as `unable_to_test`. The product was not at fault — no banner was present because the precondition could never be established.
- **Expected:** An automated agent should be able to set the extension's internal state and verify the rating banner appears, without requiring a human to manually operate DevTools before the run.
- **Evidence:** TR-001, TR-002 in `promptmate_test_results_2026-06-19.jsonl`.
- **Suggested fix:** Add a generic test-state function to the PromptMate content script that reads two URL parameters — a storage key and a JSON value — and writes them into `chrome.storage.local` on page load. A single function covers the rating prompt, future banners, onboarding state, and any other storage-backed feature without adding a new flag each time.

  **Proposed content script function:**
  ```js
  function applyTestStateFromURL(params) {
    const key = params.get('pm_test_key');
    const raw = params.get('pm_test_value');
    if (!key || !raw) return;
    try {
      chrome.storage.local.set({ [key]: JSON.parse(raw) }, () => location.reload());
    } catch (e) {
      console.warn('[PromptMate test hook] Invalid pm_test_value JSON', e);
    }
  }

  // Called once on content script init — gated so it never runs in production:
  if (process.env.NODE_ENV !== 'production') {
    applyTestStateFromURL(new URLSearchParams(location.search));
  }
  ```

  **Example usage for TC-087 (rating banner):**
  ```
  https://chatgpt.com?pm_test_key=promptmate.ratingPrompt&pm_test_value={"action":null,"dismissedAt":null,"firstSeenAt":"2026-06-11T17:40:26.356Z","version":"0.7.1"}
  ```

  **Reusable for other banners** — any storage-backed state can be seeded the same way:
  ```
  ?pm_test_key=promptmate.onboarding&pm_test_value={"step":0,"completed":false}
  ?pm_test_key=promptmate.someFeatureFlag&pm_test_value={"enabled":true}
  ```

  The function sets the value and reloads once so the extension reads fresh state. On the second load the params are still present but `chrome.storage.local.set` is idempotent so re-running is safe. Must be stripped or no-op'd in production builds.
- **Status:** Fixed — `pm_test_key`/`pm_test_value` hook implemented in `scripts/sidebar-core.js`, gated on `process.env.BUILD !== 'production'`. `@rollup/plugin-replace` added to `rollup.config.js` to strip the hook from production bundles. AGENTS.md fixture section updated.

## 2026-06-16 - PromptMate Button Hidden While Panel Open

- **Type:** UX
- **Platform:** chatgpt.com
- **Related tests:** TC-008
- **Severity:** P2
- **Observed:** The floating PromptMate button becomes hidden while the panel is open, so users cannot close the panel by clicking the same button again.
- **Expected:** If the product supports toggle behavior, the button should remain visible/clickable or the test expectation should be updated to only support the close button.
- **Evidence:** TR-004 in `promptmate_test_results_2026-06-16.jsonl`.
- **Suggested fix:** Keep a visible active-state PromptMate pill while the panel is open, or update product copy/tests to make the close-button-only behavior explicit.
- **Status:** Fixed — `updatePillVisibility()` in `sidebar-core.js` now toggles `pm-active` instead of `pm-hidden`. Pill remains visible and clickable when panel is open. `aria-label` updates to "Close PromptMate" when active. `.pm-pill.pm-active` style added to `pm-v2.css`.

## 2026-06-16 - Search Clear Button Missing

- **Type:** UX
- **Platform:** chatgpt.com
- **Related tests:** TC-012
- **Severity:** P2
- **Observed:** With a search query active, no visible clear-search X/button was found.
- **Expected:** Users should have a visible one-click affordance to clear search and restore the full library.
- **Evidence:** TR-008 in `promptmate_test_results_2026-06-16.jsonl`.
- **Suggested fix:** Add a visible clear button inside the search input when `query.length > 0`, with an accessible label such as `Clear search`.
- **Status:** Fixed — `buildSearch()` in `sidebar-core.js` now appends a `pm-search-clear` button (×, `aria-label="Clear search"`) that appears when the query is non-empty and hides when cleared. Also hidden on view switch. `.pm-search-clear` styles added to `pm-v2.css`.

## 2026-06-16 - Edit Validation Partially Persists Empty Title Edit

- **Type:** Bug
- **Platform:** chatgpt.com
- **Related tests:** TC-039
- **Severity:** P1
- **Observed:** Editing a prompt with an empty title left the modal open, but the prompt body changed to the attempted edit body.
- **Expected:** Invalid edits should be fully blocked; no title, body, group, history, or sync changes should persist until validation passes.
- **Evidence:** TR-032 in `promptmate_test_results_2026-06-16.jsonl`.
- **Suggested fix:** Run validation before any persistence/update side effects, and add a regression test asserting that failed validation leaves the original prompt object unchanged.
- **Status:** Investigated — current HEAD (`onSavePrompt` in `sidebar-core.js` lines 2682–2687) has correct early-return validation before any writes. No secondary edit path that bypasses validation was found. The observed behavior likely occurred against an intermediate version. Re-test TC-039 against the current build to confirm.

## 2026-06-16 - Copy Action Copies Title Instead of Body

- **Type:** Bug
- **Platform:** chatgpt.com
- **Related tests:** TC-041
- **Severity:** P1
- **Observed:** Copy action on `AutoTest-TC037-edited` placed the prompt title on the clipboard instead of the prompt body.
- **Expected:** Copy should copy the prompt body exactly.
- **Evidence:** TR-034 in `promptmate_test_results_2026-06-16.jsonl`.
- **Suggested fix:** Check the prompt action handler receives the prompt body field, not the title/display label, and add clipboard unit coverage for prompt cards with distinct title/body.
- **Status:** Investigated — `onCopy()` and `buildAssembledText()` in `sidebar-core.js` correctly read `prompt.body` (line 1724). The title-on-clipboard behavior was most likely caused by TC-039 state corruption: the partial-edit bug swapped body content before the copy ran. Re-test TC-041 after confirming TC-039 is clean.

## 2026-06-16 - Chrome Automation Stability Limited Back-Half Coverage

- **Type:** Testability
- **Platform:** chatgpt.com
- **Related tests:** TC-042, TC-043, TC-044, TC-045, TC-046, TC-047, TC-048, TC-049, TC-051, TC-052, TC-053, TC-057, TC-058, TC-059, TC-060, TC-061, TC-062, TC-063, TC-064, TC-065, TC-067, TC-068, TC-069, TC-070, TC-072, TC-074, TC-075, TC-076, TC-077, TC-078, TC-079, TC-080, TC-081, TC-083, TC-084, TC-085, TC-086
- **Severity:** P2
- **Observed:** Chrome automation reset twice while working through the Version History section, preventing reliable completion of the back half of the suite in one session.
- **Expected:** QA harness should support resuming from a known test ID with stable AutoTest fixtures and minimal manual reconstruction.
- **Evidence:** Multiple `unable_to_test` results in `promptmate_test_results_2026-06-16.jsonl`.
- **Suggested fix:** Add a resumable runner checklist or split smoke/regression suites into smaller platform chunks, with fixture setup/cleanup guidance for AutoTest prompts and groups.
- **Status:** Fixed — AGENTS.md updated with "Resuming a Partial Run" instructions and "Suite Chunks" table (`smoke` TC-001–TC-020, `compose` TC-021–TC-060, `personalize` TC-061–TC-078, `context` TC-079–TC-088).

## 2026-06-14 - Release Version and QA Scope Handoff

- **Type:** Docs
- **Platform:** all
- **Related tests:** TC-065, TC-066, TC-067, TC-068, TC-069, TC-070, TC-071, TC-072, TC-073, TC-074, TC-075, TC-076, TC-077, TC-078, TC-079, TC-080, TC-081, TC-082, TC-083, TC-084, TC-085, TC-086
- **Severity:** P2
- **Observed:** Live Chrome exploration on chatgpt.com showed PromptMate now includes variable prompts, grouped prompt sections, group-specific instructions, user context, context extraction, prompt preview/fill flows, version history, and trash restore. The old harness language under-described the product as prompt-list management.
- **Expected:** Treat the next live release as `0.8.0`, not `1.0.0`; the previous release was `0.7.1`. QA scope should cover the expanded composition/personalization workflows before release.
- **Evidence:** Chrome exploration on 2026-06-14 observed `Fill in variables`, `Group instruction`, `Your context`, `Recently deleted`, group actions, and `Version history` surfaces in the installed extension.
- **Suggested fix:** Keep release metadata, changelog, store copy, and QA reports aligned to `0.8.0`; use the expanded `promptmate_test_cases.jsonl` inventory through TC-086 for release validation.
- **Status:** Resolved — `manifest.json` is already at `0.8.0`. No version drift found.
