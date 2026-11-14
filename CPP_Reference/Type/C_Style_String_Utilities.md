# C Style 字串常用 std：C++14 One-Liners

依個人應試經驗，**Amazon Embedded（嵌入式軟體）職位的線上程式測驗（Online Assessment，簡稱 OA）常考 C style 字串處理**：題目提供 `char*`／`char**` 輸入參數，但允許使用 C++14。準備這類測驗時，需要熟悉標準函式庫的字串比較、數值轉換與輸入檢查。

本文整理這些情境常用的 `std` 函式。每個範例區塊獨立閱讀；以一行操作＋註解說明結果，需要連續步驟時才拆行。

## 1. 起點：C string 是指標＋結尾 `\0`

```cpp
#include <cstddef>  // size_t、ptrdiff_t
#include <cstring>  // strcmp、strncmp、strlen、strchr、strstr、strcpy、memcpy
#include <cstdlib>  // strtol、strtoll、strtod
#include <cerrno>   // errno、ERANGE
#include <climits>  // INT_MIN、INT_MAX
#include <cctype>   // isdigit、isspace
#include <cmath>    // isfinite
#include <string>   // string、stoi、stod
```

```cpp
const char* s = "123";             // 唯讀字串；s 指向第一個字元，不保存長度或容量
char buf[] = "123";               // 可修改陣列，內容是 {'1', '2', '3', '\0'}
std::size_t bytes = sizeof(buf);  // 4：整個陣列的大小，包含 '\0'
std::size_t len = std::strlen(s); // 3：從 s 掃到 '\0'；O(n)，不包含結尾
bool empty = s[0] == '\0';        // false；空字串是第一個字元就是 '\0'
const char* missing = nullptr;   // 沒有指向字串；不能傳給 strlen／strcmp／strtol
```

## 2. `strcmp`：比較內容，回傳 0 才是相等

```cpp
const char* token = "+";
bool equal = std::strcmp(token, "+") == 0;   // true；適合判斷 C string operator
bool less = std::strcmp("abc", "abd") < 0;  // true；字典序，依第一個不同的 unsigned char 比較
bool greater = std::strcmp("b", "aa") > 0; // true；字典序不是先比長度
bool prefix = std::strncmp("hello", "he", 2) == 0; // true；最多比 2 個字元，遇 '\0' 仍停止
bool numeric = std::strcmp("10", "2") < 0; // true；比較文字，不是數值 10 < 2
// token == other 比的是兩個指標的位址；strcmp 比的是它們指向的字元內容。
// 只保證結果 <0／==0／>0，不保證一定回傳 -1／0／1；相等不能寫成 if (strcmp(...))。
```

## 3. `strtol`：字串轉 long，順便知道「停在哪裡」

```cpp
const char* s = "123abc"; char* end = nullptr; // end 是輸出變數；由 strtol 寫入停止位置
long value = std::strtol(s, &end, 10);        // 123；10 是十進位；end 指向原字串的 'a'
std::string rest = end;                      // "abc"；沒有複製或修改原字串的是 strtol 本身
std::ptrdiff_t used = end - s;               // 3；已消耗的字元數
bool converted = end != s;                   // true：至少成功轉換一個數字
bool complete = converted && *end == '\0';  // false：後面還有 abc，整個 token 並非合法整數
// &end 是 char**：函式要修改呼叫端的 char* 變數，所以要傳「指標變數的位址」。
// end 指向原始輸入中的位置，不另配置字串；即使宣告成 char*，也不能藉它修改字串常值。
```

```cpp
const char* s = "123"; char* end = nullptr;
long value = std::strtol(s, &end, 10); // 123；end == s + 3，而且 *end == '\0'
bool all = end != s && *end == '\0'; // true；end 不是 nullptr，而是指向結尾的 null character
long hex = std::strtol("ff", nullptr, 16);    // 255；不需要停止位置時，第二個參數才傳 nullptr
long binary = std::strtol("1010", nullptr, 2); // 10；base 可指定 2..36
long octal = std::strtol("010", nullptr, 0);  // 8；C++14 的 base=0 會依前綴辨識，OA 十進位宜明寫 10
// "abc"、""、"+"：無數字可轉，回傳 0 且 end == s；"0" 也回傳 0，但 end != s。
// 會跳過前導空白並接受 +/-；"  -12" 可轉，"12 " 則停在尾端空白。
```

## 4. `errno`＋範圍：成功解析，不代表放得進 int

以下假設 `s` 已指向有效、以 `\0` 結尾的字串；每次轉換前都重設 `errno`。

```cpp
const char* s = "-123"; char* end = nullptr;
errno = 0;                                      // 成功不保證清掉舊錯誤；必須在呼叫前清零
long value = std::strtol(s, &end, 10);            // 超出 long 範圍時回傳 LONG_MIN／LONG_MAX，並設 ERANGE
bool validLong = end != s && *end == '\0' && errno != ERANGE; // 有轉換＋完整消耗＋沒有範圍錯誤
bool validInt = validLong && value >= INT_MIN && value <= INT_MAX; // long 不保證與 int 同寬
bool strictInt = validInt && !std::isspace(static_cast<unsigned char>(*s)); // 若規格禁止前導空白，再加這項
int result = validInt ? static_cast<int>(value) : 0; // 先驗證才縮窄；0 是此例 fallback，不能充當錯誤旗標
// atoi("abc") 和 atoi("0") 都可能得到 0；atoi 沒有 end／可靠範圍錯誤回報，不適合驗證輸入。
// strtoll(s, &end, 10) 回傳 long long；同樣檢查 end 與 errno，別假設 long 永遠是 64-bit。
```

## 5. `strtod`：轉 double，檢查方式相同

```cpp
const char* s = "-3.5e2"; char* end = nullptr;
errno = 0;
double value = std::strtod(s, &end); // -350.0；沒有 base 參數
bool valid = end != s && *end == '\0' && errno != ERANGE && std::isfinite(value); // 要求可表示且有限
// isfinite 排除 NaN／Inf；ERANGE 可表示 overflow，也可能是 underflow。
// strtod 接受前導空白、十六進位浮點等格式，並受 C locale 影響；不等於 LC 65 的語法規則。
// 語法合法與數值可表示是兩件事："1e9999" 可符合十進位數字語法，卻超出 double 範圍。
// OA 若要求保留中間小數，運算也要用 double；最後如何轉 int 仍依題目指定的截斷／四捨五入規則。
```

## 6. 搜尋與字元分類

```cpp
const char* s = "abc:def";
const char* colon = std::strchr(s, ':');       // 指向 ':'；找不到才回傳 nullptr
const char* suffix = std::strstr(s, "def");   // 指向 "def" 的開頭；找不到回傳 nullptr
std::ptrdiff_t index = colon ? colon - s : -1; // 3；同一陣列內的指標相減得到距離
bool digit = std::isdigit(static_cast<unsigned char>(s[0])) != 0; // false；cctype 傳 unsigned char 值或 EOF
bool asciiDigit = '0' <= s[0] && s[0] <= '9'; // false；只判斷單一字元，不是整個字串是否合法數字
```

## 7. `char*` ↔ `std::string`：C style 參數不代表內部只能用 C API

```cpp
const char* raw = "123";
std::string s(raw);                    // 複製內容；之後可用 string 的比較、substr、find 等操作
bool equal = s == "123";               // true；只要一邊是 std::string，這裡就比較內容
const char* view = s.c_str();          // 不複製；借用 s 的 null-terminated buffer，不能透過 view 修改
// s 被銷毀或發生使指標失效的操作後，view 就不能再用；不要保存 std::string("123").c_str()。
// C++14 的 s.data() 也回傳 const char*；可寫的非 const data() overload 是 C++17 才加入。
std::size_t pos = 0;
int value = std::stoi("12abc", &pos);  // 12，pos == 2；stoi 同樣只轉可辨識的前綴，不保證整串合法
// stoi／stod 可用 pos == s.size() 驗證完整消耗，另 catch invalid_argument／out_of_range。
// from_chars 要 C++17；string_view 要 C++17；string::starts_with 要 C++20。
```

## 8. 複製與容量：寫入前先確定 buffer 放得下

```cpp
char dest[8] = {};                     // 容量 8 bytes，最多存 7 個字元＋'\0'
std::strcpy(dest, "abc");             // 複製 a、b、c、'\0'；目的地容量足夠且不與來源重疊才可用
std::memcpy(dest, "xyz", 4);          // 複製指定 4 bytes，這裡刻意包含 '\0'；不重疊才可用
// strcpy 依 '\0' 停止；memcpy 只看 byte 數，不會自動補 '\0'；重疊記憶體搬移用 memmove。
// strncpy(dest, src, n) 不保證結尾有 '\0'，也不是 strcpy 的「自動安全版」。
// char** tokens 搭配 count 可逐項用 tokens[i]；指標本身不告訴你 token 數，須依參數契約。
```

## 速記與延伸

**比較看 0；解析看 end；範圍看 errno；寫入看容量。** `strlen` 為 O(n)，`strcmp` 為 O(min(m,n)+1)；反覆掃描時避免每輪重新 `strlen`。

- [字元與整數互轉](Char_Int_Conversion.md)：`c - '0'`、`stoi`、`to_string`。
- [C++ 版本相容性](../CPP_Version_Compatibility.md)：C++14 可用 API。
- [浮點數轉整數](Double_to_Integer_Verification.md)：型別轉換與數值範圍。

## 來源與原文修正

- [GeeksforGeeks 原文](https://www.geeksforgeeks.org/cpp/strol-function-in-c/)：討論起點；標題的 `strol` 應為 `strtol`。原文將完整轉換後的 end 描述成 null pointer 不正確，應為「指向結尾的 `\0`」。
- [Microsoft：strtol](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/strtol-wcstol-strtol-l-wcstol-l?view=msvc-170)：停止位置、base、無轉換與範圍錯誤。
- [Microsoft：strcmp](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/strcmp-wcscmp-mbscmp?view=msvc-170)：unsigned character 比較與回傳值符號。
- [Microsoft：strtod](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/strtod-strtod-l-wcstod-wcstod-l?view=msvc-170)：浮點格式、停止位置與 ERANGE。
- [C++ 標準草案：數值轉換](https://eel.is/c++draft/string.conversions)：stoi／stod 的轉換、位置與例外契約。
