# C++ STL 心法：`std::accumulate` vs. `std::reduce` 比較

在 C++ STL 的 `<numeric>` 頭文件中，`std::accumulate` 和 `std::reduce` 都用於對一個範圍內的元素進行摺疊（fold）或累加操作。儘管功能相似，但它們在設計理念、執行方式和使用場景上有著本質的區別。

---

## `std::accumulate` (自 C++98) - 循序的摺疊

`std::accumulate` 是一個經典的、嚴格**循序 (sequentially)** 執行的摺疊演算法。

### 參數設計深度解析

```cpp
template<class InputIt, class T, class BinaryOperation>
T accumulate(InputIt first, InputIt last, T init, BinaryOperation op);
```

1. **`first`, `last`**: 定義了要進行操作的元素範圍 `[first, last)`。
2. **`init` (初始值)**: 這是 `accumulate` 中最關鍵也最微妙的參數。
   - **決定累加器類型:** `init` 的類型決定了內部累加變數的類型。如果你對一個 `int` 向量求和，但傳入一個 `0LL` (long long) 作為 `init`，那麼整個累加過程都會使用 `long long`，有效防止溢位。
   - **作為計算起點:** `init` 是整個運算的起始值。計算會從 `init` 開始，然後逐一將範圍內的元素疊加上去。
   - **空範圍的返回值:** 如果 `[first, last)` 範圍為空，函式將直接返回 `init` 的值。
3. **`op` (二元運算)**: 一個可選的二元函式，定義了如何將當前累加結果與序列中的下一個元素結合。如果未提供，預設使用 `std::plus<>()`，其效果等同於 `operator+`。

### 核心特性

- **執行順序保證:** `accumulate` 保證從 `first` 到 `last` **嚴格地、從左到右**執行。`op(op(op(init, *first), *(first+1)), *(first+2))`...
- **運算要求:** 由於順序固定，二元運算 `op` **不需要**滿足交換律 (commutative) 或結合律 (associative)。例如，你可以用它來實現 `a - b - c` 這種順序敏感的操作。

### 範例

```cpp
#include <vector>
#include <numeric>
#include <iostream>
#include <string>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};

    // 基本求和
    int sum = std::accumulate(v.begin(), v.end(), 0); // 0 + 1 + 2 + 3 + 4 + 5 = 15

    // 使用 long long 防止溢位
    long long large_sum = std::accumulate(v.begin(), v.end(), 0LL);

    // 字符串拼接 (非結合律操作)
    std::vector<std::string> words = {"Hello", " ", "World", "!"};
    std::string sentence = std::accumulate(words.begin(), words.end(), std::string(""));
    // sentence = "Hello World!"

    // 計算乘積
    long long product = std::accumulate(v.begin(), v.end(), 1LL, std::multiplies<long long>());
    // 1LL * 1 * 2 * 3 * 4 * 5 = 120
    // 注意：初始值必須是 1 (乘法單位元)，且型別為 long long (1LL) 防止溢位
}
```

---

## 歸約 (Reduction) vs. 累加 (Accumulation)

在我們討論 `std::reduce` 之前，先理解「歸約」和「累加」在概念上的細微差別很重要。

- **累加 (Accumulation):** 這個詞強調一個**循序的過程**。想像你手動計算一列數字的總和：你從一個初始值（比如 0）開始，然後一個接一個地把數字加上去。順序是固定的 `((((0 + a) + b) + c) + ...)`。`std::accumulate` 正是這個過程的直接體現。

- **歸約 (Reduction):** 這個詞源於函數式編程和並行計算，它描述了一個更廣泛的概念：將一個資料集合透過某個二元運算，**最終合併成單一的值**。它不關心計算的順序。
  - **核心思想：** 只要運算滿足結合律（`(a+b)+c == a+(b+c)`），我們就可以用任何順序來計算。
  - **並行化比喻：** 想像有一大堆數字要加總。你可以把一半紙條給朋友，你和他同時計算各自那半的總和，最後再把你們兩個的結果相加。最終答案是一樣的，但速度快了一倍。這就是歸約操作可以被並行化的原因。

`std::reduce` 的命名正是在強調它執行的是一個可並行、不保證順序的歸約操作，而不是一個嚴格循序的累加。

## `std::reduce` (自 C++17) - 可並行的歸約

`std::reduce` 是 `accumulate` 的現代化、可並行版本，它實現了上述的「歸約」思想，旨在利用多核心處理器的優勢。

### 核心特性與差異

1. **支援並行執行:**

   - `reduce` 有一個額外的多載，可以接受**執行策略 (Execution Policy)**，如 `std::execution::par`，允許演算法並行執行。這是它與 `accumulate` 最本質的區別。

2. **對運算的要求更嚴格:**

   - 為了能夠並行計算（即以任意順序組合元素），傳遞給 `reduce` 的二元運算**必須同時滿足交換律和結合律**。例如，加法和乘法滿足，但減法不滿足。

3. **`init` 參數的行為不同:**
   - **`accumulate`**: `init` **總是**被用作計算的起始點。
   - **`reduce` (不帶 `init` 的版本)**: 如果範圍不為空，會使用**第一個元素**作為初始值。
   - **`reduce` (帶 `init` 的版本)**: `init` 的角色更像是當並行計算的多個子結果需要合併時的“單位元素”。

### 範例

```cpp
#include <vector>
#include <numeric>
#include <iostream>
#include <execution> // 需要 C++17

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};

    // 並行求和
    int sum = std::reduce(std::execution::par, v.begin(), v.end());
    // 計算順序不保證，但結果正確 (15)
}
```

---

## 總結比較

| 特性            | `std::accumulate`    | `std::reduce`                                      |
| :-------------- | :------------------- | :------------------------------------------------- |
| **C++ 標準**    | C++98                | C++17                                              |
| **執行方式**    | **嚴格循序**         | **可並行** (需指定執行策略)                        |
| **執行順序**    | **保證**從左到右     | **不保證**                                         |
| **運算要求**    | 無特殊要求           | **必須**滿足交換律和結合律                         |
| **預設運算**    | `operator+`          | `std::plus<>()` (效果同 `operator+`)               |
| **`init` 行為** | 總是作為計算的起始值 | 僅在範圍為空時作為返回值（或作為並行計算的單位元） |
| **標頭檔**      | `<numeric>`          | `<numeric>`                                        |

## 何時使用？

- **使用 `std::accumulate`:**

  - 當你的運算**順序敏感**時（如減法、字符串拼接）。
  - 當你需要與舊版 C++ 標準相容時。
  - 當數據量不大，並行化帶來的開銷可能超過收益時。

- **使用 `std::reduce`:**
  - 當處理大量數據且運算滿足交換律和結合律時（如大規模的數值加總），希望利用多核心加速。
  - 當你希望程式碼意圖更清晰地表達一個“歸約”而非“循序累加”操作時。
