# Sliding Window 技巧

## 核心心法

> **Sliding Window 最難的是 constraint check 的資料結構設計與優化**

成功運用 Sliding Window 的關鍵在於：

1. **識別 constraint metric** - 窗口需要滿足什麼條件？
2. **設計狀態追蹤** - 用什麼資料結構追蹤窗口狀態？
3. **優化驗證邏輯** - 如何 O(1) 判斷窗口是否有效？

## 要點

1. **window** 表示 subarray
2. 維持兩個 index - **left** and **right**
3. **right** 會增加，讓 window 變大; **left** 會增加，讓 window 變小
4. sliding window 長度是 **`right - left + 1`**
5. 因為 **right** 會不斷的增加，所以 window 會 **slide**
6. **constraint metric** 會決定要做什麼 window 的"特性"判斷, 例如 sum, 出現的數字個數等等
7. 通常問題會給一個 array，去找到滿足 **contraint metric** 某個特性的 subarray

## 通用模板

```
function fn(arr):
    for (int left, int right = 0; right < arr.length; right++):
        Do some logic to "add" element at arr[right] to window

        while WINDOW_IS_INVALID:
            Do some logic to "remove" element at arr[left] from window
            left++

        Do some logic to update the answer
```

## 特定類型

### Fixed window size

- 在右側添加一個元素，同時在左側移除一個元素以維持窗口長度不變。

**小訣竅**：

- 當添加位置 i 的元素時，被移除的元素一定在 `i-k` 位置（k 是窗口大小）
- 這樣就可以省略顯式追蹤 left 的 index

## Update 時機的統一框架

```cpp
for (right...) {
    expand window

    while (invalid) {
        // Fix 階段
        // 求最小窗口：在有效時 update（嘗試縮小）
        if (valid before shrinking) update_min_answer();
        shrink left
    }

    // 求最大窗口：fix 後 update（窗口此時有效且盡量大）
    update_max_answer();
}
```

**判斷規則**：

- **求最大窗口**：fix 後 update（窗口有效且最大化）
- **求最小窗口**：fix 中 update（找到有效窗口後嘗試縮小）

## 進階技巧

### Sliding Window 與 Hashmap 結合

Sliding Window 有機會跟 hashmap 結合，用於追蹤窗口內元素的頻率或其他特性，特別適用於需要統計窗口內不同元素出現次數的問題。

#### 兩個 Hashmap 設計模式

許多複雜的 sliding window 問題需要兩個 hashmaps：

1. **Target Map (targetMap)** - 記錄目標 constraint（全局需求）
2. **Window Map (windowMap)** - 記錄當前窗口狀態（動態追蹤）

#### 實現方式

- Hashmap (e.g., unordered_map) 用於記錄窗口內的 **constraint metric**
- 這個 constraint metric 作為 `while WINDOW_IS_INVALID` 的比較來源
- 當右指針移動時，更新 hashmap 中的頻率計數
- 當窗口無效時，移動左指針並相應地更新 hashmap

#### 常見應用場景

- 限制窗口內不同字符的數量
- 限制窗口內元素出現的最大/最小頻率
- 要求窗口內的元素滿足特定的頻率分佈
- 查找包含特定元素集合的最小窗口

### Constraint Check Optimization: Counter Variable Pattern

#### 使用時機

當 constraint 是**複合條件**（多個獨立子條件的 AND），例如：

- 窗口必須包含字符串 t 中的所有字符（每個字符及其數量）
- 需要同時滿足 k 個不同的條件

#### 問題與優化

**❌ Naive Approach: O(k) per check**

```cpp
bool isValid() {
    for (auto& [ch, count] : targetMap) {
        if (windowMap[ch] < count) return false;
    }
    return true;
}
// 在 sliding window 循環中調用 → O(n × k)
```

**✅ Optimized: Counter Variable → O(1) per check**

引入計數變量追蹤「已滿足的獨立條件數量」，將驗證從 O(k) 降為 O(1)。

#### 實現模式

```cpp
// Setup (在 sliding window 前)
unordered_map<char, int> targetMap;  // 目標 constraint
unordered_map<char, int> windowMap;  // 當前窗口狀態
int required = targetMap.size();     // 需要滿足的獨立條件總數
int formed = 0;                      // 已滿足的條件數

// During sliding window
for (int left = 0, right = 0; right < s.size(); right++) {
    char c = s[right];

    // Expand: 更新窗口狀態
    windowMap[c]++;

    // 關鍵：只在狀態轉換時更新 formed
    // 從「不滿足」→「剛好滿足」
    if (targetMap.count(c) && windowMap[c] == targetMap[c]) {
        formed++;
    }

    // O(1) validity check
    while (formed == required) {
        // 窗口有效，執行相應邏輯
        update_answer();

        // Shrink: 收縮窗口
        char leftChar = s[left];

        // 關鍵：只在狀態轉換時更新 formed
        // 從「滿足」→「即將不滿足」
        if (targetMap.count(leftChar) &&
            windowMap[leftChar] == targetMap[leftChar]) {
            formed--;
        }
        windowMap[leftChar]--;
        left++;
    }
}
```

#### 關鍵設計原則

1. **狀態轉換追蹤**：`formed` 只在條件「狀態改變」時更新

   - 增加：`windowMap[c] == targetMap[c]`（剛好達成）
   - 減少：`windowMap[c] == targetMap[c]` 且即將 `--`（即將失去）

2. **使用 `==` 而非 `>=`**：只關注狀態轉換點

3. **複雜度改進**：O(n × k) → O(n)

#### 心法總結

- **Constraint 設計是核心**：選對資料結構（hashmap + counter）
- **狀態轉換追蹤**：只在關鍵時刻更新 counter
- **O(1) 驗證**：`formed == required` 替代遍歷 hashmap
- **兩個 Hashmap 模式**：target（需求）vs. window（現狀）
