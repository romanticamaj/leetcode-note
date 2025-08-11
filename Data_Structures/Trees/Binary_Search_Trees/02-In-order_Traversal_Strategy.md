# BST 解題心法：利用 In-order Traversal 的有序性

二元搜尋樹（Binary Search Tree, BST）一個最重要的特性是：**中序遍歷（In-order Traversal）會得到一個嚴格遞增的有序序列**。這個特性是許多 BST 題目的解題關鍵。

---

## 核心思想

在對 BST 進行 In-order Traversal 的過程中，我們可以利用其有序性來進行即時的比較和判斷。

- **與前一個節點比較**：當訪問到當前節點時，它一定比「上一個」被訪問的節點大。
- **與後一個節點比較**：當前節點一定比「下一個」將被訪問的節點小。

---

## 如何實現？

通常，我們會使用一個外部變數（例如 `prev_node` 或 `prev_val`）來記錄中序遍歷中「上一個」被訪問的節點。

**範例：驗證一棵樹是否為 BST**

```cpp
#include <limits>

long long prev_val = std::numeric_limits<long long>::min(); // 使用 numeric_limits 確保初始值為最小值

bool isValidBST(TreeNode* root) {
    if (root == nullptr) {
        return true;
    }

    // 1. 先遞迴檢查左子樹
    if (!isValidBST(root->left)) {
        return false;
    }

    // 2. 處理當前節點 (In-order 位置)
    //    當前節點的值必須大於前一個節點的值
    if (root->val <= prev_val) {
        return false;
    }
    prev_val = root->val; // 更新前一個節點的值

    // 3. 再遞迴檢查右子樹
    return isValidBST(root->right);
}
```

---

## 適用場景

這個心法適用於所有需要利用 BST「局部有序性」或「全局有序性」的題目，例如：

- **驗證 BST**：如上例，檢查中序遍歷是否嚴格遞增。
- **尋找第 K 小/大元素**：中序遍歷的第 K 個元素就是第 K 小元素。
- **尋找兩個節點的最小絕對差**：在中序遍歷過程中，最小差值一定出現在相鄰的兩個節點之間。
- **將 BST 轉換為排序好的鏈表**：在中序遍歷的過程中，修改節點的指標。

---

---

## 結論

當題目給定的是一棵 BST 時，請立刻想到「**In-order Traversal = Sorted Array**」。這個特性是解開許多 BST 問題的鑰匙，能讓你將複雜的樹問題，轉化為更簡單的有序序列問題。
