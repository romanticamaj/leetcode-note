# 二元樹的迭代式 DFS 遍歷

## 核心概念總結

在三種迭代遍歷中，`root` 指標統一表示當前正要探索的節點。`stack` 的用途則根據遍歷順序的目標而變化：

- **Preorder Traversal (前序遍歷)**:
  - `stack`: 主要用於保存父節點，以便在完成左子樹的探索後，能返回並探索其右子樹。

- **In-order Traversal (中序遍歷)**:
  - `stack`: 用於保存路徑上的父節點，其目的有二：(1) 在左子樹處理完畢後，返回以處理該父節點；(2) 接著探索右子樹。

- **Post-order Traversal (後序遍歷)**:
  - `stack`: 同樣用於保存路徑上的父節點，目的也是 (1) 稍後處理 和 (2) 探索右節點。
  - 需要搭配一個額外的 `lastVisited` 標記，以確保右子樹在父節點之前被正確訪問，且 `只訪問一次`。(關鍵設計策略!!!)

---

本文件探討二元樹 Preorder、Inorder 和 Postorder 遍歷的迭代實現。其核心思想是使用一個顯式的 `stack` 資料結構和一個指向當前節點 (`root`) 的指標，來精確模擬遞迴調用堆疊（call stack）的行為。

## 核心組件

- **`TreeNode* root`**: 此指標代表當前處理的節點或子樹，作為遍歷過程中的「程式計數器」。
- **`stack<TreeNode*> s`**: 此堆疊明確管理遞迴中由調用堆疊隱式處理的狀態，主要用於儲存待返回的父節點。
- **`TreeNode* lastVisited`** (用於 Postorder): 一個額外的狀態變數，用於區分是從左子節點還是右子節點返回父節點。

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
