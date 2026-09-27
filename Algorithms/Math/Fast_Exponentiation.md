# 快速冪 (Fast Exponentiation / Binary Exponentiation)

計算 `xⁿ` 時，暴力法連乘 n 次是 O(n)。快速冪每一步把指數砍半，只要 **O(log n)** 次乘法。

## 🧠 核心概念

```
xⁿ = (x^(n/2))²        n 為偶數
xⁿ = (x^(n/2))² · x    n 為奇數（n/2 下取整）
```

指數每層減半，所以只有 log n 層。

## 🧩 遞迴版

```cpp
double power(double x, long long n) {   // n >= 0
    if (n == 0) return 1.0;
    double half = power(x, n / 2);       // 子問題只算一次
    return (n % 2) ? half * half * x : half * half;
}
```

## 🧩 迭代版（看 n 的二進位）

`x¹³ = x⁸ · x⁴ · x¹`，因為 13 = `1101₂`。從低位往高位掃：`x` 每輪平方（`x¹ → x² → x⁴ → x⁸`），遇到 bit 為 1 就乘進答案。

```cpp
double power(double x, long long n) {   // n >= 0
    double result = 1.0;
    while (n > 0) {
        if (n & 1) result *= x;          // 這個 bit 是 1 → 乘進答案
        x *= x;                          // x^(2^k) → x^(2^(k+1))
        n >>= 1;
    }
    return result;
}
```

不變量：`result · xⁿ` 永遠等於原本要求的答案。O(1) 空間。

## ⚠️ 常見陷阱

- **子問題算兩次**：`power(x, n/2) * power(x, n/2)` 的遞迴式是 T(n) = 2T(n/2) + O(1) = **O(n)**，跟暴力法一樣。要先存成一個變數
- **負指數**：`x⁻ⁿ = (1/x)ⁿ`，在入口轉換一次，核心函式只處理 `n >= 0`
- **`-INT_MIN` 溢位**：`n` 是 `int` 時，先轉 `long long` 再取負號（見 [Integer_Overflow_Prevention.md](../../CPP_Reference/Type/Integer_Overflow_Prevention.md) 場景六）
- **取模版本**：整數冪通常要 `% MOD`，每次乘完都要取模，中間值用 `long long`（見 [Modular_Arithmetic_A_Practical_Guide.md](Modular_Arithmetic_A_Practical_Guide.md)）

## ⏱️ 複雜度

| 版本 | 時間 | 空間 |
| :--- | :--- | :--- |
| 暴力連乘 | O(n) | O(1) |
| 遞迴快速冪 | O(log n) | O(log n) call stack |
| 迭代快速冪 | O(log n) | O(1) |

## 延伸

只要運算**可結合**，同一招都能用：矩陣快速冪可以把線性遞推（例如 Fibonacci）從 O(n) 降到 O(log n)。

## 參考範例

- **50 Pow(x, n)**
- **372 Super Pow**（取模版本）
