# 演算法組合拳：前綴和 + 二分搜尋

## 核心思想：將區間問題轉化為點的查找

「前綴和 + 二分搜尋」是一種高效的組合技巧，專門用於在 `O(n log n)` 時間內，解決關於**連續子陣列 (Subarray)** 總和的查詢問題。

其威力根植於兩大基石：

1. **前綴和的代數變換：**
   前綴和的本質是將一個**區間** `[i, j]` 的和，通過公式 `sum(i, j) = prefix[j] - prefix[i-1]`，轉化為對兩個**端點** `prefix[j]` 和 `prefix[i-1]` 的代數運算。這成功地將一個「區間問題」降維成了一個「點問題」。

2. **二分搜尋的加速能力：**
   當問題被轉化為「對於每個 `prefix[j]`，去查找一個滿足特定條件的歷史 `prefix[i-1]`」時，如果前綴和陣列 `prefix` 恰好是**單調的（有序的）**，那麼這個查找過程就可以從 `O(n)` 的線性掃描，加速為 `O(log n)` 的二分搜尋。

> **連續性是關鍵：** 此技巧專為 **Subarray** 設計。因為 `prefix` 的定義基於連續累加，所以其差值也必然對應一個連續區間。這也是它無法直接應用於元素可不連續的 **Subsequence** 的根本原因。

---

## 通用問題模式與演算法

**典型問題：** 在一個陣列 `nums` 中，找到一個**連續子陣列** `nums[i..j]`，使其總和滿足特定條件（例如 `sum(i, j) >= k`）。

1. **條件轉化：**

   - `sum(i, j) >= k`
   - `prefix[j] - prefix[i-1] >= k`
   - `prefix[i-1] <= prefix[j] - k` _(將問題轉化為尋找一個滿足不等式的歷史前綴和)_

2. **演算法流程：**

   - **預處理:** `O(n)` 時間計算出前綴和陣列 `prefix`。
   - **遍歷與搜尋:**
     - 外層循環遍歷 `prefix` 陣列的每一個 `j`。
     - 對於每個 `prefix[j]`，我們需要在其歷史區間 `prefix[0...j-1]` 中，尋找是否存在一個 `prefix[i-1]` 滿足 `prefix[i-1] <= prefix[j] - k`。
     - **如果 `prefix` 陣列單調**，這個尋找過程就可以透過**二分搜尋**（例如 `std::upper_bound`）在 `O(log n)` 時間內完成。

3. **總時間複雜度:** `O(n)` (遍歷) \* `O(log n)` (搜尋) = `O(n log n)`。

---

**C++ 實用模板:**

```cpp
#include <vector>
#include <algorithm> // for std::upper_bound

// 模板解決的問題：在一個正整數陣列中，尋找滿足特定條件的、關於子陣列和的問題。
// 例如：找到和 >= k 的最短子陣列。
int solve_with_prefix_sum_bs(const std::vector<int>& nums, int k) {
    // 1. 建立前綴和陣列 (哨兵模式)
    // 使用 long long 防止溢位
    std::vector<long long> prefix(nums.size() + 1, 0);
    for (int i = 0; i < nums.size(); ++i) {
        prefix[i + 1] = prefix[i] + nums[i];
    }

    int result; // 根據問題初始化 (例如：min_len = INT_MAX)
    // ...

    // 2. 遍歷與搜尋
    // 對於每個結束點 j，尋找滿足條件的最早起始點 i
    for (int j = 1; j <= nums.size(); ++j) {
        // a. 根據 `prefix[j] - prefix[i-1] >= k` 推導查找目標
        //    即 `prefix[i-1] <= prefix[j] - k`
        long long target = prefix[j] - k;

        // b. 在 prefix[0...j-1] 中，用二分搜尋尋找 `target`
        //    std::upper_bound 找到第一個 > target 的元素。
        //    因此，其前一個位置就是滿足 `<= target` 的最右側（也是最大）的元素。
        auto it = std::upper_bound(prefix.begin(), prefix.begin() + j, target);

        // c. 根據找到的迭代器更新結果
        if (it != prefix.begin()) {
            // 找到了滿足條件的歷史前綴和
            auto target_it = it - 1;
            int i_minus_1 = std::distance(prefix.begin(), target_it);

            // 根據 i_minus_1 和 j 計算並更新結果
            // update_result(result, j, i_minus_1);
        }
    }

    return result; // 返回最終結果
}
```

## 適用性與限制

- **單調性是前提：**
  二分搜尋能夠應用的**充要條件**是 `prefix` 陣列必須具有單調性。這通常意味著原始陣列 `nums` 的所有元素應**同號**（例如，均為非負數）。如果 `nums` 中包含正負數，`prefix` 陣列會上下波動，失去單調性，此時無法直接應用二分搜尋。

- **與滑動窗口的比較：**
  對於「所有元素均為正數」的特定情況，滑動窗口 (Sliding Window) 技巧通常能提供更優的 `O(n)` 線性時間解法。然而，「前綴和 + 二分搜尋」在概念上更具普適性，它清晰地展示了如何將問題代數化，並利用數據結構（有序陣列）的特性來加速查找。
