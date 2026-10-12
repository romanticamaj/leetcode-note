---
name: practice-log
description: >-
  Use when the user reports finishing a LeetCode problem, gives a 心得/reflection about one, or mentions a practice date — e.g. "完成 226", "今天新增一題: 141. Linked List Cycle", "心得：...". Also use when the user asks to sync or update Checklists/Lists.
---

# Practice Log

Record what the user solved, then **always** sync the lists. The sync is not optional and not "on request" — a log edit without a sync is the bug this skill exists to prevent.

## Feedback on reflections

When the user provides a technical reflection, proactively respond to its substance before treating the task as complete. Explain what their observation gets right, correct any supported misconception, and answer questions embedded in the reflection. Ground feedback in their code and stated experience; without code, do not invent a specific implementation diagnosis. Link an existing technique note when it helps.

Give this feedback in the user-facing reply and record its key points under **LLM 點評**. Writing feedback only into the file does not replace discussing it with the user. A bare completion report, sync request, or small follow-up such as "這題要重做，記錄在 log" needs only a brief confirmation unless it introduces a new technical point; do not pad it with praise or repeat earlier feedback.

## Steps

1. **Edit `Checklists/Practice_Log.md`**
   - Find the `## YYYY-MM-DD` block for the stated date (default: today — check with `date +%F`). If missing, create it **at the top** (newest first), with an empty `**心得**：` line.
   - Add `- <num>. <title>` under the date. Keep the user's numbering; look up the title if only a number is given.
   - For a 心得: put it under that day's `**心得**：`. If the day has >1 problem, use `- <num>：...` bullets. Fix typos only; keep the user's voice.
   - **LLM 點評** — record the substantive feedback prepared for the user's reflection under the day's `**LLM 點評**：` block, after 心得. One `- <num>：...` bullet per problem, a few lines each, in your own voice. Always include the model line. Preserve earlier useful feedback when adding new points or correcting a diagnosis. Skip the block entirely when there is no substantive feedback; never pad it.
     ```markdown
     **LLM 點評**：
     model: <exact model name you are running as, e.g. Fable 5.1 or GPT-5-Codex>
     - 15：...
     ```
2. **Run the sync — every time, right after step 1:**
   ```bash
   python3 scripts/sync_lists.py
   ```
3. **Reply with the substantive feedback**, including answers to questions in the reflection, followed by a brief recording confirmation with today's count and the Master Union tally from the script output. For a request with no new technical reflection, the confirmation alone can be one or two lines.

## What the sync does

`scripts/sync_lists.py` reads every dated block in the log and marks solved problems `[x]` + `✔ <earliest date>` in the master union and four source lists (`00–04`) under `Checklists/Lists/`, updating each header's `**已刷：n / total**`. Idempotent. Personal selections (`05–07`), follow-ups (`08`), and review notes (`09`) keep their own format and are not rewritten. The `✅` marker means a problem was previously included in `05_Essential_Problems.md`; it is separate and untouched.

## Don'ts

- Don't add tables, timing, stats, or review queues to the log — the user rejected that.
- Don't invoke `mock-interview` on a bare "完成 X" / problem-title list; it's a log entry, not a problem to interview on.
- Don't hand-edit completion checkboxes in the master union and four source lists — the script owns them.
