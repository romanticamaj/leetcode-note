# C++ STL 演算法中的自訂操作：謂詞與函式物件深度解析

C++ STL 演算法的強大之處，在於其高度的可擴展性。這種擴展性主要來自於它們能夠接受自訂的操作函式（通常以 Lambda 表達式、函式指標或函式物件的形式傳入）。理解這些操作的類型和介面，是精通 STL 的關鍵。

---

## 核心概念：謂詞 (Predicate) 與運算 (Operation)

傳遞給 STL 演算法的自訂邏輯，主要可以分為以下幾種類型：

1. **一元謂詞 (Unary Predicate):** 測試**單一**元素是否滿足某個條件。
2. **二元謂詞 (Binary Predicate):** **比較**兩個元素之間的關係。
3. **二元運算 (Binary Operation):** 將兩個元素**結合**成一個新值。

接下來我們將逐一探討。

---

## 1. 一元謂詞 (Unary Predicate)

- **介面 (Signature):** `bool op(const Type& a);`
- **核心概念:** 接受**一個**引數，返回一個 `bool` 值。
- **常用演算法:** `find_if`, `count_if`, `any_of`, `all_of`, `none_of`, `remove_if`。
- **範例：** 在一個整數向量中，尋找第一個大於 10 的偶數。

```cpp
std::vector<int> v = {1, 11, 4, 12, 15};
auto it = std::find_if(v.begin(), v.end(), [](int x) {
    return (x > 10) && (x % 2 == 0);
});
// *it == 12
```

---

## 2. 二元謂詞 (Binary Predicate)

排序關係的回傳值、strict weak ordering、多條件 tie-break 與 stable_sort 的配合，見 [Comparator 設計心法](Comparator_Design.md)。

- **介面 (Signature):** `bool op(const Type1& a, const Type2& b);`
- **核心概念:** 接受**兩個**引數，返回一個 `bool` 值，通常用於定義“小於”關係。
- **常用演算法:** `sort`, `stable_sort`, `lower_bound`, `upper_bound`, `max_element`, `min_element`。
- **範例：** 根據字串長度對向量進行排序。

```cpp
std::vector<std::string> words = {"cat", "elephant", "dog", "mouse"};
std::sort(words.begin(), words.end(), [](const std::string& a, const std::string& b) {
    return a.length() < b.length(); // 定義 'a' 是否應該在 'b' 之前
});
// 結果: {"cat", "dog", "mouse", "elephant"}
```

---

## 3. 二元運算 (Binary Operation)

- **介面 (Signature):** `ResultType op(const Type1& a, const Type2& b);`
- **核心概念:** 接受**兩個**引數，返回一個**計算結果**。
- **常用演算法:** `accumulate`, `reduce`, `transform` (雙範圍版本)。

這是最需要仔細區分其介面的地方，特別是針對 `std::accumulate`。

### 情況 A：同質運算 (Homogeneous Operation)

當累加的初始值 `init` 和序列中元素的類型**相同**時，二元運算的兩個引數類型也相同。

- **介面:** `T op(const T& accumulator, const T& element);`
- **範例:** 整數向量求和。
  ```cpp
  std::vector<int> v = {1, 2, 3, 4, 5};
  // init 是 int (0), 元素是 int -> op 的介面是 int(int, int)
  int sum = std::accumulate(v.begin(), v.end(), 0);
  ```

### 情況 B：異質運算 (Heterogeneous Operation) - "初值 + 下一個元素"

當累加的初始值 `init` 和序列中元素的類型**不同**時，二元運算的兩個引數類型也不同。

- **介面:** `T op(const T& accumulator, const U& element);`
  - 第一個引數 `accumulator` 的類型與 `init` 的類型 `T` 相同。
  - 第二個引數 `element` 的類型與序列元素的類型 `U` 相同。
- **範例：** 計算一個字串向量中所有字串的總長度。
  ```cpp
  std::vector<std::string> words = {"a", "bb", "ccc"};
  // init 是 int (0), 序列元素是 std::string
  // 因此 op 的介面是 int(int, const std::string&)
  int total_length = std::accumulate(words.begin(), words.end(), 0,
      [](int current_sum, const std::string& word) {
          return current_sum + word.length();
      }); // 結果: 6
  ```

---

## 實踐與除錯

### 常見錯誤：當簽名寫錯時

若自訂操作無法接受演算法傳入的引數，可能在**編譯時期 (compile-time)** 遇到很長的模板錯誤；但隱式轉換也可能讓錯誤寫法通過編譯，仍需檢查比較關係與數值範圍。

**核心除錯技巧：** 當你看到來自 STL 演算法內部、充滿 `template` 和 `static_assert` 的冗長錯誤訊息時，**首先回頭檢查你的 Lambda 或函式物件的簽名**：參數數量、參數類型、`const` 正確性以及返回類型。

#### 範例 1：`std::sort` 的比較關係錯誤

```cpp
// 錯誤：相減結果轉成 bool 後，正數與負數都為 true
std::sort(v.begin(), v.end(), [](int a, int b) {
    return a - b; // <--- 錯誤！應為 a < b
});
```

- **實際問題：** 這通常可以編譯，因為 int 可轉成 bool；但 1-2 與 2-1 都非零，雙向比較都變成 true，違反 strict weak ordering，排序行為未定義。相減也可能發生 signed integer overflow。
- **修正：** 直接回傳 `a < b`；若使用 `string::compare`，則判斷其結果 `< 0`。

#### 範例 2：`std::accumulate` 的累加器類型錯誤

```cpp
// 錯誤：accumulator (current_sum) 的類型應該是 long long
int total_length = std::accumulate(words.begin(), words.end(), 0LL, // <-- init 是 long long
    [](int current_sum, const std::string& word) { // <-- 但 accumulator 是 int
        return current_sum + word.length();
    });
```

- **實際問題：** 這通常也能編譯，因為 long long 可以轉成 int；但每次呼叫 lambda 都可能窄化累加值，失去使用 `0LL` 的目的。
- **原因：** 初始化型別決定 accumulator 型別，lambda 的參數與運算也應保留足夠寬度，而不是依賴隱式轉換。
- **修正：** `[](long long current_sum, ...)`

---

## 總結

| 類型         | 介面 (Signature) | 目的         | 常用演算法             |
| :----------- | :--------------- | :----------- | :--------------------- |
| **一元謂詞** | `bool(T)`        | 測試單一元素 | `find_if`, `count_if`  |
| **二元謂詞** | `bool(T, T)`     | 比較兩個元素 | `sort`, `lower_bound`  |
| **二元運算** | `T(T, U)`        | 結合兩個元素 | `accumulate`, `reduce` |

理解這幾種函式簽名模式，能幫助你更靈活、更準確地使用 C++ STL 演算法來解決複雜問題。
