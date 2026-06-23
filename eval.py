"""
PromptMate Agent QA - Consistency Eval

Measures how reliably the agent gives the same verdict for the same test
across multiple runs. This is the first eval metric for the harness.

Usage:
    python eval.py
    python eval.py --json   (machine-readable output)
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
RUNS_DIR = ROOT / "runs"
HANDOFF_FILE = ROOT / "DEVELOPMENT_HANDOFF.md"

EVALUABLE = {"pass", "fail"}           # statuses that represent real verdicts
INCONCLUSIVE = {"unable_to_test", "skip"}  # not a verdict on the product


def load_runs():
    runs = {}
    for run_dir in sorted(RUNS_DIR.iterdir()):
        if not run_dir.is_dir():
            continue
        results_file = run_dir / "test_results.jsonl"
        if not results_file.exists():
            continue
        entries = {}
        with open(results_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                tid = obj["test_id"]
                entries[tid] = {
                    "status": obj["status"],
                    "platform": obj.get("platform", "unknown"),
                    "notes": obj.get("notes", ""),
                }
        runs[run_dir.name] = entries
    return runs


def load_handoff_tids():
    if not HANDOFF_FILE.exists():
        return set()
    text = HANDOFF_FILE.read_text(encoding="utf-8")
    return set(re.findall(r"TC-\d{3}", text))


def classify(tid, appearances, handoff_tids):
    """
    Classify a test ID given its appearances across runs.

    Returns one of:
      consistent       - same evaluable status every time it ran
      scope_gap        - never produced conflicting evaluable verdicts;
                         variation was only unable_to_test or skip
      regression       - conflicting evaluable statuses + documented in HANDOFF
      inconsistent     - conflicting evaluable statuses + NOT in HANDOFF
      single_run       - only one data point, nothing to compare
    """
    if len(appearances) < 2:
        return "single_run"

    evaluable_statuses = {
        date: v["status"]
        for date, v in appearances.items()
        if v["status"] in EVALUABLE
    }

    # No evaluable verdicts at all (all unable/skip)
    if not evaluable_statuses:
        return "scope_gap"

    unique_verdicts = set(evaluable_statuses.values())

    if len(unique_verdicts) == 1:
        # Only one distinct evaluable verdict — consistent regardless of
        # how many unable_to_test rows also exist
        return "consistent"

    # Conflicting evaluable verdicts (pass in one run, fail in another)
    if tid in handoff_tids:
        return "regression"
    return "inconsistent"


def run_eval():
    runs_data = load_runs()
    handoff_tids = load_handoff_tids()
    run_dates = sorted(runs_data.keys())

    all_tids = sorted({tid for run in runs_data.values() for tid in run})

    buckets = defaultdict(list)

    for tid in all_tids:
        appearances = {
            date: runs_data[date][tid]
            for date in run_dates
            if tid in runs_data[date]
        }
        cat = classify(tid, appearances, handoff_tids)
        buckets[cat].append((tid, appearances))

    return buckets, run_dates, handoff_tids


def short_platform(p):
    return (
        p.replace("https://", "")
        .replace("http://", "")
        .replace("chatgpt.com", "chatgpt")
        .replace("claude.ai", "claude")
        .replace("chat.deepseek.com", "deepseek")
        .replace("kimi.com", "kimi")
    )


def status_cell(v):
    icons = {
        "pass": "PASS  ",
        "fail": "FAIL  ",
        "unable_to_test": "UNABLE",
        "skip": "SKIP  ",
    }
    s = icons.get(v["status"], v["status"].upper()[:6])
    return f"{s}({short_platform(v['platform'])})"


def print_report(buckets, run_dates, handoff_tids):
    consistent = buckets["consistent"]
    scope_gap = buckets["scope_gap"]
    regression = buckets["regression"]
    inconsistent = buckets["inconsistent"]
    single_run = buckets["single_run"]

    total_multi = len(consistent) + len(scope_gap) + len(regression) + len(inconsistent)
    explained = len(consistent) + len(scope_gap) + len(regression)
    rate = explained / total_multi * 100 if total_multi else 0

    W = 72
    print("=" * W)
    print("  PROMPTMATE AGENT QA - CONSISTENCY EVAL")
    print("=" * W)
    print(f"  Runs         : {', '.join(run_dates)}")
    print(f"  Handoff refs : {len(handoff_tids)} unique TC-IDs in DEVELOPMENT_HANDOFF.md")
    print()

    print("  SUMMARY")
    print("  " + "-" * 50)
    print(f"  {'Multi-run test IDs':<35} {total_multi:>4}")
    print(f"  {'  consistent (same verdict always)':<35} {len(consistent):>4}")
    print(f"  {'  scope gaps (only unable/skip vary)':<35} {len(scope_gap):>4}")
    print(f"  {'  confirmed regressions':<35} {len(regression):>4}   << real bugs caught")
    print(f"  {'  genuine inconsistencies':<35} {len(inconsistent):>4}   << investigate these")
    print(f"  {'Single-run only (no comparison)':<35} {len(single_run):>4}")
    print()
    print(f"  CONSISTENCY RATE  {rate:.1f}%")
    print(f"  ({explained} explained / {total_multi} multi-run)  target: >= 90%")
    print()

    # --- Confirmed regressions ---
    if regression:
        print("  CONFIRMED REGRESSIONS  (agent caught real product bugs)")
        print("  " + "-" * (W - 2))
        header = f"  {'Test ID':<10}" + "".join(f"  {d:<28}" for d in run_dates)
        print(header)
        for tid, apps in regression:
            row = f"  {tid:<10}"
            for date in run_dates:
                cell = status_cell(apps[date]) if date in apps else "---   "
                row += f"  {cell:<28}"
            print(row)
        print()

    # --- Genuine inconsistencies ---
    if inconsistent:
        print("  GENUINE INCONSISTENCIES  (same feature, different verdict - no HANDOFF entry)")
        print("  These represent harness or agent reliability gaps.")
        print("  " + "-" * (W - 2))
        header = f"  {'Test ID':<10}" + "".join(f"  {d:<28}" for d in run_dates)
        print(header)
        for tid, apps in inconsistent:
            row = f"  {tid:<10}"
            for date in run_dates:
                cell = status_cell(apps[date]) if date in apps else "---   "
                row += f"  {cell:<28}"
            print(row)
            # Print fail notes (truncated) to help diagnosis
            for date, v in sorted(apps.items()):
                if v["status"] == "fail":
                    note = v["notes"]
                    if len(note) > 130:
                        note = note[:130] + "..."
                    print(f"    [{date} FAIL] {note}")
        print()

    # --- Action plan ---
    print("  WHAT TO DO NEXT")
    print("  " + "-" * (W - 2))
    if inconsistent:
        print(f"  1. Review {len(inconsistent)} genuine inconsistencies above.")
        print("     For each: manually verify current product state, then either:")
        print("       a) Add a DEVELOPMENT_HANDOFF entry if a real bug exists")
        print("       b) Tighten the test case assertion if the expected behaviour")
        print("          was ambiguous (the agent may have interpreted it differently")
        print("          on different platforms or builds)")
    else:
        print("  No genuine inconsistencies — harness is fully consistent.")
    print()
    print("  2. Run the same chunk on a second agent (Claude Code vs Codex)")
    print("     and compare results - that adds an inter-agent dimension to the eval.")
    print()
    print("  3. After 2 more runs: re-run this script and track rate over time.")
    print("     Trending toward 90%+ means the harness is becoming reliable.")
    print("=" * W)


def json_output(buckets, run_dates):
    def serialise(items):
        return [
            {
                "test_id": tid,
                "runs": {
                    date: {"status": v["status"], "platform": v["platform"]}
                    for date, v in apps.items()
                },
            }
            for tid, apps in items
        ]

    consistent = buckets["consistent"]
    scope_gap = buckets["scope_gap"]
    regression = buckets["regression"]
    inconsistent = buckets["inconsistent"]
    total_multi = len(consistent) + len(scope_gap) + len(regression) + len(inconsistent)
    explained = len(consistent) + len(scope_gap) + len(regression)

    print(json.dumps({
        "runs": run_dates,
        "consistency_rate": round(explained / total_multi * 100, 1) if total_multi else 0,
        "summary": {
            "consistent": len(consistent),
            "scope_gap": len(scope_gap),
            "regression": len(regression),
            "inconsistent": len(inconsistent),
            "single_run": len(buckets["single_run"]),
        },
        "regression": serialise(regression),
        "inconsistent": serialise(inconsistent),
    }, indent=2))


if __name__ == "__main__":
    buckets, run_dates, handoff_tids = run_eval()
    # Fix single_run: it's a list of (tid, apps) pairs but apps has 1 entry
    # Reformat for the summary count
    if "--json" in sys.argv:
        json_output(buckets, run_dates)
    else:
        print_report(buckets, run_dates, handoff_tids)
