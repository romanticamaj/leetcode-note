# 心法：Running Sum vs. Prefix Sum

## tl;dr: Running Sum 的核心心法

**Running Sum** 是一種在單次遍歷中「邊建構，邊操作」的強大技巧。

傳統方法可能是「先建構一個資料結構（如 Prefix Sum 陣列），再遍歷一次進行操作」。而 Running Sum 將這兩步合併，在更新當前狀態（`running_state`）的同時，立即用它來進行計算或比較。

---

## Running Sum 的兩大應用模式

**Running Sum** 的核心是在遍歷過程中**動態維護**一個或多個狀態變數。根據問題的不同，我們可以將其應用歸納為兩種主要模式：

### 模式一：利用歷史紀錄 (History-Based)

**核心思想**：在更新當前狀態的同時，利用一個輔助資料結構（通常是 HashMap）來儲存歷史狀態，並透過查詢歷史來找到答案。

**模板**：利用 `running_state` 與 `history` 達成「邊走邊看」。

```cpp
// 初始化結果、當前狀態和歷史紀錄
result = ...
running_state = ...
history = ... // e.g., a hash map

for (element : data) {
    // 1. 更新當前狀態
    update(running_state, element);

    // 2. 利用當前狀態和歷史紀錄，檢查是否滿足條件
    if (check_condition(running_state, history)) {
        update(result);
    }

    // 3. 將當前狀態存入歷史紀錄
    update(history, running_state);
}

return result;
```

這個模式的核心是「**更新狀態 -> 檢查條件 -> 記錄狀態**」的循環，在一次遍歷中完成所有操作。

### 模式二：條件式重置 (Conditional Reset)

**核心思想**：當前維護的 `running_state` 若對未來的計算不再有益（甚至有害），就果斷將其重置，從而開始一個新的計算區間。這常用於尋找局部最優解。

**模板**：根據條件重置 `running_state`，以尋找局部最優解。

```cpp
// 初始化全域最優解和當前狀態
global_result = ...
running_state = ...

for (element : data) {
    // 1. 更新當前狀態
    update(running_state, element);

    // 2. 用當前狀態更新全域最優解
    update(global_result, running_state);

    // 3. 檢查是否需要重置當前狀態
    if (condition_to_reset(running_state)) {
        reset(running_state);
    }
}

return global_result;
```

這個模式的精髓在於 `condition_to_reset`，它的核心是「**更新狀態 -> 更新全域解 -> 檢查並重置**」的循環。

## 觀念比較：Running Sum vs. Prefix Sum

為了更清晰地理解 Running Sum 的價值，以下是它與傳統 Prefix Sum 的詳細比較：

| 特性           | Prefix Sum (前綴和)                                                                                                | Running Sum (動態和)                                                                                 |
| :------------- | :----------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| **核心思想**   | **預處理 & 儲存**                                                                                                  | **動態計算 & 即時使用**                                                                              |
| **空間複雜度** | `O(N)`，需要一個額外陣列儲存所有前綴和。                                                                           | `O(1)` (若不計額外資料結構如 HashMap)，通常只需要一個變數。                                          |
| **操作模式**   | 1. **建構**：先完整遍歷一次，建構 `prefix_sum` 陣列。<br>2. **查詢**：之後可以 `O(1)` 查詢任意 `[i, j]` 區間的和。 | **邊建構，邊操作**：在單次遍歷中同時更新 `running_sum` 並進行計算。                                  |
| **適用場景**   | - 需要**多次**查詢不同區間和。<br>- 問題需要回溯或訪問非連續的前綴和。                                             | - 只需要**單次遍歷**即可解決問題。<br>- 關注點是 "截至目前為止" 的狀態。<br>- 空間複雜度有嚴格限制。 |
| **靈活性**     | 較低。一旦建構，`prefix_sum` 陣列是固定的。                                                                        | 較高。可以根據條件**重置** `running_sum`，使其適用於尋找局部最優解 (如 Kadane's Algorithm)。         |

---
