# Augmented BST for Order Statistics 心法

## 🧠 核心哲學

當需要**動態的 rank query**（第 k 大/小）並支援**插入操作**時，透過在 BST node 上附加 subtree metadata 來實現 O(h) 的 rank-based navigation，取代 O(n) 的 traversal。

## 核心概念：Order Statistic Tree

**Order Statistic Tree (OST)** 是一種 BST，每個 node 儲存其 **subtree size**，實現：

- 查詢第 k 大/小：O(h)
- 插入/刪除並更新 metadata：O(h)
- 查詢元素 rank：O(h)

**Rank 定義**：元素在排序序列中的位置（1-indexed）。

- rank = 1 表示最大元素
- rank = 2 表示第二大元素
- 範例：集合 {3, 7, 1, 9, 5} 中，9 的 rank = 1，7 的 rank = 2，5 的 rank = 3

**關鍵洞察**：在 BST 中，如果 node 的 right subtree 有 `m` 個節點，則該 node 是第 **(m+1) 大**的元素（rank = m+1）。

**狀態轉移機制**：透過比較 `k` 與 `rightSize + 1`（或 `val` 與 `root->val`）來 **trim 掉不需要的 subtree**，然後將狀態轉移到目標子樹，同時調整參數。這種 subtree pruning 將搜尋空間從 O(n) 降至 O(h)。

```cpp
struct Node {
    int val;
    int size;  // Total subtree size (including self)
    Node *left, *right;

    Node(int v) : val(v), size(1), left(nullptr), right(nullptr) {}
};
```

## 通用模板

```cpp
// Insert with size update
Node* insert(Node* root, int val) {
    if (!root) return new Node(val);

    if (val <= root->val)
        root->left = insert(root->left, val);
    else
        root->right = insert(root->right, val);

    root->size++;  // 插入路徑上每個 node 的 subtree size 都增加 1
    return root;
}

int getSize(Node* node) {
    return node ? node->size : 0;
}

// Find kth largest (1-indexed: 1 = largest)
// Given rank → find value
int findKthLargest(Node* root, int k) {
    int rightSize = getSize(root->right);

    if (k == rightSize + 1)
        return root->val;  // 當前 node 是第 k 大

    if (k < rightSize + 1)
        return findKthLargest(root->right, k);  // Trim left subtree
    else
        return findKthLargest(root->left, k - (rightSize + 1));  // Trim right subtree, adjust k
}

// Get rank of value (1-indexed: 1 = largest)
// Given value → find rank
int getRank(Node* root, int val) {
    if (!root) return -1;  // Not found

    int rightSize = getSize(root->right);

    if (val == root->val)
        return rightSize + 1;  // 當前 node 的 rank

    if (val > root->val)
        return getRank(root->right, val);  // Trim left subtree
    else
        return getRank(root->left, val) + rightSize + 1;  // Trim right subtree, add offset
}
```

## 適用場景

| 情境 | 為何用 OST？ | 替代方案 |
|------|-------------|---------|
| **動態 kth largest stream** | O(h) insert + query | Min-heap: O(k) 空間但 O(log k) |
| **元素 rank 查詢** | O(h) lookup | Sort: O(n log n) |
| **Range rank queries** | O(h) per query | Sorted array: O(n) inserts |

**何時不該用**：如果只需要 **kth largest**（不需 rank queries），用 size 為 k 的 min-heap 更簡單且空間效率更高（O(k) vs O(n)）。

## ⏱️ 複雜度分析

| 操作 | 時間 | 空間 | 備註 |
|-----|------|------|------|
| Insert | O(h) | O(n) | h = tree height (worst O(n)) |
| Find kth | O(h) | O(1) | 單一路徑 traversal |
| Get rank | O(h) | O(1) | 單一路徑 traversal |
| With balancing | O(log n) | O(n) | AVL/Red-Black tree |

## ✅ 關鍵要點

- [ ] **Rank 定義**：元素在排序序列中的位置（1-indexed），rank = 1 是最大元素
- [ ] **Augmentation invariant**：每次 insert/delete 路徑上都要更新 `size`
- [ ] **Rank 公式**：有 `m` 個 right children 的 node 是第 **(m+1) 大**
- [ ] **對偶操作**：
  - `findKthLargest(k)`: given rank → find value
  - `getRank(val)`: given value → find rank
- [ ] **Navigation 邏輯**：
  - `k == rightSize + 1` 或 `val == root->val` → 找到目標
  - `k <= rightSize` 或 `val > root->val` → 往 right 走
  - `k > rightSize + 1` 或 `val < root->val` → 往 left 走，調整參數
- [ ] **Helper function**：總是用 `getSize(node)` 安全處理 nullptr
- [ ] **Balancing**：若要保證 O(log n)，需使用 self-balancing BST (AVL/RB-tree)

## 相關題目

- LeetCode 230 (Kth Smallest Element in BST) - 更簡單，不需 augmentation (會用 Followup 來考)
- LeetCode 703 (Kth Largest Element in Stream)
- CLRS Chapter 14: Augmenting Data Structures
