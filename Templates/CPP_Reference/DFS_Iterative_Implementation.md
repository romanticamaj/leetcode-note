# DFS 迭代實現參考 (C++)

本文檔提供了深度優先搜索 (DFS) 的迭代實現方法，使用 C++ 語言。迭代實現避免了遞歸調用的開銷，在某些情況下可以提高效率，並且避免了遞歸深度過大導致的棧溢出問題。

## 二叉樹的迭代 DFS 實現

### 二叉樹節點定義

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};
```

### 前序遍歷 (Preorder Traversal)

前序遍歷順序：根 -> 左 -> 右

```cpp
vector<int> preorderTraversal(TreeNode* root) {
    vector<int> result;
    if (!root) return result;
    
    stack<TreeNode*> s;
    s.push(root);
    
    while (!s.empty()) {
        // 彈出當前節點並訪問
        TreeNode* node = s.top();
        s.pop();
        result.push_back(node->val);
        
        // 注意：先右後左入棧，因為棧是後進先出的
        if (node->right) s.push(node->right);
        if (node->left) s.push(node->left);
    }
    
    return result;
}
```

**關鍵點**：
- 使用棧存儲待訪問的節點
- 先訪問當前節點，再將其子節點入棧
- 由於棧是後進先出的，所以先將右子節點入棧，再將左子節點入棧，這樣出棧時就是先左後右

### 中序遍歷 (Inorder Traversal)

中序遍歷順序：左 -> 根 -> 右

```cpp
vector<int> inorderTraversal(TreeNode* root) {
    vector<int> result;
    if (!root) return result;
    
    stack<TreeNode*> s;
    TreeNode* curr = root;
    
    while (curr || !s.empty()) {
        // 將所有左子節點入棧
        while (curr) {
            s.push(curr);
            curr = curr->left;
        }
        
        // 彈出棧頂節點並訪問
        curr = s.top();
        s.pop();
        result.push_back(curr->val);
        
        // 轉向右子節點
        curr = curr->right;
    }
    
    return result;
}
```

**關鍵點**：
- 使用一個額外的指針 `curr` 跟踪當前節點
- 先將所有左子節點入棧，然後訪問節點，最後轉向右子節點
- 這個模式確保了訪問順序是：左 -> 根 -> 右

### 後序遍歷 (Postorder Traversal)

後序遍歷順序：左 -> 右 -> 根

方法一：使用兩個棧

```cpp
vector<int> postorderTraversal(TreeNode* root) {
    vector<int> result;
    if (!root) return result;
    
    stack<TreeNode*> s1, s2;
    s1.push(root);
    
    // 第一個棧用於生成訪問順序
    while (!s1.empty()) {
        TreeNode* node = s1.top();
        s1.pop();
        s2.push(node);
        
        // 先左後右入棧，這樣在第二個棧中的順序就是：根 -> 右 -> 左
        if (node->left) s1.push(node->left);
        if (node->right) s1.push(node->right);
    }
    
    // 第二個棧的出棧順序就是後序遍歷：左 -> 右 -> 根
    while (!s2.empty()) {
        result.push_back(s2.top()->val);
        s2.pop();
    }
    
    return result;
}
```

方法二：使用一個棧和一個訪問標記

```cpp
vector<int> postorderTraversal(TreeNode* root) {
    vector<int> result;
    if (!root) return result;
    
    stack<TreeNode*> s;
    TreeNode* curr = root;
    TreeNode* lastVisited = nullptr;
    
    while (curr || !s.empty()) {
        // 將所有左子節點入棧
        while (curr) {
            s.push(curr);
            curr = curr->left;
        }
        
        // 查看棧頂節點
        TreeNode* node = s.top();
        
        // 如果右子節點存在且未訪問過，轉向右子節點
        if (node->right && node->right != lastVisited) {
            curr = node->right;
        } else {
            // 訪問當前節點
            result.push_back(node->val);
            lastVisited = node;
            s.pop();
        }
    }
    
    return result;
}
```

**關鍵點**：
- 後序遍歷是三種遍歷中最複雜的
- 方法一：利用兩個棧，先生成「根 -> 右 -> 左」的順序，然後反轉得到「左 -> 右 -> 根」
- 方法二：使用一個額外的指針 `lastVisited` 跟踪上一個訪問的節點，確保右子樹訪問完畢後才訪問根節點

## 圖的迭代 DFS 實現

對於圖的 DFS 遍歷，需要使用訪問標記避免重複訪問節點。

### 鄰接表表示的圖

```cpp
vector<bool> visited;

void dfsIterative(vector<vector<int>>& graph, int start) {
    int n = graph.size();
    visited.assign(n, false);
    
    stack<int> s;
    s.push(start);
    visited[start] = true;  // 入棧時標記為已訪問
    
    while (!s.empty()) {
        int node = s.top();
        s.pop();
        
        cout << node << " ";  // 訪問節點
        
        // 遍歷所有鄰居
        for (int neighbor : graph[node]) {
            if (!visited[neighbor]) {
                s.push(neighbor);
                visited[neighbor] = true;  // 入棧時標記為已訪問
            }
        }
    }
}
```

### 遍歷整個圖（包含多個連通分量）

```cpp
void dfsAllComponents(vector<vector<int>>& graph) {
    int n = graph.size();
    visited.assign(n, false);
    
    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            cout << "Component starting at " << i << ": ";
            dfsIterative(graph, i);
            cout << endl;
        }
    }
}
```

## 迭代 DFS 的關鍵心法

1. **棧的使用**：
   - 使用棧模擬遞歸調用棧
   - 理解棧的後進先出特性，合理安排入棧順序

2. **訪問時機**：
   - 前序遍歷：出棧時立即訪問
   - 中序遍歷：左子樹遍歷完畢後訪問
   - 後序遍歷：左右子樹都遍歷完畢後訪問

3. **避免重複訪問**：
   - 樹：不需要訪問標記（因為沒有循環）
   - 圖：需要使用訪問標記（避免循環）

4. **入棧策略**：
   - 前序遍歷：先右後左入棧
   - 中序遍歷：先將所有左子節點入棧
   - 後序遍歷：需要額外的機制確保根節點在左右子節點之後訪問

5. **入棧順序與訪問順序的關係**：
   - **重要說明**：在迭代實現中，入棧順序和訪問順序是相反的。例如，如果我們先將左子節點入棧，再將右子節點入棧，由於棧的後進先出特性，實際上會先訪問右子樹，再訪問左子樹。
   - 這與遞歸實現中的訪問順序可能相反，但在某些問題中，訪問順序可能不重要。
   - **核心原則**：在迭代實現中，想要先訪問哪個節點，就後將其入棧。

6. **特殊技巧**：
   - 使用 nullptr 作為標記，區分不同階段
   - 使用額外的指針跟踪訪問狀態
   - 使用兩個棧簡化後序遍歷

## 遞歸 vs 迭代

| 特性 | 遞歸實現 | 迭代實現 |
|------|---------|---------|
| 代碼簡潔度 | 更簡潔 | 較複雜 |
| 空間效率 | 使用系統棧，可能導致棧溢出 | 使用顯式棧，可控制大小 |
| 時間效率 | 有函數調用開銷 | 無函數調用開銷，通常更快 |
| 實現難度 | 簡單 | 複雜，特別是中序和後序遍歷 |
| 適用場景 | 樹的深度適中，代碼簡潔性優先 | 樹的深度很大，性能優先 |

## 總結

迭代實現 DFS 的關鍵在於理解遞歸版本的執行流程，然後使用顯式棧模擬這個流程。不同的遍歷順序（前序、中序、後序）需要不同的實現策略，其中後序遍歷是最複雜的。

對於圖的 DFS，還需要使用訪問標記避免重複訪問節點，這在處理有環圖時尤為重要。

掌握這些模式和技巧後，你可以靈活地實現各種 DFS 算法，並根據具體問題選擇最合適的實現方式。