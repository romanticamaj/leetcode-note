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

---

## 4. 尋找後繼者 (Successor)

### 定義

**CLRS 定義:**

> If all keys are distinct, the successor of a node x is the node with the smallest key greater than x.key. The structure of a binary search tree allows us to determine the successor of a node without ever comparing keys.
>
> Even if keys are not distinct, we define the successor and predecessor of any node x as the node returned by calls made to TREE-SUCCESSOR(x).

**LeetCode 定義:**

> The successor of a node p is the node with the smallest key greater than p.val.

因為 successor 定義為「比目標值大的節點中最小的那個」，這恰好符合 **Upper Bound** 的定義，所以可以用 Binary Search 尋找 upper bound 的方式來解決（見情況 2）。

### 情況 1: 帶有父節點指標 (CLRS 風格 - Structural Approach)

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

#### 設計核心：Leverage BST Structure

**關鍵洞察：此方法完全基於 BST 的結構特性，不需要比較鍵值。**

CLRS 強調："The structure of a binary search tree allows us to determine the successor of a node without ever comparing keys." 這個演算法利用 BST 的拓撲結構（父子關係和左右子樹位置），而非鍵值比較來找到後繼者。

此演算法的核心設計策略可以分解為以下三個關鍵點：

1. **用右子樹是否存在來分類:**

   - 這是整個演算法的主要分支條件
   - `if x.right != NIL` 將問題分為兩個完全不同的情況

2. **情況 A - 右子樹存在:**

   - 後繼者必然在右子樹中
   - 具體是右子樹的最小值（最左節點）
   - 這是因為右子樹中所有值都大於 `x`，而其中最小的就是「緊接著」的下一個

3. **情況 B - 右子樹不存在:**
   - 後繼者是**第一個左子樹轉折的節點**
   - 也就是說，我們向上遍歷，直到找到一個祖先節點 `y`，使得我們是從 `y` 的**左子樹**上來的
   - 換句話說：找到第一個「當前節點是其左子節點」的祖先
   - 如果一直都是從右子節點向上走（`x == y.right`），說明還沒找到轉折點，繼續向上
   - 第一次從左子節點向上走時，該父節點就是後繼者

#### 邏輯解釋

1. **如果 `x` 有右子樹:** 後繼者必定是該右子樹中的最小元素。這是因為右子樹中的所有元素都大於 `x`，而其中最小的那個將是緊隨其後的後繼者。
2. **如果 `x` 沒有右子樹:** 後繼者是 `x` 的最低祖先，且該祖先的左子節點也是 `x` 的祖先。我們透過向上遍歷樹來找到它。只要我們是從一個右子節點向上移動，我們就繼續。```第一次從左子節點向上移動時，那個父節點就是後繼者。```

### 情況 2: 沒有父節點指標 - Binary Search Upper Bound

**⚠️ 重要前提：此方法僅適用於 LeetCode 定義的 successor**

因為 LeetCode 定義 successor 為「比目標值大的節點中最小的那個」，這正是 **Binary Search Upper Bound** 的定義。所以我們可以直接用 Binary Search 的模板來解決。

**此方法不適用於 inorder traversal 定義的 successor（當有重複鍵值時）:**

```
反例：
     1
    / \
   1   2

若將 successor 定義為「inorder traversal 的下一個節點」：
- 左邊 1 的 inorder successor 應該是 root 1
- 但 Binary Search Upper Bound 會找到 2（第一個 > 1 的節點）

LeetCode 定義下（smallest key > p.val）：
- 左邊 1 的 successor 是 2 ✓ (正確，因為 2 > 1)
```

**結論：**

- Binary Search Upper Bound = LeetCode 定義（基於值比較）
- Inorder Successor with parent pointers = CLRS 定義（基於位置，適用於重複鍵值）

```cpp
TreeNode* successor(TreeNode* root, TreeNode* p) {
    TreeNode* successor = nullptr;

    while (root) {
        if (root->val > p->val) {
            // 找到一個比 p->val 大的候選
            // 記錄下來，並向左尋找更小的 upper bound
            successor = root;
            root = root->left;
        } else {
            // root->val <= p->val
            // upper bound 一定在右子樹
            root = root->right;
        }
    }

    return successor;
}
```

#### 為什麼這個方法正確？

這個演算法本質上是在 BST 上執行 **Binary Search 尋找 Upper Bound**：

1. **Upper Bound 定義:** 第一個嚴格大於目標值的元素
2. **Successor 定義:** 比 `p->val` 大的節點中最小的那個


#### 與情況 1 的關聯

**注意：兩種方法在有重複鍵值時會有不同行為**

- **情況 1 (Structural):**
  - 基於樹的拓撲位置（parent pointers）
  - 找「inorder traversal 的下一個節點」
  - 適用於 CLRS 定義（即使有重複鍵值）
- **情況 2 (Value-based):**
  - 基於鍵值比較（Binary Search Upper Bound）
  - 找「第一個嚴格大於目標值的節點」
  - 適用於 LeetCode 定義（假設沒有重複鍵值，或用值定義 successor）

**當所有鍵值唯一時**，兩種方法會找到相同的節點：

- 情況 1：利用父指標和拓撲結構找到「第一個左轉的祖先」
- 情況 2：利用 Binary Search 找到「第一個大於目標值的節點」

**當有重複鍵值時**，使用哪種方法取決於問題的定義：

- 需要「位置上的下一個」→ 使用情況 1（需要 parent pointers）
- 需要「值上的下一個」→ 使用情況 2（Binary Search Upper Bound）
