# Boyer-Moore Voting Algorithm 解題心法

## 🧠 核心哲學

**配對抵消 (Pairing and Cancellation)**：透過「不同元素互相抵消」的策略，在 O(n) 時間、O(1) 空間內找出多數元素或眾數。

## 核心概念：Majority Voting

### 定義

在長度為 n 的序列中，若元素 x 出現次數 **嚴格大於** n/k，則 x 為 k-majority element。

**關鍵洞察**：

- 最多只有 k-1 個 k-majority elements
- 1/2-majority (經典問題)：最多 1 個候選
- 1/3-majority：最多 2 個候選

## 通用模板 / General Template

### Pattern 1: 單一多數元素 (n/2)

```cpp
int findMajorityElement(vector<int>& nums) {
    int candidate = 0, count = 0;

    // Phase 1: 找候選人 (Pairing)
    for (int num : nums) {
        if (count == 0) candidate = num;
        count += (num == candidate) ? 1 : -1;
    }

    // Phase 2: 驗證候選人 (Optional，題目保證存在時可省略)
    count = 0;
    for (int num : nums) {
        if (num == candidate) count++;
    }
    return count > nums.size() / 2 ? candidate : -1;
}
```

### Pattern 2: 多個多數元素 (n/k)

```cpp
vector<int> findKMajority(vector<int>& nums, int k) {
    // 最多 k-1 個候選人
    unordered_map<int, int> candidates;

    // Phase 1: 維護至多 k-1 個候選
    for (int num : nums) {
        if (candidates.count(num)) {
            candidates[num]++;
        } else if (candidates.size() < k - 1) {
            candidates[num] = 1;
        } else {
            // 所有候選計數 -1 (配對抵消)
            for (auto it = candidates.begin(); it != candidates.end(); ) {
                if (--it->second == 0) it = candidates.erase(it);
                else ++it;
            }
        }
    }

    // Phase 2: 驗證每個候選
    vector<int> result;
    for (auto& [num, _] : candidates) {
        int count = std::count(nums.begin(), nums.end(), num);
        if (count > nums.size() / k) result.push_back(num);
    }
    return result;
}
```

## 🧩 心法要點

### 為何有效？反證法證明

**1/2-majority 證明**：

- 若真正的多數元素 M 出現 > n/2 次
- 配對過程中，M 與非 M 元素抵消
- **最多**抵消掉所有非 M 元素（< n/2 個）
- M 仍會剩餘，成為最終 candidate

**關鍵**：多數元素的「數量優勢」保證其能在配對戰中存活

### 配對抵消的時機選擇

| 策略         | count == 0 時            | count > 0 時                    |
| ------------ | ------------------------ | ------------------------------- |
| **新元素**   | 成為新候選               | num == candidate 則 +1，否則 -1 |
| **物理意義** | 前面配對平手，重新選候選 | 繼續累積或抵消                  |

### 兩階段設計模式

```cpp
// Phase 1: Candidate Selection (必要)
//   - 找出「可能」的多數元素
//   - O(n) 時間，O(k) 空間

// Phase 2: Validation (條件性必要)
//   - 驗證候選是否真的滿足條件
//   - 僅當題目不保證存在多數元素時需要
```

## 適用場景 / Use Cases

| 問題類型         | k 值 | 候選數量 | 典型題目        |
| ---------------- | ---- | -------- | --------------- |
| **經典多數元素** | 2    | 1        | LeetCode 169    |
| **超過 1/3**     | 3    | ≤2       | LeetCode 229    |
| **頻率追蹤**     | 任意 | k-1      | Stream majority |

**識別關鍵字**：

- "出現次數 > n/k"
- "多數元素" (majority element)
- "O(1) 空間" 限制

## ⏱️ 複雜度分析

| 階段     | 時間     | 空間     | 備註              |
| -------- | -------- | -------- | ----------------- |
| Phase 1  | O(n)     | O(k)     | k 為 n/k 中的 k   |
| Phase 2  | O(n)     | O(1)     | 可與 Phase 1 合併 |
| **總計** | **O(n)** | **O(k)** | k=2 時為 O(1)     |

## ✅ 關鍵檢查點

- [ ] **確認 k 值**：問題要求 > n/k 還是 ≥ n/k？
- [ ] **存在性保證**：題目是否保證多數元素存在？
  - ✅ 保證存在 → Phase 2 可省略
  - ❌ 不保證 → 必須 Phase 2 驗證
- [ ] **候選數量**：最多 k-1 個候選人
- [ ] **配對時機**：`count == 0` 時更換候選
- [ ] **驗證閾值**：`count > n/k`（注意是嚴格大於）

## 延伸應用

- **Stream 演算法**：處理無限數據流的多數元素
- **分散式投票**：多數決共識演算法
- **錯誤更正碼**：找出主要錯誤模式
