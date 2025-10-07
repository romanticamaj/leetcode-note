# Hard Techniques Reference

Hard 題必備技巧清單，包含難度等級、核心概念、以及從簡單到困難的學習路徑。

## 📊 Difficulty Levels

- ⭐ **Essential**: 必備技巧，Medium/Hard 常見
- ⭐⭐ **Advanced**: 進階技巧，Hard 題常見
- ⭐⭐⭐ **Expert**: 專家級技巧，Top Hard 題或競賽題

---

## 目錄

- [Dynamic Programming](#dynamic-programming)
- [Data Structures](#data-structures)
- [Graph Algorithms](#graph-algorithms)
- [Divide & Conquer / Sorting](#divide--conquer--sorting)
- [Math & Other Tricks](#math--other-tricks)

---

## Dynamic Programming

### Digit DP
- **Level**: ⭐⭐⭐ Expert
- **Use Case**: Counting numbers with constraints on digits
- **Core Concept**: DP on digit positions with state tracking (tight bound, leading zeros, etc.)
- **Learning Path**:
  - 📘 Easy: 理解基礎計數 DP
  - 📙 Medium: LC 233 (Number of Digit One), LC 902 (Numbers At Most N Given Digit Set)
  - 📕 Hard: LC 1012 (Numbers With Repeated Digits), LC 1397 (Find All Good Strings)

### Interval DP
- **Level**: ⭐⭐ Advanced
- **Use Case**: Merging stones, bursting balloons, palindrome partitioning
- **Core Concept**: DP on subarrays `dp[i][j]` = optimal value for range `[i, j]`
- **Learning Path**:
  - 📘 Easy: LC 516 (Longest Palindromic Subsequence)
  - 📙 Medium: LC 1039 (Minimum Score Triangulation), LC 1130 (Minimum Cost Tree From Leaf Values)
  - 📕 Hard: LC 312 (Burst Balloons), LC 1000 (Minimum Cost to Merge Stones)

### Bitmask DP (State Compression)
- **Level**: ⭐⭐ Advanced
- **Use Case**: Traveling salesman, assignment problems, subset DP
- **Core Concept**: Use bitmask to represent state, DP on subsets
- **Learning Path**:
  - 📘 Easy: LC 78 (Subsets), LC 1863 (Sum of All Subset XOR Totals)
  - 📙 Medium: LC 1125 (Smallest Sufficient Team), LC 1986 (Minimum Number of Work Sessions)
  - 📕 Hard: LC 847 (Shortest Path Visiting All Nodes), LC 1879 (Minimum XOR Sum)

### Tree DP
- **Level**: ⭐⭐ Advanced
- **Use Case**: DP on tree structure, rerooting DP
- **Core Concept**: DP state at each node based on subtree information
- **Learning Path**:
  - 📘 Easy: LC 543 (Diameter of Binary Tree), LC 104 (Maximum Depth of Binary Tree)
  - 📙 Medium: LC 124 (Binary Tree Maximum Path Sum), LC 337 (House Robber III)
  - 📕 Hard: LC 834 (Sum of Distances in Tree), LC 968 (Binary Tree Cameras)

### Probability / Expectation DP
- **Level**: ⭐⭐⭐ Expert
- **Use Case**: Expected value calculation, game theory
- **Core Concept**: DP with probabilities, expected value recurrence
- **Learning Path**:
  - 📙 Medium: LC 688 (Knight Probability in Chessboard), LC 837 (New 21 Game)
  - 📕 Hard: LC 808 (Soup Servings), LC 1467 (Probability of a Two Boxes Having The Same Number)

---

## Data Structures

### Fenwick Tree (Binary Indexed Tree)
- **Level**: ⭐⭐ Advanced
- **Use Case**: Prefix sums with updates, frequency counts, range queries, counting inversions
- **Core Concept**: Tree structure using bit manipulation (i & -i) for O(log n) update and query
- **詳細文檔**: [Binary Indexed Tree 完整指南](../Data_Structures/Advanced/Binary_Indexed_Tree/)
- **Learning Path**:
  - 📘 Easy: LC 303 (Range Sum Query - Immutable) - 理解 prefix sum
  - 📙 Medium: LC 307 (Range Sum Query - Mutable) - BIT 入門題 ⭐ 必做
  - 📕 Hard: LC 315 (Count of Smaller Numbers After Self), LC 493 (Reverse Pairs)

### Segment Tree / Lazy Propagation
- **Level**: ⭐⭐ Advanced
- **Use Case**: Range updates, range queries (sum/min/max), interval problems
- **Core Concept**: Tree structure for O(log n) range operations
- **Learning Path**:
  - 📙 Medium: LC 307 (Range Sum Query - Mutable), LC 729 (My Calendar I)
  - 📕 Hard: LC 715 (Range Module), LC 732 (My Calendar III)

### Monotonic Stack / Monotonic Queue
- **Level**: ⭐ Essential
- **Use Case**: Next greater/smaller element, sliding window max/min
- **Core Concept**: Maintain monotonic property while traversing
- **Learning Path**:
  - 📘 Easy: LC 496 (Next Greater Element I), LC 739 (Daily Temperatures)
  - 📙 Medium: LC 503 (Next Greater Element II), LC 907 (Sum of Subarray Minimums)
  - 📕 Hard: LC 84 (Largest Rectangle in Histogram), LC 85 (Maximal Rectangle)

### Trie
- **Level**: ⭐ Essential
- **Use Case**: Prefix matching, XOR max queries, word search
- **Core Concept**: Tree structure for prefix-based operations
- **Learning Path**:
  - 📘 Easy: LC 208 (Implement Trie), LC 720 (Longest Word in Dictionary)
  - 📙 Medium: LC 211 (Design Add and Search Words), LC 421 (Maximum XOR)
  - 📕 Hard: LC 212 (Word Search II), LC 1707 (Maximum XOR With an Element From Array)

### Union-Find (Disjoint Set)
- **Level**: ⭐ Essential
- **Use Case**: Connectivity, Kruskal MST, dynamic connectivity
- **Core Concept**: Union and find operations with path compression
- **Learning Path**:
  - 📘 Easy: LC 547 (Number of Provinces)
  - 📙 Medium: LC 200 (Number of Islands), LC 684 (Redundant Connection)
  - 📕 Hard: LC 685 (Redundant Connection II), LC 1697 (Checking Existence of Edge)

---

## Graph Algorithms

### Eulerian Path / Circuit (Hierholzer's Algorithm)
- **Level**: ⭐⭐⭐ Expert
- **Use Case**: Find path visiting every edge exactly once
- **Core Concept**: Greedy DFS with edge removal
- **Learning Path**:
  - 📙 Medium: LC 332 (Reconstruct Itinerary)
  - 📕 Hard: LC 753 (Cracking the Safe)

### Topological Sort + DP
- **Level**: ⭐⭐ Advanced
- **Use Case**: DAG path problems, course scheduling with optimization
- **Core Concept**: Combine topological order with DP
- **Learning Path**:
  - 📘 Easy: LC 207 (Course Schedule)
  - 📙 Medium: LC 210 (Course Schedule II), LC 1136 (Parallel Courses)
  - 📕 Hard: LC 1632 (Rank Transform of a Matrix), LC 2050 (Parallel Courses III)

### Maximum Bipartite Matching (Hopcroft-Karp)
- **Level**: ⭐⭐⭐ Expert
- **Use Case**: Matching problems in bipartite graphs
- **Core Concept**: Augmenting path algorithm
- **Learning Path**:
  - 📘 Easy: LC 785 (Is Graph Bipartite?)
  - 📙 Medium: LC 886 (Possible Bipartition)
  - 📕 Hard: Implement Hopcroft-Karp for max matching

### Strongly Connected Components (Tarjan/Kosaraju)
- **Level**: ⭐⭐⭐ Expert
- **Use Case**: Finding SCCs in directed graphs
- **Core Concept**: DFS-based algorithms
- **Learning Path**:
  - 📙 Medium: LC 1192 (Critical Connections in a Network)
  - 📕 Hard: LC 1568 (Minimum Number of Days to Disconnect Island)

---

## Divide & Conquer / Sorting

### Merge Sort Variants
- **Level**: ⭐⭐ Advanced
- **Use Case**: Counting inversions, smaller elements after self, reverse pairs
- **Core Concept**: Count during merge process
- **Learning Path**:
  - 📙 Medium: LC 327 (Count of Range Sum)
  - 📕 Hard: LC 315 (Count of Smaller Numbers After Self), LC 493 (Reverse Pairs)

### Binary Search on Answer
- **Level**: ⭐ Essential
- **Use Case**: Minimize/maximize target value, optimization problems
- **Core Concept**: Binary search on solution space
- **Learning Path**:
  - 📘 Easy: LC 69 (Sqrt(x)), LC 374 (Guess Number)
  - 📙 Medium: LC 875 (Koko Eating Bananas), LC 1283 (Find Smallest Divisor)
  - 📕 Hard: LC 410 (Split Array Largest Sum), LC 1231 (Divide Chocolate)

### Divide & Conquer Optimization (Knuth, Monge)
- **Level**: ⭐⭐⭐ Expert
- **Use Case**: DP optimization, quadrangle inequality
- **Core Concept**: Reduce DP complexity from O(n³) to O(n²)
- **Learning Path**:
  - 📙 Medium: Study quadrangle inequality property
  - 📕 Hard: LC 1478 (Allocate Mailboxes), competitive programming problems

---

## Math & Other Tricks

### Prefix Sum / Difference Array (2D/3D)
- **Level**: ⭐ Essential
- **Use Case**: Range queries, subarray problems
- **Core Concept**: Precompute cumulative sums for O(1) queries
- **Learning Path**:
  - 📘 Easy: LC 303 (Range Sum Query), LC 304 (Range Sum Query 2D)
  - 📙 Medium: LC 1314 (Matrix Block Sum), LC 1738 (Find Kth Largest XOR)
  - 📕 Hard: LC 363 (Max Sum of Rectangle No Larger Than K)

### Matrix Exponentiation
- **Level**: ⭐⭐ Advanced
- **Use Case**: DP state transitions, Fibonacci-like recurrence
- **Core Concept**: Use matrix multiplication for fast DP
- **Learning Path**:
  - 📙 Medium: LC 70 (Climbing Stairs with large n)
  - 📕 Hard: LC 552 (Student Attendance Record II)

### Two Pointers / Sliding Window
- **Level**: ⭐ Essential
- **Use Case**: Subarray/substring problems, optimization
- **Core Concept**: Maintain window with two pointers
- **Learning Path**:
  - 📘 Easy: LC 1 (Two Sum), LC 167 (Two Sum II)
  - 📙 Medium: LC 3 (Longest Substring Without Repeating), LC 76 (Minimum Window)
  - 📕 Hard: LC 992 (Subarrays with K Different Integers), LC 1425 (Constrained Subsequence Sum)

### Combinatorics (Catalan, Binomial)
- **Level**: ⭐⭐ Advanced
- **Use Case**: Counting problems, combinatorial optimization
- **Core Concept**: Mathematical formulas for counting
- **Learning Path**:
  - 📙 Medium: LC 62 (Unique Paths), LC 96 (Unique BSTs)
  - 📕 Hard: LC 95 (Unique BSTs II), LC 1569 (Number of Ways to Reorder Array)

---

## 📑 Quick Reference: Hard → Simpler Problem Mapping

| Hard Technique           | Example Hard Problems                                  | Practice First (Simpler)                                             |
| ------------------------ | ------------------------------------------------------ | -------------------------------------------------------------------- |
| **Merge Sort Variants**  | LC 315, LC 493                                         | LC 327 (Count of Range Sum)                                          |
| **Digit DP**             | LC 1012, LC 1397                                       | LC 233 (Number of Digit One), LC 902                                 |
| **Interval DP**          | LC 312 (Burst Balloons), LC 1000                       | LC 516 (Longest Palindromic Subsequence), LC 1039                    |
| **Bitmask DP**           | LC 847, LC 1879                                        | LC 78 (Subsets), LC 1125, LC 1986                                    |
| **Fenwick Tree**         | LC 315, LC 493                                         | LC 303 (Immutable) → LC 307 (Mutable) ⭐                              |
| **Segment Tree**         | LC 715, LC 732                                         | LC 307, LC 729                                                       |
| **Monotonic Stack**      | LC 84, LC 85                                           | LC 496, LC 739 (Daily Temperatures)                                  |
| **Trie**                 | LC 212 (Word Search II), LC 1707                       | LC 208 (Implement Trie), LC 421                                      |
| **Eulerian Path**        | LC 753 (Cracking the Safe)                             | LC 332 (Reconstruct Itinerary)                                       |
| **Topological Sort + DP**| LC 1632, LC 2050                                       | LC 207, LC 210                                                       |
| **Tree DP**              | LC 834, LC 968                                         | LC 124 (Binary Tree Maximum Path Sum), LC 543                        |
| **Binary Search on Ans** | LC 410, LC 1231                                        | LC 875 (Koko Eating Bananas), LC 1283                                |

---

## 💡 使用建議

1. **遇到 Hard 題時**:
   - 快速識別用到的技巧
   - 如果技巧完全陌生，先標記，去練 "Practice First" 欄位的題目
   - 建立基礎後再回來解 Hard 題

2. **學習新技巧時**:
   - 按照 📘 Easy → 📙 Medium → 📕 Hard 的順序練習
   - 確保理解核心概念後再進階

3. **複習時**:
   - 同類題型一起練，建立肌肉記憶
   - 注意技巧的變形和組合應用

---

## 🔗 相關資源

- **學習策略**: [Hard_Problem_Learning_Strategy.md](Hard_Problem_Learning_Strategy.md)
- **問題追蹤**: [Problem_Review_Checklist.md](../Problem_Review_Checklist.md)
- **通用技巧**: [Algorithm_Techniques_Checklist.md](../Algorithm_Techniques_Checklist.md)
