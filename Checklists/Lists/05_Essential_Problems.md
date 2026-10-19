# Essential Problems

**Gary Hsieh's Personal Collection**

A curated list of must-do problems that build core competencies. Completing these problems will significantly strengthen your problem-solving abilities.

## Binary Search

- LeetCode 153. Find Minimum in Rotated Sorted Array
- LeetCode 33. Search in Rotated Sorted Array
- 🟡 LeetCode 378. Kth Smallest Element in a Sorted Matrix
- 🟡 LeetCode 981. Time Based Key-Value Store
- 🟢 LeetCode 69. Sqrt(x)

## Binary Search on Value Space

- 🔴 LeetCode 4. Median of Two Sorted Arrays

## Two Pointers

- LeetCode 141. Linked List Cycle
- 🟢 LeetCode 202. Happy Number
- LeetCode 125. Valid Palindrome
- LeetCode 345. Reverse Vowels of a String
- LeetCode 86. Partition List
- 🟡 🔴 LeetCode 143. Reorder List
- 🔴 LeetCode 42. Trapping Rain Water
- 🟡 LeetCode 75. Sort Colors
- LeetCode 9. Palindrome Number
- 🟢 🟡 LeetCode 26. Remove Duplicates from Sorted Array
- 🟡 🔴 LeetCode 31. Next Permutation
  - 找出最長非遞增 suffix，再調整 pivot 與 suffix。

## Linked List

- 🟡 LeetCode 142. Linked List Cycle II
- 🟡 🔴 LeetCode 143. Reorder List
- 🟡 🔴 LeetCode 287. Find the Duplicate Number

## Sliding Window

- LeetCode 438. Find All Anagrams in a String
- LeetCode 424. Longest Repeating Character Replacement
- 🟡 LeetCode 567. Permutation in String
- 🔴 LeetCode 76. Minimum Window Substring
- 🟢 LeetCode 219. Contains Duplicate II

## Backtracking

- 🟡 LeetCode 40. Combination Sum II
- 🟡 LeetCode 78. Subsets
- 🟡 🔴 LeetCode 131. Palindrome Partitioning
- 🟡 LeetCode 90. Subsets II

## BFS (Breadth-First Search)

- 🟡 🔴 LeetCode 45. Jump Game II
  - [ ] Greedy (嚴格說起來，是 BFS + 狀態壓縮去除 queue)

## DFS (Depth-First Search)

## Dynamic Programming

- LeetCode 72. Edit Distance
- 🟡 LeetCode 494. Target Sum
- 🟡 LeetCode 416. Partition Equal Subset Sum
- 🟡 🔴 LeetCode 139. Word Break
- 🟡 LeetCode 322. Coin Change
- 🟡 LeetCode 22. Generate Parentheses
- 🟡 LeetCode 97. Interleaving String
- 🟡 🔴 LeetCode 152. Maximum Product Subarray
  - 需要特別設計的查表邏輯 (其實就是遞迴式的設計)
- 🟡 🔴 LeetCode 124. Binary Tree Maximum Path Sum
  - Tree DP

## Kadane's Pattern DP

- LeetCode 53. Maximum Subarray
- LeetCode 32. Longest Valid Parentheses
- 🟡 🔴 LeetCode 134. Gas Station

## Greedy

- LeetCode 122. Best Time to Buy and Sell Stock II
- LeetCode 45. Jump Game II
- LeetCode 435. Non-overlapping Intervals
- 🟡 🔴 LeetCode 134. Gas Station

## Intervals

- LeetCode 435. Non-overlapping Intervals
- 🟡 LeetCode 763. Partition Labels

## Divide and Conquer

- LeetCode 218. The Skyline Problem
- LeetCode 190. Reverse Bits
- LeetCode 191. Number of 1 Bits
- 🟡 LeetCode 22. Generate Parentheses
- 🟢 🟡 LeetCode 50. Pow(x, n)
- 🟡 🔴 LeetCode 114. Flatten Binary Tree to Linked List
- 🟡 🔴 LeetCOde 148. Sort List

## Decrease and Conquer

- LeetCode 235. Lowest Common Ancestor of a Binary Search Tree
  - BST 順序剪枝 → 單一路徑搜尋 → 尾遞迴轉 iterative；時間 O(h)、輔助空間 O(1)。

## Union Find

## Topological Sort

- LeetCode 207. Course Schedule
- 🟡 LeetCode 310. Minimum Height Trees

## Prefix Sum / Running Sum

- LeetCode 238. Product of Array Except Self
- 🟡 🔴 LeetCode 134. Gas Station

## Bit Manipulation

- LeetCode 137. Single Number II
- LeetCode 191. Number of 1 Bits
- LeetCode 338. Counting Bits
  - Bit manipulation + bottom-up DP；移除最低位，或清除最低位的 1，重用較小數字的答案。

## State Compression through Bit Manipulation

- LeetCode 36. Valid Sudoku

## Sweep Line

## Graph Algorithms

- LeetCode 130. Surrounded Regions
- LeetCode 417. Pacific Atlantic Water Flow
- 🟡 🔴 LeetCode 399. Evaluate Division

## Tree Algorithms

- LeetCode 230. Kth Smallest Element in a BST

## Math & Number Theory

- LeetCode 7. Reverse Integer
- LeetCode 202. Happy Number
- LeetCode 168. Excel Sheet Column Title
- LeetCode 263. Ugly Number
- LeetCode 319. Bulb Switcher
- LeetCode 1925. Count Square Sum Triples
- 🟡 LeetCode 189. Rotate Array

## Sorting & Partition

- LeetCode 49. Group Anagrams

## String Matching

- LeetCode 28. Find the Index of the First Occurrence in a String

## String Manipulation

- LeetCode 8. String to Integer (atoi)
- LeetCode 13. Roman to Integer
- 🟡 🔴 LeetCode 43. Multiply Strings
  - Medium 偏難；反轉後按位累加乘積，再統一處理進位與前導零。
- LeetCode 165. Compare Version Numbers
- LeetCode 58. Length of Last Word

## Finite State Machine (FSM)

- 🟡 LeetCode 8. String to Integer (atoi)
  - 空白 → 可選符號 → 數字；解析階段決定下一個字元能否被接受。
- 🟡 LeetCode 54. Spiral Matrix
  - 方向是四種狀態；下一格越界或已走過時，轉到下一個方向。

## Stack Invariant Design (Monotonic)

- LeetCode 32. Longest Valid Parentheses
- LeetCode 402. Remove K Digits

## Trie

- LeetCode 421. Maximum XOR of Two Numbers in an Array
- 🟡 🔴 LeetCode 139. Word Break
- 🟡 LeetCode 211. Design Add and Search Words Data Structure

## Hashmap

- LeetCode 49. Group Anagrams
- LeetCode 36. Valid Sudoku
- LeetCode 424. Longest Repeating Character Replacement
- LeetCode 409. Longest Palindrome
- 🟡 LeetCode 981. Time Based Key-Value Store
- 🟢 🟡 LeetCode 73. Set Matrix Zeroes

## Mapping & Canonicalization

- LeetCode 205. Isomorphic Strings
  - 一對一映射（bijection）；也可比較字元的出現模式，或依首次出現順序正規化。

## Boyer-Moore Voting Algorithm

- LeetCode 229. Majority Element II

## Brute Force

- LeetCode 36. Valid Sudoku
- 🟡 🔴 LeetCode 567. Permutation in String

## Brainteaser

- LeetCode 319. Bulb Switcher
- 🟡 🔴 LeetCode 134. Gas Station

## Simulation

- LeetCode 409. Longest Palindrome

## Look Simple, Easy to Make Mistakes

- 🟢 🟡 LeetCode 73. Set Matrix Zeroes

---

## 🎯 Technique Integration

Problems that require integrating multiple advanced techniques. These are excellent for developing multi-dimensional problem-solving skills and understanding how different algorithmic paradigms synergize.

### Combined Techniques

- LeetCode 327. Count of Range Sum
  - Divide and Conquer + Prefix Sum + Merge Sort + Two Pointers
- LeetCode 212. Word Search II
  - Trie + Backtracking
- LeetCode 642. Design Search Autocomplete System
  - Trie + DFS + Priority Queue
- LeetCode 373. Find K Pairs with Smallest Sums
  - Merge K Sorted Lists + Priority Queue
- LeetCode 438. Find All Anagrams in a String
  - Sliding Window + Hashmap + matchedCount
- LeetCode 443. String Compression
  - Two Pointer + String Manipulation
- LeetCode 137. Single Number II
  - Bit Manipulation + Math + Bit Invaraint Design + State Machine
- LeetCode 424. Longest Repeating Character Replacement
  - Sliding Window + Hash Table + Greedy
- LeetCode 139. Word Break
  - 1-D DP (dp[length], look backward) + Hash Set / Trie
- 🟡 🔴 LeetCode 128. Longest Consecutive Sequence
  - Hashmap + Connected Component
- 🟡 🔴 LeetCode 114. Flatten Binary Tree to Linked List
  - Tree + Divide and Conquer
- 🟡 🔴 LeetCode 143. Reorder List
  - Middle Point + Rerverse + Merge
- 🟡 LeetCode 211. Design Add and Search Words Data Structure
  - Trie + DFS
- 🟡 🔴 LeetCode 399. Evaluate Division
  - DFS and Math
- 🟡 🔴 LeetCode 25. Reverse Nodes in k-Group
  - k-gap pointer and revese (hard to implement and easy to forget to update links)
- 🔴 🟡 LeetCode 124. Binary Tree Maximum Path Sum
  - Post-ordering + Tree Dynamic Programming

### Followup Possible (Multiple Solutions)

- LeetCode 45. Jump Game II
- LeetCode 137. Single Number II
- 🟡 🔴 LeetCode 128. Longest Consecutive Sequence
- LeetCode 1925. Count Square Sum Triples
- 🟡 LeetCode 981. Time Based Key-Value Store
- 🟡 LeetCode 494. Target Sum
- 🟡 🔴 LeetCode 567. Permutation in String
- 🟢 🟡 LeetCode 73. Set Matrix Zeroes
- 🟡 🔴 LeetCode 131. Palindrome Partitioning
- 🟡 🔴 LeetCode 134. Gas Station
- 🟡 LeetCode 678. Valid Parenthesis String
- 🟡 🔴 LeetCode 114. Flatten Binary Tree to Linked List
- 🟢 LeetCode 219. Contains Duplicate II
  - brute force -> hashmap -> sliding window
- 🟢 🟡 LeetCode 234. Palindrome Linked List
  - Time O(n) + Space O(1)
- 🟢 🟡 142. Linked List Cycle II
  - Time O(n) + Space O(1)
- 🟡 🔴 LeetCode 287. Find the Duplicate Number
  - Time O(n) + Space O(1)
- 🟡 LeetCode 189. Rotate Array
  - Reverse Trick
- 🟢 LeetCode 392. Is Subsequence

## LeetCode Solution Worth Reading

- LeetCode 137. Single Number II

## Gary's Choice

- LeetCode 424. Longest Repeating Character Replacement
- 🟡 LeetCode 494. Target Sum
- 🟡 🔴 LeetCode 567. Permutation in String
- 🟡 LeetCode 131. Palindrome Partitioning
- 🟡 LeetCode 417. Pacific Atlantic Water Flow
- 🟡 LeetCode 678. Valid Parenthesis String
- 🟡 🔴 LeetCode 114. Flatten Binary Tree to Linked List
- 🟡 🔴 LeetCode 124. Binary Tree Maximum Path Sum

## Classic Optimization / Brain Development

- 🔴 LeetCode 134. Gas Station
  - Greedy / Reset Argument / Running Sum
- 🟡 🔴 LeetCode 73. Set Matrix Zeroes
  - Space O(1)
- 🟢 🟡 142. Linked List Cycle II
  - Time O(n) + Space O(1)
- 🟡 🔴 287. Find the Duplicate Number
  - Based on LeetCode 142.
- 🟡 LeetCode 189. Rotate Array
