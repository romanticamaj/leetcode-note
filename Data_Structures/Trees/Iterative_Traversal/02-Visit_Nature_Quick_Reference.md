# Visit Nature 快速參考 / Quick Reference

## 核心概念：每個節點的訪問次數

| Traversal     | Visits | 1st Visit                    | 2nd Visit            |
| ------------- | ------ | ---------------------------- | -------------------- |
| **Preorder**  | 1      | Process + push children      | N/A                  |
| **Inorder**   | 2      | Push self + go left          | Process + go right   |
| **Postorder** | 2      | Push self + explore children | Process with results |

**關鍵洞察**：

- Preorder = **見面即處理** (1-pass)
- Inorder/Postorder = **需要回訪** (2-pass)

---

## 實作模式：State Flag (明確標記)

用 `pair<TreeNode*, bool>` 明確追蹤每個節點是第幾次訪問：

```cpp
stack<pair<TreeNode*, bool>> stk;  // (node, isFirstVisit)

while (!stk.empty()) {
    auto [node, first] = stk.top(); stk.pop();
    if (!node) continue;

    if (first) {
        // 1st visit: prepare children (order matters!)
    } else {
        // 2nd visit: process
    }
}
```

> 💡 **另一種實作方式**：參見 [`03-Current_Pointer_Implementations.md`](03-Current_Pointer_Implementations.md) 的 Current Pointer 模式（隱式狀態追蹤）

---

## 實作範例

### Preorder (1 Visit - Process First)

```cpp
stk.push(root);
while (!stk.empty()) {
    auto node = stk.top(); stk.pop();
    process(node);  // Only visit
    if (node->right) stk.push(node->right);  // LIFO order
    if (node->left) stk.push(node->left);
}
```

### Inorder (2 Visits - State Flag)

```cpp
stk.push({root, true});
while (!stk.empty()) {
    auto [node, first] = stk.top(); stk.pop();
    if (!node) continue;

    if (first) {
        stk.push({node->right, true});  // Later
        stk.push({node, false});        // 2nd visit
        stk.push({node->left, true});   // First
    } else {
        process(node);
    }
}
```

### Postorder (2 Visits - State Flag)

```cpp
stk.push({root, true});
while (!stk.empty()) {
    auto [node, first] = stk.top(); stk.pop();
    if (!node) continue;

    if (first) {
        stk.push({node, false});        // 2nd visit
        stk.push({node->right, true});
        stk.push({node->left, true});
    } else {
        process(node);  // Children done
    }
}
```

---

## ✅ 記憶要點

- [ ] **Visit count 決定複雜度**：1 visit = 簡單；2 visits = 需要狀態追蹤
- [ ] **State tracking 兩種方式**：顯式 flag OR 隱式 pointer
- [ ] **Push 順序很重要**：LIFO 特性，反向推入
- [ ] **完整實作細節**：參見 `03-Current_Pointer_Implementations.md`
