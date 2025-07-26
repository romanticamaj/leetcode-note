# 設計模式：滾動狀態 (Design Pattern: Running State)

這是一個在序列處理問題中極為強大的優化模式，其本質是將一個需要兩次遍歷（一次預處理，一次計算）的 O(n) 空間問題，轉化為一次遍歷的 O(1) 或 O(k) 空間解法（k 為狀態種類數）。

此心法通常應用於「前綴和」、「前綴積」等需要依賴歷史累計狀態的問題。

---

## 核心概念

傳統的「前綴和」方法，是先建立一個完整的 `prefix` 陣列，然後再遍歷這個陣列來尋找答案。而「滾動狀態」模式則提出了一個問題：**我們真的需要儲存所有的歷史狀態嗎？**

在很多情況下，答案是否定的。我們需要的，往往只是**在遍歷到某個點 `j` 時，能夠快速查詢到在 `j` 之前，是否存在一個滿足特定關係的歷史狀態 `i`**。

這就催生了「滾動狀態 + 歷史回溯」模式：

- **滾動狀態 (Running State):** 我們不再使用一個 O(n) 的陣列，而是用一個 O(1) 的變數（例如 `running_sum`）來動態計算「截至目前為止」的累計狀態。
- **歷史回溯 (History Lookup):** 我們使用一個高效的查找資料結構（通常是**哈希表**）來儲存我們感興趣的歷史狀態及其出現次數。

通過這種方式，我們將「預處理」和「計算」兩個階段，巧妙地融合到一個單次遍歷的循環中。

---

## 兩大應用模式

### 模式一：利用歷史紀錄 (History-Based)

這是「滾動狀態」最經典的應用，其循環的核心是「**更新狀態 -> 查詢歷史 -> 記錄狀態**」。

- **核心思想：** 在更新當前狀態的同時，利用一個輔助資料結構（通常是 HashMap）來儲存歷史狀態，並透過查詢歷史來找到答案。
- **關鍵設計元素：**

  1. **滾動狀態變數 (`running_state`):** 用於累計當前狀態。
  2. **歷史紀錄容器 (`history`):** 用於儲存歷史狀態及其頻次。
  3. **狀態轉移方程 (`history_state = running_state - k`):** 用於確定要從歷史中查找的目標。
  4. **初始化 (`history[0] = 1`):** 用於處理從序列起點就滿足條件的邊界情況。

- **泛化模板：**

```cpp
#include <vector>
#include <unordered_map>

// T: 陣列元素類型, U: 結果類型
template<typename T, typename U>
U history_based_template(const std::vector<T>& nums, int k) {
    U result = 0; // 或其他初始值
    long long running_state = 0; // 滾動狀態，使用 long long 防溢位

    // 歷史紀錄容器，key 為狀態，value 為該狀態出現次數
    std::unordered_map<long long, int> history;
    history[0] = 1; // 初始化：和為 0 的前綴出現 1 次

    for (const T& num : nums) {
        // 1. 更新當前狀態
        running_state += num;

        // 2. 根據狀態轉移方程，查找歷史紀錄
        long long target_history_state = running_state - k;
        if (history.count(target_history_state)) {
            result += history[target_history_state];
        }

        // 3. 將當前狀態存入歷史紀錄
        history[running_state]++;
    }

    return result;
}
```

### 模式二：條件式重置 (Conditional Reset)

此模式適用於尋找局部最優解的問題，其循環的核心是「**更新狀態 -> 更新全域解 -> 檢查並重置**」。

- **核心思想：** 當前維護的 `running_state` 若對未來的計算不再有益（甚至有害），就果斷將其重置，從而開始一個新的計算區間。
- **關鍵設計元素：**

  1. **滾動狀態變數 (`running_state`):** 用於累計當前「局部」的狀態。
  2. **全域結果變數 (`global_result`):** 用於儲存整個遍歷過程中的最優解。
  3. **重置條件 (`condition_to_reset`):** 這是模式的精髓，決定了何時應該放棄當前的累計，開始新的計算。

- **泛化模板：**

```cpp
#include <vector>
#include <algorithm> // for std::max

// T: 陣列元素類型
template<typename T>
T conditional_reset_template(const std::vector<T>& nums) {
    if (nums.empty()) return 0;

    T global_result = nums[0]; // 全域最優解
    T running_state = nums[0]; // 滾動狀態

    for (size_t i = 1; i < nums.size(); ++i) {
        // 1. 更新當前狀態 (Kadane's Algorithm 範例)
        //    看是要「延續」之前的狀態，還是「從當前元素重新開始」
        running_state = std::max(nums[i], running_state + nums[i]);

        // 2. 用當前狀態更新全域最優解
        global_result = std::max(global_result, running_state);

        // 3. 隱含的重置條件
        //    在 Kadane's Algorithm 中，當 running_state + nums[i] < nums[i] 時，
        //    選擇 nums[i] 本身就相當於對 running_state 進行了重置。
    }

    return global_result;
}
```

---

## 時空複雜度優化分析

- **時間複雜度：**

  - **傳統方法：** O(n) 預處理 + O(n) 計算 = O(n)
  - **優化方法：** 單次 O(n) 遍歷，每次遍歷中的哈希表操作均為 O(1)。總時間複雜度為 **O(n)**。
  - **結論：** 時間複雜度量級不變，但通常能減少一次完整的遍歷，在實踐中可能更快。

- **空間複雜度：**
  - **傳統方法：** O(n) 用於儲存 `prefix` 陣列。
  - **優化方法：** O(1) 用於 `running_state` 變數。哈希表的空間取決於不同狀態的數量，最壞情況下可能也是 O(n)，但通常遠小於 n。這是最核心的優化點。
  - **結論：** 實現了從 **O(n) 到 O(1) 或 O(k) 的空間優化**。
