# LeetCode Tricks and Keywords

## 1200. Minimum Absolute Difference

- Sort + 1 Traversal (running minimum absolute difference)

## 84. Largest Rectangle in Histogram

- Divide and Conquer

## 173. Binary Search Tree Iterator

- Keep a successor
- Flattening the BST, using a vector
- Controlled Recursion (Iterative Stack)

## 261. Graph Valid Tree

- iterative cycle detection + visited count(for forest)
- iterative unconditionally visited + edge count + visited count(for forest)

## 1059. All Paths from Source Lead to Destination

- node-coloring variant for cycle detection

## 1089. Duplicate Zeros

- two pointers to find new end
- edge case: last one not duplicate (handle at two pointer stage)
- backward fill

## 1168. Optimize Water Distribution in a Village

- super source + MST

## 15. 3Sum

- Sort + Two Pointers (Two Sum variant)
- Fix k, search [k+1, n-1], skip duplicates

## 310. Minimum Height Trees

- Centroids (at most two)
- Kahn's algorithm on leaf nodes (indegree 1)

## 31. Next Permutation

- Find first `less than pair` from the end
- Reverse sorted at the end
- Find the next big from the reverse sorted from the end
- Reverse the reverse sorted

## 222. Count Complete Tree Nodes

- Use the property of complete tree -> depth (0, 1, ...)
- Binary search and pivot/mid of binary search as direction indicator

## 109. Convert Sorted List to Binary Search Tree

- Divide And Conquer
- In-order simulation using a global state (a pointer tracking the control state)

## 146. LRU Cache

- Doubly linked list with dummy head and tail

## 212. Word Search II

- Backtracking + Dynamic Trie
