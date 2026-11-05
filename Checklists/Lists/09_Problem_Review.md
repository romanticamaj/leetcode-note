# 演算法題目複習清單

這份清單用於追蹤需要重點複習的演算法題目。

## 必練星級

之後新增或更新複習項目時，皆在題目前標註 **⭐～⭐⭐⭐⭐⭐**。星數表示個人的**必練程度／複習優先級**，不代表題目難度；同題不同版本可分別評級。使用者指定的星級優先，未指定時依練習紀錄與重練目標判斷。既有未標星項目待更新時再補。

| 星級 | 意義 |
|:---|:---|
| ⭐⭐⭐⭐⭐ | 必練，優先安排並獨立重做 |
| ⭐⭐⭐⭐ | 重點複習，核心觀念或實作仍需鞏固 |
| ⭐⭐⭐ | 一般複習，值得再練一次 |
| ⭐⭐ | 延伸練習，核心版本熟悉後再做 |
| ⭐ | 選修，有餘裕時練習 |

## 重練追蹤

從 [刷題日誌](../Practice_Log.md) 與下方複習目標整理，聚焦已練過的題目；尚未練過的題目保留在下方清單。**前次練習**是整理時日誌裡最近一次記錄該題的日期（已完成的列保留重做前的練習日）；**重做日期**只填已確認完成這項目標的日期，`—` 表示仍待做。舊筆記中的「二刷日期」是當時的計畫，不能當作已完成紀錄。同一題的不同版本分開追蹤。之後重做時先記入日誌；達成該目標才把狀態改成「已完成」並填上實際日期。

| 狀態 | 題目／重練目標 | 前次練習 | 重做日期 |
|:---|:---|:---:|:---:|
| 待做 | ⭐⭐⭐ 545. Boundary of Binary Tree：one-pass DFS；結合 preorder／postorder 與 isLeftBoundary／isRightBoundary 多狀態傳遞，獨立推導邊界旗標、葉節點去重與輸出順序；目前只完成分段版本 | 2026-11-05 | — |
| 待做 | ⭐⭐⭐⭐ 518. Coin Change II：計畫 2026-11-04 寫二維 bottom-up；保留 (coin index, remaining amount) 語義，獨立推導 base case 與填表方向，說明選取留在同一 i、跳過依賴 i+1；先不要求一維壓縮 | 2026-11-03 | — |
| 待做 | ⭐⭐⭐⭐⭐ 787. Cheapest Flights Within K Stops：Bellman-Ford／邊數 DP；獨立定義至多 i 條邊的最小費用，實作每輪只讀上一層快照，說明 k stops = k+1 edges 與原地更新會超用邊數 | 2026-11-03 | — |
| 待做 | ⭐⭐⭐⭐⭐ 787. Cheapest Flights Within K Stops：BFS with condition k；按已用邊數分層做費用 relaxation、同層同城市合併再擴展，限制最多 k+1 條邊；說明不能首次 visited 就封鎖城市或首次抵達 dst 就回傳 | 2026-11-03 | — |
| 待做 | ⭐⭐⭐⭐⭐ 787. Cheapest Flights Within K Stops：better Dijkstra；獨立推導 cost-ordered pop＋minEdges 支配剪枝，保留較貴但邊數較少的候選，解釋為何只能在 pop 時套用此判斷、合法 dst 可提早回傳，分析 heap 成本 | 2026-11-03 | — |
| 待做 | ⭐⭐⭐ 846. Hand of Straights：獨立推導最小剩餘值必須當組頭的 greedy，以 ordered frequency map 批次開 count 組並扣除連續值；分析 O(n log(U+1)) 時間、O(U) 空間，O(n) 延伸版本暫不列必做 | 2026-10-31 | — |
| 待做 | ⭐⭐⭐⭐ 240. Search a 2D Matrix II：已完成三區域 divide and conquer；獨立推導並實作 O(m+n) 時間、O(1) 空間搜尋，證明每次可安全排除整列或整欄；此延伸尚未完成 | 2026-10-31 | — |
| 待做 | ⭐⭐⭐⭐ 721. Accounts Merge：獨立建立 graph，說明節點、邊與共享 email 的傳遞連通性；避免同名誤合併、同帳戶重複展開或不必要的兩兩連邊，分析遍歷與排序成本 | 2026-10-30 | — |
| 待做 | ⭐⭐⭐⭐⭐ 678. Valid Parenthesis String：目前完成 recursive → top-down DP；另日學習並獨立實作 O(n) 時間、O(1) 空間的做法，重點在狀態摘要與正確性 invariant；尚未完成此延伸版本 | 2026-10-30 | — |
| 待做 | 222. Count Complete Tree Nodes：本次經提示完成；獨立重建最後一層存在性的單調判定、編號 bits 對應根到節點路徑，以及 binary search 邊界；驗證空樹與未滿最後一層，分析 O(log² n) 時間、O(log n) 遞迴空間 | 2026-10-30 | — |
| 待做 | 380. Insert Delete GetRandom O(1)：獨立實作 hashmap + vector 尾端補位刪除，維持 value → index 一致；驗證刪中間／尾端／唯一元素與刪後重插，整合 uniform_int_distribution 均勻取樣並說明 modulo bias | 2026-10-29 | — |
| 待做 | 279. Perfect Squares：獨立重做以目標總和為狀態的 DP，枚舉最後一個平方數並推導最小化轉移；說明不能只取最大平方數，以及 Θ(n√n) 時間、O(n) 空間的分析 | 2026-10-29 | — |
| 待做 | 647. Palindromic Substrings：獨立推導並實作 O(n²) 時間、O(1) 額外空間的 follow-up；目前已完成 O(n²) 空間的 DP 版本 | 2026-10-28 | — |
| 待做 | 560. Subarray Sum Equals K：獨立推導並實作 running sum + frequency hashmap，不建立 prefix sum 陣列；說明負數為何使此題無法直接套 sliding window、空前綴初始化，以及先查詢再記錄的 invariant | 2026-10-28 | — |
| 待做 | 373. Find K Pairs with Smallest Sums：獨立重做 k-way merge；從隱式有序序列推導每列一個候選的 invariant、同列補位與 min-heap comparator | 2026-10-28 | — |
| 待做 | **【必做】221. Maximal Square：再做一次，獨立重建固定右下角、逐邊長 DP 的狀態與三個小正方形的覆蓋證明；檢查邊長 1、全 0 與座標偏移** | 2026-10-27 | — |
| 待做 | **【高優先級】542. 01 Matrix：獨立推導並實作 two-pass DP（distance transform）；說明為何一次掃描不足、兩次足夠，以及無障礙四鄰接網格的適用條件** | 2026-10-26 | — |
| 待做 | 117. Populating Next Right Pointers in Each Node II：獨立實作迭代版，真正 O(1) 額外空間（無 queue、無遞迴堆疊）；沿當前層 next 鏈走訪，以固定數量指標建立下一層 | 2026-10-25 | — |
| 已完成 | 117. Populating Next Right Pointers in Each Node II：不使用額外 queue 的 recursive follow-up（經提示修正為先右後左；實際呼叫堆疊 O(h)） | 2026-10-25 | 2026-10-25 |
| 待做 | **【必做】117. Populating Next Right Pointers in Each Node II：獨立重做 recursive 版本，重建 parent 更新 children、先右後左與右側 next 鏈已建立的 invariant；驗證稀疏樹跨層／跨子樹連結** | 2026-10-25 | — |
| 待做 | 355. Design Twitter：回來獨立實作 k-way merge＋max-heap；目前已實作固定大小 min-heap 的 Top-k 版本，此版本尚未完成 | 2026-10-24 | — |
| 待做 | **【必做】394. Decode String：再做一次，獨立重建解析狀態、stack 各層上下文與片段合併順序，分析字串複製成本** | 2026-10-24 | — |
| 待做 | 394. Decode String：獨立實作 recursive 版本 | 2026-10-24 | — |
| 待做 | 394. Decode String：獨立實作 two-stack 版本 | 2026-10-24 | — |
| 待做 | 106. Construct Binary Tree from Inorder and Postorder Traversal：再做一次，搭配 hashmap 獨立實作預期 O(n) 解法；預建 value → inorder index，維持兩種 traversal 區間語義與參數順序 | 2026-10-23 | — |
| 待做 | 137. Single Number II：單次掃描、無 array，以 ones / twos 保存各 bit 的 mod 3 狀態；自行推導與實作 | 2026-10-22 | — |
| 待做 | 494. Target Sum：經提示仍未掌握；獨立推導總和值域、offset 邊界與 bottom-up Counting DP | 2026-10-21 | — |
| 待做 | 91. Decode Ways：重新推導 bottom-up Counting DP，釐清切點狀態與計數轉移 | 2026-10-20 | — |
| 待做 | **【必做】416. Partition Equal Subset Sum：先練固定 target 的 Subset Sum，再獨立重做** | 2026-10-21 | — |
| 待做 | 84. Largest Rectangle in Histogram：重做並練單一 stack，彈出時結算、掃描後處理剩餘項目 | 2026-10-19 | — |
| 待做 | 84. Largest Rectangle in Histogram：Divide and Conquer | 2026-10-19 | — |
| 待做 | 399. Evaluate Division：改用 [Weighted Union-Find](../../Algorithms/Union_Find/10-Weighted_Union_Find_with_Path_Compression.md) 練習比值關係維護 | 2026-10-18 | — |
| 待做 | 43. Multiply Strings：獨立重做位數對齊、進位與前導零處理 | 2026-10-16 | — |
| 待做 | 31. Next Permutation：再做一次 | 2026-10-16 | — |
| 待做 | 8. String to Integer (atoi)：Phase Based Parsing | 2026-10-16 | — |
| 待做 | 40. Combination Sum II：獨立重做同層去重 | 2026-10-16 | — |
| 待做 | 12. Integer to Roman：固定面額表／Greedy | 2026-10-16 | — |
| 待做 | 703. Kth Largest Element in a Stream：Augmented BST | 2026-10-14 | — |
| 待做 | 572. Subtree of Another Tree：字串比對／canonical form | 2026-10-13 | — |
| 待做 | 4. Median of Two Sorted Arrays：獨立推導 | 2026-10-12 | — |
| 待做 | 392. Is Subsequence：LCS DP／next-position table | 2026-10-12 | — |
| 待做 | 347. Top K Frequent Elements：bucket sort／quickselect | 2026-10-11 | — |
| 待做 | 6. Zigzag Conversion：O(1) 額外空間 | 2026-10-10 | — |
| 待做 | 409. Longest Palindrome：one-pass | 2026-10-10 | — |
| 待做 | 143. Reorder List：O(1) 額外空間 | 2026-10-09 | — |
| 待做 | 268. Missing Number：bit manipulation | 2026-10-09 | — |
| 待做 | 287. Find the Duplicate Number：Floyd 與其他做法 | 2026-10-09 | — |
| 待做 | 189. Rotate Array：暴力法／三次反轉 | 2026-10-09 | — |
| 待做 | 232. Implement Queue using Stacks：最壞 O(1) peek | 2026-10-06 | — |
| 待做 | 152. Maximum Product Subarray：重講暴力法與時間 | 2026-10-05 | — |
| 待做 | 95. Unique Binary Search Trees II：複習 | 2026-10-04 | — |
| 待做 | 131. Palindrome Partitioning：獨立重做 | 2026-10-02 | — |
| 待做 | 69. Sqrt(x)：再刷並驗收 binary search | 2026-10-02 | — |
| 待做 | 28. Find the Index of the First Occurrence in a String：再做 | 2026-10-01 | — |
| 待做 | 13. Roman to Integer：從右到左解析 | 2026-09-29 | — |
| 待做 | 114. Flatten Binary Tree to Linked List：O(1) 空間迭代版 | 2026-09-29 | — |
| 待做 | 97. Interleaving String：bottom-up／空間壓縮 | 2026-09-28 | — |
| 待做 | 36. Valid Sudoku：bit manipulation | 2026-09-26 | — |
| 待做 | 300. Longest Increasing Subsequence：O(n log n) | 2026-09-22 | — |
| 待做 | 215. Kth Largest Element in an Array：quickselect | 2026-09-21 | — |
| 待做 | 236. Lowest Common Ancestor of a Binary Tree：用節點當回傳值 | 2026-09-21 | — |
| 待做 | 78. Subsets：模式 B | 2026-09-20 | — |
| 待做 | 128. Longest Consecutive Sequence：起點錨定版 | 2026-09-20 | — |
| 待做 | 73. Set Matrix Zeroes：O(1) 空間版 | 2026-09-19 | — |
| 待做 | 42. Trapping Rain Water：monotonic stack | 2026-09-18 | — |
| 待做 | 22. Generate Parentheses：D&C／DP | 2026-09-17 | — |
| 待做 | 238. Product of Array Except Self：prefix 設計 | 2026-09-15 | — |
| 待做 | 23. Merge k Sorted Lists：bottom-up D&C／heap | 2026-09-15 | — |
| 選做 | 169. Majority Element：D&C 版 | 2026-09-15 | — |
| 待做 | 230. Kth Smallest Element in a BST：iterative inorder／Augmented BST | 2026-09-14 | — |
| 待做 | 139. Word Break：樸素 DP 再到 Trie | 2026-09-11 | — |
| 待做 | 146. LRU Cache：一次寫對 | 2026-09-11 | — |
| 已完成 | 15. 3Sum：sort + two pointers（使用者確認） | 2026-10-20 | 2026-10-20 |
| 已完成 | 15. 3Sum：running hashmap（九月完成紀錄誤記，本次完成） | 2026-10-20 | 2026-10-20 |
| 待做 | 15. 3Sum：no-sort follow-up | 2026-10-20 | — |
| 待做 | 33. Search in Rotated Sorted Array：獨立重寫 | 2026-09-07 | — |
| 待做 | 39. Combination Sum：多叉決策樹 | 2026-09-07 | — |
| 待做 | 53. Maximum Subarray：獨立推導 Kadane | 2026-09-07 | — |
| 待做 | 5. Longest Palindromic Substring：複習 | 2026-09-05 | — |
| 待做 | 104／226. Maximum Depth／Invert Binary Tree：迭代版 | 2026-09-05 | — |
| 已完成 | 8. String to Integer (atoi)：FSM／DFA | 2026-10-16 | 2026-10-16 |
| 已完成 | 416. Partition Equal Subset Sum：經提示完成 top-down memoization 版本 | 2026-09-22 | 2026-10-19 |
| 已完成 | 283. Move Zeroes：O(n) 雙指標 | 2026-10-11 | 2026-10-11 |
| 已完成 | 235. Lowest Common Ancestor of a BST：迭代版 | 2026-10-10 | 2026-10-10 |
| 已完成 | 45. Jump Game II：O(n) 壓縮 BFS | 2026-09-17 | 2026-09-18 |
| 已完成 | 42. Trapping Rain Water：two pointers | 2026-09-18 | 2026-09-18 |


**使用說明**:

- ✅ 標記為「需要複習」的題目
- 📌 **標記原因**: 記錄為什麼需要複習（技巧陌生、實作細節、思路盲點等）
- 🔗 **前置題型**: 如果技巧完全陌生，先去練習的 simpler 題目（參考 [Hard_Techniques_Reference.md](../../Interview_Playbook/Hard_Techniques_Reference.md)）
- 📅 **複習計畫**: 二刷/三刷時間規劃

---

## 題目列表格式

```markdown
- [ ] LeetCode XXX. Problem Name
  - 📌 標記原因: [技巧陌生 / 實作細節 / 思路盲點]
  - 🏷️ 技巧分類: [Monotonic Stack / DP / Graph / etc.]
  - 🔗 前置題型: [LC YYY, LC ZZZ]（如果需要）
  - 📅 二刷: YYYY-MM-DD
  - 📅 三刷: YYYY-MM-DD
```

---

## 題目列表

- [ ] **⭐⭐⭐ LeetCode 545. Boundary of Binary Tree — one-pass DFS**
  - 🔗 歷史與教材：[EPI 的 Exterior、早期面試紀錄與 Euler Tour 遍歷框架](../../Problem_History/LC_0545_Boundary_of_Binary_Tree.md)。
  - 📌 標記原因：2026-11-05 已完成左邊界／葉節點／右邊界的分段遞迴；看過 one-pass 設計後，想另日獨立實作，尚未完成此版本。
  - 🏷️ 關鍵字：**Preorder + Postorder / Multi-state DFS / Boundary Flags / Top-down State Propagation / 輸出順序設計**。
  - [ ] 定義 `isLeftBoundary`／`isRightBoundary`，由父節點往子節點傳遞邊界身分，不依賴「第一個／最後一個 leaf」的全域階段切換。
  - [ ] 左邊界在 preorder 加入，右邊界在 postorder 加入；葉節點只加入一次並直接返回。
  - [ ] 獨立推導缺少 child 時的旗標轉移：左邊界優先左、缺左走右；右邊界優先右、缺右走左。root 單獨加入，左右子樹分別以 `(true, false)`／`(false, true)` 起始。
  - [ ] 用單節點、單側鏈與缺少偏好 child 的樹驗證順序及去重；說明 O(n) 時間、O(h) 呼叫堆疊，輸出另計。
  - 🔗 前置閱讀：[遞迴設計：狀態與職責](../../Algorithms/Design_Principles/Recursion/01-Recursion_Design_Principles.md)。

- [ ] **⭐⭐⭐⭐⭐ LeetCode 787. Cheapest Flights Within K Stops**
  - 📌 標記原因：第三次做仍卡在 C++ 型別表示與邊數狀態；本次經提示完成二維 distance 版本，以下三種解法仍須分別獨立驗收。
  - 🔗 前置閱讀：[邊數限制最短路徑的出處、歷史與三種排程](../../Problem_History/LC_0787_Cheapest_Flights_Within_K_Stops.md)。
  - [ ] Bellman-Ford：以快照維持至多 i 條邊的 DP invariant。
  - [ ] BFS with condition k：按邊數分層、合併同層費用，不套用普通 BFS 的 visited／首次抵達終點規則。
  - [ ] Better Dijkstra：依費用出隊，以 minEdges 做 dominance pruning，區分與二維 distance 版本的保證。
  - 📌 共通驗收：用本次 node 4 的反例說明低費用與少邊數互不支配；比較正確性、時間與含 queue／heap 的空間成本。

- [ ] **LeetCode 201. Bitwise AND of Numbers Range**
  - 📌 標記原因：2026-10-29 嘗試後暫停，尚未完成；逐 bit 枚舉整個區間的版本時間成本過高，推導 bit 週期時感到缺少工具。
  - 🏷️ 技巧分類：Bit Manipulation / 區間二進位觀察
  - [ ] 複習位移操作與連續整數的 bit pattern，再獨立推導不逐一掃描區間的做法。
  - [ ] 檢查 bitwise 與比較運算的優先序、整數邊界，以及以區間長度分析暴力法時間。

- [ ] **K-way Merge（多路合併）專題重練**
  - 🔗 前置閱讀：[K-way Merge 的演算法與文獻歷史](../../Problem_History/LC_0373_Find_K_Pairs_with_Smallest_Sums.md)。
  - [ ] 373. Find K Pairs with Smallest Sums：不看本次討論，獨立辨識隱式有序列、實作 heap frontier，證明每次取出的配對是全域剩餘最小值。
  - [ ] 23. Merge k Sorted Lists：練 heap 版本，與原有 bottom-up D&C 目標分開驗收。
  - [ ] 355. Design Twitter：完成既有待做的 max-heap k-way merge 目標，不以固定大小 min-heap Top-k 版本代替。
  - 📌 重點：多條有序來源、每來源只保留一個前端、取出後只補同來源；區分「來源數 r」與「取出數 q」，分析 O(r + q log(r+1))（線性建堆）與 O(r) heap 空間。

- [ ] **【必做】LeetCode 221. Maximal Square**
  - 📌 標記原因：做了這麼多次，還是覺得這題很難；本次經 code review 修正後完成逐邊長 boolean DP，並在討論後完成 O(mn) top-down 版本，仍需獨立重做。
  - [ ] 明確定義每輪開始時 dp 的邊長與右下角語意，推導三個小正方形加當前格的充分必要條件。
  - [ ] 獨立處理邊長 1 的答案、全 0、單列／單欄、字元比較，以及隨邊長變動的迴圈起點與固定座標偏移。
  - [ ] 說明時間 O(mn · min(m,n))、額外空間 O(mn)；再獨立推導以最大可行邊長取代 boolean 邊長維度的 O(mn) 版本，說明局部狀態與全域答案的差別，以及遇到 0 時是否仍走訪其他位置。
  - 🏷️ 技巧分類：Grid DP / 狀態定義 / 幾何覆蓋

- [ ] **【高優先級】LeetCode 542. 01 Matrix：Two-pass DP / Distance Transform**
  - 📌 標記原因：已完成 Multi-source BFS；two-pass DP 尚未練習，優先補足以掃描順序傳播距離的思考方式。
  - [ ] 獨立定義距離狀態、初始化與兩次掃描的轉移；釐清第二趟使用第一趟已更新的結果。
  - [ ] 解釋一次掃描為何不足、兩次為何足夠；利用無障礙、四方向等成本移動下的 Manhattan 最短路徑結構證明，不能直接推廣到有障礙的網格。
  - [ ] 實作並分析 O(mn) 時間；區分距離表的 O(mn) 儲存與表以外的 O(1) 工作空間。
  - 🏷️ 技巧分類：DP / Two-pass Relaxation / Distance Transform
  - 🔗 相關筆記：[雙向約束分解](../../Algorithms/Design_Principles/Bidirectional_Constraint_Decomposition.md)、[State Decomposition](../../Algorithms/Dynamic_Programming/Advanced_Techniques/State_Decomposition.md)。這些是相關的方向分解概念；本題第二趟承接第一趟結果，不是兩個獨立方向求解後合併。
  - 🔗 已完成解法：[Multi-source BFS](../../Algorithms/BFS/MultiSource_BFS_Thinking_Framework.md)。

- [ ] LeetCode 43. Multiply Strings
  - 📌 標記原因: 第一次花 35m 46s，過程中持續依靠提示，還沒獨立完成；體感 Medium 偏難。
  - [ ] 不看提示獨立重做，確認位數對齊、進位與前導零（包含零乘零）的處理。
  - 🏷️ 技巧分類: String / Simulation / Digit Alignment

- [ ] LeetCode 40. Combination Sum II
  - 📌 標記原因: 題目難，想再做一次；需分清排序剪枝、同層去重與不同層選用另一個相同值。
  - [ ] 不看解答重做一次，說明 `i > start` 與下一層 `i + 1` 各自保證什麼。
  - 🏷️ 技巧分類: Backtracking / Same-level Deduplication

- [ ] LeetCode 31. Next Permutation
  - 📌 標記原因: 第一次完成後仍覺得難，想再練習一次；特別確認重複值、pivot 與非遞增 suffix 的關係。
  - [ ] 不看解答再做一次。
  - 🏷️ 技巧分類: Permutation / Non-increasing Suffix

- [ ] LeetCode 703. Kth Largest Element in a Stream
  - 📌 標記原因: 已用 k-size min heap 完成；之後想練 Augmented BST 的動態 order statistics 版本。
  - [ ] 用 subtree size 維護動態 BST，實作插入與第 k 大查詢，說明每次更新如何保持 size 不變量。
  - 🏷️ 技巧分類: Augmented BST / Order Statistics
  - 🔗 前置閱讀: [Augmented BST for Order Statistics](../../Data_Structures/Trees/Binary_Search_Trees/Augmented_BST_for_Order_Statistics.md)

- [ ] LeetCode 392. Is Subsequence
  - 📌 標記原因: 已完成 two pointers 與位置列表 + upper_bound；下次理解並實作提供的 LCS DP 版本。
  - [ ] 從兩個前綴的狀態意義推導轉移，說明為何 LCS 長度等於 s.length() 就能判定 subsequence；先自行思考，需要時只給一句話提示。
  - [ ] 大量查詢 follow-up：另外練習預處理固定 t 的 next-position table，與上述 LCS DP 區分；尚待實作。
  - 🏷️ 技巧分類: String / Two Pointers / Binary Search / DP

- [ ] LeetCode 409. Longest Palindrome
  - 📌 標記原因: 已完成先計數、再掃描頻率表的版本，下次練習 one-pass traversal。
  - [ ] 重寫 one-pass traversal 版本：只遍歷輸入字串一次，不再額外遍歷頻率表。
  - [ ] 用 unordered_map 實作 one-pass traversal，想清楚為什麼可行。
  - [ ] 用 unordered_set 實作 one-pass traversal，想清楚為什麼可行；比較兩者維護的資訊。
  - 🏷️ 技巧分類: Hash Table / Counting / One-pass Traversal

- [ ] LeetCode 6. Zigzag Conversion
  - 📌 標記原因: 已完成依 row 分桶的版本，下次練習省去分桶暫存空間。
  - [ ] 重寫 O(n) 時間、O(1) 額外空間的版本（不計回傳字串所需的 O(n) 空間）。
  - 🏷️ 技巧分類: String / Index Mapping / Periodicity

- [ ] LeetCode 268. Missing Number
  - 📌 標記原因: 已做 hashmap 與加總版本；bit manipulation 版本直接看解答仍無感、不直觀，需要重做。
  - [ ] Bit manipulation：不看解答自行推導並重寫，說清楚為什麼能找出遺失的數字。
  - 🏷️ 技巧分類: Bit Manipulation / XOR

- [ ] LeetCode 189. Rotate Array
  - 📌 標記原因: 整題之後再做一次；reverse 解法不直觀，暴力法也值得重做。
  - [ ] 暴力右移：保存尾元素、由右往左搬移、放回開頭；先 k %= n，檢查 k = 0、k >= n。
  - [ ] 三次 reverse：從 A|B → B|A 自行推導，不只背操作順序；說明先整條反轉時切在 k、先兩段反轉時切在 n-k。
  - 🔗 歷史與理解線索: [Rotate Array：三次反轉的歷史](../../Problem_History/LC_0189_Rotate_Array.md)
  - 🏷️ 技巧分類: Array Rotation / Simulation / Reversal

- [ ] LeetCode 287. Find the Duplicate Number
  - 📌 標記原因: 非常困難，首次完全靠解答與 gpt-6.1-sol 提示；必須重做，並嘗試不同解法。
  - [ ] Array as HashMap (Recursion)：space O(n)，下次先給方向性提示，再自行重做，不直接給解法或程式碼。
  - [ ] Array as HashMap (Iterative)：space O(1)，下次先給方向性提示，再自行重做，不直接給解法或程式碼。
  - 🏷️ 技巧分類: Array as Functional Graph / Floyd Cycle Detection / Pigeonhole Principle
  - 🔗 前置題型: LeetCode 142. Linked List Cycle II
  - [ ] Floyd：不看解答重寫；說明入口為何是重複值、兩階段起點如何一致，以及為何回傳入口 index。
  - [ ] 值域二分 + 計數：推導鴿籠原理如何決定搜尋方向。
  - [ ] Bit counting：比較 nums 與 1～n 的各 bit 計數，說明重複值出現超過兩次時為何仍成立。
  - [ ] 暴力、Hash Set、排序：實作並比較時間、空間與是否修改輸入；指出哪些不符合題目限制。

- [ ] LeetCode 95. Unique Binary Search Trees II
- [ ] LeetCode 240. Search a 2D Matrix II
  - ⭐⭐⭐⭐ 2026-10-31 已完成 divide-and-conquer 版本；O(m+n) 時間、O(1) 空間版本仍待練，見上方重練追蹤。
- [ ] LeetCode 489. Robot Room Cleaner
- [ ] LeetCode 215. Kth Largest Element in an Array
- [ ] LeetCode 37. Sudoku Solver
- [ ] LeetCode 84. Largest Rectangle in Histogram
  - 📌 標記原因: 2026-10-19 經提示完成暴力法與雙向 monotonic stack／邊界陣列版本；使用者指定再做一次、優化 monotonic stack，並另練 divide and conquer。
  - [x] Brute Force：2026-10-19 完成逐柱尋找左右最近較矮邊界的 O(n²) 版本。
  - [x] Monotonic Stack：2026-10-19 經提示完成雙向掃描、記錄左右邊界後計算面積的 O(n) 版本。
  - [ ] Monotonic Stack：再做一次，練單一 stack；從左到右掃描，彈出時直接結算面積，最後處理剩餘項目。下次再理解其設計模式並實作，目前尚未完成。
  - [ ] Divide and Conquer：另做此版本。
    - [ ] Segment Tree for Divide and Conquer（保留原有延伸目標）
- [ ] LeetCode 347. Top K Frequent Elements
  - [ ] Bucket sort：利用 frequency 在 1 到 n 的範圍內，時間 O(n)；先記下來，下次實作。
  - [ ] Quickselect (Hoare's selection algorithm)
- [ ] LeetCode 285. Inorder Successor in BST
  - [ ] iterative with BST property
- [ ] LeetCode 145. Binary Tree Postorder Traversal
  - [ ] Two Stack Postorder Traversal (Iterative)
- [ ] LeetCode 261. Graph Valid Tree
- [ ] LeetCode 1059. All Paths from Source Lead to Destination
- [ ] LeetCode 1631. Path With Minimum Effort
  - [ ] Union Find - Disjoint Set
- [ ] LeetCode 1089. Duplicate Zeros
- [ ] LeetCode 1770. Maximum Score from Performing Multiplication Operations
- [ ] LeetCode 91. Decode Ways
  - 📌 標記原因: top-down 從 recursion 容易推導，但 bottom-up Counting DP 仍不直覺。
  - 🏷️ 技巧分類: Counting DP / Prefix Length / Cut Position
  - 重練目標: 獨立定義狀態，從最後一個編碼長度推導轉移，說明為何累加前綴方案數而非 +1，以及空前綴的計數基底；驗證含 0 的情況與中間計數溢位風險。
  - 重做日期: —
- [ ] LeetCode 15. 3Sum
  - 📌 標記原因: 九月 running hashmap「已完成」是誤記；2026-10-20 先完成完整索引表版本，接著完成排序後 running hashmap。使用者確認 sort + two pointers 亦已完成，目前僅 no-sort 尚未嘗試。
  - [x] Running hashmap：2026-10-20 完成；經提示修正內層去重，找到配對後才跨過相同值。
  - [x] Sort + two pointers：2026-10-20 使用者確認完成。
  - [ ] No-sort follow-up：探索不排序時如何確保合法位置與輸出去重。
  - 🏷️ 技巧分類: Sort + Two Pointers / Dedup
  - 📅 二刷: 2026-09-13（用 2-pointer 寫，重點感受「排序讓 two-pointer 成立」）
- [ ] LeetCode 236. Lowest Common Ancestor of a Binary Tree
  - [ ] 用 `TreeNode*` 當回傳值重寫（無全域變數、無 reset）
  - 📌 標記原因: 思路盲點 — 二刷仍只想到 `pair<bool,bool>` + 全域 `LCA`，回傳型別太弱導致要補 reset 與早退兩個補丁
  - 🏷️ 技巧分類: 後序遞迴 / 回傳型別即子問題答案
  - 🔗 後續題型: LC 235（BST 版）、LC 1644（不保證 p、q 存在，才需要布林增強）
  - 📅 二刷: 2026-09-21（仍是舊寫法）
- [ ] LeetCode 1335. Minimum Difficulty of a Job Schedule
  - [ ] Monotonic Stack
- [ ] LeetCode 53. Maximum Subarray
  - [ ] Divide and Conquer
  - 📌 標記原因: 思路盲點 — 看了解答才寫出 bottom-up DP，且不直觀為何 `dp[i]` 要定義成「以 i 結尾」而答案要 global max
  - 🏷️ 技巧分類: Kadane / Local State vs Global Optimum
  - 🔗 前置閱讀: `DP/State_Design/05-Local_State_vs_Global_Optimum.md`
  - 📅 二刷: 2026-09-12（不看解答，要能自己說出 state 為什麼這樣定）
- [ ] LeetCode 918. Maximum Sum Circular Subarray
  - [ ] Max & Min, Space O(1)
- [ ] LeetCode 718. Maximum Length of Repeated Subarray
- [ ] LeetCode 790. Domino and Tromino Tiling
- [ ] LeetCode 1473. Paint House III
  - [ ] 3D Dynamic Programming
- [ ] LeetCode 97. Interleaving String
- [ ] LeetCode 222. Count Complete Tree Nodes
  - 📌 2026-10-30 經提示完成編號 binary search 版本；獨立重做仍待完成，目標見上方重練追蹤。
- [ ] LeetCode 425. Word Squares
  - [ ] Trie
- [ ] LeetCode 212. Word Search II
  - [ ] Backtracking + Dynamic Trie
- [ ] LeetCode 654. Maximum Binary Tree
  - [ ] Monotonic Stack?
- [ ] LeetCode 951. Flip Equivalent Binary Trees
  - [ ] Canonical Forms
- [x] LeetCode 42. Trapping Rain Water（two pointers，2026-09-18；monotonic stack 仍待做）
  - [x] Two Pointers Technique (from brute force to prefix sum, then duplicate work removal through two-pointers)
  - [ ] Dynamic Programming
- [ ] LeetCode 253. Meeting Rooms II
  - [ ] Chronological Ordering
- [ ] LeetCode 135. Candy
  - [ ] Constraint Decomposition for Greedy or DP
- [ ] LeetCode 394. Decode String
  - **【必做】再做一次**：2026-10-24 覺得異常困難，stack 操作與解析狀態仍需重練；本次單一 stack＋sentinel 版經修正完成，不代表以下其他版本已完成。
  - [ ] 獨立重建解析狀態、每層上下文與合併順序，確認 string 建構方式並分析字串複製成本。
  - [ ] Two Stacks：獨立實作 two-stack 版本，尚未完成。
  - [ ] Recursion：獨立實作 recursive 版本，尚未完成。
- [ ] LeetCode 777. Swap Adjacent in LR String
- [ ] LeetCode 308. Range Sum Query 2D - Mutable
  - [ ] Binary Indexed Tree for 2D
- [ ] LeetCode 5. Longest Palindromic Substring
- [ ] LeetCode 590. N-ary Tree Postorder Traversal
  - [ ] visit flag (visit twice natural)
- [ ] LeetCode 1249. Minimum Remove to Make Valid Parentheses
  - [ ] Can you do it without using a stack?
- [ ] LeetCode 431. Encode N-ary Tree to Binary Tree
  - [ ] Can you solve it using BFS?
- [ ] LeetCode 47. Permutations II
  - [ ] Backtracking sorting + duplicate check trick + visited
  - [ ] Backtracking + grouping/counting/hashmap + visited
- [ ] LeetCode 428. Serialize and Deserialize N-ary Tree
  - [ ] DFS
- [ ] LeetCode 450. Delete Node in a BST
  - [ ] Recursion Version (必做, 太有趣)
- [x] LeetCode 235. Lowest Common Ancestor of a Binary Search Tree
  - [x] Iterative version（2026-10-10：時間 O(h)、輔助空間 O(1)）
- [ ] LeetCode 220. Contains Duplicate III
  - [ ] O(nlogk) solution + exactly one condition
  - [ ] Buckets: Inspired by bucket sort, we can achieve linear time complexity in our problem using buckets as window.
- [ ] LeetCode 732. My Calendar III
- [ ] LeetCode 297. Serialize and Deserialize Binary Tree
  - [ ] Pre-ordering/Recursion
  - [ ] BFS with structural optimized
- [ ] LeetCode 493. Reverse Pairs
  - [ ] BIT
- [ ] LeetCode 315. Count of Smaller Numbers After Self
  - [ ] Segment Tree
  - [ ] Binary Indexed Tree (Fenwick Tree)
- [ ] LeetCode 8. String to Integer (atoi)
  - [ ] Phase Based Parsing
  - [x] Deterministic Finite Automaton (DFA)（2026-10-16：心得記錄 FSM 解法）
- [ ] LeetCode 468. Validate IP Address
- [ ] LeetCode 32. Longest Valid Parentheses
  - [ ] Dynamic Programming
  - [ ] One Stack
- [ ] LeetCode 4. Median of Two Sorted Arrays
- [ ] LeetCode 421. Maximum XOR of Two Numbers in an Array
  - [ ] Trie
  - [ ] Bitwise Prefixes in HashSet
- [ ] LeetCode 336. Palindrome Pairs (Damn Hard!)
  - [ ] HashMap
  - [ ] Trie
- [ ] LeetCode 238. Product of Array Except Self
  - [ ] A Better Design of Prefix Array
- [ ] LeetCode 402. Remove K Digits
- [ ] LeetCode 229. Majority Element II
- [ ] LeetCode 645. Set Mismatch
  - [ ] Bit Manipulation
- [ ] LeetCode 36. Valid Sudoku
  - [ ] Bit Manipulation
- [ ] LeetCode 122. Best Time to Buy and Sell Stock II
  - [ ] Brute Force
- [ ] LeetCode 443. String Compression
- [x] LeetCode 45. Jump Game II（2026-09-18）
  - [x] Extreme State Compression BFS
- [ ] LeetCode 137. Single Number II
  - [ ] Bit Manipulation + State Machine + Bit Invariant：單次掃描、無 array，用 `ones` / `twos` 兩個變數保存各 bit 的 mod 3 狀態；之後自行推導轉移、確認更新順序並實作。
  - 📌 標記原因：2026-10-22 經提示完成逐位計數陣列版；目前覺得狀態機版難以思考，先留作 follow-up，尚未完成，重做日期保持空白。
- [ ] LeetCode 12. Integer to Roman
  - [ ] Phase Based Traversal (Greedy to select possible number)
- [ ] LeetCode 128. Longest Consecutive Sequence
  - Hash Table + Possible Start (check num - 1)
  - amortized analysis
- [ ] LeetCode 416. Partition Equal Subset Sum
  - **【必做】再做一次**，目前仍待獨立重建。
  - 2026-10-21 bottom-up 重做經提示修正列數 n、空集合 base case 與 nums[0] 超過 target 時的初始化越界，最終程式正確；獨立重建目標仍待完成，重做日期保持空白。
  - 📌 標記原因: 2026-09-22 嘗試後未解出；2026-10-19 經提示完成 top-down memoization，但自述仍不理解，尚未能獨立重建。
  - [x] 2026-10-19 經提示完成 `(index, remaining)` 的選／不選遞迴與 cache 版本。
  - [ ] 前置練習：直接給定正整數陣列與 target，每個位置最多一次，判斷是否存在子集和恰好為 target；先理解原始 Subset Sum，再回到 416 的轉換。見 [背包 DP 筆記](../../Algorithms/Dynamic_Programming/Problem_Types/Knapsack_DP.md)。
  - [ ] 理解與獨立重建：說清楚狀態語義、base case、每個元素最多用一次，以及不同歷史何時能共用 cache 答案；重做日期待確認。
- [ ] LeetCode 494. Target Sum
  - 📌 標記原因: 2026-10-21 經提示練習，使用者表示完全靠 gpt-6.1-sol review，目前仍不行、尚未獨立完成。尤其難以自行想到用總和界定 range，再處理 offset 與 index 越界；不能視為已掌握。Recursive → top-down Counting DP 較直覺，bottom-up 則與 LC 91 是第二次遇到同類障礙。
  - 重練目標: 分開處理狀態語義與填表順序；解釋 W±nums[i] 的來源、0 的兩種符號計數、值域 offset 與 target 越界檢查。
  - [ ] 獨立重建：從 S=sum(nums) 推導 [-S,S]，說明為何配置 2S+1 格、如何映射 W+S，並區分 target 範圍與轉移來源範圍；重做日期：—。
  - [ ] Convert to Subset Sum problem
- [x] LeetCode 567. Permutation in String
  - [x] Sliding Window (Frequency Counting)：2026-11-04 已提供實作；經討論釐清「至少達標」的種類計數與固定長度迫使頻率相等的 invariant。
- [ ] LeetCode 572. Subtree of Another Tree
  - 📌 標記原因: 已用逐點遞迴 + Same Tree 完成；想另外練 string matching 與 canonical form compare，並各做一系列相關題目。
  - [ ] String matching 系列：LC 28. Find the Index of the First Occurrence in a String 練 KMP / Z-algorithm → 回來做 LC 572 的先序序列化 + 字串比對；保留空節點與值的邊界，避免不同樹得到相同字串。
  - [ ] Canonical form 系列：LC 652. Find Duplicate Subtrees 練有序子樹簽章 → 回來用 post-order `(value, leftID, rightID)` 比較 LC 572 的子樹；兩棵樹共用 ID 字典。
  - [ ] LC 951. Flip Equivalent Binary Trees：延伸比較允許左右翻轉時的 canonical form；此題也已在本清單獨立列出。
  - [ ] 子樹雜湊（Merkle hashing）/ Tree hashing：若用固定長度 hash 判等，釐清碰撞風險與驗證方式。
  - 🏷️ 技巧分類: String Matching / Tree Serialization / Canonical Form / Tree Hashing
  - 🔗 前置閱讀: [KMP String Matching 練習路徑](../Trick%20Practice/KMP_String_Matching_Playbook.md)、[Canonicalization](../../Algorithms/Design_Principles/Canonicalization.md)、[Binary Tree Canonical Forms](../../Data_Structures/Trees/Binary_Trees/Canonical_Forms_Transformation.md)
- [ ] LeetCode 73. Set Matrix Zeroes
  - [ ] Hash Table Optimization (Space Optimization)
- [ ] LeetCode 131. Palindrome Partitioning
  - [ ] Backtracking
  - [ ] Dynamic Programming
- [ ] LeetCode 417. Pacific Atlantic Water Flow
  - 2026-10-22 已練反向 DFS／destination as source；程式邊界初始化漏掉 Pacific 左下角與 Atlantic 右上角，待確認修正，暫不標記複習完成。
- [ ] LeetCode 143. Reorder List
  - [ ] Space O(1)
- [ ] LeetCode 22. Generate Parentheses
  - 從結構唯一性的分解方式下去想 -> Divide and Conquer -> Dynamic Programming

- [ ] LeetCode 33. Search in Rotated Sorted Array
  - 📌 標記原因: 思路盲點 — 做過多次仍錯，根源是混用 153 的「找拐點」predicate；33 是「找 sorted 半邊 → range check → prune 另一半」
  - 🏷️ 技巧分類: Binary Search（predicate 設計）
  - 🔗 前置閱讀: `Binary_Search/03-Peak_and_Rotated_Array_Search.md` 的「33 vs 153 對照」節
  - 📅 二刷: 2026-09-12
- [ ] LeetCode 39. Combination Sum
  - 📌 標記原因: 已用二元「選/不選」樹過，補 N 多叉決策樹版；複雜度分析 `O(2^(N+T/M))` vs `O(N^(T/M))` 要能自己推
  - 🏷️ 技巧分類: Backtracking（二元 vs 多叉 state space tree）
  - 🔗 前置閱讀: `Backtracking/05-State_Space_Tree_and_N_Tuple_Representation.md`
  - 📅 二刷: 2026-09-13
- [ ] LeetCode 104. Maximum Depth of Binary Tree / 226. Invert Binary Tree
  - 📌 標記原因: 遞迴版秒殺，迭代版待補；面試官會在遞迴寫太快時追問迭代。兩題同一個模板，集中一次練完
  - 🏷️ 技巧分類: Iterative Tree Traversal（explicit stack）
  - 🔗 前置閱讀: `Trees/Iterative_Traversal/01-Recursive_to_Iterative_Conversion.md`
  - 📅 二刷: 累積到 4–5 題 tree DFS 後一起做
- [ ] LeetCode 139. Word Break
  - 📌 標記原因: 技巧盲點 — Trie + DFS 寫了 40 分鐘還 TLE，原因是把「dp[i] = 後綴可切」和「查字典」揉在同一個 DFS 裡，看不出少了 memo
  - 🏷️ 技巧分類: 1-D DP + Trie / Memoized DFS
  - 📅 二刷: 2026-09-13（先寫樸素 `dp[i] = any(dp[j] && s[j..i) ∈ set)`，過了再把 set 換 Trie）
  - 📅 三刷: 2026-09-25（連 140 Word Break II 一起）
- [ ] LeetCode 146. LRU Cache
  - 📌 標記原因: 實作細節 — 思路對但四版才過（巢狀型別解析、dummy 尾、淘汰三步、get 要 refresh）；本質是 map + list 兩個結構同步維護不變量
  - 🏷️ 技巧分類: Design / Hash Map + Doubly Linked List
  - 📅 二刷: 2026-09-14（目標：一次寫對，先列出每個操作要維護的不變量再動手）
  - 📅 三刷: 2026-09-25（連 460 LFU 一起）
- [ ] LeetCode 230. Kth Smallest Element in a BST
  - 📌 標記原因: 實作細節 — 同一天做兩次都錯很多次；卡在「可變狀態 + early return + 帶答案回傳」三者的簽名設計，第一版還用了 `-1` sentinel
  - 🏷️ 技巧分類: In-order Traversal + External State / Recursion Signature Design
  - 🔗 前置閱讀: `Divide_and_Conquer/06_External_State_Traversal_Order.md`、`Trees/Iterative_Traversal/03-Current_Pointer_Implementations.md`
  - 📅 二刷: 2026-09-16（直接寫 iterative in-order 版，不需要那三個欄位）
  - 📅 三刷: 2026-09-28（加 follow-up：augmented BST subtree size）
- [ ] LeetCode 23. Merge k Sorted Lists（bottom-up D&C 版）
  - 📌 標記原因: top-down D&C 已通過；想練 bottom-up 版（interval 倍增 + 原地配對合併），for loop 的 index 設計是重點
  - 🏷️ 技巧分類: Bottom-Up Divide and Conquer / Iterative Merge
  - 🔗 前置閱讀: `Divide_and_Conquer/04_Bottom_Up_Divide_and_Conquer.md`
  - 📅 二刷: 2026-09-18（另外再寫 priority_queue 版，比較兩者同為 O(N log k) 的來源）
- [ ] LeetCode 229. Majority Element II（169 的延伸，下次做）
  - 📌 標記原因: 做完 169 後的指定延伸 — 逼出 Boyer-Moore 的推廣形式（>n/k 需要 k-1 個候選），以及「第二輪驗證為何必須」（169 題目保證多數元素存在才能省，229 不保證）
  - 🏷️ 技巧分類: Boyer-Moore Voting (n/k 推廣)
  - 🔗 前置閱讀: `Algorithms/Boyer_Moore_Voting/Boyer_Moore_Voting_Algorithm.md` Pattern 2
  - 📅 下次練習: 2026-09-16
- [ ] LeetCode 169. Majority Element（D&C 版，選做）
  - 📌 標記原因: 不是為了解這題，而是它是 **D&C 的非典型 combine** — 左右各自的多數元素未必是整體的多數元素，combine 時必須回頭數一次，這就是 O(n log n) 的來源。與 LC 23「兩條已排序 list 直接接起來」形成對照
  - 🏷️ 技巧分類: Divide and Conquer (combine 需額外驗證)
  - 🔗 前置閱讀: `Divide_and_Conquer/05_Conquer_Strategy_Comparison.md`
  - 📅 選做: 229 完成後
- [ ] LeetCode 42. Trapping Rain Water（monotonic stack 版）
  - 📌 標記原因: 前三種解法（brute force / prefix-suffix max / two pointers）都是**逐格、直著算**；單調棧是**逐層、橫著算**，是第四種分解方式。最初卡住時那個「找下一根更高的柱子」的直覺，正是它的核心操作 — 當時走錯方向，現在回頭把它補完
  - 🏷️ 技巧分類: Monotonic Stack / 同一題多解對照
  - 🔗 前置閱讀: `Data_Structures/Stacks_and_Queues/` 單調棧相關筆記
  - 📅 下次練習: 2026-09-19（寫完後把四種解法的分解方式列成一張對照表）
- [ ] LeetCode 205 / 890. Isomorphic Strings / Find and Replace Pattern
  - 📌 標記原因: 49 之後的正規化練習 — 正規形式從「字母計數」換成「**依首次出現順序重編號**」（`abb` 和 `xyy` 都正規化成 `0,1,1`）。這種 key 沒建過；205 另藏一個坑：**映射必須雙向**，只檢查單向會把 `ab → aa` 判成同構
  - 🏷️ 技巧分類: Canonical Form (分組用途) / Hash Map 雙向映射
  - 🔗 前置閱讀: `Divide_and_Conquer/08_Canonical_Anchor_Decomposition.md`「正規化的另一種用途：分組」
  - 📅 下次練習: 2026-09-19（42 之後）
- [ ] LeetCode 73. Set Matrix Zeroes（O(1) space 版，重寫一次）
  - 📌 標記原因: 第一次自己想到「拿一列一行當標記區」但寫錯了 — 標記區整個落在掃描區內（讀到自己剛寫的標記當成原始資料），且角落那格身兼兩職。**方向是對的，死在三項機械檢查**，值得在不看筆記的情況下重寫一次驗收
  - 🏷️ 技巧分類: In-Place Marking（把輸入當輔助空間）
  - 🔗 前置閱讀: `Algorithms/Design_Principles/In_Place_Marking.md`
  - 📅 下次練習: 之後安排（寫完再往下接 448 → 41，把「借正負號」與「搬到正確位置」兩種載體補齊）
- [ ] LeetCode 78. Subsets（改用模式 B 重寫一次）
  - 📌 標記原因: 第一次寫的是「每個元素選 / 不選」的二元遞迴（解在葉節點）。下次改用另一種形狀：**從 choice set 挑「下一個加入誰」→ `start` 當不變量的守衛（索引嚴格遞增，防重複，不是為了切子問題）→ 答案推在每個被拜訪的節點**。這是 46 / 131 / 39 / 77 共用的通用形狀，二元版只在「每個元素獨立選或不選」時才存在
  - 🏷️ 技巧分類: Backtracking 模式 B（解在所有節點）/ 不變量驅動的參數設計
  - 🔗 前置閱讀: `Algorithms/Backtracking/07-Guards_from_Invariants.md`「遞迴參數也是不變量推出來的」、`01-Backtracking_Templates_and_Patterns.md` 模式 A vs 模式 B
  - 📅 下次練習: 之後安排（寫完接 90 Subsets II，把第二條去重不變量「排序 + 同層跳過相同值」補齊）
- [ ] LeetCode 128. Longest Consecutive Sequence（錨點版，重寫一次）
  - 📌 標記原因: 第一次是看 tag 才做出 hashmap + DFS 連通分量，答案對但常數極大（兩個 hash 容器、遞迴深度等於序列長度、`operator[]` 誤插入）。正解只有 8 行、**不需要 `visited`**：`if (s.count(x-1)) continue;` —— 只從「沒有前驅的元素」出發，每個值一生只被自己那段的起點走過一次
  - 🏷️ 技巧分類: Canonical Anchor（結構決定的起點）/ 用結構保證取代檢查
  - 🔗 前置閱讀: `Algorithms/Divide_and_Conquer/08_Canonical_Anchor_Decomposition.md`、`Interview_Playbook/Problem_Solving_Strategies.md` BUD Optimization
  - 📅 下次練習: 之後安排（重點不是背那一行，是自己走完「直覺雜湊版是 O(n²) → 哪些工作重複了 → 只讓起點走」這條鏈）
