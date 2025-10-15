# Vector O(1) 刪除：Swap-to-End 技巧

## 🧠 核心心法

> **「不動千軍，只換一兵」**
> 將待刪元素與末尾元素交換，然後 pop_back()，只需更新一個索引。

**適用前提**：不需要維持元素的相對順序

---

## 問題與解法

### ❌ 問題：傳統刪除破壞索引映射

```cpp
vector<int> arr = {10, 20, 30, 40, 50};
unordered_map<int, int> index; // val -> index

// 刪除 arr[2] (值為 30)
arr.erase(arr.begin() + 2);  // O(n) - 需要移動元素

// 災難：所有後續元素的索引都改變了！
// 40: index 3 -> 2
// 50: index 4 -> 3
// HashMap 中的索引映射全部失效
```

### ✅ 解法：Swap-to-End

```cpp
const int idx = index[val];
const int last = arr.size() - 1;

if (idx != last) {
    index[arr[last]] = idx;      // 1. 更新末尾元素的新位置
    swap(arr[idx], arr[last]);   // 2. 交換到末尾
}

arr.pop_back();                  // 3. O(1) 刪除
index.erase(val);
```

**關鍵優勢**：

- 只有末尾元素的索引改變，其他元素不受影響
- 時間複雜度：O(1)

---

## 🧩 實作模式

### Pattern 1: 基本版（按索引刪除）

適用於只需要 O(1) 刪除，不關心順序的場景。

```cpp
void removeAtIndex(int idx) {
    if (idx != arr.size() - 1) {
        swap(arr[idx], arr.back());
    }
    arr.pop_back();
}
```

### Pattern 2: 混合設計（HashMap + Vector）

適用於需要同時支援：

- O(1) 插入
- O(1) 按值刪除
- O(1) 隨機存取（uniform distribution）

**數據結構組合**：

- `unordered_map<Value, Index>`：O(1) 值查找和索引映射
- `vector<Value>`：O(1) 隨機存取和 `rand() % size`

**典型應用**：

- LeetCode 380: Insert Delete GetRandom O(1)
- LeetCode 381: Insert Delete GetRandom O(1) - Duplicates allowed

**為什麼不能單用 HashMap？**
HashMap 無法實現等機率隨機選取（bucket 數量未知，hash collision 導致機率不均）

## 適用場景

### O(1) 隨機存取 + O(1) 刪除

- 需要 uniform distribution 的隨機選取
- 遊戲中隨機選擇玩家
- 負載均衡隨機選擇伺服器
- 抽獎系統等機率抽取

### 圖演算法節點移除

- 動態圖中刪除節點並維護索引
- Tarjan's Algorithm 的優化實作

---

## ⏱️ 複雜度分析

| 操作        | 時間複雜度 | 空間複雜度 |
| ----------- | ---------- | ---------- |
| insert(val) | O(1)       | O(1)       |
| remove(val) | O(1)       | O(1)       |
| getRandom() | O(1)       | O(1)       |
| 總空間      | -          | O(n)       |

---

## 相關技巧

- **In-Place Array Manipulation**：同樣使用 swap 避免 O(n) 移動
- **Index as Reference**：使用索引代替物件，減少空間開銷
