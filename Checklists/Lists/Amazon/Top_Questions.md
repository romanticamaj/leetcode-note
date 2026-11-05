# Amazon Top Questions 練習清單

[返回 Amazon 練習總表](README.md)

來源：[LeetCode — Top Amazon Questions](https://leetcode.com/problem-list/7p5x763/)。

**擷取日期：2026-11-05｜共 50 題：3 Easy、27 Medium、20 Hard｜🔒 Premium：11 題**

本檔完整收錄指定清單，保留 LeetCode 清單 API 回傳的順序；**順序不代表近期出題頻率**。這是一般 Amazon coding 練習清單，尚未確認與 Embedded Software Engineer「兩題、135 分鐘」OA 使用相同題庫。

題號、題名、難度與 Premium 標記直接取自 LeetCode；技巧分類與下方練習順序是整理建議。

## 使用方式

- 🟢 Easy／🟡 Medium／🔴 Hard；🔒 表示題目需要 Premium。
- 完成勾選只依 [Practice Log](../../Practice_Log.md) 的紀錄；已刷不代表已完成所有變體或能獨立重寫。
- **已刷：12 / 50**（2026-11-06 快照）。本檔未納入 `scripts/sync_lists.py` 的自動同步範圍；後續更新完成狀態仍須核對 Practice Log。

## OA 複習建議

**目前 OA 優先順序**：先看 [Amazon Explore 的 Editor’s choice 分類](Explore_Editors_Choice.md)，優先練習 OA 明確標註的 5 題（尚無日誌紀錄的 819、937 先做）；下方 12 題保留為題型補強。

時間有限時，可先按這個順序做 12 題，涵蓋排序、字串、heap、prefix、DP、BFS 與指標實作：

**2357 → 1710 → 937 → 767 → 2055 → 2100 → 2222 → 1567 → 973 → 994 → 138 → 146**

這是依題型覆蓋與難度安排的練習順序，並非 Amazon 出題機率排名。已刷過的題目可直接限時重寫；Hard 題可等基礎題型穩定後再補。

## 完整清單（LeetCode 回傳順序）

- [ ] **2357.** [Make Array Zero by Subtracting Equal Amounts](https://leetcode.com/problems/make-array-zero-by-subtracting-equal-amounts/) — 🟢 Easy · Hash Set / Greedy
- [x] **138.** [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) — 🟡 Medium · Linked List / Hash Map · <sub>✔ 2026-09-21</sub>
- [ ] **767.** [Reorganize String](https://leetcode.com/problems/reorganize-string/) — 🟡 Medium · Greedy / Heap
- [ ] **140.** [Word Break II](https://leetcode.com/problems/word-break-ii/) — 🔴 Hard · Backtracking / Memoization
- [ ] **863.** [All Nodes Distance K in Binary Tree](https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/) — 🟡 Medium · Tree / BFS / DFS
- [x] **994.** [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) — 🟡 Medium · Multi-source BFS · <sub>✔ 2026-09-22</sub>
- [x] **273.** [Integer to English Words](https://leetcode.com/problems/integer-to-english-words/) — 🔴 Hard · String / Simulation · <sub>✔ 2026-11-05</sub>
- [x] **146.** [LRU Cache](https://leetcode.com/problems/lru-cache/) — 🟡 Medium · Hash Map / Doubly Linked List · <sub>✔ 2026-09-11</sub>
- [ ] **2398.** [Maximum Number of Robots Within Budget](https://leetcode.com/problems/maximum-number-of-robots-within-budget/) — 🔴 Hard · Sliding Window / Monotonic Queue
- [x] **2221.** [Find Triangular Sum of an Array](https://leetcode.com/problems/find-triangular-sum-of-an-array/) — 🟡 Medium · Array / Simulation · <sub>✔ 2026-11-05</sub>
- [ ] **2222.** [Number of Ways to Select Buildings](https://leetcode.com/problems/number-of-ways-to-select-buildings/) — 🟡 Medium · Prefix Counts / Counting DP
- [ ] **1567.** [Maximum Length of Subarray With Positive Product](https://leetcode.com/problems/maximum-length-of-subarray-with-positive-product/) — 🟡 Medium · State Machine DP
- [ ] **2100.** [Find Good Days to Rob the Bank](https://leetcode.com/problems/find-good-days-to-rob-the-bank/) — 🟡 Medium · Prefix / Suffix
- [ ] **2386.** [Find the K-Sum of an Array](https://leetcode.com/problems/find-the-k-sum-of-an-array/) — 🔴 Hard · Sorting / Heap
- [ ] **2102.** [Sequentially Ordinal Rank Tracker](https://leetcode.com/problems/sequentially-ordinal-rank-tracker/) — 🔴 Hard · Heap / Ordered Set
- [x] **545.** [Boundary of Binary Tree](https://leetcode.com/problems/boundary-of-binary-tree/) — 🟡 Medium 🔒 · Tree Traversal · <sub>✔ 2026-11-05</sub>
- [ ] **2262.** [Total Appeal of A String](https://leetcode.com/problems/total-appeal-of-a-string/) — 🔴 Hard · Contribution Counting / Last Occurrence
- [ ] **1710.** [Maximum Units on a Truck](https://leetcode.com/problems/maximum-units-on-a-truck/) — 🟢 Easy · Sorting / Greedy
- [x] **295.** [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) — 🔴 Hard · Two Heaps · <sub>✔ 2026-09-27</sub>
- [x] **42.** [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) — 🔴 Hard · Two Pointers / Monotonic Stack · <sub>✔ 2026-09-18</sub>
- [ ] **2340.** [Minimum Adjacent Swaps to Make a Valid Array](https://leetcode.com/problems/minimum-adjacent-swaps-to-make-a-valid-array/) — 🟡 Medium 🔒 · Array / Greedy
- [ ] **1603.** [Design Parking System](https://leetcode.com/problems/design-parking-system/) — 🟢 Easy · Design / Counting
- [x] **49.** [Group Anagrams](https://leetcode.com/problems/group-anagrams/) — 🟡 Medium · Hash Map / String · <sub>✔ 2026-09-18</sub>
- [ ] **2214.** [Minimum Health to Beat Game](https://leetcode.com/problems/minimum-health-to-beat-game/) — 🟡 Medium 🔒 · Greedy
- [ ] **2104.** [Sum of Subarray Ranges](https://leetcode.com/problems/sum-of-subarray-ranges/) — 🟡 Medium · Monotonic Stack / Contribution Counting
- [ ] **2272.** [Substring With Largest Variance](https://leetcode.com/problems/substring-with-largest-variance/) — 🔴 Hard · DP / Enumeration
- [ ] **2355.** [Maximum Number of Books You Can Take](https://leetcode.com/problems/maximum-number-of-books-you-can-take/) — 🔴 Hard 🔒 · Monotonic Stack / DP
- [ ] **1291.** [Sequential Digits](https://leetcode.com/problems/sequential-digits/) — 🟡 Medium · Enumeration
- [ ] **2281.** [Sum of Total Strength of Wizards](https://leetcode.com/problems/sum-of-total-strength-of-wizards/) — 🔴 Hard · Monotonic Stack / Prefix Sum
- [ ] **818.** [Race Car](https://leetcode.com/problems/race-car/) — 🔴 Hard · DP / State-space Search
- [x] **200.** [Number of Islands](https://leetcode.com/problems/number-of-islands/) — 🟡 Medium · DFS / BFS / Union-Find · <sub>✔ 2026-09-14</sub>
- [ ] **1597.** [Build Binary Expression Tree From Infix Expression](https://leetcode.com/problems/build-binary-expression-tree-from-infix-expression/) — 🔴 Hard 🔒 · Stack / Expression Tree
- [ ] **1864.** [Minimum Number of Swaps to Make the Binary String Alternating](https://leetcode.com/problems/minimum-number-of-swaps-to-make-the-binary-string-alternating/) — 🟡 Medium · String / Greedy
- [ ] **588.** [Design In-Memory File System](https://leetcode.com/problems/design-in-memory-file-system/) — 🔴 Hard 🔒 · Design / Trie
- [ ] **2193.** [Minimum Number of Moves to Make Palindrome](https://leetcode.com/problems/minimum-number-of-moves-to-make-palindrome/) — 🔴 Hard · Two Pointers / Greedy
- [ ] **937.** [Reorder Data in Log Files](https://leetcode.com/problems/reorder-data-in-log-files/) — 🟡 Medium · String / Custom Sorting
- [x] **207.** [Course Schedule](https://leetcode.com/problems/course-schedule/) — 🟡 Medium · Topological Sort / Cycle Detection · <sub>✔ 2026-09-14</sub>
- [ ] **719.** [Find K-th Smallest Pair Distance](https://leetcode.com/problems/find-k-th-smallest-pair-distance/) — 🔴 Hard · Binary Search on Answer / Two Pointers
- [ ] **1152.** [Analyze User Website Visit Pattern](https://leetcode.com/problems/analyze-user-website-visit-pattern/) — 🟡 Medium 🔒 · Hash Map / Sorting / Enumeration
- [ ] **828.** [Count Unique Characters of All Substrings of a Given String](https://leetcode.com/problems/count-unique-characters-of-all-substrings-of-a-given-string/) — 🔴 Hard · Contribution Counting
- [ ] **472.** [Concatenated Words](https://leetcode.com/problems/concatenated-words/) — 🔴 Hard · Trie / DP
- [ ] **348.** [Design Tic-Tac-Toe](https://leetcode.com/problems/design-tic-tac-toe/) — 🟡 Medium 🔒 · Design / Counting
- [ ] **2268.** [Minimum Number of Keypresses](https://leetcode.com/problems/minimum-number-of-keypresses/) — 🟡 Medium 🔒 · Frequency / Sorting / Greedy
- [ ] **1628.** [Design an Expression Tree With Evaluate Function](https://leetcode.com/problems/design-an-expression-tree-with-evaluate-function/) — 🟡 Medium 🔒 · Stack / Tree / Design
- [ ] **239.** [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) — 🔴 Hard · Monotonic Queue
- [ ] **1268.** [Search Suggestions System](https://leetcode.com/problems/search-suggestions-system/) — 🟡 Medium · Sorting / Binary Search / Trie
- [x] **973.** [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) — 🟡 Medium · Heap / Quickselect · <sub>✔ 2026-10-15</sub>
- [ ] **2055.** [Plates Between Candles](https://leetcode.com/problems/plates-between-candles/) — 🟡 Medium · Prefix Sum / Boundary Lookup
- [ ] **253.** [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) — 🟡 Medium 🔒 · Sorting / Heap / Sweep Line
- [ ] **127.** [Word Ladder](https://leetcode.com/problems/word-ladder/) — 🔴 Hard · BFS / Bidirectional BFS

## LeetCode Discuss：實際問法與面經

查閱日期：2026-11-05。以下是公開面經的摘要；**個別考生回報與社群彙整不能當成出題頻率或通過門檻**。

### 指定文章：SDE II 近六個月彙整（Part 1）

來源：[Questions asked by Amazon in past 6 months — SDE2 (DSA/Design), Part 1](https://leetcode.com/discuss/post/8519174/questions-asked-by-amazon-in-past-6-mont-zxfk/)，2026-09-13 發表、09-14 更新。這是作者蒐集多篇面經的彙整，混合 coding、LLD／HLD 與行為題，未逐項標明面試日期與關卡；不能直接視為 Embedded OA 題庫。本次只整理已讀到的 Part 1。

| 題型 | 文中實際問法／追問 |
|---|---|
| Graph | 匯率換算追加多次查詢；島嶼改為八方向連通 |
| Stack | 支援 O(1) 取中間元素；去重字母改求字典序最大 |
| Tree | 不提供 parent pointer，求兩節點距離 |
| Heap | 到貨時間逐筆加入，每次回報中位數 |
| LLD | Pub/Sub 訂閱管理；通知依優先度分流 |
| Concurrency | 最後一件庫存遇到同時下單，如何避免超賣 |

注意：原文有重複題與編號混雜；中位數範例看似採偶數筆取較小中間值，實作前應確認定義。上述八方向島嶼也不能直接套用原題的四方向規格。

### Embedded 職缺的直接回報

- [SDE I — Embedded systems（2025-02-02）](https://leetcode.com/discuss/post/6362731/Amazon-Interview-experience-and-doubt-%28SDE1-Embedded%29/)：作者已完成的兩關分別問 grid DP／BFS，以及 matrix 題；都搭配 Leadership Principles。作者表示當時只被考 DSA，要求最佳化與模組化程式碼。**這是面試回報，沒有描述 OA**。
- [Senior Embedded Software — 印度（2020 年，歷史案例）](https://leetcode.com/discuss/post/974067/nda-microsoft-amazon-senior-software-engineer-embedded-software-india-offers/)：Amazon 多關包含 Medium DSA、LP、Embedded Design 與工作經驗。作者另建議複習 OS／Linux；那份主題建議不能全部視為實際考題。

### OA 的兩種公開回報

- [SDE II — Texas（2024 年）](https://leetcode.com/discuss/post/5878470/Amazon-SDE-2-Interview-Experience-or-Texas-or-Reject/)：OA 為兩題、90 分鐘，分別涉及 array 與 string；後續面試則問業務情境包裝的 graph／interval 題。
- [SDE I OA — Bitwise 題（2026-10-02）](https://leetcode.com/discuss/post/8552696/)：一題 DSA 加一題 AI-assisted repository。DSA 要在總增量預算內調整陣列，選定數量的元素，最大化其 bitwise AND；作者回報暴力枚舉會 TLE。文章未提供已確認正確的解法。

### 這次準備如何使用

這些回報支持練習「讀情境、確認規格、辨認題型、處理追問」，但**本次查到的 Discuss 文章沒有確認你的兩題、135 分鐘版本**。先依邀請信確認兩題是否都從零寫程式，或含 repository 題，再分配準備時間。

上方 50 題保留為指定清單；本節的題型與變體是面經補充，不計入 50 題或已刷數。

## 來源與核對

- [指定清單：Top Amazon Questions](https://leetcode.com/problem-list/7p5x763/)
- 擷取方式：LeetCode 公開 GraphQL `favoriteQuestionList(favoriteSlug: "7p5x763", limit: 100, skip: 0)`；回傳 `totalLength = 50`，實際取得 50 個不重複題目。
- 題目識別使用 `questionFrontendId` 與 `titleSlug`；難度使用 `difficulty`；Premium 使用 `paidOnly`。
- 本次回傳的 `frequency` 為空值，因此不建立「近 30 天／近 6 個月高頻」排名。
- 完成日期取 Practice Log 中該題最早的練習日期。
