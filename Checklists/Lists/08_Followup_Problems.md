# Follow-up 題型清單

`00_Master_Union.md` 的 250 題是**母題**；這份收的是面試官在你解完母題後**最常追加的那一題**。

所有條目都**不在** Master Union 裡（在裡面的就不列了）。🔥 = 高頻，值得主動準備。

> 來源：LeetCode Discuss「Series Questions」整理 + 個人判斷。頻率標記是判斷，不是統計數據。

---

## 📌 兩種 follow-up

| 類型 | 特徵 | 準備方式 |
| :--- | :--- | :--- |
| **有獨立題號** | 「那如果有重複元素呢？」→ 另一題 | 直接刷（下面 1–13 節） |
| **無獨立題號** | 「能不能 O(1) 空間？」「資料量超過記憶體呢？」 | 想清楚並能口述（第 14 節） |

第 14 節那些**不用寫 code，但一定要能講**，CP 值最高。

---

## 1. Two Pointers / K-Sum

| 母題 | Follow-up | 考什麼 |
| :--- | :--- | :--- |
| 15. 3Sum | 🔥 **16. 3Sum Closest** | 從「找等於」變「找最接近」，指針移動條件要改 |
| 15. 3Sum | 🔥 **18. 4Sum** | 多一層迴圈 + 溢位處理；推廣到 k-Sum 的遞迴寫法 |
| 125. Valid Palindrome | 🔥 **680. Valid Palindrome II** | 允許刪一個字元 → 分岔成兩種嘗試 |
| 167. Two Sum II | **653. Two Sum IV - Input is a BST** | 同一招換資料結構 |

## 2. Boyer-Moore Voting

| 母題 | Follow-up | 考什麼 |
| :--- | :--- | :--- |
| 169. Majority Element | 🔥 **229. Majority Element II** | >n/3 需要 **k-1 = 2** 個候選；**第二輪驗證變成必須**（169 因題目保證存在才能省） |

## 3. Binary Search

| 母題 | Follow-up | 考什麼 |
| :--- | :--- | :--- |
| 33. Search in Rotated | 🔥 **81. Search in Rotated Sorted Array II** | **有重複值**時 `nums[l] == nums[m]` 無法判斷哪半 sorted → 退化成 O(n) |
| 153. Find Minimum in Rotated | 🔥 **154. Find Minimum in Rotated Sorted Array II** | 同上，重複值破壞單調性 |
| 875. Koko Eating Bananas | 🔥 **1011. Capacity To Ship Packages Within D Days** | 同一個「answer space 二分」模板 |
| 875. Koko Eating Bananas | **410. Split Array Largest Sum** | 二分答案 + 貪心驗證，最能看出模板本質 |

## 4. Sliding Window

| 母題 | Follow-up | 考什麼 |
| :--- | :--- | :--- |
| 3. Longest Substring Without Repeating | 🔥 **340. Longest Substring with At Most K Distinct** 🔒 | 從「不重複」推廣到「最多 K 種」 |
| 424. Longest Repeating Char Replacement | 🔥 **1004. Max Consecutive Ones III** | 同一題換皮（把 replacement 想成翻轉 0） |
| 209. Minimum Size Subarray Sum | **862. Shortest Subarray with Sum at Least K** | **有負數** → 滑窗失效，要改 prefix sum + 單調 deque |
| 3. | **395. Longest Substring with At Least K Repeating Characters** | 滑窗不直接適用，要枚舉「字元種類數」或分治 |

## 5. Linked List

| 母題 | Follow-up | 考什麼 |
| :--- | :--- | :--- |
| 146. LRU Cache | 🔥 **460. LFU Cache** | 多一個「頻率」維度 → 兩層 hash + 每個頻率一條 list |
| 21 / 23. Merge Lists | **（口頭）遞迴 vs 迭代兩種都寫** | 空間 O(n) vs O(1) |
| 2. Add Two Numbers | 🔥 **445. Add Two Numbers II** | 高位在前且不准反轉 → 進位方向與走訪方向相反，必須用 stack 或遞迴 |

## 6. Tree

| 母題 | Follow-up | 考什麼 |
| :--- | :--- | :--- |
| 98. Validate BST | 🔥 **99. Recover Binary Search Tree** | 中序找出兩個被交換的節點；Morris 可做到 O(1) 空間 |
| 104. Maximum Depth | **111. Minimum Depth of Binary Tree** | 陷阱：單邊子樹為空時不能取 min |
| 105 / 106. Construct Tree | **889. Construct from Preorder and Postorder** | 前+後序**不唯一**，要解釋為什麼 |
| 297. Serialize and Deserialize Binary Tree | 🔥 **449. Serialize and Deserialize BST** | 利用 BST 性質可以不存 null，編碼更短 |
| 124. Binary Tree Maximum Path Sum | **687. Longest Univalue Path** | 同一個「回傳值 ≠ 答案」的形狀 |
| 236. LCA of Binary Tree | **1650. LCA III（有 parent 指標）** 🔒 | 轉成「兩條鏈的交點」= LC 160 |
| 102. Level Order | **515. Find Largest Value in Each Tree Row** | 每層取特定屬性的變形 |

## 7. Graph

| 母題 | Follow-up | 考什麼 |
| :--- | :--- | :--- |
| 200. Number of Islands | 🔥 **305. Number of Islands II** 🔒 | **動態加陸地** → DFS 每次重掃太慢，非 Union-Find 不可 |
| 127. Word Ladder | 🔥 **126. Word Ladder II** | 從「最短長度」變「列出所有最短路徑」→ BFS 建圖 + DFS 回溯 |
| 684. Redundant Connection | **685. Redundant Connection II** | **有向圖**：要同時處理「入度 2」和「成環」兩種情況 |
| 207 / 210. Course Schedule | **630. Course Schedule III** | 變成貪心 + 堆，跟拓撲排序無關（考你會不會誤套） |
| 200. | **1254. Number of Closed Islands** | 從邊界反向淘汰 |

## 8. Dynamic Programming

| 母題 | Follow-up | 考什麼 |
| :--- | :--- | :--- |
| 139. Word Break | 🔥 **140. Word Break II** | 從「能不能」變「列出所有」→ memo 存的是**方案列表**不是 bool |
| 198. House Robber | 🔥 **337. House Robber III** | 搬到樹上：post-order 回傳 `(偷, 不偷)` 兩個值 |
| 121. Stock 系列 | 🔥 **714. Best Time to Buy and Sell Stock with Transaction Fee** | state machine 的最後一塊拼圖 |
| 300. LIS | 🔥 **673. Number of Longest Increasing Subsequence** | 從「最長」變「有幾個最長」→ 要同時維護長度和計數 |
| 300. LIS | **354. Russian Doll Envelopes** | 二維排序 + LIS；第二維要降序排以避免同寬互套 |
| 5. Longest Palindromic Substring | 🔥 **516. Longest Palindromic Subsequence** | **substring → subsequence**，DP 形狀完全不同 |
| 72. Edit Distance | **583. Delete Operation for Two Strings** | 只允許刪除 → 等價於 LCS |
| 131. Palindrome Partitioning | **132. Palindrome Partitioning II** | 從「列出所有」變「最少切幾刀」→ 回溯變 DP |
| 416. Partition Equal Subset Sum | **698. Partition to K Equal Sum Subsets** | 從 2 份變 k 份 → 回溯 + 剪枝 |
| 62 / 63. Unique Paths | **980. Unique Paths III** | 必須走完所有空格 → 回溯 |
| 312. Burst Balloons | **1039. Minimum Score Triangulation of Polygon** | 同一個區間 DP 骨架 |
| 91. Decode Ways | **639. Decode Ways II** 🔒 | 加入萬用字元 `*` |
| 45. Jump Game II | 🔥 **1306. Jump Game III** | **可左可右** → 可達集合不再是連續區間，區間 greedy 失效，退回真正的 BFS |
| 45. Jump Game II | 🔥 **1696. Jump Game VI** | 骨架不變、目標換成最大分數 → 瓶頸從「枚舉落點」變「查區間最大值」→ 單調佇列 |
| 45. Jump Game II | **1345. Jump Game IV** | 可跳到任何相同值的位置 → BFS + 值分組，用完即清空該組避免重複展開 |

## 9. Backtracking

| 母題 | Follow-up | 考什麼 |
| :--- | :--- | :--- |
| 46. Permutations | 🔥 **47. Permutations II** | **有重複元素**時的去重剪枝（排序 + 跳過同層相同值） |
| 39. Combination Sum | 🔥 **377. Combination Sum IV** | 名字騙人 — **順序不同算不同**，其實是 DP 不是回溯 |
| 39. Combination Sum | **216. Combination Sum III** | 加「剛好 k 個數」的限制 |

## 10. Monotonic Stack

| 母題 | Follow-up | 考什麼 |
| :--- | :--- | :--- |
| 739. Daily Temperatures | 🔥 **503. Next Greater Element II** | **環形陣列** → 掃兩圈或取模 |
| 739. | **496. Next Greater Element I** | 兩個陣列的映射 |
| 84. Largest Rectangle in Histogram | 🔥 **85. Maximal Rectangle** | 逐列轉成直方圖 → 呼叫 84 |
| 739. | **901. Online Stock Span** | 串流版本，單調棧存 `(值, 跨度)` |

## 11. Stack / Parsing

| 母題 | Follow-up | 考什麼 |
| :--- | :--- | :--- |
| 224. Basic Calculator | 🔥 **227. Basic Calculator II** | 加 `*` `/` → 優先級處理 |
| 224 / 227 | **772. Basic Calculator III** 🔒 | 括號 + 四則，兩者合體 |
| 20. Valid Parentheses | **1249. Minimum Remove to Make Valid Parentheses** | 從「判斷」變「修復」 |
| 155. Min Stack | **225. Implement Stack using Queues** | 232 的反向 |

## 12. Intervals / Prefix Sum

| 母題 | Follow-up | 考什麼 |
| :--- | :--- | :--- |
| 56. Merge Intervals | 🔥 **986. Interval List Intersections** | 從「合併」變「求交集」→ 雙指針 |
| 253. Meeting Rooms II | **1094. Car Pooling** | 同一個差分陣列 / sweep line |
| 560. Subarray Sum Equals K | 🔥 **974. Subarray Sums Divisible by K** | prefix sum 改存**餘數** |
| 560. | **523. Continuous Subarray Sum** | 同上 + 長度限制 |

## 13. Design / Bit / Matrix

| 母題 | Follow-up | 考什麼 |
| :--- | :--- | :--- |
| 380. Insert Delete GetRandom O(1) | 🔥 **381. …with Duplicates allowed** | value → **index 集合**，swap-to-end 要改 |
| 136. Single Number | 🔥 **260. Single Number III** | 兩個只出現一次 → 用 lowbit 分組 |
| 54. Spiral Matrix | **59. Spiral Matrix II** | 反過來：生成而非讀取 |
| 208. Trie | **648. Replace Words** | Trie 找最短字根 |
| 347. Top K Frequent Elements | **692. Top K Frequent Words** | 加上**字典序 tie-break** → 比較器設計 |
| 295. Find Median from Data Stream | **480. Sliding Window Median** | 雙堆 + **延遲刪除** |

---

## 14. ⭐ 沒有題號但一定會被問的 follow-up

**這一節 CP 值最高** — 不用寫 code，但要能在 30 秒內講清楚。

| 母題 | 口頭 follow-up | 答案方向 |
| :--- | :--- | :--- |
| 🔥 **238. Product of Array Except Self** | 「輸出陣列不算，能 O(1) 額外空間嗎？」 | 回傳陣列先存 prefix，再用一個變數 running suffix 掃回來 |
| 🔥 **73. Set Matrix Zeroes** | 「能 O(1) 空間嗎？」 | 用第一行/第一列當標記，額外一個變數記第一列本身 |
| 🔥 **138. Copy List with Random Pointer** | 「能 O(1) 額外空間嗎？」 | 把複本交錯插在原節點後面 → 接 random → 拆開 |
| **15. 3Sum** | 「不排序也能做嗎？」（待練習） | 思考合法 index 與 value triplet 去重；與 running hashmap、sort + two pointers 分別追蹤，見 [複習清單](09_Problem_Review.md) |
| 🔥 **215. Kth Largest Element** | 「不用堆呢？」 | Quickselect，平均 O(n)、最壞 O(n²)，隨機化 pivot |
| 🔥 **230. Kth Smallest in BST** | 「如果 BST 頻繁被修改？」 | 節點上 augment **subtree size**，查詢降到 O(h) |
| 🔥 **141. Linked List Cycle** | 「為什麼快慢指針一定會相遇？」「起點怎麼找？」 | 相對速度差 1 必相遇；142 的數學推導 |
| 🔥 **1. Two Sum** | 「如果陣列已排序？」「如果要回傳所有 pair？」 | 排序 → 雙指針 O(1) 空間；所有 pair 要處理去重 |
| **297. Serialize/Deserialize** | 「如果是 BST / N 元樹？」 | 449 / 428 |
| **23. Merge k Sorted Lists** | 「k 很大但每條很短？反過來呢？」 | 影響選 heap（O(N log k)）還是分治 |
| **208. Trie** | 「記憶體太大怎麼辦？」 | 用 hash map 取代 26-array；或壓縮成 Radix Tree |
| **347. Top K Frequent** | 「資料是串流？」「n 極大放不進記憶體？」 | 串流用固定大小 min-heap；超大用 bucket sort / 分散式 count |
| **146. LRU Cache** | 「多執行緒安全？」 | 加鎖的粒度討論；或分片（sharding） |
| **200. Number of Islands** | 「矩陣大到放不進記憶體？」 | 分塊處理 + Union-Find 合併邊界 |
| **任何排序題** | 「穩定嗎？」「in-place 嗎？」 | 知道 `std::sort` 不穩定、`stable_sort` 穩定 |

---

## 📋 使用建議

1. **母題通過後，當天順手看一眼對應的 🔥 follow-up**，通常 10 分鐘內能掌握差異在哪
2. **第 14 節優先** — 那些是「不用刷題就能拿分」的部分
3. Follow-up 的價值不在多解一題，而在**回答「為什麼原本的解法在新條件下會壞掉」**
