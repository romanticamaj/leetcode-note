# BFS 解題模式：頂點映射 (Vertex Mapping)

## 1. 核心概念 (High-Level Concept)

此模式用於解決圖論問題中，節點以複雜、非線性的座標系統（例如：特殊佈局的二維網格）呈現的場景。其核心思想是**將遍歷邏輯與座標的複雜性解耦 (decouple)**，方法是建立一個映射層 (mapping layer)。

我們建立一個雙向的映射關係，讓我們可以在「複雜座標」（如棋盤格子）和「線性整數標籤」（如 1 到 N）之間自由轉換。這使得主要的演算法（如 BFS）可以只對簡單的標籤進行操作，從而使遍歷邏輯保持簡潔和標準化。

## 2. 動機與典型場景 (Motivation & Typical Scenarios)

當你遇到以下情況時，應使用此模式：

- **非標準佈局 (Non-Standard Layouts)**: 問題涉及「牛耕式」(Boustrophedon / zig-zag)、螺旋式 (spiral) 或其他自訂排序的網格。
- **複雜索引 (Complex Indexing)**: 你需要在多維結構（如矩陣）和一維表示之間進行轉換。
- **簡化目標 (Simplification Goal)**: 你希望簡化核心的 BFS 演算法，使其只處理整數節點，並將座標計算分離為預處理步驟或輔助函數。

## 3. 核心策略：映射函數 (The Mapping Function)

此模式的核心是一個（或一對）函數，用於在標籤 (label) 和座標 (coordinates) 之間進行轉換。

`座標 = to_coords(標籤)`

以一個 `n x n` 的棋盤為例，其標籤從 `1` 到 `n*n` 以「牛耕式」風格排列（從左下角開始，每行交替方向），如「蛇與梯子」問題：

1. **標準化標籤 (Normalize Label)**: 將從 1 開始的 `label` 轉換為從 0 開始的索引：`(label - 1)`。
2. **計算從底部開始的行 (Calculate Row from Bottom)**: 從底部計數的行 (`rawRow`) 是 `(label - 1) / n`。
3. **計算列 (Calculate Column)**: 初始的列 (`rawCol`) 是 `(label - 1) % n`。
4. **反轉行為自頂向下的座標 (Invert Row for Top-Down Coords)**: 最終的矩陣行是 `row = n - 1 - rawRow`。
5. **根據交替方向調整列 (Adjust Column for Alternating Direction)**:
   - 如果 `rawRow` 是偶數（如 0, 2, ...），方向是從左到右。`col = rawCol`。
   - 如果 `rawRow` 是奇數（如 1, 3, ...），方向是從右到左。`col = n - 1 - rawCol`。

### C++ 實作範例 (兩種等效寫法)

#### 寫法一：分步解析 (更易讀)

此寫法將邏輯拆解，方便理解每一步的用途。

```cpp
pair<int, int> to_coords_verbose(int label, int n) {
    // 1. 計算從底部開始的 0-indexed 行號
    int rawRow = (label - 1) / n;
    // 2. 計算初始的 0-indexed 列號
    int rawCol = (label - 1) % n;

    // 3. 轉換為棋盤頂部開始的 0-indexed 行號
    int row = n - 1 - rawRow;

    // 4. 根據行號的奇偶性，決定最終列號
    int col = (rawRow % 2 == 0)
              ? rawCol            // 偶數行 (0, 2, ...)，從左到右
              : (n - 1 - rawCol); // 奇數行 (1, 3, ...)，從右到左

    return {row, col};
}
```

#### 寫法二：緊湊實現 (更簡潔)

此寫法將計算合併，程式碼更短，其邏輯與分步解析完全相同。

```cpp
pair<int, int> to_coords_compact(int label, int n) {
    int r = (n - 1) - (label - 1) / n;
    int c = (label - 1) % n;

    // 判斷條件 (n - 1 - r) % 2 等價於 rawRow % 2
    if ((n - 1 - r) % 2 == 1) {
        c = n - 1 - c;
    }
    return {r, c};
}
```

## 4. 在 BFS 中的應用 (Application in BFS)

一旦建立了映射，BFS 就可以只對標籤進行操作：

1. 佇列儲存整數標籤: `queue<int> q;`
2. 訪問過的集合儲存整數標籤: `vector<bool> visited(n*n + 1, false);`
3. 當探索 `curr_label` 的鄰居時，你會得到 `next_label`。
4. 要檢查是否有蛇或梯子，你使用映射函數：`coords = to_coords(next_label, n);`，然後檢查 `board[coords.first][coords.second]`。

這種方法清晰地將「我在棋盤上的哪個位置」的邏輯與「我如何到達那裡」的圖遍歷邏輯分開。
