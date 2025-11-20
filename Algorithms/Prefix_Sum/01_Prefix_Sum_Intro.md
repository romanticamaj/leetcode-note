# 演算法技巧：前綴和 (Prefix Sum)

**前綴和**是一種強大的預處理 (Preprocessing) 技巧，其核心思想是將一個序列的「區間和查詢」問題，轉化為兩次「單點查詢」的差值計算。

透過預先計算並儲存從序列起點到每個位置的累計和，我們可以在 O(1) 的時間複雜度內，快速獲取任意子區間的和，從而極大地優化演算法的整體效率。

---

## 核心概念與公式

- **定義:** 對於一個陣列 `nums`，其前綴和陣列 `prefix` 的定義是 `prefix[i] = nums[0] + ... + nums[i]`。
- **區間和公式:** 計算 `nums` 中從索引 `i` 到 `j` (包含 `i` 和 `j`) 的子陣列之和，公式為：
  `sum(i, j) = prefix[j] - prefix[i-1]`
- **效率:**
  - **預處理時間:** O(n)
  - **單次查詢時間:** O(1)

---

## 前綴和的兩種建構方式

### 方式一：索引對齊 (Index-Aligned)

前綴和陣列 `prefix` 的索引與原陣列 `nums` 完全對應。

- **建構:** `prefix[i] = prefix[i-1] + nums[i]`，其中 `prefix[0] = nums[0]`。
- **查詢 `sum(i, j)`:**
  - `prefix[j] - prefix[i-1]` (當 `i > 0`)
  - `prefix[j]` (當 `i = 0`)
- **優點:** 索引直觀，易於理解。
- **缺點:** 查詢時需要對 `i=0` 的情況做邊界處理。

```cpp
// 方式一：prefix[0] = nums[0]
vector<int> prefix(nums.size());
prefix[0] = nums[0];
for (int i = 1; i < nums.size(); i++) {
    prefix[i] = prefix[i-1] + nums[i];
}
```

### 方式二：哨兵節點 (Sentinel Node)

前綴和陣列 `prefix` 的長度比原陣列 `nums` 多一，並在開頭設置一個 `prefix[0] = 0` 的「哨兵」節點。

- **建構:** `prefix[i+1] = prefix[i] + nums[i]`。
- **查詢 `sum(i, j)`:**
  - `prefix[j+1] - prefix[i]` (統一公式)
- **優點:** 查詢公式統一，無需邊界判斷，代碼更簡潔。
- **缺點:** `nums[i]` 對應 `prefix[i+1]`，索引有 1 的偏移。

```cpp
// 方式二：prefix[0] = 0
vector<int> prefix(nums.size() + 1, 0);
for (int i = 0; i < nums.size(); i++) {
    prefix[i + 1] = prefix[i] + nums[i];
}
```

> **實戰建議:** 方式二（哨兵節點）是競賽和面試中的首選，因為它能有效簡化代碼，減少因邊界處理而出錯的機率。

## 常見陷阱與注意事項

### ⚠️ Integer Overflow 風險

前綴和計算中最常見的陷阱是**累計溢位 (Cumulative Overflow)**：

- **問題**: 即使原陣列的每個元素都在 `int` 範圍內（≤ `2×10⁹`），但累加後的總和可能超過 `INT_MAX`
- **心法**: **「容器要夠大」** - 前綴和陣列必須使用能容納最終結果的資料型別

**錯誤範例：**

```cpp
vector<int> nums = {1000000000, 1000000000}; // 每個元素都在 int 範圍內
vector<int> prefix(nums.size() + 1, 0);      // ❌ prefix 用 int
for (int i = 0; i < nums.size(); i++) {
    prefix[i + 1] = prefix[i] + nums[i];     // 溢位！
}
```

**正確做法：**

```cpp
vector<int> nums = {1000000000, 1000000000};
vector<long long> prefix(nums.size() + 1, 0); // ✅ 使用 long long
for (int i = 0; i < nums.size(); i++) {
    prefix[i + 1] = prefix[i] + nums[i];
}
```

**判斷原則：**

- 如果 `n × max(nums[i])` 可能 > `2×10⁹`，必須使用 `long long`
- 例如：`n = 10⁵`, `max(nums) = 10⁴` → 總和 ≤ `10⁹` → `int` 安全
- 例如：`n = 10⁵`, `max(nums) = 10⁵` → 總和 ≤ `10¹⁰` → 需要 `long long`

> 📖 延伸閱讀：[`Arithmetic_Overflow_Prevention_Playbook.md`](../Math/Arithmetic_Overflow_Prevention_Playbook.md:1)

---

---

## 優化技巧：從「前綴和」到「滾動和」

### Running Sum: 邊遍歷，邊計算

在許多問題中，我們並不需要儲存**所有**的前綴和。如果問題的目標只依賴於**當前的前綴和**與**歷史前綴和**之間的關係（例如，在哈希表中查找 `current_sum - target`），那麼我們就沒有必要為了 O(1) 的查詢效率而犧牲 O(n) 的空間。

這時，我們可以將「預處理」和「計算」兩個階段合二為一。我們只用一個變數來維護**滾動和 (Running Sum)**，在遍歷原陣列的過程中，動態計算當前的前綴和，並立即用它來進行判斷或更新結果。

- **核心思想:** 放棄儲存整個前綴和陣列，只保留當前遍歷到的累計和。
- **適用場景:** 當我們只需要「當前累計和」與「歷史累計和」的關係，而不需要隨機查詢任意區間和時。
- **優勢:** 空間複雜度從 O(n) 降至 O(1)。

**範例：**

```cpp
// 傳統方法：先建構，再操作 (空間 O(n))
vector<int> prefix(nums.size() + 1, 0);
for (int i = 0; i < nums.size(); i++) {
    prefix[i + 1] = prefix[i] + nums[i];
}
// ... 之後再遍歷 prefix 陣列進行操作 ...

// 優化方法：使用 Running Sum (空間 O(1))
int runningSum = 0;
for (int i = 0; i < nums.size(); i++) {
    runningSum += nums[i];
    // 直接使用 runningSum (即當前的前綴和) 進行計算
    // 例如：if (map.count(runningSum - k)) { ... }
}
```

這種從「靜態的前綴和陣列」到「動態的滾動和變數」的思維轉變，是前綴和技巧的重要優化。
