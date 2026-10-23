# Subset Sum & 0/1 Knapsack：從增加變數到動態規劃

**先問選擇改變了什麼，再把缺少的數值資訊放進 recurrence；定義目標與範圍後，才談 memoization、table 與 bottom-up。**

這是一組可獨立閱讀的文件草稿，供檢視新的教學脈絡；現有 Subset Sum、Knapsack Playbook 與通用 DP 文件暫不整併。

## 閱讀主線

| 順序 | 文件 | 要回答的問題 |
|---|---|---|
| 1 | [Subset Sum：Adding a Variable、目標與值域](01-Subset_Sum_State_and_Range.md) | 為什麼只記項目進度不夠？數值變數、目標與 range 如何從問題推導？為什麼能共用答案？ |
| 2 | [從 Memoization 到 Table／Bottom-up](02-From_Memoization_to_Tabulation.md) | 相同 recurrence 如何安排成填表？何時保留 suffix，何時改用前 i 個項目？ |
| 3 | [從 Subset Sum 到 0/1 Knapsack 最佳化](03-From_Subset_Sum_to_01_Knapsack.md) | 恰好可達、容量內最大總重量、容量內最大價值，如何沿同一骨架延伸？ |
| 分析篇 | [偽多項式時間與 NP-completeness](04-Complexity_and_NP_Completeness.md) | O(nT) 為何不保證一般多項式時間？有 DP 為何仍是 NP-complete？ |

主線是：

```text
選／不選的遞迴
→ 只有項目進度不足以描述剩餘問題
→ adding a variable：記住剩餘目標／容量
→ 定義數值語義、原始目標與安全 range
→ 證明相同狀態有相同後續問題
→ memoization
→ 依狀態依賴建立 table 與 bottom-up
→ 保留選／不選，將可行性延伸成最佳值
```

各步可以來回修正，不是要求一次猜中所有設計；固定的是「先定義問題，再決定儲存與計算方式」。

## 與 Algorithm Design 的關係

Kleinberg、Tardos 的 *Algorithm Design* §6.4 **Subset Sums and Knapsacks: Adding a Variable**，書頁 266–271，先說明只用前 i 個項目不足，再增加容量變數，最後延伸到物品具有獨立價值的 Knapsack。

原書該節的 Subset Sum 採「容量內最大總重量」版本。本組為銜接判定與計數練習，先從「是否恰好湊出 target」出發，再在第三篇接回原書的最佳化脈絡。這是教學安排，不把兩個版本的定義混用。

來源：[專案中的原書](../../../Reading/Algorithm%20Design%20by%20Jon%20Kleinberg,%20Eva%20Tardos.pdf#page=292)、[依 §6.4 編寫的大學講義](https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/subsetsum.pdf)。

## 如何檢查自己是否理解

先不寫程式，依序說出：原始目標是什麼、選擇改變哪個數值、為什麼只記 i 不夠、數值範圍為何安全、哪些歷史可以忘記、每個狀態回傳什麼。

能說清楚後，再安排 cache、base case、填表順序與答案位置；最後才做空間壓縮。

練習路徑可用 **LC 416. Partition Equal Subset Sum** 驗證可行性，用 **LC 494. Target Sum** 練習轉換與計數，再用 **LC 474. Ones and Zeroes** 觀察兩個容量軸如何保留相同的選／不選骨架。
