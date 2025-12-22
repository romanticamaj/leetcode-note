# 位元加法 (Bitwise Addition)

不用 `+` 運算子，純粹用位元操作實現加法。

## 🧠 核心概念：位元操作不管語義

位元操作只關心**位模式 (bit pattern)**，不關心這個數字「代表什麼」。

這意味著：

- 不管是正數、負數、還是 unsigned
- XOR、AND、shift 都只看 0 和 1 的排列
- Two's complement 表示的負數，做位元運算後結果自動正確，不需特殊處理

## 核心公式

```
a + b = (a ^ b) + ((a & b) << 1)
        -------   -------------
        非進位部分    進位部分
```

**拆解：**
- `a ^ b`：相加但不考慮進位（0+1=1, 1+0=1, 0+0=0, 1+1=0）
- `a & b`：找出需要進位的位置（只有 1+1 需要進位）
- `<< 1`：進位要往左移一位

## 實作

```cpp
int getSum(int a, int b) {
    unsigned int ua = a, ub = b;  // 轉 unsigned 確保 shift 行為可預測
    while (ub != 0) {
        unsigned int carry = (ua & ub) << 1;
        ua = ua ^ ub;
        ub = carry;
    }
    return (int)ua;  // 轉回 int，自動還原正負號
}
```

**Loop Invariant：** `ua + ub` 的值始終等於原始 `a + b`，直到 `ub == 0`

## 為什麼用 `unsigned int`？

```cpp
int a = -1;              // 位模式: 0xFFFFFFFF
unsigned int ua = a;     // 位模式仍是 0xFFFFFFFF
```

- C++ 的 signed 右移是算術移位（補符號位），行為依實作而定
- unsigned 右移是邏輯移位（補 0），行為明確
- 轉回 `int` 時，位模式不變，自動還原成正確的負數

## 手動追蹤：`-1 + 1`

```
初始: ua = 0xFFFFFFFF (-1), ub = 0x00000001 (1)

第 1 次:
  carry = (0xFFFFFFFF & 0x00000001) << 1 = 0x00000002
  ua    = 0xFFFFFFFF ^ 0x00000001       = 0xFFFFFFFE
  ub    = 0x00000002

第 2 次:
  carry = (0xFFFFFFFE & 0x00000002) << 1 = 0x00000004
  ua    = 0xFFFFFFFE ^ 0x00000002       = 0xFFFFFFFC
  ub    = 0x00000004

... (進位持續往左推進)

最終: ua = 0x00000000, ub = 0x00000000
return 0 ✅
```

進位像波浪一樣從右往左推，最終「溢出」32 位元邊界消失。

## ✅ 關鍵要點

- 位元操作只看 bit pattern，不管數值語義
- `a ^ b` = 不進位加法，`(a & b) << 1` = 進位
- 用 `unsigned` 確保 shift 行為可預測
- Two's complement 的負數做位元運算後結果自動正確
