# 🎯 問題分類框架 (Problem Classification Framework)

## 🚀 快速開始 (Quick Start)

### 三步驟分類法

```
1. Intent (問什麼？ or Output) → 問題要什麼輸出？
2. Domain (什麼結構？ or Input) → 處理什麼資料結構？
3. Constraint (什麼限制？ or Condition) → 有什麼條件約束？
```

### 使用流程

1. **核心思維**：先學習 [`01-演算法設計三連問.md`](01-演算法設計三連問.md) → State/Transition/Traversal 核心框架
2. **快速分類**：從 [`02-快速決策地圖.md`](02-快速決策地圖.md) 開始 → 30 秒分類流程
3. **深入理解**：參考 [`03-問題分類法.md`](03-問題分類法.md) → Intent/Domain/Constraint 分類維度
4. **技術選擇**：查閱 [`04-解法策略矩陣.md`](04-解法策略矩陣.md) → Intent × Domain 對應
5. **完整流程**：學習 [`05-DSA設計模式路線圖.md`](05-DSA設計模式路線圖.md) → 25分鐘解題流程與題型映射
6. **面試準備**：掌握 [`06-ChatGPT高階心法.md`](06-ChatGPT高階心法.md) → 面試導向快速決策與一頁式速查表

---

## 📁 文件導覽 (Document Guide)

| 順序 | 檔案                                                                | 用途                                | 何時使用                 |
| ---- | ------------------------------------------------------------------- | ----------------------------------- | ------------------------ |
| -    | **[README.md](README.md)**                                          | 框架總覽與使用指南                  | 初次使用、了解架構       |
| 1    | **[01-演算法設計三連問.md](01-演算法設計三連問.md)**                | State/Transition/Traversal 核心框架 | 建立演算法設計基礎思維   |
| 2    | **[02-快速決策地圖.md](02-快速決策地圖.md)**                        | 30 秒決策流程                       | 快速分類、實戰參考       |
| 3    | **[03-問題分類法.md](03-問題分類法.md)**                            | Intent/Domain/Constraint 分類       | 深入理解問題本質         |
| 4    | **[04-解法策略矩陣.md](04-解法策略矩陣.md)**                        | 技術選擇對照表                      | 選擇演算法技術           |
| 5    | **[05-DSA設計模式路線圖.md](05-DSA設計模式路線圖.md)**              | 25 分鐘完整解題流程 + 題型映射圖    | 面試準備、建立解題流程   |
| 6    | **[06-ChatGPT高階心法.md](06-ChatGPT高階心法.md)**                  | 面試導向快速心法與一頁式速查表      | 面試準備、快速模式識別   |

---

## 🎯 四層分類架構 (Four-Layer Architecture)

### Layer 1: Intent Taxonomy (意圖分類)

**問題問什麼？** 六種基本意圖：

- 🔍 **Boolean** - 判斷是非
- 🔢 **Counting** - 計算數量
- ⚡ **Optimization** - 尋找最佳值
- 🏗️ **Construction** - 建構結構
- 🎯 **Selection** - 選擇元素
- 🔄 **Transformation** - 轉換形式

### Layer 2: Domain Taxonomy (領域分類)

**處理什麼結構？** 八種核心領域：

- 📊 Array、📝 String、🎲 Matrix
- 🌲 Tree、🕸️ Graph
- ⏱️ Interval、🔗 LinkedList、🎰 Set

### Layer 3: Constraint Taxonomy (約束分類)

**有什麼限制？** 六種約束類型：

- ⏱️ Resource、📍 Ordering、🎯 Positional
- 🧩 Compositional、🏗️ Structural、⏳ Temporal

### Layer 4: Cross-Cutting Patterns (跨領域模式)

**什麼抽象模式？** 六種通用模式：

- 📏 Interval、🛤️ Path、✂️ Partition
- 🔗 Matching、📊 Aggregation、🔍 Search Space

📖 **詳細內容**：[`03-問題分類法.md`](03-問題分類法.md)

---

## 🧭 使用範例 (Usage Example)

### 問題："Find the longest increasing subsequence"

#### Step 1: 識別 Intent

- 問題：找「最長」→ **Optimization Intent**

#### Step 2: 識別 Domain

- 輸入：序列 → **Array Domain**

#### Step 3: 識別 Constraint

- "increasing" → **Ordering Constraint**
- "subsequence" → **Structural Constraint**

#### Step 4: 查閱策略矩陣

- Optimization + Array → DP, Binary Search, Greedy
- Optimization + Ordering → DP (state design)

#### Step 5: 決策

**主要技術**：Dynamic Programming

- 狀態：`dp[i]` = 以 index i 結尾的最長長度
- **最佳化**：Binary Search + DP (O(n log n))

---

## 💡 關鍵洞察 (Key Insights)

### Intent 決定 DP 狀態設計

```
Boolean:  dp[i] = true/false  (可達性)
Counting: dp[i] = count       (方法數)
Optimization: dp[i] = min/max (最佳值)
```

### Complexity 驅動技術選擇

| n 範圍 | 允許複雜度  | 技術選擇                  |
| ------ | ----------- | ------------------------- |
| ≤20    | O(2^n)      | Backtracking, Bitmask     |
| ≤1000  | O(n²)       | 2D DP                     |
| ≤10⁵   | O(n log n)  | Sort, Heap, Binary Search |
| >10⁶   | O(n) 或更低 | Hash, Prefix Sum          |

### 輸入特性影響決策

```
已排序 → Binary Search, Two Pointers
未排序 → 先 Sort 或用 Heap
加權圖 → Dijkstra
無權圖 → BFS
DAG → Topological Sort, DAG DP
```

---

## 🔗 與其他資源整合 (Integration)

本框架與現有知識庫的連結：

- **演算法技術**：提供技術應用時機的脈絡
- **問題解決框架**：增加結構化的問題分析
- **領域專屬指南**：展示領域與技術的互動關係

### 延伸閱讀

- [Algorithm_Techniques_Checklist.md](../../Algorithm_Techniques_Checklist.md)
- [Problem_Solving_Process_and_Assumption_Checklist.md](../../Interview_Playbook/Problem_Solving_Process_and_Assumption_Checklist.md)
- [Problem_Transformation.md](../Problem_Transformation.md)

---

## 📌 使用建議 (Usage Tips)

### 建議學習路徑

1. **第一階段 - 建立基礎思維** (01)
   - 學習 [`01-演算法設計三連問.md`](01-演算法設計三連問.md)
   - 理解 State/Transition/Traversal 核心概念

2. **第二階段 - 快速實戰** (02-04)
   - 使用 [`02-快速決策地圖.md`](02-快速決策地圖.md) 練習 30 秒分類
   - 參考 [`03-問題分類法.md`](03-問題分類法.md) 深入理解分類維度
   - 查閱 [`04-解法策略矩陣.md`](04-解法策略矩陣.md) 選擇技術

3. **第三階段 - 面試準備** (05-06)
   - 學習 [`05-DSA設計模式路線圖.md`](05-DSA設計模式路線圖.md) 建立完整解題流程
   - 掌握 [`06-ChatGPT高階心法.md`](06-ChatGPT高階心法.md) 面試快速決策

### 日常使用

- **刷題時**：按照 01→02→04 的順序思考
- **複習時**：重讀 03 和 05 鞏固理解
- **面試前**：快速瀏覽 02 和 06

---

**版本 (Version):** 2.0  
**最後更新 (Last Updated):** 2025-01-28  
**維護者 (Maintainer):** LeetCode Note Repository
