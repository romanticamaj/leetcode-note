# Height-Balanced BST 解題心法

## 🧠 核心哲學

Height-Balanced BST 的核心在於通過自動平衡維持樹高為 **O(log N)**，確保所有基本操作（搜尋、插入、刪除）在最壞情況下仍保持 **O(log N)** 時間複雜度。

## 核心概念：Tree Metrics and Balance Property

### 樹的度量定義

```cpp
// Depth of node: 從 root 到該節點的 edge 數量 (aka, distance)
// Height of node: 從該節點到 leaf 的最長路徑 edge 數量 (aka, distance)
// Height of tree: root 的 height
```

**關鍵性質**：

- 高度為 h 的 binary tree 最多包含 `2^(h+1) - 1` 個節點
- N 個節點的 binary tree，高度 h 滿足：`2^h ≤ N < 2^(h+1)`
- 因此：`h ≤ log₂(N+1) - 1`，即 **h = O(log N)**

### Height-Balanced Property

**定義**：一個 BST 是 height-balanced 若滿足：

1. **任意節點的左右子樹高度差 ≤ 1** (LeetCode 實作上關鍵定義), 或
2. **樹的總高度 = O(log N)**

**驗證方法**：

- **方法 1**: 遞歸檢查每個節點的左右子樹高度差
- **方法 2**: 計算總節點數 N 和樹高 h，驗證 `h ≈ log N`

## 為何需要 Height-Balanced BST？

### Normal BST vs Height-Balanced BST

| BST Type     | Best Height | Worst Height | Search Time         |
| ------------ | ----------- | ------------ | ------------------- |
| Normal BST   | O(log N)    | O(N) (chain) | O(N) worst          |
| Balanced BST | O(log N)    | O(log N)     | O(log N) guaranteed |

**退化場景**：普通 BST 在順序插入時退化為 linked list

```
插入 1,2,3,4,5 → 高度 = 5 (N)
   1
    \
     2
      \
       3
        \
         4
          \
           5
```

**平衡保證**：Height-balanced BST 在任意插入順序下維持 `h = O(log N)`

## 🧩 常見實現 / Common Implementations

### Self-Balancing BST 變體

- **Red-Black Tree**: 通過顏色標記和旋轉維持平衡
- **AVL Tree**: 嚴格平衡（高度差 ≤ 1）
- **Splay Tree**: 自調整，頻繁訪問節點移至 root
- **Treap**: 結合 BST 和 heap 性質

**共同特性**：

- 滿足 binary search property
- 滿足 height-balanced property
- 支援 **O(log N)** 的 search/insert/delete

## C++ 實務應用 / Practical Usage

### Set 的兩種實現

#### Tree Set (Ordered)

```cpp
#include <set>

// 基於 Red-Black Tree (height-balanced BST)
std::set<int> tree_set;

// 性質：
// - 元素自動排序
// - 所有操作 O(log N) guaranteed
// - 支援 lower_bound/upper_bound 等順序查詢
```

#### Hash Set (Unordered)

```cpp
#include <unordered_set>

// 基於 Hash Table (with BST for collision)
std::unordered_set<int> hash_set;

// 性質：
// - 元素無序
// - 平均 O(1)，最壞 O(log N) (BST fallback)
// - 當 hash collision 過多時，使用 BST 優化
```

### Hash Set 中的 BST 角色

**Hash Collision 處理演進**：

```
傳統: Chaining with Linked List → O(N) lookup
現代: Chaining with BST → O(log N) lookup
```

當 hash bucket 中元素過多（例如 > 8），自動升級為 height-balanced BST：

- **鏈表查找**: O(N)，N = bucket 中元素數
- **BST 查找**: O(log N)，顯著提升性能

## ⏱️ 複雜度分析

| Operation   | Tree Set     | Hash Set (avg) | Hash Set (worst) |
| ----------- | ------------ | -------------- | ---------------- |
| Search      | O(log N)     | O(1)           | O(log N)         |
| Insert      | O(log N)     | O(1)           | O(log N)         |
| Delete      | O(log N)     | O(1)           | O(log N)         |
| Range Query | O(log N + k) | N/A            | N/A              |

## ✅ 關鍵要點 / Key Points

- [ ] **Height = O(log N)**: 平衡的本質是維持對數樹高
- [ ] **Balance property**: 任意節點左右子樹高度差 ≤ 1
- [ ] **Performance guarantee**: O(log N) 在最壞情況下仍保證
- [ ] **C++ set = Red-Black Tree**: 自動平衡 + 有序
- [ ] **C++ unordered_set**: Hash + BST fallback（collision 優化）
- [ ] **選擇關鍵**: 需要順序用 `set`，純查找用 `unordered_set`
- [ ] **Hash collision 升級**: 從 linked list 升級到 BST 處理大量碰撞
