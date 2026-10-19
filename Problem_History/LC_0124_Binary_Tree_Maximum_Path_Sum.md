# 124. Binary Tree Maximum Path Sum：樹直徑與最大子陣列的交會

**記憶線索：向父節點交出一支可延伸的路徑，在當前節點可合併兩支作為完整答案。**

查證日期：2026-10-19。

## 題目情境與查證結論

LC 124 要在二元樹中找節點總和最大的非空簡單路徑。端點可以是任意節點，不必經過 root；節點值允許負數。[LeetCode 原題](https://leetcode.com/problems/binary-tree-maximum-path-sum/)

目前確認的經典教材背景是 **樹的直徑（Tree Diameter）**與 **最大子陣列（Maximum Subarray）**。本次未找到經典教材收錄 LC 124 完全相同版本的明確證據，也未確認最初發明者、LeetCode 的直接取題來源或首次上架日期。

## 可確認的歷史

### 1977 年的最大子陣列故事，由 Bentley 在 1984 年記載

Jon Bentley 的〈Programming Pearls: Algorithm Design Techniques〉刊於 *Communications of the ACM*，27(9)，865–871，1984 年 9 月。第 868–869 頁記載：Ulf Grenander 從影像辨識中的二維問題出發，簡化為一維；1977 年向 Michael Shamos 提出問題，Shamos 設計出分治演算法，稍後 Jay Kadane 在研討會上提出線性演算法。[Bentley 原文](https://www.cs.rpi.edu/~moorthy/Courses/CSCI2300/p865-bentley.pdf#page=4)

**這是 Maximum Subarray 的歷史，不是 LC 124 的發明史。** 它提供「保留可延伸狀態、另記完整答案」的相關背景，不能據此聲稱 Kadane 發明了二元樹最大路徑和。

### 至少 2012 年已有 LeetCode 同題的公開紀錄

chkkch 的解題文章標示日期為 **2012-12-02**，題名為 *[LeetCode] Binary Tree Maximum Path Sum*，題面明確允許任意起終點，並使用節點 1、2、3，答案為 6 的例子。[當年的文章](https://www.cnblogs.com/chkkch/archive/2012/12/02/2798140.html)

這是目前找到的早期同題線索；文章所示日期不是 LeetCode 官方上架證明，也不證明它是最早的公開紀錄。

## 經典教科書是否收錄？

| 教材 | 可核對的位置 | 與 LC 124 的關係 |
|---|---|---|
| Cormen、Leiserson、Rivest、Stein，*Introduction to Algorithms*，第三版，2009 | §22.2，習題 **22.2-8**，書頁 **602** | 求樹的直徑；不是帶正負節點值的最大路徑和。另有 §4.1 最大子陣列，書頁 68–75。 |
| Antti Laaksonen，*Competitive Programmer’s Handbook*，2018-07-03 draft | §14.2 **Diameter**，書頁 **135–136** | 直接說明單支延伸與雙支合併的 Tree DP，是最貼近本題狀態設計的教材對照。 |
| *Elements of Programming Interviews* | 作者官方題目索引中的 **Compute the diameter of a tree** | 確認有相關原型；此處未主張收錄完全相同的 LC 124 版本，也未統一不同版本的題號。 |
| Jon Bentley，*Programming Pearls*，第二版，1999 | Column 8，**Algorithm Design Techniques** | 討論一維最大連續區段總和，提供陣列版本的背景。 |

來源：[CLRS 第三版原書，第 602 頁](https://www.cs.mun.ca/~harold/Courses/Old/CS3600.W23/Files/text.pdf#page=623)、[CPH 作者提供的全文，第 135–136 頁](https://cses.fi/book/book.pdf#page=145)、[EPI 作者官方索引](https://elementsofprogramminginterviews.com/solutions-alpha/)、[Programming Pearls 第二版章節](https://www.oreilly.com/library/view/programming-pearls-2nd/9780134498058/ch08.html)。頁碼與題號僅適用於表中指定版本。

## 🧠 數學觀點：每條路徑都有唯一最高節點

以下是結構上的推導，不是已證實的歷史傳承。

將樹定根後，每條簡單路徑都有唯一最高節點。在此處，路徑最多伸入兩個不同的 child 子樹；若還要向父節點延伸，就只能保留其中一支，否則會產生三叉。

因此要區分兩種狀態：

- **可延伸路徑**：以當前節點為端點，往下最多接一個 child，供父節點使用。
- **完整候選**：以當前節點為最高點，可以合併左右兩支，更新整棵樹的答案。

CPH 的直徑演算法分別用 `toLeaf(x)` 與 `maxLength(x)` 描述單支長度與以 x 為最高點的完整路徑長度。LC 124 將長度換成節點權重總和，還要處理負貢獻。

若左右子樹交出的可延伸總和為 L、R：

```text
向上回傳 = value + max(0, L, R)
當前完整候選 = value + max(0, L) + max(0, R)
```

負的分支可以不接，但完整答案必須包含至少一個節點。全負數時仍須選一個節點，不能把全域答案初始化成 0。先取得子樹結果再合併，是 postorder、由下而上的 Tree DP；每個節點處理一次，時間 O(n)、遞迴空間 O(h)。

陣列若視為一條鏈，其連續子陣列就是樹上的簡單路徑，因此最大子陣列是這類問題在鏈狀結構上的特例。這解釋兩者的狀態設計為何相似，並不證明 LeetCode 的出題者沿此路徑發展題目。

## ⚠️ 相關但不同的概念

- **一般樹直徑**：最大化邊數或非負邊長；LC 124 最大化可含負值的節點總和。不能把直徑的所有性質原封不動搬過來，例如答案未必以原樹的葉節點為端點。
- **兩次最遠點搜尋**：是常見直徑方法；這裡的教科書對照以 Tree DP 為主，不把兩次搜尋直接當成帶負節點權重版本的證明。
- **Root-to-leaf path sum**：限制起終點，本題則允許在任意節點開始或結束。
- **Global tracking 是實作選擇**：也可以向上回傳「單邊最佳值、子樹完整最佳值」的 pair；必要的是區分兩種語義，不是必須使用全域變數。
- **來源界線**：教材收錄相關原型、數學上可推廣、LeetCode 直接取題，是三件不同的事；目前未確認直接傳承。

## 延伸閱讀

先讀 CPH §14.2 的兩種狀態，再對照 CLRS 22.2-8 的直徑問題與 §4.1 的最大子陣列；歷史故事則讀 Bentley 1984 原文。既有概念筆記可參考 [Path-Based Thinking 與 Aggregation](../Data_Structures/Trees/Path_Based_Thinking_Aggregation.md)，本題的分類見 [Archetype Problems：Tree DP](../Checklists/Lists/06_Archetype_Problems.md#tree-dp)。
