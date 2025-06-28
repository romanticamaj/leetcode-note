# ChatGPT Advice: How to Construct Test Cases Under Interview Pressure

When you're in a high-pressure interview and the problem doesn't come with test cases, here's how ChatGPT would guide you to think clearly and systematically.

---

## 🎯 Step 1: Clarify the Problem

Before writing any test case, make sure you understand:

- What are the **inputs** and **outputs**?
- What are the **constraints** (e.g., size limits, value ranges)?
- Are there **edge behaviors** (e.g., empty input, nulls, duplicates)?

Ask clarifying questions if needed. If not allowed, make and state your assumptions.

---

## 🧠 Step 2: Use the "GEC" Framework

A fast and reliable way to generate test cases is to think in three categories:

### ✅ Generic Case

- A normal, expected input that exercises the main logic.
- Example: For "Two Sum", `nums = [2, 7, 11, 15], target = 9`.

### ⚠️ Edge Cases

- Empty input
- Single element
- Max/min values
- Sorted/reverse-sorted
- Duplicates
- Zero/negative numbers

Use the mnemonic **ZOMBIES**:

- **Z**ero
- **O**ne
- **M**ax/Min
- **B**lank (empty)
- **I**nvalid (if applicable)
- **E**ven/Odd
- **S**orted/Special

### 🧪 Corner Cases

- Combinations of edge cases
- Inputs that might break assumptions
- Example: For a graph traversal, a cycle or disconnected component

---

## 🧾 Step 3: Write 3–5 Test Cases Quickly

In your code or on the whiteboard, write:

1. A generic case
2. One or two edge cases
3. One corner case

This shows the interviewer you’re thinking deeply and testing thoroughly.

---

## 🧩 Step 4: Trace One Case by Hand

Pick a small test case and walk through your code **line by line**.

- This helps you catch bugs early.
- It also shows the interviewer your thought process.

---

## 🧘 Practice the Pattern

The more you practice generating test cases, the faster and more natural it becomes. Try this:

- Pick a random LeetCode problem.
- Don’t solve it.
- Just write 5 test cases for it.

This builds the muscle memory you’ll need in interviews.

---

## Summary

| Step | Action                              |
| ---- | ----------------------------------- |
| 1    | Clarify the problem and constraints |
| 2    | Use GEC (Generic, Edge, Corner)     |
| 3    | Write 3–5 test cases                |
| 4    | Trace one by hand                   |
| 5    | Practice this skill regularly       |
