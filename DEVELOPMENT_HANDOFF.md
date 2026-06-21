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

## 2026-06-21 - Claude Floating Pill Does Not Close the Open Panel

- **Type:** Bug
- **Platform:** claude.ai
- **Related tests:** TC-008
- **Severity:** P2
- **Observed:** After opening PromptMate on Claude, clicking the active floating pill labelled `Close PromptMate` left the panel open. The panel-header Close button worked.
- **Expected:** Re-clicking the active floating pill should close the panel.
- **Evidence:** TR-005 in `runs/2026-06-21/test_results.jsonl`.
- **Suggested fix:** Verify the active-pill click handler is bound once on Claude and calls the same close path as the panel-header Close button. Add a Claude-specific regression check after content-script reinjection.
- **Status:** Open

## 2026-06-21 - Pin and Move Updates Appear Several Seconds Late

- **Type:** UX
- **Platform:** all
- **Related tests:** TC-021, TC-028, TC-030, TC-078
- **Severity:** P2
- **Observed:** Pin/Unpin and Move to group actions changed their menu state before the card visibly relocated. Claude still showed the pinned card inside Group1 after the first short wait, while ChatGPT and Kimi required roughly 3–4 seconds before section/group counts and card placement settled.
- **Expected:** The card and counts should update immediately or show an explicit pending state until the sync result arrives.
- **Evidence:** TR-018, TR-022, TR-026, TR-076 in `runs/2026-06-21/test_results.jsonl`.
- **Suggested fix:** Apply an optimistic local move with rollback on sync failure, or keep a visible per-card syncing state and disable repeat actions until reconciliation completes.
- **Status:** Open

## 2026-06-21 - Copy Action Leaves Clipboard Empty

- **Type:** Bug
- **Platform:** chatgpt.com
- **Related tests:** TC-041
- **Severity:** P1
- **Observed:** Copy on the run-created prompt produced an empty browser clipboard. A subsequent paste attempt reported that no clipboard data was available.
- **Expected:** Copy should place the exact prompt body on the clipboard.
- **Evidence:** TR-037 in `runs/2026-06-21/test_results.jsonl`.
- **Suggested fix:** Surface clipboard-write failures, add a visible success/error toast, and regression-test both `navigator.clipboard.writeText` and the fallback copy path in the content-script context.
- **Status:** Open

## 2026-06-21 - Escape Does Not Dismiss New Prompt Modal

- **Type:** Bug
- **Platform:** chat.deepseek.com
- **Related tests:** TC-064
- **Severity:** P2
- **Observed:** Pressing Escape while the New prompt dialog contained unsaved title/body text left the dialog open and retained the draft.
- **Expected:** Escape should close the modal without saving, matching Cancel.
- **Evidence:** TR-059 in `runs/2026-06-21/test_results.jsonl`.
- **Suggested fix:** Add a document-level Escape handler while a PromptMate modal is active, stop propagation after handling, and route through the same discard path as Cancel.
- **Status:** Open

## 2026-06-21 - Native Confirm Dialogs Stall Agent Automation

- **Type:** Testability
- **Platform:** all
- **Related tests:** TC-045
- **Severity:** P2
- **Observed:** Restore opened a native JavaScript confirm. Accepting it repeatedly stalled Chrome control and reset the automation session; the same behavior appeared while cleaning up an AutoTest group deletion.
- **Expected:** Destructive or revision-changing confirmations should be operable and verifiable through the extension DOM.
- **Evidence:** TR-041 in `runs/2026-06-21/test_results.jsonl`; repeated confirmation hang during AutoTest group cleanup.
- **Suggested fix:** Replace `window.confirm` with an accessible in-panel confirmation dialog that exposes stable buttons and a deterministic pending/success state.
- **Status:** Open

## 2026-06-21 - Rating Test Hook Reloads Kimi Repeatedly

- **Type:** Testability
- **Platform:** kimi.com
- **Related tests:** TC-087, TC-088
- **Severity:** P1
- **Observed:** Navigating to Kimi with `pm_test_key` and `pm_test_value` retained both parameters and repeatedly reloaded the page. The PromptMate button alternated between present and absent, so the rating banner could not be opened or dismissed.
- **Expected:** The hook should write state once, remove both parameters from the URL, reload once, and then leave a stable page with the eligible banner visible.
- **Evidence:** TR-084 and TR-085 in `runs/2026-06-21/test_results.jsonl`.
- **Suggested fix:** Remove the test parameters with `history.replaceState` before reloading and add a one-shot session guard. Add coverage for `kimi.com` redirecting to `www.kimi.com`.
- **Status:** Open

## 2026-06-21 - Missing Safe Fixtures for Empty Library and 10+ Revisions

- **Type:** Testability
- **Platform:** all
- **Related tests:** TC-020, TC-046
- **Severity:** P3
- **Observed:** TC-020 could not safely reach an empty library without deleting user prompts. TC-046 had no prompt with more than 10 revisions; the richest available prompt had 8.
- **Expected:** Both state-dependent tests should have agent-safe fixtures that do not mutate unrelated user data.
- **Evidence:** TR-017 and TR-042 in `runs/2026-06-21/test_results.jsonl`.
- **Suggested fix:** Add fixture keys for an isolated empty-library dataset and a prompt with at least 11 revisions, injectable through the non-production test hook.
- **Status:** Open

## Resolved / Archived Items

Implemented, resolved, or superseded findings are retained here for historical context. Any current regression is tracked as a separate open item above.

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
- **Status:** Archived — implemented via the `pm_test_key`/`pm_test_value` hook in `scripts/sidebar-core.js`, gated on `process.env.BUILD !== 'production'`. The Kimi reload regression discovered later is tracked separately in the 2026-06-21 open items.

## 2026-06-16 - PromptMate Button Hidden While Panel Open

- **Type:** UX
- **Platform:** chatgpt.com
- **Related tests:** TC-008
- **Severity:** P2
- **Observed:** The floating PromptMate button becomes hidden while the panel is open, so users cannot close the panel by clicking the same button again.
- **Expected:** If the product supports toggle behavior, the button should remain visible/clickable or the test expectation should be updated to only support the close button.
- **Evidence:** TR-004 in `promptmate_test_results_2026-06-16.jsonl`.
- **Suggested fix:** Keep a visible active-state PromptMate pill while the panel is open, or update product copy/tests to make the close-button-only behavior explicit.
- **Status:** Archived — fixed by changing `updatePillVisibility()` to use `pm-active` instead of `pm-hidden`. The separate Claude close-handler regression discovered later is tracked in the 2026-06-21 open items.

## 2026-06-16 - Search Clear Button Missing

- **Type:** UX
- **Platform:** chatgpt.com
- **Related tests:** TC-012
- **Severity:** P2
- **Observed:** With a search query active, no visible clear-search X/button was found.
- **Expected:** Users should have a visible one-click affordance to clear search and restore the full library.
- **Evidence:** TR-008 in `promptmate_test_results_2026-06-16.jsonl`.
- **Suggested fix:** Add a visible clear button inside the search input when `query.length > 0`, with an accessible label such as `Clear search`.
- **Status:** Resolved — `buildSearch()` now provides an accessible clear button, and TC-012 passed on 2026-06-21 (TR-009 in `runs/2026-06-21/test_results.jsonl`).

## 2026-06-16 - Edit Validation Partially Persists Empty Title Edit

- **Type:** Bug
- **Platform:** chatgpt.com
- **Related tests:** TC-039
- **Severity:** P1
- **Observed:** Editing a prompt with an empty title left the modal open, but the prompt body changed to the attempted edit body.
- **Expected:** Invalid edits should be fully blocked; no title, body, group, history, or sync changes should persist until validation passes.
- **Evidence:** TR-032 in `promptmate_test_results_2026-06-16.jsonl`.
- **Suggested fix:** Run validation before any persistence/update side effects, and add a regression test asserting that failed validation leaves the original prompt object unchanged.
- **Status:** Resolved — TC-039 and TC-040 passed on 2026-06-21 (TR-035 and TR-036 in `runs/2026-06-21/test_results.jsonl`), confirming invalid edits no longer persisted partial changes.

## 2026-06-16 - Copy Action Copies Title Instead of Body

- **Type:** Bug
- **Platform:** chatgpt.com
- **Related tests:** TC-041
- **Severity:** P1
- **Observed:** Copy action on `AutoTest-TC037-edited` placed the prompt title on the clipboard instead of the prompt body.
- **Expected:** Copy should copy the prompt body exactly.
- **Evidence:** TR-034 in `promptmate_test_results_2026-06-16.jsonl`.
- **Suggested fix:** Check the prompt action handler receives the prompt body field, not the title/display label, and add clipboard unit coverage for prompt cards with distinct title/body.
- **Status:** Superseded — the title-copy symptom was not reproduced after validation was fixed. TC-041 still failed on 2026-06-21 with an empty clipboard, which is tracked as a separate open item above.

## 2026-06-16 - Chrome Automation Stability Limited Back-Half Coverage

- **Type:** Testability
- **Platform:** chatgpt.com
- **Related tests:** TC-042, TC-043, TC-044, TC-045, TC-046, TC-047, TC-048, TC-049, TC-051, TC-052, TC-053, TC-057, TC-058, TC-059, TC-060, TC-061, TC-062, TC-063, TC-064, TC-065, TC-067, TC-068, TC-069, TC-070, TC-072, TC-074, TC-075, TC-076, TC-077, TC-078, TC-079, TC-080, TC-081, TC-083, TC-084, TC-085, TC-086
- **Severity:** P2
- **Observed:** Chrome automation reset twice while working through the Version History section, preventing reliable completion of the back half of the suite in one session.
- **Expected:** QA harness should support resuming from a known test ID with stable AutoTest fixtures and minimal manual reconstruction.
- **Evidence:** Multiple `unable_to_test` results in `promptmate_test_results_2026-06-16.jsonl`.
- **Suggested fix:** Add a resumable runner checklist or split smoke/regression suites into smaller platform chunks, with fixture setup/cleanup guidance for AutoTest prompts and groups.
- **Status:** Archived — AGENTS.md now includes resume instructions and suite chunks. The narrower native-confirmation automation issue discovered later is tracked separately above.

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
