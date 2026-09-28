# 解題 Follow-up 待辦清單

這個文件用來記錄在解題過程中遇到的各種 follow-up 問題、待優化項目、或下次需要深入練習的技巧。

---

## 🌳 樹 (Trees)

- [ ] **比較**：比較 Morris Traversal 與標準遞迴/迭代 traversal 的優缺點。
- [ ] **學習**：研究 Min-Max Heap 和 Deap (Double-ended heap) 資料結構，了解其如何同時高效支援查找最小和最大元素。
- [ ] 子樹雜湊（Merkle hashing）/ Tree hashing
- [ ] **follow-up（295 Approach 4）**：[295. Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) 用 **`multiset` + 中位數 iterator** 取代 two heaps。`std::multiset` 底層是自平衡 BST（紅黑樹），插入 O(log n)；維護一到兩個指向中間的 iterator，每次插入後依新值落在左邊或右邊，把 iterator 往前或往後移一格。
  - 比較：two heaps 只能看兩個堆頂；ordered set 整組有序，所以能**刪除任意元素** → 直接推到 [480. Sliding Window Median](https://leetcode.com/problems/sliding-window-median/)
  - 相關筆記：`Algorithms/Sliding_Window/02-Sorted_Sliding_Window.md`（Ordered Set 版窗口）、`Data_Structures/Heaps/04-Two_Heaps_Balancing.md`

---

## 📈 圖 (Graphs)

- [ ] **研究**：研究 A\* 搜尋演算法，並比較它與 Dijkstra、BFS 的差異。 ([Sliding Puzzle](https://leetcode.com/problems/sliding-puzzle/description/))

---

## 🔢 陣列與字串 (Arrays and Strings)

- [ ] **【必做】整理 Quickselect 心法**（Hoare 選擇演算法，平均 O(n) 找第 k 小）——2026-09-21 刷 [215. Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) 時發現一直沒整理。要點：只遞迴一邊、隨機 pivot 避開最壞 O(n²)、median-of-medians 只需口述、第 k 大 → 索引 `n - k`、寫成 while 迴圈。接 [`Algorithms/Partition/01-Lomuto_Partition_Scheme.md`](../Algorithms/Partition/01-Lomuto_Partition_Scheme.md)，並對照 heap 解的取捨（streaming / 記憶體放不下 → 只能 heap）。
  - follow-up 家族：347 Top K Frequent、703 Kth Largest in a Stream、973 K Closest Points、295 Find Median from Data Stream、4 Median of Two Sorted Arrays。
- [ ] **研究**：研究 Deterministic Finite Automaton (DFA) 在 string parsing 的應用，包含 explicit `enum State` + `transition()` 函數的設計模式。與 Sequential Phase Consumption（隱式 FSM）做比較。([Valid Number](https://leetcode.com/problems/valid-number/))
- [ ] Knuth-Morris-Pratt algorithm

---

## 💡 動態規劃 (Dynamic Programming)

- [ ] **實作 LIS O(n log n)**（[300. Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/)，2026-09-22 做完 O(n²) 版後排入）：自己寫一次 `tails` + `lower_bound`，並把**「為什麼」**補進 [`Data_Structures/Arrays_and_Strings/Subsequence_Problem_Solving_Strategies.md`](../Data_Structures/Arrays_and_Strings/Subsequence_Problem_Solving_Strategies.md) §2（目前只有步驟）：
  - 關鍵：把 dp 的**索引與值對調**——`dp[i]`（結尾位置 → 長度）翻成 `tails[k]`（長度 → 最小結尾），翻過來後單調才能二分
  - `tails` 為何嚴格遞增；為何同長度只留最小結尾（exchange argument：結尾越小後面能接越多）
  - 陷阱：嚴格遞增 `lower_bound` / 非遞減 `upper_bound`；`tails` 不是真正的 LIS，只有長度對
  - 延伸：354 Russian Doll Envelopes（排序後降成 LIS）、673 Number of LIS、1671 Minimum Removals to Make Mountain Array
- [ ] **follow-up（97 Bottom-up）**：[97. Interleaving String](https://leetcode.com/problems/interleaving-string/) 2026-09-28 寫完 top-down memo 後排入。改寫成 bottom-up，再壓成一維。
  - 狀態改講 **prefix**：`dp[i][j]` = `s1` 前 `i` 個 + `s2` 前 `j` 個能否交錯成 `s3` 前 `i+j` 個；base `dp[0][0] = true`；讀字元是 `s1[i-1]` / `s2[j-1]` / `s3[i+j-1]`
  - 第 0 列、第 0 欄要單獨處理（只能從一個字串拿），或在轉移裡用 `i > 0` / `j > 0` 守衛
  - 空間 O(mn) → **滾動陣列 O(n)**：`dp[j]` 更新前的值是「上一列」，`dp[j-1]` 是「這一列」；再把較短的字串放內層可到 O(min(m, n))
  - 相關筆記：[`Data_Structures/Arrays_and_Strings/Index_as_Cut.md`](../Data_Structures/Arrays_and_Strings/Index_as_Cut.md)（suffix ↔ prefix 對照表）、`Algorithms/Dynamic_Programming/Fundamentals/03-TopDown_to_BottomUp.md`（滾動陣列）
- [ ] **研究**：研究矩陣快速冪 (Matrix Exponentiation) 如何將線性遞迴的 DP 問題從 O(N) 優化到 O(logN)，以 Fibonacci 數為例。

---

## 🧮 數學 (Math)

- [ ] **複習**：複習 Catalan Number 的定義、遞迴關係、以及經典應用 (如括號匹配、唯一二元搜尋樹)。

---

## 🔄 回溯 (Backtracking)

- [ ] **重新建立與討論**：重新建立一份關於回溯演算法複雜度分析的完整文件。

---

## 🔑 雜湊表 (Hash Tables)

- [ ] **研究**：研究 hash function 的時間複雜度計算
- [ ] **學習**：深入理解 hash function 的設計原則與實作：key type → key range → bucket number → hash function
- [ ] **研究 (collision handling)**：研究並比較不同的碰撞處理策略：
  - [Separate Chaining](https://en.wikipedia.org/wiki/Hash_table#Separate_chaining): for values with the same hash key, we keep them in a _bucket_, and each bucket is independent of each other.
  - [Open Addressing](https://en.wikipedia.org/wiki/Hash_table#Open_addressing): whenever there is a collision, we keep on _probing_ on the main space with certain strategy until a free slot is found.
  - [2-Choice Hashing](https://en.wikipedia.org/wiki/2-choice_hashing): we use two hash functions rather than one, and we pick the generated address with fewer collision.
- [ ] **實作目標**：完成 **[705. Design HashSet](https://leetcode.com/problems/design-hashset/)** 的實作

---

## 🧮 位元運算 (Bit Manipulation)

- [ ] **follow-up（190 + 191 一起做）**：[190. Reverse Bits](https://leetcode.com/problems/reverse-bits/)、[191. Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/)
  - **divide and conquer（mask 分治）**：用 `0x55555555`、`0x33333333`、`0x0F0F0F0F`… 這組 mask，190 是在每一層交換左右半，191 是在每一層把左右半的 1 的個數相加
  - **fixed precalculated（查表）**：預先算好 256 格的 byte 表（190 存反轉結果、191 存 1 的個數），每次拆成 4 個 byte 查表再合併

---

## ⚙️ 其他

- [ ] **比較**: 在貪婪演算法的脈絡下，深入比較 Bucket Sort 與傳統比較排序 (如 `std::sort`) 和堆 (Heap) 的使用時機與複雜度。

- [ ] **研究 (Bucket Sort)**:
  - 如何根據資料分佈選擇最佳的 bucket 數量？
  - 如何高效地建構 bucket 列表？例如 `vector<vector<int>> bucket(k);` 的適用時機與限制。
