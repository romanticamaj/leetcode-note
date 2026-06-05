# Decision Tree 設計決策：Splitting Criterion

## 1. 核心問題

給定 samples，如何找到最佳 split？

| 問題           | 描述                          |
| -------------- | ----------------------------- |
| Which feature? | 選擇哪個 feature 來分割       |
| Which value?   | 選擇該 feature 的哪個值來分割 |

### Good Split 的定義

> 分割後的 subgroups 越 **uniform (純淨)**，越容易分類

---

## 2. Gini Impurity

### 定義

衡量一組值的**不純度**，可解釋為：隨機抽兩個 samples（with replacement），抽到不同值的機率。

### 公式

```cpp
// P[i] = 第 i 類的機率 (該類數量 / 總數量)
double gini_impurity(vector<double>& P) {
    double sum_sq = 0;
    for (double p : P) {
        sum_sq += p * p;
    }
    return 1 - sum_sq;
}

// 從 group 計算機率分佈，再算 gini impurity
double gini(Group& group) {
    unordered_map<Label, int> count;
    for (auto& sample : group) {
        count[sample.label]++;
    }
    vector<double> P;
    for (auto& [label, cnt] : count) {
        P.push_back(1.0 * cnt / group.size());
    }
    return gini_impurity(P);
}
```

### 特性

| Gini 值 | 意義                            |
| ------- | ------------------------------- |
| **0**   | 完全純淨，所有 samples 同一類別 |
| **0.5** | 二分類時最大混亂（50/50）       |

### 範例

```cpp
// [🍎, 🍎, 🍎, 🍎] → P = {1.0}
// gini = 1 - 1.0^2 = 0 (純淨)

// [🍎, 🍎, 🍊, 🍊] → P = {0.5, 0.5}
// gini = 1 - 0.5^2 - 0.5^2 = 0.5 (最大混亂)
```

---

## 3. Gini Gain

### 公式

```cpp
// L = 原始 group, L1/L2 = 分割後的兩個 subgroups
double gini_gain(Group& L, Group& L1, Group& L2) {
    double weight1 = 1.0 * L1.size() / L.size();
    double weight2 = 1.0 * L2.size() / L.size();

    return gini(L) - gini(L1) * weight1 - gini(L2) * weight2;
}
```

> **Gini Gain = 分割前 Gini - 分割後 Weighted Gini**

### 原則

**Gini Gain 越高 → Split 越好**

---

## 4. Entropy (熵)

### 來源

來自 Information Theory，由 Shannon 提出。

### 定義

衡量狀態的**不可預測性**，也可解釋為編碼資訊所需的最小 bit 數。

### 公式

```cpp
// P[i] = 第 i 類的機率
double entropy(vector<double>& P) {
    double H = 0;
    for (double p : P) {
        if (p > 0) {  // 避免 log(0)
            H -= p * log2(p);
        }
    }
    return H;
}
```

### 特性

| Entropy | 意義                      |
| ------- | ------------------------- |
| **0**   | 完全純淨                  |
| **1**   | 二分類時最大混亂（50/50） |

---

## 5. Information Gain

### 公式

```cpp
// L = 原始 group, L1/L2 = 分割後的兩個 subgroups
double information_gain(Group& L, Group& L1, Group& L2) {
    double weight1 = 1.0 * L1.size() / L.size();
    double weight2 = 1.0 * L2.size() / L.size();

    return entropy(L) - entropy(L1) * weight1 - entropy(L2) * weight2;
}
```

> **Information Gain = 分割前 Entropy - 分割後 Weighted Entropy**

### 原則

**Information Gain 越高 → Split 越好**

---

## 6. Gini vs Entropy 比較

| 特性           | Gini Impurity    | Entropy        |
| -------------- | ---------------- | -------------- |
| **數值範圍**   | 0 ~ 0.5 (二分類) | 0 ~ 1 (二分類) |
| **計算成本**   | 較低             | 較高 (需 log)  |
| **曲線陡峭度** | 較平緩           | 較陡峭         |
| **實務選擇**   | 通常為預設值     | 對比度更明顯   |

### 結論

> 兩者**沒有本質差異**，都適合衡量 split 品質。scikit-learn 等函式庫通常預設使用 Gini（計算較快）。

---

## ⚠️ 名詞辨析

| 術語                       | 用途                   |
| -------------------------- | ---------------------- |
| **Gini Impurity**          | ML：衡量不純度         |
| **Gini Index/Coefficient** | 經濟學：衡量不平等程度 |

兩者是不同概念，勿混淆。
