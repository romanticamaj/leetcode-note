# 刷題日誌

---

## 2026-09-07

- 15. 3Sum（重做，通過 — running hash map）
- 17. Letter Combinations of a Phone Number
- 33. Search in Rotated Sorted Array

**心得**：
- 15：我個人覺得是 medium 到 hard。思路一開始是先處理 duplicate，用 sort 解決之後，開始想 loop iterate (i, j) 這個 pair、再去找對應的 k。直覺是放一個 cache 做快速查找，但發現 hash map 一直沒辦法很好地建構出來，特別是去掉重複出現的 index 這部分，就是 build 不出來。
- 15（第二次）：用 running hash map 做出來了。關鍵是透過 sort 去 eliminate output duplicate。running hash map 的關鍵是：candidate 一路往下找，最後那個補數用 hash map 來記 — 但它不是往後找，是找**前面曾經看過的**；沒有的話就繼續往下，而當下 traverse 到的那個人，就成為 running hash map 裡「曾經出現過」的項目。
  ```
  // [i, ...., j, ...]
  //      *      <- 往前找有沒有出現過可用的人，有就把它當 k 取出來
  ```
  再過幾天要回來用 2-pointer 再做一次，也要熟悉「running hash map 是查看當前，然後它成為下一個 candidate 可查找的項目」這個核心概念。
- 17：大概沒什麼問題，就想到 backtracking。不小心又把 const 的 `unordered_map` 忘記用 `.at()` 存取，這樣 compile 會有問題。
- 33：已經做了蠻多次，每次都還是錯得一塌糊塗。這次的關鍵點在於，它確實會有一個 inflection point，但用 inflection point 去切出左半跟右半其實很沒有效率。更直覺的做法是看哪一半是 normal sorted，然後去 sorted 的那一半裡找：在裡面就往那個方向前進；沒有的話就直接把另外一半 prune 掉。所以應該是判斷哪一半 sorted → 往 sorted 那半前進，其餘 prune。

**LLM 點評**：
model: Fable 5.1
- 15：hash map build 不出來，是因為方向選錯，不是 dedup 沒做好。「固定 (i, j)、用 map 找 k」在 2Sum 可行是因為它回傳 index 且只要一組；3Sum 回傳**值**、要**所有不重複組合**，map 這條路要同時處理「k 的 index ≠ i, j」和「值重複」，天生就髒。排序後的標準解只用一個 outer loop：固定 i，剩下區間用對向雙指針找 j, k — 就是 LC 11 那個 greedy 淘汰（`sum < 0` 丟左、`sum > 0` 丟右）。排序的價值不只是 dedup，**它讓 two pointer 成立**，所以 map 根本不需要；dedup 只剩三處 `while (nums[x] == nums[x-1]) skip`。看 `K-Sum_Problems/02-Three_Sum.md` 後重寫，通過後 16、18 是同一個模板。
- 15（第二次）：你做出來的就是「固定 i，內層跑 Two Sum I（seen-set）」— 「往前找曾經看過的」正是 LC 1 的 seen-set 概念，只是把 target 換成 `-nums[i]`，所以 hash map 其實是內層 2Sum 的 cache，不是 3Sum 層級的。它和 two-pointer 一樣 O(N²)，差別在 dedup：two-pointer 靠有序跳過三處相同值就乾淨；seen-set 版要在 i 跳重複 + 內層用 set 收 (j, k) 值對，比較容易漏。二刷時兩種都寫，重點感受「排序讓 two-pointer 成立」這件事。
- 17：queue（BFS）版不用另外寫。它和 backtracking 是同一棵 state space tree 的 BFS / DFS 兩種走法，沒有新的設計決策，面試也極少追問（這題的 follow-up 通常是 digits 為空、或 mapping 動態給定）。真正值得留意的是這題把 backtracking 的三要素展示得很乾淨：path、candidates 由 `digits[depth]` 決定、terminate 在 `depth == digits.size()`。`const` map 用 `.at()` 這個坑 repo 已有：`CPP_Reference/Container/Const_Map_and_Operator_Bracket.md`。
- 33：你這次抓到的判準是對的，而且它和 153 是**兩種不同的 binary search**，混用就是你一直錯的原因。153 找 inflection point，predicate 是 `nums[m] > nums[r]`（跟右端比）；33 不找 inflection，每輪只問「`[l, m]` 是否 sorted」（`nums[l] <= nums[m]`），sorted 那半可以用普通 range check 決定 target 在不在，不在就整半 prune。**是「兩段 binary search」壓成一段**，不是「先找 pivot 再二分」。注意 `<=` 而非 `<`：`l == m` 時單元素也算 sorted，否則會漏。repo 的 `07-Inflection_Point_Binary_Search.md` 目前只收 153 / 162，這個「找 sorted 半邊」的 predicate 還沒寫進去，值得補一段對照。

---

## 2026-09-05

- 104. Maximum Depth of Binary Tree
- 121. Best Time to Buy and Sell Stock
- 141. Linked List Cycle
- 226. Invert Binary Tree
- 5. Longest Palindromic Substring
- 11. Container With Most Water
- 15. 3Sum（未通過）

**心得**：
- 104：recursive tree DP 可以秒殺，但是要練習 followup iterative 版本
- 121：標記是 easy，但感覺解題難度是 medium。以前是用 Bottom-up DP 設計 buying / selling 兩個狀態，再推導到 Kadane's；這次直接做出類似 Kadane's 的解法，反而看不懂為什麼 Bottom-up DP 是有辦法想出來的，它其實蠻複雜的
- 226：同 104，迭代版待補
- 5：我感覺是 medium 到 hard，因為必須從 DP 突破，要設計的東西滿多的。DP 設計有一個大關鍵是 table 的 traverse 方向。目前這一塊比較弱，如果可以把 table traverse 的方向很快地透過 index 的 loop 建構好，解題才會相對容易，特別注意 index 的邊界。我認為這是 Array 底層 traverse 方向設計的能力之一，它直接影響 DP 的解題效率。另外，有人會把 base case 或需要邊界判斷的條件都拉成 base case 一起處理掉，程式碼就會比較乾淨。所以遇到子問題的合法性需要多判斷時，可以考慮用邊界 case 直接處理掉，讓子問題不會碰到邊界、還要去判斷數值的情況。
- 11：一看到題目直覺是 divide and conquer，可能被 container 類的裝水題影響了，但很明顯這個方向不對。看了提示後知道是 two pointer，只要把 move 策略定好解法就出來了。可是我還沒辦法連結，為什麼可以把 O(N²) 透過這種 two pointer greedy 降到 O(N)？
- 15：有做但失敗了，沒有成功處理 duplicate 的問題。跟 Gemini 討論後，這類「回傳結果不能有 duplicate」的切入點通常都是排序。更大的問題是沒有馬上釐清輸入與輸出的格式：這次一直把輸出誤會成 index，到最後才發現是「值」，而「值」沒辦法直接對應到重複的項目，這才是最大的問題。如果一開始就發現，切入方向也許就對了。

---

## 2026-09-04

- 1. Two Sum
- 3. Longest Substring Without Repeating Characters
- 20. Valid Parentheses
- 21. Merge Two Sorted Lists
- 70. Climbing Stairs

**心得**：
