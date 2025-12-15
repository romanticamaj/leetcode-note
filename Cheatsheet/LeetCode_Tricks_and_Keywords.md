# LeetCode Tricks and Keywords

## Divide and Conquer

- LeetCode 84. Largest Rectangle in Histogram
- LeetCode 109. Convert Sorted List to Binary Search Tree
  - In-order simulation using a global state (a pointer tracking the control state)

## Sort + Traversal

- LeetCode 1200. Minimum Absolute Difference
  - Sort + 1 Traversal (running minimum absolute difference)
- LeetCode 15. 3Sum
  - Sort + Two Pointers (Two Sum variant)
  - Fix k, search [k+1, n-1], skip duplicates

## Binary Search Tree Iterator

- LeetCode 173. Binary Search Tree Iterator
  - Keep a successor
  - Flattening the BST, using a vector
  - Controlled Recursion (Iterative Stack)

## Graph Cycle Detection

- LeetCode 261. Graph Valid Tree
  - iterative cycle detection + visited count(for forest)
  - iterative unconditionally visited + edge count + visited count(for forest)
- LeetCode 1059. All Paths from Source Lead to Destination
  - node-coloring variant for cycle detection

## Two Pointers

- LeetCode 1089. Duplicate Zeros
  - two pointers to find new end
  - edge case: last one not duplicate (handle at two pointer stage)
  - backward fill

## MST (Minimum Spanning Tree)

- LeetCode 1168. Optimize Water Distribution in a Village
  - super source + MST

## Topological Sort

- LeetCode 310. Minimum Height Trees
  - Centroids (at most two)
  - Kahn's algorithm on leaf nodes (indegree 1)

## Permutation

- LeetCode 31. Next Permutation
  - Find first `less than pair` from the end
  - Reverse sorted at the end
  - Find the next big from the reverse sorted from the end
  - Reverse the reverse sorted

## Binary Search

- LeetCode 222. Count Complete Tree Nodes
  - Use the property of complete tree -> depth (0, 1, ...)
  - Binary search and pivot/mid of binary search as direction indicator

## LRU Cache

- LeetCode 146. LRU Cache
  - Doubly linked list with dummy head and tail

## Backtracking + Trie

- LeetCode 212. Word Search II
  - Backtracking + Dynamic Trie

## Randomized Data Structure

- LeetCode 380. Insert Delete GetRandom O(1)
  - hashmap + vector + swap to the end then delete

## Palindrome

- LeetCode 5. Longest Palindromic Substring
  - Dynamic Programming boolean DP + globaling tracking
  - Two Pointers + Expand Around Center
  - Manacher's Algorithm

## Tree Traversal

- LeetCode 590. N-ary Tree Postorder Traversal
  - node + processed child count
  - visit flag (due to visit twice nature)

## Integer Manipulation

- LeetCode 7. Reverse Integer
  - C++ Modulo Operator Returns Negative if input is negative
  - Integer out of bound detection (Memorize: 2147483647, -2147483648)

## Prefix Sum

- LeetCode 238. Product of Array Except Self
  - Prefix Sum / Running Sum

## Cycle Detection (Linked List / Number)

- LeetCode 202. Happy Number
  - Hashmap
