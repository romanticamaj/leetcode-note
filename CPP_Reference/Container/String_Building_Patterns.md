# String Building Patterns

## 核心問題

反向掃描產生字元，如何有效率建立正向字串？

## 方法比較

| 方法                   | 單次   | 總時間 |
| ---------------------- | ------ | ------ |
| `s = c + s`            | O(n)   | O(n²)  |
| `s.insert(begin(), c)` | O(n)   | O(n²)  |
| `s += c` + `reverse`   | O(1)\* | O(n)   |

> \*amortized O(1)

## 標準寫法

```cpp
string result;
while (...) {
    result += char('0' + digit);  // 尾部插入
}
std::reverse(result.begin(), result.end());
```

## 為什麼頭部插入慢？

`std::string` 是連續記憶體（動態陣列），頭部插入需要 memmove 全部元素。

## 常見錯誤

```cpp
// 型別錯誤：'0' + digit 是 int，不是 char
s = ('0' + digit) + s;  // 編譯錯誤

// 修正但仍 O(n²)
s = string(1, '0' + digit) + s;
```

## 適用題型

- 大數加法/減法 (LC 415, 67)
- 反向掃描 + 正向輸出
- 字串模擬
