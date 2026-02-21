# 問題轉換心法：目的地反轉為起點 (Destination-as-Source Reachability)

## 🧠 核心哲學

當問題要求「從每個點出發，判斷能否到達某個目的地」時，**反轉方向，從目的地出發反向搜尋**。

這個轉換的本質：**將 N 次「正向可達性查詢」轉化為 1 次（或少數幾次）「反向可達性標記」**。

> **口訣：與其逐個問「我能到那裡嗎？」，不如從終點問「誰能到我這裡？」**

---

## 為什麼有效？

### 正向思維的問題

從每個 cell 出發做 DFS/BFS 判斷是否能到達目的地：

- 每個起點各做一次完整搜尋
- 時間複雜度：O(V × (V + E))
- 大量重複計算：許多路徑會重疊

### 反向思維的優勢

從目的地出發，反向搜尋所有能到達它的 cell：

- 只做 k 次搜尋（k = 目的地群組數，通常為常數）
- 時間複雜度：O(k × (V + E))，k 通常為常數故等效 O(V + E)
- 自然消除重複：每次搜尋中，每個 cell 最多訪問一次

**關鍵洞察**：正向是「多對一」查詢（多個起點 → 一個目的地），反向是「一對多」標記（一個起點 → 標記所有可達者），後者天然更高效。

---

## 🧩 轉換框架

### 識別信號

當你看到以下模式時，考慮反轉方向：

1. **多對一/多對少可達性**：很多起點，但目的地是固定的邊界/集合
2. **邊界條件明確**：目的地是矩陣邊界、特定 node 集合、或某個固定狀態
3. **邊的方向可以反轉**：正向是 `A → B if height[A] >= height[B]`，反向就是 `B → A if height[A] >= height[B]`（即從 B 出發，走向更高或等高的鄰居）

### 轉換步驟

```
正向問題：對每個 cell，判斷是否能到達目的地 D
        ↓ 反轉
反向問題：從 D 出發，標記所有能到達 D 的 cell
```

具體操作：

1. **確定起點集合**：將目的地（邊界、目標 node）作為新的起點
2. **反轉邊的條件**：如果正向條件是 `can_flow(A → B)`，反向條件變成 `can_flow(B → A)`
3. **執行一次搜尋**：從所有新起點同時 BFS/DFS，標記所有可達的 cell
4. **收集結果**：被標記的 cell 就是正向能到達目的地的 cell

---

## 相關題目

- LeetCode 417. Pacific Atlantic Water Flow
- LeetCode 130. Surrounded Regions
- LeetCode 1020. Number of Enclaves
- LeetCode 286. Walls and Gates
- LeetCode 542. 01 Matrix

---

## ⚠️ 常見陷阱

1. **忘記反轉邊的條件**：方向反了，但不等式的語義要重新理解。正向的 `A → B` 條件在反向時變成從 B 的視角看 A
2. **多個目的地群組要分開標記**：如果有多組不同的目的地，需要各自獨立的 visited 陣列，最後取交集或聯集
3. **邊界起點要全部加入**：不是只從一個點開始，而是整組目的地都是起點（multi-source BFS/DFS）

---

## ✅ 快速判斷清單

- [ ] 問題是「多對一」或「多對少」的可達性查詢嗎？
- [ ] 目的地是固定且明確的嗎？（邊界、特定集合）
- [ ] 邊的方向可以合理反轉嗎？
- [ ] 反轉後，能否用一次 BFS/DFS 取代多次搜尋？

如果以上都是 ✅，就應該使用 **Destination-as-Source** 轉換。

---

## 🧠 與其他心法的關聯

- **[Problem Transformation - Inversion](../../../Meta_Frameworks/Problem_Transformation.md)**：本心法是 Inversion 策略在 graph reachability 問題上的具體實例化
- **[Transforming Constraints into Tools](./Transforming_Constraints_into_Tools.md)**：同屬「重塑問題視角」的思想家族，但本心法專注於搜尋方向的反轉
- **Multi-source BFS**：反向搜尋的起點通常是一組邊界 cell，天然適合 multi-source BFS/DFS
