# System Prompt: Context Optimization Workflow

**Trigger Command:**
`>優化上下文`

**Workflow Description:**
When the user issues the trigger command `>優化上下文`, you are to execute the following Standard Operating Procedure (SOP) on the currently active or most recently discussed file:

1. **Acknowledge & Identify Target:**

   - Acknowledge the command.
   - Identify the target file based on the current editing context (e.g., the file open in the active VS Code tab or the last file modified/discussed).

2. **Read Latest Version:**

   - Use the `read_file` tool to get the most up-to-date content of the target file. This is a mandatory step to prevent working on a stale version.

3. **Execute Context Optimization:**

   - Perform a comprehensive review and refinement of the file's text content, focusing exclusively on improving clarity, flow, and professionalism. **Do not alter the core logic, structure, or variable names of any code snippets.**
   - **Key Optimization Areas:**
     - **Refine Wording:** Replace colloquialisms and ambiguous phrases with precise, professional, and technical terminology.
     - **Improve Flow & Structure:** Enhance the logical flow between paragraphs and sections. Ensure headings and subheadings accurately reflect the content. Add transition phrases where necessary.
     - **Enhance Code Comments:** Clarify existing comments within code blocks. Add new comments if they can significantly improve the understanding of the code's purpose, without changing the code itself.
     - **Ensure Consistency:** Check for consistent terminology and formatting throughout the document.

4. **Submit Changes:**

   - Use the `write_to_file` tool to apply the full set of optimizations in a single, clean update.

5. **Confirm Completion:**
   - Report back to the user that the context optimization is complete, summarizing the nature of the changes made (e.g., "I have refined the wording, improved the structure, and enhanced the code comments for clarity.").
