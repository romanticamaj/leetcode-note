# Decision Tree 評量

## 1. Confusion Matrix (混淆矩陣)

|                          | Predicted: Positive | Predicted: Negative |
| ------------------------ | ------------------- | ------------------- |
| **Actual: Positive**     | True Positive (TP)  | False Negative (FN) |
| **Actual: Negative**     | False Positive (FP) | True Negative (TN)  |

### 四種情況

| 術語   | 說明                             | 口訣           |
| ------ | -------------------------------- | -------------- |
| **TP** | 預測 Positive，實際也是 Positive | ✅ 猜有，真有  |
| **TN** | 預測 Negative，實際也是 Negative | ✅ 猜沒，真沒  |
| **FP** | 預測 Positive，實際是 Negative   | ❌ 誤報        |
| **FN** | 預測 Negative，實際是 Positive   | ❌ 漏報        |

---

## 2. Precision & Recall

### Precision (精確率)

```cpp
// 在預測為 Positive 的樣本中，有多少真的是 Positive？
double precision(int TP, int FP) {
    return 1.0 * TP / (TP + FP);
}
```

> "How many **selected** items are **relevant**?"

### Recall (召回率)

```cpp
// 在所有真正 Positive 的樣本中，有多少被成功找出？
double recall(int TP, int FN) {
    return 1.0 * TP / (TP + FN);
}
```

> "How many **relevant** items are **selected**?"

---

## 3. Accuracy (準確率)

```cpp
// 所有預測中，正確的比例
double accuracy(int TP, int TN, int FP, int FN) {
    return 1.0 * (TP + TN) / (TP + TN + FP + FN);
}
```

### ⚠️ Accuracy 的陷阱

在 **Imbalanced Dataset** 上會產生誤導：

> 100 封 email：5 封 spam、95 封正常
>
> 永遠預測 "non-spam" 的 naive classifier：
> - Accuracy = **95%** (看似很高)
> - Precision = **0%**、Recall = **0%** (實際沒用)

**結論：** Precision-Recall 比 Accuracy 更能反映 classifier 的真實能力。

---

## 4. Feature Importance (特徵重要性)

### 定義

衡量每個 input feature 對預測結果的**貢獻程度**。

### Decision Tree 的計算方式

**直觀理解：**
- 被選中作為 split feature 的比未被選中的重要
- 用 Gini Gain / Information Gain 量化貢獻
- 根據經過該 node 的 samples 比例加權

### 公式

```cpp
// 計算單一 feature 的 importance
double feature_importance(Feature& feature, DecisionTree& tree) {
    double importance = 0;
    for (Node& node : tree.nodes_using(feature)) {
        double weight = 1.0 * node.samples / tree.total_samples;
        importance += weight * node.gini_gain;
    }
    return importance;
}
```

### Normalization

```cpp
// 正規化到 [0, 1]，方便比較
double normalized_importance(Feature& f, vector<Feature>& all_features) {
    double total = 0;
    for (Feature& feat : all_features) {
        total += feature_importance(feat);
    }
    return feature_importance(f) / total;
}
```
