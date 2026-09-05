# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a structured collection of notes, patterns, and mental models (心法) for mastering technical interviews and engineering problem-solving. It focuses on extracting reusable strategies, design principles, and testing frameworks rather than collecting solutions.

**Markdown documentation only** — there are no build, test, or lint commands. ~300 notes, written primarily in Traditional Chinese with English technical terms.

## Repository Structure

### Core Knowledge

- **`Algorithms/`** (152) — Technique playbooks across 20 categories: Two Pointers, Sliding Window, Binary Search, DFS/BFS, DP, Greedy, Divide & Conquer, Union Find, Topological Sort, Sweep Line, Bit Manipulation, Prefix Sum, Sorting, Partition, Math, Boyer-Moore, Traversal Strategies, Design Principles
- **`Data_Structures/`** (63) — Implementation details, trade-offs, and patterns: Trees, Graphs, Heaps, Trie, Monotonic Stacks, Binary Indexed Tree, Hash Tables, Linked Lists
- **`CPP_Reference/`** (30) — C++ idioms, STL container behavior, type traps, common coding mistakes

### Strategy & Frameworks

- **`Interview_Playbook/`** (7) — Pre-solve checklists, interview stage breakdown, hard-problem learning strategy, code review principles
- **`Meta_Frameworks/`** (7) — Problem Classification Framework, Quick Decision Map, Problem Transformation, Orthogonality
- **`Test_Case_Construction/`** (7) — Test case design frameworks with tree/graph-specific strategies
- **`Proof_Techniques/`** (3) — Exchange Argument, Loop Invariant, Structural Induction

### Checklists & Reference

- **`Checklists/`** — Practice lists, technique checklist, roadmap, practice log (see below)
- **`Cheatsheet/`** — `Gary's DSA Cheatsheet.md`, `LeetCode_Tricks_and_Keywords.md`, `CPP_One_Liners.md`
- **`Reading/`** — Reference book PDFs (not tracked as notes)

### Key Files

- **`Checklists/Algorithm_Techniques_Checklist.md`** — Technique master table with difficulty ratings and complexity
- **`Checklists/Learning_Roadmap.md`** — Follow-up TODO list generated while solving problems
- **`Cheatsheet/LeetCode_Tricks_and_Keywords.md`** — Problem-specific tricks and keyword→pattern mapping

## Practice Tracking System

### `Checklists/Lists/` — Curated problem lists

All entries carry LeetCode number, title, difficulty, and link. Premium problems are marked 🔒. Problems already covered by `Essential Problems/` are marked ✅ with a pre-checked box.

- **`00_Master_Union.md`** — Deduplicated union of the four lists below (250 problems), sorted into four tiers by how many lists contain each problem (🔥🔥🔥🔥 = all four, 37 problems). **This tier ordering is the recommended grind priority.**
- `01_Grind75_Easy_Warmup.md` — 24 Easy problems from Grind 75 weeks 1–2, plus a technique coverage table
- `NeetCode_150.md`, `Grind_75.md`, `Top_Interview_150.md`, `Top_100_Liked.md` — the individual source lists

These were generated from authoritative sources (official LeetCode study plan pages, `krmanik/Anki-NeetCode` JSON) with numbers resolved via the LeetCode `/api/problems/all/` endpoint. **Do not edit problem numbers by hand or regenerate them from memory** — re-fetch from source if they need updating.

### `Checklists/Essential Problems/` — Gary's personal collection

- `Essential_Problems.md` — curated must-do problems by technique
- `Archetype_Problems.md` — prototype problem per algorithm family
- `Technique_Integration_Problems.md` — problems requiring multiple techniques
- `Problem_Review.md` — problems flagged for review

### `Checklists/Practice_Log.md` — Daily practice diary

**Deliberately minimal.** Format is one block per day, **newest block first**:

```markdown
## YYYY-MM-DD

- 104. Maximum Depth of Binary Tree
- 121. Best Time to Buy and Sell Stock

**心得**：
- 104：one-line reflection
- 121：one-line reflection
```

**Do not add tables, statistics, time tracking, spaced-repetition queues, or scripts** — the user explicitly rejected that complexity.

### Daily practice workflow

**Governed by the project skill `practice-log`** (`.claude/skills/practice-log/SKILL.md`). Invoke it whenever the user reports a finished problem, gives a 心得, or asks to sync lists.

The non-negotiable rule: **every edit to `Practice_Log.md` is immediately followed by `python3 scripts/sync_lists.py`.** The script marks solved problems `[x]` + `✔ date` across all `Checklists/Lists/*.md` and refreshes each `**已刷：n / total**` header. Never hand-edit those checkboxes; the `✅` marker (from `Essential Problems/`) is separate and left alone.

For a conceptual question about a problem just solved: answer it, and if the user wants it recorded, append a few key lines with links to the **existing** technique note rather than creating a new file.

## Interview Practice Mode

**IMPORTANT**: When the user pastes a LeetCode problem (identifiable by problem number, difficulty rating, or LeetCode problem format), **automatically invoke the `google-interviewer` subagent** to conduct a mock Google L5 technical interview using that problem.

**Do NOT**:
- Solve the problem directly
- Provide solutions or hints
- Analyze the problem yourself

**Always use the google-interviewer agent for interactive interview practice** when a LeetCode problem is detected.

**Exception**: A bare list of problem titles or numbers given in the context of logging practice (e.g. right after discussing `Practice_Log.md`) is a log entry, not a problem to interview on. Record it and move on.

## Subagents

`.claude/agents/` defines three agents:

| Agent | Purpose |
|---|---|
| `google-interviewer` | Simulates a Google L5 interview in Traditional Chinese. Gives minimal hints only on request; never reveals solutions before submission. |
| `playbook-extractor` | Extracts and formalizes a pattern from a solution into a structured playbook document following repo conventions. |
| `pattern-trick-extractor` | Extracts shared 心法 across several related solutions into a concise playbook, light on implementation detail. |

## Architecture & Design Patterns

### Problem-Solving Philosophy

1. **Pattern Extraction**: Each problem solution should identify the underlying reusable pattern
2. **Systematic Thinking**: Apply structured frameworks for complex tasks
3. **Best Practices Documentation**: Capture language-specific idioms, common pitfalls, and performance considerations

### Note Organization Principles

- Problems are organized by technique/pattern rather than by problem number
- Each technique includes:
  - Difficulty level (⭐ to ⭐⭐⭐⭐⭐)
  - Time and space complexity
  - Core thinking pattern
  - Common problem examples
  - Implementation tips

### Common Patterns Referenced

- **Two Pointers**: Fast/Slow, K-Gap, Adjacent, Expand Around Center
- **Sliding Window**: Variable and fixed-size windows
- **Monotonic Stack/Queue**: For "next greater/smaller" problems
- **Graph Traversal**: BFS for shortest path, DFS for connectivity
- **Dynamic Programming**: 1D, 2D, and state compression variants
- **Binary Search**: On sorted arrays and answer spaces
- **Transformation Patterns**: Destination-as-Source Reachability, Movement Constraint Transformation, Constraints into Tools

## Document Style Conventions for 心法/Playbook Files

### File Naming Convention

**The `00-` slot is reserved for the standard template.** Every technique folder should have exactly one canonical "memorize this" file, named:

```
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

### Section Markers

- 🧠 for philosophy/core thinking
- 🧩 for problem-solving framework
- ⚠️ for warnings and pitfalls
- ⏱️ for complexity analysis
- ✅ for checklists or key takeaways

### Code Block Conventions

- Always specify language (```cpp, ```python, etc.)
- Focus on algorithm implementation or pseudo code
- Add inline comments explaining key logic and concepts
- Emphasize core algorithmic flow over specific examples
