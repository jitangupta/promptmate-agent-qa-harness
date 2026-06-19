# PromptMate Test Report - 2026-06-16

## Summary

| Platform | Pass | Fail | Skip | Unable | Total |
|---|---:|---:|---:|---:|---:|
| chatgpt.com | 30 | 6 | 1 | 42 | 79 |
| **TOTAL** | **30** | **6** | **1** | **42** | **79** |

## Results Matrix

| ID | Category | Test Name | chatgpt.com |
|---|---|---|---|
| TC-002 | Extension Presence | Button visible on chatgpt.com | pass |
| TC-006 | Panel UI | Panel opens on button click | pass |
| TC-007 | Panel UI | Panel closes via close button | pass |
| TC-008 | Panel UI | Panel closes via PromptMate button re-click | fail |
| TC-009 | Search | Search filters by title | pass |
| TC-010 | Search | Search filters by body content | pass |
| TC-011 | Search | Search empty state | pass |
| TC-012 | Search | Clear search via X button | fail |
| TC-013 | Search | Search is case-insensitive | pass |
| TC-014 | Tone & Format | Section expands and collapses | fail |
| TC-015 | Tone & Format | Tone dropdown has correct options | pass |
| TC-016 | Tone & Format | Format dropdown has correct options | pass |
| TC-017 | Tone & Format | Selection persists in collapsed summary | pass |
| TC-018 | Tone & Format | Tone & Format appended when prompt is used | pass |
| TC-019 | Prompt Library | Grouped sections display prompts | pass |
| TC-020 | Prompt Library | Empty library state | unable_to_test |
| TC-021 | Prompt Library | PINNED section appears above RECENT when prompts are pinned | unable_to_test |
| TC-022 | Prompt Library | Prompts ordered by recency in RECENT | unable_to_test |
| TC-024 | Prompt Injection | Use injects prompt on chatgpt.com | pass |
| TC-027 | Prompt Injection | Use increments usage counter | pass |
| TC-028 | Pin / Unpin | Pin moves prompt to PINNED section | fail |
| TC-029 | Pin / Unpin | Unpin returns prompt to RECENT | pass |
| TC-030 | Pin / Unpin | Multiple prompts can be pinned simultaneously | unable_to_test |
| TC-031 | Prompt CRUD | New prompt modal opens with correct fields | pass |
| TC-032 | Prompt CRUD | Create new prompt successfully | pass |
| TC-033 | Prompt CRUD | Create prompt - Cancel discards | pass |
| TC-034 | Prompt CRUD | Create prompt - empty title is blocked | pass |
| TC-035 | Prompt CRUD | Create prompt - empty body is blocked | pass |
| TC-036 | Prompt CRUD | Edit opens modal pre-filled | pass |
| TC-037 | Prompt CRUD | Edit save persists changes | pass |
| TC-038 | Prompt CRUD | Edit cancel discards changes | pass |
| TC-039 | Prompt CRUD | Edit - empty title is blocked | fail |
| TC-040 | Prompt CRUD | Edit - empty body is blocked | pass |
| TC-041 | Prompt CRUD | Copy puts prompt body on clipboard | fail |
| TC-042 | Version History | History modal opens with revision list | unable_to_test |
| TC-043 | Version History | Show changes reveals diff | unable_to_test |
| TC-044 | Version History | Hide changes collapses diff | unable_to_test |
| TC-045 | Version History | Restore creates a new revision | unable_to_test |
| TC-046 | Version History | History capped at 10 revisions | unable_to_test |
| TC-047 | Trash | Delete moves prompt to Trash | unable_to_test |
| TC-048 | Trash | Deleted prompt appears in Trash with 30-day label | unable_to_test |
| TC-049 | Trash | Restore from Trash returns prompt to library | unable_to_test |
| TC-050 | Trash | Delete forever permanently removes prompt | skip |
| TC-051 | Trash | Navigate to Trash and back to library | unable_to_test |
| TC-052 | Cloud Sync | Sync indicator appears after a change | unable_to_test |
| TC-053 | Cloud Sync | Prompts persist after page reload | unable_to_test |
| TC-054 | Cloud Sync | Prompt created on one platform appears on another | pass |
| TC-055 | Account | Logged-in email is displayed | pass |
| TC-056 | Account | Sign out button is present | pass |
| TC-057 | Help & Feedback | User Guide opens in a new tab | unable_to_test |
| TC-058 | Help & Feedback | Rate PromptMate link is present and clickable | unable_to_test |
| TC-059 | Help & Feedback | Request a feature link is present and clickable | unable_to_test |
| TC-060 | Edge Cases | Very long title does not break layout | unable_to_test |
| TC-061 | Edge Cases | Very long body injects without truncation | unable_to_test |
| TC-062 | Edge Cases | Prompt with special characters saves and injects correctly | unable_to_test |
| TC-063 | Edge Cases | Duplicate prompt titles are allowed | unable_to_test |
| TC-064 | Edge Cases | Escape key closes modals without saving | unable_to_test |
| TC-065 | Variables | Editor detects double-brace variables | unable_to_test |
| TC-066 | Variables | Prompt card shows variable count badge | pass |
| TC-067 | Variables | Use opens fill-in dialog for variable prompt | unable_to_test |
| TC-068 | Variables | Insert disabled until required variables are filled | unable_to_test |
| TC-069 | Variables | Live preview replaces variable values | unable_to_test |
| TC-070 | Variables | Variable insert injects resolved prompt | unable_to_test |
| TC-071 | Groups | Group headers show names and counts | pass |
| TC-072 | Groups | Group expand and collapse toggles cards | unable_to_test |
| TC-073 | Groups | Group actions menu exposes management actions | pass |
| TC-074 | Groups | Rename group updates header | unable_to_test |
| TC-075 | Groups | Group instruction dialog opens | unable_to_test |
| TC-076 | Groups | Group instruction save persists enabled state and text | unable_to_test |
| TC-077 | Groups | Group instruction is included during insertion | unable_to_test |
| TC-078 | Groups | Move to group changes prompt grouping | unable_to_test |
| TC-079 | User Context | Your context dialog opens from PromptMate menu | unable_to_test |
| TC-080 | User Context | Use context toggle controls attachment | unable_to_test |
| TC-081 | User Context | Add or edit context persists ABOUT YOU text | unable_to_test |
| TC-082 | User Context | Pull it from this chat extracts context draft | unable_to_test |
| TC-083 | User Context | Context is included during insertion when enabled | unable_to_test |
| TC-084 | User Context | Context is omitted during insertion when disabled | unable_to_test |
| TC-085 | Prompt Preview | Preview opens resolved prompt preview | unable_to_test |
| TC-086 | Prompt Preview | Preview respects variables and insertion controls | unable_to_test |

Legend: pass | fail | skip | unable_to_test | n/a not applicable

## Failures & Issues

### [TC-008] Panel closes via PromptMate button re-click - chatgpt.com

**Expected:** PromptMate button remains clickable and closes the panel when clicked again.
**Actual:** The PromptMate button became hidden while the panel was open.
**Notes:** Users must use the panel close button instead.

### [TC-012] Clear search via X button - chatgpt.com

**Expected:** A visible clear X resets the search.
**Actual:** No visible clear-search button was found with a query active.
**Notes:** Keyboard clearing worked as a workaround.

### [TC-014] Tone & Format expands and collapses - chatgpt.com

**Expected:** Tone & Format toggles open/closed.
**Actual:** The section appeared as an already-open details/select area; no collapse behavior was verified.

### [TC-028] Pin moves prompt to PINNED section - chatgpt.com

**Expected:** Pinning an AutoTest prompt creates a visible PINNED section and moves the prompt.
**Actual:** Pin action did not produce a visible PINNED section during the run.

### [TC-039] Edit empty title is blocked - chatgpt.com

**Expected:** Empty-title edit is fully blocked and no prompt fields persist.
**Actual:** The modal stayed open, but the card body changed to the attempted body.
**Notes:** This is a data integrity issue because a validation failure partially persisted.

### [TC-041] Copy puts prompt body on clipboard - chatgpt.com

**Expected:** Copy action copies the prompt body.
**Actual:** Clipboard contained the prompt title `AutoTest-TC037-edited`.

## Development Handoff Additions

- 2026-06-16 - PromptMate Button Hidden While Panel Open
- 2026-06-16 - Search Clear Button Missing
- 2026-06-16 - Edit Validation Partially Persists Empty Title Edit
- 2026-06-16 - Copy Action Copies Title Instead of Body
- 2026-06-16 - Chrome Automation Stability Limited Back-Half Coverage

## Observations & Recommendations

The core ChatGPT injection path, search matching, new prompt creation, edit save/cancel, account footer, variable badge display, and group header display worked.

The run was partial because Chrome automation reset twice while entering the Version History portion. Re-run TC-042 onward in a fresh Chrome automation session, ideally starting from a clean AutoTest group and prompt set.
