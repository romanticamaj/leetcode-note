<div align="center">

# DSA Pattern Playbook

**Learn to derive algorithms, recognize patterns, and explain why they work.**

A framework-first guide to data structures and algorithms.<br>
Reusable mental models · C++ templates · Curated practice · Correctness reasoning

**English** · [繁體中文](README.zh-TW.md)

[Start Learning](#start-learning) · [Core Frameworks](#core-frameworks) · [Pattern Library](#pattern-library) · [Practice Lists](#practice-with-purpose) · [Beyond the Algorithm](#beyond-the-algorithm)

</div>

---

What information should an algorithm keep? Which work can it avoid? Why is it safe to discard a candidate?

**DSA Pattern Playbook connects these questions to concrete patterns and practice problems.** Built from Gary Hsieh’s ongoing study notes, it organizes learning around reusable reasoning: define the answer, establish a correct baseline, identify wasted work, and derive an improvement you can justify.

> **Language:** Both READMEs provide a complete learning guide. The underlying notes are primarily in **Traditional Chinese**, with English technical terms and **C++** implementations. English translations of the full library are not yet available.

## Start learning

You’ll get the most from this collection if you can already write basic programs and understand arrays, loops, functions, and recursion. Choose an entry point:

| Your starting point | Start here | What to do next |
|---|---|---|
| Learning DSA patterns | [Two Pointers](Algorithms/Two_Pointers/01-Two_Pointers_Core_Patterns_and_Templates.md) + [Grind 75](Checklists/Lists/02_Grind_75.md) | Work at your own pace; use each problem to understand a pattern before timing yourself. |
| Can code, but struggle to find an approach | [Problem-solving workflow](Interview_Playbook/Problem_Solving_Process_and_Assumption_Checklist.md) + [optimization strategy](Interview_Playbook/Problem_Solving_Strategies.md) | Describe a correct brute force, then identify the work to eliminate. |
| Know individual algorithms, want the connections | [State → Transition → Traversal](Meta_Frameworks/Problem_Classification_Framework/03-State_Transition_Traversal.md) | Compare familiar techniques in the [Algorithm Atlas](Meta_Frameworks/State_Transition_Algorithm_Atlas.md). |
| Preparing for coding interviews | [Pre-solve checklist](Interview_Playbook/Pre_Solve_Interview_Checklist.md) + [Master Union](Checklists/Lists/00_Master_Union.md) | Start with the problems shared by all four lists, then practice [follow-ups](Checklists/Lists/08_Followup_Problems.md). |

**A first session:** Read the [Binary Search template](Algorithms/Binary_Search/00-Binary_Search_Standard_Template.md), find a matching problem in the [practice lists](Checklists/Lists/), and explain the monotone predicate, interval invariant, and termination condition before coding.

## The learning loop

```text
Define the answer → Build a correct baseline → Identify wasted work
        ↑                                             ↓
Transfer to a related problem ← Prove and test ← Derive a pattern
```

For each problem, leave yourself four things you can reconstruct later:

1. **Answer definition:** A condition or formula precise enough to check.
2. **Baseline and cost:** What you enumerate, how you evaluate it, and where the time goes.
3. **Pattern and preconditions:** What work the technique saves, and which property makes that valid.
4. **Correctness and transfer:** An invariant or proof, boundary tests, and what changes in a follow-up.

## Core frameworks

These are the conceptual backbone of the repository. Read them alongside practice rather than trying to finish every note first.

| Framework | The question it helps answer |
|---|---|
| [Define the answer before coding](Interview_Playbook/Problem_Solving_Process_and_Assumption_Checklist.md) | Can I turn the statement into an explicit, testable `ANSWER`? |
| [Brute Force → BUD ↔ BCR](Interview_Playbook/Problem_Solving_Strategies.md) | Where are the bottlenecks, unnecessary work, and duplicated work? What runtime target can I justify? |
| [Problem Transformation](Meta_Frameworks/Problem_Transformation.md) | How do I translate a story into entities, relationships, constraints, and a computational model? |
| [Quick Decision Map](Meta_Frameworks/Problem_Classification_Framework/02-Quick_Decision_Map.md) | How do output goals, input structure, constraints, and input size narrow my options? |
| [State → Transition → Traversal](Meta_Frameworks/Problem_Classification_Framework/03-State_Transition_Traversal.md) | What must I remember, how can it change, and what must be processed first? |
| [Orthogonality](Meta_Frameworks/Orthogonality-Problem-Solving.md) | Which design decisions can I reason about separately before checking how they fit together? |
| [Loop Invariants](Proof_Techniques/Loop_Invariant.md) · [Structural Induction](Proof_Techniques/Structural_Induction.md) · [Exchange Arguments](Proof_Techniques/Exchange_Argument.md) | How do I justify an iteration, a recursive composition, or a greedy choice? |

### One map for the bigger picture

The **[State–Transition Algorithm Atlas](Meta_Frameworks/State_Transition_Algorithm_Atlas.md)** describes algorithms and data structures through shared questions: **goal, state, transition, computation order, correctness, termination, and cost**.

Its September 2026 snapshot contains **212 entries across 11 categories**, with source-note mappings. Entries include variants and combined patterns; they are not 212 distinct algorithms.

[Read the Markdown atlas](Meta_Frameworks/State_Transition_Algorithm_Atlas.md) · [Downloadable HTML reader](Meta_Frameworks/State_Transition_Algorithm_Atlas.html)

The HTML reader supports search, category filters, and expandable entries. Download it and open it locally in a browser.

## Pattern library

Each entry below gives you a concrete starting point and a deeper modeling question.

| Topic | Start with | Then explore |
|---|---|---|
| Two Pointers | [Core patterns and templates](Algorithms/Two_Pointers/01-Two_Pointers_Core_Patterns_and_Templates.md) | [Fast and slow pointers](Algorithms/Two_Pointers/02_Fast_and_Slow_Pointers.md) |
| Sliding Window | [Expand → repair → evaluate](Algorithms/Sliding_Window/00-Sliding_Window_Standard_Template.md) | [Constraint tracking](Algorithms/Sliding_Window/01-Constraint_Tracking_and_Optimization.md) |
| Binary Search | [Find the first true predicate](Algorithms/Binary_Search/00-Binary_Search_Standard_Template.md) | [Search the solution space](Algorithms/Binary_Search/04-Binary_Search_on_Solution_Space.md) |
| Prefix Sum | [Core concepts](Algorithms/Prefix_Sum/01_Prefix_Sum_Intro.md) | [Running-state patterns](Algorithms/Prefix_Sum/02_Running_State_Pattern.md) |
| Recursion & Trees | [Recursion design principles](Algorithms/Design_Principles/Recursion/01-Recursion_Design_Principles.md) | [State design across recursive paradigms](Algorithms/Design_Principles/Recursion/State_Design_Across_Recursive_Paradigms.md) |
| Backtracking | [Templates and patterns](Algorithms/Backtracking/01-Backtracking_Templates_and_Patterns.md) | [Decided vs. undecided candidates](Algorithms/Backtracking/03-Backtracking_Candidate_Modeling.md) |
| Dynamic Programming | [From exhaustive search to DP](Algorithms/Dynamic_Programming/Fundamentals/02-Problem_Solving_Framework.md) | [State design](Algorithms/Dynamic_Programming/State_Design/01-Essentials.md) |
| Graph Search | [Graph problem-solving principles](Data_Structures/Graphs/Graph_Problem_Solving_Principles.md) | [Constructing implicit graph nodes](Data_Structures/Graphs/Implicit_Graph_Node_Construction.md) |
| Greedy & Heaps | [Recognizing greedy approaches](Algorithms/Greedy/Greedy_Identification_and_Application.md) | [Heap decision-making](Data_Structures/Heaps/01-Heap_Decision_Making.md) |
| Monotonic Stack & Queue | [Core concepts](Data_Structures/Stacks_and_Queues/Monotonic_Stacks/01-Monotonic_Stack_and_Queue.md) | [Search-space conversion](Data_Structures/Stacks_and_Queues/Monotonic_Stacks/02-Search_Space_Conversion.md) |
| Connectivity & Dependencies | [Union Find](Algorithms/Union_Find/01-Core_Concepts.md) | [Topological Sort](Algorithms/Topological_Sort/01-Core_Concepts_and_Applications.md) |

Browse all [algorithms](Algorithms/), [data structures](Data_Structures/), or the [technique checklist](Checklists/Algorithm_Techniques_Checklist.md).

**Template convention:** Files named `00-<Technique>_Standard_Template.md` identify a canonical template, with a mnemonic, invariant, pitfalls, and interview explanation. Start with the Binary Search and Sliding Window templates linked above.

## Practice with purpose

Use a list to choose problems, then return to the pattern library to explain what you learned.

| Collection | Learning purpose |
|---|---|
| [Master Union — 250 problems](Checklists/Lists/00_Master_Union.md) | A deduplicated snapshot of four lists, grouped by overlap. The 37 problems in all four are a compact starting set; overlap is a prioritization heuristic. |
| [NeetCode 150](Checklists/Lists/01_NeetCode_150.md) | Practice by pattern category. |
| [Grind 75](Checklists/Lists/02_Grind_75.md) | Follow a week-based practice sequence. |
| [Top Interview 150](Checklists/Lists/03_Top_Interview_150.md) · [Top 100 Liked](Checklists/Lists/04_Top_100_Liked.md) | Broaden coverage with the collected LeetCode study-plan lists. |
| [Essential Problems](Checklists/Lists/05_Essential_Problems.md) | Explore the maintainer’s curated selection by technique. |
| [Technique Integration](Checklists/Lists/07_Technique_Integration_Problems.md) | Practice combining techniques and comparing approaches. |
| [Follow-up Problems](Checklists/Lists/08_Followup_Problems.md) | Change a constraint, handle a variant, or explain a trade-off. Frequency labels are editorial judgments. |
| [Focused practice playbooks](Checklists/Trick%20Practice/) | Deepen a specific technique: answer-space binary search, Kadane, knapsack, KMP, and more. |

> List checkboxes, completion dates, and progress totals reflect **the maintainer’s practice**, not prerequisites for readers. `✅` means a problem also appears in the personal collection; `🔒` marks Premium problems. Use your own copy to track your progress.

**When a Hard problem stalls:** Use the [Hard-problem learning strategy](Interview_Playbook/Hard_Problem_Learning_Strategy.md) and [technique reference](Interview_Playbook/Hard_Techniques_Reference.md) to distinguish a missing insight from an unfamiliar technique, then return to simpler prerequisites when needed.

## Beyond the algorithm

A selection of notes that connect implementation, modeling, mathematics, and history:

| Read this | Take away this idea |
|---|---|
| [Correct by Construction](Algorithms/Design_Principles/Correct_by_Construction.md) | Encode correctness in names, types, and structure so it survives forgetting a detail. |
| [Destination as Source](Algorithms/Design_Principles/Transformation_Patterns/Destination_as_Source_Reachability.md) | Reverse reachability to share work across many starting points. |
| [Multi-source BFS](Algorithms/BFS/MultiSource_BFS_Thinking_Framework.md) | Let all sources expand together instead of repeating nearest-source searches. |
| [Canonical Anchor Decomposition](Algorithms/Divide_and_Conquer/08_Canonical_Anchor_Decomposition.md) | Use a structurally determined anchor to reason about unique decomposition. |
| [Bidirectional Constraint Decomposition](Algorithms/Design_Principles/Bidirectional_Constraint_Decomposition.md) | Solve directional constraints separately, then combine them. |
| [Gas Station: history and the prefix-sum minimum](Problem_History/LC_0134_Gas_Station.md) | Connect a coding problem to a mathematical puzzle and its documented sources. |
| [Linked List Cycle II — interactive walkthrough](Visualizations/142-Linked_List_Cycle_II.html) | Follow fast and slow pointers visually; download the HTML and open it locally. |

Explore the [problem-history collection](Problem_History/README.md), [C++ reference](CPP_Reference/), [pattern and keyword cheatsheet](Cheatsheet/LeetCode_Tricks_and_Keywords.md), and [C++ one-liners](Cheatsheet/CPP_One_Liners.md).

## Repository map

| Directory | What you’ll find |
|---|---|
| [`Meta_Frameworks/`](Meta_Frameworks/) | Modeling, classification, and connections between techniques |
| [`Algorithms/`](Algorithms/) · [`Data_Structures/`](Data_Structures/) | Pattern notes, implementations, and trade-offs |
| [`Proof_Techniques/`](Proof_Techniques/) | Tools for correctness reasoning |
| [`Checklists/`](Checklists/) | Practice collections and technique coverage |
| [`Interview_Playbook/`](Interview_Playbook/) | Communication, testing, review, and learning strategies |
| [`CPP_Reference/`](CPP_Reference/) · [`Cheatsheet/`](Cheatsheet/) | Language details and quick reference |
| [`Problem_History/`](Problem_History/README.md) · [`Visualizations/`](Visualizations/) | Historical context and standalone visual explainers |

<details>
<summary><strong>Maintainer’s learning journal and AI-assisted workflows</strong></summary>

The [practice log](Checklists/Practice_Log.md), [learning roadmap](Checklists/Learning_Roadmap.md), and [review list](Checklists/Lists/09_Problem_Review.md) remain part of this repository. They document how the collection evolves through actual practice.

Project skills support [mock interviews](.agents/skills/mock-interview/SKILL.md), [pattern extraction](.agents/skills/extract-pattern/SKILL.md), [Hard-problem coaching](.agents/skills/hard-coach/SKILL.md), and [practice logging](.agents/skills/practice-log/SKILL.md). Repository conventions live in [AGENTS.md](AGENTS.md); Claude Code reads them through [CLAUDE.md](CLAUDE.md).

</details>

## Help improve the playbook

Corrections, clearer explanations, counterexamples, translations, and connections between existing notes are welcome. For a proposed change, identify the note, explain the issue, and include a small example or correctness argument when relevant.

If this collection helps you understand a pattern, consider starring it or sharing the note that helped you.
