# 545. Boundary of Binary Tree：EPI 的 Exterior 與 DFS 輸出時機

**記憶線索：邊界身分向下傳，左邊界進入時輸出，右邊界返回時輸出，葉節點只輸出一次。**

查證日期：2026-11-06。依作者官網、官方解答原始碼、教材投影片、原論文與公開討論整理。

## 1. 已確認的教材出處

Adnan Aziz、Tsung-Hsien Lee、Amit Prakash 的 **Elements of Programming Interviews（EPI）** 收錄 **Compute the exterior of a binary tree**；[作者官網題目索引](https://elementsofprogramminginterviews.com/solutions-alpha/) 列有此題及 C++／Java 解答。

本次實際讀取的 [官方 EPI Judge Python 解答](https://github.com/adnanaziz/EPIJudge/blob/master/epi_judge_python_solutions/tree_exterior.py) 採用：

```text
root
→ left_boundary(tree.left)
→ leaves(tree.left)、leaves(tree.right)
→ right_boundary(tree.right)
```

左邊界優先左、缺左走右，在遞迴前加入；右邊界優先右、缺右走左，在返回時加入；兩者都排除葉節點。這與本次先完成的分段遞迴具有相同結構。官方解答回傳節點，本次 LC 實作回傳節點值。

**可確認教材收錄同型題，不能確認 LeetCode 直接改編自 EPI，也不能據此認定作者是問題發明者。**

作者在 [2016 年的版本說明](https://elementsofprogramminginterviews.com/2016/06/22/2016-06-22-variants/) 特別指出，書籍自 2012 年首版後持續增刪題目。因此不能把全書的首版年份直接當成本題首次收錄年份；本次未確認最早收錄版本，章節編號也應依手上版本核對。

## 2. 早期公開題目與面試使用紀錄

| 日期 | 來源 | 可確認的內容與限制 |
|---|---|---|
| 2012-06-28 | [Stack Overflow：print boundary of binary tree](https://stackoverflow.com/questions/11244526/print-boundary-of-binary-tree) | 已有樹外框輸出、分段遍歷與 one-pass 的討論；題面範例定義與 LC 545 有差異，僅作早期近似題的證據 |
| 2015-05-16 | [Stack Overflow：To print the boundary of Binary Tree](https://stackoverflow.com/questions/30275735/to-print-the-boundary-of-binary-tree) | 提問者回報面試考過，並描述 boolean flag 與分段方案；未透露公司，無法追溯業界最初出題者 |

這些頁面的程式有個別規格差異與討論中的錯誤，**作為歷史使用紀錄，不作為已驗證的解法模板**。其中面試官要求少走幾趟，是個別面試回報，不代表分段 O(n) 解法不合格。

目前未找到可信來源，能把本題連到某個產品功能、公司發明紀錄、最初出題者，或確認 LC 545 的首次發布日期。

## 3. One-pass 的教材背景：Euler Tour Traversal

Goodrich、Tamassia 的 [2004 年 Trees 教材投影片](https://cs.brown.edu/cgc/java3.datastructures.net/handouts/Trees.pdf)（投影片 15–16，PDF 第 4 頁）以 **Euler Tour Traversal** 統一 preorder、inorder、postorder：

| 遞迴事件 | 對應順序 | 本題 one-pass 可做的事 |
|---|---|---|
| 進入節點，尚未走訪子樹 | Preorder | 輸出左邊界 |
| 完成左子樹，尚未走訪右子樹 | Inorder | 本題不需此事件輸出 |
| 完成兩個子樹，準備返回 | Postorder | 輸出右邊界 |

**以下是設計上的對照，不是已證實的直接傳承。** 本題再加上由父節點傳入的 `isLeftBoundary`／`isRightBoundary`，便能讓同一次 DFS 對不同身分採用不同輸出時機；葉節點統一處理並返回，避免重複。

這裡的 Euler tour 是一般遍歷事件框架；LC 545 要求的是特定邊界節點序列，不能把完整 Euler tour 的所有事件直接當作答案。

## 4. 相關學術文獻與歸屬界線

Robert E. Tarjan、Uzi Vishkin，**An Efficient Parallel Biconnectivity Algorithm**，*SIAM Journal on Computing* 14(4), 862–874，1985。

- [出版社論文頁／DOI](https://epubs.siam.org/doi/10.1137/0214061)
- [作者學術網站提供的論文 PDF](https://users.umiacs.umd.edu/~vishkin/TEACHING/ENEE759KS12/TV85.pdf)

該文處理圖的雙連通分量，並提出一般性的平行樹計算技術，是 Euler-tour 樹計算相關的研究背景。**它不是本題的命題論文，也沒有證據表明 LC 545 直接出自該文。** 本次不將它稱為 preorder／postorder 或 Boundary Traversal 的最初發明文獻。

## 5. 與本次練習的關係

- **已完成**：分段遞迴；時間 O(n)，呼叫堆疊 O(h)，輸出另計。
- **尚待獨立實作**：one-pass、多狀態 DFS；時間與堆疊界相同，重點是狀態傳遞與輸出時機的整合。
- **關鍵字**：Preorder + Postorder、Multi-state DFS、Boundary Flags、Top-down State Propagation、Traversal Events。
- 延伸：[遞迴設計原則](../Algorithms/Design_Principles/Recursion/01-Recursion_Design_Principles.md)、[Binary Tree Traversal](../Data_Structures/Trees/Binary_Trees/Binary_Tree_Traversal.md)、[Problem Review](../Checklists/Lists/09_Problem_Review.md)。

## ✅ 閱讀後應能回答

- [ ] 教材收錄同型題，為何不能推論它是 LeetCode 的直接來源？
- [ ] 左右邊界與葉節點如何分工，才能避免重複？
- [ ] 如何由父節點傳遞邊界身分，並利用進入／返回事件安排輸出？
- [ ] 為何 one-pass 的價值在設計整合，而非把本題由 O(n²) 改成 O(n)？
