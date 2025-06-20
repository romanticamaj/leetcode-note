# Morris Traversal for Inorder

Morris Traversal 是一種在 O(1) 空間複雜度下，對二元樹進行中序遍歷的演算法。它不使用遞迴或堆疊，而是巧妙地修改樹的結構來記錄返回路徑。

---

## 核心思想

其核心思想是利用樹中「空的」右子指標（`right pointer`）來建立一個臨時的「線索」（thread），指向中序遍歷中的下一個節點（即當前節點的後繼者）。

1.  **當前節點 `curr` 的左子樹為空**：

    - 訪問 `curr`。
    - 移動到 `curr` 的右子節點。

2.  **當前節點 `curr` 的左子樹不為空**：
    - 找到 `curr` 在中序遍歷中的**前驅節點**（predecessor），即其左子樹中最右側的節點。
    - **如果前驅節點的右子指標為空**：
      - 將其右子指標指向 `curr`（建立線索）。
      - 移動到 `curr` 的左子節點。
    - **如果前驅節點的右子指標指向 `curr`**：
      - 說明左子樹已經遍歷完畢。
      - 斷開線索（將前驅節點的右子指標恢復為 `nullptr`）。
      - 訪問 `curr`。
      - 移動到 `curr` 的右子節點。

---

## 演算法步驟

```cpp
void morrisInorderTraversal(TreeNode* root) {
    TreeNode* curr = root;
    while (curr != nullptr) {
        if (curr->left == nullptr) {
            // 1. 左子樹為空，訪問當前節點，移至右子樹
            cout << curr->val << " ";
            curr = curr->right;
        } else {
            // 2. 左子樹不為空，找到前驅節點
            TreeNode* predecessor = curr->left;
            while (predecessor->right != nullptr && predecessor->right != curr) {
                predecessor = predecessor->right;
            }

            if (predecessor->right == nullptr) {
                // 2a. 建立線索，移至左子樹
                predecessor->right = curr;
                curr = curr->left;
            } else {
                // 2b. 斷開線索，訪問當前節點，移至右子樹
                predecessor->right = nullptr;
                cout << curr->val << " ";
                curr = curr->right;
            }
        }
    }
}
```

---

## 優點與缺點

| 優點                                | 缺點                               |
| ----------------------------------- | ---------------------------------- |
| **空間複雜度 O(1)**：無需額外空間。 | **暫時修改樹結構**：非執行緒安全。 |
| **無遞迴**：避免了堆疊溢位的風險。  | **程式碼較複雜**：不如遞迴直觀。   |

---

## 適用場景

- 當記憶體空間極度受限時。
- 當需要避免遞迴深度過大的問題時。
- 在面試中，作為一個展示對樹遍歷深入理解的進階解法。

雖然在常規開發中不常用，但 Morris Traversal 是理解樹結構和指標操作的一個絕佳練習。

---

## 與 Threaded Binary Tree 的關係

Morris Traversal 的核心思想與 **線索二元樹（Threaded Binary Tree）** 非常相似，但有一個關鍵的區別：

- **Threaded Binary Tree**：

  - 是一種**靜態**的資料結構。
  - 它**永久性地**修改樹的結構，將所有原本為 `nullptr` 的右子指標（對於中序遍歷）指向其後繼者，並用一個布林標記來區分「線索」和「正常的子節點指標」。
  - 一旦建立，遍歷可以非常高效，但樹的結構被改變了。

- **Morris Traversal**：
  - 是一種**動態**的演算法過程。
  - 它在遍歷過程中**暫時性地**建立線索，並在完成對某個子樹的遍歷後，**立即將其恢復原狀**。
  - 遍歷結束後，樹的結構與原始結構完全相同。

**可以這樣理解**：Morris Traversal 就像是在「飛行中」即時建立和拆除一個臨時的 Threaded Binary Tree，以達到 O(1) 空間複雜度的遍歷，同時又不永久性地破壞原始樹的結構。
