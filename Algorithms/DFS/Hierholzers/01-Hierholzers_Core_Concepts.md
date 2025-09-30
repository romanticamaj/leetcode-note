# Hierholzer's Algorithm 核心概念

## 問題定義

- **Eulerian Path（歐拉路徑）**: 一條通過圖中**每一條邊**恰好一次的路徑
- **Eulerian Circuit（歐拉迴路）**: 起點和終點相同的歐拉路徑

**存在條件**：

- Eulerian Circuit: 所有節點的入度 = 出度
- Eulerian Path: 最多兩個節點的入度 ≠ 出度（起點出度多 1，終點入度多 1）

## 算法核心概念

Hierholzer's Algorithm 是一個貪心算法，透過 DFS 遍歷所有邊並利用 Post-order 特性建構路徑。

### 算法直覺

1. **貪心探索**：從起點開始，沿著任意未訪問的邊深入
2. **碰壁回溯**：當到達沒有未訪問出邊的節點時「碰壁」
3. **縫合迴路**：回溯時探索其他分支，形成新的迴路並縫合到主路徑
4. **反轉結果**：Post-order 收集的是反向路徑，需要反轉

**關鍵洞察**：因為入度=出度（除了起終點），進入中間節點後一定有路離開，只會在起點或終點碰壁。

## Post-Order Collection 的重要性

### 核心原理

```cpp
void dfs(current) {
    // Step 1: 探索所有出邊
    for (edge : unvisited_edges_from(current)) {
        mark_visited(edge);
        dfs(edge.target);
    }

    // Step 2: Post-order - 所有出邊探索完才收集
    collect(current);  // 關鍵：在這裡收集
}
```

### 為什麼必須是 Post-Order？

考慮圖：`A→C`, `C→A`, `A→B`，從 A 開始，假設訪問順序為 B 優先於 C。

#### Pre-Order 的錯誤（過早承諾）

```
1. 進入 A，收集 A → path: [A]
2. 選擇 A→B，進入 B，收集 B → path: [A, B]
3. B 無出邊，回溯到 A
4. 選擇 A→C，進入 C，收集 C → path: [A, B, C]
5. 選擇 C→A，進入 A，收集 A → path: [A, B, C, A]

結果：[A, B, C, A] ✗ 錯誤順序
```

問題：Pre-order 過早地將 B 固定在路徑中，無法正確插入 A→C→A 迴路。

#### Post-Order 的正確性

```
1. 從 A 出發，選擇 A→B
2. B 無出邊，碰壁，收集 B → path: [B]
3. 回溯到 A，選擇 A→C
4. 從 C 出發，選擇 C→A
5. A 無未訪問邊，碰壁，收集 A → path: [B, A]
6. 回溯到 C，無未訪問邊，收集 C → path: [B, A, C]
7. 回溯到起始 A，收集 A → path: [B, A, C, A]
8. 反轉得到：[A, C, A, B] ✓ 正確

實際路徑：A→C→A→B
```

**關鍵洞察**：Post-order 確保一個節點只有在其所有分支都探索完並正確縫合後才被收集，避免過早固定順序。

## 算法步驟詳解
 
### 1. 初始化

```cpp
// 選擇起點
startNode = findStartNode();  // Euler Path: 出度 > 入度的節點
                              // Euler Circuit: 任意節點
```

### 2. DFS 遍歷

```cpp
void dfs(node) {
    while (hasUnvisitedEdge(node)) {
        edge = getUnvisitedEdge(node);
        markVisited(edge);
        dfs(edge.target);
    }
    // Post-order: 所有邊都訪問完
    result.push_back(node);
}
```

### 3. 路徑建構

```cpp
dfs(startNode);
reverse(result);  // 反轉得到正確順序
```

## 複雜度分析

### 時間複雜度

- **基本情況**：O(V + E) - 每條邊訪問一次
- **需要排序**：O(E log E) - 如字典序要求

### 空間複雜度

- **遞迴堆疊**：O(V) - 最深可能訪問所有節點
- **儲存結構**：O(V + E) - 鄰接表或邊集合

## 正確性證明

1. **完整性**：每條邊恰好訪問一次（標記機制保證）
2. **連續性**：Post-order 確保迴路正確縫合
3. **可達性**：入度=出度保證中間節點一定有出路

## ✅ 核心要點

- Hierholzer's Algorithm 是找 Eulerian Path/Circuit 的標準算法
- **Post-order Collection** 是算法正確性的關鍵
- 收集的是反向路徑，需要最後反轉
- 適用於「一筆畫」類型的問題
