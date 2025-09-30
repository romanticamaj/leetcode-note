# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a structured collection of notes, patterns, and mental models for mastering technical interviews and engineering problem-solving. It focuses on extracting reusable strategies, design principles, and testing frameworks rather than just collecting solutions.

## Repository Structure

### Core Knowledge Areas
- **`Data_Structures/`**: Implementation details, trade-offs, and patterns for fundamental data structures
- **`Algorithms/`**: Key algorithm strategies (Sliding Window, Two Pointers, BFS, DFS, etc.)
- **`CPP_Reference/`**: C++ specific best practices, STL implementation details, common mistakes
- **`Interview_Playbook/`**: High-level strategies, checklists, mental models for technical interviews
- **`Test_Case_Construction/`**: Frameworks for designing effective test cases
- **`Problem_Transformation/`**: Techniques for reframing problems into familiar forms

### Key Files
- **`Algorithm_Techniques_Checklist.md`**: Comprehensive list of algorithm techniques with difficulty ratings, time/space complexity, and core concepts
- **`LeetCode_Tricks_and_Keywords.md`**: Problem-specific tricks and keywords for quick reference
- **`Problem_Review_Checklist.md`**: Tracking list for problems requiring review (in Chinese)

## Development Commands

This repository contains markdown documentation only. There are no build, test, or lint commands needed for development.

## Interview Practice Mode

**IMPORTANT**: When the user pastes a LeetCode problem (identifiable by problem number, difficulty rating, or LeetCode problem format), **automatically invoke the `google-interviewer` subagent** to conduct a mock Google L5 technical interview using that problem.

**Do NOT**:
- Solve the problem directly
- Provide solutions or hints
- Analyze the problem yourself

**Always use the google-interviewer agent for interactive interview practice** when a LeetCode problem is detected.

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
- **Two Pointers**: Fast/Slow, K-Gap, Adjacent
- **Sliding Window**: Variable and fixed-size windows
- **Monotonic Stack/Queue**: For "next greater/smaller" problems
- **Graph Traversal**: BFS for shortest path, DFS for connectivity
- **Dynamic Programming**: 1D, 2D, and state compression variants
- **Binary Search**: On sorted arrays and answer spaces

## Document Style Conventions for 心法/Playbook Files

### File Naming Convention
- Use numbering prefix when multiple related files exist (e.g., `01-Core_Concepts.md`, `02-Advanced_Techniques.md`)
- Use descriptive names that reflect the content (e.g., `DFS_Tree_vs_Graph.md`, `State_Space_Tree.md`)
- File names should be content-focused, not necessarily ending with "Playbook" or "心法"
- Place in appropriate algorithm/technique folder

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