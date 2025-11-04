# 去重剪枝設計心法

## 問題場景：為何需要 Duplicate Removal？

當 input 包含**重複元素**時（例如 `[1, 1, 2]`），naive backtracking 會產生**重複的解**。

**範例**：生成排列

```
Input: [1, 1, 2]
Naive output: [1,1,2], [1,2,1], [1,1,2], [1,2,1], [2,1,1], [2,1,1]
                 ↑              ↑              重複！
Desired output: [1,1,2], [1,2,1], [2,1,1]  (每個只出現一次)
```

**問題根源**：兩個 `1` 在 index 0 和 1，但它們的**值相同**，交換位置後產生相同排列。

## 🧠 核心哲學：去重的本質

Duplicate removal 的核心在於：**設計 pruning rule 來跳過會產生重複解的分支**。

有三種思考方向：

### 方向 1: 不排序，記錄「已嘗試的值」 (Local Pruning)

- **思路**：在每個決策點，記住「這個位置試過哪些值」
- **工具**：`unordered_set<Value>` per recursion level
- **Rule**：如果某個值在當前位置已試過，就跳過

### 方向 2: 排序後，強制「選擇順序」(Global Pruning)

- **思路**：對相同的值建立固定的選擇順序（例如：必須先選 index 小的）
- **工具**：先 `sort()`，然後用 index ordering rule
- **Rule**：當 `nums[i] == nums[i-1]` 時，只有 `nums[i-1]` 已被選才能選 `nums[i]`

### 方向 3: Domain Transformation - Grouping (Frequency-Based)

- **思路**：將 array domain 轉換成 frequency table domain，直接用「值」和「剩餘次數」建模
- **工具**：`unordered_map<Value, Count>` 代表 candidate pool
- **Rule**：每次選擇一個值，減少它的 count；count 為 0 時自然不再選

**關鍵差異**：

- Local pruning: 關心「這個位置用過什麼**值**」
- Global pruning: 關心「相同值之間的**選擇順序**」
- Grouping: 改變問題表示，從「選 index」變成「選 value + count」

## 核心問題：該用哪種去重策略？

答案取決於你如何管理 **Decided/Undecided sets**：

| Candidate Set 管理方式             | 適合的 Pruning 策略                     |
| ---------------------------------- | --------------------------------------- |
| **Swap-based** (候選集動態變化)    | Local Pruning                           |
| **Visited-based** (候選集靜態不變) | Global Pruning 或 Local Pruning         |
| **Frequency table** (改變 domain)  | Grouping (天然去重，根本不需要 pruning) |

## 🎯 設計決策樹

```
包含重複元素的 Backtracking 問題
             |
             v
    如何表示 Candidate Set?
             |
    ┌───────────┼─────────┐
    |           |         |
  Swap       Visited   Frequency
  方式         方式      Table
    |           |         |
    v           v         v
候選集       候選集      改變 domain
動態變化     靜態不變    值+次數建模
    |           |         |
    v           v         v
必須            可選      天然去重
Local         Global/  不需pruning
Pruning         Local     |
    |             |       v
    v             v      直接用
用 HashSet    ┌───┴───┐  count控制
記錄已試過     v        v  選擇次數
的「值」    Sort+   HashSet
          Ordering   記錄
            Rule    已試過
```

**關鍵判斷點**：

- Swap 會破壞排序 → 只能 Local pruning
- Frequency table 改變問題表示 → 天然去重，最簡潔

## 🔧 Pattern 1: Swap-Based → Local Pruning

**State Representation**:

```cpp
// Decided: nums[0:start]
// Undecided: nums[start:]
```

**關鍵 Data Structure + Pruning**:

```cpp
unordered_set<int> used;  // 🔑 每層遞迴都是新的 set

for (int i = start; i < nums.size(); i++) {
    if (used.count(nums[i])) continue;  // Pruning: 跳過已試過的值
    used.insert(nums[i]);
    // ... swap + backtrack + swap back
}
```

**為何必須 Local?**

- Swap 破壞排序 → 無法用 global ordering rule
- 只能在每個位置記錄「試過哪些值」

**Pruning Rule**: 在位置 `start`，值 X 只能被 swap 到這裡一次

## 🔧 Pattern 2: Visited-Based → Global Pruning

**State Representation**:

```cpp
// Decided: indices where visited[i] == true
// Undecided: indices where visited[i] == false
```

**關鍵 Data Structure + Pruning**:

```cpp
sort(nums.begin(), nums.end());  // 🔑 前置：讓相同值相鄰

vector<bool> visited(n, false);  // 🔑 全局追蹤已選的 index

for (int i = 0; i < nums.size(); i++) {
    if (visited[i]) continue;

    // 🔑 Global pruning: 強制相同值按 index 順序選
    if (i > 0 && nums[i] == nums[i-1] && !visited[i-1])
        continue;

    // ... mark visited, backtrack, unmark
}
```

**為何可用 Global?**

- `nums` 保持 sorted → 相同值相鄰
- 建立 canonical ordering: 前面的相同值必須先選

**Pruning Rule**: 只有 `nums[i-1]` 已被選，才能選 `nums[i]`（當值相同時）

## 🔧 Pattern 3: Grouping → Domain Transformation

**Domain Transformation**:

```cpp
// Array Domain → Frequency Table Domain
Input: [1, 1, 2]  →  freq: {1: 2, 2: 1}
```

**關鍵 Data Structure + 去重機制**:

```cpp
unordered_map<int, int> freq;  // 🔑 值 → 剩餘次數
for (int num : nums) freq[num]++;

// 在 backtrack 中：
for (auto& [value, count] : freq) {
    if (count == 0) continue;  // 這個值用完了

    freq[value]--;  // 使用一次
    // ... backtrack
    freq[value]++;  // 歸還
}
```

**為何天然去重？**

- 用「值」當 key，根本不存在「不同 index 但同值」的問題
- `count` 本身就控制「這個值能用幾次」

**優勢**: 不需 sorting、visited、或 pruning HashSet

## ⚖️ 三種方式的對比分析

| 維度              | Swap + Local          | Visited + Global | Grouping                  |
| ----------------- | --------------------- | ---------------- | ------------------------- |
| **Domain**        | Array/Index           | Array/Index      | Value/Count               |
| **Candidate Set** | 動態變化，無序        | 靜態，可 sorted  | Frequency table           |
| **Pruning 方式**  | HashSet per level     | Ordering rule    | 不需要 (天然去重)         |
| **Memory**        | 每層 O(unique values) | O(n) visited[]   | O(unique values) freq map |
| **前置要求**      | 無                    | Sort: O(n log n) | Build freq: O(n)          |
| **Code 複雜度**   | 中等                  | 中等             | 最簡潔                    |
| **直覺性**        | position-value        | ordering rule    | value-count (最直覺)      |

## 🎓 設計思路提煉

當遇到 duplicate removal 時，問自己：

### Step 1: 分析 Candidate Set 管理方式

```
Q: 我的 undecided set 會被修改嗎？
   - Yes (例如 swap) → 傾向 Local pruning
   - No (例如 visited) → 可選 Global pruning
```

### Step 2: 檢查是否能建立 Global Ordering

```
Q: 能否對所有 candidates 建立 total order？
   - Yes + sorted → Global pruning 更簡潔
   - No → 必須 Local pruning
```

### Step 3: 考慮 Domain Transformation

```
Q: 能否改變問題表示？
   - Array domain → Frequency table domain
   - 優勢：天然去重，code 最簡潔
   - 適合：排列/組合問題，不需要保留原始 index
```

### Step 4: 選擇 Pruning Data Structure

```
Local pruning:
  - unordered_set<Value> per level
  - O(1) check, O(unique values) space

Global pruning:
  - Sort once + ordering rule
  - O(1) check, no extra space

Grouping:
  - Frequency map: unordered_map<Value, Count>
  - 不需要額外 pruning logic
```

## ✅ 關鍵要點

- [ ] Duplicate removal 有三種思考方向：Local pruning、Global pruning、Domain transformation
- [ ] **Swap-based** → 動態 candidate set → **Local pruning**（hashset per position）
- [ ] **Visited-based** → 靜態 candidate set → **Global pruning**（sorted + ordering rule）
- [ ] **Grouping** → 改變 domain 到 frequency table → **天然去重**（最簡潔）
- [ ] Local: 關心「位置用過什麼值」｜ Global: 關心「值的選擇順序」｜ Grouping: 關心「值的剩餘次數」
- [ ] 三種方式都是 O(n! × n)，但 constant factor 和 code 複雜度不同
- [ ] Grouping 在不需要保留原始 index 時是最佳選擇

## 🔗 相關文件

- [`03-Backtracking_Candidate_Modeling.md`](./03-Backtracking_Candidate_Modeling.md) - Decided/Undecided 集合建模
- [`Swap_as_In_Place_State_Management.md`](./Swap_as_In_Place_State_Management.md) - Swap 技巧詳解
