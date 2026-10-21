# 背包型動態規劃（Knapsack DP）

**主教材：[0/1 Knapsack 變形題整理](../../../Checklists/Trick%20Practice/Knapsack_Variations_Playbook.md)。** 原有 Playbook 已整理背包模型、題目轉換、學習路徑與使用限制；本頁整理名稱與閱讀入口，詳細內容由各篇筆記承接。

## 名稱與範圍

- **Knapsack DP**：背包型問題與狀態設計的家族名稱。
- **0/1 Knapsack**：每個物品最多使用一次的版本。
- **Subset Sum**：判定是否存在總和恰好為 target 的子集，可視為 0/1 背包的特例。
- **Pseudo-polynomial／偽多項式**：描述標準數值 DP 依賴數值大小的成本，不是與背包互斥的另一個問題分類。

## 依目前需要閱讀

| 想釐清的問題 | 文件 |
|---|---|
| 背包模型、變形與練習路徑 | [既有 Knapsack Playbook](../../../Checklists/Trick%20Practice/Knapsack_Variations_Playbook.md) |
| 如何從 input 與選擇效果推導數值軸、range，再映射成 index？ | [數值範圍設計的起手式](../Subset_Sum/01-Subset_Sum_and_NP_Completeness.md#4-數值範圍讓狀態數可以估計) |
| 為何候選進度與數值目標能形成狀態表？O(nT) 為何是偽多項式？ | [Subset Sum：候選進度 × 數值範圍](../Subset_Sum/01-Subset_Sum_and_NP_Completeness.md) |
| 數值 T 與輸入位元長度有何不同？有 DP 為何仍是 NP-complete？ | [偽多項式時間與 NP-completeness](../Subset_Sum/03-Pseudopolynomial_Time.md) |
| 理解狀態後，如何改成 bottom-up 與一維陣列？ | [Subset Sum 實作指南](../Subset_Sum/02-Implementation_Guide.md) |

## 先打底，再做題目轉換

先練原始問題：**直接給定正整數陣列與 target，每個位置最多使用一次，判定是否存在子集和恰好為 target。**

理解這個 Subset Sum 判定模型後，再回到 **416. Partition Equal Subset Sum** 的等和分割轉換；**494. Target Sum** 則多了符號分配的轉換與計數語義。

個人練習目標見 [Problem Review](../../../Checklists/Lists/09_Problem_Review.md)；完成紀錄以 [Practice Log](../../../Checklists/Practice_Log.md) 為準。
