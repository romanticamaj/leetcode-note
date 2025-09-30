# 遞迴設計四大流派：狀態設計心法

## 核心哲學

遞迴算法的本質是**狀態演化**。從狀態設計出發，可歸納為四大流派：

1. **Divide and Conquer**：多叉分裂，拆分與合併
2. **Decrease and Conquer**：單鏈遞減，縮小與擴展
3. **Dynamic Programming**：重疊子問題，記憶化避免重複
4. **Backtracking**：狀態樹枚舉，探索與剪枝

---

## 四大流派對比

| 特徵       | Divide & Conquer | Decrease & Conquer | Dynamic Programming | Backtracking     |
| ---------- | ---------------- | ------------------ | ------------------- | ---------------- |
| 狀態定義   | 問題規模 n       | 問題規模 n         | 子問題編號 + 參數   | 部分解 (partial) |
| 遞迴樹     | 多叉樹           | 單鏈               | DAG（有重疊）       | 狀態樹           |
| 子問題關係 | 獨立             | 線性依賴           | 重疊                | 互斥             |
| 核心操作   | 拆分與合併       | 縮小與擴展         | 狀態轉移 + 記憶化   | 選擇與回溯       |

---

## 典型遞迴式

**Divide and Conquer**: `T(n) = a*T(n/b) + f(n)`
**Decrease and Conquer**: `T(n) = T(n-1) + f(n)`
**Dynamic Programming**: `T(state) = min/max/sum { T(smaller_states) }`
**Backtracking**: `T(state) = Σ T(state + choice)`

---

## 流派選擇決策樹

```
問題分析
├─ 需要「所有解」或「枚舉路徑」？ → Backtracking
├─ 有「最優化/計數」且「重疊子問題」？ → Dynamic Programming
├─ 可「分裂成多個獨立子問題」？ → Divide and Conquer
└─ 只能「一步步縮小」且無重疊？ → Decrease and Conquer
```

---

## 解題策略

**Divide**: 排序、區間、分治結構 (Merge Sort、線段樹)
**Decrease**: 單步縮減、遞推 (Binary Search、GCD)
**DP**: 最優化、計數、重疊 (背包、LCS、Paint House)
**Backtracking**: 所有解、組合、排列 (N-Queens、全排列)

---

## 心法總結

問三個問題：

1. **子問題如何定義？**

   - 可分裂成多個獨立 → Divide
   - 只能縮小一步 → Decrease
   - 有重疊依賴 → DP
   - 是部分解，要探索多選項 → Backtracking

2. **遞迴樹長什麼樣？**

   - 多分支樹 → Divide
   - 單鏈 → Decrease
   - DAG（有重疊）→ DP
   - 狀態樹枚舉 → Backtracking

3. **解題策略怎麼選？**
   - Divide：快速結構（排序/分裂）
   - Decrease：迭代或遞迴 + 擴展
   - DP：Top-down + cache 或 Bottom-up + 表格
   - Backtracking：DFS + 剪枝
