# 廣度優先搜索 (Breadth-First Search, BFS)

## 基本概念

廣度優先搜索是一種遍歷樹或圖的算法，它按照節點的層級順序 (level order) 進行遍歷，先訪問同一層的所有節點，然後再移動到下一層。在二叉樹中，BFS 也被稱為層序遍歷 (Level-Order Traversal)。

### 常用定義

Node 的深度 (depth) : root 到此 node 的距離 (distance)

在 BFS 中，節點的遍歷順序與它們到根節點的距離（深度）成正比。
例如，在一個完全二叉樹中，BFS 遍歷的節點深度順序會是：0, 1, 1, 2, 2, 2, 2, 3, 3, ...

## 實現方式

BFS 通常使用**隊列(queue)**來實現，很少使用遞歸。

### 為什麼需要檢查空節點？

雖然 BFS 通常使用迭代而非遞歸實現，但檢查空節點仍然很重要。
如果不檢查 `root == nullptr`，嘗試訪問 `root->val` 或其他屬性會導致空指針異常，因為 null 不具有這些屬性。
此外，在 BFS 的過程中，我們也需要檢查子節點是否為 null 再將其添加到隊列中。

### 標準 BFS 實現

```cpp
void bfs(TreeNode* root) {
    // 檢查空樹情況
    if (root == nullptr) return;
    
    queue<TreeNode*> q;
    q.push(root);
    
    while (!q.empty()) {
        TreeNode* node = q.front();
        q.pop();
        
        // 處理當前節點
        cout << node->val << " ";
        
        // 將子節點加入隊列
        if (node->left) q.push(node->left);
        if (node->right) q.push(node->right);
    }
}
```

### Level-ordered BFS 實現（明確區分 Level）

```cpp
vector<vector<int>> levelOrder(TreeNode* root) {
    if (root == nullptr) return result;
    
    queue<TreeNode*> q;
    q.push(root);
    
    while (!q.empty()) {
        const int levelSize = q.size(); // 務必先取得同 order 元素數量

        // do some logic here for the current level
        // ...
        
        // 處理當前層的所有節點
        for (int i = 0; i < levelSize; i++) { // 在一個 for loop 中 visit 完同 level 所有元素
            TreeNode* node = q.front();
            q.pop();
            
            // 處理當前節點
            // ...
            
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
    }
    
    return result;
}
```

### 關鍵差異

| 特性 | 標準 BFS | 層序 BFS |
|------|---------|----------|
| 層級識別 | 不跟踪層級信息 | 明確識別每個層級 |
| 層級操作 | 無法在層級級別上進行操作 | 可以對整個層級進行特定操作 |
| 實現複雜度 | 更簡單 | 稍微複雜(多一個 for loop) |
| 適用場景 | 普通的廣度優先遍歷 | 需要按層級處理的問題（如層序遍歷結果、每層的平均值等） |
| 代碼結構 | 單層循環 | 嵌套循環（外層遍歷層級，內層遍歷節點） |

### 實現細節說明

1. **標準 BFS**:
   - 簡單地將節點依序加入隊列並處理
   - 不區分哪些節點屬於同一層級
   - 無法在處理完一個層級後執行特定操作

2. **層序 BFS**:
   - 使用 `int nodesInCurrentLevel = queue.size()` 獲取當前層級的節點數量
     ```
     int nodesInCurrentLevel = queue.size();
     ```
     務必先獲取層級數量，因為內層遍歷節點時會操作 queue 內容，導致 queue 大小改變

     **這是層序 BFS 的關鍵決策點**：當你的 BFS 需要知道 "level"，這行代碼允許你在 while 循環內先把同一層級的所有節點一次性處理完，然後再處理下一層。
   - 使用內層循環精確處理當前層級的所有節點，確保層級的完整性
   - 可以在層級之間添加邏輯（例如，在外層循環中計算每層的平均值或找出每層的最大值）
   - 非常適合需要按層級分組的問題，如返回層序遍歷結果的二維數組，或者需要知道節點在第幾層的問題

### 選擇指南

- 如果不需要區分層級，使用標準 BFS（更簡潔）
- 如果需要按層級處理節點，或者需要知道節點在哪一層，使用層序 BFS
- 層序 BFS 是解決「按層收集節點」、「找到特定層的節點」或「計算每層統計數據」等問題的理想選擇

## BFS 的應用場景

BFS 特別適用於以下場景：

1. **尋找最短路徑**：由於 BFS 按照節點與根節點的距離順序遍歷，它可以用來找到兩個節點之間的最短路徑
2. **層序遍歷**：當需要按層處理樹節點時
3. **連通性問題**：檢查圖中的連通性
4. **查找距離根節點特定距離的所有節點**
5. **查找最接近根節點的特定值**：當目標節點可能在樹的上層時，BFS 可以更快地找到它

## BFS 的特性與優勢

1. **層序處理**：天然適合按層級處理節點
2. **最短路徑**：保證首先找到的路徑是最短的
3. **空間效率**：對於窄而深的樹，BFS 的空間複雜度較低
4. **查找上層節點**：當目標節點靠近根節點時，BFS 更高效

## BFS 的主要缺點

- 如果目標節點在樹的底層，BFS 需要遍歷所有上層節點才能到達底層
- 對於寬而淺的樹，BFS 可能需要存儲大量節點，導致空間複雜度較高
- 實現通常比 DFS 更複雜，特別是需要跟踪層級信息時

## 最佳實踐

- 當問題涉及最短路徑或按層處理時，優先考慮 BFS
- 對於可能在樹上層的目標節點，BFS 通常更高效
- 根據問題需求選擇標準 BFS 或層序 BFS
- 使用隊列 (queue) 實現 BFS，避免使用遞歸