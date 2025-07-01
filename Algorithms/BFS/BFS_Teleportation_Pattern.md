# BFS 解題模式：處理傳送 (Handling Teleportation)

## 1. 核心概念 (High-Level Concept)

此模式適用於最短路徑問題，其中圖包含兩種邊：

1. **標準邊 (Standard Edges)**: 正常的、可預測的移動到相鄰節點（例如：擲骰子後移動 `+1` 到 `+6`）。
2. **傳送邊 (Teleport Edges)**: 特殊的、無條件的從一個源節點跳轉到一個固定目的地（例如：踩到蛇或梯子）。

核心思想是將這種「落地即跳轉」的行為，在 BFS 遍歷中模型化為一條**重定向的邊 (redirected edge)**。一次移動的目的地不總是緊鄰的下一個方格，而是經過任何潛在傳送後的**最終落點 (final landing spot)**。

## 2. 動機與典型場景 (Motivation & Typical Scenarios)

當你遇到以下情況時，應使用此模式：

- 問題涉及「捷徑 (shortcuts)」或「陷阱 (traps)」，如**蛇與梯子 (Snakes and Ladders)**。
- 某個節點的屬性會將任何進入的路徑重定向到另一個節點。
- 圖中有覆蓋正常移動的即時、非標準轉移規則。

## 3. 核心策略：目的地重定向 (Destination Redirection)

關鍵在於**在將任何移動推入佇列並標記為已訪問之前，確定其真正的目的地**。

1. **計算初始目的地 (Calculate Initial Destination)**: 根據標準規則確定下一個方格（例如：`next = current + dice_roll`）。
2. **檢查傳送 (Check for Teleport)**: 查詢 `next` 方格是否關聯了傳送規則。
3. **確定最終目的地 (Determine Final Destination)**:
   - 如果 `board[next]` 有一個傳送值（例如，不等於 -1），則 `final_destination` 是 `board[next]`。
   - 否則，`final_destination` 就是 `next`。
4. **處理最終目的地 (Process Final Destination)**: BFS 的佇列、`visited` 集合和距離計算，都應該對這個 `final_destination` 進行操作。

### C++ 實作範例

這段邏輯通常放在 BFS 的鄰居探索迴圈內部。

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
    int final_destination = (board[next_label] != -1) ? board[next_label] : next_label;
    // ------------------------------------

    if (!visited[final_destination]) {
        visited[final_destination] = true;
        q.push(final_destination);
    }
}
```

## 4. 關鍵注意事項 (Key Considerations)

- **無條件跳轉 (Unconditional Jump)**: 傳送是強制性的。如果存在蛇或梯子，玩家不能選擇停留在 `next_label`。
- **單次跳轉規則 (Single Jump Rule)**: 如「蛇與梯子」中所述，每次移動只會發生一次傳送。如果 `final_destination` 是另一個傳送的起點，它不會被觸發。上面的邏輯自然地處理了這一點，因為下一次主 BFS 迴圈的迭代將處理從 `final_destination` 出發的移動。
- **對最終目的地進行訪問標記 (Visited on Final Destination)**: 至關重要的是將 `final_destination` 標記為已訪問，而不是中間的 `next_label`。這可以防止冗餘路徑，例如，如果多次擲骰都可能落到一個會傳送到相同目的地的方格上。
