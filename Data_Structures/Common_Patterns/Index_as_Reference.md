# 心法：使用索引作為參考 (Index as Reference)

## 核心思想

在演算法中，當需要在輔助資料結構（如 `priority_queue`, `queue`, `vector`）中儲存或追蹤一組複雜物件（如二維座標、自訂結構）時，應優先考慮**只儲存這些物件在原始輸入容器中的索引**，而非複製整個物件。

這種「索引即參考」的模式是一種空間優化技巧，它利用一個輕量級的整數（索引）來間接指向一個重量級的資料，從而達成以下優點：

1. **空間效率**：顯著減少輔助資料結構的記憶體開銷。儲存 `int` 或 `size_t` 遠比儲存 `vector<int>`、`pair<int, int>` 或自訂物件更節省空間。
2. **時間效率**：減少資料複製的成本。將索引推入容器通常比複製整個物件更快。
3. **程式碼簡潔性**：在需要存取原始物件時，只需透過 `original_data[index]` 即可，邏輯清晰。

## 應用場景與範例

### 1. Top-K 問題 (以 LeetCode 973. K Closest Points to Origin 為例)

**問題描述**：給定一個 `points` 陣列，其中 `points[i] = [xi, yi]`，找到最接近原點的 `k` 個點。

**優化前思路**：
建立一個 `priority_queue<pair<double, pair<int, int>>>`，其中儲存 `(距離, {x, y})`。

```cpp
// 優化前：儲存 pair<int, int>
priority_queue<pair<double, pair<int, int>>> q;
for (auto const& p : points) {
    const int x = p[0];
    const int y = p[1];
    const double distance = std::sqrt(x * x + y * y);
    q.push({distance, {x, y}}); // 儲存了座標本身
    if (q.size() > k) q.pop();
}
```

**優化後思路 (索引即參考)**：
建立一個 `priority_queue<pair<double, int>>`，其中儲存 `(距離, 索引)`。這樣 `priority_queue` 的空間複雜度從 `O(k * sizeof(point))` 降至 `O(k * sizeof(int))`。

```cpp
// 優化後：只儲存索引
priority_queue<pair<double, int>> q;
for (int i = 0; i < points.size(); ++i) {
    const int x = points[i][0];
    const int y = points[i][1];
    const double distance = std::sqrt(x * x + y * y);
    q.push({distance, i}); // 只儲存索引 i
    if (q.size() > k) q.pop();
}

// 建構結果時，再透過索引取回座標
vector<vector<int>> result;
while (!q.empty()) {
    int index = q.top().second;
    q.pop();
    result.push_back(points[index]);
}
```

### 2. Index Mapping：批次操作的索引映射

當需要協調**多個操作**，每個操作都有「目標位置」和「操作資料」時，使用 `pair<位置索引, 資料索引>` 可以：
1. **追蹤位置**：記錄操作在序列中的位置
2. **快速查找資料**：透過資料索引存取相關資訊

**應用場景**：批次字串替換、批次刪除元素

```cpp
// 場景：多個替換操作，每個有位置和對應的替換資料
vector<int> positions;        // 替換位置
vector<string> sources;       // 原始字串
vector<string> targets;       // 目標字串

// 建立索引映射：位置 -> 操作編號
vector<pair<int, int>> mapping;  // {position, operation_index}
for (int i = 0; i < positions.size(); i++) {
    mapping.push_back({positions[i], i});
}

// 可以按位置排序，便於處理
sort(mapping.rbegin(), mapping.rend());  // 逆序：從右到左處理

// 使用映射處理每個操作
for (auto [pos, opIdx] : mapping) {
    // 透過 opIdx 快速存取操作資料
    const string& source = sources[opIdx];
    const string& target = targets[opIdx];
    // 在位置 pos 進行替換
}
```

**核心優勢**：
- ✅ **資料分離**：位置資訊和操作資料分開儲存
- ✅ **靈活排序**：可按位置排序，不影響資料存取
- ✅ **空間效率**：只需儲存整數索引，不需複製操作資料

### 3. 圖演算法 (Graph Algorithms)

這個原則在圖論中是標準實踐。當節點本身是複雜物件（例如，一個二維網格中的座標 `(r, c)`）時，我們通常會：

1. **建立對應關係**：將複雜的節點（如 `pair<int, int>`）映射到一個唯一的整數 ID（`0` 到 `N-1`）。
2. **使用 ID 操作**：在鄰接串列、`visited` 集合、BFS/DFS 的佇列中，都只使用這些整數 ID。

這避免了在各種資料結構中儲存大量重複的 `pair` 或其他自訂結構。

**範例**：在一個 `m x n` 的網格上進行 BFS，可以將座標 `(r, c)` 映射到 `id = r * n + c`。

```cpp
// 概念程式碼
queue<int> q;
vector<bool> visited(m * n, false);

int start_id = start_r * n + start_c;
q.push(start_id);
visited[start_id] = true;

while (!q.empty()) {
    int curr_id = q.front();
    q.pop();

    // 從 id 反向計算座標
    int r = curr_id / n;
    int c = curr_id % n;

    // ... 處理鄰居 ...
}
```

## 總結心法

當演算法中的輔助資料結構需要引用原始輸入資料時，問自己一個問題：「我需要儲存整個物件，還是只需要一個指向它的方式？」

在大多數情況下，儲存**索引**就足夠了。這個簡單的轉變是提升程式碼空間效率和優雅性的關鍵一步。
