# LeetCode Tricks and Keywords

- LeetCode 84. Largest Rectangle in Histogram

  - Divide and Conquer

- LeetCode 109. Convert Sorted List to Binary Search Tree

  - Divide and Conquer
  - In-order simulation using a global state (a pointer tracking the control state)

- LeetCode 1200. Minimum Absolute Difference

  - Sort + Traversal
  - Sort + 1 Traversal (running minimum absolute difference)

- LeetCode 15. 3Sum

  - Sort + Two Pointers (Two Sum variant)
  - Fix k, search [k+1, n-1], skip duplicates

- LeetCode 173. Binary Search Tree Iterator

  - Keep a successor
  - Flattening the BST, using a vector
  - Controlled Recursion (Iterative Stack)

- LeetCode 261. Graph Valid Tree

  - Graph Cycle Detection
  - iterative cycle detection + visited count(for forest)
  - iterative unconditionally visited + edge count + visited count(for forest)

- LeetCode 1059. All Paths from Source Lead to Destination

  - Graph Cycle Detection
  - node-coloring variant for cycle detection

- LeetCode 1089. Duplicate Zeros

  - Two Pointers to find new end
  - Edge Case: last one not duplicate (handle at two pointer stage)
  - Backward Filling

- LeetCode 1168. Optimize Water Distribution in a Village

  - MST (Minimum Spanning Tree)
  - Super Source + MST

- LeetCode 310. Minimum Height Trees

  - Topological Sort
  - Centroids (at most two)
  - Kahn's algorithm on leaf nodes (indegree 1)

- LeetCode 31. Next Permutation

  - Permutation
  - Find first `less than pair` from the end
  - Reverse sorted at the end
  - Find the next big from the reverse sorted from the end
  - Reverse the reverse sorted

- LeetCode 222. Count Complete Tree Nodes

  - Binary Search
  - Use the property of complete tree -> depth (0, 1, ...)
  - Binary search and pivot/mid of binary search as direction indicator

- LeetCode 146. LRU Cache

  - LRU Cache
  - Doubly linked list with dummy head and tail

- LeetCode 212. Word Search II

  - Backtracking + Trie
  - Backtracking + Dynamic Trie

- LeetCode 380. Insert Delete GetRandom O(1)

  - Randomized Data Structure
  - hashmap + vector + swap to the end then delete

- LeetCode 5. Longest Palindromic Substring

  - Palindrome
  - Dynamic Programming boolean DP + globaling tracking
  - Two Pointers + Expand Around Center
  - Manacher's Algorithm

- LeetCode 590. N-ary Tree Postorder Traversal

  - Tree Traversal
  - node + processed child count
  - visit flag (due to visit twice nature)

- LeetCode 7. Reverse Integer

  - Integer Manipulation
  - C++ Modulo Operator Returns Negative if input is negative
  - Integer out of bound detection (Memorize: 2147483647, -2147483648)

- LeetCode 238. Product of Array Except Self

  - Prefix Sum / Running Sum

- LeetCode 202. Happy Number

  - Cycle Detection (Linked List / Number)
  - Hashmap

- LeetCode 1752. Check if Array Is Sorted and Rotated

  - Inflection Point

- LeetCode 371. Sum of Two Integers

  - Bit Manipulation

- LeetCode 373. Find K Pairs with Smallest Sums

  - Merge K Sorted Lists + Priority Queue

- LeetCode 45. Jump Game II

  - Dynamic Programming
  - Greedy (Expand Range, maintain an expandable range, update jump count at proper timing)

- LeetCode 292. Nim Game

  - brainteaser
  - Considering which one you take on 5, then you must win

- LeetCode 72. Edit Distance

  - Considering word1[0..i-1] and word2[0..j-1]
  - Comparing word1[i-1] and word2[j-1]
  - if not equal: replace check dp[i-1][j-1], insert check dp[i][j-1], remove check dp[i-1][j]

- LeetCode 128. Longest Consecutive Sequence

  - Hash Table + Possible Start (check num - 1)

- LeetCode 424. Longest Repeating Character Replacement

  - Sliding Window + Hash Table + Greedy (maxCount and frequency)

- LeetCode 1925. Count Square Sum Triples
  - sqrt + integer verification
