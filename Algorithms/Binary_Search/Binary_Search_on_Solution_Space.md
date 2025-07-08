# 演算法心法：答案空間上的二分搜尋 (Binary Search on Solution Space)

## 核心思想

當一個問題的答案具有**單調性**時，我們可以直接對由“所有可能的答案”組成的空間進行二分搜尋，來找到滿足條件的最佳解。這種技巧將問題從“在輸入數據中查找”轉化為“在答案範圍內驗證”，是解決許多優化問題的強大武器。

---

## 關鍵前提：答案的單調性 (Monotonicity)

**單調性是應用二分搜尋的絕對前提。**

- **定義：** 在這個情境下，單調性指的是可行性函數 `can(value)` 的結果，會隨著 `value` 的增減，呈現出一個**單向的、可預測的變化趨勢**。
- **為何重要：** 因為二分搜尋的威力在於**每次都能排除一半的答案空間**。如果 `can(mid)` 為 `True`，根據單調性，我們可以放心地拋棄一側，去另一側尋找更優的解。如果答案不具備單調性（例如，結果是 `[False, True, False, True]`），我們就無法判斷應該往哪一側搜索，二分搜尋的前提便不成立。

---

## 案例分析：LeetCode 875. Koko Eating Bananas

> Koko 有 `n` 堆香蕉，第 `i` 堆有 `piles[i]` 根。守衛將在 `h` 小時後返回。Koko 可以決定她吃香蕉的速度 `k`（根/小時）。她想盡可能慢地吃，但又要在守衛返回前吃完。返回她可以吃完所有香蕉的**最小**整數速度 `k`。

在這個問題中，答案 `k` 就具有完美的單調性：

- `value` 就是吃香蕉的速度 `k`。
- `can(k)` 檢查以速度 `k` 能否在 `h` 小時內吃完。
- 當速度 `k` **增加**時，吃完所有香蕉所需的時間**只會減少或不變**。
- 這導致了 `can(k)` 的結果必然是 `[False, False, ..., True, True, ...]` 的形式。

既然確認了單調性，我們就可以套用以下框架來求解。

---

## 🚀 答案空間二分搜尋框架 (5-Step Framework)

### ✦ 步驟一：問題類型判定

首先，判斷問題的本質。問題要求的是 **"最小的"** 可行速度 `k`。

> 這是一個典型的 **“求滿足條件的最小值”** 問題，因此我們應該使用 `lower_bound` 的變體來尋找答案。

### ✦ 步驟二：定義答案空間 (Solution Space)

答案空間是所有**可能的答案 `k`** 的集合。

- **最小可能速度 (left):** Koko 每小時至少要吃 `1` 根香蕉。所以 `left = 1`。
  - _重要陷阱：_ `left` 不能設為 `min(piles)`。如果 `h` 非常大，`k` 可以比任何一堆的數量都小。**邊界不要先入為主地假設。**
- **最大可能速度 (right):** 為了在最壞情況下也能吃完，最快的速度就是一次吃掉最大的一堆。所以 `right = max(piles)`。

**答案空間:** `[1, max(piles)]`

### ✦ 步驟三與四：設計判定函數並套用模板

```cpp
class Solution {
public:
    // 主函數：負責定義答案空間和啟動二分搜尋
    int solve(const vector<int>& data, ..._other_params) {
        // 步驟二：定義答案空間
        int left = min_possible_answer;
        int right = max_possible_answer;

        // 步驟四：套用 lower_bound 模板
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (can(mid, data, ..._other_params)) {
                // mid 是一個可行的解，嘗試尋找更小的解
                right = mid;
            } else {
                // mid 不可行，必須增大
                left = mid + 1;
            }
        }
        return left; // 循環結束時，left 即為最小可行解
    }

private:
    // 步驟三：設計可行性判定函數
    // 檢查給定的“答案” candidate_answer 是否滿足問題的所有約束條件
    bool can(int candidate_answer, const vector<int>& data, ..._other_params) {
        // 1. 根據 candidate_answer 和 data 計算出一個結果
        auto result = process(candidate_answer, data);

        // 2. 將該結果與問題的約束(limit)進行比較
        return result <= limit; // 或 >=, <, >，取決於問題定義
    }
};
```

**圖像化收斂過程 (`F` = 不可行, `T` = 可行):**

```
初始狀態:
F F F F F T T T T T
l                 r
          m

(can(m) 為 True, 表示 mid 可行, 答案在 [l, m] 之間)
right = mid;

第二次迭代:
F F F F F T T T T T
l         r
    m

(can(m) 為 False, 表示 mid 不可行, 答案在 [m+1, r] 之間)
left = mid + 1;

第三次迭代:
F F F F F T T T T T
      l   r
        m

(can(m) 為 Frue, 表示 mid 不可行, 答案在 [m+1, r] 之間)
left = mid + 1;

最終狀態:
F F F F F T T T T T
          lr
```

### ✦ 步驟五：返回結果

循環終止時，`left` (或 `right`) 的值就是滿足條件的最小速度 `k`。

---

## 心法總結

1. **識別單調性**：當問題要求「最小的...」或「最大的...」，且答案的可行性呈現 `[F, F, ..., T, T]` 或 `[T, T, ..., F, F]` 的單調趨勢時，就是使用答案空間二分搜尋的強烈信號。

2. **轉化問題**：核心是將一個**尋找最優解**的問題，轉化為一個**驗證給定解是否可行**的問題。這個驗證過程就是你的 `can()` 函數。

3. **定義答案邊界**：仔細思考答案的理論最小值和最大值是什麼，這將構成你的初始 `left` 和 `right`。不要想當然地從輸入數據中取值。

4. **選擇正確模板**：

   - 求**最小**可行解 -> 使用 `lower_bound` 模板 (`if (can(mid)) right = mid;`)
   - 求**最大**可行解 -> 使用 `upper_bound` 模板 (`if (can(mid)) left = mid;` 且 `mid` 計算需 `+1`, i.e., mid = left + (right - left + 1) / 2)

5. **相信邊界**：只要模板正確，循環結束時 `left` (或 `right`) 就是你想要的最佳解。
