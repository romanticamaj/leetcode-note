# 統一心法：迭代遍歷的多重視角

## 核心洞見：迭代即是手動執行的狀態機

所有遞迴演算法的迭代化，本質上都是在手動模擬一個**狀態機 (State Machine)**。遞迴的美妙之處在於它隱藏了狀態管理的複雜性，而迭代則將其明確化。這個狀態機由三個核心元素構成：

1. **當前狀態 (Current State)**：通常由一個變數（如 `current` 指標）表示，代表當前需要處理的工作單元。
2. **待辦清單 (Pending Tasks)**：通常由一個堆疊 (`stack`) 表示，儲存了所有被暫停的父任務，等待我們回頭處理。
3. **狀態轉換邏輯 (State Transition Logic)**：定義了如何在 `current` 和 `stack` 之間移動，精確模擬遞迴的兩個核心動作：
   - **向下走訪 (Descending)**：從當前狀態移動到一個子狀態（例如 `current = current->left`）。
   - **向上返回 (Ascending)**：當一個分支探索完畢，從待辦清單中取出父任務以繼續執行（例如 `current = stack.top(); stack.pop()`）。

---

## 視角一：時序模式（何時處理）

### 迭代狀態機的生命週期與時序模式

一個典型的迭代循環包含以下幾個關鍵的「時間點」，對應著狀態的轉換：

```cpp
while (current || !stack.empty()) {
    if (current) {
        // --- 時間點 A: 執行「向下走訪」之前 ---
        stack.push(current);
        current = current->left; // 狀態轉換：向下走訪
    } else {
        // --- 時間點 B: 執行「向上返回」之後 ---
        current = stack.top();
        stack.pop();
        // --- 時間點 C: 準備下一次走訪之前 ---
        current = current->right; // 狀態轉換：向下走訪（到另一個分支）
    }
}
```

**時序模式決定了「處理」這個動作應該在狀態機的哪個轉換點被觸發：**

| 模式          | 時間點   | 資訊流    | 本質                   |
| ------------- | -------- | --------- | ---------------------- |
| **Preorder**  | A        | Top-Down  | 探索前處理             |
| **Inorder**   | B/C 之間 | Linear    | 左探索後，右探索前處理 |
| **Postorder** | C 之後   | Bottom-Up | 所有子問題完成後處理   |

---

## 視角二：Visit Nature（訪問幾次）

### 每個節點需要幾次訪問？

從**訪問次數**的角度思考，可以更直觀地理解三種遍歷：

| Traversal     | Visit Count | 1st Visit                    | 2nd Visit            |
| ------------- | ----------- | ---------------------------- | -------------------- |
| **Preorder**  | **1 次**    | Process + push children      | N/A                  |
| **Inorder**   | **2 次**    | Push self + go left          | Process + go right   |
| **Postorder** | **2 次**    | Push self + explore children | Process with results |

**核心洞察**：

- **Preorder = 見面即處理**（1-pass）：訪問時立即處理，不需要回訪
- **Inorder/Postorder = 需要回訪**（2-pass）：第一次訪問準備工作，第二次訪問才處理

### 狀態追蹤的兩種實作方式

**方式 1：顯式狀態標記**

```cpp
stack<pair<TreeNode*, bool>> stk;  // (node, isFirstVisit)

while (!stk.empty()) {
    auto [node, first] = stk.top(); stk.pop();
    if (!node) continue;

    if (first) {
        // 第一次訪問：準備子節點
        stk.push({node, false});        // 標記第二次訪問
        stk.push({node->right, true});
        stk.push({node->left, true});
    } else {
        // 第二次訪問：處理節點
        process(node);
    }
}
```

**方式 2：隱式狀態（current pointer + lastVisited）**

```cpp
stack<TreeNode*> stk;
TreeNode *curr = root, *lastVisited = nullptr;

while (curr || !stk.empty()) {
    // curr 指標的狀態 + lastVisited 隱式追蹤訪問次數
}
```

---

## 兩種視角的對應關係

| 視角             | Preorder | Inorder    | Postorder              |
| ---------------- | -------- | ---------- | ---------------------- |
| **時序模式**     | 時間點 A | 時間點 B/C | 時間點 C 之後          |
| **Visit Nature** | 1 次訪問 | 2 次訪問   | 2 次訪問               |
| **處理時機**     | 向下前   | 左完右前   | 全部完成               |
| **狀態需求**     | 簡單     | 中等       | 複雜（需 lastVisited） |

**統一理解**：

- **時序模式**強調「何時」：在狀態機的哪個時間點處理
- **Visit Nature**強調「幾次」：需要訪問節點幾次才能處理
- 兩者本質相同，只是思考角度不同

---

## 統一心法：從概念到實作

### Step 1: 識別資訊流向 → 確定模式

- 需要將父層級的資訊**向下傳遞**？ → **Preorder**（1 次訪問，時間點 A）
- 需要在兩個探索方向之間處理？ → **Inorder**（2 次訪問，時間點 B/C）
- 需要將子層級的結果**向上整合**？ → **Postorder**（2 次訪問，時間點 C 後）

### Step 2: 選擇實作策略

**選擇依據**：

| 考量         | State Flag   | Current Pointer   |
| ------------ | ------------ | ----------------- |
| **可讀性**   | ★★★ 明確     | ★★ 需理解隱式狀態 |
| **效率**     | ★★ 額外 bool | ★★★ 更緊湊        |

### Step 3: 建立狀態機框架

```cpp
// 基本框架（current pointer 版本）
while (current || !stack.empty()) {
    if (current) {
        // 向下走訪邏輯
    } else {
        // 向上返回邏輯
    }
}
```

### Step 4: 在正確位置插入處理邏輯

根據選定的模式（時序/訪問次數），將 `process()` 插入對應位置。

---

## ✅ 核心要點總結

- [ ] **狀態機三要素**：current state + pending tasks + transition logic
- [ ] **兩種思考視角**：時序模式（何時）vs Visit Nature（幾次）
- [ ] **Preorder 特殊性**：唯一的 1 次訪問，最簡單
- [ ] **Inorder/Postorder 共性**：都需要 2 次訪問，區別在處理時機
- [ ] **實作選擇權衡**：State Flag（明確）vs Implicit State（高效）
- [ ] **詳細實作參考**：
  - Visit Nature 快速表：`02-Visit_Nature_Quick_Reference.md`
  - Current Pointer 實作：`03-Current_Pointer_Implementations.md`
  - Postorder 深入：`04-Postorder_lastVisited_Deep_Dive.md`
