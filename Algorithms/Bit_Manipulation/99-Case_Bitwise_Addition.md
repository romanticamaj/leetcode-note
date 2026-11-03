# 位元加法 (Bitwise Addition)

不用 `+` 運算子，純粹用位元操作實現加法。

歷史與教材脈絡見 [LC 371：加法器、二補數與位元加法的歷史](../../Problem_History/LC_0371_Sum_of_Two_Integers.md)。

## 🧠 核心概念：位元操作不管語義

位元操作只關心**位模式 (bit pattern)**，不關心這個數字「代表什麼」。

這意味著：

- 不管是正數、負數、還是 unsigned
- XOR、AND 同時處理所有對應 bits；shift 另須遵守 C++ 型別與版本規則。
- w-bit 二補數將 `-x` 編碼為 `2^w-x`，所以模 `2^w` 的加法不需另處理負號；若真實答案在 signed 範圍內，解讀即為正確整數。

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
    return static_cast<int>(ua);  // C++20 起保證模數轉換；舊版見下方
}
```

**Loop Invariant：** `ua + ub` 在模 `2^w` 下始終等於原始總和，直到 `ub == 0`；w 是 unsigned int 的位寬。

## 為什麼用 `unsigned int`？

```cpp
int a = -1;              // 位模式: 0xFFFFFFFF
unsigned int ua = a;     // 位模式仍是 0xFFFFFFFF
```

- 此演算法使用的是**左移**：unsigned 左移有明確的模數規則，捨棄超出位寬的高位。
- C++17 對負值左移屬 UB；C++20 起 signed 左移也採模數規則，因此新版用 int 亦可，不代表 unsigned 寫法有問題。
- unsigned 轉回超出範圍的 int：C++17 為 implementation-defined，C++20 起保證模數轉換。
- 詳見 [Bit Shift UB 地雷](99-Case_Shift_UB_Pitfall.md) 的版本對照與標準來源；右移的補符號位問題見 [Sign Extension](05-Sign_Extension_Trap.md)。

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
