# 🌲 Path-Based Thinking & Aggregation in Tree Problems

在處理二元樹（binary tree）或一般樹結構的題目時，若題目要求分析祖先與子孫的關係、做跨層比較、或保留 path 上的狀態資訊，  
可以運用「**Path-Based Thinking**」結合「**Aggregation（狀態聚合）**」的解法框架。

這個策略的核心是：

- 所有祖先與子孫的關係必然落在一條從 root 出發的 path 上
- 在 DFS 遍歷過程中，沿著這條 path 傳遞並更新狀態資訊
- 在葉節點或遞迴 return 時完成聚合運算（例如計算最大差值、累積條件次數等）

這種策略可廣泛應用於：最大值查找、祖先關係判斷、條件統計、祖先查找、遞推資料流處理等問題。

---

## ✅ 通用觀察

> 在一棵樹中，所有合法的祖先-子孫節點對 `(a, b)`，都必定存在於某一條從 root 到 b 的 path 上。  
> 這是因為樹的定義保證了從 root 到任意節點的路徑唯一性。  
>
> **因此，凡是針對祖先與子孫的邏輯判斷或資訊聚合問題，皆可轉化為沿著 root-to-node path 的狀態傳遞與計算問題。**  
>
> - 在 DFS 遍歷的過程中，對每一條 root-to-node path 傳遞必要的狀態（例如最大值、累計資訊、節點記錄等）  
> - 在遞迴或回溯過程中進行資訊的聚合、比較或判斷  
> - 💡 **最終的答案更新/運算常在 leaf node（或到達某條 path 的末端）進行，因為此時整條祖先鏈條完整，狀態資訊才具備意義**

---

## ✅ 通用策略：祖先-子孫問題 ➝ Path-Based DFS + Aggregation

| 類型           | 範例需求                             | 解法策略（狀態聚合）                     |
|----------------|--------------------------------------|-------------------------------------------|
| 差值最大/最小   | 找祖先與子孫之間最大差值              | 傳遞 path 上的 `max` / `min`             |
| 限制範圍        | 確保所有祖先值小於當前節點            | 傳遞 ancestor 最大值並進行檢查           |
| 統計條件次數    | 計算祖先節點中滿足條件者的數量        | 傳遞 counter 或累加器                    |
| 映射條件節點    | 找到第一個符合條件的祖先節點          | 用 stack 或 path 記錄模擬 ancestor list |
| 最近有效祖先    | 找距離最近且符合條件的 ancestor       | 模擬 DFS 並回傳相關資訊                  |

---

## ✅ 通用語句模板（Path-Based Reduction）

> 若題目中涉及祖先與子孫的關係（不限定於直接 parent-child），可將問題轉化為**針對 root-to-node path 的狀態遞傳與資訊聚合問題**。  
> 由於任一祖先-子孫對，皆只能出現在一條 root-to-node path 上，因此可透過 DFS 設計狀態參數，進行有效的遞傳與聚合，完成整體問題求解。  
> ✅ **最終答案的更新位置通常在葉節點（leaf node），因為此時聚合資訊涵蓋了完整祖先路徑。**

---

## ✅ 實用案例參考（以此策略切入）

- [Leetcode 1026 – Maximum Difference Between Node and Ancestor](https://leetcode.com/problems/maximum-difference-between-node-and-ancestor/)
- [Leetcode 1123 – Lowest Common Ancestor of Deepest Leaves]（使用 DFS 傳回多種 path 狀態）
- [Leetcode 124 – Binary Tree Maximum Path Sum]（雖是任意 path，但可改為 postorder 聚合）
- [Leetcode 235 – Lowest Common Ancestor of a BST]（利用 path 分析找最近祖先）

---

## ✅ 延伸關鍵詞

- DFS + state propagation
- Path-based aggregation
- Ancestor-descendant reduction
- Tree path dynamic programming
- Stack-based path simulation