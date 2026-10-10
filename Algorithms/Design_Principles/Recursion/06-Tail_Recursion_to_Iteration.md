# 尾遞迴消除：單一路徑搜尋（Tail Recursion → Iteration）解題心法

**難度**：⭐⭐｜**核心問題**：往下解完子問題後，父層還有什麼事要做？

若每一步只選一個子問題，且直接回傳它的答案，父層就沒有待完成的工作。
當必要狀態可用固定數量變數保存時，可以用「更新狀態 → 下一輪」取代遞迴，不必保存 stack。

## 🧠 三個概念，分開理解

| 概念 | 回答的問題 | 意義 |
| --- | --- | --- |
| Decrease and conquer（減治） | 要解幾個子問題？ | 只解一個更小的子問題 |
| Tail recursion（尾遞迴） | 子問題回來後還要做什麼？ | 直接回傳子問題的結果，沒有後續工作 |
| Tail recursion elimination | 如何執行這條呼叫鏈？ | 用迴圈更新狀態，省掉不必要的父層紀錄 |

**減治不一定是尾遞迴，尾遞迴也不保證整個演算法只用 O(1) 空間。**
例如 `return n * factorial(n - 1)` 只解一個子問題，但回來後還要乘上 `n`，不是尾遞迴。
若能另行設計 accumulator，也可能改寫；這需要重新整理狀態，不能直接刪掉 stack。

## 🧩 轉換口訣：判停 → 選路 → 換狀態

| 步驟 | 檢查與動作 |
| --- | --- |
| 判停 | 將遞迴的 base case 轉成 return／break |
| 選路 | 證明只需保留哪一個子問題 |
| 換狀態 | 將遞迴參數改成下一輪狀態 |
| 檢查回程 | 確認沒有 combine、待探索分支或其他未完成工作 |

`return solve(nextState)` 可以改成更新目前狀態，再進入下一輪。
若有多個狀態變數，更新時須保留彼此需要的舊值。

## 原型：BST 的 Lowest Common Ancestor

前提：BST 節點值唯一，`p`、`q` 都存在於樹中。
兩者同側時，只搜尋該側；分居兩側，或目前節點就是其中之一時，答案已確定。

```cpp
TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    while (root) {
        if (root == p || root == q)
            return root;

        if (p->val < root->val && q->val < root->val)
            root = root->left;  // 取代 return solve(root->left, p, q)
        else if (p->val > root->val && q->val > root->val)
            root = root->right;
        else
            return root;       // 分居左右子樹，不必是直接 children
    }
    return nullptr;
}
```

這裡只有 `root` 隨搜尋改變；`p`、`q` 固定不變。
父層原本只會直接回傳子問題的答案，因此不必記住父節點，也不必模擬返回地址。

## ✅ 正確性與終止

**Loop invariant：目前 root 的子樹仍包含 p、q，因此也包含它們的 LCA。**

1. **初始化**：原始樹包含兩個目標，invariant 成立。
2. **維持**：兩者同側時，該側子樹已包含兩者，LCA 必在其中；更新 root 不會排除答案。
3. **回傳**：分居兩側時，更低的節點無法涵蓋兩者；遇到其中一個目標時，另一個仍在其子樹內。兩種情況的 root 都是 LCA。
4. **終止**：每次繼續搜尋都下降一層；有限樹高保證不會無限執行。

## 從通用分治到減治：額外 constraint 的作用

| 階段 | 可用資訊與策略 | 時間 | 輔助空間 |
| --- | --- | --- | --- |
| 一般 Binary Tree LCA | 不知道目標在哪側，搜尋左右再 combine | O(n) | O(h) |
| BST LCA，遞迴 | 利用順序選一側，直接回傳子問題結果 | O(h) | O(h) |
| BST LCA，迭代 | 同樣選一側，以更新 root 取代尾遞迴 | O(h) | O(1) |

**BST constraint 改變搜尋策略；尾遞迴消除改變執行方式。**
先有「可證明另一側不需要搜尋」，才能從左右聚合改成單一路徑。
再有「回來後沒有工作」，才能直接用迴圈執行這條路徑。

## ⚠️ 常見陷阱

- **只有一個子問題就直接省 stack**：仍須檢查回程工作與必要狀態。
- **改成迭代就一定 O(1)**：explicit stack、成長中的容器與輸出成本仍需另外計算。
- **BST 就是 O(log n)**：沒有平衡保證；h 最壞可達 n。
- **剪枝就是減半**：保留的子樹可能只比原問題少一個節點。
- **依賴編譯器消除尾呼叫**：C++ 不保證此最佳化；手動迴圈才保證本例 O(1) 輔助空間。

## 相關心法

- [遞迴四大流派](State_Design_Across_Recursive_Paradigms.md)：比較子問題的組織方式。
- [遞迴轉迭代](../../../Data_Structures/Trees/Iterative_Traversal/01-Recursive_to_Iterative_Conversion.md)：需要保存回程工作時的 explicit stack。
- [將限制轉化為工具](../Transformation_Patterns/Transforming_Constraints_into_Tools.md)：將輸入保證轉成可排除搜尋分支的證據。

**自問：額外條件排除了哪些分支？子問題回來後還有工作嗎？下一輪真正需要保存什麼？**
