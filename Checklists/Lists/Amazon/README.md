# Amazon 練習總表

兩份來源清單的統一練習入口；按 LeetCode 題號去重，保留每題來源及 Explore 編輯標註。

**整理日期：2026-11-06｜共 105 題｜已刷：54 / 105**

## 來源

| 代號 | 清單 | 題數 | 獨有題數 |
|---|---|---:|---:|
| T | [Top Amazon Questions](Top_Questions.md) | 50 | 37 |
| E | [Amazon LeetCode Explore Editors Choice](Explore_Editors_Choice.md) | 68 | 55 |

兩份重疊 **13 題**，所以合併為 `50 + 68 − 13 = 105` 題。來源清單各自保留原本順序、分類、題目說明與出處。

## 練習優先序

1. **P0：OA 編輯標註**。先做尚無完成紀錄的 **819 → 937**，再限時複習 **1 → 5 → 973**。
2. **P1：分類介紹推薦**。補 387、273、121、957；此層是本次準備安排，不代表它們有 OA 標籤。
3. **P2：Phone**。103、200 有逐題編輯標註；215 只在分類介紹中被推薦為 phone 題。
4. **P3：Onsite**。42、138、146 有逐題編輯標註。
5. **P4：其他題型補強**。其餘依難度、是否已刷及題號排列。

優先序是依目前 OA 目標與練習紀錄安排，不是出題機率排名。Explore 未提供統計期間；`—` 表示沒有逐題階段標註，不表示不常考。章節整體建議仍見來源清單。

勾選及日期只依 [Practice Log](../../Practice_Log.md)，本表為 2026-11-06 快照，與兩份來源清單均未納入 `scripts/sync_lists.py` 的自動同步範圍。已刷不表示所有變體都已完成，也不表示已能限時重寫。

## 105 題去重總表

| 已刷 | 題目 | 難度 | 來源 | Explore 階段／推薦 | 優先序 | 完成日期 |
|:---:|---|---|---|---|:---:|:---:|
| [ ] | [819. Most Common Word](https://leetcode.com/problems/most-common-word/) | Easy | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2973/) | OA | P0 | — |
| [ ] | [937. Reorder Data in Log Files](https://leetcode.com/problems/reorder-data-in-log-files/) | Medium | [T](Top_Questions.md) + [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2974/) | OA | P0 | — |
| [x] | [1. Two Sum](https://leetcode.com/problems/two-sum/) | Easy | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/508/) | OA | P0 | 2026-09-04 |
| [x] | [5. Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/80/dynamic-programming/489/) | OA | P0 | 2026-09-05 |
| [x] | [973. K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | Medium | [T](Top_Questions.md) + [E](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/2996/) | OA | P0 | 2026-10-15 |
| [ ] | [387. First Unique Character in a String](https://leetcode.com/problems/first-unique-character-in-a-string/) | Easy | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/480/) | 分類推薦 | P1 | — |
| [ ] | [957. Prison Cells After N Days](https://leetcode.com/problems/prison-cells-after-n-days/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/82/others/3005/) | 分類推薦 | P1 | — |
| [x] | [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | [E](https://leetcode.com/explore/interview/card/amazon/80/dynamic-programming/505/) | 分類推薦 | P1 | 2026-09-05 |
| [x] | [273. Integer to English Words](https://leetcode.com/problems/integer-to-english-words/) | Hard | [T](Top_Questions.md) + [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/481/) | 分類推薦 | P1 | 2026-11-05 |
| [x] | [103. Binary Tree Zigzag Level Order Traversal](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2980/) | Phone | P2 | 2026-10-21 |
| [x] | [200. Number of Islands](https://leetcode.com/problems/number-of-islands/) | Medium | [T](Top_Questions.md) + [E](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/894/) | Phone | P2 | 2026-09-14 |
| [x] | [215. Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/482/) | Phone（分類介紹推薦） | P2 | 2026-09-21 |
| [x] | [42. Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Hard | [T](Top_Questions.md) + [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2975/) | Onsite | P3 | 2026-09-18 |
| [x] | [138. Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | Medium | [T](Top_Questions.md) + [E](https://leetcode.com/explore/interview/card/amazon/77/linked-list/2978/) | Onsite | P3 | 2026-09-21 |
| [x] | [146. LRU Cache](https://leetcode.com/problems/lru-cache/) | Medium | [T](Top_Questions.md) + [E](https://leetcode.com/explore/interview/card/amazon/81/design/478/) | Onsite | P3 | 2026-09-11 |
| [ ] | [1603. Design Parking System](https://leetcode.com/problems/design-parking-system/) | Easy | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [1710. Maximum Units on a Truck](https://leetcode.com/problems/maximum-units-on-a-truck/) | Easy | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2357. Make Array Zero by Subtracting Equal Amounts](https://leetcode.com/problems/make-array-zero-by-subtracting-equal-amounts/) | Easy | [T](Top_Questions.md) | — | P4 | — |
| [x] | [13. Roman to Integer](https://leetcode.com/problems/roman-to-integer/) | Easy | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2965/) | — | P4 | 2026-09-29 |
| [x] | [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Easy | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2972/) | — | P4 | 2026-09-04 |
| [x] | [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Easy | [E](https://leetcode.com/explore/interview/card/amazon/77/linked-list/2976/) | — | P4 | 2026-09-04 |
| [x] | [28. Find the Index of the First Occurrence in a String](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) | Easy | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2968/) | — | P4 | 2026-10-01 |
| [x] | [101. Symmetric Tree](https://leetcode.com/problems/symmetric-tree/) | Easy | [E](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/507/) | — | P4 | 2026-09-24 |
| [x] | [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Easy | [E](https://leetcode.com/explore/interview/card/amazon/77/linked-list/2979/) | — | P4 | 2026-09-16 |
| [x] | [268. Missing Number](https://leetcode.com/problems/missing-number/) | Easy | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2971/) | — | P4 | 2026-10-09 |
| [x] | [543. Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | Easy | [E](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2985/) | — | P4 | 2026-09-16 |
| [x] | [733. Flood Fill](https://leetcode.com/problems/flood-fill/) | Easy | [E](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2987/) | — | P4 | 2026-10-10 |
| [ ] | [16. 3Sum Closest](https://leetcode.com/problems/3sum-closest/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2967/) | — | P4 | — |
| [ ] | [48. Rotate Image](https://leetcode.com/problems/rotate-image/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2969/) | — | P4 | — |
| [ ] | [165. Compare Version Numbers](https://leetcode.com/problems/compare-version-numbers/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/502/) | — | P4 | — |
| [ ] | [176. Second Highest Salary](https://leetcode.com/problems/second-highest-salary/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/82/others/3003/) | — | P4 | — |
| [ ] | [253. Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) | Medium 🔒 | [T](Top_Questions.md) + [E](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/497/) | — | P4 | — |
| [ ] | [348. Design Tic-Tac-Toe](https://leetcode.com/problems/design-tic-tac-toe/) | Medium 🔒 | [T](Top_Questions.md) + [E](https://leetcode.com/explore/interview/card/amazon/81/design/517/) | — | P4 | — |
| [ ] | [767. Reorganize String](https://leetcode.com/problems/reorganize-string/) | Medium | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [863. All Nodes Distance K in Binary Tree](https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/) | Medium | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [1152. Analyze User Website Visit Pattern](https://leetcode.com/problems/analyze-user-website-visit-pattern/) | Medium 🔒 | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [1268. Search Suggestions System](https://leetcode.com/problems/search-suggestions-system/) | Medium | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [1291. Sequential Digits](https://leetcode.com/problems/sequential-digits/) | Medium | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [1567. Maximum Length of Subarray With Positive Product](https://leetcode.com/problems/maximum-length-of-subarray-with-positive-product/) | Medium | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [1628. Design an Expression Tree With Evaluate Function](https://leetcode.com/problems/design-an-expression-tree-with-evaluate-function/) | Medium 🔒 | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [1864. Minimum Number of Swaps to Make the Binary String Alternating](https://leetcode.com/problems/minimum-number-of-swaps-to-make-the-binary-string-alternating/) | Medium | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2055. Plates Between Candles](https://leetcode.com/problems/plates-between-candles/) | Medium | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2100. Find Good Days to Rob the Bank](https://leetcode.com/problems/find-good-days-to-rob-the-bank/) | Medium | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2104. Sum of Subarray Ranges](https://leetcode.com/problems/sum-of-subarray-ranges/) | Medium | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2214. Minimum Health to Beat Game](https://leetcode.com/problems/minimum-health-to-beat-game/) | Medium 🔒 | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2222. Number of Ways to Select Buildings](https://leetcode.com/problems/number-of-ways-to-select-buildings/) | Medium | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2268. Minimum Number of Keypresses](https://leetcode.com/problems/minimum-number-of-keypresses/) | Medium 🔒 | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2340. Minimum Adjacent Swaps to Make a Valid Array](https://leetcode.com/problems/minimum-adjacent-swaps-to-make-a-valid-array/) | Medium 🔒 | [T](Top_Questions.md) | — | P4 | — |
| [x] | [2. Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/77/linked-list/513/) | — | P4 | 2026-09-16 |
| [x] | [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2961/) | — | P4 | 2026-09-04 |
| [x] | [7. Reverse Integer](https://leetcode.com/problems/reverse-integer/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/82/others/3002/) | — | P4 | 2026-10-15 |
| [x] | [8. String to Integer (atoi)](https://leetcode.com/problems/string-to-integer-atoi/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2962/) | — | P4 | 2026-10-16 |
| [x] | [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2963/) | — | P4 | 2026-09-05 |
| [x] | [12. Integer to Roman](https://leetcode.com/problems/integer-to-roman/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2964/) | — | P4 | 2026-10-16 |
| [x] | [15. 3Sum](https://leetcode.com/problems/3sum/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2966/) | — | P4 | 2026-09-05 |
| [x] | [17. Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/84/recursion/521/) | — | P4 | 2026-09-07 |
| [x] | [22. Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/84/recursion/2988/) | — | P4 | 2026-09-17 |
| [x] | [33. Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/2992/) | — | P4 | 2026-09-07 |
| [x] | [49. Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Medium | [T](Top_Questions.md) + [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/2970/) | — | P4 | 2026-09-18 |
| [x] | [53. Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/80/dynamic-programming/899/) | — | P4 | 2026-09-07 |
| [x] | [56. Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/2993/) | — | P4 | 2026-09-10 |
| [x] | [79. Word Search](https://leetcode.com/problems/word-search/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/84/recursion/2989/) | — | P4 | 2026-09-10 |
| [x] | [98. Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/514/) | — | P4 | 2026-09-10 |
| [x] | [102. Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/506/) | — | P4 | 2026-09-10 |
| [x] | [139. Word Break](https://leetcode.com/problems/word-break/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/80/dynamic-programming/2997/) | — | P4 | 2026-09-11 |
| [x] | [155. Min Stack](https://leetcode.com/problems/min-stack/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/81/design/503/) | — | P4 | 2026-09-11 |
| [x] | [167. Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/2994/) | — | P4 | 2026-10-09 |
| [x] | [207. Course Schedule](https://leetcode.com/problems/course-schedule/) | Medium | [T](Top_Questions.md) + [E](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2983/) | — | P4 | 2026-09-14 |
| [x] | [236. Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2984/) | — | P4 | 2026-09-21 |
| [x] | [238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/499/) | — | P4 | 2026-09-15 |
| [x] | [322. Coin Change](https://leetcode.com/problems/coin-change/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/80/dynamic-programming/2998/) | — | P4 | 2026-09-15 |
| [x] | [347. Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/2995/) | — | P4 | 2026-10-11 |
| [x] | [545. Boundary of Binary Tree](https://leetcode.com/problems/boundary-of-binary-tree/) | Medium 🔒 | [T](Top_Questions.md) | — | P4 | 2026-11-05 |
| [x] | [763. Partition Labels](https://leetcode.com/problems/partition-labels/) | Medium | [E](https://leetcode.com/explore/interview/card/amazon/82/others/3004/) | — | P4 | 2026-10-15 |
| [x] | [994. Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | Medium | [T](Top_Questions.md) | — | P4 | 2026-09-22 |
| [x] | [2221. Find Triangular Sum of an Array](https://leetcode.com/problems/find-triangular-sum-of-an-array/) | Medium | [T](Top_Questions.md) | — | P4 | 2026-11-05 |
| [ ] | [126. Word Ladder II](https://leetcode.com/problems/word-ladder-ii/) | Hard | [E](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/483/) | — | P4 | — |
| [ ] | [127. Word Ladder](https://leetcode.com/problems/word-ladder/) | Hard | [T](Top_Questions.md) + [E](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2982/) | — | P4 | — |
| [ ] | [140. Word Break II](https://leetcode.com/problems/word-break-ii/) | Hard | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [212. Word Search II](https://leetcode.com/problems/word-search-ii/) | Hard | [E](https://leetcode.com/explore/interview/card/amazon/84/recursion/2990/) | — | P4 | — |
| [ ] | [239. Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | Hard | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [297. Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Hard | [E](https://leetcode.com/explore/interview/card/amazon/81/design/2999/) | — | P4 | — |
| [ ] | [472. Concatenated Words](https://leetcode.com/problems/concatenated-words/) | Hard | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [588. Design In-Memory File System](https://leetcode.com/problems/design-in-memory-file-system/) | Hard 🔒 | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [642. Design Search Autocomplete System](https://leetcode.com/problems/design-search-autocomplete-system/) | Hard 🔒 | [E](https://leetcode.com/explore/interview/card/amazon/81/design/3000/) | — | P4 | — |
| [ ] | [675. Cut Off Trees for Golf Event](https://leetcode.com/problems/cut-off-trees-for-golf-event/) | Hard | [E](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2986/) | — | P4 | — |
| [ ] | [719. Find K-th Smallest Pair Distance](https://leetcode.com/problems/find-k-th-smallest-pair-distance/) | Hard | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [818. Race Car](https://leetcode.com/problems/race-car/) | Hard | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [828. Count Unique Characters of All Substrings of a Given String](https://leetcode.com/problems/count-unique-characters-of-all-substrings-of-a-given-string/) | Hard | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [895. Maximum Frequency Stack](https://leetcode.com/problems/maximum-frequency-stack/) | Hard | [E](https://leetcode.com/explore/interview/card/amazon/81/design/3001/) | — | P4 | — |
| [ ] | [1597. Build Binary Expression Tree From Infix Expression](https://leetcode.com/problems/build-binary-expression-tree-from-infix-expression/) | Hard 🔒 | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2102. Sequentially Ordinal Rank Tracker](https://leetcode.com/problems/sequentially-ordinal-rank-tracker/) | Hard | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2193. Minimum Number of Moves to Make Palindrome](https://leetcode.com/problems/minimum-number-of-moves-to-make-palindrome/) | Hard | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2262. Total Appeal of A String](https://leetcode.com/problems/total-appeal-of-a-string/) | Hard | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2272. Substring With Largest Variance](https://leetcode.com/problems/substring-with-largest-variance/) | Hard | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2281. Sum of Total Strength of Wizards](https://leetcode.com/problems/sum-of-total-strength-of-wizards/) | Hard | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2355. Maximum Number of Books You Can Take](https://leetcode.com/problems/maximum-number-of-books-you-can-take/) | Hard 🔒 | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2386. Find the K-Sum of an Array](https://leetcode.com/problems/find-the-k-sum-of-an-array/) | Hard | [T](Top_Questions.md) | — | P4 | — |
| [ ] | [2398. Maximum Number of Robots Within Budget](https://leetcode.com/problems/maximum-number-of-robots-within-budget/) | Hard | [T](Top_Questions.md) | — | P4 | — |
| [x] | [4. Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Hard | [E](https://leetcode.com/explore/interview/card/amazon/79/sorting-and-searching/2991/) | — | P4 | 2026-10-12 |
| [x] | [23. Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | Hard | [E](https://leetcode.com/explore/interview/card/amazon/77/linked-list/512/) | — | P4 | 2026-09-15 |
| [x] | [25. Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) | Hard | [E](https://leetcode.com/explore/interview/card/amazon/77/linked-list/2977/) | — | P4 | 2026-10-19 |
| [x] | [76. Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Hard | [E](https://leetcode.com/explore/interview/card/amazon/76/array-and-strings/902/) | — | P4 | 2026-09-25 |
| [x] | [124. Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Hard | [E](https://leetcode.com/explore/interview/card/amazon/78/trees-and-graphs/2981/) | — | P4 | 2026-10-19 |
| [x] | [295. Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Hard | [T](Top_Questions.md) + [E](https://leetcode.com/explore/interview/card/amazon/81/design/495/) | — | P4 | 2026-09-27 |

## 維護方式

- 更新題庫時，先更新對應來源清單，再以題號合併；來源出現兩次仍只保留一列。
- 題目完成狀態依 Practice Log 核對；個別變體的重練仍留在 [Problem Review](../09_Problem_Review.md)。
- Explore 的 OA／Phone／Onsite 僅從原始逐題編輯標註帶入；分類介紹推薦另外標明，不自行補上階段。
