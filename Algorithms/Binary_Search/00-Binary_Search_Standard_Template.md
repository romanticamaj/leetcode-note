# Binary Search 標準模板

Binary Search 的唯一標準寫法：**半開區間 `[lo, hi)`、`while (lo < hi)`，找「第一個讓 predicate 成立的位置」**。

`lower_bound`、`upper_bound`、插入點、binary search on answer 全都是這一個模板換 predicate。細節與變體見 [02-Binary_Search_Comprehensive_Guide.md](02-Binary_Search_Comprehensive_Guide.md)。

---

## 1. 🧠 核心心法

> **二分搜尋不是「找 target」，是在一條單調的 `F F F T T T` 上找第一個 `T`。**

先把題目問的東西寫成一個 predicate `ok(i)`，確認它**單調**（一旦變 `T` 就一直是 `T`），剩下的全部是機械動作：

```
index:  0  1  2  3  4  5  | n
ok(i):  F  F  F  T  T  T  | (T)   ← n 是哨兵：「全部都是 F」時的答案
                  ^
                答案 = 第一個 T
```

搜尋空間是 **`[0, n]`**，因為答案可能是「沒有任何一個成立」＝ `n`（例：插入點在最後面）。

## 2. 標準模板

```cpp
// 找第一個 ok(i) == true 的 i；全部都是 false 則回傳 n
int firstTrue(int n, auto ok) {
    int lo = 0;
    int hi = n;                          // n 在搜尋空間內：「都不成立」也是合法答案

    while (lo < hi) {                    // lo == hi 時空間只剩一格，就是答案
        const int mid = lo + (hi - lo) / 2;  // 下取整 → mid < hi，永遠不會讀到 index n

        if (!ok(mid))
            lo = mid + 1;                // mid 不是答案，連同左邊一起丟掉
        else
            hi = mid;                    // mid 可能就是答案，留著
    }
    return lo;
} // 就背這個
```

具體化成 `lower_bound`（35. Search Insert Position，`ok(i) = nums[i] >= target`）：

```cpp
int searchInsert(vector<int>& nums, int target) {
    int i = 0;
    int j = nums.size();                 // n is in search space

    while (i < j) {
        const int mid = i + (j - i) / 2;

        if (nums[mid] < target)          // !ok(mid)
            i = mid + 1;
        else
            j = mid;
    }
    return i;
}
```

### 四步推導（口訣）

> **定答案 → 定空間 → 定移動 → 定終止**

| 步驟 | 問自己 | 35 的答案 |
| :--- | :--- | :--- |
| 1. 定答案 | 答案是「第一個滿足什麼」的位置？寫出 `ok(i)` | 第一個 `nums[i] >= target` |
| 2. 定空間 | 答案最小、最大可能是多少？「都不成立」算不算答案？ | `[0, n]`，`n` 算 |
| 3. 定移動 | `!ok(mid)` → `lo = mid + 1`（丟掉 mid）；`ok(mid)` → `hi = mid`（留住 mid） | `nums[mid] < target` 往右 |
| 4. 定終止 | `while (lo < hi)`，結束時 `lo == hi` 就是答案 | `return i` |

**move-right 的條件永遠是 `!ok(mid)`**——丟掉的是「確定不是答案」的那一側。寫錯 lower/upper bound 幾乎都是這一步把 predicate 和它的否定搞混。

### ⏱️ 複雜度

| Time | Space |
| :--- | :--- |
| O(log n) × `ok` 的成本 | O(1) |

## 3. 循環不變量

在每一輪迴圈開始時恆有：

- `[0, lo)` 全部是 **F**（被 `lo = mid + 1` 丟掉的都確定不是答案）
- `[hi, n]` 全部是 **T**（`n` 視為哨兵 T）
- 因此答案必在 **`[lo, hi]`** 之內

**進展**：`mid` 下取整 ⇒ `lo <= mid < hi`，所以 `lo = mid + 1` 和 `hi = mid` 都**嚴格縮小**區間，不會無窮迴圈；也因為 `mid < hi <= n`，**永遠不會讀到 `nums[n]`**。

**終止**：`lo == hi` 時，`[0, lo)` 全 F、`[lo, n]` 全 T ⇒ `lo` 就是第一個 T。

## 4. 換 predicate 就換題

| 要找 | `ok(i)` | move-right 條件 (`!ok`) | 回傳 |
| :--- | :--- | :--- | :--- |
| `lower_bound`：第一個 `>= t` | `nums[i] >= t` | `nums[mid] < t` | `lo` |
| `upper_bound`：第一個 `> t` | `nums[i] > t` | `nums[mid] <= t` | `lo` |
| `t` 是否存在 / 位置 | 同 `lower_bound` | `nums[mid] < t` | `lo < n && nums[lo] == t ? lo : -1` |
| 最後一個 `<= t` | 同 `upper_bound` | `nums[mid] <= t` | `lo - 1` |
| 最後一個 `< t` | 同 `lower_bound` | `nums[mid] < t` | `lo - 1` |
| 旋轉陣列最小值 (153) | `nums[i] <= nums.back()` | `nums[mid] > nums.back()` | `nums[lo]` |
| Binary search on answer (875) | `can(x)` | `!can(mid)` | `lo` |

「找**最後一個** X」不用另一套模板：它就是「第一個 **非 X**」的前一格，`firstTrue(...) - 1`。

Binary search on answer 只是把空間從 index `[0, n]` 換成答案值域 `[minAns, maxAns]`，模板一字不改。見 [04-Binary_Search_on_Solution_Space.md](04-Binary_Search_on_Solution_Space.md)。

## 5. ⚠️ 被淘汰的寫法（不要背）

> ⚠️ **閉區間 `[0, n-1]` + `while (left <= right)` + 三路比較**（[01-Binary_Search_Template.md](01-Binary_Search_Template.md) 的寫法）
> - `==` 就 return，有重複值時回傳的是**任意一個**符合的位置，不是第一個。
> - 插入點靠「迴圈結束時 `left` 剛好停在對的地方」的**事後解釋**，不是從定義推出來的，壓力下很難重建。
> - 三個分支、兩種收斂，無法直接推廣到 predicate / binary search on answer。

> ⚠️ **`lower_bound` 但 `right = size - 1`**
> 答案 `n` 不在搜尋空間內，`target` 比所有元素都大時永遠回傳不了 `n`。空間要從「答案可能是什麼」推，不是從「陣列有哪些 index」推。

> ⚠️ **`lo = mid`（為了找最後一個 true）**
> 搭配下取整 `mid` 會無窮迴圈：`lo = 0, hi = 1` → `mid = 0` → `lo = mid = 0`，永遠不動。硬要寫得改成上取整 `mid`，多一個要記的規則。改用「第一個非 X 的前一格」就沒有這個問題。

> ⚠️ **`mid = (lo + hi) / 2`**
> 在值域很大的 binary search on answer 會 overflow。一律 `lo + (hi - lo) / 2`。

## 6. 面試溝通策略

**推薦話術**：

> 「我把問題轉成：找第一個滿足 `nums[i] >= target` 的位置。這個條件是單調的——一旦成立，右邊都成立——所以可以二分。答案可能是 `n`（全部都比 target 小），所以搜尋空間是 `[0, n]`。每次看 `mid`：不成立就把 `mid` 和左邊丟掉，`lo = mid + 1`；成立的話 `mid` 可能就是答案，所以 `hi = mid` 留住它。`lo == hi` 時剩一格，就是答案。」

先講 predicate 和單調性，再講空間，最後講移動——面試官會看到你是**推出來的**，不是背出來的。

## 7. ✅ 總結

- **只背一個模板**：`[lo, hi)`、`while (lo < hi)`、找第一個 `ok(i)` 成立的位置
- **先寫 predicate**，確認單調；**空間從答案推**，常常要包含 `n`
- **move-right 條件 = `!ok(mid)`**；`ok(mid)` 時 `hi = mid` 留住它
- 找「最後一個」＝ 第一個非 X 的**前一格**，不另開模板

## 相關筆記

- **[02-Binary_Search_Comprehensive_Guide.md](02-Binary_Search_Comprehensive_Guide.md)** — lower/upper bound 對照、`right = size - 1` 陷阱的完整走查
- **[03-Deep_Dive_Existence_Positioning_Duplicates.md](03-Deep_Dive_Existence_Positioning_Duplicates.md)** — 存在性、定位與重複值
- **[04-Binary_Search_on_Solution_Space.md](04-Binary_Search_on_Solution_Space.md)** / **[05-Binary_Search_on_Constraint.md](05-Binary_Search_on_Constraint.md)** — 在答案值域上二分
- **[07-Inflection_Point_Binary_Search.md](07-Inflection_Point_Binary_Search.md)** — 旋轉陣列、峰值
- **[Loop_Invariant.md](../../Proof_Techniques/Loop_Invariant.md)** — 不變量證明方法
