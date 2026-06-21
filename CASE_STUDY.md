# Agent-Driven QA for Chrome Extensions: Testability Gaps, Architecture, and Real Token Costs

**Author:** Jitan Gupta — Senior Platform Engineer  
**Date:** June 2026  
**Repo:** [promptmate-agent-qa-harness](https://github.com/jitangupta/promptmate-agent-qa-harness)

---

## Introduction

I set out to answer a simple question: can an AI agent reliably QA a real, shipped Chrome extension?

Not a toy. Not a demo. A production extension — [PromptMate](https://promptmate.world) — that runs inside Claude, ChatGPT, DeepSeek, and Kimi, renders a floating UI panel, manages a prompt library with cloud sync, and handles a full CRUD lifecycle including version history, trash, and restore.

The short answer is: yes, with important caveats. Agents can drive browser automation, execute test cases, and write structured results at a quality comparable to a junior QA engineer. But they hit walls that are invisible until they hit them. One wall in particular — the browser extension storage boundary — stopped me mid-run and required a product-side fix before testing could continue.

This report documents the architecture of the harness, the testability gap I found, how I fixed it, what a full run looks like in practice, and what it actually costs in tokens.

---

## 1. The Problem with Testing Chrome Extensions with Agents

Testing a web application with an AI agent is well-trodden ground. You point the agent at a URL, it drives the browser, checks DOM state, and reports results. The pattern is understood.

Chrome extensions break this model in two ways.

**First, the UI is injected, not native.** PromptMate renders its panel as a content script injected into the host page. The extension button and panel are part of the page DOM, but their structure changes across platform updates and can conflict with the host page's own z-index, focus management, and shadow DOM. Agents that rely on stable CSS selectors or fixed coordinates fail quickly. The harness teaches agents to prefer accessible text, visible labels, and DOM semantics — the same evidence a real user uses.

**Second, the extension has its own storage that the page cannot reach.** This is the harder problem. `chrome.storage.local` lives in the extension process, not the page context. A page script cannot read or write it. A DevTools console command cannot write it (only the Application tab can). An AI agent — which can inject scripts, manipulate the DOM, and navigate to URLs — cannot touch it at all.

This matters because modern extensions use `chrome.storage.local` for everything that needs to persist: feature flags, onboarding state, usage thresholds, and UI state like rating prompts. Any UI component gated on this storage is effectively invisible to agents until the product exposes a way in.

I discovered this gap mid-run, which cost me a full session.

---

## 2. Harness Architecture

The harness is a single repository containing:

- **`AGENTS.md`** — the agent runbook. Every agent (Codex, Claude Code, Claude Desktop) reads this file and follows the same instructions. No agent-specific forks. No drift.
- **`promptmate_test_cases.jsonl`** — 88 test cases across 4 platforms, one JSON object per line.
- **`fixtures/`** — JSON files documenting internal extension states that cannot be reached through navigation.
- **Result logs and reports** — dated JSONL result files and Markdown reports generated after each run.

The agent-neutral design is deliberate. I can run the same suite with Codex on Monday and Claude Code on Thursday and compare results without rewriting anything. The test cases describe what to do; the agent decides how to do it. This separation matters when you're evaluating agents themselves, not just the product under test.

The test suite is split into named chunks — `smoke`, `compose`, `personalize`, `context` — so a partial run or a targeted regression can be scoped without loading the full 88-case suite every time.

---

## 3. The Testability Gap: `chrome.storage.local` is Invisible to Agents

The PromptMate rating prompt — a "quick favor" dialog asking for a Chrome Web Store review — only appears when `chrome.storage.local` contains a specific key indicating the user has reached a usage threshold. The key is `promptmate.ratingPrompt`.

When I tried to write a test case for this dialog, I hit the wall. Here is the boundary in plain terms:

| | `localStorage` | `chrome.storage.local` |
|---|---|---|
| Lives in | Page context | Extension process |
| Writable by page script | Yes | No |
| Writable by DevTools console | Yes | Only via Application tab GUI |
| Writable by an AI agent | Via script injection | **Blocked** |

DevTools can reach it through a point-and-click GUI, but agents cannot open DevTools panels. I could have written the test as `unable_to_test` and moved on. Instead, I documented it in the development handoff and filed it as a testability gap requiring a product-side fix.

---

## 4. The Fix: The Testability Hook Pattern

The solution is a **testability seam** — a controlled entry point into internal extension state accessible through a channel agents already have: URL navigation.

PromptMate implements it as two URL parameters read by the content script on page load:

```
https://chatgpt.com?pm_test_key=promptmate.ratingPrompt&pm_test_value=<urlEncodedJSON>
```

When both parameters are present, the content script:

1. Reads `pm_test_key` and `pm_test_value`
2. Writes the value to `chrome.storage.local` at the given key
3. Removes the parameters from the URL
4. Reloads the page once

The next load behaves exactly as if the user had organically reached that storage state. The agent navigates to one URL and the extension is in the right state on the next load. No DevTools, no manual steps.

**The production gating requirement is non-negotiable.** Any page on any domain could craft a URL with these parameters and overwrite a user's extension state if this hook shipped in production. PromptMate gates it on `process.env.BUILD !== 'production'`, stripped at bundle time by `@rollup/plugin-replace`. The hook is compiled out entirely — not a runtime conditional, not a feature flag, not something that can be toggled. It does not exist in production builds.

**The pattern generalizes.** The same problem applies to any UI element gated on opaque browser storage:

- `localStorage` feature flags or A/B cohort assignments — agents *can* seed these via script injection, so this is less urgent
- `sessionStorage`-backed onboarding progress
- `IndexedDB`-backed state (usage thresholds, upgrade prompts)
- Cookies that gate paywalls or trial expiry banners

The rule of thumb: before writing a test case for any state-dependent UI component, ask whether an agent can reach that state through normal navigation. If the answer is no, design the testability hook before writing the test. Discovering the gap during a live run wastes a session.

---

## 5. A Full Run: What Actually Happened

The 2026-06-21 run used Codex Desktop (GPT-5.5) launched from VS Code, targeting ChatGPT, Claude, DeepSeek, and Kimi.

The session produced two log files — one for the main agent thread, one for the guardian subagent — which is how Codex Desktop structures multi-agent sessions. Together they cover:

- **351 API requests** across 18 turns
- **2 hours 32 minutes** of active agent time on the main session

The turn structure tells the story of the session:

| Turn | Time | Requests | What happened |
|---|---|---|---|
| 1 | 08:17 | 5 | Initial setup and orientation |
| 2 | 08:18 | 10 | First platform tests |
| 3 | 08:21 | 6 | Continued testing |
| *(gap)* | 08:21–09:44 | — | Rate limit window; I stepped away |
| 4 | 09:44 | 7 | Resumed; context rolled back once |
| 5 | 09:46 | **302** | Main bulk run — 57 minutes, 302 requests |
| 6 | 10:47 | 9 | Final wrap-up and report generation |

Turn 5 is the bulk of the session. A single continuous agentic turn running 302 API requests across 57 minutes, working through the test suite systematically. The context window grows with every request in a turn because the full conversation history is re-sent each time. By the end of Turn 5, each request was carrying roughly 180K+ tokens of context.

### The Guardian Subagent

The guardian is a Codex-native policy enforcement agent that I had not explicitly configured or invoked. Codex spawned it automatically whenever the main agent proposed an action that touched the filesystem or ran a tool call. The guardian's job, per its system prompt:

> *"You are judging one planned coding-agent action. Assess the exact action's intrinsic risk and whether the transcript authorizes its target and side effects."*

It ran 12 turns with exactly 1 API request per turn — one judgment per proposed action. Each evaluation took 3–6 seconds. The guardian added $1.01 to the total cost and added a small but consistent latency to any action requiring approval. For a QA harness that calls tools frequently, this is worth factoring into session time estimates.

---

## 6. Token Economics

The full run processed **55.85 million input tokens** and **95,767 output tokens** across both sessions.

Those numbers sound alarming until you understand cache hit rate.

### Why input tokens accumulate so fast

Codex re-sends the full conversation history with every API request. A session with a growing context window and 302 requests in a single turn is not 302 independent calls — it is 302 calls each carrying an increasingly large history. By the end of Turn 5, each request included the base instructions, the full test case list, every prior result, and all intermediate agent reasoning. The context grew to approximately 180K tokens per request.

### Cache hit rate saves the session

Of the 55.85M input tokens processed, **54.84M were served from cache** — a **98.1% cache hit rate**. This is prompt caching working exactly as designed: the stable prefix (base instructions, test cases, prior results) is cached and served cheaply on each subsequent request. Only the novel delta in each request is billed at the full input rate.

| Token type | Count | Rate | Cost |
|---|---|---|---|
| Fresh input | 1.01M | $5.00 / 1M | $5.05 |
| Cached input | 54.84M | $0.50 / 1M | $27.42 |
| Output | 95.8K | $30.00 / 1M | $2.87 |
| **Total** | | | **$35.34** |

Without caching, the same 55.85M input tokens at full rate would have cost **$279.25** in input alone — roughly 8× higher. The cache hit rate compressed the effective cost to $35.34.

### What this means for planning

A full 88-test-case run across 4 platforms costs approximately **$35 API-equivalent** with Codex Desktop at current GPT-5.5 rates. The dominant cost is cached input — the large, stable context that gets re-sent on every request. This scales with session length and context size more than with the number of test cases.

Practical estimates for similar harnesses:
- A 30-minute targeted chunk (20 test cases, 1 platform): ~$5–8
- A full suite run with interruptions and rollbacks: ~$35–45
- A run with a significantly larger system prompt or test fixture set: proportionally more cached input, but similar fresh-input and output costs

---

## 7. Lessons for AI Deployment

These observations generalize beyond PromptMate and beyond Chrome extensions.

**Design testability hooks before writing test cases.** Any product state that lives outside the page context — extension storage, native app state, server-side flags — is invisible to agents by default. Find those boundaries upfront, design the hook, gate it from production, then write the tests. The reverse order wastes runs.

**Agent-neutral runbooks pay off immediately.** Writing `AGENTS.md` as the single source of truth, with no agent-specific instructions, meant I could switch between Codex and Claude Code without rewriting anything. If you are evaluating multiple agents, the harness should not be one of the variables.

**Cache hit rate is the real cost lever.** The difference between $35 and $279 for the same run is cache hit rate. Sessions with large, stable context prefixes benefit enormously from prompt caching. Design your agent context so that the stable parts (instructions, test cases, known state) come before the volatile parts (results, intermediate reasoning) in the context window.

**The guardian is not overhead — it is legible authorization.** Every action the main agent took that required file or tool access was evaluated by the guardian before execution. This adds latency, but it gives you an auditable record of what the agent was permitted to do and why. For enterprise deployments where authorization is a compliance requirement, this pattern is worth understanding and potentially replicating at the application layer.

**Token accumulation in long agentic turns is predictable and manageable.** Knowing that a single continuous turn re-sends the full context on every request lets you plan session structure deliberately. Breaking a long run into shorter turns (by having the agent checkpoint and resume) resets the growing context and keeps per-request token counts manageable. This is especially relevant for runs that approach the model's context window limit.

---

## Conclusion

Agent-driven QA for real products works — with the right harness design and upfront investment in testability. The chrome.storage.local gap is not unique to PromptMate; it is a structural property of the Chrome extension model that any extension developer will encounter when they try to automate state-dependent UI testing with an agent.

The token economics are tractable. A full QA session costs roughly what you'd pay for a junior QA contractor for a couple of hours, runs in the background while you work on other things, produces structured JSONL output, and catches regressions at a consistency that manual testing does not.

The remaining gap is judgment. Agents are good at checking whether an element exists, whether a button is clickable, whether text appears after an action. They are less reliable at assessing whether a workflow *feels* right to a real user — the friction, the copy clarity, the recovery paths. The harness includes a usability review rule specifically to push agents toward surfacing this, but it requires deliberate prompting rather than emerging naturally.

The code, test cases, fixtures, runbook, and token dashboard for this run are in the [promptmate-agent-qa-harness](https://github.com/jitangupta/promptmate-agent-qa-harness) repository.

---

*Pricing reference: GPT-5.5 API — $5.00/1M input · $0.50/1M cached input · $30.00/1M output (June 2026). Codex Desktop operates on a subscription rate-limit model; cost figures represent API-equivalent rates at standard per-token pricing.*
