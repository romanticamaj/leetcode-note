# 樹狀遞迴設計心法：從基本結構到優雅解

本文旨在從第一性原理出發，拆解並推導出一種優雅且高效的樹狀遞迴設計模式。這個模式透過組合兩個關鍵優化技巧，能簡潔地解決許多看似複雜的樹狀問題。

## 1. 萬用骨架：後序遍歷遞迴

任何一個樹的遞迴函式，其最基本的結構都基於**後序遍歷 (Post-order Traversal)**。這個骨架確保我們在處理當前節點 `root` 之前，已經拿到了其左右子樹的處理結果。

**基本遞迴骨架**：

```cpp
ReturnType solve(TreeNode* root, ...args) {
    // 1. Base Case: 處理空節點，返回一個代表「無」或「空」的值
    if (root == nullptr) {
        return identity_value; // e.g., nullptr, 0, true/false
    }

    // 2. 遞迴收集：從左右子樹收集資訊
    ReturnType left_result = solve(root->left, ...args);
    ReturnType right_result = solve(root->right, ...args);

    // 3. 聚合邏輯：根據左右子樹的結果和當前節點的狀態，計算並返回結果
    return aggregate(left_result, right_result, root);
}
```

這個結構是我們所有優化的基礎。

---

## 2. 優化一：提前返回 (Pre-order Pruning)

在深入遞迴之前，我們可以加入一個**前序 (Pre-order)** 的判斷，用於**剪枝**。

**思考邏輯**：

> 「在探訪子樹之前，我能否根據 `root` 當前的狀態，就直接確定這整棵子樹的答案？如果可以，就沒必要再往下走了。」

**程式碼實現**：
這個判斷被加在遞迴收集**之前**。

```cpp
ReturnType solve(TreeNode* root, ...args) {
    if (root == nullptr) {
        return identity_value;
    }

    // << 優化點：Pre-order Pruning >>
    if (is_target(root, ...args)) {
        return root; // 或其他代表「已找到」的證據
    }

    ReturnType left_result = solve(root->left, ...args);
    ReturnType right_result = solve(root->right, ...args);

    return aggregate(left_result, right_result, root);
}
```

這個技巧能大幅減少不必要的遞迴呼叫，尤其當目標節點靠近樹根時。

---

## 3. 優化二：證據聚合 (Post-order Evidence Aggregation)

這是模式中最精妙的部分，它要求我們重新定義 `aggregate` 邏輯。核心是建立一個清晰的**「回傳值契約 (Return Value Contract)」**。

**回傳值契約**：
函式的回傳值不應只是一個簡單的數值，而應被視為一份**「證據」**。這份證據能告訴上層呼叫者，在這棵子樹中發生了什麼。

**聚合邏輯**：
在後序位置，我們根據從左右子樹收集到的 `left_result` 和 `right_result` 這兩份證據，來決定當前 `root` 節點要向上層提交什麼新的、更強的證據。

這通常可以被抽象成一個**證據聚合四象限**：

| 左子樹證據 (`left`) | 右子樹證據 (`right`) | 當前節點 (`root`) 的決策 | 意義                                                                               |
| :------------------ | :------------------- | :----------------------- | :--------------------------------------------------------------------------------- |
| `空證據`            | `空證據`             | `return 空證據;`         | **無發現**：左右皆空，此子樹無任何發現。                                           |
| **有效證據**        | `空證據`             | `return 左證據;`         | **單邊發現**：僅左側有發現，將此證據向上传遞。                                     |
| `空證據`            | **有效證據**         | `return 右證據;`         | **單邊發現**：僅右側有發現，將此證據向上传遞。                                     |
| **有效證據**        | **有效證據**         | `return 處理交匯(root);` | **證據交匯**：兩側皆有發現。當前節點成為關鍵決策點，需合併、比較或宣告自身為答案。 |

---

## 4. 案例研究：最低共同祖先 (LCA)

現在，我們將上述心法應用於 LCA 問題。

**問題定義**：尋找節點 `p` 和 `q` 的最低共同祖先。

1. **定義回傳值契約**：

   - 回傳 `TreeNode*` 作為「證據」。
   - `nullptr` 代表「空證據」（未找到 `p` 或 `q`）。
   - 非 `nullptr` 代表「有效證據」（找到了 `p`、`q` 或它們的 LCA）。

2. **套用遞迴骨架與優化**：

```cpp
TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    // 1. Base Case: 空節點返回「空證據」
    if (root == nullptr) {
        return nullptr;
    }

    // 2. 優化一：Pre-order Pruning
    // 如果當前節點是 p 或 q，它就是這棵子樹能提供的最強證據
    if (root == p || root == q) {
        return root;
    }

    // 3. 遞迴收集證據
    TreeNode* leftEvidence = lowestCommonAncestor(root->left, p, q);
    TreeNode* rightEvidence = lowestCommonAncestor(root->right, p, q);

    // 4. 優化二：Post-order Evidence Aggregation
    // 應用證據聚合四象限邏輯
    if (leftEvidence && rightEvidence) {
        return root; // 左右都有證據 -> 我是 LCA (交匯點)
    }
    // 如果只有一邊有證據，就將該證據向上传遞
    // 如果兩邊都沒證據，leftEvidence 為空，返回 rightEvidence (也是空) 也正確
    return leftEvidence ? leftEvidence : rightEvidence;
}
```

## 總結心智模型

通過這個推導過程，我們得到了一個強大的遞迴設計流程：

1. **建立骨架**：從後序遍歷的基本結構開始。
2. **定義契約**：明確回傳值的「證據」意義。
3. **思考剪枝**：加入「提前返回」的 Pre-order 判斷來優化效能。
4. **設計聚合**：根據回傳值契約，設計優雅的「證據聚合」邏輯。

這個從基本到優雅的構建過程，才是真正可遷移的、解決複雜遞迴問題的核心能力。
