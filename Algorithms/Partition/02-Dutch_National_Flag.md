# 荷蘭國旗問題 (Dutch National Flag / 3-Way Partition) 解題心法

把陣列**一次掃描**切成三段：`< pivot`、`== pivot`、`> pivot`。原型是 [75. Sort Colors](https://leetcode.com/problems/sort-colors/)（值只有 0 / 1 / 2），也是三向切分快排的分割步驟（見 [07-Quicksort_Advanced.md](../Sorting/Comparison_Based_Sorting/07-Quicksort_Advanced.md)）。

- **難度**：⭐⭐⭐
- **時間**：O(n)，一趟
- **空間**：O(1)，in-place

---

## 🧠 核心概念：四段 invariant

三個指標把陣列切成**四段**，不是三段：

```
 0        left       i          right        n
 ├─── 0 ───┼─── 1 ───┼─ 未處理 ─┤──── 2 ────┤
 [0, left)  [left, i)  [i, right]  (right, n)
```

| 區段 | 內容 | 說明 |
|---|---|---|
| `[0, left)` | 全是 0 | `left` = 下一個放 0 的位置 |
| `[left, i)` | 全是 1 | **已看過**，常被漏寫 |
| `[i, right]` | 未處理 | 迴圈要把它縮到空 |
| `(right, n)` | 全是 2 | `right` = 下一個放 2 的位置 |

初始時 `left = 0`、`i = 0`、`right = n - 1`：前三段是空的，整個陣列都在未處理區，invariant 成立。迴圈結束時 `i > right`，未處理區是空的，陣列就排好了。

> ⚠️ 只寫 `[0 | unsorted | 2]` 三段的話，說明不了為什麼換 0 之後 `i` **可以**前進、換 2 之後 `i` **不能**前進。兩個分支不對稱，靠的就是 `[left, i)` 這一段。

---

## 🧩 標準模板

```cpp
void sortColors(vector<int>& nums) {
    int left = 0;                  // [0, left)   是 0
    int i = 0;                     // [left, i)   是 1
    int right = nums.size() - 1;   // (right, n)  是 2；[i, right] 未處理

    while (i <= right) {           // 未處理區非空（i == right 那格也還沒看過）
        if (nums[i] == 0) {
            swap(nums[i++], nums[left++]);   // 換回來的是已看過的 1（或自己）→ i 前進
        } else if (nums[i] == 1) {
            i++;                             // 1 本來就屬於 [left, i)
        } else {
            swap(nums[i], nums[right--]);    // 換回來的是未處理的值 → i 不動
        }
    }
}
```

**口訣**：

| 看到 | 動作 | `i` | 為什麼 |
|---|---|---|---|
| 0 | 跟 `left` 換，`left++` | **前進** | `nums[left]` 在 `[left, i)` 裡，是看過的 1；或 `left == i`，換自己 |
| 1 | 不換 | **前進** | 直接併入 `[left, i)` |
| 2 | 跟 `right` 換，`right--` | **不動** | `nums[right]` 在未處理區，換回來的值還沒看過 |

> 一句話：**換 0 前進，換 2 不動；看左邊換來的是熟人，右邊換來的是生人。**

---

## ✅ 正確性論證

**Loop invariant**：每輪開始時，四段區間如上表所述。

- **初始化**：`left = i = 0`、`right = n - 1`，0 / 1 / 2 三段是空的，成立。
- **維持**：逐一檢查三個分支。
  - `nums[i] == 0`：`swap(nums[i], nums[left])` 後 `nums[left]` 是 0，`left++` 讓 0 段多一格。原本的 `nums[left]` 是 1（`left < i` 時），換到位置 `i`，`i++` 後它落在 1 段的尾端；`left == i` 時是跟自己換，兩個指標一起前進，1 段仍是空的。成立。
  - `nums[i] == 1`：`i++` 讓 1 段多一格。成立。
  - `nums[i] == 2`：換完後 `nums[right]` 是 2，`right--` 讓 2 段多一格。位置 `i` 拿到的是原本未處理區的值，所以 `i` 不動，它仍在未處理區。成立。
- **終止**：每一輪 `i++` 或 `right--` 至少發生一個，未處理區 `right - i + 1` 嚴格遞減，最後變成 0，也就是 `i == right + 1`。這時四段 invariant 等於「0 段、1 段、2 段」，陣列排好了。

**為什麼是 `i <= right` 而不是 `i < right`**：`[i, right]` 是閉區間，`i == right` 時還剩一格沒看。反例是 `[1, 0]`：用 `<` 的話，看完 `nums[0] = 1` 之後 `i = 1 == right` 就停了，0 沒被換到前面。

---

## ⚠️ 常見陷阱

1. **換 2 之後讓 `i++`**：換回來的值可能是 0 或 2，跳過就漏了。例：`[1, 2, 0]` 會得到 `[1, 0, 2]`。
2. **迴圈條件寫成 `i < n`**：`i` 會掃進已經放好的 2 段，而那一段裡 `right` 已經走過了，會把 2 換錯位置。上界是 `right`，它會一直縮。
3. **`right` 宣告成 `size_t` / `unsigned`**：`n = 1` 且元素是 2 時，`right--` 從 0 變成 `SIZE_MAX`，迴圈不會停。用 `int`。
4. **以為它是 stable**：三向切分會打亂同一段內的相對順序。題目要求保持原順序（例如 [2161. Partition Array According to Given Pivot](https://leetcode.com/problems/partition-array-according-to-given-pivot/)）時不能用，要改成多趟掃描或額外空間。

---

## ⚠️ 其他做法（不用背）

- **Counting sort 兩趟**：先數 0 / 1 / 2 各幾個，再覆寫。O(n)、O(1)，也對，但要掃兩趟；75 的 follow-up 明確要求 one pass。
- **一般排序 `sort()`**：O(n log n)，沒用到「只有三種值」這個條件，面試會被追問。
- **Insertion / selection sort**：O(n²)。n ≤ 300 會過，但這題考的不是這個。

---

## 🧩 同一套切法的變形

| 題目 | 怎麼套 |
|---|---|
| [75. Sort Colors](https://leetcode.com/problems/sort-colors/) | 原型，pivot = 1 |
| 三向切分快排 | pivot 任取，`<` / `==` / `>` 取代 0 / 1 / 2，只遞迴兩側；見 [07-Quicksort_Advanced.md](../Sorting/Comparison_Based_Sorting/07-Quicksort_Advanced.md) |
| Quickselect（215）大量重複值 | 用三向切分，第 k 小落在 `==` 段就直接回傳，避免重複值讓分割退化 |
| [283. Move Zeroes](https://leetcode.com/problems/move-zeroes/)、[905. Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/) | 退化成**兩段**：只留 `left` 和 `i`，就是 [Lomuto](01-Lomuto_Partition_Scheme.md) 的形狀（283 要保持非零元素順序，只能用同向版本） |
| [324. Wiggle Sort II](https://leetcode.com/problems/wiggle-sort-ii/) | 先 quickselect 找中位數，再對 virtual index 做三向切分 |

---

## 🗣️ 面試話術

> 「值只有三種，所以不需要一般排序，用荷蘭國旗的三向切分一趟做完。我維護四段 invariant：`[0, left)` 是 0、`[left, i)` 是 1、`[i, right]` 未處理、`(right, n)` 是 2。看到 0 跟 `left` 換，換回來的是已經看過的 1，所以 `i` 可以前進；看到 2 跟 `right` 換，換回來的還沒看過，所以 `i` 不動。每一步未處理區都會縮一格，所以是 O(n) 時間、O(1) 空間。」

---

## ✅ Checklist

- [ ] 能畫出四段 invariant，包含 `[left, i)` 的 1 段
- [ ] 能說明換 0 與換 2 時 `i` 行為不同的原因
- [ ] 迴圈條件是 `i <= right`，能舉 `[1, 0]` 當反例
- [ ] 知道它不是 stable，以及什麼時候不能用
- [ ] 能把 0 / 1 / 2 換成 `< pivot` / `== pivot` / `> pivot` 套到三向快排
