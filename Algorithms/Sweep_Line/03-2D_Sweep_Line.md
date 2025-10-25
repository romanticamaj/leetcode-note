# 2D Sweep Line 解題心法 / 2D Sweep Line Pattern

## 🧠 核心哲學

面對 2D 問題時，**固定一個維度作為掃描軸，將問題降維為一系列 1D 問題**。關鍵洞察：不是在 2D 空間中同時處理所有點，而是一次處理一個主要位置，並在該位置一起處理所有次要值。

## 核心概念：維度分解 (Dimension Decomposition)

將 2D 問題轉換為有序的 1D 掃描：

```cpp
// 主軸提供排序（通常是 X）
map<int, vector<int>> primaryToSecondary;  // X -> Y values

// 按主要維度分組
for (auto& point : points) {
    primaryToSecondary[point.x].push_back(point.y);
}

// 按順序掃描主軸
for (auto& [primary, secondaryValues] : primaryToSecondary) {
    // 在此主要位置處理所有次要值
    processSecondaryDimension(secondaryValues);
}
```

**重點摘要**：固定 X 軸作為掃描線 → 將每個 X 的所有 Y 值分組 → 在每個 X 位置一起處理 Y 值

## 通用模板 / General Template

```cpp
template<typename Point>
void solve2DSweep(vector<Point>& points) {
    // 步驟 1：選擇主軸並將次要值分組
    map<int, vector<int>> sweep;
    for (auto& p : points) {
        sweep[p.primary].push_back(p.secondary);
    }

    // 步驟 2：掃描主軸
    for (auto& [pos, values] : sweep) {
        // 步驟 3：在此位置處理次要值
        // - 如需要則排序
        // - 比較配對
        // - 更新運行狀態
        processAtPosition(pos, values);
    }
}
```

## 🧩 設計模式 / Implementation Patterns

### Pattern 1: 基於 Hash 的分組 (LC939)

```cpp
unordered_map<int, vector<int>> xToY;
for (auto& p : points)
    xToY[p[0]].push_back(p[1]);

// 掃描 x 軸，在每個 x 處理 y 配對
for (auto& [x, ys] : xToY) {
    sort(ys.begin(), ys.end());
    // 在已排序的 y 值中尋找配對
}
```

### Pattern 2: 帶狀態的有序掃描

```cpp
map<int, vector<int>> sweep;  // 按 key 自動排序
State runningState;

for (auto& [x, values] : sweep) {
    // 根據此 x 的值更新狀態
    runningState.update(values);
    // 狀態在掃描過程中傳遞資訊
}
```

## 實作選擇：`map` vs `unordered_map` + sort

### 方法 1：直接使用 `map`（推薦起手式）

```cpp
map<int, vector<int>> xToY;  // 自動排序
for (auto& point : points) {
    xToY[point[0]].push_back(point[1]);
}

// 迭代時已經按 x 排序
for (auto& [x, yValues] : xToY) {
    sort(yValues.begin(), yValues.end());
    // 處理當前 x 的所有 y 值...
}
```

**特點**：

- ✅ 簡單直接，一步到位
- ✅ 自動維護 key 的排序
- ✅ 程式碼清晰，符合直覺
- 複雜度：O(n log n) 插入

**適用情況**：

- 大部分面試場景
- unique keys 數量 ≈ 資料點數量（k ≈ n）
- 資料規模不大（n < 10⁴）

### 方法 2：`unordered_map` + 提取排序（效能優化）

```cpp
unordered_map<int, vector<int>> xToY;
for (auto& point : points) {
    xToY[point[0]].push_back(point[1]);  // O(1) 插入
}

// 提取並排序 keys
vector<int> xCoords;
for (auto& [x, _] : xToY) {
    xCoords.push_back(x);
}
sort(xCoords.begin(), xCoords.end());

// 按排序後的順序處理
for (int x : xCoords) {
    auto& yValues = xToY[x];
    sort(yValues.begin(), yValues.end());
    // 處理...
}
```

**特點**：

- 兩階段：grouping (O(n)) + sorting (O(k log k))
- 只在 k << n 時有明顯效能優勢
- 程式碼較複雜

**適用情況**：

- unique keys << 資料點數量（k << n）
- 例如：10000 個點，但只有 100 個 unique x 座標
- 面試官明確要求優化效能

**複雜度分析**：

| 方法                   | 時間複雜度     | 何時較優       |
| ---------------------- | -------------- | -------------- |
| `map`                  | O(n log n)     | k ≈ n（通用）  |
| `unordered_map` + sort | O(n + k log k) | k << n（稀疏） |

**實例**：

- n = 10000, k = 100
  - `map`: ~40000 operations
  - `unordered_map` + sort: ~10200 operations（4x 更快）
- n = 10000, k = 8000
  - 兩者差異不大，`map` 更簡潔

### 面試建議

1. **起手式**：從 `map` 開始
2. **優化時機**：只在以下情況考慮優化
   - 面試官明確詢問效能優化
   - 能清楚解釋 trade-off
   - 題目限制保證 k << n
3. **溝通**：先寫出 `map` 版本，然後說明「如果座標有大量重複，可以用 unordered_map + sort 優化到 O(n + k log k)」

## 適用場景 / Use Cases

- **矩形問題**：固定一邊作為掃描軸，處理其他邊
- **點配對問題**：按一個座標分組點，在另一個座標中找關係
- **幾何關係**：當相同主要位置的點有特殊關係時
- **2D 範圍查詢**：將問題分解為每個主要位置的 1D 查詢

## ⏱️ 複雜度分析

| 操作 | 時間       | 空間 | 備註                       |
| ---- | ---------- | ---- | -------------------------- |
| 分組 | O(n)       | O(n) | 建立 primary→secondary map |
| 掃描 | O(k·m)     | -    | k 個位置，每個位置 m 個值  |
| 總體 | O(n log n) | O(n) | 如需排序則排序為主導因素   |

## ✅ 關鍵要點 / Key Points

- [ ] **明智地選擇主軸** - 通常選擇提供自然排序或具有較少不同值的軸
- [ ] **將所有次要值分組** - 不要逐一處理；先收集，再一起處理
- [ ] **利用排序** - 使用 `map` 進行自動排序掃描，或使用 `unordered_map` + 手動排序
- [ ] **完整處理次要維度** - 在每個主要位置，完全處理所有次要值後再繼續
- [ ] **考慮兩個軸** - 有時交換主要/次要軸可獲得更好的複雜度

**關鍵識別**："位置 X 的所有點" 或 "按一個座標分組" → 考慮 2D Sweep
