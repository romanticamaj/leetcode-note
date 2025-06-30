# ChatGPT's Guide to Building Test Cases Under Pressure

Here’s a straightforward guide, as if you asked ChatGPT, on how to effectively build test cases during a high-pressure coding interview.

---

### "How should I build test cases in an interview?"

That's a great question. Building your own test cases shows the interviewer that you're thorough and think about robustness. Here’s a simple, effective strategy:

#### **1. Start with the Obvious: The "Happy Path"**

First, create a simple, standard test case that you expect to work. This is to verify that your main logic is correct.

- **Example (Two Sum):** `nums = [2, 7, 11, 15], target = 9`. The answer is clearly `[0, 1]`.
- **Why?** It’s a quick sanity check. If your code fails this, you have a fundamental logic error.

#### **2. Think About the Edges: The "Empty and Small" Cases**

Next, consider the absolute limits of the input. This is where many bugs hide.

- **Empty Inputs:** What if the array, string, or list is empty? `[]`, `""`. Does your code handle it gracefully or crash?
- **Single-Element Inputs:** What if there's only one item? `[5]`. This tests loops and boundary conditions.
- **Two-Element Inputs:** A simple case to test interactions.

#### **3. Probe the Constraints: The "Boundary" Cases**

Look at the problem's constraints (e.g., `1 <= n <= 10^5`, `values are positive`).

- **Minimums and Maximums:** Test with the smallest and largest possible values.
- **Duplicates:** What if the input contains duplicate numbers or characters? `[3, 5, 3, 1]`.
- **Pre-sorted / Reverse-sorted:** Does your algorithm handle data that's already in a specific order?

#### **4. Look for "Evil" Combinations: The "Corner" Cases**

These are tricky scenarios where multiple edge cases might interact.

- **All Duplicates:** An array where all elements are the same, like `[5, 5, 5, 5]`.
- **A mix of negatives and positives.**
- **For Trees/Graphs:** A single long chain (like a linked list), a disconnected graph, or a graph with a cycle.

---

### A Practical Workflow in an Interview:

1.  **Verbalize First:** Say, "Okay, before I code, I'm thinking about a few test cases to validate my approach."
2.  **Write 3 Key Cases on the Whiteboard/Comment:**
    - A simple "happy path" case.
    - An "empty/single element" edge case.
    - A "duplicates" or "boundary" case.
3.  **Code Your Solution.**
4.  **Trace Your Code:** Pick one of your written test cases (usually the happy path) and walk the interviewer through your code line-by-line, showing how it works.
5.  **Mention Others:** "I'd also want to test for an empty array and an array with all duplicate values to be fully confident."

This structured approach demonstrates a professional, quality-oriented mindset, which is often just as important as the code itself.
