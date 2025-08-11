# BST 核心操作與屬性

本文件概述了二元搜尋樹（BST）的基本操作，並分析其正確性和複雜度。

---

## 1. 樹中搜尋 (Tree Search)

在 BST 中搜尋一個鍵值 `k` 是一項基礎操作。

### 遞迴搜尋 (Recursive Search)

```cpp
TreeNode* search(TreeNode* root, const int k) {
  if (!root || root->val == k) {
    return root;
  }
  if (root->val > k) {
    return search(root->left, k);
  } else {
    return search(root->right, k);
  }
}
```

#### 正確性（結構歸納法）

- **基本情況 (Base Case):** 如果 `root` 是 `nullptr`，表示鍵值不在樹中，返回 `nullptr` 是正確的。如果 `root->val == k`，我們找到了節點，返回該節點是正確的。
- **歸納假設 (Inductive Hypothesis):** 假設 `search` 對於所有高度小於 `h` 的子樹都能正確運作。
- **歸納步驟 (Inductive Step):** 對於一棵高度為 `h` 的樹，如果 `root->val > k`，根據 BST 的屬性，鍵值 `k` 只可能存在於左子樹中。由於左子樹的高度小於 `h`，根據歸納假設，遞迴呼叫 `search(root->left, k)` 會正確地找到鍵值或返回 `nullptr`。如果 `root->val < k`，對稱的論證也適用。

#### 複雜度分析

- **時間複雜度:** `O(h)`，其中 `h` 是樹的高度。對於一個平衡的 BST，`h = log n`，所以複雜度是 `O(log n)`。在最壞的情況下（傾斜的樹），`h = n`，導致 `O(n)`。
- **空間複雜度:** `O(h)`，來自於遞迴呼叫堆疊的深度。

### 迭代搜尋 (Iterative Search)

```cpp
TreeNode* iterativeSearch(TreeNode* root, const int k) {
  while (root) {
    if (root->val == k) {
      return root;
    } else if (root->val > k) {
      root = root->left;
    } else {
      root = root->right;
    }
  }
  return root; // 或 return nullptr
}
```

#### 正確性（迴圈不變量）

- **不變量 (Invariant):** 在每次 `while` 迴圈迭代開始時，如果鍵值 `k` 存在於原始樹中，它必定位於以*當前* `root` 節點為根的子樹中。
- **初始化 (Initialization):** 在第一次迭代之前，`root` 是整棵樹的根，所以不變量顯然成立。
- **維持 (Maintenance):** 如果 `root->val > k`，鍵值（如果存在）必定在左子樹中。透過賦值 `root = root->left`，我們為下一次迭代維持了不變量。`root->val < k` 的情況同理。
- **終止 (Termination):** 當 `root` 為 `nullptr`（未找到鍵值）或 `root->val == k`（找到鍵值）時，迴圈終止。無論哪種情況，函數都會根據終止時的狀態返回正確的結果。

#### 複雜度分析

- **時間複雜度:** `O(h)`。
- **空間複雜度:** `O(1)`。

---

## 2. 尋找最小元素

最小元素是樹中最左側的節點。

```cpp
TreeNode* minimum(TreeNode* root) {
  while (root && root->left) {
    root = root->left;
  }
  return root;
}
```

### 正確性（迴圈不變量）

- **不變量:** 在每次迭代開始時，原始樹的最小元素位於以當前 `root` 為根的子樹中。
- **初始化:** 該不變量初始為真，因為我們從樹的根開始。
- **維持:** BST 屬性確保最小值總是在左子樹中。透過移動到 `root->left`，我們保持了不變量。
- **終止:** 當 `root->left` 為 `nullptr` 時，迴圈停止。此時，`root` 是最左側的節點，它擁有最小值。

### 複雜度分析

- **時間複雜度:** `O(h)`。
- **空間複雜度:** `O(1)`。

---

## 3. 尋找最大元素

最大元素是樹中最右側的節點。

```cpp
TreeNode* maximum(TreeNode* root) {
  while (root && root->right) {
    root = root->right;
  }
  return root;
}
```

### 正確性（迴圈不變量）

- **不變量:** 在每次迭代開始時，原始樹的最大元素位於以當前 `root` 為根的子樹中。
- **初始化:** 初始為真。
- **維持:** 最大值總是在右子樹中。移動到 `root->right` 保持了不變量。
- **終止:** 當 `root->right` 為 `nullptr` 時，迴圈停止，意味著 `root` 是最右側的節點，因此是最大值。

### 複雜度分析

- **時間複雜度:** `O(h)`。
- **空間複雜度:** `O(1)`。

---

## 4. 尋找後繼者 (Successor)

節點 `x` 的後繼者是鍵值大於 `x->val` 的所有節點中，鍵值最小的那個節點。

### 情況 1: 帶有父節點指標 (CLRS 風格)

此版本假設每個 `TreeNode` 都有一個 `parent` 指標。

```cpp
// CLRS 的虛擬碼
TREE-SUCCESSOR(x):
  if x.right != NIL
    return TREE-MINIMUM(x.right)

  y = x.p
  while y != NIL and x == y.right
    x = y
    y = y.p
  return y
```

#### 邏輯解釋

1. **如果 `x` 有右子樹:** 後繼者必定是該右子樹中的最小元素。這是因為右子樹中的所有元素都大於 `x`，而其中最小的那個將是緊隨其後的後繼者。
2. **如果 `x` 沒有右子樹:** 後繼者是 `x` 的最低祖先，且該祖先的左子節點也是 `x` 的祖先。我們透過向上遍歷樹來找到它。只要我們是從一個右子節點向上移動，我們就繼續。第一次從左子節點向上移動時，那個父節點就是後繼者。

#### 複雜度分析

- **時間複雜度:** `O(h)`。遍歷的方向要麼是向下到葉節點，要麼是向上到根節點。
- **空間複雜度:** `O(1)`。

### 情況 2: 沒有父節點指標

當沒有父節點指標可用時，搜尋必須從根節點開始。

```cpp
// 在以 root 為根的樹上尋找 p 的後繼者
TreeNode* successor(TreeNode* root, TreeNode* p) {
  if (!p) return nullptr;

  // 情況 1: p 有右子樹
  if (p->right) {
    return minimum(p->right);
  }

  // 情況 2: p 沒有右子樹
  TreeNode* succ = nullptr;
  while (root) {
    if (root->val > p->val) {
      succ = root; // 一個可能的 successor
      root = root->left;
    } else if (root->val < p->val) {
      root = root->right;
    } else { // p->val == root->val
      break;
    }
  }
  return succ;
}
```

#### 邏輯解釋

1. **如果 `p` 有右子樹:** 邏輯與之前相同；後繼者是其右子樹中的最小元素。
2. **如果 `p` 沒有右子樹:** 我們從主 `root` 向下遍歷。我們使用一個候選指標 `succ`。
   - 如果當前節點的值大於 `p` 的值，則此節點是一個潛在的後繼者。我們記錄它（`succ = root`）並向左移動以尋找一個「更好」（更小）的後繼者。
   - 如果當前節點的值小於或等於 `p` 的值，後繼者必定在右子樹中，所以我們向右移動。
   - 當路徑分歧或終止時，最後記錄的 `succ` 就是中序後繼者。

#### 複雜度分析

- **時間複雜度:** `O(h)`。
- **空間複雜度:** `O(1)`。

#### 優化版本 (單一迴圈)

這個版本將尋找後繼者的邏輯整合到一個更簡潔的迴圈中，專門處理「沒有右子樹」的情況。它從根節點開始，尋找值大於 `p->val` 的最小節點。

```cpp
TreeNode* successor_optimized(TreeNode* root, TreeNode* p) {
    TreeNode* successor = nullptr;
    while (root) {
        if (root->val > p->val) {
            // 這是一個可能的後繼者，記錄下來，並試圖在左邊找到更小的
            successor = root;
            root = root->left;
        } else {
            // 後繼者必須在右子樹中
            root = root->right;
        }
    }
    return successor;
}
```

##### 邏輯解釋

這個迴圈利用了 BST 的性質。我們從 `root` 開始遍歷：

- 如果當前 `root` 的值大於 `p->val`，那麼這個 `root` 本身就是一個潛在的後繼者。我們將 `successor` 更新為 `root`，然後向左子樹移動（`root = root->left`），試圖尋找一個鍵值仍然大於 `p->val` 但更小（因此是更好）的後繼者。
- 如果當前 `root` 的值小於或等於 `p->val`，那麼 `root` 和它的整個左子樹都不可能是後繼者。我們必須向右子樹尋找（`root = root->right`）。

這個過程持續進行，直到 `root` 變為 `nullptr`。最後被記錄的 `successor` 就是 `p` 的中序後繼者。這個方法巧妙地避免了找到節點 `p` 後再做判斷，而是將整個過程融合在一次遍歷中。
