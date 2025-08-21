# 數論實用工具：GCD 與 LCM

最大公因數 (Greatest Common Divisor, GCD) 和最小公倍數 (Least Common Multiple, LCM) 是數論中非常實用且頻繁出現的概念。

## 1. 最大公因數 (GCD)

兩個或多個整數共有的因數中，最大的一個即為它們的最大公因數。

### 核心算法：歐幾里得算法 (Euclidean Algorithm)

歐幾里得算法，又稱輾轉相除法，是求兩個非負整數最大公因數的經典算法。其核心遞歸關係如下：

**`gcd(a, b) = gcd(b, a % b)`**

其中 `a > b`，且遞歸的終止條件是 `b == 0`，此時 `a` 即為最大公因數。

#### C++ 模板實現

```cpp
/**
 * @brief 使用歐幾里得算法遞歸計算最大公因數
 *
 * @param a 非負整數 a
 * @param b 非負整數 b
 * @return int a 和 b 的最大公因數
 */
int gcd(int a, int b) {
    // 終止條件：當 b 為 0 時，a 就是最大公因數
    return b == 0 ? a : gcd(b, a % b);
}
```

### C++17 標準庫：`std::gcd` (首選方法)

從 C++17 開始，標準庫在 `<numeric>` 頭文件中提供了 `std::gcd` 函數，其內部實現通常就是高效的歐幾里得算法。**在競賽和現代 C++ 項目中，應始終優先使用 `std::gcd`**。

#### 使用方法

```cpp
#include <numeric> // 需要包含此頭文件

int a = 54;
int b = 24;

// 直接調用 std::gcd
int result = std::gcd(a, b); // result 將會是 6
```

#### 優點

- **標準化**: 官方庫的一部分，程式碼更具可讀性和可移植性。
- **高效性**: 內建實現經過高度優化。
- **簡潔性**: 無需手動實現，減少出錯可能。

## 2. 最小公倍數 (LCM)

兩個或多個整數的公倍數中，最小的一個正整數即為它們的最小公倍數。

### 核心公式

LCM 可以通過 GCD 計算得出，它們之間存在一個非常重要的關係：

**`lcm(a, b) * gcd(a, b) = |a * b|`**

由此可得計算 LCM 的公式：

**`lcm(a, b) = (|a * b|) / gcd(a, b)`**

### C++17 標準庫：`std::lcm`

同樣地，C++17 在 `<numeric>` 頭文件中也提供了 `std::lcm` 函數。

#### 使用方法

```cpp
#include <numeric>

int a = 12;
int b = 18;

// 直接調用 std::lcm
int result = std::lcm(a, b); // result 將會是 36
```

### 溢出問題與安全計算

在使用公式 `(a * b) / gcd(a, b)` 計算 LCM 時，如果 `a` 和 `b` 都很大，`a * b` 可能會導致整數溢出。為了避免這種情況，應使用更安全的計算順序：

**`lcm(a, b) = a * (b / gcd(a, b))`**

這種寫法先進行除法，可以有效降低中間結果的大小，防止溢出。`std::lcm` 的標準庫實現已經考慮了這個問題，因此使用標準庫函數是最安全、最推薦的方式。

#### 手動安全實現

```cpp
#include <numeric> // 為了 std::gcd

long long lcm(int a, int b) {
    if (a == 0 || b == 0) return 0;
    // 使用 long long 防止 a * b 溢出
    // 先除後乘，避免中間結果過大
    return std::abs((long long)a * b) / std::gcd(a, b);
}

// 更安全的版本
long long safe_lcm(int a, int b) {
    if (a == 0 || b == 0) return 0;
    return std::abs((long long)a / std::gcd(a, b) * b);
}
```

## 3. 應用場景

- **分數運算**: 分數的化簡（分子分母同除以 GCD）、通分（尋找分母的 LCM）。
- **週期性問題**: 尋找兩個或多個事件的共同發生週期（LCM）。
- **網格與幾何問題**: 判斷網格中的點是否共線等。
- **數組問題**: 求解數組中所有元素的 GCD 或 LCM。

## 4. 相關主題

- [質因數分解](02-Prime_Factorization.md)
- [數論應用](04-Number_Theory_Applications.md)
