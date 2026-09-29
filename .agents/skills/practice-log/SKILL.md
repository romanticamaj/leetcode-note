---
name: practice-log
description: Use when the user reports finishing a LeetCode problem, gives a 心得/reflection about one, or mentions a practice date — e.g. "完成 226", "今天新增一題: 141. Linked List Cycle", "心得：...". Also use when the user asks to sync or update Checklists/Lists.
---

# Practice Log

Record what the user solved, then **always** sync the lists. The sync is not optional and not "on request" — a log edit without a sync is the bug this skill exists to prevent.

## Steps

1. **Edit `Checklists/Practice_Log.md`**
   - Find the `## YYYY-MM-DD` block for the stated date (default: today — check with `date +%F`). If missing, create it **at the top** (newest first), with an empty `**心得**：` line.
   - Add `- <num>. <title>` under the date. Keep the user's numbering; look up the title if only a number is given.
   - For a 心得: put it under that day's `**心得**：`. If the day has >1 problem, use `- <num>：...` bullets. Fix typos only; keep the user's voice.
   - **LLM 點評** — when you gave the user substantive feedback on a problem in this turn (a misdiagnosis, a better direction, a link to the right note), record it under the day's `**LLM 點評**：` block, after 心得. One `- <num>：...` bullet per problem, a few lines each, in your own voice. Always include the model line. Skip the block entirely for days with nothing worth saying; never pad it.
     ```markdown
     **LLM 點評**：
     model: <exact model name you are running as, e.g. Fable 5.1 or GPT-5-Codex>
     - 15：...
     ```
2. **Run the sync — every time, right after step 1:**
   ```bash
   python3 scripts/sync_lists.py
   ```
3. **Reply in one or two lines**: what was recorded, today's count, and the Master Union tally from the script output.

## What the sync does

`scripts/sync_lists.py` reads every dated block in the log and marks solved problems `[x]` + `✔ <earliest date>` in **all** `Checklists/Lists/*.md`, updating each header's `**已刷：n / total**`. Idempotent. The `✅` marker (in `Essential Problems/`) is separate and untouched.

## Don'ts

- Don't add tables, timing, stats, or review queues to the log — the user rejected that.
- Don't invoke `mock-interview` on a bare "完成 X" / problem-title list; it's a log entry, not a problem to interview on.
- Don't hand-edit checkboxes in `Checklists/Lists/` — the script owns them.
