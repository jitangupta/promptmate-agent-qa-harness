# PromptMate Test Report - 2026-06-21

## Summary

| Platform | Pass | Fail | Skip | Unable | Total |
|---|---:|---:|---:|---:|---:|
| claude.ai | 18 | 3 | 0 | 1 | 22 |
| chatgpt.com | 20 | 1 | 0 | 2 | 23 |
| chat.deepseek.com | 19 | 1 | 1 | 0 | 21 |
| kimi.com | 17 | 1 | 0 | 2 | 20 |
| **TOTAL** | **74** | **6** | **1** | **5** | **86** |

Authentication tests TC-055 and TC-056 were excluded by request. Each remaining test was assigned to one supported platform and executed once. TC-054 used its required Claude-to-ChatGPT path.

## Results Matrix

| ID | Category | Test Name | claude.ai | chatgpt.com | chat.deepseek.com | kimi.com |
|---|---|---|---|---|---|---|
| TC-001 | Extension Presence | Button visible on claude.ai | pass | n/a | n/a | n/a |
| TC-002 | Extension Presence | Button visible on chatgpt.com | n/a | pass | n/a | n/a |
| TC-003 | Extension Presence | Button visible on chat.deepseek.com | n/a | n/a | pass | n/a |
| TC-004 | Extension Presence | Button visible on kimi.com | n/a | n/a | n/a | pass |
| TC-005 | Extension Presence | Button NOT present on unsupported sites | pass | n/a | n/a | n/a |
| TC-006 | Panel UI | Panel opens on button click | pass | n/a | n/a | n/a |
| TC-007 | Panel UI | Panel closes via × button | pass | n/a | n/a | n/a |
| TC-008 | Panel UI | Panel closes via PromptMate button re-click | fail | n/a | n/a | n/a |
| TC-009 | Search | Search filters by title | pass | n/a | n/a | n/a |
| TC-010 | Search | Search filters by body content | pass | n/a | n/a | n/a |
| TC-011 | Search | Search empty state | pass | n/a | n/a | n/a |
| TC-012 | Search | Clear search via × button | pass | n/a | n/a | n/a |
| TC-013 | Search | Search is case-insensitive | pass | n/a | n/a | n/a |
| TC-014 | Tone & Format | Section expands and collapses | pass | n/a | n/a | n/a |
| TC-015 | Tone & Format | Tone dropdown has correct options | pass | n/a | n/a | n/a |
| TC-016 | Tone & Format | Format dropdown has correct options | pass | n/a | n/a | n/a |
| TC-017 | Tone & Format | Selection persists in collapsed summary | pass | n/a | n/a | n/a |
| TC-018 | Tone & Format | Tone & Format appended when prompt is used | pass | n/a | n/a | n/a |
| TC-019 | Prompt Library | Grouped sections display prompts | pass | n/a | n/a | n/a |
| TC-020 | Prompt Library | Empty library state | unable_to_test | n/a | n/a | n/a |
| TC-021 | Prompt Library | PINNED section appears above RECENT when prompts are pinned | fail | n/a | n/a | n/a |
| TC-022 | Prompt Library | Prompts ordered by recency in RECENT | pass | n/a | n/a | n/a |
| TC-023 | Prompt Injection | Use injects prompt on claude.ai | pass | n/a | n/a | n/a |
| TC-024 | Prompt Injection | Use injects prompt on chatgpt.com | n/a | pass | n/a | n/a |
| TC-025 | Prompt Injection | Use injects prompt on chat.deepseek.com | n/a | n/a | pass | n/a |
| TC-026 | Prompt Injection | Use injects prompt on kimi.com | n/a | n/a | n/a | pass |
| TC-027 | Prompt Injection | Use increments usage counter | pass | n/a | n/a | n/a |
| TC-028 | Pin / Unpin | Pin moves prompt to PINNED section | fail | n/a | n/a | n/a |
| TC-029 | Pin / Unpin | Unpin returns prompt to RECENT | n/a | pass | n/a | n/a |
| TC-030 | Pin / Unpin | Multiple prompts can be pinned simultaneously | n/a | pass | n/a | n/a |
| TC-031 | Prompt CRUD | New prompt modal opens with correct fields | n/a | pass | n/a | n/a |
| TC-032 | Prompt CRUD | Create new prompt successfully | n/a | pass | n/a | n/a |
| TC-033 | Prompt CRUD | Create prompt — Cancel discards | n/a | pass | n/a | n/a |
| TC-034 | Prompt CRUD | Create prompt — empty title is blocked | n/a | pass | n/a | n/a |
| TC-035 | Prompt CRUD | Create prompt — empty body is blocked | n/a | pass | n/a | n/a |
| TC-036 | Prompt CRUD | Edit opens modal pre-filled | n/a | pass | n/a | n/a |
| TC-037 | Prompt CRUD | Edit save persists changes | n/a | pass | n/a | n/a |
| TC-038 | Prompt CRUD | Edit cancel discards changes | n/a | pass | n/a | n/a |
| TC-039 | Prompt CRUD | Edit — empty title is blocked | n/a | pass | n/a | n/a |
| TC-040 | Prompt CRUD | Edit — empty body is blocked | n/a | pass | n/a | n/a |
| TC-041 | Prompt CRUD | Copy puts prompt body on clipboard | n/a | fail | n/a | n/a |
| TC-042 | Version History | History modal opens with revision list | n/a | pass | n/a | n/a |
| TC-043 | Version History | Show changes reveals diff | n/a | pass | n/a | n/a |
| TC-044 | Version History | Hide changes collapses diff | n/a | pass | n/a | n/a |
| TC-045 | Version History | Restore creates a new revision | n/a | unable_to_test | n/a | n/a |
| TC-046 | Version History | History capped at 10 revisions | n/a | unable_to_test | n/a | n/a |
| TC-047 | Trash | Delete moves prompt to Trash | n/a | pass | n/a | n/a |
| TC-048 | Trash | Deleted prompt appears in Trash with 30-day label | n/a | pass | n/a | n/a |
| TC-049 | Trash | Restore from Trash returns prompt to library | n/a | n/a | pass | n/a |
| TC-050 | Trash | Delete forever permanently removes prompt | n/a | n/a | skip | n/a |
| TC-051 | Trash | Navigate to Trash and back to library | n/a | n/a | pass | n/a |
| TC-052 | Cloud Sync | Sync indicator appears after a change | n/a | n/a | pass | n/a |
| TC-053 | Cloud Sync | Prompts persist after page reload | n/a | n/a | pass | n/a |
| TC-054 | Cloud Sync | Prompt created on one platform appears on another | n/a | pass | n/a | n/a |
| TC-057 | Help & Feedback | User Guide opens in a new tab | n/a | n/a | pass | n/a |
| TC-058 | Help & Feedback | Rate PromptMate link is present and clickable | n/a | n/a | pass | n/a |
| TC-059 | Help & Feedback | Request a feature link is present and clickable | n/a | n/a | pass | n/a |
| TC-060 | Edge Cases | Very long title does not break layout | n/a | n/a | pass | n/a |
| TC-061 | Edge Cases | Very long body injects without truncation | n/a | n/a | pass | n/a |
| TC-062 | Edge Cases | Prompt with special characters saves and injects correctly | n/a | n/a | pass | n/a |
| TC-063 | Edge Cases | Duplicate prompt titles are allowed | n/a | n/a | pass | n/a |
| TC-064 | Edge Cases | Escape key closes modals without saving | n/a | n/a | fail | n/a |
| TC-065 | Variables | Editor detects double-brace variables | n/a | n/a | pass | n/a |
| TC-066 | Variables | Prompt card shows variable count badge | n/a | n/a | pass | n/a |
| TC-067 | Variables | Use opens fill-in dialog for variable prompt | n/a | n/a | pass | n/a |
| TC-068 | Variables | Insert disabled until required variables are filled | n/a | n/a | pass | n/a |
| TC-069 | Variables | Live preview replaces variable values | n/a | n/a | pass | n/a |
| TC-070 | Variables | Variable insert injects resolved prompt | n/a | n/a | n/a | pass |
| TC-071 | Groups | Group headers show names and counts | n/a | n/a | n/a | pass |
| TC-072 | Groups | Group expand and collapse toggles cards | n/a | n/a | n/a | pass |
| TC-073 | Groups | Group actions menu exposes management actions | n/a | n/a | n/a | pass |
| TC-074 | Groups | Rename group updates header | n/a | n/a | n/a | pass |
| TC-075 | Groups | Group instruction dialog opens | n/a | n/a | n/a | pass |
| TC-076 | Groups | Group instruction save persists enabled state and text | n/a | n/a | n/a | pass |
| TC-077 | Groups | Group instruction is included during insertion | n/a | n/a | n/a | pass |
| TC-078 | Groups | Move to group changes prompt grouping | n/a | n/a | n/a | pass |
| TC-079 | User Context | Your context dialog opens from PromptMate menu | n/a | n/a | n/a | pass |
| TC-080 | User Context | Use context toggle controls attachment | n/a | n/a | n/a | pass |
| TC-081 | User Context | Add or edit context persists ABOUT YOU text | n/a | n/a | n/a | pass |
| TC-082 | User Context | Pull it from this chat extracts context draft | n/a | n/a | n/a | unable_to_test |
| TC-083 | User Context | Context is included during insertion when enabled | n/a | n/a | n/a | pass |
| TC-084 | User Context | Context is omitted during insertion when disabled | n/a | n/a | n/a | pass |
| TC-085 | Prompt Preview | Preview opens resolved prompt preview | n/a | n/a | n/a | pass |
| TC-086 | Prompt Preview | Preview respects variables and insertion controls | n/a | n/a | pass | n/a |
| TC-087 | Rating Prompt | Rating prompt banner appears when eligible | n/a | n/a | n/a | fail |
| TC-088 | Rating Prompt | Rating prompt banner dismiss closes it and does not reappear | n/a | n/a | n/a | unable_to_test |

Legend: pass | fail | skip | unable_to_test | n/a not applicable

## Failures & Issues

### [TC-008] Panel closes via PromptMate button re-click - claude.ai

**Expected:** Clicking the active floating PromptMate pill closes the panel.

**Actual:** The pill remained labelled `Close PromptMate`, but the panel stayed open. The panel-header Close button worked.

**Notes:** See TR-005.

### [TC-021, TC-028] Pinning immediately creates and moves into PINNED - claude.ai

**Expected:** Pinning creates a PINNED section and moves the prompt there.

**Actual:** The action state changed, but the card initially remained under Group1 and no visible pinned section appeared during the short verification window. Later pin/move checks on other platforms settled after several seconds.

**Notes:** Treat as a synchronization/feedback failure rather than evidence of permanent data loss. See TR-018, TR-022, TR-026, and TR-076.

### [TC-041] Copy puts prompt body on clipboard - chatgpt.com

**Expected:** Clipboard contains the exact prompt body.

**Actual:** Clipboard was empty; paste reported no clipboard data.

**Notes:** See TR-037.

### [TC-064] Escape closes modal without saving - chat.deepseek.com

**Expected:** Escape dismisses the New prompt modal and discards its draft.

**Actual:** The modal remained open with the typed title/body still present.

**Notes:** See TR-059.

### [TC-087] Rating banner appears when eligible - kimi.com

**Expected:** The test hook writes the eligible state, removes URL parameters, reloads once, and shows the A QUICK FAVOR banner.

**Actual:** The parameters remained in the URL and Kimi repeatedly reloaded; the PromptMate button alternated between present and absent and the banner never stabilized.

**Notes:** TC-088 was consequently unable to test. See TR-084 and TR-085.

### Unable and skipped coverage

- TC-020: no safe empty-library fixture; deleting existing user prompts was not acceptable.
- TC-045: accepting the native restore confirmation repeatedly stalled Chrome automation, so the restored revision could not be verified.
- TC-046: no prompt had more than 10 revisions; the richest candidate had 8.
- TC-050: skipped by irreversible-delete policy because permanent deletion was not separately approved.
- TC-082: Kimi required login to send the synthetic seed message; authentication was not attempted.
- TC-088: blocked because TC-087 did not produce a stable banner.

## Development Handoff Additions

- 2026-06-21 - Claude Floating Pill Does Not Close the Open Panel
- 2026-06-21 - Pin and Move Updates Appear Several Seconds Late
- 2026-06-21 - Copy Action Leaves Clipboard Empty
- 2026-06-21 - Escape Does Not Dismiss New Prompt Modal
- 2026-06-21 - Native Confirm Dialogs Stall Agent Automation
- 2026-06-21 - Rating Test Hook Reloads Kimi Repeatedly
- 2026-06-21 - Missing Safe Fixtures for Empty Library and 10+ Revisions

## Observations & Recommendations

- Core extension presence, panel opening, search, tone/format, CRUD validation, prompt injection, variables, groups, context attachment, preview, trash restore, and cloud sync were broadly successful.
- Prompt injection worked on all four supported sites. Long bodies, special characters, duplicate titles, variable resolution, group instructions, and context ordering behaved correctly.
- Pin and Move actions need clearer pending feedback; the menu can report the new state several seconds before the card/count UI reconciles.
- Replace native JavaScript confirmations with accessible extension dialogs so restore and destructive-action tests can complete reliably.
- Add agent-safe fixtures for empty libraries and 11+ revision histories.
- Cleanup soft-deleted the AutoTest prompts created during this run and restored the pre-run empty user-context text with Use context enabled. Deleting the now-empty AutoTest group hit the native-confirmation automation issue, so its final removal could not be verified.
