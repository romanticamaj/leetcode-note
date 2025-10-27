# Problem Transformation Framework

## 簡介：問題解決的 Meta-Framework

**Problem Transformation** 是一個高階的 meta-framework，教你如何系統性地將基於敘述的或真實世界的算法問題轉換為正式的、可解決的計算模型。

與特定算法技術（如 binary search 或 dynamic programming）不同，Problem Transformation 是一種 **meta-cognitive 方法**，幫助你：

- **識別** 隱藏在問題敘述中的底層結構
- **翻譯** 真實世界場景為數學模型
- **選擇** 適當的資料結構和算法
- **泛化** 模式以便在類似問題中重複使用

這個框架連結了「這個問題到底在問什麼？」和「我確切知道如何建模和解決這個問題」之間的鴻溝。

---

## 五步驟轉換流程

### 步驟 1：提取抽象模型

**目標：** 剝離故事並識別底層的資料結構或算法模型。

**核心原則：** 每個問題敘述都包含實體、關係和約束，它們映射到眾所周知的計算結構。

#### 自問問題：

- **實體是什麼？** (例如：城市 → nodes, 人 → vertices, 任務 → elements)
- **關係是什麼？** (例如：道路 → edges, 友誼 → connections, 依賴關係 → directed edges)
- **結構是什麼？** (例如：tree, graph, array, matrix, sequence)
- **目標是什麼？** (例如：reachability, counting, optimization, validation)

#### 實體識別

識別問題空間中的主要物件：

- 這些實體具有哪些屬性？
- 這些實體如何被量化或約束？
- 是否有隱含的實體（如時間、狀態或配置）？

#### 關係映射

分析實體如何互動：

- 關係是否具有方向性、權重或條件？
- 關係是否形成可識別的結構（trees, graphs, lattices）？
- 是否有 transitive 或衍生的關係？

---

### 步驟 2：用 Graph/數學術語重新框架

**目標：** 使用精確的數學語言將故事轉換為正式的問題陳述。

**核心原則：** 將定性描述轉譯為定量的、正式的規格，使算法推理成為可能。

#### 自問問題：

- **我能將其建模為 graph、array 或 tree 嗎？**
- **約束是什麼？** (例如：acyclic, connected, unique values, size limits)
- **cost function 或優化目標是什麼？**
- **必須保持哪些 invariants？**

#### 結構形式化

- 識別適當的資料結構（graph, tree, array 等）
- 確定結構屬性（connected, directed, weighted 等）
- 識別特殊情況（DAG, bipartite, planar 等）

#### Constraint 編碼

- 將限制表達為數學約束
- 識別必須維持的 invariants
- 從問題上下文識別隱含約束

#### Objective Function 定義

- 將目標制定為清晰的數學 objective
- 確定是 minimization 還是 maximization 問題
- 識別可操作的變量

---

### 步驟 3：選擇正確的表示法

**目標：** 選擇最適當的資料結構來有效地建模問題。

**核心原則：** 表示法的選擇決定了解決方案的清晰度和執行時間複雜度。

#### 自問問題：

- **我需要保持方向嗎？** → 使用 directed graph
- **我需要自由遍歷嗎？** → 使用 undirected graph（或 bidirectional adjacency list）
- **我需要快速查找嗎？** → 使用 hash sets/maps
- **我需要追蹤原始狀態嗎？** → 分別儲存 metadata
- **我需要修改結構嗎？** → 考慮是否複製或標記

#### 表示法策略

**對於 Graphs：**

- **Adjacency List：** 對 sparse graphs 有效，支援 directed/undirected
- **Edge List：** 簡單，適用於 union-find 或當順序重要時
- **Adjacency Matrix：** 快速查找，適合 dense graphs

**對於 Trees：**

- **Parent Pointers：** 適用於 ancestor queries
- **Children Lists：** 適用於 top-down traversal
- **Implicit Representation：** 基於 array 的 complete binary trees

**Metadata 儲存：**

- 將 edge attributes（weights, directions, original state）與結構分離
- 使用 pairs, tuples 或 custom structs 來捆綁資料
- 考慮使用 parallel arrays 或 hash maps 以獲得靈活的 metadata

---

### 步驟 4：設計算法

**目標：** 使用 traversal、simulation 或 search 來解決形式化的問題。

**核心原則：** 有了正確的模型和表示法，算法通常變得直截了當。

#### 自問問題：

- **我能使用 DFS/BFS 來探索嗎？** (graph traversal)
- **我能模擬過程嗎？** (state machines, dynamic programming)
- **我能在 traversal 期間計數或累積嗎？** (online algorithms)
- **base case 和 recursive case 是什麼？** (用於 recursive 解決方案)

#### Traversal 策略選擇

- 選擇適當的 traversal 方法（DFS, BFS, topological sort）
- 確定 traversal 方向和起點
- 決定如何處理 disconnected components 或 cycles

#### State 追蹤設計

- 識別在 traversal 期間需要追蹤的資訊
- 設計資料結構以有效維持此 state
- 確定如何在算法執行期間更新 state

#### Edge Case 處理

- 識別 boundary conditions 和特殊情況
- 確保算法對 minimal 和 maximal inputs 的正確性
- 驗證算法對 degenerate cases 的行為

---

### 步驟 5：泛化模式

**目標：** 提取可重複使用的見解和適用於類似問題的模式。

**核心原則：** 轉換過程本身通常揭示適用於整個問題家族的技術。

#### 自問問題：

- **關鍵見解是什麼？** (「啊哈！」時刻)
- **哪些其他問題有類似的結構？**
- **我能重複使用這個模型嗎？** (類似問題的模板)
- **可能出現哪些變化？** (weighted, constrained, multi-objective)

#### 模式提取

識別可重複使用的組件：

- **結構模式：** 問題如何映射到標準資料結構
- **算法模式：** 解決此結構的一般方法
- **表示技巧：** 簡化解決方案的巧妙編碼

#### 相關問題

找到具有類似轉換模式的問題：

- 相同的核心結構（例如：所有具有方向要求的 tree 問題）
- 相同的算法方法（例如：所有可通過 DFS + counting 解決的問題）
- 類似的表示技巧（例如：undirected graph + metadata）

---

## Meta-Cognitive 策略

超越機械性的五步驟過程，培養這些高階思維技能，成為問題轉換大師。

### 模式識別

訓練自己立即識別常見的問題家族：

#### Graph Traversal 模式

- **Reachability：** 我能從 Y 到達 X 嗎？ → DFS/BFS
- **Connectivity：** 所有 nodes 都連接嗎？ → Union-Find 或 DFS
- **Shortest Path：** 最小距離是多少？ → BFS (unweighted) 或 Dijkstra (weighted)
- **Cycle Detection：** 有 cycle 嗎？ → DFS with coloring 或 Union-Find

#### Tree 模式

- **Hierarchical Relationships：** Parent-child, ancestor-descendant → tree traversal
- **Path Queries：** 從 node A 到 B 的路徑 → LCA 或 tree DP
- **Subtree Aggregation：** 計算 subtrees 的值 → post-order DFS

#### Dynamic Programming 模式

- **Optimal Substructure：** 解決方案由 optimal subsolutions 構建 → DP
- **Overlapping Subproblems：** 相同的 subproblems 重複解決 → memoization
- **State Transitions：** 當前 state 依賴於先前 states → recurrence relation

#### Greedy 模式

- **Exchange Argument：** 交換維持最優性 → greedy sorting
- **Staying Ahead：** 局部最優就是全局最優 → greedy selection
- **Interval Scheduling：** 選擇 non-overlapping intervals → sort + greedy

### 轉換啟發法

當你卡住時，應用這些策略性轉換：

#### 1. Inversion

考慮問題的補集或相反：

- 與其「最大化可達 nodes」，不如想「最小化不可達 nodes」
- 與其「找到有效分配」，不如想「消除無效分配」
- 與其「計數解決方案」，不如想「計數非解決方案並減去」

#### 2. Relaxation

暫時忽略約束以找到更簡單的解決方案：

- 移除約束以獲得更簡單的問題
- 解決 relaxed 版本
- 逐步添加回約束
- 使用 relaxed solution 作為起點或界限

#### 3. Restriction

先解決特殊情況，然後泛化：

- 如果只有 2 個 nodes 呢？3 個 nodes 呢？
- 如果 graph 是一條線？一個星形？一個 complete graph？
- 如果所有 weights 都是 1？所有值都唯一？

#### 4. Reduction

轉換為已知問題並使用現有解決方案：

- 我能將其簡化為 shortest path？Maximum flow？Matching？
- 我能用稍作修改的標準算法重複使用嗎？
- 我能組合多個標準算法嗎？

### 驗證技術

系統性地驗證你的轉換和解決方案：

#### 1. Invariant 檢查

識別在執行過程中必須保持為真的屬性：

- Loop invariants：每次迭代之前/之後什麼為真？
- Structural invariants：資料結構維持哪些屬性？
- Problem invariants：哪些約束必須始終成立？

#### 2. Boundary 測試

在極端和 edge cases 驗證行為：

- **Minimal Input：** n = 0, 1, 2
- **Maximal Input：** n = constraint limit
- **Degenerate Cases：** 所有相同值、所有不同、最壞情況結構
- **Special Structures：** Line graph, star graph, complete graph, disconnected graph

#### 3. Contradiction 分析

通過證明替代方案失敗來證明正確性：

- 假設你的解決方案是錯誤的
- 從這個假設推導出矛盾
- 這證明你的解決方案必須是正確的

---

## 總結：完整框架

| 步驟            | 目的                 | 關鍵行動                                      | 輸出           |
| --------------- | -------------------- | --------------------------------------------- | -------------- |
| **1. 提取模型** | 識別核心結構         | 找到實體、關係、結構類型                      | 抽象模型       |
| **2. 重新框架** | 形式化問題           | 轉換為數學、識別約束和目標                    | 正式規格       |
| **3. 表示**     | 選擇資料結構         | 選擇 graph/tree 表示法、metadata 策略         | 實作結構       |
| **4. 解決**     | 設計算法             | 選擇 traversal/search、追蹤 state、處理 edges | 工作解決方案   |
| **5. 泛化**     | 學習可重複使用的模式 | 提取見解、找到類似問題、創建模板              | 問題解決工具包 |

### 快速參考：常見轉換

| 問題敘述               | 抽象模型               | 典型算法                           |
| ---------------------- | ---------------------- | ---------------------------------- |
| 「城市和道路」         | Graph nodes 和 edges   | Graph traversal (DFS/BFS)          |
| 「具有依賴關係的任務」 | DAG                    | Topological sort                   |
| 「層次結構」           | Tree                   | Tree traversal (pre/in/post-order) |
| 「優化選擇」           | Greedy 或 DP           | Sorting + greedy 或 DP recurrence  |
| 「找到最短/最長路徑」  | Weighted graph         | Dijkstra/Bellman-Ford 或 DP        |
| 「分區元素」           | Array/set partitioning | Two pointers, sliding window 或 DP |
| 「計數配置」           | Combinatorial DP       | State-space DP                     |

---

## 結論

Problem Transformation 既是一種分析技能，也是一種創造性藝術。通過系統性地解構問題、用數學重新表述、選擇適當的表示法、實作解決方案和泛化模式，你可以清晰而精確地處理複雜問題。

**記住：** 轉換過程本身通常揭示了優雅解決方案所需的關鍵見解。掌握這個 meta-framework，你會發現大多數算法問題變成模式識別的練習，而不是需要神聖靈感的謎題。

---

_這是一個 meta-framework 文件。對於特定算法實作，請參見 `/Algorithms/` 和 `/Data_Structures/` 中的相應算法 playbooks。_
