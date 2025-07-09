# C++ 浮點數與科學記號 (Floating-Point and Scientific Notation)

這份文件整理了在 C++ 中處理浮點數和科學記號時常見的技巧和注意事項。

---

## 1. 科學記號 (Scientific Notation - E Notation)

在 C++ 中，可以使用 `e` 或 `E` 來表示以 10 為底的指數，這是在處理極大或極小數值時的便捷寫法。

- **語法**: `mantissa e exponent` 或 `mantissa E exponent`
- **等價於**: `mantissa * 10^exponent`

### 範例：`1e7` vs `pow(10, 7)`

`1e7` 是一個編譯時即可確定的 `double` 型別常數，代表 `1.0 * 10^7`。

**優點**:

- **效能**: `1e7` 是一個常數，在編譯時期就被解析，沒有任何執行時期的函數調用開銷。相比之下，`pow(10, 7)` 是一個函數調用，會在執行時期進行計算，開銷較大。
- **可讀性**: 對於熟悉科學記號的開發者來說，`1e7` 簡潔明瞭。
- **型別安全**: `1e7` 的型別是 `double`。如果需要 `float`，可以使用 `1e7f`。

```cpp
#include <iostream>
#include <cmath>

int main() {
    // 使用科學記號
    double a = 1e7; // 1.0 * 10^7 = 10,000,000.0

    // 使用 pow 函數
    double b = std::pow(10, 7);

    std::cout.precision(10);
    std::cout << "Using 1e7: " << a << std::endl;
    std::cout << "Using pow(10, 7): " << b << std::endl;

    // 也適用於負指數
    double c = 1.5e-3; // 0.0015
    std::cout << "1.5e-3: " << c << std::endl;

    return 0;
}
```

---

## 2. `ceil` 函數的型別行為

`ceil` (ceiling) 函數用於計算大於或等於給定參數的最小整數，但其回傳值是浮點數型別。

- **原型**: `<cmath>` 或 `<math.h>`

```cpp
  double ceil(double x);
  float ceil(float x);
  long double ceil(long double x);
```

- **核心行為**: `ceil` 接收一個浮點數，回傳一個浮點數。它執行的數學運算結果是整數，但型別仍保留為浮點數。

### 注意事項：型別轉換

如果需要將 `ceil` 的結果存儲在整數型別中，必須進行顯式轉換 (`static_cast`)。

```cpp
#include <iostream>
#include <cmath>

int main() {
    double value = 7.1;

    // ceil 的回傳值是 double
    double ceil_result_double = std::ceil(value); // 結果是 8.0

    // 如果需要整數型別，必須轉換
    int ceil_result_int = static_cast<int>(std::ceil(value)); // 結果是 8

    std::cout << "Original value: " << value << std::endl;
    std::cout << "ceil(value) (double): " << ceil_result_double << std::endl;
    std::cout << "static_cast<int>(ceil(value)) (int): " << ceil_result_int << std::endl;

    // 範例：整數除法的向上取整
    int a = 10;
    int b = 3;

    // 錯誤方式：直接使用整數除法
    // int result = std::ceil(a / b); // a / b = 3, ceil(3.0) = 3.0

    // 正確方式：先轉換為浮點數再運算
    double result_double = std::ceil(static_cast<double>(a) / b); // ceil(10.0 / 3) = ceil(3.33...) = 4.0
    int final_result = static_cast<int>(result_double);

    std::cout << "Ceiling of 10/3 is: " << final_result << std::endl;

    return 0;
}
```
