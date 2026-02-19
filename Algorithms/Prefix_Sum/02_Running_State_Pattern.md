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

## 應用模式

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

此模式有兩個常見變體：

#### 變體 A：隱含式重置（Kadane 型）

重置邏輯隱含在 `max` 運算中：當延續不如重新開始時，自動重置。

- **適用場景：** 最大子陣列和（LC 53）、最佳買賣時機（LC 121）
- **重置語意：** 「延續累積 vs 從當前元素重新開始」，由 `max` 自動決定

```cpp
// 變體 A：隱含式重置
// running_state 透過 max 自動決定「延續」或「重新開始」
for (size_t i = 0; i < nums.size(); ++i) {
    // 1. 更新狀態（重置隱含在 max 中）
    running_state = std::max(nums[i], running_state + nums[i]);

    // 2. 更新全域最優解
    global_result = std::max(global_result, running_state);
}
```

#### 變體 B：顯式重置 + 跳躍剪枝（Feasibility 型）

重置條件是顯式的 `if` 判斷，且重置時**同時跳過一整段候選**，不只是重置累積值。

- **適用場景：** 環形路線可行性（LC 134 Gas Station）、需要找「最佳起點」的問題
- **重置語意：** 「從 `start` 出發在 `i` 處失敗 → `[start, i]` 之間所有起點都不可行 → 直接跳到 `i+1`」
- **額外 invariant：** 通常需要一個 `global_sum` 來判斷整體可行性，與 `running_state` 分工

**跳躍剪枝的正確性論證：**
> 從 `start` 出發到中間任意點 `j`（`start < j <= i`）的累積都 `>= 0`（否則在 `j` 之前就已經觸發重置了）。
> 因此從 `j` 出發，能取得的資源只會**更少**（缺少了 `[start, j-1]` 的正累積），所以 `j` 也不可能是可行起點。

```cpp
// 變體 B：顯式重置 + 跳躍剪枝
// 同時維護 global_state（整體可行性）和 running_state（局部累積）
int global_state = 0;   // 整體可行性判斷
int running_state = 0;  // 當前候選起點的累積狀態
int candidate = 0;      // 當前候選起點

for (int i = 0; i < n; ++i) {
    int delta = compute_delta(i);  // 每步的淨增減量

    global_state += delta;   // 全域累積，不重置
    running_state += delta;  // 局部累積，可能重置

    if (running_state < 0) {       // 顯式重置條件
        candidate = i + 1;         // 跳躍剪枝：跳過 [candidate, i] 整段
        running_state = 0;         // 重置局部累積
    }
}

// global_state >= 0 → 可行，回傳 candidate
// global_state <  0 → 整體不可行
```

**兩個變體的對比：**

| 面向 | 變體 A（隱含式） | 變體 B（顯式 + 跳躍） |
|------|-----------------|----------------------|
| 重置機制 | `max` 自動選擇 | 顯式 `if` 判斷 |
| 重置時做什麼 | 只重置累積值 | 重置累積值 **+ 跳過候選** |
| 全域判斷 | 全域結果在 loop 中隨時更新 | 通常需要獨立的 `global_state` |
| 典型問題 | LC 53, LC 121 | LC 134 Gas Station |
| 關鍵 insight | 負累積不值得延續 | 失敗區間內的所有起點都不可行 |

### 模式三：自定義累計運算 (Custom Accumulation Operation)

此模式是 Running Sum 的泛化：**核心不在於容器類型，而在於「如何更新累計值」的運算定義**。

- **本質認知：**
  - Running Sum 本質：`result = update_operation(result, current)`
  - 傳統加法累計：`result += current`
  - 數字解析累計：`result = result * 10 + digit`
  - 重點是**運算本身**，而非輸入容器（可以是數字陣列、字符串、甚至任意序列）

- **核心思想：** 邊遍歷邊用自定義運算更新結果，避免兩階段處理（先收集再轉換）。

- **關鍵設計元素：**

  1. **滾動累計變數 (`running_result`):** 存儲當前累計結果
  2. **更新運算 (`update_op`):** 定義如何用當前元素更新累計值
  3. **容器遍歷 (`iterate`):** 可以是任意可遍歷的序列

- **運算對比：**

| 應用場景 | 更新運算 | 說明 |
|---------|---------|------|
| 前綴和 | `result += num` | 標準加法累計 |
| 前綴積 | `result *= num` | 乘法累計 |
| 十進制數字解析 | `result = result * 10 + digit` | 位權累加（每次左移一位） |
| 二進制數字解析 | `result = result * 2 + bit` | 二進制位權累加 |
| 十六進制解析 | `result = result * 16 + hex_digit` | 十六進制位權累加 |

- **字串轉數字範例：**

```cpp
// 從字串容器提取數字到整數輸出
int parseDigits(const std::string& str, int& pos) {
    int result = 0;  // 累計結果
    
    while (pos < str.size() && isdigit(str[pos])) {
        // 更新運算：位權累加
        result = result * 10 + (str[pos] - '0');
        pos++;
    }
    
    return result;
}
```

- **對比傳統兩階段處理：**

```cpp
// ❌ 兩階段：先提取字串，再轉換
int digitEnd = j;
while (digitEnd < k && isdigit(abbr[digitEnd])) digitEnd++;
int num = std::stoi(abbr.substr(j, digitEnd - j));  // 階段1: 提取, 階段2: 轉換
j = digitEnd;

// ✅ 單階段：邊遍歷邊用運算更新
int num = 0;
while (j < k && isdigit(abbr[j])) {
    num = num * 10 + (abbr[j] - '0');  // 直接用運算更新累計值
    j++;
}
```

- **優勢：**
  - **概念統一：** 將各種累計問題統一到「定義更新運算」的框架
  - **避免中間步驟：** 不需要先收集再處理
  - **性能提升：** 避免 `substr()` 的記憶體分配和 `stoi()` 的解析開銷

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
