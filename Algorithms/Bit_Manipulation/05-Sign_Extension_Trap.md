# ⚠️ Sign Extension 陷阱

## 問題核心

```cpp
// 算術右移 (Arithmetic Shift) - 有符號整數
int32_t x = -1;           // 11111111...11111111
int32_t y = x >> 1;       // 11111111...11111111 (符號位填充)

// 邏輯右移 (Logical Shift) - 無符號整數
uint32_t x = 0xFFFFFFFF;  // 11111111...11111111
uint32_t y = x >> 1;      // 01111111...11111111 (零填充)
```

## 防範策略

```cpp
// 策略 1：使用無符號型別
unsigned int safe_shift(int n, int shift) {
    unsigned int r = n;  // 關鍵轉換
    return r >> shift;
}

// 策略 2：明確型別轉換
int result = ((unsigned)n >> shift);

// 策略 3：使用標準型別
#include <cstdint>
uint32_t value = n;  // 明確使用 uint32_t
```

## ✅ 關鍵要點

- **需要邏輯右移時使用無符號型別**；不是所有位元操作都禁止 signed。
- 負的 signed 右移：C++17 為 implementation-defined；C++20 起保證算術右移，補符號位。
- 邏輯右移（unsigned）：補 0
- 左移不做 sign extension；負值左移的版本差異與位移量限制，見 [Bit Shift UB 地雷](99-Case_Shift_UB_Pitfall.md)。
