# Sliding Window 進階技巧：Constraint 追蹤與優化

承接 [00-Sliding_Window_Standard_Template.md](00-Sliding_Window_Standard_Template.md)。

基礎模板解決了「窗口怎麼移動」，本文解決更難的另一半：**窗口的合法性要怎麼追蹤與 O(1) 驗證**。

> **核心心法**：Sliding Window 最難的不是指針移動，是 constraint check 的資料結構設計與優化。

---

## Sliding Window 與 Hashmap 結合

Sliding Window 有機會跟 hashmap 結合，用於追蹤窗口內元素的頻率或其他特性，特別適用於需要統計窗口內不同元素出現次數的問題。

### 兩個 Hashmap 設計模式

許多複雜的 sliding window 問題需要兩個 hashmaps：

1. **Target Map (targetMap)** - 記錄目標 constraint（全局需求）
2. **Window Map (windowMap)** - 記錄當前窗口狀態（動態追蹤）

### 實現方式

- Hashmap (e.g., unordered_map) 用於記錄窗口內的 **constraint metric**
- 這個 constraint metric 作為 `while WINDOW_IS_INVALID` 的比較來源
- 當右指針移動時，更新 hashmap 中的頻率計數
- 當窗口無效時，移動左指針並相應地更新 hashmap

### 常見應用場景

- 限制窗口內不同字符的數量
- 限制窗口內元素出現的最大/最小頻率
- 要求窗口內的元素滿足特定的頻率分佈
- 查找包含特定元素集合的最小窗口

## Constraint Check Optimization: Counter Variable Pattern

### 使用時機

當 constraint 是**複合條件**（多個獨立子條件的 AND），例如：

- 窗口必須包含字符串 t 中的所有字符（每個字符及其數量）
- 需要同時滿足 k 個不同的條件

### 問題與優化

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

### 實現模式

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

### 關鍵設計原則

1. **狀態轉換追蹤**：`formed` 只在條件「狀態改變」時更新

   - 增加：`windowMap[c] == targetMap[c]`（剛好達成）
   - 減少：`windowMap[c] == targetMap[c]` 且即將 `--`（即將失去）

2. **使用 `==` 而非 `>=`**：只關注狀態轉換點

3. **複雜度改進**：O(n × k) → O(n)

### 心法總結

- **Constraint 設計是核心**：選對資料結構（hashmap + counter）
- **狀態轉換追蹤**：只在關鍵時刻更新 counter
- **O(1) 驗證**：`formed == required` 替代遍歷 hashmap
- **兩個 Hashmap 模式**：target（需求）vs. window（現狀）

## 相關筆記

- **[00-Sliding_Window_Standard_Template.md](00-Sliding_Window_Standard_Template.md)** — 標準模板、update 時機、Fixed window
- **[02-Sorted_Sliding_Window.md](02-Sorted_Sliding_Window.md)** — 窗口內需維持有序時的變體（Ordered Set）
- **[Frequency_Matching_Counting_Invariant](../../Data_Structures/Hash_Tables/Frequency_Matching_Counting_Invariant.md)** — 頻率匹配的計數不變量
- **[Sliding_Window_Frequency_Matching_Playbook](../../Checklists/Trick%20Practice/Sliding_Window_Frequency_Matching_Playbook.md)** — 專題練習
