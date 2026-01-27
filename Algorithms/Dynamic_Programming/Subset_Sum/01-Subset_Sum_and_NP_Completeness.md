# Subset Sum Problem 與 NP-Completeness

本文檔深入探討 Subset Sum Problem 的理論背景，解釋為什麼它是 NP-Complete 問題，以及動態規劃如何在實踐中有效解決它。

---

## 1. 問題定義

### 形式化定義 (Formal Definition)

根據 Cormen et al. (CLRS) 的定義：

> **SUBSET-SUM** = {⟨S, t⟩ : 存在子集 S' ⊆ S 使得 t = Σ(s ∈ S') s}

**輸入：**

- S: 一個有限的**正整數**集合
- t: 一個目標正整數

**問題：**
是否存在 S 的某個子集 S'，使得 S' 中所有元素的和等於 t？

### 實例 (Example)

給定 S = {1, 2, 7, 14, 49, 98, 343, 686, 2409, 2793, 16808, 17206, 117705, 117993}，t = 138457

**解：** S' = {1, 2, 7, 98, 343, 686, 2409, 17206, 117705}

驗證：1 + 2 + 7 + 98 + 343 + 686 + 2409 + 17206 + 117705 = 138457 ✓

---

## 2. NP-Completeness 背景

### 為什麼是 NP-Complete？

**定理 (Cormen 34.15):** Subset Sum Problem 是 NP-Complete。

#### 關鍵理解

1. **編碼假設 (Encoding Assumption)**
   - 標準編碼假設輸入整數以**二進制**表示
   - 這是理解時間複雜度的關鍵

2. **輸入規模的定義**
   - 在複雜度理論中，**輸入規模 = 表示輸入所需的位元數**
   - 對於整數 N，表示它需要 **O(log N)** 個位元

3. **指數增長關係**
   - 如果整數 N 的位元數是 b，則 N ≈ 2^b
   - 因此，N 的數值與它的位元數成**指數關係**

---

## 3. 動態規劃解法 (Dynamic Programming Solution)

### 3.1 為什麼 DP 看起來是多項式時間？

經典的 DP 解法時間複雜度為：

```
T(n, sum) = O(n × sum)
```

其中：

- n = 陣列長度
- sum = 所有元素的總和

這看起來像多項式時間，但**實際上不是**。

### 3.2 虛擬多項式時間 (Pseudo-polynomial Time)

#### 核心觀念

**虛擬多項式時間：** 演算法的時間複雜度對於**輸入的數值**是多項式的，但對於**輸入的位元數**是指數的。

#### 數學關係

假設整數 `sum` 需要 b 個位元表示：

```
sum ≈ 2^b
```

則 DP 的時間複雜度：

```
T = O(n × sum) = O(n × 2^b)
```

這對於 b（真正的輸入規模）來說是**指數級**的！

### 3.3 為什麼這在實踐中可行？

#### LeetCode 的約束條件 (Constraints)

以 **LC 494. Target Sum** 為例：

```
1 <= nums.length <= 20
0 <= nums[i] <= 1000
0 <= sum(nums[i]) <= 1000
-1000 <= target <= 1000
```

**分析：**

1. **sum 的範圍被限制在常數範圍**
   - sum ≤ 1000 (非常小的數值)
   - 即使是 1000，也只需要 10 個位元 (2^10 = 1024)

2. **實際複雜度**
   - 時間：O(n × sum) = O(20 × 1000) = O(20,000) → **完全可行**
   - 空間：O(sum) = O(1000) → **完全可行**

3. **如果沒有約束**
   - 假設 sum = 2^64（64 位元整數的上限）
   - 時間：O(n × 2^64) → **完全不可行**

---

## 4. 弱 NP-Complete vs 強 NP-Complete

### 分類

| 類型               | 定義                       | 虛擬多項式時間解法存在？ | 例子                     |
| ------------------ | -------------------------- | ------------------------ | ------------------------ |
| **弱 NP-Complete** | 可以在虛擬多項式時間內解決 | ✅ 是                    | Subset Sum, 0/1 Knapsack |
| **強 NP-Complete** | 不存在虛擬多項式時間解法   | ❌ 否                    | 3-SAT, Clique            |

### Subset Sum 是弱 NP-Complete

- 當輸入整數的數值被約束時，DP 解法變得實際可行
- 這也是為什麼 LeetCode 可以用 DP 解決這類問題

---

## 5. 與 0/1 Knapsack 的關係

### Subset Sum 是 Knapsack 的特例

**0/1 Knapsack:**

- 每個物品有 **weight** 和 **value**
- 目標：在重量限制 W 下，最大化價值

**Subset Sum:**

- 每個物品的 weight = value
- 目標：恰好填滿容量 t

**轉化：** Subset Sum ≡ Knapsack where weight[i] = value[i] and W = t

---

## 6. 關鍵洞察總結

### 理論 vs 實踐的差距

1. **理論上 (Computational Complexity Theory)**
   - Subset Sum 是 NP-Complete
   - 不存在真正的多項式時間演算法（除非 P = NP）

2. **實踐上 (LeetCode / 真實應用)**
   - 當輸入有界時，DP 解法完全可行
   - 時間複雜度 O(n × sum) 在 sum 很小時是高效的

### 面試時的考量點

當你看到類似問題時，應該：
  
1. **檢查 Constraints**
   - sum 的範圍是多少？
   - 如果 sum ≤ 10^4，DP 幾乎總是可行的

2. **識別問題本質**
   - 是否可以轉化為 Subset Sum？
   - 是否需要計數、判定、或優化？

3. **選擇合適的方法**
   - 有界輸入 → DP (虛擬多項式時間)
   - 無界輸入 → 考慮近似演算法或啟發式方法

---

## 7. 延伸閱讀

- **實作指南**: [`02-Implementation_Guide.md`](02-Implementation_Guide.md)
- **0/1 背包變形題**: [`../../../Checklists/Trick Practice/Knapsack_Variations_Playbook.md`](../../../Checklists/Trick%20Practice/Knapsack_Variations_Playbook.md)
- **DP 狀態設計**: [`../State_Design/01-Essentials.md`](../State_Design/01-Essentials.md)

---

## 參考文獻

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). _Introduction to Algorithms_ (3rd ed.). Section 34.5.5: The subset-sum problem.
- Wikipedia: [Subset sum problem](https://en.wikipedia.org/wiki/Subset_sum_problem)
