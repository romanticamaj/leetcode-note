# Essential Problems

**Gary Hsieh's Personal Collection**

A curated list of must-do problems that build core competencies. Completing these problems will significantly strengthen your problem-solving abilities.

## Binary Search

- LeetCode 153. Find Minimum in Rotated Sorted Array
- LeetCode 33. Search in Rotated Sorted Array
- 🟡 LeetCode 378. Kth Smallest Element in a Sorted Matrix
- 🟡 LeetCode 981. Time Based Key-Value Store
- 🟢 LeetCode 69. Sqrt(x)
- 🟢 🟡 LeetCode 162. Find Peak Element

## Binary Search on Value Space

- 🔴 LeetCode 4. Median of Two Sorted Arrays
- 🟡 🔴 LeetCode 222. Count Complete Tree Nodes
  - Tree Height + Search on Value + Bit Manipulation
- 🟡 LeetCode 875. Koko Eating Bananas

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
- 🟡 LeetCode 151. Reverse Words in a String

## Linked List

- 🟡 LeetCode 142. Linked List Cycle II
- 🟡 🔴 LeetCode 143. Reorder List
- 🟡 🔴 LeetCode 287. Find the Duplicate Number

## Sliding Window

- LeetCode 438. Find All Anagrams in a String
- LeetCode 424. Longest Repeating Character Replacement
- 🟡 🔴 LeetCode 567. Permutation in String
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
- 🟢 🟡 LeetCode 542. 01 Matrix
- 🔴 LeetCode 126. Word Ladder II
  - BFS + Distance-Constrained Predecessor DAG + Backtracking

## DFS (Depth-First Search)

## Dynamic Programming

- LeetCode 309. Best Time to Buy and Sell Stock with Cooldown
  - 多維／State Machine DP：日期 × 持股狀態；buy[i] 從 sell[i-2] 買入以滿足 cooldown，並與前一天持股狀態取 max。
- 🟡 🔴 LeetCode 221. Maximal Square
- LeetCode 72. Edit Distance
- 🟡 🔴 LeetCode 139. Word Break
- 🟡 LeetCode 22. Generate Parentheses
- 🟡 LeetCode 97. Interleaving String
- 🟡 🔴 LeetCode 152. Maximum Product Subarray
  - 需要特別設計的查表邏輯 (其實就是遞迴式的設計)
- 🟡 🔴 LeetCode 124. Binary Tree Maximum Path Sum
  - Tree DP
- 🟡 LeetCode 91. Decode Ways
  - bottom-up counting dynamic programming 不好寫
- 🔴 LeetCode 10. Regular Expression Matching
  - 光是 recursion 就超級難寫，關鍵是看 pattern 下一個字元，來決定當前要怎麼跳轉
  - 需要小心 string 走完，但是 pattern 還沒走完，要讓 pattern 走完
  - 程式碼很短，但是判斷式很複雜

## Knapsack DP / Value-Range DP

- 🟡 🔴 LeetCode 494. Target Sum
  - Counting Dynamic Programming，設計 value range 很難，但是 Top-Down DP 很直觀
- 🟡 LeetCode 416. Partition Equal Subset Sum
  - **必做、再做一次。0/1 Knapsack／Subset Sum 判定型**：先練固定 target 的原始子集和，再回來獨立推導等和分割。每個元素最多選一次；由選／不選的暴力搜尋，推導 `(index, remaining)` 的 memoization。見 [背包 DP 筆記](../../Algorithms/Dynamic_Programming/Problem_Types/Knapsack_DP.md)。
- 🟡 LeetCode 322. Coin Change
- 🟡 LeetCode 518. Coin Change II
  - **完全背包／組合計數**：以 `(coin index, remaining amount)` 為狀態的 top-down value-range DP；選取後保留 index，允許重複使用同面額，跳過才前進，避免重複計算排列。
  - 筆記：[Knapsack DP](../../Algorithms/Dynamic_Programming/Problem_Types/Knapsack_DP.md)、[Counting DP 的組合去重](../../Algorithms/Dynamic_Programming/Problem_Types/Counting_DP.md)。

## Kadane's Pattern DP

- LeetCode 53. Maximum Subarray
- LeetCode 32. Longest Valid Parentheses
- 🟡 🔴 LeetCode 134. Gas Station

## Greedy

- LeetCode 122. Best Time to Buy and Sell Stock II
- LeetCode 45. Jump Game II
- 🟢 🟡 LeetCode 435. Non-overlapping Intervals
- 🟡 🔴 LeetCode 134. Gas Station
- LeetCode 853. Car Fleet
  - Sorting + Greedy + Fleet Arrival Time
  - 以抵達時間取代連續移動模擬；依 position 由大到小處理，用一個抵達時間摘要前方車隊。後車單獨抵達時間 ≤ 前方車隊抵達時間時合併，並保留前方時間。

## Intervals

- 🟢 🟡 LeetCode 435. Non-overlapping Intervals
- 🟡 LeetCode 763. Partition Labels

## Divide and Conquer

- 🟢 🟡 LeetCode 427. Construct Quad Tree
  - 二維區域四分＋bottom-up 合併；練習 1×1 base case、閉區間切分、象限座標與節點生命週期。
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

- 🟡 LeetCode 684. Redundant Connection
  - 無向圖增量判環：加入邊前，若兩端已連通，該邊就閉合環。見 [Union-Find 推薦實作](../../Algorithms/Union_Find/06-Optimized_Implementation_and_Analysis.md)。
- 🟢 🟡 LeetCode 261. Graph Valid Tree
- 🟡 LeetCode 778. Swim in Rising Water

## Topological Sort

- LeetCode 207. Course Schedule
- 🟡 LeetCode 310. Minimum Height Trees
- 🔴 LeetCode 269. Alien Dictionary

## Prefix Sum / Running Sum

- LeetCode 238. Product of Array Except Self
- 🟡 🔴 LeetCode 134. Gas Station
- 🟡 🔴 LeetCode 560. Subarray Sum Equals K

## Bit Manipulation

- LeetCode 201. Bitwise AND of Numbers Range
  - 區間 bit pattern 與位移操作；目前暫停、尚未完成，補強二進位觀察後再獨立推導。
- 🟢 🟡 LeetCode 137. Single Number II
- LeetCode 191. Number of 1 Bits
- LeetCode 338. Counting Bits
  - Bit manipulation + bottom-up DP；移除最低位，或清除最低位的 1，重用較小數字的答案。
- 🟡 🔴 LeetCode 222. Count Complete Tree Nodes
  - Tree Height + Search on Value + Bit Manipulation
- 🟡 LeetCode 371. Sum of Two Integers
- 🟡 LeetCode 957. Prison Cells After N Days

## State Compression through Bit Manipulation

- LeetCode 36. Valid Sudoku

## Sweep Line

## Graph Algorithms

- LeetCode 130. Surrounded Regions
- LeetCode 417. Pacific Atlantic Water Flow
- 🟡 🔴 LeetCode 399. Evaluate Division
- 🟡 LeetCode 778. Swim in Rising Water
  - Connectivity with Constraint

## Tree Algorithms

- 🟡 🔴 LeetCode 117. Populating Next Right Pointers in Each Node II
  - Parent 更新 children 的 next；先右後左的遞迴依賴，同層鏈必須在使用前建立。
- LeetCode 230. Kth Smallest Element in a BST
- 🟡 🔴 LeetCode 297. Serialize and Deserialize Binary Tree
  - preordering + parenthesis count

## Math & Number Theory

- LeetCode 7. Reverse Integer
- LeetCode 202. Happy Number
- LeetCode 168. Excel Sheet Column Title
- LeetCode 263. Ugly Number
- LeetCode 319. Bulb Switcher
- LeetCode 1925. Count Square Sum Triples
- 🟡 LeetCode 189. Rotate Array
- 🟡 LeetCode 380. Insert Delete GetRandom O(1)

## Sorting & Partition

- LeetCode 49. Group Anagrams
- 🟢 🟡 LeetCode 274. H-Index
  - Naive 是 Sorting; 頻率桶 + suffix sum

## String Matching

- LeetCode 28. Find the Index of the First Occurrence in a String
- 🟡 LeetCode 394. Decode String
  - Stack + Finite State Machine

## String Manipulation

- LeetCode 8. String to Integer (atoi)
- LeetCode 13. Roman to Integer
- 🟡 🔴 LeetCode 43. Multiply Strings
  - 反轉後按位累加乘積，再統一處理進位與前導零。
- LeetCode 165. Compare Version Numbers
- LeetCode 58. Length of Last Word
- 🟡 LeetCode 151. Reverse Words in a String
  - Two Pointers + In-place + Reverse
- 🟢 LeetCode 819. Most Common Word
- 🔴 LeetCode 269. Alien Dictionary
- 🔴 🟡 LeetCode 224. Basic Calculator

## Finite State Machine (FSM)

- 🟡 LeetCode 8. String to Integer (atoi)
  - 空白 → 可選符號 → 數字；解析階段決定下一個字元能否被接受。
- 🟡 LeetCode 54. Spiral Matrix
  - 方向是四種狀態；下一格越界或已走過時，轉到下一個方向。
- 🟡 LeetCode 394. Decode String
  - Stack + Finite State Machine

### 數值門檻驅動的分段轉換（Phase-based Simulation）

共通心法：**依數值門檻選適用單位 → 輸出對應字串 → 消耗數值 → 處理剩餘部分**。將目前單位／數值區間視為控制階段，以有序 mapping 取代大量散落的判斷式；這裡練習的是 FSM 式控制流程，數值分解與查表負責各階段的轉換。

- 🟡 LeetCode 12. [Integer to Roman](https://leetcode.com/problems/integer-to-roman/)
  - 合法面額由大到小排列，包含 `900/400/90/40/9/4`；選目前最大的可扣面額，接上符號並扣減，直到剩餘值為 0。
- 🔴 LeetCode 273. [Integer to English Words](https://leetcode.com/problems/integer-to-english-words/)
  - 同樣依門檻選規則；大單位先轉換商再接單位字串，接著處理餘數。也可每三位一組，共用 `1..999` 的轉換規則，再接 Thousand／Million／Billion。
  - 邊界重點：整體 `0`、空的三位組、`10..19` 特例與空白；本題輸入上限只需處理到 Billion。

## Priority Queue

- 🟡 LeetCode 355. Design Twitter
  - Top-k：用固定大小 min-heap 維持最新 10 則，超過容量時淘汰最舊者；取出後反轉成由新到舊。另可用 max-heap 做 k-way merge，兩者的 heap 語義不同。

### K-way Merge（多路合併）

概念整理：[K-way Merge／Heap Frontier](../../Meta_Frameworks/State_Transition_Algorithm_Atlas.md#merge-k)。
演算法推導與文獻歷史：[373：K-way Merge 與外部排序](../../Problem_History/LC_0373_Find_K_Pairs_with_Smallest_Sums.md)。

- 🟡 LeetCode 373. Find K Pairs with Smallest Sums
  - **隱式有序序列的合併**：固定 i，(i,0)、(i,1)…的總和非遞減；min-heap 只保留每列尚未取出的第一組，取出 (i,j) 後補 (i,j+1)，不必先生成全部 m\*n 組配對。
  - 相關題：23. Merge k Sorted Lists（直接合併有序串列）、355. Design Twitter（各作者依時間排序，用 max-heap 合併最新候選；此版本仍待練習）。既有參考：[Heap 使用場景](../../Data_Structures/Heaps/01-Heap_Decision_Making.md)。

## Stack Operations

- 🟡 LeetCode 394. Decode String
  - 巢狀上下文的保存與恢復、sentinel 邊界、片段彈出與合併順序；注意字串組合成本。

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
- 🔴 LeetCode 424. Longest Repeating Character Replacement
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

## Cycle Detection

- 🟡 LeetCode 957. Prison Cells After N Days
  - Simulation + Cycle Detection + Fast Forwarding

## Look Simple, Easy to Make Mistakes

- 🟢 🟡 LeetCode 73. Set Matrix Zeroes

## Design

- 🔴 895. Maximum Frequency Stack
  - O(1) push and pop

## Extreme Edge Case

- 🟡 🔴 LeetCode 65. Valid Number

---

## 🎯 Technique Integration

Problems that require integrating multiple advanced techniques. These are excellent for developing multi-dimensional problem-solving skills and understanding how different algorithmic paradigms synergize.

### Combined Techniques

- 🟡 🔴 LeetCode 117. Populating Next Right Pointers in Each Node II
  - Tree DFS + Linked List Traversal + Invariant；沿 parent 的 next 鏈尋找下一個 child，right-first preorder 確保跨子樹鏈已備妥。
- LeetCode 327. Count of Range Sum
  - Divide and Conquer + Prefix Sum + Merge Sort + Two Pointers
- 🔴 LeetCode 212. Word Search II
  - Dynamic Trie + Backtracking
- LeetCode 642. Design Search Autocomplete System
  - Trie + DFS + Priority Queue
- LeetCode 373. Find K Pairs with Smallest Sums
  - K-way Merge + Priority Queue：將配對空間拆成多條隱式有序序列，見上方 K-way Merge 分類。
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
- 🟡 🔴 LeetCode 15. 3Sum
  - sort + hashmap or sort + two-pointer
- 🟡 🔴 LeetCode 560. Subarray Sum Equals K
  - Prefix Sum + Running Hashmap
- 🟡 🔴 LeetCode 222. Count Complete Tree Nodes
  - Tree Height + Search on Value + Bit Manipulation
- 🟡 🔴 LeetCode 437. Path Sum III
  - Preordering Recursion + Prefix Sum + Running Sum
- 🔴 LeetCode 126. Word Ladder II
  - BFS + Distance-Constrained Predecessor DAG + Backtracking
- 🟡 🔴 LeetCode 918. Maximum Sum Circular Subarray
  - Kadane's Algorithm + Prefix Sum + Suffix Maximum
- 🔴 LeetCode 269. Alien Dictionary
  - String Manipulation + Topological Sort
- 🔴 🟡 LeetCode 224. Basic Calculator
  - String Manipulation + State Design + Recursion

### Followup Possible (Multiple Solutions)

- LeetCode 45. Jump Game II
- 🟢 🟡 LeetCode 137. Single Number II
- 🟡 🔴 LeetCode 128. Longest Consecutive Sequence
- LeetCode 1925. Count Square Sum Triples
- 🟡 LeetCode 981. Time Based Key-Value Store
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
- 🟡 🔴 LeetCode 15. 3Sum
- 🟢 🟡 LeetCode 120. Triangle
  - Dynamic Programing with different space tradeoff
- 🟢 🟡 LeetCode 279. Perfect Squares
  - Value-Range DP or BFS
- 🟡 🔴 LeetCode 222. Count Complete Tree Nodes
  - Tree Height + Search on Value + Bit Manipulation

## LeetCode Solution Worth Reading

- LeetCode 137. Single Number II

## Gary's Choice

- 🟡 LeetCode 221. Maximal Square
- 🟡 🔴 LeetCode 117. Populating Next Right Pointers in Each Node II
- LeetCode 424. Longest Repeating Character Replacement
- 🟡 🔴 LeetCode 494. Target Sum
- 🟡 🔴 LeetCode 567. Permutation in String
- 🟡 LeetCode 131. Palindrome Partitioning
- 🟡 LeetCode 417. Pacific Atlantic Water Flow
- 🟡 LeetCode 678. Valid Parenthesis String
- 🟡 🔴 LeetCode 114. Flatten Binary Tree to Linked List
- 🟡 🔴 LeetCode 124. Binary Tree Maximum Path Sum
- 🟡 🔴 LeetCode 15. 3Sum
- 🟡 LeetCode 151. Reverse Words in a String
- 🟡 🔴 LeetCode 222. Count Complete Tree Nodes
  - Tree Height + Search on Value + Bit Manipulation
- 🟡 LeetCode 371. Sum of Two Integers
- 🟡 🔴 LeetCode 297. Serialize and Deserialize Binary Tree
  - preordering + parenthesis count
- 🔴 LeetCode 212. Word Search II
  - Dynamic Trie + Backtracking
- 🟡 LeetCode 957. Prison Cells After N Days
  - Simulation + Cycle Detection + Fast Forwarding
- 🟡 🔴 LeetCode 918. Maximum Sum Circular Subarray
  - Kadane's Algorithm + Prefix Sum + Suffix Maximum

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
- 🟡 🔴 LeetCode 15. 3Sum
- 🟢 🟡 LeetCode 162. Find Peak Element
