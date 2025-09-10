# 一次遍歷找出最小值與次小值的技巧

在許多演算法問題中，我們需要在一個集合中找出最小值（min）和次小值（second min）。一個直觀的方法是先排序（O(N log N)）或遍歷兩次，但存在一個更優雅、更高效的技巧，只需**一次遍歷**即可完成。

---

## 核心思想

我們維護兩個變數，`min_val` 和 `second_min_val`，並在遍歷過程中動態更新它們。

1. **初始化**: 將 `min_val` 和 `second_min_val` 都初始化為一個極大值（例如 `INT_MAX`）。
2. **遍歷**: 對於集合中的每一個元素 `x`：
   - **情況一：`x` 比 `min_val` 還小**
     - 這表示我們找到了一個新的最小值。
     - 原來的 `min_val` 就變成了現在的 `second_min_val`。
     - 新的 `x` 成為新的 `min_val`。
     - 更新順序很重要：先更新 `second_min_val`，再更新 `min_val`。
   - **情況二：`x` 介於 `min_val` 和 `second_min_val` 之間**
     - 這表示我們找到了一個比當前 `second_min_val` 更小的次小值。
     - 更新 `second_min_val` 為 `x`。
   - **情況三：`x` 大於等於 `second_min_val`**
     - 不做任何事。

---

## C++ 實作範例

```cpp
#include <iostream>
#include <vector>
#include <limits>

void findMinAndSecondMin(const std::vector<int>& nums) {
    int min_val = std::numeric_limits<int>::max();
    int second_min_val = std::numeric_limits<int>::max();

    if (nums.size() < 2) {
        std::cout << "Cannot find min and second min in a list with less than 2 elements." << std::endl;
        return;
    }

    for (int x : nums) {
        if (x < min_val) {
            second_min_val = min_val; // 原本的 min 變成 second min
            min_val = x;          // 新的數成為 min
        } else if (x < second_min_val && x != min_val) { // x > min_val 且 x < second_min_val
            second_min_val = x;
        }
    }

    if (second_min_val == std::numeric_limits<int>::max()) {
        std::cout << "No distinct second minimum value found." << std::endl;
    } else {
        std::cout << "Minimum value: " << min_val << std::endl;
        std::cout << "Second minimum value: " << second_min_val << std::endl;
    }
}

int main() {
    std::vector<int> data = {4, 5, 1, 2, 8, 3};
    findMinAndSecondMin(data); // Output: Minimum value: 1, Second minimum value: 2

    std::vector<int> data_with_duplicates = {4, 1, 1, 2, 8, 3};
    findMinAndSecondMin(data_with_duplicates); // Output: Minimum value: 1, Second minimum value: 2

    std::vector<int> all_same = {5, 5, 5, 5};
    findMinAndSecondMin(all_same); // Output: No distinct second minimum value found.
    return 0;
}
```

### 關鍵細節

- **`x != min_val`**: 在更新 `second_min_val` 時，這個條件是為了處理重複元素的情況。如果沒有這個條件，當 `min_val` 重複出現時，`second_min_val` 會被錯誤地更新為 `min_val`。
- **初始化**: 使用 `numeric_limits<int>::max()` 可以確保第一個元素能正確地被設定為 `min_val`。

這個技巧的時間複雜度為 **O(N)**，空間複雜度為 **O(1)**，是解決此類問題的最佳方法。
