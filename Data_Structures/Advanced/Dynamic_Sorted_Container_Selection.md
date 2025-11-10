# 動態排序容器選擇指南

## 🎯 基於查詢類型的決策樹

**從對 window 內項目的查詢需求，決定使用哪種資料結構：**

```
Window 內需要什麼查詢？
├─ Specific value / Counting (存在性、頻率)
│  └─ HashMap/HashSet → O(1) query
│
├─ Value 符合某個 constraint (範圍、大小關係)
│  └─ Ordered Set (set/multiset) → O(log k) query
│
└─ Min/Max / Top-K
   └─ Heap (priority_queue) → O(1) access, O(log k) maintain
```

## 📊 容器選擇速查表

| 查詢需求               | 推薦容器         | Insert   | Query    | Access | 典型應用           |
| ---------------------- | ---------------- | -------- | -------- | ------ | ------------------ |
| **Specific value**     | `unordered_map`  | O(1)     | O(1)     | O(1)   | 重複元素檢查       |
| **Counting/Frequency** | `unordered_map`  | O(1)     | O(1)     | O(1)   | 字符頻率、anagram  |
| **Range constraint**   | `set/multiset`   | O(log k) | O(log k) | O(1)\* | Value diff ≤ k     |
| **Min/Max only**       | `priority_queue` | O(log k) | -        | O(1)   | Sliding window max |
| **Top-K**              | `priority_queue` | O(log k) | -        | O(1)   | K 個最大值         |

*Min: `*set.begin()`, Max: `\*set.rbegin()`

## 🔍 查詢能力對比

### 1. HashMap/HashSet - O(1) 查詢

```cpp
unordered_map<int, int> freq;  // value -> count
unordered_set<int> seen;       // value existence

// Specific value check
if (seen.count(x)) { ... }      // O(1)

// Counting
freq[x]++;                       // O(1)
if (freq[x] >= k) { ... }       // O(1)
```

**適用查詢**：

- ✅ 特定值是否存在
- ✅ 值的出現頻率
- ✅ 快速 insert/delete
- ❌ 無法 range query
- ❌ 無法快速找 min/max

### 2. Ordered Set - O(log k) 範圍查詢

```cpp
set<int> s;
s.insert(x);                     // O(log k)
s.erase(x);                      // O(log k)
auto it = s.lower_bound(x);     // O(log k) - 成員函數
int min = *s.begin();           // O(1)
int max = *s.rbegin();          // O(1)
```

**適用查詢**：

- ✅ Range query (`[a, b]` 範圍內的值)
- ✅ lower_bound / upper_bound
- ✅ 前驅/後繼
- ✅ Min/Max
- ❌ 較慢的 insert/delete (vs hashmap)

### 3. Heap - O(1) Min/Max 存取

```cpp
priority_queue<int> maxHeap;                              // Max heap
priority_queue<int, vector<int>, greater<int>> minHeap;   // Min heap

maxHeap.push(x);        // O(log k)
int top = maxHeap.top();   // O(1)
maxHeap.pop();          // O(log k)
```

**適用查詢**：

- ✅ Top element (min 或 max)
- ✅ Top-K 問題
- ❌ 無法 lower_bound
- ❌ 無法高效刪除特定元素
- ❌ 無法隨機存取

## ⚠️ 常見陷阱

### 陷阱 1：`std::lower_bound` vs `set.lower_bound`

```cpp
set<int> s = {1, 3, 5};

// ❌ 錯誤：O(n) 時間
auto it1 = lower_bound(s.begin(), s.end(), 3);

// ✅ 正確：O(log n) 時間
auto it2 = s.lower_bound(3);
```

**原因**：全局 `lower_bound` 假設 random access iterator，對 set 退化為線性搜尋。

### 陷阱 2：Heap 無法高效刪除特定元素

```cpp
// ❌ 錯誤：無法直接刪除 window 最舊元素
priority_queue<int> pq;
// 無法 erase(oldest_value)

// ✅ 正確：Lazy deletion
priority_queue<pair<int, int>> pq;  // {value, index}
// 檢查 top 的 index 是否過期
```

## ✅ 選擇檢查清單

**基於查詢需求：**

- [ ] **查詢特定值/計數？** → `unordered_map/set`
- [ ] **查詢範圍/約束？** → `set/multiset`
- [ ] **只需 min/max？** → `priority_queue` 或 `set`

**基於操作特性：**

- [ ] **需要動態更新？** Yes → 排除靜態 `sort()`
- [ ] **有重複值？** Yes → `multiset` 或 `unordered_map<int, int>`
- [ ] **需要刪除特定元素？** Yes → `set` 優於 `heap`
