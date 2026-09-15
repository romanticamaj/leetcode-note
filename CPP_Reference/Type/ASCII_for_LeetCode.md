# LeetCode ASCII 必備知識

本指南涵蓋了 LeetCode 問題中經常需要的 ASCII 核心值和字元操作。

## 需要記住的關鍵 ASCII 值

理解這些字元到整數的映射至關重要。在 C++ 中，`char` 是一個整數類型，因此您可以直接對其執行算術運算。

| 字元    | ASCII (十進位) | C++ `char` Literal |
| :------ | :------------- | :----------------- |
| **'0'** | 48             | `'0'`              |
| **'A'** | 65             | `'A'`              |
| **'a'** | 97             | `'a'`              |

## 常見操作與陷阱

### 1. 將字元數字轉換為整數

一個常見的錯誤是假設字元 `'5'` 的整數值為 `5`。它的 ASCII 值實際上是 `53`。

**正確方法：**
要取得字元數字的整數值，請減去 `'0'` 的 ASCII 值。

```cpp
char c = '7';
int value = c - '0'; // value 是 7 (55 - 48)
```

**陷阱：** 直接轉型或賦值不會產生數值。

```cpp
char c = '7';
int value = c; // 錯誤：value 是 55，而不是 7
```

### 2. 將小寫字母轉換為 0-Indexed Vector Index

當使用 frequency arrays 或 vectors 處理 26 個小寫英文字母時，您可以將每個字母映射到 0 到 25 的 index。

**正確方法：**
減去 `'a'` 的 ASCII 值。

```cpp
char letter = 'c';
int index = letter - 'a'; // index 是 2 (99 - 97)

std::vector<int> freq(26, 0);
freq[index]++;
```

這對於涉及字元計數的問題（例如 anagrams 或找到第一個唯一字元）至關重要。

### 3. 將大寫字母轉換為 0-Indexed Vector Index

同樣的原則也適用於大寫字母，但您必須減去 `'A'`。

**正確方法：**

```cpp
char letter = 'X';
int index = letter - 'A'; // index 是 23 (88 - 65)
```

**陷阱：** 混合使用大小寫的基準會導致不正確的 index。`'c' - 'A'` 的結果是 `34`，這對於一個 26 個元素的 array 來說是 out of bounds。

### 4. 大小寫轉換

您可以利用 ASCII 表中大小寫字母之間的固定距離來進行轉換。

- `'a'` 和 `'A'` 之間的距離是 `97 - 65 = 32`。

**小寫轉大寫：**

```cpp
char lower = 'h';
char upper = lower - 32; // 'H'
// 或更具可讀性的寫法：
char upper = lower - 'a' + 'A'; // 'H'
```

**大寫轉小寫：**

```cpp
char upper = 'T';
char lower = upper + 32; // 't'
// 或更具可讀性的寫法：
char lower = upper - 'A' + 'a'; // 't'
```

### 5. 檢查字元是否為字母或數字

雖然您可以手動檢查範圍（例如，`c >= 'a' && c <= 'z'`），但 C++ 在 `<cctype>` 中提供了更具可讀性且不易出錯的標準函式庫函式。

- `isalpha(c)`: 檢查 `c` 是否為字母。
- `isdigit(c)`: 檢查 `c` 是否為數字。
- `islower(c)`: 檢查 `c` 是否為小寫字母。
- `isupper(c)`: 檢查 `c` 是否為大寫字母。
- `tolower(c)`: 將 `c` 轉換為小寫。
- `toupper(c)`: 將 `c` 轉換為大寫。

> ⚠️ **傳 `char` 進去是 UB。** 這些函式的參數必須是**能用 `unsigned char` 表示的值**或 `EOF`。`char` 在多數平台是有號的，遇到非 ASCII 位元組（值為負）就會踩到未定義行為。
>
> ```cpp
> isalnum(s[i]);                              // ❌ s[i] 可能是負值
> isalnum(static_cast<unsigned char>(s[i]));  // ✅
> ```
>
> LeetCode 題目多半保證純 ASCII 所以不會出事，但這是面試常被追問的細節。

**範例：**

```cpp
#include <cctype>

char c = 'f';
if (islower(c)) {
    // ...
}

char digit_char = '8';
if (isdigit(digit_char)) {
    // ...
}
```

使用這些函式通常是首選，因為它能提高程式碼的清晰度並正確處理地區設定（儘管對於 LeetCode，標準 ASCII 通常就足夠了）。

## 陷阱總結

1. **`'0'` 不是 `0`**: `char '0'` 的 ASCII 值為 48。務必透過減去 `'0'` 來進行轉換。
2. **混合大小寫**: `c - 'a'` 和 `c - 'A'` 不可互換。請根據字元的大小寫使用正確的基準。
3. **整數與字元算術**: 請記住 `char` 的操作是整數操作。`'a' + 1` 的結果是 `'b'`。
4. **Out-of-Bounds Access**: 未能正確地將字元映射到 indices 可能導致存取 frequency array 超出其邊界，從而導致 undefined behavior。
