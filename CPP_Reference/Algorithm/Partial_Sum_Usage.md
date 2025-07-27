# `std::partial_sum`: 高效計算前綴和

`std::partial_sum` 是 C++ `<numeric>` 標頭檔中的一個強大演算法，專門用來計算一個範圍內元素的前綴和 (Prefix Sum)。它能有效地將手動迴圈計算前綴和的過程簡化為單一函數呼叫。

## 基本用法

`std::partial_sum` 接受輸入範圍的起始和結束迭代器，以及一個輸出範圍的起始迭代器。它會將計算結果寫入到輸出範圍中。

```cpp
#include <iostream>
#include <vector>
#include <numeric> // For std::partial_sum

void basic_usage() {
    std::vector<int> input = {1, 2, 3, 4, 5};
    std::vector<int> prefix_sum(input.size());

    // 計算前綴和
    std::partial_sum(input.begin(), input.end(), prefix_sum.begin());

    // 輸出結果
    // prefix_sum 將會是 {1, 3, 6, 10, 15}
    std::cout << "Basic 0-indexed prefix sum: ";
    for (int val : prefix_sum) {
        std::cout << val << " ";
    }
    std::cout << std::endl;
}
```

---

## 前綴和的兩種主流實現：0-indexed vs 1-indexed

在演算法競賽和日常實作中，有兩種常見的前綴和陣列設計風格：0-indexed 和 1-indexed。`std::partial_sum` 的預設行為產生的是 0-indexed 的結果，但我們可以輕易地調整它以符合 1-indexed 的需求，後者在計算區間和時更為方便。

### 1. 0-indexed 前綴和 (預設風格)

這是最直觀的實現，`prefix_sum[i]` 儲存的是原始陣列從 `input[0]` 到 `input[i]` 的總和。

- **定義**: `prefix_sum[i] = input[0] + ... + input[i]`
- **區間和 `sum(i, j)`**: `prefix_sum[j] - prefix_sum[i-1]` (需要對 `i=0` 的情況做邊界檢查)

### 2. 1-indexed 前綴和 (競賽常用風格)

這種風格在原陣列的基礎上，在最前面補一個 0。`prefix_sum[i]` 儲存的是原始陣列前 `i` 個元素的總和。

- **定義**: `prefix_sum[0] = 0`, `prefix_sum[i] = input[0] + ... + input[i-1]` for `i > 0`
- **優點**: 計算區間和的公式變得非常簡潔，無需邊界檢查。
- **區間和 `sum(i, j)`**: `prefix_sum[j+1] - prefix_sum[i]`

#### 使用 `std::partial_sum` 實現 1-indexed

我們可以透過將輸出向量的大小設為 `N+1` 並從 `begin() + 1` 開始寫入來輕鬆實現。

```cpp
#include <iostream>
#include <vector>
#include <numeric>

void one_indexed_usage() {
    std::vector<int> input = {1, 2, 3, 4, 5};
    // 輸出向量大小為 N+1，並自動初始化為 0
    std::vector<int> prefix_sum_1_based(input.size() + 1, 0);

    // 從輸出向量的第二個位置開始填寫
    std::partial_sum(input.begin(), input.end(), prefix_sum_1_based.begin() + 1);

    // 輸出結果
    // prefix_sum_1_based 將會是 {0, 1, 3, 6, 10, 15}
    std::cout << "1-indexed prefix sum: ";
    for (int val : prefix_sum_1_based) {
        std::cout << val << " ";
    }
    std::cout << std::endl;

    // 使用 1-indexed 計算區間和 [1, 3] (即 2+3+4)
    int sum_1_to_3 = prefix_sum_1_based[3 + 1] - prefix_sum_1_based[1];
    std::cout << "Sum of range [1, 3] is: " << sum_1_to_3 << std::endl; // 輸出 9
}
```

---

## 比較與總結

| 特性                   | 0-indexed (預設風格)                             | 1-indexed (競賽風格)                                                       |
| ---------------------- | ------------------------------------------------ | -------------------------------------------------------------------------- |
| **陣列大小**           | `N`                                              | `N + 1`                                                                    |
| **`prefix_sum[i]`**    | 儲存 `input` 從 `[0]` 到 `[i]` 的總和 (包含兩端) | 儲存 `input` 的前 `i` 個元素總和 (即 `input[0]` 到 `input[i-1]`)           |
| **`prefix_sum[0]`**    | `input[0]`                                       | `0` (哨兵值)                                                               |
| **區間和 `sum(i, j)`** | `prefix_sum[j] - (i > 0 ? prefix_sum[i-1] : 0)`  | `prefix_sum[j+1] - prefix_sum[i]`                                          |
| **優點**               | 直觀，與 `std::partial_sum` 預設行為一致         | 區間和公式統一，無須邊界檢查，程式碼更簡潔                                 |
| **缺點**               | 區間和公式需要對 `i=0` 進行特殊處理              | 需要額外一個空間，索引對應關係需要轉換 (`input[k]` 對應 `prefix_sum[k+1]`) |

---

### 具體範例對照

假設 `input = {10, 20, 30}`

- **0-indexed**:

  - `prefix_sum` = `{10, 30, 60}`
  - `prefix_sum[2]` 的值是 `60`，代表 `input[0] + input[1] + input[2]` (10 + 20 + 30)。

- **1-indexed**:
  - `prefix_sum` = `{0, 10, 30, 60}`
  - `prefix_sum[2]` 的值是 `30`，代表 `input` 的前 2 個元素和，即 `input[0] + input[1]` (10 + 20)。

---

**結論**: 對於需要頻繁計算區間和的場景，**1-indexed** 風格由於其公式的簡潔性而更受青睞。對於簡單的前綴和計算，`std::partial_sum` 的預設 **0-indexed** 行為已經足夠。
