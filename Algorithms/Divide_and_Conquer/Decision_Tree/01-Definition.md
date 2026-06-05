# Decision Tree 定義

## 1. 用途

Decision Tree 用於 **Supervised Machine Learning** 中的：

- **Classification** (分類)
- **Regression** (迴歸)

---

## 2. 結構

Decision Tree 是一種特殊的 **Binary Tree**，包含兩種節點：

| 節點類型                     | 說明                              |
| ---------------------------- | --------------------------------- |
| **Leaf Node (葉節點)**       | 沒有 child node，代表最終分類結果 |
| **Decision Node (決策節點)** | Non-leaf node，包含分支條件       |

---

## 3. Branching Rule (分支規則)

```cpp
if (condition == true) {
    // go to left child
} else {
    // go to right child
}
```

### Condition 的形式

| Attribute 類型           | 條件形式                    | 範例                   |
| ------------------------ | --------------------------- | ---------------------- |
| **Numerical (數值型)**   | `attribute ≤ C`             | `height ≤ 1.7`         |
| **Categorical (類別型)** | `attribute ∈ {C1, C2, ...}` | `color ∈ {red, green}` |

---

## 4. Model Inference (模型推論)

將 Decision Tree 應用於分類 sample 的過程：

1. 從 root 開始，根據 branching rule 向下走
2. 到達 leaf node 後，輸出該節點的 label

---

## 5. Interpretability (可解釋性)

沿著路徑的條件組合形成 **規則鏈 (chain of rules)**，解釋決策過程。

**優勢：** 相較於 Neural Network 等 blackbox models，Decision Tree 的決策邏輯對人類是可理解的。

> 範例：`height ≤ 1.7 AND weight > 60 → Class A`
