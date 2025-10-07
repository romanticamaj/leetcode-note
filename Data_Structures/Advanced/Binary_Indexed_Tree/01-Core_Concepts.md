# Binary Indexed Tree (Fenwick Tree) 核心概念

## TL;DR

Binary Indexed Tree (BIT) 支援 **O(log n) update** 和 **O(log n) query**，空間 O(n)，實作簡潔（~20 行）。

### 五大設計要點

1. **i & -i**：提取最低位的 1，決定區間長度
2. **tree[i]**：管理區間 `[i - (i & -i) + 1, i]`
3. **Update**：`i += i & -i`（向上）
4. **Query**：`i -= i & -i`（向下）
5. **索引從 1**：避免 `i & -i = 0`

### 適用場景

- ✅ 動態區間和查詢
- ✅ 計數問題（逆序對）
- ❌ 區間更新（用 Segment Tree）

---

## 🎯 為什麼需要 Binary Indexed Tree？

### 問題場景

```
給定陣列 nums，支援：
1. update(index, val): 更新 nums[index] = val
2. sumRange(left, right): 查詢 nums[left..right] 總和
```

### 解法對比

| 方法         | Update       | Range Query  | Space    | 評價         |
| ------------ | ------------ | ------------ | -------- | ------------ |
| Prefix Sum   | O(n)         | O(1)         | O(n)     | Update 太慢  |
| **BIT**      | **O(log n)** | **O(log n)** | **O(n)** | ✅ 最佳平衡  |
| Segment Tree | O(log n)     | O(log n)     | O(4n)    | 功能強但複雜 |

---

## 🧮 核心公式：`i & -i`

### 數學原理

> **`i & -i` 提取二進制最低位的 1** (Lowest Set One, LSOne)

```
i = 6:
  i     = 0000 0110
  NOT i = 1111 1001
  +1    = 1111 1010  (= -i，補碼)

i & -i:
  0000 0110
  1111 1010
  ─────────
  0000 0010 = 2  ← 只留最低位的 1
```

### 範例

```
i = 1:  0001 → i & -i = 1
i = 2:  0010 → i & -i = 2
i = 3:  0011 → i & -i = 1
i = 4:  0100 → i & -i = 4
i = 5:  0101 → i & -i = 1
i = 6:  0110 → i & -i = 2
i = 8:  1000 → i & -i = 8
```

**規律**：`i & -i` = 2^(尾隨零的數量)

---

## 🏗️ 區間管理設計

### tree[i] 管理的區間

```
tree[i] 管理區間：[i - (i & -i) + 1, i]
區間長度：i & -i
```

### 範例（n = 8）

```
tree[1] 管理 [1, 1]   長度 1
tree[2] 管理 [1, 2]   長度 2
tree[3] 管理 [3, 3]   長度 1
tree[4] 管理 [1, 4]   長度 4
tree[5] 管理 [5, 5]   長度 1
tree[6] 管理 [5, 6]   長度 2
tree[7] 管理 [7, 7]   長度 1
tree[8] 管理 [1, 8]   長度 8
```

### 樹狀結構

```
                    tree[8]
                   ↗ ↗ ↗ ↗
             tree[4] tree[6]
               ↗ ↗   ↗ ↗
          tree[2] tree[5]
            ↗      ↗
       tree[1] tree[3] tree[7]
```

**直覺**：

- `i & -i` 越大 → 管理越大區間（越「高」）
- `i & -i` 越小 → 管理越小區間（越「低」）

---

## 🔧 三大操作

### 1. Construction（O(n) Bottom-Up）⭐

```cpp
// Step 1: 初始化 leaf
for (int i = 0; i < n; i++) {
    tree[i + 1] = nums[i]; // spread 原值進去 tree
}

// Step 2: 向上傳播
for (int i = 1; i <= n; i++) {
    int parent = i + (i & -i);
    if (parent <= n) {
        tree[parent] += tree[i]; // propagate tree 值給 parent
    }
}
```

**原理**：每個節點只向父節點傳播一次 → O(n)

---

### 2. Update（O(log n)）

```cpp
void update(int index, int val) {
    int delta = val - nums[index];
    nums[index] = val;

    int i = index + 1;  // 轉為 BIT 索引
    while (i <= n) {
        tree[i] += delta;
        i += i & -i;  // 向上到父節點
    }
}
```

**路徑範例**（n=8, update index 2）：

```
BIT 索引 3 → 4 → 8
```

**公式**：`parent(i) = i + (i & -i)`

---

### 3. Query（O(log n)）

#### Prefix Sum

```cpp
int query(int index) {
    int i = index + 1;  // 轉為 BIT 索引
    int sum = 0;
    while (i > 0) {
        sum += tree[i];
        i -= i & -i;  // 向下查詢路徑
    }
    return sum;
}
```

**路徑範例**（查詢 index 5）：

```
BIT 索引 6 → 4 → 0
sum = tree[6] + tree[4]
```

**公式**：`queryPath(i) = i - (i & -i)`

#### Range Sum

```cpp
int sumRange(int left, int right) {
    return query(right) - query(left - 1);
}
```

---

## 🎨 為什麼索引從 1 開始？

### 問題

```cpp
i = 0
i & -i = 0
parent(0) = 0 + 0 = 0  // 無限迴圈！
```

### 解決

```cpp
// 陣列索引：[0, n-1]
// BIT 索引： [1, n]

int bitIndex = arrayIndex + 1;
```

---

## 📊 口訣與記憶

### 口訣 1: i & -i

> **「負數翻轉加一，AND 後只留最低燈」**

### 口訣 2: Update vs Query

> **「Update 向上爬，Query 向下找」**

```
Update: i += i & -i  (往上跳)
Query:  i -= i & -i  (往下走)
```

### 口訣 3: 區間管理

> **「i & -i 決定長，最低位越大管越廣」**

---

## 🔗 資料結構對比

| 特性     | BIT      | Segment Tree | Sqrt Decomposition |
| -------- | -------- | ------------ | ------------------ |
| Update   | O(log n) | O(log n)     | O(1)               |
| Query    | O(log n) | O(log n)     | O(√n)              |
| Space    | O(n)     | O(4n)        | O(n + √n)          |
| 實作難度 | ⭐       | ⭐⭐⭐       | ⭐⭐               |
| 功能擴展 | 受限     | 強大         | 中等               |

**結論**：

- BIT：單點更新 + 區間查詢（面試首選）
- Segment Tree：區間更新 + 區間查詢
