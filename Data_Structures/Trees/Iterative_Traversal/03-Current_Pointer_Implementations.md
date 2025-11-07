# Current Pointer 實作模式 / Iterative Traversal Implementations

## 核心概念：隱式狀態追蹤

本文展示使用 **Current Pointer + Stack** 的隱式狀態追蹤模式實作三種遍歷。這種方法不使用顯式的 state flag，而是透過指標位置和輔助變數來隱式追蹤訪問狀態。

**核心組件**：

- **`TreeNode* root`/`current`**：當前正要探索的節點（狀態指標）
- **`stack<TreeNode*> s`**：待處理的父節點（pending tasks）
- **`TreeNode* lastVisited`**（Postorder 專用）：追蹤上一個完成的節點

**Stack 用途隨遍歷變化**：

| Traversal     | Stack 用途               | 額外狀態           |
| ------------- | ------------------------ | ------------------ |
| **Preorder**  | 保存父節點以便探索右子樹 | 無                 |
| **Inorder**   | 保存待處理的父節點       | 無                 |
| **Postorder** | 保存待處理的父節點       | `lastVisited` 指標 |

**為何 Postorder 需要 `lastVisited`？**
必須區分「從左返回」vs「從右返回」，確保右子樹在父節點前被訪問，且只訪問一次。

> 💡 **相關文件**：關於 `lastVisited` 的深入解析，請參見 [`04-Postorder_lastVisited_Deep_Dive.md`](04-Postorder_lastVisited_Deep_Dive.md)

---

## 1. Preorder Traversal (根 -> 左 -> 右)

**目標**: 先處理當前節點，再處理其左子樹，最後處理其右子樹。

### 實作 (狀態驅動版)

此版本透過 `root` 指標是否為 `nullptr` 來驅動狀態轉換。

```cpp
class Solution {
public:
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> ans;
        stack<TreeNode*> s;

        while (root || !s.empty()) {
            if (root) {
                ans.push_back(root->val); // 處理當前節點
                s.push(root);             // 保存父節點以便後續探索右子樹
                root = root->left;        // 深入左子樹
            } else {
                root = s.top(); s.pop();  // 左路徑已盡，返回父節點
                root = root->right;       // 探索右子樹
            }
        }
        return ans;
    }
};
```

### 實作 (任務驅動版)

此版本將堆疊視為一個「待辦事項」列表，更直觀地模擬遞迴。

```cpp
class Solution {
public:
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> ans;
        stack<TreeNode*> s;
        if (root) s.push(root);

        while (!s.empty()) {
            const auto curr = s.top(); s.pop();
            ans.push_back(curr->val); // 處理節點

            // 模擬遞迴呼叫：先推右再推左，以確保先處理左
            if (curr->right) s.push(curr->right);
            if (curr->left) s.push(curr->left);
        }
        return ans;
    }
};
```

---

## 2. Inorder Traversal (左 -> 根 -> 右)

**目標**: 先處理左子樹，再處理當前節點，最後處理右子樹。

### 實作 (if/else 分支版)

```cpp
class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> ans;
        stack<TreeNode*> s;

        while (root || !s.empty()) {
            if (root) {
                s.push(root);      // 延後處理，先保存節點
                root = root->left; // 深入左子樹
            } else {
                root = s.top(); s.pop(); // 左路徑已盡，取出節點
                ans.push_back(root->val); // 處理該節點
                root = root->right;    // 探索右子樹
            }
        }
        return ans;
    }
};
```

### 實作 (內嵌迴圈版)

此版本將「探左」的邏輯內聚，結構更清晰。

```cpp
class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> ans;
        stack<TreeNode*> s;

        while (root || !s.empty()) {
            // 1. 一路向左，將路徑上的節點全部入棧
            while (root) {
                s.push(root);
                root = root->left;
            }

            // 2. 到達最左端，從堆疊頂部取出節點處理
            root = s.top(); s.pop();
            ans.push_back(root->val);

            // 3. 轉向右子樹，開始下一輪的「一路向左」
            root = root->right;
        }
        return ans;
    }
};
```

---

## 3. Postorder Traversal (左 -> 右 -> 根)

**目標**: 先處理左子樹，再處理右子樹，最後處理當前節點。

### 實作 (if/else 分支版)

```cpp
class Solution {
public:
    vector<int> postorderTraversal(TreeNode* root) {
        vector<int> ans;
        stack<TreeNode*> s;
        TreeNode* lastVisited = nullptr;

        while (root || !s.empty()) {
            if (root) {
                s.push(root);
                root = root->left;
            } else {
                TreeNode* peekNode = s.top();
                // 檢查右子樹是否存在且尚未訪問
                if (peekNode->right && peekNode->right != lastVisited) {
                    root = peekNode->right;
                } else {
                    // 左、右子樹均已處理完畢
                    ans.push_back(peekNode->val);
                    s.pop();
                    lastVisited = peekNode;
                    root = nullptr; // 設為 nullptr 以便從堆疊取下一個父節點
                }
            }
        }
        return ans;
    }
};
```

### 實作 (內嵌迴圈版)

此版本突顯了與 Inorder 的關鍵差異：窺視 (`peek`) 而非立即彈出。

```cpp
class Solution {
public:
    vector<int> postorderTraversal(TreeNode* root) {
        vector<int> ans;
        stack<TreeNode*> s;
        TreeNode* lastVisited = nullptr;

        while (root || !s.empty()) {
            // 1. 一路向左，將路徑上的節點全部入棧
            while (root) {
                s.push(root);
                root = root->left;
            }

            // 2. 到達最左端，窺視堆疊頂部的節點
            TreeNode* peekNode = s.top();

            // 3. 決定是處理右子樹，還是處理當前節點
            if (peekNode->right && peekNode->right != lastVisited) {
                // 如果右子樹存在且未被訪問，則轉向右子樹
                root = peekNode->right;
            } else {
                // 否則，表示左右子樹都已處理完畢，可以處理當前節點
                ans.push_back(peekNode->val);
                s.pop();
                lastVisited = peekNode;
                root = nullptr; // 保持 root 為 nullptr，以便下一輪繼續從堆疊頂部判斷
            }
        }
        return ans;
    }
};
```

### 核心差異分析：Inorder vs Postorder (內嵌迴圈版)

- **Inorder**: 當從堆疊中取出節點時 (`s.pop()`)，是**無條件處理**該節點，然後轉向右子樹。
- **Postorder**: 當窺視堆疊頂部節點時 (`s.top()`)，是**有條件的**。它必須先檢查右子樹的狀態。只有當右子樹不存在或已被訪問過時，才能處理並彈出 (`s.pop()`) 該節點。如果需要訪問右子樹，節點會**暫時留在堆疊中**。這個「窺視而不立即彈出」的行為是 Postorder 的精髓。
