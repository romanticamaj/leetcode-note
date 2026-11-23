# Amazon LeetCode Explore Editors Choice

來源：[LeetCode Explore — Top Questions from Amazon](https://leetcode.com/explore/interview/card/amazon/)。

**來源查閱日期：2026-11-06｜8 個分類、68 題｜13 Easy、40 Medium、15 Hard**

依 Explore 原始分類與順序收錄。題型為整理用標籤，可包含不同解法；面試階段依原頁編輯標註，不代表近期出題頻率。

- **OA**：Online Assessment，共 5 題。
- **Phone**：Phone Interview，共 2 題；另有 215 的分類介紹推薦。
- **Onsite**：Onsite Interview，共 3 題。
- **—**：未見逐題面試階段標註。🔒 表示 Premium 題目。

## 面試階段索引

### OA

| 題目 | 難度 | 題型 | 標註依據 | 來源 |
|---|---|---|---|---|
| [1. Two Sum](https://leetcode.com/problems/two-sum/) | Easy | Hash Map | Editors Choice | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/508/) |
| [819. Most Common Word](https://leetcode.com/problems/most-common-word/) | Easy | Tokenization + Frequency Counting | Editors Choice | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2973/) |
| [937. Reorder Data in Log Files](https://leetcode.com/problems/reorder-data-in-log-files/) | Medium | Custom Sorting | Editors Choice | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2974/) |
| [973. K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | Medium | Top-K Selection + Squared Distance | Editors Choice | [Explore](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/2996/) |
| [5. Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Medium | Palindrome Expansion / DP | Editors Choice | [Explore](https://leetcode.com/explore/interview/card/amazon/80/dynamic-programming/489/) |

### Phone

| 題目 | 難度 | 題型 | 標註依據 | 來源 |
|---|---|---|---|---|
| [103. Binary Tree Zigzag Level Order Traversal](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) | Medium | BFS + Zigzag Level Order | Editors Choice | [Explore](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2980/) |
| [200. Number of Islands](https://leetcode.com/problems/number-of-islands/) | Medium | Grid + Connected Components | Editors Choice | [Explore](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/894/) |
| [215. Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Medium | Quickselect / Heap | 分類介紹推薦 | [Explore](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/482/) |

### Onsite

| 題目 | 難度 | 題型 | 標註依據 | 來源 |
|---|---|---|---|---|
| [42. Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Hard | Two Pointers / Monotonic Stack | Editors Choice | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2975/) |
| [138. Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | Medium | Linked List + Hash Map / Interleaving | Editors Choice | [Explore](https://leetcode.com/explore/interview/card/amazon/77/linked-list/2978/) |
| [146. LRU Cache](https://leetcode.com/problems/lru-cache/) | Medium | Hash Map + Doubly Linked List | Editors Choice | [Explore](https://leetcode.com/explore/interview/card/amazon/81/design/478/) |

## 題目分類

### Arrays and Strings（21 題）

[原始分類](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/)

| 題目 | 難度 | 題型 | 面試階段 | 來源 | 備註 |
|---|---|---|---|---|---|
| [1. Two Sum](https://leetcode.com/problems/two-sum/) | Easy | Hash Map | OA | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/508/) | — |
| [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | Sliding Window | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2961/) | — |
| [8. String to Integer (atoi)](https://leetcode.com/problems/string-to-integer-atoi/) | Medium | String Parsing | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2962/) | — |
| [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Medium | Two Pointers | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2963/) | — |
| [12. Integer to Roman](https://leetcode.com/problems/integer-to-roman/) | Medium | Greedy + Symbol Mapping | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2964/) | — |
| [13. Roman to Integer](https://leetcode.com/problems/roman-to-integer/) | Easy | String Parsing + Symbol Mapping | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2965/) | — |
| [15. 3Sum](https://leetcode.com/problems/3sum/) | Medium | Sorting + Two Pointers | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2966/) | — |
| [16. 3Sum Closest](https://leetcode.com/problems/3sum-closest/) | Medium | Sorting + Two Pointers | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2967/) | — |
| [28. Find the Index of the First Occurrence in a String](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) | Easy | String Matching | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2968/) | Explore 題名：Implement strStr() |
| [48. Rotate Image](https://leetcode.com/problems/rotate-image/) | Medium | Matrix Rotation | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2969/) | — |
| [49. Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Medium | Hash Map + Anagram Signature | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2970/) | — |
| [76. Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Hard | Sliding Window + Frequency Counting | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/902/) | — |
| [165. Compare Version Numbers](https://leetcode.com/problems/compare-version-numbers/) | Medium | String Parsing + Two Pointers | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/502/) | — |
| [238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Medium | Prefix/Suffix Products | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/499/) | — |
| [268. Missing Number](https://leetcode.com/problems/missing-number/) | Easy | XOR / Arithmetic Sum | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2971/) | — |
| [273. Integer to English Words](https://leetcode.com/problems/integer-to-english-words/) | Hard | Number Decomposition + String Construction | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/481/) | — |
| [387. First Unique Character in a String](https://leetcode.com/problems/first-unique-character-in-a-string/) | Easy | Frequency Counting | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/480/) | — |
| [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Easy | Stack | — | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2972/) | — |
| [819. Most Common Word](https://leetcode.com/problems/most-common-word/) | Easy | Tokenization + Frequency Counting | OA | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2973/) | — |
| [937. Reorder Data in Log Files](https://leetcode.com/problems/reorder-data-in-log-files/) | Medium | Custom Sorting | OA | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2974/) | Explore 題名：Reorder Log Files |
| [42. Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Hard | Two Pointers / Monotonic Stack | Onsite | [Explore](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2975/) | — |

### Linked Lists（6 題）

[原始分類](https://leetcode.com/explore/interview/card/amazon/77/linked-list/)

| 題目 | 難度 | 題型 | 面試階段 | 來源 | 備註 |
|---|---|---|---|---|---|
| [2. Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | Medium | Linked List + Carry Simulation | — | [Explore](https://leetcode.com/explore/interview/card/amazon/77/linked-list/513/) | — |
| [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Easy | Linked List Merge | — | [Explore](https://leetcode.com/explore/interview/card/amazon/77/linked-list/2976/) | — |
| [25. Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) | Hard | Linked List + Group Reversal | — | [Explore](https://leetcode.com/explore/interview/card/amazon/77/linked-list/2977/) | — |
| [138. Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | Medium | Linked List + Hash Map / Interleaving | Onsite | [Explore](https://leetcode.com/explore/interview/card/amazon/77/linked-list/2978/) | — |
| [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Easy | Linked List Reversal | — | [Explore](https://leetcode.com/explore/interview/card/amazon/77/linked-list/2979/) | — |
| [23. Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | Hard | Min-Heap / Divide and Conquer | — | [Explore](https://leetcode.com/explore/interview/card/amazon/77/linked-list/512/) | — |

### Trees and Graphs（13 題）

[原始分類](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/)

| 題目 | 難度 | 題型 | 面試階段 | 來源 | 備註 |
|---|---|---|---|---|---|
| [98. Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | Medium | BST + Bound Propagation | — | [Explore](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/514/) | — |
| [101. Symmetric Tree](https://leetcode.com/problems/symmetric-tree/) | Easy | Tree + Symmetry Check | — | [Explore](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/507/) | — |
| [102. Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | Medium | BFS + Level Order Traversal | — | [Explore](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/506/) | — |
| [103. Binary Tree Zigzag Level Order Traversal](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) | Medium | BFS + Zigzag Level Order | Phone | [Explore](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2980/) | — |
| [124. Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Hard | Tree DP + Path Gain | — | [Explore](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2981/) | — |
| [126. Word Ladder II](https://leetcode.com/problems/word-ladder-ii/) | Hard | BFS + Predecessor DAG + Backtracking | — | [Explore](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/483/) | — |
| [127. Word Ladder](https://leetcode.com/problems/word-ladder/) | Hard | BFS + Shortest Path | — | [Explore](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2982/) | — |
| [200. Number of Islands](https://leetcode.com/problems/number-of-islands/) | Medium | Grid + Connected Components | Phone | [Explore](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/894/) | — |
| [207. Course Schedule](https://leetcode.com/problems/course-schedule/) | Medium | Topological Sort + Cycle Detection | — | [Explore](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2983/) | — |
| [236. Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | Medium | Tree + Lowest Common Ancestor | — | [Explore](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2984/) | — |
| [543. Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | Easy | Tree DFS + Height Aggregation | — | [Explore](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2985/) | — |
| [675. Cut Off Trees for Golf Event](https://leetcode.com/problems/cut-off-trees-for-golf-event/) | Hard | Repeated BFS + Height Ordering | — | [Explore](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2986/) | — |
| [733. Flood Fill](https://leetcode.com/problems/flood-fill/) | Easy | Grid + Flood Fill | — | [Explore](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2987/) | — |

### Recursion（4 題）

[原始分類](https://leetcode.com/explore/interview/card/amazon/84/recursion/)

| 題目 | 難度 | 題型 | 面試階段 | 來源 | 備註 |
|---|---|---|---|---|---|
| [17. Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | Medium | Backtracking + Cartesian Product | — | [Explore](https://leetcode.com/explore/interview/card/amazon/84/recursion/521/) | — |
| [22. Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | Medium | Backtracking + Prefix Constraints | — | [Explore](https://leetcode.com/explore/interview/card/amazon/84/recursion/2988/) | — |
| [79. Word Search](https://leetcode.com/problems/word-search/) | Medium | Grid DFS + Backtracking | — | [Explore](https://leetcode.com/explore/interview/card/amazon/84/recursion/2989/) | — |
| [212. Word Search II](https://leetcode.com/problems/word-search-ii/) | Hard | Trie + Grid DFS + Backtracking | — | [Explore](https://leetcode.com/explore/interview/card/amazon/84/recursion/2990/) | — |

### Sorting and Searching（8 題）

[原始分類](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/)

| 題目 | 難度 | 題型 | 面試階段 | 來源 | 備註 |
|---|---|---|---|---|---|
| [4. Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Hard | Binary Search + Partition | — | [Explore](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/2991/) | — |
| [33. Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | Binary Search + Sorted-Half Detection | — | [Explore](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/2992/) | — |
| [56. Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Medium | Sorting + Interval Merge | — | [Explore](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/2993/) | — |
| [167. Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Medium | Two Pointers | — | [Explore](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/2994/) | Explore 題名：Two Sum II - Input array is sorted |
| [215. Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Medium | Quickselect / Heap | Phone（分類介紹推薦） | [Explore](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/482/) | — |
| [253. Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) | Medium 🔒 | Min-Heap / Sweep Line | — | [Explore](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/497/) | — |
| [347. Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Medium | Frequency Counting + Top-K Selection | — | [Explore](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/2995/) | — |
| [973. K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | Medium | Top-K Selection + Squared Distance | OA | [Explore](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/2996/) | — |

### Dynamic Programming（5 題）

[原始分類](https://leetcode.com/explore/interview/card/amazon/80/dynamic-programming/)

| 題目 | 難度 | 題型 | 面試階段 | 來源 | 備註 |
|---|---|---|---|---|---|
| [5. Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Medium | Palindrome Expansion / DP | OA | [Explore](https://leetcode.com/explore/interview/card/amazon/80/dynamic-programming/489/) | — |
| [53. Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | Medium | Kadane’s Algorithm | — | [Explore](https://leetcode.com/explore/interview/card/amazon/80/dynamic-programming/899/) | — |
| [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | Running Minimum + Maximum Profit | — | [Explore](https://leetcode.com/explore/interview/card/amazon/80/dynamic-programming/505/) | — |
| [139. Word Break](https://leetcode.com/problems/word-break/) | Medium | DP + Word Segmentation | — | [Explore](https://leetcode.com/explore/interview/card/amazon/80/dynamic-programming/2997/) | — |
| [322. Coin Change](https://leetcode.com/problems/coin-change/) | Medium | DP + Unbounded Knapsack | — | [Explore](https://leetcode.com/explore/interview/card/amazon/80/dynamic-programming/2998/) | — |

### Design（7 題）

[原始分類](https://leetcode.com/explore/interview/card/amazon/81/design/)

| 題目 | 難度 | 題型 | 面試階段 | 來源 | 備註 |
|---|---|---|---|---|---|
| [146. LRU Cache](https://leetcode.com/problems/lru-cache/) | Medium | Hash Map + Doubly Linked List | Onsite | [Explore](https://leetcode.com/explore/interview/card/amazon/81/design/478/) | — |
| [155. Min Stack](https://leetcode.com/problems/min-stack/) | Medium | Stack + Minimum Tracking | — | [Explore](https://leetcode.com/explore/interview/card/amazon/81/design/503/) | — |
| [295. Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Hard | Two Heaps | — | [Explore](https://leetcode.com/explore/interview/card/amazon/81/design/495/) | — |
| [297. Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Hard | Tree Serialization + Parsing | — | [Explore](https://leetcode.com/explore/interview/card/amazon/81/design/2999/) | — |
| [348. Design Tic-Tac-Toe](https://leetcode.com/problems/design-tic-tac-toe/) | Medium 🔒 | Row/Column/Diagonal Counters | — | [Explore](https://leetcode.com/explore/interview/card/amazon/81/design/517/) | — |
| [642. Design Search Autocomplete System](https://leetcode.com/problems/design-search-autocomplete-system/) | Hard 🔒 | Trie + Frequency Tracking + Top-K Suggestions | — | [Explore](https://leetcode.com/explore/interview/card/amazon/81/design/3000/) | — |
| [895. Maximum Frequency Stack](https://leetcode.com/problems/maximum-frequency-stack/) | Hard | Frequency Map + Frequency-Grouped Stacks | — | [Explore](https://leetcode.com/explore/interview/card/amazon/81/design/3001/) | — |

### Others（4 題）

[原始分類](https://leetcode.com/explore/interview/card/amazon/82/others/)

| 題目 | 難度 | 題型 | 面試階段 | 來源 | 備註 |
|---|---|---|---|---|---|
| [7. Reverse Integer](https://leetcode.com/problems/reverse-integer/) | Medium | Digit Manipulation + Overflow Check | — | [Explore](https://leetcode.com/explore/interview/card/amazon/82/others/3002/) | — |
| [176. Second Highest Salary](https://leetcode.com/problems/second-highest-salary/) | Medium | SQL + Distinct Ranking | — | [Explore](https://leetcode.com/explore/interview/card/amazon/82/others/3003/) | — |
| [763. Partition Labels](https://leetcode.com/problems/partition-labels/) | Medium | Greedy + Last Occurrence | — | [Explore](https://leetcode.com/explore/interview/card/amazon/82/others/3004/) | — |
| [957. Prison Cells After N Days](https://leetcode.com/problems/prison-cells-after-n-days/) | Medium | Simulation + Cycle Detection + Fast Forwarding | — | [Explore](https://leetcode.com/explore/interview/card/amazon/82/others/3005/) | — |

## 分類介紹推薦

以下保留 Explore 分類介紹中的推薦，與逐題 Editors Choice 標註分開記錄。

| 分類 | 推薦內容 |
|---|---|
| Arrays and Strings | 387. First Unique Character in a String、273. Integer to English Words |
| Linked Lists | 該分類全部題目 |
| Trees and Graphs | 200. Number of Islands |
| Recursion | 該分類全部題目 |
| Sorting and Searching | 215. Kth Largest Element in an Array（Phone Interview） |
| Dynamic Programming | 121. Best Time to Buy and Sell Stock |
| Design | 146. LRU Cache |
| Others | 957. Prison Cells After N Days |
