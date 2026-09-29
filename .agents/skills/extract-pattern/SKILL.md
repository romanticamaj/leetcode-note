---
name: extract-pattern
description: Use when the user wants to turn a solution or a set of related problems into a reusable note — "幫我 extract pattern", "整理成心法", "formalize this pattern", "寫成 playbook", "I solved LC 327, 315, 493, make a playbook". Extracts the reusable 心法 / template and writes it following the repo's note conventions, extending an existing note when one fits.
---

# Extract Pattern

Turn concrete solutions into a reusable pattern note. Extract the **why** and the one template to memorize — not a problem-specific solution.

Follow the conventions in `AGENTS.md` (Document Style Conventions, File Naming, `00-` Standard Template). This skill only adds the extraction workflow.

## Step 1 — Gather

Use what's already in the conversation (problem, the user's code, 心得, earlier discussion). Ask only for what's missing: the solution code and the insight the user found.

Pick the mode:

| Mode | Input | Output |
|---|---|---|
| **Playbook** | One solution (+ takeaways) | Pattern + C++ template, 80–150 lines |
| **心法** | Several related problems | Mental model + learning path, 80–120 lines, light on code |

In 心法 mode, ask once: 「需要加程式碼模板嗎？(1) 要 — pseudocode / C++ template (2) 不要 — 純文字流程」 and wait.

## Step 2 — Find the home first

Before creating anything, search the technique folder:

```bash
ls Algorithms/<Technique>/ Data_Structures/<Structure>/
grep -rl "<keyword>" Algorithms Data_Structures Meta_Frameworks
```

- **Existing note covers it** → append a section there (a few key lines + link). This is the default.
- **It's the canonical template of a technique with no `00-` file** → create `00-<Technique>_Standard_Template.md` (template, 口訣 table, invariant, ⚠️ rejected alternatives, 話術).
- **Genuinely new pattern** → new file in that folder, next number prefix (e.g. `09_...md`), descriptive name.

State the chosen path and why in one line before writing.

## Step 3 — Extract

- **Core insight**: one sentence — what property makes it work, vs. brute force
- **2–4 core concepts**: what's exploited, what ordering/timing is critical
- **One template**: abstract C++ (or phase flow in 心法 mode without code). **One template per technique** — alternatives go in ⚠️ as rejected, with why; never "Variant 1 / Variant 2" as equals
- **Learning path** (心法 mode): 3+ problems, ordered, each with what it adds. Reference by number + title only (`LC 857. Minimum Cost to Hire K Workers`), no full implementations
- **⚠️ Pitfalls**: only the ones actually hit or likely in interviews

## Step 4 — Write

Structure:

```markdown
# [Pattern Name] ([English]) 心法

## 🧠 核心哲學        ← insight + vs brute force; 1–2 paragraphs
## 核心概念            ← 1️⃣ 2️⃣ 3️⃣, bullets + small ASCII visual
## 🧩 核心設計模式     ← the one template / phase flow + 設計要點
## ⚠️ 常見陷阱          ← optional, short
## 📚 LeetCode 學習路徑 ← 心法 mode; problems + 關鍵心法
## ⏱️ 複雜度            ← one line or small table
```

Style: 繁體中文 narrative, English technical terms; **bold** key concepts; `code` for identifiers; every code block has a language tag. Gold-standard example: `Algorithms/Divide_and_Conquer/07_Merge_Sort_Variants_Pattern.md`.

## Step 5 — Self-review, then compress

- Merge overlapping sections (核心哲學 vs 核心概念 often repeat)
- Cut hypothetical or "impressive but rare" variants
- Prefer tables and bullets over prose
- Hard limit: **150 lines**. If over, cut until under

Reply in a few lines: file path (new or appended), line count, what was compressed.
