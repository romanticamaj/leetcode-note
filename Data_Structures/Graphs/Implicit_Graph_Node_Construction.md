# 心法：隱性圖的節點建構 (Node Construction in Implicit Graphs)

## 🧠 核心思想：從「位置」到「狀態」

在許多圖論問題中，圖是明確給出的（explicit graph），節點就是題目給的 `0, 1, ..., n-1`。然而，在更複雜的問題中，圖是**隱性**的（implicit graph），我們搜尋的對象不再是單純的位置，而是一個**狀態 (State)**。

**節點建構**的核心，就是找出如何定義這個「狀態」，從而將問題轉化為我們熟悉的圖搜尋問題。

> **The Art of Node Construction**: Identifying the minimal set of information that uniquely defines a point in the problem's state space and determines all future valid moves.

---

## ✅ 如何觀察與建構節點？提問法

當你覺得一個圖問題無法用簡單的 `visited[node]` 來解決時，問自己以下幾個關鍵問題：

1. **「到達同一個『物理位置』，但條件不同，會影響我的未來嗎？」**
   - **Yes**: 如果答案為是，那麼這些「條件」就必須成為節點定義的一部分。
   - **No**: 如果答案為否，那麼節點可能就是單純的物理位置。

2. **「為了做出下一步的『合法』決策，我必須攜帶哪些資訊？」**
   - 這個問題會直接揭示狀態的組成部分。你需要的每一樣資訊，都是狀態的一個維度。

3. **「問題的『約束』是什麼？」**
   - 約束條件（constraints）往往是狀態的來源。有限的資源、特定的序列要求、必須滿足的條件等，都應該被模型化為狀態的一部分。

---

## 案例分析：LeetCode 1129. "Shortest Path with Alternating Colors"

讓我們用這套提問法來解構這題的節點建構過程：

### 1. 初步思考

- **物理位置**: 節點 `0` 到 `n-1`。
- **直覺節點定義**: `node_id`。

### 2. 提問與挑戰

- **提問**: 「我到達節點 `u`，是從紅邊來的，跟從藍邊來的，會影響我的未來嗎？」
- **回答**: **會！**

  - 如果我是從**紅邊**到達 `u`，下一步我**只能**走藍邊。
  - 如果我是從**藍邊**到達 `u`，下一步我**只能**走紅邊。

- **結論**: 「上一步的顏色」這個條件，直接影響了未來的合法移動。因此，它必須被納入節點的定義中。

### 3. 重新建構節點

- **物理位置**: `node_id`
- **必要條件**: `incoming_edge_color`

- **最終節點定義 (State)**: `(node_id, incoming_edge_color)`

一旦這個新的節點定義確立，整個問題就豁然開朗：

- **圖的節點**: 不再是 `n` 個，而是最多 `n * 2` 個狀態。
- **`visited` 陣列**: 自然而然地變成了 `visited[n][2]`，用來標記 `(node, color)` 這個狀態是否被訪問過。
- **BFS 佇列**: 儲存的不再是 `node_id`，而是 `pair<int, int>` 或 `struct State`，代表 `(node, color)`。

---

## 🪜 通用節點建構框架

1. **識別物理位置 (Identify Physical Location)**:

   - 這是最基本的狀態維度。通常是圖中的節點 ID、Grid 中的 `(r, c)` 座標，或是 Puzzle 中的盤面。

2. **識別約束與條件 (Identify Constraints & Conditions)**:

   - 列出所有會影響「移動合法性」或「成本」的變數。
   - 例如：剩餘資源 (`k`)、已收集的物品 (`mask`)、上一步的方向或顏色。

3. **組合狀態 (Combine into a State)**:

   - `State = (Physical Location, Condition1, Condition2, ...)`
   - 這個 `State` 就是你在隱性圖中真正要遍歷的「節點」。

4. **驗證最小完備性 (Verify Minimality & Completeness)**:
   - **完備性**: 這個 `State` 是否包含了做出所有未來決策所需的**全部**資訊？
   - **最小性**: 能否移除 `State` 中的任何一個維度，而仍然能做出正確決策？如果不行，那它就是最小的。

這個框架能幫助你系統性地將複雜的約束問題，轉化為清晰的圖搜尋問題。
