# 刷題日誌

---

## 2026-09-10

- 54. Spiral Matrix

**心得**：
- 54：方向正確，可是寫太久了。另外，在設計初始狀態跟 index boundary 的時候，可以再想一下，也許程式碼可以更精簡。如果看到 redundant 的 code，應該有地方可以再優化。

**LLM 點評**：
model: Sonnet 5
- 54：實際做法是 direction array + 原地 visited 標記，撞到邊界或 visited 就轉向（`d = (d+1) % 4`）。看過實際 code 後找到兩處 redundant：(1) `while` 迴圈條件跟迴圈內的 if 判斷是同一組 boundary/visited check，做了兩次；(2) 「move → 發現撞牆 → undo 這步 → 轉向 → 再 move 一次」可以省掉，因為總步數已知是 `m*n`，改成 `for (k < m*n)` 驅動迴圈，並用暫存的 `ni, nj` 算出下一步候選座標、決定完方向後一次到位，不用先移動再退回。演算法本身（direction array + sentinel）沒問題，純粹是這兩處檢查重複。

---

## 2026-09-07

- 15. 3Sum（重做，通過 — running hash map）
- 17. Letter Combinations of a Phone Number
- 33. Search in Rotated Sorted Array
- 39. Combination Sum
- 46. Permutations
- 53. Maximum Subarray

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
- 39：我的做法是「選或不選」。常見方式是直接做成多叉決策樹，我做的是二元決策樹。最麻煩的是時間複雜度計算：選或不選是 2 的某個次方，次方看有幾個元素，也就是 target 最大除以最小值，就知道指數級數了。一開始沒想到可以用數字的範圍來推導需要分叉幾次。之後可以再回來算一次，用 N 多叉決策樹的做法做一遍。
- 53：太經典了。直覺是 Kadane's，一時間被轉去 sliding window，但知道要用 DP。卡了蠻久，完全解不出 Kadane 的解法。偷看解答後做了 bottom-up DP，但在算最大值時忘記為什麼全域最大值要在每個子陣列的可能性裡 globally tracking — 每個位置都有可能，而不是最後那個項目。現在沒辦法直觀地看出這個東西。

**LLM 點評**：
model: Fable 5.1
- 15：hash map build 不出來，是因為方向選錯，不是 dedup 沒做好。「固定 (i, j)、用 map 找 k」在 2Sum 可行是因為它回傳 index 且只要一組；3Sum 回傳**值**、要**所有不重複組合**，map 這條路要同時處理「k 的 index ≠ i, j」和「值重複」，天生就髒。排序後的標準解只用一個 outer loop：固定 i，剩下區間用對向雙指針找 j, k — 就是 LC 11 那個 greedy 淘汰（`sum < 0` 丟左、`sum > 0` 丟右）。排序的價值不只是 dedup，**它讓 two pointer 成立**，所以 map 根本不需要；dedup 只剩三處 `while (nums[x] == nums[x-1]) skip`。看 `K-Sum_Problems/02-Three_Sum.md` 後重寫，通過後 16、18 是同一個模板。
- 15（第二次）：你做出來的就是「固定 i，內層跑 Two Sum I（seen-set）」— 「往前找曾經看過的」正是 LC 1 的 seen-set 概念，只是把 target 換成 `-nums[i]`，所以 hash map 其實是內層 2Sum 的 cache，不是 3Sum 層級的。它和 two-pointer 一樣 O(N²)，差別在 dedup：two-pointer 靠有序跳過三處相同值就乾淨；seen-set 版要在 i 跳重複 + 內層用 set 收 (j, k) 值對，比較容易漏。二刷時兩種都寫，重點感受「排序讓 two-pointer 成立」這件事。
- 17：queue（BFS）版不用另外寫。它和 backtracking 是同一棵 state space tree 的 BFS / DFS 兩種走法，沒有新的設計決策，面試也極少追問（這題的 follow-up 通常是 digits 為空、或 mapping 動態給定）。真正值得留意的是這題把 backtracking 的三要素展示得很乾淨：path、candidates 由 `digits[depth]` 決定、terminate 在 `depth == digits.size()`。`const` map 用 `.at()` 這個坑 repo 已有：`CPP_Reference/Container/Const_Map_and_Operator_Bracket.md`。
- 33：你這次抓到的判準是對的，而且它和 153 是**兩種不同的 binary search**，混用就是你一直錯的原因。153 找 inflection point，predicate 是 `nums[m] > nums[r]`（跟右端比）；33 不找 inflection，每輪只問「`[l, m]` 是否 sorted」（`nums[l] <= nums[m]`），sorted 那半可以用普通 range check 決定 target 在不在，不在就整半 prune。**是「兩段 binary search」壓成一段**，不是「先找 pivot 再二分」。注意 `<=` 而非 `<`：`l == m` 時單元素也算 sorted，否則會漏。repo 的 `07-Inflection_Point_Binary_Search.md` 目前只收 153 / 162，這個「找 sorted 半邊」的 predicate 還沒寫進去，值得補一段對照。
- 39：你的推導方向對，補一個精確化：二元樹的深度不是 `T/M`，而是 `N + T/M` — 每個「不選」讓 `i` 前進一格（最多 N 次），每個「選」讓 `target` 減至少 M（最多 T/M 次），所以 `O(2^(N + T/M))`；多叉樹版是 `O(N^(T/M))`，兩者都是同一個 state space `(i, remaining)` 的不同枚舉方式。**「用數值範圍推遞迴深度」這個感覺是 backtracking 複雜度分析的核心**：深度 = 「還能做幾次決策直到終止」，這題的終止由 target 給，所以深度由 T/M 給。二元 vs 多叉在 repo 有專文：`Algorithms/Backtracking/05-State_Space_Tree_and_N_Tuple_Representation.md`。
- 39（code review）：演算法正確，排序後 `candidates[i] > remaining` 同時砍掉選/不選兩支是亮點；開頭的 input/output 註解是 3Sum 教訓的落實。要改：複雜度註解 `O(n^n * n)` 錯，應為 `O(2^(N+T/M) · T/M)`，空間是遞迴深度 `O(T/M)` 不是 `O(n)`；`solutions` 做 member 會讓重複呼叫累加，改 by-ref 傳或開頭 clear；`sol` 改名 `path`。
- 53：你卡的點是 **state 的定義跟答案的形狀不一樣**。`dp[i]` 定義的是「**以 i 結尾**的最大子陣列和」，這是一個被限制的子問題，不是答案；答案是 `max(dp[0..n-1])`，因為最優子陣列可以在任何位置結尾，`dp[n-1]` 只是「必須包含最後一個元素」那一種。為什麼要這樣定義？因為「以 i 結尾」才能讓遞推 O(1)：`dp[i] = max(nums[i], dp[i-1] + nums[i])` — 要嘛接上前面，要嘛重新開始。如果把 state 定成答案的形狀「`[0..i]` 內的最大子陣列和」，遞推就寫不出來（不知道前面的最優段有沒有碰到 i-1，無法延伸）。所以這是一個交易：**把 state 綁死在「必須包含 i」換取乾淨的遞推，代價是最後要多一層 global max**。這正是 repo 的 `Kadanes_Pattern_DP.md`（dp[i] 必須包含位置 i）和 `State_Design/05-Local_State_vs_Global_Optimum.md` 在講的東西。順帶：sliding window 在這題失效是因為有負數 — 窗口不知道該不該縮，單調性不成立。

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
