# Bit Swap 技巧與 Sign Extension 陷阱

## 核心技巧：Bit Swap

### 基本公式

```cpp
// 交換距離為 shift 的位元組
result = ((n & mask_high) >> shift) | ((n & mask_low) << shift)
```

**核心概念：** `(n & mask) >> shift | (n & mask) << shift`

- 用 mask AND 選取特定位元
- shift 移動到目標位置 (0 表示不移動)
- OR 組合結果

### 常用 Mask 對

```cpp
// 互補 mask 對設計原則：high_mask | low_mask = 0xFFFFFFFF

// 選取奇偶位
const uint32_t MASK_ODD  = 0x55555555;  // 01010101...
const uint32_t MASK_EVEN = 0xAAAAAAAA;  // 10101010...

// 選取每 4 位的高低 2 位
const uint32_t MASK_2L = 0x33333333;  // 00110011...
const uint32_t MASK_2H = 0xCCCCCCCC;  // 11001100...

// 選取每 8 位的高低 4 位
const uint32_t MASK_4L = 0x0F0F0F0F;  // 00001111...
const uint32_t MASK_4H = 0xF0F0F0F0;  // 11110000...
```

## ⚠️ Sign Extension 陷阱

### 問題核心

```cpp
// 算術右移 (Arithmetic Shift) - 有符號整數
int32_t x = -1;           // 11111111...11111111
int32_t y = x >> 1;       // 11111111...11111111 (符號位填充)

// 邏輯右移 (Logical Shift) - 無符號整數
uint32_t x = 0xFFFFFFFF;  // 11111111...11111111
uint32_t y = x >> 1;      // 01111111...11111111 (零填充)
```

### 防範策略

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

- Bit swap = mask + shift + OR
- 互補 mask 確保無遺漏
- **永遠使用無符號型別**進行位元操作
- 注意算術右移 vs 邏輯右移的差異
