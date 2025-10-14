# Binary Tree Canonical Forms 標準形式轉換 Playbook

## TL;DR

**核心思想**: 透過 Post-order 結構重組，將任意二元樹轉換為唯一標準形式，使同構樹具有相同結構。

**適用場景**: 同構判斷、鏡像對稱檢測、重複子樹識別

**口訣**: 「後序先整子，左大右小定標準」

---

## 🧠 核心哲學

判斷兩棵樹是否同構，與其同步遞歸比對，不如**先標準化，後比對**。

這是一種 **Problem Transformation**: 複雜的多樹同步比對 → 先標準化，後單樹比對

**關鍵洞察**: 同構的樹經標準化後會變成完全相同的結構。

---

## 核心概念：Canonical Form 定義

對每個節點，必須符合以下其中一個條件：

1. **節點沒有子節點** (葉節點)
2. **節點只有左子節點** (右為空)
3. **左子節點的值 > 右子節點的值** (雙子節點時)

這確保了：**唯一性**、**鏡像消除**、**統一方向**

---

## 🔧 核心算法：Post-Order 標準化

### 為何使用 Post-Order?

**關鍵**: 必須先將子樹轉為標準形式，再調整當前節點。

### 標準化算法

```cpp
void toCanonicalForm(TreeNode* root) {
    if (!root) return;

    // Post-order: 先遞歸處理子樹
    toCanonicalForm(root->left);
    toCanonicalForm(root->right);

    // 處理當前節點
    // Case 1: 只有右子節點 → 移到左邊
    if (!root->left && root->right) {
        root->left = root->right;
        root->right = nullptr;
        return;
    }

    // Case 2: 兩子節點 → 確保左值 > 右值
    if (root->left && root->right) {
        if (root->left->val < root->right->val) {
            swap(root->left, root->right);
        }
    }
}
```

### 處理順序

```text
1. 遞歸左子樹 → 左子樹變標準形式
2. 遞歸右子樹 → 右子樹變標準形式
3. 調整當前節點 → 整棵樹變標準形式

決策: 無子節點? → 完成
      只有右節點? → 移到左邊
      雙子節點? → 確保 left.val > right.val
```

---

## 💡 深度探討：為何必須 Post-Order？

### 技術觀察

對於**當前實作**（比較 `root->left->val` vs `root->right->val`），Pre-order 技術上也能產生正確結果：

1. `!root->left && root->right` - 只看子節點是否存在
2. `root->left->val < root->right->val` - 只看子節點的值

這兩個決策**不依賴子樹內部的標準化狀態**，父節點操作與子樹內部調整解耦。

### 為何仍建議 Post-Order？

Post-order 的必要性體現在**通用場景**。假設規則改為比較**整個子樹結構**：

```cpp
// 規則變更：比較子樹的結構簽章
if (serialize(root->left) < serialize(root->right)) {
    swap(root->left, root->right);
}
```

此時：

- **Pre-order 失敗**: 子樹未標準化，序列化基於「錯誤的中間狀態」
- **Post-order 成功**: 先標準化子樹，再序列化，保證決策正確性

### 實際應用：LeetCode 652 (Find Duplicate Subtrees)

需要序列化子樹來識別重複結構時，**必須先標準化**：

```cpp
string dfs(TreeNode* node) {
    if (!node) return "#";

    // ✅ 先標準化，再序列化 (Post-order 思維)
    toCanonicalForm(node);
    string sig = to_string(node->val) + "," +
                 dfs(node->left) + "," + dfs(node->right);

    if (++count[sig] == 2) result.push_back(node);
    return sig;
}
```

### 結論

- **當前簡化版**（比較 `val`）: Pre-order 恰好可行
- **通用場景**（比較結構）: 必須 Post-order
- **最佳實踐**: 養成 Post-order 習慣，確保演算法的**穩健性**和**可擴展性**

---

## 🧩 應用場景

### 同構判斷

```cpp
bool isIsomorphic(TreeNode* p, TreeNode* q) {
    toCanonicalForm(p);
    toCanonicalForm(q);
    return isSameTree(p, q);
}
```

### 鏡像對稱 / 重複子樹

標準化後結合序列化或結構簽章即可實現。

---

## ⚠️ 常見陷阱

### 1. 邊界條件檢查順序

必須先處理「只有右子節點」，再處理「兩個子節點」，且第一個 case 要 `return`。

### 2. In-Place 修改

標準化會修改原樹，需保留時請先複製。

---

## 🎯 關鍵設計決策

### 為何「只保留左子節點」？

確保唯一性：`1 → 2` 只有一種表示（左子），而非兩種。

### 節點值 vs 結構？

- **含值**: 判斷完全相同
- **純結構**: 判斷同構（用結構簽章，忽略值）

---

## ⏱️ 複雜度

| 操作 | 時間 | 空間 |
|------|------|------|
| 標準化 | O(n) | O(h) |
| 比對 | O(n) | O(h) |

---

## ✅ 檢查清單

- [ ] 使用 Post-order（子樹先標準化）
- [ ] 處理三種情況（無、單、雙子節點）
- [ ] 檢查順序正確（先處理只有右子節點）
- [ ] 考慮 in-place 副作用

---

**最終心法：後序先整子，規則保唯一，同構變相同。**
