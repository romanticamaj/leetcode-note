# Difference Array 演算法心法 (基於半開區間 `[left, right)`)

## 🧠 核心概念

### 為什麼需要 Difference Array？

處理 interval 問題時，最直觀的方法是對所有區間按起點或終點**排序**，然後用掃描線處理。但當需要處理「區間更新」問題（例如：每個區間對範圍內所有點都有貢獻），排序後仍需逐點更新，導致額外的 O(m) 開銷。

**Difference Array** 透過「端點標記 + 前綴和」，將區間更新複雜度從 O(L) 降至 O(1) 或 O(log N)。

### Mental Model: 銀行帳戶餘額追蹤

將 interval 問題轉換為「時間點的狀態變化量」：

- 存款事件 → `+amount`，提款事件 → `-amount`
- 當前餘額 → running sum of all deltas
- 最高餘額 → 追蹤過程中的峰值

**核心思想**: 將連續區間操作轉化為兩個端點的離散操作

- 在 `[left, right)` 的 `left` 記錄 `+value`
- 在 `right` 記錄 `-value`
- 用 running sum 沿時間軸遍歷，還原每個點的狀態

### Delta vs Absolute State

| 方法                  | 追蹤內容         | 空間效率 | 適用場景                   |
| --------------------- | ---------------- | -------- | -------------------------- |
| Absolute State (絕對) | 活躍區間集合     | 需存所有 | 需要知道「哪些區間」活躍   |
| Delta State (變化量)  | 狀態變化量 (+/-) | 只存端點 | 只需要知道「併發數量」即可 |

**Delta 優勢**: Space efficient、自動合併相同時間點事件、符合 Prefix Sum 思維

### 🔗 與其他技術的關係

- **本質**: Prefix Sum 的應用（`prefix[i] = prefix[i-1] + delta[i]`）
- **實作**: Sweep Line 的特例（只掃事件點，不需追蹤具體對象）
- **相關**: [Running State Pattern](02_Running_State_Pattern.md)、[Sweep Line Core Concepts](../Sweep_Line/01-Sweep_Line_Core_Concepts.md)

### 🎯 適用場景

**✅ 適合使用**:

- 只需要知道「最大併發數」（不需要知道是哪些區間）
- 時間點可能重複（多個區間在同一時間開始/結束）
- 問題可以抽象為「狀態的增減」

**⚠️ 不適合使用**:

- 需要知道「是哪個區間」結束
- 需要根據區間的額外屬性做決策
- 區間有優先級或權重需要動態調整

---

## 🧩 演算法設計核心：Build + Walk

Difference Array 的演算法設計遵循兩階段模式：

1. **Build 階段**：建構差分結構，標記每個事件端點的變化量
2. **Walk 階段**：遍歷所有端點，使用前綴和 (Prefix Sum) 計算每個點的實際狀態

**關鍵決策點**：根據 **input 數量 (n)** 和 **事件範圍 (m)** 的關係，選擇不同的資料結構來實現 Build 和 Walk：

- 範圍固定且不大 → 使用 `vector<int>`
- 範圍很大但事件稀疏 → 使用 `map<int, int>` 或 `vector<pair<int, int>>`

---

## 方法一：`vector<int>` - 固定範圍的基本作法

### 適用場景

- **範圍已知且不大**：座標範圍 m ≤ 10^5（例如：0 ≤ time ≤ 1000）
- **密集事件**：大部分座標點都會被覆蓋到

### 核心操作

- **Build**：對每個區間 `[left, right)`，在 `diff[left] += value` 和 `diff[right] -= value`
- **Walk**：從 0 到 m 遍歷，計算 prefix sum（這是 Sweep Line + Prefix Sum 的組合）

### 時間複雜度

- **Build**：O(n)，n 為區間數量
- **Walk**：O(m)，m 為範圍大小
- **總計**：**O(n + m)**

### C++ 實作

```cpp
// 範例：計算所有區間的最大重疊數
void vectorDifferenceArray(const std::vector<std::vector<int>>& intervals) {
    // 假設座標範圍為 [0, MAX_TIME)
    const int MAX_TIME = 1001;
    std::vector<int> diff(MAX_TIME + 1, 0);

    // === 1. Build: 建構差分陣列 ===
    for (const auto& interval : intervals) {
        int left = interval[0];
        int right = interval[1];
        int value = interval[2];  // 每個區間的權重值

        // 確保索引不越界
        if (left < MAX_TIME) diff[left] += value;
        if (right < MAX_TIME) diff[right] -= value;
    }

    // === 2. Walk: 掃描線 + 前綴和 ===
    int running_sum = 0;
    int max_overlap = 0;

    for (int i = 0; i < MAX_TIME; ++i) {
        running_sum += diff[i];  // 計算前綴和
        max_overlap = std::max(max_overlap, running_sum);
    }

    std::cout << "Maximum overlap: " << max_overlap << std::endl;
}
```

---

## 方法二：`map<int, int>` - 稀疏事件的優化

### 適用場景

- **範圍非常大**：座標範圍 m ≤ 10^9（例如：1 ≤ time ≤ 10^9）
- **稀疏事件**：只有少數座標點有事件發生（n << m）

### 核心操作

- **Build**：用 `map` 記錄端點變化量，`map` 會自動按 key 排序
  - Concept: Sorting for later sweeping
- **Walk**：遍歷 (Sweep) `map` 中的**事件點**（Event, 而非整個範圍），計算 Prefix Sum
  - Concept: Sweep Event + Prefix Sum）

### 時間複雜度

- **Build**：O(n log k)，n 為區間數量，k 為不同端點數量（最多 2n）
- **Walk**：O(k)，k 為不同端點數量
- **總計**：**O(n log n)**（因為 k ≤ 2n）

### 優勢分析

相比固定範圍的 `vector` 方法：

- 當 m（範圍）遠大於 n（區間數）時，`map` 只處理 O(n) 個事件點，而不是 O(m) 個座標點
- 例如：1000 個區間分布在 [1, 10^9] 範圍內，`map` 只需處理約 2000 個點，而 `vector` 需要 10^9 個空間

### C++ 實作

```cpp
// 範例：計算所有區間的最大重疊數（稀疏座標）
void mapDifferenceArray(const std::vector<std::vector<int>>& intervals) {

    // === 1. Build: 建構差分映射表 ===
    // key: 時間點 (座標)，自動排序
    // value: 該時間點的淨變化量
    std::map<int, int> diff;

    for (const auto& interval : intervals) {
        int left = interval[0];
        int right = interval[1];
        int value = interval[2];

        diff[left] += value; // 在左端點增加 value
        diff[right] -= value; // 在右端點減少 value，符合 [left, right) 的半開區間
    }

    // === 2. Walk: 遍歷事件點以計算 running sum ===
    int running_sum = 0;
    int max_overlap = 0;

    // std::map 的遍歷會自動按 key (時間點) 從小到大排序
    for (const auto& [time, change] : diff) {
        running_sum += change;  // 累加當前時間點的變化量
        max_overlap = std::max(max_overlap, running_sum);
    }

    std::cout << "Maximum overlap: " << max_overlap << std::endl;
}
```

---

## 方法三：`vector<pair<int, int>>` - map 的手動替代方案

### 適用場景

- 與 `map` 相同，但希望避免 `map` 的常數因子開銷
- 需要更快的遍歷速度（`vector` 的 cache-friendly 特性）

### 核心操作

- **Build**：建立 `vector<pair<time, change>>`，手動排序
- **Walk**：遍歷排序後的 vector，計算 prefix sum

### 時間複雜度

- **Build**：O(n)，建立事件點配對
- **Sort**：O(n log n)，手動排序（瓶頸）
- **Walk**：O(n)
- **總計**：**O(n log n)**

### 與 map 的比較

- **優點**：Walk 階段比 `map` 快（連續記憶體訪問）
- **缺點**：需要額外的排序步驟，程式碼稍複雜

### C++ 實作

```cpp
// 範例：計算所有區間的最大重疊數（使用 vector + sort）
void vectorPairDifferenceArray(const std::vector<std::vector<int>>& intervals) {
    // === 1. Build: 建立事件點配對 ===
    std::vector<std::pair<int, int>> diff_pairs;

    for (const auto& interval : intervals) {
        int left = interval[0];
        int right = interval[1];
        int value = interval[2];

        // 左端點：增加 value
        diff_pairs.push_back({left, value});
        // 右端點：減少 value
        diff_pairs.push_back({right, -value});
    }

    // === 2. Sort: 手動排序事件點 ===
    // 按時間點排序，時間相同時按變化量排序
    std::sort(diff_pairs.begin(), diff_pairs.end());

    // === 3. Walk: 遍歷事件點計算 running sum ===
    int running_sum = 0;
    int max_overlap = 0;

    for (const auto& [time, change] : diff_pairs) {
        running_sum += change;
        max_overlap = std::max(max_overlap, running_sum);
    }

    std::cout << "Maximum overlap: " << max_overlap << std::endl;
}
```

---

## 📊 三種方法總結比較

| 方法       | 資料結構                 | 適用範圍 | 時間複雜度 | 空間複雜度 | 優點                    | 缺點              |
| ---------- | ------------------------ | -------- | ---------- | ---------- | ----------------------- | ----------------- |
| **方法一** | `vector<int>`            | m ≤ 10^5 | O(n + m)   | O(m)       | 實作簡單、訪問 O(1)     | 範圍大時浪費空間  |
| **方法二** | `map<int, int>`          | m ≤ 10^9 | O(n log n) | O(n)       | 自動排序、節省空間      | 單次操作 O(log n) |
| **方法三** | `vector<pair<int, int>>` | m ≤ 10^9 | O(n log n) | O(n)       | Walk 快、cache-friendly | 需手動排序        |

_註：n = 區間數量, m = 座標範圍大小_

### 選擇建議

1. **小範圍密集問題**（如時間軸 0-1000）→ 使用 `vector<int>`
2. **大範圍稀疏問題**（如座標 1-10^9）→ 優先使用 `map<int, int>`
3. **追求極致效能**（競賽/性能敏感）→ 使用 `vector<pair<int, int>>`

---

## ✅ 實作檢查清單

- [ ] 用 `map<time, delta>` 或 `vector<int>` 儲存時間點的變化量
- [ ] 根據範圍大小選擇合適的資料結構（小範圍用 vector，大範圍用 map）
- [ ] 區間開始 `+1` 或 `+weight`，結束 `-1` 或 `-weight`
- [ ] 使用半開區間 `[left, right)` 避免重複計算
- [ ] Map 自動排序，vector 需手動 sort
- [ ] Running sum 累加 delta 得到當前狀態
