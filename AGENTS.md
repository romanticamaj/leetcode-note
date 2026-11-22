# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Codex) working in this repository. `CLAUDE.md` imports it; this is the single source of truth. Read this file first; open the relevant project skill when its task applies.

## Repository Overview

This is a structured collection of notes, patterns, and mental models (心法) for mastering technical interviews and engineering problem-solving. It focuses on extracting reusable strategies, design principles, and testing frameworks rather than collecting solutions.

**Primarily Markdown documentation**, with standalone HTML visualizations. Notes are primarily in Traditional Chinese with English technical terms and C++ examples. There is no repository-wide build, test, or lint suite; verification depends on the changed files. See [Verification and Git](#verification-and-git).

## Working Rules

- Follow the user's requested scope, date, and level of help. Preserve their implementation and reasoning when a small correction suffices.
- Search existing notes before creating a file; extend relevant coverage and link it from the appropriate index.
- For conceptual questions, discuss the idea first. Record it only when requested or when the practice-log workflow applies.
- Distinguish independent completion, completion with hints, and unimplemented variants. Do not infer that a follow-up is complete from a general completion report.
- Ground code feedback in the supplied implementation and its invariant. Separate reasoned correctness, executed tests, and measured performance.
- Do not reveal an unrequested solution during solving or hint-only exchanges. Follow [Interview Practice Mode](#interview-practice-mode).

## Repository Structure

### Core Knowledge

- **`Algorithms/`** — Technique playbooks: Two Pointers, Sliding Window, Binary Search, DFS/BFS, DP, Greedy, Divide & Conquer, Union Find, Topological Sort, Sweep Line, Bit Manipulation, Prefix Sum, Sorting, Partition, Math, Boyer-Moore, Traversal Strategies, Design Principles
- **`Data_Structures/`** — Implementation details, trade-offs, and patterns: Trees, Graphs, Heaps, Trie, Monotonic Stacks, Binary Indexed Tree, Hash Tables, Linked Lists
- **`CPP_Reference/`** — C++ idioms, STL container behavior, type traps, common coding mistakes

### Strategy & Frameworks

- **`Interview_Playbook/`** — Pre-solve checklists, interview stage breakdown, hard-problem learning strategy, code review principles
- **`Meta_Frameworks/`** — Problem Classification Framework, Quick Decision Map, Problem Transformation, Orthogonality
- **`Proof_Techniques/`** — Exchange Argument, Loop Invariant, Structural Induction

### Checklists & Reference

- **`Checklists/`** — Practice lists, technique checklist, roadmap, practice log (see below)
- **`Cheatsheet/`** — `Gary's DSA Cheatsheet.md`, `LeetCode_Tricks_and_Keywords.md`, `CPP_One_Liners.md`
- **`Problem_History/`** — Sourced problem histories, textbook comparisons, and key design ideas; indexed in `Problem_History/README.md`
- **`README.md` / `README.zh-TW.md`** — English and Traditional Chinese reader guides; keep shared navigation and positioning aligned
- **`Reading/`** — Reference book PDFs (not tracked as notes)
- **`Visualizations/`** — 圖解與互動 HTML 動畫統一放在這裡。LeetCode 圖解以 `<編號>-<英文題名，空格改為底線>.html` 命名，例如 `142-Linked_List_Cycle_II.html`；保持單檔可直接用瀏覽器開啟。

### Key Files

- **`Checklists/Algorithm_Techniques_Checklist.md`** — Technique master table with difficulty ratings and complexity
- **`Checklists/Learning_Roadmap.md`** — Follow-up TODO list generated while solving problems
- **`Cheatsheet/LeetCode_Tricks_and_Keywords.md`** — Problem-specific tricks and keyword→pattern mapping

## Practice Tracking System

### `Checklists/Lists/` — Unified problem lists

Files are numbered by role: `00` master union, `01–04` source lists, `05–07` personal selections, `08` follow-ups, and `09` review. These numbers organize the files; the Master Union tiers determine practice priority.

**Master union and source lists (`00–04`)**

Source-list entries carry LeetCode number, title, difficulty, and link. Premium problems are marked 🔒. Problems already covered by `05_Essential_Problems.md` are marked ✅. Completion checkboxes are determined only by `Practice_Log.md`.

- **`00_Master_Union.md`** — Deduplicated union of the four lists below (250 problems), sorted into four tiers by how many lists contain each problem (🔥🔥🔥🔥 = all four, 37 problems). **This tier ordering is the recommended grind priority.**
- `01_NeetCode_150.md`, `02_Grind_75.md`, `03_Top_Interview_150.md`, `04_Top_100_Liked.md` — the individual source lists

These were generated from authoritative sources (official LeetCode study plan pages, `krmanik/Anki-NeetCode` JSON) with numbers resolved via the LeetCode `/api/problems/all/` endpoint. **Do not edit problem numbers by hand or regenerate them from memory** — re-fetch from source if they need updating.

**Personal selections, follow-ups, and review (`05–09`)**

- `05_Essential_Problems.md` — curated must-do problems by technique
- `06_Archetype_Problems.md` — prototype problem per algorithm family
- `07_Technique_Integration_Problems.md` — problems requiring multiple techniques
- `08_Followup_Problems.md` — variations and follow-up questions
- `09_Problem_Review.md` — problems flagged for review

### `Checklists/Practice_Log.md` — Daily practice diary

**Deliberately minimal.** Format is one block per day, **newest block first**:

```markdown
## YYYY-MM-DD

- 104. Maximum Depth of Binary Tree
- 121. Best Time to Buy and Sell Stock

**心得**：
- 104：one-line reflection
- 121：one-line reflection

**LLM 點評**：
model: <exact current model name>
- 121：the LLM's feedback on the problem, only when it said something substantive
```

**Do not add tables, statistics, time tracking, spaced-repetition queues, or scripts** — the user explicitly rejected that complexity.

### Daily practice workflow

**Governed by the project skill `practice-log`** (`.agents/skills/practice-log/SKILL.md`). Invoke it whenever the user reports a finished problem, gives a 心得, or asks to sync lists.

The non-negotiable rule: **every edit to `Practice_Log.md` is immediately followed by `python3 scripts/sync_lists.py`.** The script marks solved problems `[x]` + `✔ date` in the master union and four source lists (`Checklists/Lists/00–04`) and refreshes each `**已刷：n / total**` header. Repeated practice keeps the earliest completion date in these generated lists. Never hand-edit those checkboxes; the `✅` marker (from `05_Essential_Problems.md`) is separate and left alone.

Additional tracking rules:

- Use the explicitly requested date; otherwise check `date +%F`. Move the entire entry, reflection, and feedback when correcting a date, then immediately sync.
- For another version of the same problem on the same day, extend its existing entry rather than listing the problem twice. Preserve earlier useful feedback and update stale statements such as “not yet implemented.”
- Record an English technique summary matching the completed implementation. Without code, do not invent a diagnosis or claim verification.
- In `09_Problem_Review.md`, use ⭐–⭐⭐⭐⭐⭐ for personal review priority, not problem difficulty. The previous-practice date is the latest logged practice; the redo date stays blank until that exact target is completed. Keep variants separate.
- A review-only edit does not require a practice-log edit or synchronization. Do not manufacture a completion entry for a future exercise.
- For a conceptual question about a solved problem, use an existing technique note when recording requested takeaways. Dedicated history requests belong in [Problem History](#problem-history).

For process coaching on a Hard problem (stuck, "要不要看提示", whether to learn a technique first, planning the rewrite/review), use the project skill **`hard-coach`** (`.agents/skills/hard-coach/SKILL.md`).

## Interview Practice Mode

**IMPORTANT**: When the user pastes a LeetCode problem (identifiable by problem number, difficulty rating, or LeetCode problem format), **automatically invoke the `mock-interview` skill** to conduct a mock Google L5 technical interview using that problem.

**Do NOT** solve the problem, give solutions or unrequested hints, or analyze it yourself.

**Exception**: A bare list of problem titles or numbers given in the context of logging practice (e.g. right after discussing `Practice_Log.md`) is a log entry, not a problem to interview on. Record it and move on.

## Skills

Project skills live in **`.agents/skills/`** (the Agent Skills location Codex reads). Each `.claude/skills/<name>` is a symlink to `../../.agents/skills/<name>`, so Claude Code loads the same file — **edit only `.agents/skills/`**. To add a skill, create it there, then `ln -s ../../.agents/skills/<name> .claude/skills/<name>`.

| Skill | Purpose |
|---|---|
| `practice-log` | Record a finished problem / 心得 in `Practice_Log.md`, then run `sync_lists.py`. |
| `mock-interview` | Google L5 mock interview in Traditional Chinese. Minimal hints only on request; never reveals solutions. |
| `hard-coach` | Process coaching for Hard problems: keep trying vs. hints, learn technique first, rewrite/review plan. |
| `extract-pattern` | Turn a solution (playbook mode) or several related problems (心法 mode) into a note, extending an existing note first. |

## Notes and Technique Summaries

Organize notes by technique rather than by problem number, except for dedicated problem histories and visualizations. Explain the core state, invariant or correctness argument, complexity, implementation pitfalls, and useful examples. Use ⭐–⭐⭐⭐⭐⭐ for technique difficulty where applicable.

### Technique Summary Convention

When recording a completed problem, reviewing a supplied solution, summarizing reflections, or adding a problem-list description, include a one-line **English technique summary**. Keep explanations separate and in Traditional Chinese. Do not repeat the summary in short replies that add no technical content.

- **Format**: Use nouns or noun phrases joined by ` + `, not full sentences or procedural steps.
- **Content**: Identify the main algorithm and key state/data structure, then include pruning, acceleration, or reconstruction when it distinguishes the approach. Do not force a fixed number of components.
- **Accuracy**: Match the actual implementation. Do not call array counting a hashmap or map-based cycle detection Floyd's algorithm. Keep unimplemented follow-ups separate from completed approaches.
- **Terminology**: Prefer established terms. Define descriptive labels such as Signed Contribution Counting in the note rather than presenting them as universal terminology.
- **Examples**: `Sorting + Two Pointers`, `BFS + Distance-Constrained Predecessor DAG + Backtracking`, `Simulation + Cycle Detection + Fast Forwarding`, `Signed Contribution Counting`.
- **Interview Practice Mode**: This convention does not override its restrictions. During solving or hint-only exchanges, do not reveal techniques or solutions the user has not derived.

## Document Style Conventions for 心法/Playbook Files

### File Naming Convention

**The `00-` slot is reserved for the standard template.** Every technique folder should have exactly one canonical "memorize this" file, named:

```text
<technique folder>/00-<Technique_Name>_Standard_Template.md
```

Example: `Algorithms/Sliding_Window/00-Sliding_Window_Standard_Template.md`

This makes the canonical template of any technique findable at a glance (it always sorts first) and greppable across the repo with `find . -name '00-*_Standard_Template.md'`.

A Standard Template file should contain:
- The one template to memorize, as a C++ code block
- A step-by-step 口訣 (mnemonic) table
- The loop invariant / correctness argument
- ⚠️ Rejected alternatives and why (keep as cautionary notes, do **not** give them their own template)
- Interview 話術 for stating the approach

**Other files:**
- Numbering continues from `01-` for the remaining sequential notes (e.g., `01-Core_Concepts.md`, `02-Advanced_Techniques.md`)
- Standalone notes with no natural reading order need no prefix (e.g., `DFS_Tree_vs_Graph.md`)
- Use descriptive, content-focused names — not necessarily ending with "Playbook" or "心法"
- Place in the appropriate algorithm/technique folder

When a technique has one clearly superior approach, **prune the alternatives rather than documenting both as equals.** The goal is one template per technique, internalized as muscle memory.

### Document Structure Template

1. **Title (H1)**: `# [Topic Name] ([English]) Playbook` or `# [Topic Name] 解題心法`
2. **Introduction**: Brief description of the technique and its importance
3. **TL;DR Section** (optional): Quick reference with key formulas/operations
4. **Core Concepts (核心概念)**: Fundamental principles
5. **Main Content Sections**: Use H2 (##) for major sections
   - Number sections when presenting sequential steps or stages
   - Use emoji icons (🧠 🧩 ⚠️ ⏱️ ✅) to highlight key sections
6. **Code Blocks**:
   - Focus on algorithms, pseudo code, or core concept flow
   - Use C++ as primary language for implementation
   - Include comments explaining logic (Chinese or English)
   - Provide template code when applicable
7. **Common Pitfalls (常見陷阱)**: Warning section with ⚠️
8. **Complexity Analysis**: Time and space complexity table when relevant
9. **Checklist**: Use checkbox format for review items

### Writing Style

- Mix Chinese and English technical terms naturally
- Use **bold** for important concepts and keywords
- Use `code format` for inline code, operators, and variable names
- Include practical examples with step-by-step walkthroughs
- Add "口訣" (mnemonics) for memorization when helpful
- Label every code fence with its language (`cpp`, `python`, `text`, etc.); keep examples focused on core flow and comment on the key logic.
- Use 🧠 for core thinking, 🧩 for frameworks, ⚠️ for pitfalls, ⏱️ for complexity, and ✅ for review checklists where helpful.

## Problem History

- Follow `Problem_History/README.md`; name files `LC_<four-digit-number>_<English_Title>.md` and add the index entry in numeric order.
- Start with a memory cue and the key design concept. Keep implementation excerpts to the few lines needed to explain the idea when the user asks for a concise history.
- Prefer original publications, author code, official textbooks, and primary documentation. Preserve direct links, author/title/year, sections or pages when verified, and the verification date.
- Distinguish a documented precedent, a related concept, and proven direct adaptation. A textbook example is not evidence that LeetCode copied it; leave origins and first-publication dates unknown when unverified.
- State access limitations and identify secondary attribution. Do not turn a search snippet, page timestamp, or uninspected scan into a verified historical claim.

## Verification and Git

- After Markdown edits, run `git diff --check` and check relevant local links, anchors, and code fences. For README changes, check both language guides and navigation.
- After every practice-log edit, run `python3 scripts/sync_lists.py` immediately; inspect its output for the completion totals used in the reply. Never hand-edit generated completion markers.
- If compiling or running a supplied snippet, use its required C++ standard and meaningful boundary cases. Do not claim execution from reasoning alone; explain any untested scope.
- Before committing, inspect `git status` and the diff, preserve unrelated work, and stage deliberately. When asked to commit everything, include all reviewed pending changes and group coherent subjects into commits.
- Push only when requested. Use a normal push, then verify local/remote parity and report the resulting commit IDs and remaining worktree changes.
- This notes repository does not need a new build system, release version, changelog, or test suite for routine documentation edits.

## Tool-Specific Notes

- `CLAUDE.md` contains only the `@AGENTS.md` import and a short pointer; shared instructions belong here.
- Edit shared project skills only under `.agents/skills/`; preserve the Claude skill symlinks.
- In a practice-log **LLM 點評** block, use the exact model name actually running, not an example name or a model mentioned in the user's reflection.
