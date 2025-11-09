# Gary's DSA Cheatsheet

## Quick Reference

### Trick

- Swap Trick: Algorithms/Backtracking/Swap_as_In_Place_State_Management.md
- Level-in-Queue trick: Algorithms/BFS/01-Level_Ordering_Level_in_Queue.md
- Vertex-Mapping trick: Algorithms/BFS/BFS_Vertex_Mapping_Pattern.md
- Multi-Source BFS: Algorithms/BFS/MultiSource_BFS_Thinking_Framework.md
- State-Space BFS: Algorithms/BFS/State_Space_BFS.md
- Solution-Space or Contraint Binary Search: Algorithms/Binary_Search/04-Binary_Search_on_Solution_Space.md, Algorithms/Binary_Search/05-Binary_Search_on_Constraint.md
- Bit Space Optimization: Algorithms/Bit_Manipulation/State_Compression_with_Bitmask.md
- Bidirectional Constraint Decomposition: Algorithms/Design_Principles/Bidirectional_Constraint_Decomposition.md
- Movement Constraint Transformation: Algorithms/Design_Principles/Transformation_Patterns/Movement_Constraint_Transformation.md
- Node Coloring DFS: Algorithms/DFS/03-Node_Coloring_DFS.md
- One-liner DFS: Algorithms/DFS/06-One-Liner_DFS_Pattern.md
- Kadane's Algorithm: Algorithms/Dynamic_Programming/Advanced_Techniques/Kadane_Algorithm.md
- DPState Decomposition for DP/Greedy: Algorithms/Dynamic_Programming/Advanced_Techniques/State_Decomposition.md
- Greedy Sweep Line with Top-K: Algorithms/Greedy/Greedy_Sweep_Cost_Optimization_with_Top_K.md
- Two-Heap Trick: Algorithms/Greedy/Two_Heaps_Greedy_Selection.md
- Min and Second-Min Trick: Algorithms/Math/Find_Min_and_Second_Min_Trick.md
- Running Sum Trick: Algorithms/Prefix_Sum/02_Running_State_Pattern.md
- Difference Array: Algorithms/Prefix_Sum/05_Difference_Array.md
- Two Pointer Trick: Algorithms/Two_Pointers
- Union Find: Algorithms/Union_Find
- Reverse Processing Trick: Data_Structures/Arrays_and_Strings/Reverse_Processing_Patterns.md
- vector Swap-to-End Deletion Trick: Data_Structures/Arrays_and_Strings/Vector_O1_Deletion_Swap_to_End.md
- Validation-Transformation Trick: Data_Structures/Hash_Tables/Validation_Transformation_Duality.md
- Iterative Traversal Trick: Data_Structures/Trees/Iterative_Traversal

### Advanced Algorithm

- Hieholzers' Algorithm: Algorithms/DFS/Hierholzers
- Bellman-Ford Algorithm: Algorithms/Dynamic_Programming/Advanced_Techniques/Bellman-Ford
- Dijkstra's Algorithm: Algorithms/Greedy/Dijkstra's Algorithm
- Kruskal's Algorithm: Algorithms/Greedy/MST_Algorithms/01-Kruskals_Algorithm.md
- Prim's Algorithm: Algorithms/Greedy/MST_Algorithms/02-Prims_Algorithm.md
- Lomuto Partition: Algorithms/Partition/01-Lomuto_Partition_Scheme.md
- Topological Sort: Algorithms/Topological_Sort

### Advanced Data Structure

- Binary Indexed Tree: Data_Structures/Advanced/Binary_Indexed_Tree
- De Bruijn Graph: Data_Structures/Advanced/De_Bruijn_Graph.md
- Monotonic Stack: Data_Structures/Stacks_and_Queues/Monotonic_Stacks
- Binary Tree Canonical Form: Data_Structures/Trees/Binary_Trees/Canonical_Forms_Transformation.md
- Trie: Data_Structures/Trie

## Backtracking

| Category              | Keywords                                       |
| --------------------- | ---------------------------------------------- |
| **State Design**      | `Decision Boundary`, `Constraint`              |
| **Backtracking**      | `Promising Check`, `Choose, Explore, Unchoose` |
| **Solution Building** | `Base Case/Solution Reach`, `Combine/Collect`  |

---

## Dynamic Programming

**Progression:**

1. Exhaustive Search / Backtracking
2. Top-Down DP with Memoization
3. Bottom-Up DP with Tabulation
4. Bottom-Up DP with Space Optimization

**Advanced:**

- State Compression

**Core Frameworks:**

### Three Essential Elements

State Definition → Recurrence → Traversal Order

---

## Sliding Window

**Mantra:** Expand → Fix → Update

---

## Number Theory

- **Primality Test**: `O(sqrt(n))` trial division. Loop condition: `for (long long i = 2; i * i <= n; ++i)`.
- **GCD / LCM**: Use `std::gcd` and `std::lcm` from `<numeric>` (C++17+).
- **Prime Factorization**: Trial division up to `sqrt(n)`. Remember to handle the remaining factor if `n > 1`.

---

## Topological Sort

- **Kahn's Algorithm**: Use a queue to store vertices with an in-degree of 0.
- **DFS-based**: Node-coloring (for cycle detection) + post-ordering traversal + reverse.
