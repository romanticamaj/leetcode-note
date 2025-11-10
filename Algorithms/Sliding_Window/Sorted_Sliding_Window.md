# Sorted Sliding Window

## 🧠 核心哲學

當 sliding window 內的元素需要**維護排序屬性**或**支援 range query** 時，使用 Ordered Set 作為 window 容器，實現 O(log k) 的動態維護與查詢。

## 核心概念

**Sorted Sliding Window** = Sliding Window + Ordered Set

**識別條件**：

- ✅ 需要維護固定大小的 window（e.g. index difference 限制）
- ✅ window 內需要排序屬性（查詢、比較、range query）

**關鍵差異**：

| 傳統 Sliding Window                | Sorted Sliding Window                          |
| ---------------------------------- | ---------------------------------------------- |
| 容器：`deque`, `vector`, `hashmap` | 容器：`std::set`, `std::multiset`              |
| 無序，O(1) access/update           | 有序，O(log k) query                           |
| 適合：sum, count, 頻率統計         | 適合：range query, min/max, 排序性質           |
| **檢查 window 本身的屬性**         | **檢查 current 與 window 內 candidate 的關係** |

## 🔄 演算法架構：Check → Expand → Fix

**與傳統 Sliding Window 的差異**：

```
傳統：Expand → Fix → Update
      ↓
      檢查 window 整體屬性（sum, count）
      window 包含 current

Sorted：Check → Expand → Fix
       ↓
       檢查 current 與 window 內某個 candidate 的關係
       window 不包含 current（在 check 時）
```

**為何順序不同？**

- 傳統：window 是**狀態**，檢查 window 整體
- Sorted：window 是 **candidate set**，current 與 candidates 比較

## 通用模板

```cpp
bool sortedSlidingWindow(vector<int>& nums, int windowSize) {
    set<int> window;  // 使用 multiset 若有重複值

    for (int i = 0; i < nums.size(); i++) {
        // === Step 1: Check - 查詢 window ===
        // current (nums[i]) 尚未加入 window
        // 查詢邏輯：lower_bound, upper_bound, min, max
        if (WINDOW_HAS_VALID_CANDIDATE) {
            update_answer();
        }

        // === Step 2: Expand - 加入新元素 ===
        window.insert(nums[i]);

        // === Step 3: Fix - 維護 window size ===
        if (window.size() > windowSize) {
            window.erase(nums[i - windowSize]);
        }
    }

    return false;  // 根據具體問題返回
}
```

## 🧩 常見查詢模式

### Pattern 1: Min/Max Query

```cpp
// 取得 window 內最小值/最大值
int minVal = *window.begin();    // O(1)
int maxVal = *window.rbegin();   // O(1)
```

### Pattern 2: Range Query (lower_bound/upper_bound)

```cpp
// 查詢第一個 >= target 的元素
auto it = window.lower_bound(target);  // O(log k)

// 查詢第一個 > target 的元素
auto it = window.upper_bound(target);  // O(log k)
```

### Pattern 3: 前驅/後繼查詢

```cpp
auto it = window.find(x);

// 前驅（比 x 小的最大值）
if (it != window.begin()) {
    int predecessor = *prev(it);
}

// 後繼（比 x 大的最小值）
if (next(it) != window.end()) {
    int successor = *next(it);
}
```

## ✅ 關鍵要點

- [ ] **容器選擇**：
  - 無重複值：`std::set`
  - 有重複值：`std::multiset`
  - 只需頻率：`hashmap` (傳統 sliding window)
- [ ] **架構順序**：Check → Expand → Fix（current 與 candidates 比較）
- [ ] **Window 語意**：candidate set，check 時不包含 current
- [ ] **成員函數優先**：用 `set.lower_bound()` 而非 `std::lower_bound()`
- [ ] **邊界檢查**：任何 iterator 操作前檢查 `!= end()` 和 `!= begin()`

## 相關資源

- [傳統 Sliding Window](./00-Sliding_Window_Fundamental.md) - Expand → Fix → Update
- [動態排序容器選擇指南](../../Data_Structures/Advanced/Dynamic_Sorted_Container_Selection.md) - 何時用 set vs heap
