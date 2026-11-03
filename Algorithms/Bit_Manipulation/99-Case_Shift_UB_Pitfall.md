# Bit Shift UB 地雷

## 🧠 核心規則

```text
shift amount >= bit width  →  Undefined Behavior
```

C++ 標準：位移量 **小於 0 或 ≥ 經整數提升後左運算元的型別位寬** 時，行為未定義；signed／unsigned 都一樣。

## 直覺理解

Shift 的語意是 `value * 2^n`：

```text
1 << 32  =  1 * 2^32  =  4294967296
```

這裡 UB 的原因是 **位移量 32 等於型別位寬**，不是只因結果超過 signed 最大值。以下假設 `int` 為 32-bit、`long long` 至少 64-bit。

## 快速對照表

| Expression  | 結果                                    |
| ----------- | --------------------------------------- |
| `1 << 31`   | ✅ C++11 起有定義，32-bit int 得到 `INT_MIN` |
| `1u << 31`  | ✅ OK（unsigned 無 overflow 問題）       |
| `1 << 32`   | ❌ UB（shift ≥ bit width）              |
| `1LL << 32` | ✅ OK（long long = 64 bits，32 < 64）   |

## ⚠️ Sign bit 與 C++ 版本

| 操作（位移量合法） | C++17 | C++20 起 |
|---|---|---|
| unsigned 左移 | 乘 2 的次方後取模，捨棄高位 | 同左 |
| 負的 signed 值左移，例如 `(-1) << 1` | UB | 依固定位寬的模數規則定義 |
| 負的 signed 值右移 | Implementation-defined | 算術右移，補符號位 |

**二補數讓負數能共用同一套位元加法；unsigned 則避開舊版 C++ 的負值左移限制。** 例如 LC 371 的 `(a & b) << 1`，當 `a = b = -1` 時會左移負值，C++17 下不能保證正確；先轉成 unsigned 再運算即可避免這個問題。

unsigned 轉回 int 若超出 int 範圍，C++17 結果為 implementation-defined；C++20 起採模數轉換。詳見 [位元加法](99-Case_Bitwise_Addition.md) 與 [Sign Extension](05-Sign_Extension_Trap.md)。

依據：[C++17 左右移規則](https://timsong-cpp.github.io/cppwp/n4659/expr.shift)、[目前左移／右移規則](https://eel.is/c++draft/expr.shift)、[整數轉換](https://eel.is/c++draft/conv.integral)。

## ✅ 安全原則

1. **確保 0 ≤ shift < 提升後的型別位寬**：小整數型別可能先提升為 int。
2. **Bit 操作優先用 unsigned**：`uint32_t`、`uint64_t`
3. **需要大數值時用 `1LL`**：`1LL << 32` 而非 `1 << 32`
