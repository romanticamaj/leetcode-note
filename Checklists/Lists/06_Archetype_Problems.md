# 🎯 Archetype Problems (原型問題)

記錄各個算法領域中最經典的原型問題。

---

## Dynamic Programming

- LeetCode 118. Pascal's Triangle

### 0/1 Knapsack

- LeetCode 494. Target Sum

### Unbounded Knapsack

### LIS (Longest Increasing Subsequence)

### Interval DP

### State Machine DP

---

## Graph Algorithms

- 🟢 LeetCode 323. Number of Connected Components in an Undirected Graph

### BFS Shortest Path

### Topological Sort

- 🟢 🟡 LeetCode 210. Course Schedule II

### Union-Find

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

---

## Bit Manipulation

- LeetCode 338. Counting Bits
  - 清除最低位的 1：`dp[x] = dp[x & (x - 1)] + 1`；移除一個固定貢獻，剩下仍是同一種子問題。

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
