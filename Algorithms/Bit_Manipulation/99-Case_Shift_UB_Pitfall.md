# Bit Shift UB 地雷

## 🧠 核心規則

```
shift amount >= bit width  →  Undefined Behavior
```

C++ 標準：右運算元 **≥ 型別位寬** 時，行為未定義。

## 直覺理解

Shift 的語意是 `value * 2^n`：

```
1 << 32  =  1 * 2^32  =  4294967296
```

但 `int` (32-bit) 最大只能表達 `2^31 - 1`，標準不幫你 wrap，直接 UB。

## 快速對照表

| Expression  | 結果                                    |
| ----------- | --------------------------------------- |
| `1 << 31`   | ⚠️ signed overflow → UB                |
| `1u << 31`  | ✅ OK（unsigned 無 overflow 問題）       |
| `1 << 32`   | ❌ UB（shift ≥ bit width）              |
| `1LL << 32` | ✅ OK（long long = 64 bits，32 < 64）   |

## ⚠️ 常見地雷

**`1 << 31`**：shift 量合法（31 < 32），但結果 `0x80000000` 對 signed int 是 overflow → UB。

## ✅ 安全原則

1. **確保 shift < bit width**：`n < sizeof(T) * CHAR_BIT`
2. **Bit 操作優先用 unsigned**：`uint32_t`、`uint64_t`
3. **需要大數值時用 `1LL`**：`1LL << 32` 而非 `1 << 32`
