# Decision Tree 實作

## 1. 核心思想：Divide-and-Conquer

遞迴地將 samples 分割成 subgroups，直到不需要再分割：

1. 每個 sample 最終被分配到一個 leaf node
2. Leaf node 的 label = 該節點內 **majority samples** 的類別

---

## 2. 遞迴結構

### Base Cases (終止條件)

- Samples 都是相同 label
- 可加入額外條件來控制 tree 複雜度

### Recurrence Relation

1. 找到最佳 feature 和 split value
2. 將 samples 分成兩個 subgroups
3. 對每個 subgroup 遞迴建構 subtree

---

## 3. 演算法實作

```cpp
TreeNode build_decision_tree(samples) {
    // Base cases
    if (samples 都是同一 label ||
        depth >= max_depth ||
        samples.size() < min_samples) {
        return create_leaf_node(samples);
    }

    // 找最佳分割
    feature, value = find_best_split(samples);

    // 分割 samples
    left_samples, right_samples = split(samples, feature, value);

    // 建立 decision node
    node = create_node(feature, value);
    node.left = build_decision_tree(left_samples);
    node.right = build_decision_tree(right_samples);

    return node;
}
```

---

## 4. Stopping Conditions (停止條件)

| 條件                           | 說明               | 類型           |
| ------------------------------ | ------------------ | -------------- |
| 所有 samples 同一類別          | 無歧義，達成目標   | Natural        |
| `depth >= max_depth`           | 限制樹的深度       | Regularization |
| `samples.size() < min_samples` | 限制節點最小樣本數 | Regularization |

---

## 5. Regularization：防止 Overfitting

```
Overgrowing → Overfitting
```

- Tree 過度生長會導致 **overfitting**（過度擬合訓練資料）
- 透過 `max_depth`、`min_samples` 等參數**介入 (intervention)** 來防止
- 這種介入稱為 **Regularization (正則化)**
