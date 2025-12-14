# 快速決策地圖 (Quick Decision Map)

## 🎯 30 秒決策流程

```
1. Intent (問什麼?)
2. Domain (什麼結構?)
3. Constraint (限制?) + Complexity (n 範圍?)
4. Statefulness (記憶策略?)
5. → Technique
```

---

## 1️⃣ Intent：問題要求什麼輸出？

| Intent                    | 關鍵字                           | 典型技術                                   |
| :------------------------ | :------------------------------- | :----------------------------------------- |
| **Boolean** (判斷)        | can, is, exists, possible, valid | DFS/BFS, Feasible DP, Stack, Two Pointers  |
| **Counting** (計數)       | count, ways, number of           | Counting DP, Combinatorics, DFS/BFS        |
| **Optimization** (最佳化) | min, max, longest, shortest      | DP, Greedy, Binary Search                  |
| **Construction** (建構)   | build, generate, create          | Backtracking, Recursion, Greedy            |
| **Selection** (選擇)      | find, choose, kth, top k         | Binary Search, Heap, Quickselect, Hash Map |
| **Transformation** (轉換) | convert, reverse, rotate         | Two Pointers, Recursion                    |

---

## 2️⃣ Domain：處理什麼資料結構？

| Domain                   | 關鍵字                       | 典型技術                                                    |
| :----------------------- | :--------------------------- | :---------------------------------------------------------- |
| **Sequence** (陣列/字串) | array, string, 順序          | DP, Two Pointers, Sliding Window, Binary Search, Prefix Sum |
| **Graph** (圖)           | nodes, edges, paths          | DFS/BFS, Dijkstra, Union-Find, Topological Sort             |
| **Tree** (樹)            | parent-child, hierarchy, BST | DFS, BFS, Tree DP, Traversal                                |
| **Interval** (區間)      | range, start/end, overlap    | Sweep Line, Sort + Greedy, Merge, Difference Array          |
| **Grid** (矩陣)          | 2D array, coordinates        | BFS (最短), DFS (可達), DP                                  |
| **Set** (集合)           | unique, distinct, frequency  | Hash Map/Set, Bitmask, Multiset                             |

---

## 3️⃣ Constraint：約束條件指向什麼技術？

| Constraint               | 關鍵字                           | 技術指向                                  |
| :----------------------- | :------------------------------- | :---------------------------------------- |
| **Resource** (資源)      | capacity, budget, O(n)           | Knapsack DP, Greedy                       |
| **Ordering** (順序)      | before, after, precedence        | Topological Sort, DP (順序)               |
| **Positional** (位置)    | adjacent, boundary, coordinate   | Coordinate DP, BFS (Grid)                 |
| **Compositional** (組合) | partition, subset, decomposition | DP (分割), Backtracking, Divide & Conquer |
| **Structural** (結構)    | connected, acyclic, balanced     | DFS/BFS, Union-Find                       |
| **Temporal** (時間)      | schedule, event, time window     | Sweep Line, Priority Queue                |

---

## 4️⃣ Complexity：n 範圍允許什麼複雜度？

| n 範圍 | 最大複雜度      | 允許技術                                |
| :----- | :-------------- | :-------------------------------------- |
| ≤10    | O(n!)           | Backtracking, Permutations              |
| ≤20    | O(2^n)          | Bitmask DP, Subset Enumeration          |
| ≤100   | O(n³)           | Floyd-Warshall, 3D DP                   |
| ≤1000  | O(n²)           | 2D DP, All Pairs                        |
| ≤10⁵   | O(n log n)      | Sort, Binary Search, Heap, Segment Tree |
| ≤10⁶   | O(n)            | Hash, Prefix Sum, Union-Find            |
| >10⁶   | O(log n) / O(1) | Math, Binary Search Only                |

---

## 5️⃣ Statefulness：需要記憶什麼？

| Level                   | 特徵               | 技術                                                  |
| :---------------------- | :----------------- | :---------------------------------------------------- |
| **Stateless** (無狀態)  | 一次掃描、無需記憶 | Sort, Greedy Scan                                     |
| **Local** (局部)        | 最近 k 個元素      | Priority Queue, Sliding Window, Monotonic Stack/Queue |
| **Global** (全域)       | 所有子問題         | DP, Memoization                                       |
| **Event-Driven** (事件) | 時間排序           | Sweep Line, Priority Queue, Difference Array          |

---

## 📊 Intent × Domain 快速矩陣

| Intent ↓ / Domain → | Sequence      | Graph       | Tree       | Interval    | Grid       |
| :------------------ | :------------ | :---------- | :--------- | :---------- | :--------- |
| **Boolean**         | Two Pointers  | DFS/BFS     | Traversal  | Sweep Line  | BFS/DFS    |
| **Counting**        | DP            | Graph DP    | Tree DP    | Event Count | Grid DP    |
| **Optimization**    | DP/Greedy     | Dijkstra/DP | Tree DP    | Greedy      | Grid DP    |
| **Construction**    | Backtrack     | Path Build  | Tree Build | Merge       | State BFS  |
| **Selection**       | Binary Search | Search      | Query      | Query       | Coordinate |

---

## 🎯 常見問題模式 (Problem Patterns)

```
"k-th element"              → Quick Select, Heap, Binary Search
"All pairs"                 → O(n²) DP, Floyd-Warshall
"All subsets/permutations"  → Backtracking
"Subarray sum = k"          → Prefix Sum + Hash
"Longest/shortest substring"→ Sliding Window, DP
"Valid parentheses"         → Stack
"Range queries"             → Prefix Sum, Segment Tree
"Median in stream"          → Two Heaps
"Top k"                     → Heap, Bucket Sort
"Detect cycle"              → Floyd's / DFS Coloring
```

**輸入特性 (Input Properties)**：

```
已排序 (Sorted)   → Binary Search, Two Pointers, Merge Sort D&C
未排序 (Unsorted) → 先 Sort 或用 Heap
加權圖 (Weighted) → Dijkstra (≥0) / Bellman-Ford
無權圖 (Unweighted)→ BFS 最短路徑
DAG              → Topological Sort, DAG DP
```

---

## 🔀 Cross-Cutting Patterns (跨領域模式)

> 當基本維度無法直接指引時，用這些抽象模式重新詮釋問題。

| Pattern                     | 關鍵字                              | 典型技術                                       |
| :-------------------------- | :---------------------------------- | :--------------------------------------------- |
| **Interval** (區間)         | range, interval, merge, overlap     | Sweep Line, Sort + Merge, Binary Search        |
| **Path** (路徑)             | path, route, sequence with choices  | DFS, DP, Backtracking                          |
| **Partition** (分割)        | partition, split, divide, group     | DP (分割), Quickselect, Union-Find             |
| **Matching** (配對)         | match, pair, corresponding          | Stack (括號), Hash Map, Bipartite Matching     |
| **Aggregation** (聚合)      | aggregate, combine, accumulate      | Prefix Sum, Tree DP, Segment Tree              |
| **Search Space** (搜尋空間) | explore, state space, possibilities | Backtracking, Binary Search (答案), BFS (狀態) |

---

## ⚖️ Intent × Constraint 技術指引

> 當 Constraint 明確時，可直接縮小技術範圍。

| Intent             | Constraint         | 技術指向                    |
| :----------------- | :----------------- | :-------------------------- |
| **Boolean**        | O(log n) time      | Binary Search               |
|                    | O(1) space         | Two Pointers, Math          |
|                    | 已排序             | Binary Search, Two Pointers |
|                    | 無環圖             | Topological Sort            |
| **Counting**       | O(n²) acceptable   | 2D DP                       |
|                    | O(n) required      | Linear DP, Math Formula     |
|                    | 子集合和           | 0/1 Knapsack DP             |
| **Optimization**   | O(log n) per query | Binary Search, Segment Tree |
|                    | O(1) space         | DP State Reduction          |
|                    | 不相鄰             | DP (Max of Skip/Take)       |
| **Construction**   | 指數可接受         | Backtracking (Generate All) |
|                    | 必須 O(n)          | Greedy, Single Pass         |
|                    | 依賴順序           | Topological Sort            |
| **Selection**      | O(n) time          | Hash Map, Two Pointers      |
|                    | O(log n) time      | Binary Search               |
|                    | 第 K / Top K       | Heap, Quickselect           |
| **Transformation** | O(1) space         | In-place Algorithm          |
|                    | 保持順序           | Stable Transformation       |

---

## 🛠️ 技術驗證檢查表

| 技術                 | 何時使用            | 驗證方式                  |
| :------------------- | :------------------ | :------------------------ |
| **Two Pointers**     | Sequence, 雙向/同向 | 不變量成立                |
| **Sliding Window**   | 連續子陣列/子字串   | 單調性質                  |
| **Binary Search**    | 已排序或單調函數    | Valid/Invalid 分界        |
| **Greedy**           | 局部最優 → 全域最優 | Exchange Argument         |
| **DP**               | 重疊子問題          | 定義遞迴關係              |
| **Backtracking**     | 所有解、CSP         | 狀態空間可探索            |
| **DFS/BFS**          | Graph 遍歷          | DFS: 訪問順序 / BFS: 最短 |
| **Union-Find**       | 連通性、分組        | 集合成員查詢              |
| **Topological Sort** | DAG、依賴關係       | 無環                      |
| **Sweep Line**       | Intervals、事件     | 事件可排序                |

---

## ✅ 最終檢查清單

```
☐ Intent? (要回傳什麼)
☐ Domain? (什麼結構)
☐ Constraint? (約束類型)
☐ Complexity? (n 範圍)
☐ Statefulness? (記憶策略)
☐ 技術驗證? (驗證條件成立)
☐ Edge Cases? (空、單一、重複)
```

---

## 📝 實戰應用流程

1. **讀題 → 識別 Intent**：問題最終要求什麼？
2. **看輸入 → 識別 Domain**：處理什麼資料結構？
3. **查矩陣 → 初步選擇**：Intent × Domain → 候選技術
4. **看 n 範圍 → Complexity 篩選**：排除超時技術
5. **找限制 → Intent × Constraint 精準定位**：進一步縮小範圍
6. **判斷記憶 → Statefulness**：決定狀態管理方式
7. **驗證 → 技術檢查表**：確認技術適用條件成立
