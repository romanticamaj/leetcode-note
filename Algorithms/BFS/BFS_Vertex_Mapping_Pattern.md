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

---

## 5. 延伸模式：處理隱含邊與傳送 (Extended Pattern: Handling Implicit Edges & Teleportation)

頂點映射模式為我們提供了一套處理複雜座標的強大工具。然而，有時圖的複雜性不僅在於節點的佈局，還在於**邊的規則**。除了標準的相鄰移動外，圖中可能存在特殊的「傳送邊」，例如「蛇與梯子」遊戲中的捷徑或陷阱。

這種「落地即跳轉」的行為，可以視為頂點映射模式的一種自然延伸。核心思想是在 BFS 遍歷中，將這種跳轉模型化為一條**重定向的邊 (redirected edge)**。

### 核心策略：目的地重定向 (Destination Redirection)

關鍵在於**在將任何移動推入佇列並標記為已訪問之前，確定其真正的最終目的地 (final landing spot)**。

1. **計算初始目的地標籤 (Calculate Initial Destination Label)**: 根據標準規則確定下一個節點的標籤（例如：`next_label = current_label + dice_roll`）。
2. **檢查傳送規則 (Check for Teleport Rule)**: 查詢 `next_label` 是否有關聯的傳送規則。這通常需要一個額外的資料結構（如 `map` 或 `vector`）來儲存這些規則。
3. **確定最終目的地 (Determine Final Destination)**:
   - 如果 `board[next_label]` 有一個傳送值（例如，不等於 -1），則 `final_destination` 是 `board[next_label]`。
   - 否則，`final_destination` 就是 `next_label`。
4. **處理最終目的地 (Process Final Destination)**: BFS 的佇列、`visited` 集合和距離計算，都應該對這個 `final_destination` 進行操作，而不是中間的 `next_label`。

### C++ 實作範例

這段邏輯通常放在 BFS 的鄰居探索迴圈內部，緊跟在計算出 `next_label` 之後。

```cpp
// 假設 'board' 是一個扁平化的一維陣列，代表蛇與梯子
// board[i] = -1 表示沒有蛇或梯子，否則其值為目的地標籤。

queue<int> q;
vector<bool> visited;
// ... BFS 設定 ...

int current_label = q.front();
q.pop();

for (int i = 1; i <= 6; ++i) { // 模擬一個六面骰
    int next_label = current_label + i;
    if (next_label > n * n) break;

    // --- 傳送邏輯 (Teleportation Logic) ---
    // 在處理前，先確定最終落點
    int final_destination = (board[next_label] != -1) ? board[next_label] : next_label;
    // ------------------------------------

    if (!visited[final_destination]) {
        visited[final_destination] = true;
        q.push(final_destination);
    }
}
```

### 整合觀點

「傳送模式」完美地展示了「頂點映射」的威力。我們首先使用映射函數將複雜的二維座標簡化為一維的 `label`，然後在處理這些 `label` 時，再應用「目的地重定向」邏輯來處理圖中隱含的特殊邊。這使得整個程式碼結構保持高度的模組化和清晰度。
