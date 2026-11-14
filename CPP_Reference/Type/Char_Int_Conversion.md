# C++ 心法：字元與整數互轉 (char <-> int)

在 C++ 中，`char` 本質上是一種整數型別，儲存的是字元的 ASCII 值。理解這一點是掌握轉換技巧的關鍵。

---

## 1. 數字字元轉整數值 (Digit Char to Int Value)

這是最常見的轉換場景，目標是將 `'0', '1', ..., '9'` 轉換為 `0, 1, ..., 9`。

### ✅ 核心技巧：減去 `'0'`

由於 ASCII 編碼中，數字 `'0'` 到 `'9'` 是連續排列的，所以任何數字字元減去 `'0'` 的 ASCII 值，就等於它所代表的整數值。

```cpp
char c = '7';
int value = c - '0'; // value 現在是 7

// 驗證
// (int)c 得到 '7' 的 ASCII 值 (55)
// (int)'0' 得到 '0' 的 ASCII 值 (48)
// value = 55 - 48 = 7
```

**這是在演算法題目中處理數字字串時，最高效、最推薦的方法。**

---

## 2. 整數值轉數字字元 (Int Value to Digit Char)

這是上述操作的逆過程，目標是將 `0, 1, ..., 9` 轉換為 `'0', '1', ..., '9'`。

### ✅ 核心技巧：加上 `'0'`

將一個單一數字的整數加上 `'0'` 的 ASCII 值，就會得到對應的字元。

```cpp
int value = 7;
char c = value + '0'; // c 現在是 '7'

// 驗證
// (int)'0' 是 48
// c 的 ASCII 值 = 7 + 48 = 55，即字元 '7'
```

---

## 3. 陷阱：字元轉其 ASCII 整數值

初學者常犯的錯誤是混淆「字元代表的數值」和「字元的 ASCII 數值」。

### 直接轉換 (Implicit/Explicit Casting)

直接將 `char` 轉為 `int` 會得到其在 ASCII 表中的編號，而不是它所表示的數字。

```cpp
char c = '7';
int ascii_value = c; // 隱性轉換 (Implicit conversion)
// 或者 int ascii_value = (int)c; // 顯性轉換 (Explicit cast)

// ascii_value 現在是 55，不是 7！
```

| 轉換方式  | 結果 (`char c = '7'`) | 用途                                   |
| :-------- | :-------------------- | :------------------------------------- |
| `c - '0'` | `7` (整數)            | **正確**：取得數字字元代表的數值       |
| `(int)c`  | `55` (整數)           | **錯誤** (通常)：取得字元的 ASCII 編碼 |

---

## 4. 處理多位數：字串與整數的轉換

C style 的 `char*` 輸入、`strtol`／`strtod` 與完整字串驗證，見 [C Style 字串常用 std](C_Style_String_Utilities.md)。

當處理的不只是一位數時，需要藉助 C++ 標準庫中的字串轉換函數。

### `std::stoi`：字串轉整數 (String to Integer)

```cpp
#include <string>

std::string s = "123";
int number = std::stoi(s); // number 現在是 123
```

### `std::to_string`：整數轉字串 (Integer to String)

```cpp
#include <string>

int number = 123;
std::string s = std::to_string(number); // s 現在是 "123"
```

### 手動實作：字串轉整數

了解 `stoi` 的基本原理也很有幫助。

```cpp
int string_to_int(const std::string& s) {
    int result = 0;
    for (char c : s) {
        if (c >= '0' && c <= '9') {
            result = result * 10 + (c - '0');
        }
    }
    return result;
}
```

## ✅ 總結

| 任務                   | 起點型別             | 終點型別             | 推薦方法           |
| :--------------------- | :------------------- | :------------------- | :----------------- |
| **單一數字字元轉數值** | `char` (`'0'`-`'9'`) | `int` (`0`-`9`)      | `c - '0'`          |
| **單一數值轉數字字元** | `int` (`0`-`9`)      | `char` (`'0'`-`'9'`) | `val + '0'`        |
| **字元轉 ASCII 值**    | `char`               | `int`                | `(int)c`           |
| **多位數字串轉整數**   | `std::string`        | `int`                | `std::stoi()`      |
| **整數轉多位數字串**   | `int`                | `std::string`        | `std::to_string()` |
