# Binary Indexed Tree 實作版本

## 🎯 版本 1: 面試推薦（維護 nums）

### 適用場景

- 面試展現思路
- Update 效能要求高

### 實作

```cpp
class NumArray {
public:
    NumArray(vector<int>& nums) : nums(nums), n(nums.size()), tree(n + 1, 0) {
        // Running Construction - O(n)
        for (int i = 0; i < n; i++) {
            tree[i + 1] = nums[i];
        }

        for (int i = 1; i <= n; i++) {
            int parent = i + (i & -i);
            if (parent <= n) {
                tree[parent] += tree[i];
            }
        }
    }

    void update(int index, int val) {
        int delta = val - nums[index]; // 直接存取 nums 值, O(1)
        nums[index] = val;

        int i = index + 1;
        while (i <= n) {
            tree[i] += delta;
            i += i & -i;
        }
    }

    int sumRange(int left, int right) {
        if (left == 0) return query(right);
        return query(right) - query(left - 1);
    }

private:
    vector<int> nums
    vector<int> tree;
    int n;

    int query(int index) {
        int i = index + 1
        int sum = 0;

        while (i > 0) {
            sum += tree[i];
            i -= i & -i;
        }

        return sum;
    }
};
```

**優點**：

- ✅ Update O(log n)
- ✅ 邏輯清晰

---

## 🚀 版本 2: 節省空間（不維護 nums）

### 適用場景

- 空間受限
- Update 不頻繁

### 實作

```cpp
class NumArray {
public:
    NumArray(vector<int>& nums) : tree(nums.size() + 1, 0), n(nums.size()) {
        for (int i = 0; i < n; i++) {
            tree[i + 1] += nums[i]; // spread value into tree

            const int index = i + 1;
            const int parent = index + (index & -index);

            if (parent <= n) {
                tree[parent] += tree[i + 1]; // propagate to parent
            }
        }
    }

    void update(int index, int val) {
        const int delta = val - sumRange(index, index);  // O(2 * log n)
        const int i = index + 1;

        while (i <= n) { // check if parent valid
            tree[i] += delta;
            i += i & -i; // look for parent
        }
    }

    int sumRange(int left, int right) {
        return query(right + 1) - query(left); // same as prefix sum
    }

private:
    vector<int> tree;
    int n;

    int query(int i) {
        int sum = 0;

        while (i > 0) { // check if path valid
            sum += tree[i];
            i -= i & -i; // look for next node on path
        }

        return sum;
    }
};
```

**缺點**：Update O(2 \* log n)（慢 2 倍）

---

## ⚡ 版本 3: 競賽標準模板

### 實作

```cpp
#define LSOne(S) ((S) & -(S))  // Lowest Set One: 提取最低位的 1

class FenwickTree {
private:
    vector<int> ft;

public:
    FenwickTree(int n) { ft.assign(n + 1, 0); }

    // Range Sum Query: [1, b]
    int rsq(int b) {
        int sum = 0;
        for (; b; b -= LSOne(b)) sum += ft[b];
        return sum;
    }

    // Range Sum Query: [a, b]
    int rsq(int a, int b) {
        return rsq(b) - (a == 1 ? 0 : rsq(a - 1));
    }

    void adjust(int k, int v) {
        for (; k < (int)ft.size(); k += LSOne(k)) ft[k] += v;
    }
};
```

**特點**：

- ✅ 極簡（~15 行）
- ✅ 快速實作（< 5 分鐘）
- ⚠️ 索引從 **1** 開始
- ⚠️ `adjust` 是增量，非設值

---

## 🔄 版本 4: Generic Template

### 實作

```cpp
template<typename T>
class BIT {
private:
    vector<T> tree;
    int n;
    function<T(T, T)> merge = [](T a, T b) { return a + b; };
    function<T(T, T)> inverse = [](T a, T b) { return a - b; };

public:
    BIT(int size) : n(size), tree(size + 1, T()) {}

    BIT(int size, function<T(T, T)> mergeFunc, function<T(T, T)> invFunc)
        : n(size), tree(size + 1, T()), merge(mergeFunc), inverse(invFunc) {}

    void update(int idx, T delta) {
        idx++;
        while (idx <= n) {
            tree[idx] = merge(tree[idx], delta);
            idx += idx & -idx;
        }
    }

    T query(int idx) {
        idx++;
        T result = T();
        while (idx > 0) {
            result = merge(result, tree[idx]);
            idx -= idx & -idx;
        }
        return result;
    }

    T rangeQuery(int left, int right) {
        if (left == 0) return query(right);
        return inverse(query(right), query(left - 1));
    }
};
```

**使用範例**：

```cpp
// 整數加法
BIT<int> bit(100);
bit.update(5, 10);

// XOR 操作
auto xorOp = [](int a, int b) { return a ^ b; };
BIT<int> bitXOR(100, xorOp, xorOp);
```

---

## 📊 版本對比

| 版本   | 行數 | Update     | Query    | 空間  | 場景     |
| ------ | ---- | ---------- | -------- | ----- | -------- |
| 版本 1 | ~50  | O(log n)   | O(log n) | O(2n) | 面試 ✅  |
| 版本 2 | ~35  | O(2 log n) | O(log n) | O(n)  | 節省空間 |
| 版本 3 | ~15  | O(log n)   | O(log n) | O(n)  | 競賽 ✅  |
| 版本 4 | ~40  | O(log n)   | O(log n) | O(n)  | 通用     |

---

## 🎯 選擇建議

### 面試

- **推薦**：版本 1
- **理由**：完整註解，邏輯清晰

### LeetCode

- **推薦**：版本 1 或 版本 2
- **理由**：標準做法

### 競賽

- **推薦**：版本 3
- **理由**：極簡，實作快

### 專案

- **推薦**：版本 4
- **理由**：可擴展，支援多型態

---

## 💡 實作技巧

### 一次 Loop 建構

```cpp
// 可在一個 loop 完成初始化和傳播
for (int i = 0; i < n; i++) {
    tree[i + 1] += nums[i]; // 必須要用 +=, 把之前的 propagate 來的保留在 Tree 上

    const int index = i + 1;
    const int parent = index + (index & -index);

    if (parent <= n) {
        tree[parent] += tree[i + 1];
    }
}
```

**原理**：`parent(i) > i`，順序遍歷可立即向上傳播

### Helper Functions

```cpp
int parent(int i) { return i + (i & -i); }
int queryPath(int i) { return i - (i & -i); }
```

### 競賽 Macros

```cpp
#define LSOne(S) ((S) & -(S))
#define parent(i) ((i) + LSOne(i))
#define queryPath(i) ((i) - LSOne(i))
```
