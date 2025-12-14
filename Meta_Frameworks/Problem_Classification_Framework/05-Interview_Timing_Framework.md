# 📘 DSA Design Pattern Roadmap

> 🎯 核心目標：
> 在 **25 分鐘內完成題型辨識 → 解法設計 → 複雜度分析 → 正確實作與驗證**
> 並能在面試中展現清晰的結構化思考。

---

## 🧭 一、整體思維框架

| 層次       | 問題重點                | 思考輸出                     |
| -------- | ------------------- | ------------------------ |
| **問題理解** | 資料結構是什麼？限制條件？       | 明確定義 input / output / 約束 |
| **策略選擇** | 這類結構對應哪種演算法模式？      | 選出 DSA 類型與核心解法           |
| **實作設計** | 狀態怎麼定義？轉移怎麼推？順序怎麼算？ | 寫出狀態、轉移、遍歷順序與複雜度         |

---

## 🩻 二、題型識別表：問題結構 → 演算法方向

| 問題結構                           | 常見關鍵字                            | 推薦策略                                         | 常見複雜度              |
| ------------------------------ | -------------------------------- | -------------------------------------------- | ------------------ |
| **Sequence (Array / String)**  | subarray, substring, contiguous  | Sliding Window / Two Pointers / DP           | O(n)–O(n²)         |
| **Search / Enumeration**       | all combinations, subsets, paths | Backtracking / DFS / Bitmask                 | O(2ⁿ)–O(n!)        |
| **Optimization / Recurrence**  | max/min, optimal, path           | DP / Monotonic Stack / Kadane                | O(n²)              |
| **Interval / Range**           | start/end, overlap, merge        | Sort + Greedy / Sweep Line / Segment Tree    | O(n log n)         |
| **Graph / Connectivity**       | path, reach, connected           | BFS / DFS / Dijkstra / Union-Find            | O(V+E)–O(E log V)  |
| **Tree / Hierarchical**        | parent-child, path, LCA          | DFS / Recursion / Tree DP                    | O(n)               |
| **Sorting / Ranking**          | order, median, frequency         | Custom Sort / Heap / Counting                | O(n log n)         |
| **Binary Search / Decision**   | minimum / threshold / k-th       | Binary Search / Lower Bound                  | O(log n) per check |
| **Prefix / Aggregation**       | sum, range, prefix               | Prefix Sum / Difference Array / Fenwick Tree | O(n)–O(log n)      |
| **String Matching**            | pattern, prefix/suffix           | KMP / Rabin-Karp / Trie / Rolling Hash       | O(n+m)             |
| **Scheduling / Greedy**        | earliest, minimum steps          | Sort + Greedy Decision                       | O(n log n)         |
| **Mathematical / Counting**    | combinatorics, mod               | Math / Modular Arithmetic                    | variable           |
| **Simulation / State Machine** | simulate, step, rules            | Hash + State / BFS / Simulation              | O(n×steps)         |

> 🔍 **練習目標：**
> 題目出現後，30 秒內能說出「這是什麼問題結構 → 應該用什麼演算法」。

---

## 🧠 三、解題三階段（25 分鐘完整流程）

| 時間        | 階段          | 核心目標                    | 具體輸出                            |
| --------- | ----------- | ----------------------- | ------------------------------- |
| 0–5 min   | **題意理解與建模** | 用 input/output 形式明確問題結構 | 確認 constraints、特例               |
| 5–10 min  | **策略選擇與設計** | 找到最合理演算法及狀態轉移           | 定義 state, transition, traversal |
| 10–20 min | **實作與測試**   | 撰寫程式、手動測小樣本             | code + dry-run                  |
| 20–25 min | **驗證與總結**   | 驗證正確性 + 說明 trade-off    | time/space 分析、edge cases        |

---

## 🔭 四、進階目標：建立「心法映射圖」（完整版）

這張圖是你的「解題地圖」，幾乎涵蓋所有 LeetCode 常見題型：

```
問題類型
 ├─ Sequence (Array / String)
 │   ├─ Two Pointers / Sliding Window
 │   ├─ Prefix Sum / Difference Array
 │   ├─ Dynamic Programming
 │   │   ├─ Subsequence DP (LIS, Edit Distance)
 │   │   ├─ Substring DP (Palindrome)
 │   │   └─ Partition / Knapsack DP
 │   ├─ Monotonic Stack / Queue
 │   ├─ Binary Search on Answer
 │   └─ Kadane / Greedy Linear Scan
 │
 ├─ Search / Enumeration
 │   ├─ DFS / Backtracking
 │   ├─ BFS (Layer traversal)
 │   ├─ Bitmask Enumeration
 │   └─ Permutation / Combination Generation
 │
 ├─ Graph
 │   ├─ BFS / DFS Traversal
 │   ├─ Topological Sort / DAG DP
 │   ├─ Shortest Path (Dijkstra / Bellman-Ford)
 │   ├─ Minimum Spanning Tree (Kruskal / Prim)
 │   ├─ Union-Find (Connectivity)
 │   └─ Floyd-Warshall / DP on Graph
 │
 ├─ Tree
 │   ├─ DFS / Postorder DP
 │   ├─ Binary Search Tree / LCA
 │   ├─ Segment Tree / Fenwick Tree
 │   ├─ Recursion / Divide & Conquer
 │   └─ Binary Indexed Tree for range queries
 │
 ├─ Interval & Scheduling
 │   ├─ Sort + Merge / Overlap Detection
 │   ├─ Sweep Line + Event Sorting
 │   ├─ Heap-based Simulation
 │   └─ Greedy (Earliest Finish Time)
 │
 ├─ Searching & Sorting
 │   ├─ Binary Search
 │   ├─ QuickSort / MergeSort
 │   ├─ Counting Sort / Bucket Sort
 │   └─ Partial Selection (Quickselect)
 │
 ├─ String Processing
 │   ├─ Expand Around Center / Manacher
 │   ├─ KMP / Z-function / Rolling Hash
 │   ├─ Trie / Prefix Tree
 │   └─ Aho-Corasick / Automaton
 │
 ├─ Bit Manipulation
 │   ├─ Bitmask DP / Subset Enumeration
 │   ├─ XOR Patterns / Parity Check
 │   └─ State Compression
 │
 ├─ Math / Number Theory
 │   ├─ Modular Arithmetic / Fast Power
 │   ├─ Combinatorics / Factorials
 │   ├─ GCD / LCM / Prime Sieve
 │   └─ Probability / Expected Value
 │
 └─ Simulation / State Machine
     ├─ Time-based Simulation
     ├─ Automaton Transition
     ├─ Hashing State Compression
     └─ Game of Life / Cellular Automaton
```

> 💡 使用方式：
>
> * 每練一題，找出它在這張圖的位置；
> * 若某題跨兩個分支（例如 DP + Binary Search），記錄下這種「混合型解法」。

---

## ⚡ 五、實際問題的切入框架與思考模式

### 1️⃣ 問題結構

* 輸入資料是序列、圖、樹、還是區間？
* 是否要求「連續」？（→ Sliding Window / Substring）
* 是否可拆子問題？（→ DP）
* 是否要求最值？（→ DP / Binary Search / Greedy）

### 2️⃣ 狀態抽象

* 我需要哪些變數描述一個子問題？
* 是否能壓縮狀態或用 index 表示？
* 子問題間是否互相重疊？

### 3️⃣ 轉移關係

* 如何從已解的子問題構成更大的解？
* 是逐步擴張（DP）還是決策前進（Greedy）？
* 是否有方向性（左→右、上→下）？

### 4️⃣ 遍歷順序

* 要先算誰？（確保依賴關係）
* 能否自頂向下記憶化或自底向上填表？
* 是否能以 BFS / Queue 模擬依賴順序？

### 5️⃣ 複雜度檢查

* 暴力法 O(n³) → 可否減少一層？
* 是否能用排序、雙指標、或二分壓到 O(n log n)？
* 時間與空間能否 trade-off？

---

## 🧱 六、練習回饋表（題後筆記模板）

| 問題         | 我的回答 |
| ---------- | ---- |
| 題型分類       |      |
| 初始策略       |      |
| 為何錯或卡？     |      |
| 正確 pattern |      |
| 下次判斷依據     |      |

---

## 🕒 七、Google 面試節奏現實模型

### 📋 官方建議摘要

> **45 分鐘面試 → 約 2~3 題（1 大題 + 2 延伸）**
> 目標：**25 分鐘內完成一題中等難度的 Optimal 解**

### 💡 實際時間配置（建議如下）

| 階段            | 時間               | 內容                              | 目的                          |
| ------------- | ---------------- | ------------------------------- | --------------------------- |
| **0–3 min**   | 快速理解題目           | 重述題意 + 核心要求                     | 展現溝通力                       |
| **3–10 min**  | **問題分析與演算法設計**   | 確定演算法策略（e.g. DP / BFS / Greedy） | ✅ 重點：這階段不用 code，只要能口頭說出正確思路 |
| **10–20 min** | **Coding Phase** | 寫主要解法骨架 + base cases            | 展現熟練度                       |
| **20–25 min** | **測試與修正**        | 驗邊界、dry-run                     | 展現細節嚴謹性                     |
| **25–30 min** | **Follow-up 1**  | 分析 time/space, 提出更優化版本          | 彈性思考                        |
| **30–40 min** | **Follow-up 2**  | 變形題、功能延伸                        | 抽象思考與 generalization        |
| **40–45 min** | **總結 / 自我回顧**    | 講出 trade-off 與改進點               | 結尾強化印象                      |

---

## 🧩 時間分配現實性分析

> ❓「5 分鐘設計好演算法可能嗎？」

✔️ **答案：有條件地可以。**

取決於：

* 你是否能在看到題目時，**立即定位題型類別**；
* 是否有「pattern → 解法樹」的肌肉記憶。

例如：

| 題型                            | 是否能在 5 分鐘內完成設計？              |
| ----------------------------- | ---------------------------- |
| Sliding Window / Two Pointers | ✅ 幾乎都可在 5 分鐘內完成              |
| Binary Search / Greedy        | ✅ 若題意明確                      |
| DP (一維、序列型)                   | ⚠️ 需要 7–10 分鐘分析狀態轉移          |
| Graph / BFS / DFS             | ✅ 若結構簡單（如 grid, word ladder） |
| Interval DP / Hard DP         | ❌ 通常需要 ≥15 分鐘建模              |

> ✅ 建議：
> 面試初期題目（中等難度）應該能在 **7 分鐘內明確講出解法策略 + 複雜度預估**，
> 再花 12 分鐘寫 code，3–5 分鐘測試。

---

## 💬 小結

> 你需要的不是背模板，而是「快速定位 + 有條理地表達」。
>
> 🌱 一開始卡在 30–40 分鐘設計很正常。
> 經過反覆練習與心法歸納後，你會發現：
>
> 「題目分類 → 思維模板 → 狀態轉移 → 實作節奏」
> 才是能讓你在 25 分鐘內穩定輸出的核心能力。