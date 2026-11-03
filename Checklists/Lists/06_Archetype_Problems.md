# 🎯 Archetype Problems (原型問題)

記錄各個算法領域中最經典的原型問題。

---

## Dynamic Programming

- LeetCode 118. Pascal's Triangle
- LeetCode 746. Min Cost Climbing Stairs

### Counting DP

- 🟡 LeetCode 63. Unique Paths II
  - `dp[r][c]` 是到達該格的路徑數；障礙格為 0，其餘累加上方與左方的路徑數。

### 0/1 Knapsack

筆記：[Knapsack DP：物品使用限制、數值目標與偽多項式成本](../../Algorithms/Dynamic_Programming/Problem_Types/Knapsack_DP.md)。

- 🟡 LeetCode 416. [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/)
  - **判定型原型**：`dp(i, remaining)` 表示剩餘物品能否湊出目標；選／不選都前進到 `i + 1`。同一狀態共用答案；令 `T = sum / 2`，時間 O(nT)、cache 空間 O(nT)。見 [數值範圍如何形成可負擔的狀態表](../../Algorithms/Dynamic_Programming/Subset_Sum/01-Subset_Sum_and_NP_Completeness.md)。
- LeetCode 494. Target Sum
  - **計數型延伸**：由加減符號分配轉為子集和計數；與判定型的狀態值、聚合方式不同。

### Unbounded Knapsack

### LIS (Longest Increasing Subsequence)

### Interval DP

### State Machine DP

- LeetCode 309. Best Time to Buy and Sell Stock with Cooldown
  - **日期 × 持股狀態的多維 DP 原型**：以 buy[i]／sell[i] 分別保存當天結束時持股／未持股的最大收益；cooldown 使買入轉移依賴 sell[i-2]，每個狀態都保留休息的選項。時間 O(n)、array 空間 O(n)。

### Tree DP

- 🔴 🟡 LeetCode 124. [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/)

---

## Graph Algorithms

- 🟢 LeetCode 323. Number of Connected Components in an Undirected Graph

### BFS Shortest Path

#### Multi-source BFS（多源 BFS）

- 🟡 LeetCode 542. [01 Matrix](https://leetcode.com/problems/01-matrix/)
  - 將所有 `0` 同時作為距離為 0 的起點入隊，逐層向外擴展；每格首次被發現時，就得到到最近 `0` 的最短距離。入隊時標記，避免重複加入；m × n 矩陣的時間與最壞額外空間皆為 O(mn)。

### Topological Sort

- 🟢 🟡 LeetCode 210. Course Schedule II

### Dijkstra（非負權重單源最短路徑）

- LeetCode 743. Network Delay Time
  - **單源到所有節點的最短路徑原型**：有向、非負權重圖；min-heap 存 `{累積距離, node}`，透過 relaxation 更新距離並跳過過時候選。答案取所有最短距離的最大值，不可達則回傳 -1。
  - ⚠️ pair 的第一欄是排序鍵，不能放 node，也不是單條邊的 weight。見 [Dijkstra 指南](../../Algorithms/Greedy/Dijkstra's%20Algorithm/01-Dijkstra_Algorithm_Guide.md)。

### Union-Find

- 🟡 LeetCode 684. [Redundant Connection](https://leetcode.com/problems/redundant-connection/)
  - **無向圖增量判環原型**：依輸入順序加入邊；兩端已在同一連通分量時，當前邊閉合唯一環，也就是環中輸入順序最後的邊。見 [Union-Find 推薦實作](../../Algorithms/Union_Find/06-Optimized_Implementation_and_Analysis.md)。

---

## Two Pointers

### Opposite Direction (相向雙指針)

- 🟢 🟡 LeetCode 27. Remove Element

### Fast-Slow Pointers (快慢指針)

- 🟢 🟡 LeetCode 26. Remove Duplicates from Sorted Array

### Read/Write Pointers（讀取／寫入雙指針）

- 🟢 LeetCode 283. Move Zeroes

---

## Binary Search

### Binary Search on Answer

- 🟢 🟡 LeetCode 69. Sqrt(x)

### Lower/Upper Bound

---

## Sliding Window

- 🟢 LeetCode 219. Contains Duplicate II

### Variable Size Window

---

## String Matching

### Substring Search

- LeetCode 28. Find the Index of the First Occurrence in a String

---

## Greedy

### Interval Scheduling

---

## Backtracking

### Combinations（固定長度組合）

- 🟡 LeetCode 77. Combinations
  - `start` 保證選出的數嚴格遞增；還缺 `k - path.size()` 個時，候選上界是 `n - (k - path.size()) + 1`，只展開仍能湊滿的分支。

### Subsets

---

## Tree Traversal

### DFS - Path Sum

### BFS - Level Order Traversal

---

## Decrease and Conquer

- LeetCode 235. Lowest Common Ancestor of a Binary Search Tree
  - Tail Recursion → Iteration

---

## Bucket Sort（桶排序）

- 🟢 🟡 LeetCode 347. Top K Frequent Elements

---

## Priority Queue（priority_queue）

### Bounded Min-Heap — Top K（固定容量最小堆）

- 🟢 🟡 LeetCode 347. Top K Frequent Elements
- 🟢 LeetCode 703. Kth Largest Element in a Stream

### Bounded Max-Heap — K Smallest（固定容量最大堆）

- 🟢 LeetCode 973. K Closest Points to Origin

---

## Bit Manipulation

- LeetCode 338. Counting Bits
  - 清除最低位的 1：`dp[x] = dp[x & (x - 1)] + 1`；移除一個固定貢獻，剩下仍是同一種子問題。
- 🟢 🟡 LeetCode 137. Single Number II

---

## Data Structures

### Linked List — Find Middle + Reverse + Merge（找中點、反轉、交錯合併）

- LeetCode 143. Reorder List

### Hash Set (Seen-Set)

- LeetCode 217. Contains Duplicate

### Bijection（一對一映射）

- LeetCode 290. Word Pattern
  - 雙向 mapping，或 forward mapping + used set；另須確認 pattern 長度與 word 數量一致。

### Monotonic Stack

- 🟡 LeetCode 739. Daily Temperatures

### Prefix Sum
