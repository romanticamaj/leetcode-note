# 統一心法：從時序模式看遞迴與迭代的轉換

## 核心洞見：迭代即是手動執行的狀態機

所有遞迴演算法的迭代化，本質上都是在手動模擬一個**狀態機 (State Machine)**。遞迴的美妙之處在於它隱藏了狀態管理的複雜性，而迭代則將其明確化。這個狀態機由三個核心元素構成：

1. **當前狀態 (Current State)**：通常由一個變數（如 `current` 指標）表示，代表當前需要處理的工作單元。
2. **待辦清單 (Pending Tasks)**：通常由一個堆疊 (`stack`) 表示，儲存了所有被暫停的父任務，等待我們回頭處理。
3. **狀態轉換邏輯 (State Transition Logic)**：定義了如何在 `current` 和 `stack` 之間移動，精確模擬遞迴的兩個核心動作：
   - **向下走訪 (Descending)**：從當前狀態移動到一個子狀態（例如 `current = current->left`）。
   - **向上返回 (Ascending)**：當一個分支探索完畢，從待辦清單中取出父任務以繼續執行（例如 `current = stack.top(); stack.pop()`）。

當我們將「時序模式」的概念融入這個狀態機時，就能得到一個強大且通用的思考框架。**時序模式決定了「處理」這個動作，應該在狀態機的哪個轉換點被觸發。**

---

## 迭代狀態機的生命週期與時序模式

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

現在，我們可以將三種時序模式精確地對應到這些時間點：

### 1. 前序處理 (Pre-order): 在「向下走訪」之前處理

- **資訊流**: 自頂向下 (Top-Down)。
- **本質**: 在深入探索子問題**之前**，就對當前狀態進行處理。
- **觸發點**: 時間點 A。
- **迭代實現**:
  ```cpp
  if (current) {
      process(current); // <--- 在此處理
      stack.push(current);
      current = current->left;
  }
  ```

### 2. 中序處理 (In-order): 在一次「向上返回」後，下一次「向下走訪」前處理

- **資訊流**: 線性有序 (Linearly Ordered)。
- **本質**: 在一個方向（左）的探索完畢並「向上返回」後，處理當前狀態，然後再開始另一個方向（右）的探索。
- **觸發點**: 時間點 B 與 C 之間。
- **迭代實現**:
  ```cpp
  else { // current is null
      current = stack.top();
      stack.pop();
      process(current); // <--- 在此處理
      current = current->right;
  }
  ```

### 3. 後序處理 (Post-order): 在所有「向下走訪」完成，「向上返回」時處理

- **資訊流**: 自底向上 (Bottom-Up)。
- **本質**: 必須在所有子問題（左、右）都探索完畢**之後**，才能在最終「向上返回」的時刻整合並處理當前狀態。
- **觸發點**: 需要額外狀態 (`lastVisited`) 來判斷是否所有子路徑都已返回。
- **迭代實現**:

  ```cpp
  else { // current is null
      TreeNode* peekNode = stack.top();
      if (peekNode->right && peekNode->right != lastVisited) {
          current = peekNode->right; // 轉向右側，開始新的向下走訪
      } else {
          // 所有子路徑均已返回，可以處理
          process(peekNode); // <--- 在此處理
          stack.pop();

          // 讓右子樹不被重複拜訪以便讓 current 可以確認自己是否要被處理
          lastVisited = peekNode;

          // 關鍵：強制下一次循環繼續向上返回
          current = nullptr;
      }
  }
  ```

---

## 統一心法：三步驟轉換

1. **識別資訊流向 -> 確定時序模式**:

   - 需要將父層級的資訊**向下傳遞**？ -> **前序 (Pre-order)**
   - 需要將子層級的結果**向上整合**？ -> **後序 (Post-order)**
   - 需要在兩個探索方向之間處理？ -> **中序 (In-order)**

2. **建立迭代狀態機框架**:

   - 定義 `current` 和 `stack`。
   - 寫出 `while (current || !stack.empty())` 主循環。
   - 寫出 `if (current)` 和 `else` 的基本結構，分別對應「向下走訪」和「向上返回」的邏輯。

3. **在正確的時間點插入 `process()`**:
   - 根據判斷出的時序模式，將核心處理邏輯 `process()` 插入到對應的時間點 A、B/C 或 C 之後。

這個統一模型提供了一個從問題本質出發，系統性地構建迭代解法的強大心法。
