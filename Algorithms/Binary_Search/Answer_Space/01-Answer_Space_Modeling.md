# 答案空間建模（Binary Search on Answer / Value / Solution Space）

## 核心思想

當一個問題的答案具有**單調性**時，我們可以直接對由"所有可能的答案"組成的空間進行二分搜尋，來找到滿足條件的最佳解。

這種技巧將問題從

> 在輸入數據中查找

轉化為

> 在答案範圍內驗證

是解決許多優化問題的強大武器。

## 關鍵前提：答案的單調性 (Monotonicity)

**單調性是應用二分搜尋的絕對前提。**

- **定義：** 在這個情境下，單調性指的是可行性函數 `can(value)` 的結果，會隨著 `value` 的增減，呈現出一個**單向的、可預測的變化趨勢**。
- **為何重要：** 因為二分搜尋的威力在於**每次都能排除一半的答案空間**。如果 `can(mid)` 為 `True`，根據單調性，我們可以放心地拋棄一側，去另一側尋找更優的解。如果答案不具備單調性（例如，結果是 `[False, True, False, True]`），我們就無法判斷應該往哪一側搜索，二分搜尋的前提便不成立。

## 案例分析：LeetCode 875. Koko Eating Bananas

> Koko 有 `n` 堆香蕉，第 `i` 堆有 `piles[i]` 根。守衛將在 `h` 小時後返回。Koko 可以決定她吃香蕉的速度 `k`（根/小時）。她想盡可能慢地吃，但又要在守衛返回前吃完。返回她可以吃完所有香蕉的**最小**整數速度 `k`。

在這個問題中，答案 `k` 就具有完美的單調性：

- `value` 就是吃香蕉的速度 `k`。
- `can(k)` 檢查以速度 `k` 能否在 `h` 小時內吃完。
- 當速度 `k` **增加**時，吃完所有香蕉所需的時間**只會減少或不變**。
- 這導致了 `can(k)` 的結果必然是 `[False, False, ..., True, True, ...]` 的形式。

既然確認了單調性，我們就可以套用以下框架來求解。

## 🚀 答案空間二分搜尋框架 (5-Step Framework)

### 1. 問題類型判定

首先，判斷問題的本質。問題要求的是 **"最小的"** 可行速度 `k`。

> 這是 **「找第一個可行值」的邊界搜尋**，與 lower bound 的 first-true 思路相同。是否需要邊界搜尋取決於 predicate 的轉折，**與候選值是否重複無關**；不同速度雖是不同數值，仍可能有一整段都回傳 true。

標準寫法見 [唯一標準模板](../00-Binary_Search_Standard_Template.md)。本文保留閉區間寫法作邊界推導對照：`FFFFTTTT` 找第一個 T；`TTTTFFFF` 找最後一個 T。兩者都正確，不能混用各自的更新與終止規則。

### 2. 定義答案空間 (Solution Space)

答案空間是所有**可能的答案 `k`** 的集合。

- **最小可能速度 (left):** Koko 每小時至少要吃 `1` 根香蕉。所以 `left = 1`。
  - _重要陷阱：_ `left` 不能設為 `min(piles)`。如果 `h` 非常大，`k` 可以比任何一堆的數量都小。**邊界不要先入為主地假設。**
- **最大可能速度 (right):** 為了在最壞情況下也能吃完，最快的速度就是一次吃掉最大的一堆。所以 `right = max(piles)`。

**答案空間:** `[1, max(piles)]`

### 3. 設計判定函數與套用模板

以下為閉區間對照用的偽代碼。初始範圍 `[L,R]`；第一個 T 不存在時回傳 `R+1`，最後一個 T 不存在時回傳 `L-1`。須先確認題目保證有解，或另行處理此哨兵值，且型別能容納邊界更新。

```cpp
class Solution {
public:
    // 主函數：負責定義答案空間和啟動二分搜尋
    int solve(const vector<int>& data, ..._other_params) {
        // 步驟二：定義答案空間
        int left = min_possible_answer;
        int right = max_possible_answer;

        // 步驟三：套用二分搜尋模板（尋找最小可行解）
        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (can(mid, data, ..._other_params)) {
                // mid 是一個可行的解，但我們要找最小的可行解
                // 所以縮小右邊界，在左半部繼續尋找更小的可行解
                right = mid - 1;
            } else {
                // mid 不可行，必須增大
                left = mid + 1;
            }
        }

        return left; // 循環結束時，left 即為最小可行解
    }

    // 尋找最大可行解的變體
    int solve_for_maximum(const vector<int>& data, ..._other_params) {
        // 步驟二：定義答案空間
        int left = min_possible_answer;
        int right = max_possible_answer;

        // 步驟三：套用二分搜尋模板（尋找最大可行解）
        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (can(mid, data, ..._other_params)) {
                // mid 是一個可行的解，但我們要找最大的可行解
                // 所以增加左邊界，在右半部繼續尋找更大的可行解
                left = mid + 1;
            } else {
                // mid 不可行，必須減小
                right = mid - 1;
            }
        }

        return right; // 循環結束時，right 即為最大可行解
    }

private:
    // 步驟三：設計可行性判定函數
    // 檢查給定的"答案" candidate_answer 是否滿足問題的所有約束條件
    bool can(int candidate_answer, const vector<int>& data, ..._other_params) {
        // 1. 根據 candidate_answer 和 data 計算出一個結果
        auto result = process(candidate_answer, data);

        // 2. 將該結果與問題的約束(limit)進行比較
        return result <= limit; // 或 >=, <, >，取決於問題定義
    }
};
```

### 4. 圖像化收斂過程

```
尋找最小可行解的收斂過程 (`F` = 不可行, `T` = 可行):

初始狀態:
F F F F F T T T T T
l                 r
        m

(can(m) 為 False，mid 及左側皆不可行；未判定候選縮至 [m+1, r])
left = mid + 1;

第二次迭代:
F F F F F T T T T T
          l       r
              m

(can(m) 為 True，mid 可能就是答案；只繼續檢查 [l, m-1] 是否有更小的可行值)
right = mid - 1;

第三次迭代:
F F F F F T T T T T
          l r
          m

(can(m) 為 True，mid 可能就是答案；只繼續檢查 [l, m-1] 是否有更小的可行值)
right = mid - 1;

最終狀態:
F F F F F T T T T T
        r l

此時 left 指向第一個可行解（第一個 T），即為答案。

尋找最大可行解的收斂過程:

初始狀態:
T T T T T F F F F F
l                 r
        m

(can(m) 為 True，mid 可能就是答案；只繼續檢查 [m+1, r] 是否有更大的可行值)
left = mid + 1;

第二次迭代:
T T T T T F F F F F
          l       r
              m

(can(m) 為 False，mid 及右側皆不可行；未判定候選縮至 [l, m-1])
right = mid - 1;

第三次迭代:
T T T T T F F F F F
          l r
          m

(can(m) 為 False，mid 及右側皆不可行；未判定候選縮至 [l, m-1])
right = mid - 1;

最終狀態:
T T T T T F F F F F
        r l

此時 right 指向最後一個可行解（最後一個 T），即為答案。
```

### 5. 返回結果與原理解析

現在讓我們深入理解為什麼二分搜尋能夠找到精確的邊界點，以及為什麼我們在不同情況下返回不同的指針：

#### 搜尋空間的單調性模式

在二分搜尋的答案空間中，單調性模式決定了我們如何設計算法和返回結果：

**尋找最小可行解**：

- 搜尋空間通常呈現 `F F F F F T T T T T` 的模式
- 所有**小於**最小可行解的值都**不可行**
- 所有**大於等於**最小可行解的值都**可行**
- 我們要找的是第一個 `T`（可行值）
- 使用模板：當 `can(mid)` 為 `true` 時，執行 `right = mid - 1` (往左逼近)
- 返回 `left`

**尋找最大可行解**：

- 搜尋空間通常呈現 `T T T T T F F F F F` 的模式
- 所有**小於等於**最大可行解的值都**可行**
- 所有**大於**最大可行解的值都**不可行**
- 我們要找的是最後一個 `T`（可行值）
- 使用模板：當 `can(mid)` 為 `true` 時，執行 `left = mid + 1` (往右逼近)
- 返回 `right`

這種單調性是二分搜尋能夠有效工作的基礎，也決定了我們在循環結束時應該返回 `left` 還是 `right`。

#### 為什麼尋找最小值時返回 `left`，而尋找最大值時返回 `right`？

用不變量推導即可，不需要假設最後一定先出現 `left == right`：

| 判定排列 | 每輪開始時已確定的區域（限原範圍 `[L,R]`） | 結束時回傳 |
| :--- | :--- | :--- |
| `FFFFTTTT` | `[L,left)` 全 F；`(right,R]` 全 T | `left`：第一個 T，或無解哨兵 `R+1` |
| `TTTTFFFF` | `[L,left)` 全 T；`(right,R]` 全 F | `right`：最後一個 T，或無解哨兵 `L-1` |

閉區間 `[left,right]` 是**尚未判定的候選**，答案本身可能已被移出這個區間；其位置仍由兩側不變量保留。每次排除 mid，區間嚴格縮小，終止時 **`left == right + 1`**，沒有任何未判定候選。

例如 LC 222 的 `exist(index)` 為 `TTTTFFFF`，因此 `return right` 與 `return left - 1` 等價。若最後一層全存在，`left` 會走到初始上界之外，`right` 仍是最大的存在編號。

若要沿用標準 first-true 模板，將 `TTTTFFFF` 的 predicate 取反成 `FFFFTTTT`，找第一個 F 的位置再減一即可；兩種模板的終止條件不可互換。

## 心法總結

1. **識別單調性**：

   - 當問題要求「最小的...」或「最大的...」
   - 且答案的可行性呈現單調趨勢（`[F, F, ..., T, T]` 或 `[T, T, ..., F, F]`）
   - 這就是使用答案空間二分搜尋的強烈信號

2. **轉化問題**：

   - 核心是將**尋找最優解**的問題，轉化為**驗證給定解是否可行**的問題
   - 這個驗證過程就是你的 `can()` 函數

3. **定義答案邊界**：

   - 仔細思考答案的理論最小值和最大值
   - 這將構成你的初始 `left` 和 `right`
   - 不要想當然地從輸入數據中取值

4. **選擇正確模板**：

   - 求**最小**可行解：
     - 使用 `while (left <= right)` 模板
     - 當 `can(mid)` 為 `true` 時，執行 `right = mid - 1`
     - 返回 `left`
   - 求**最大**可行解：
     - 使用 `while (left <= right)` 模板
     - 當 `can(mid)` 為 `true` 時，執行 `left = mid + 1`
     - 返回 `right`

5. **相信邊界**：
   - 只要模板正確，循環結束時的邊界就是你想要的最佳解
   - 尋找最小值時返回 `left`，尋找最大值時返回 `right`
