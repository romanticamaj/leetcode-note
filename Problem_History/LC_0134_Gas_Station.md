# 134. Gas Station：汽油謎題與前綴和的最低谷

題目：[LeetCode 134. Gas Station](https://leetcode.com/problems/gas-station/)

**記憶線索：從全程最低的谷底出發。**

查證日期：2026-10-01。

## 可確認的歷史

László Lovász 的《Combinatorial Problems and Exercises》（1979）第 3.21 題收錄了 **Gasoline Puzzle（汽油謎題）**：環形賽道上有若干加油站，總汽油恰好足夠繞一圈，證明存在一站，讓車子從空油箱出發也能完成全程。

這是 LC 134 的同型數學問題：原謎題問「證明存在」，LeetCode 問「找出起點」，並允許總油量不足或有剩餘。Guido Schäfer 的論文明確指出謎題取自 Lovász 書中的第 3.21 題，並列出 1979 年的書目。[來源：作者論文，文獻說明與參考文獻](https://ir.cwi.nl/pub/25468/25468.pdf)

**目前可確認的是這本書收錄了題目；尚未確認誰最早提出謎題，也未確認 LeetCode 直接取材自哪份文獻。**

## 🧠 背後的數學觀點

令每站的淨變化為：

```text
d[i] = gas[i] - cost[i]
P[0] = 0
P[t] = d[0] + ... + d[t - 1]
```

把前綴和 `P` 看成一條高低起伏的路線。選取 `P[0]` 到 `P[n-1]` 中的最低點 `P[k]`，便相當於從第 `k` 站出發。

- **還沒繞回開頭時**：油量為 `P[t] - P[k]`。因為起點位於最低點，這個差值不會是負數（終點另由 `P[n] >= 0` 與 `P[k] <= 0` 保證）。
- **繞回開頭後**：油量為 `P[n] + P[t] - P[k]`。最低點保證後兩項的差非負；全程總和 `P[n] >= 0`，便能保證這段也不缺油。

因此，全程總和非負時，一定存在合法起點。學術文獻中的 **Gasoline Lemma（汽油引理）** 通常以總和恰好為 0 的循環序列表述，並以最低前綴和證明。[來源：研究論文，第 2.3 節](https://iris.uniroma3.it/bitstream/11590/381271/6/budget-mp.pdf)

## 🧩 和 greedy reset 的關係

若目前候選起點是 `k`，掃到第 `j` 站後局部累積變負，就有：

```text
P[j + 1] - P[k] < 0
```

也就是 `P[j + 1]` 比目前候選谷底更低。將候選起點更新成 `j + 1`，等於更新谷底；局部累積歸零，等於重新以這個谷底作為高度基準。

這個推導說明了：**greedy 的 reset 和最低前綴和，是同一件事的兩種理解方式。** 這是數學上的對應，並非已查證的演算法發明史。

另一個等價理由是候選排除：如果 `k` 到 `j` 首次累積失敗，從任何中間站出發，都會失去前面那筆非負的累積油量，因此也無法通過失敗點。

## ⚠️ 相關但不同的概念

### Cycle Lemma（循環引理）

Dvoretzky 與 Motzkin 在 1947 年的〈A problem of arrangements〉提出 Cycle Lemma。相關研究探討循環旋轉、部分和與計數；這和汽油謎題的「選擇旋轉起點，讓部分和保持非負」有數學關聯。[來源：SIAM 研究論文的歷史說明與參考文獻](https://epubs.siam.org/doi/pdf/10.1137/100796431?download=true)

這項關聯不代表原始 Cycle Lemma 就是 LC 134 的完整命題，也不足以證明汽油謎題直接源自該論文。

### Kadane's algorithm

兩者都有「累積不利時重設」的形式。Gas Station 的目標是找到能繞完一圈的起點；Kadane 的目標是最大子陣列和。Gas Station 的 reset 由候選排除／最低前綴和支持。

閱讀時可以用 Kadane 幫助記憶操作形狀，但目前沒有來源支持將它寫成 Gas Station 的歷史起源。

## 來源與延伸閱讀

| 來源 | 支持的內容 |
|---|---|
| [Guido Schäfer, *Budgeted Matching via the Gasoline Puzzle*](https://ir.cwi.nl/pub/25468/25468.pdf) | 汽油謎題的敘述；明確引用 Lovász（1979），Problem 3.21；Gasoline Lemma 在組合最佳化中的應用 |
| [Berger、Bonifaci、Grandoni、Schäfer, *Budgeted matching and budgeted matroid intersection via the gasoline puzzle*，2011 年期刊版](https://iris.uniroma3.it/bitstream/11590/381271/6/budget-mp.pdf) | 第 2.3 節的 Gasoline Lemma，以及最低前綴和證明 |
| [*Counting Lattice Paths via a New Cycle Lemma*](https://epubs.siam.org/doi/pdf/10.1137/100796431?download=true) | Cycle Lemma 的研究脈絡，及 Dvoretzky／Motzkin 1947 年論文的書目 |

相關技巧筆記：[Prefix Sum](../Algorithms/Prefix_Sum/01_Prefix_Sum_Intro.md)、[Greedy 的辨識與應用](../Algorithms/Greedy/Greedy_Identification_and_Application.md)、[Kadane Algorithm](../Algorithms/Dynamic_Programming/Advanced_Techniques/Kadane_Algorithm.md)。
