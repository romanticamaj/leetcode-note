# C++ 常用演算法與工具函式

這份文件整理了在 C++ 中，特別是在解題時經常使用的標準庫演算法和工具函式。

## 常用演算法 (`<algorithm>`)

```cpp
// 排序
sort(v.begin(), v.end());                    // 升序排序
sort(v.begin(), v.end(), greater<int>());    // 降序排序
sort(v.begin(), v.end(), [](int a, int b) {  // 自定義排序
    return a > b;
});
// `std::sort` 的行為:
// 1. 預設行為: 如果不提供第三個參數，`std::sort` 預設使用 `operator<` 進行比較，結果為 **升序 (ascending order)**，即從小排到大。
// 2. 自定義行為:
//    - 若要 **降序 (descending order)**，可以傳入 `std::greater<>()`。
//   - 特別注意, 建構一個 object, 跟 priority_queue 用 type 即可不一樣
//    - 若要實現更複雜的排序邏輯（例如，按物件的某個成員排序），可以傳入一個自定義的比較函式 (Lambda)。
//    - 比較函式 `comp(a, b)` 應回傳 `true` 如果 `a` 應該排在 `b` 的前面。
詳細比較請參見：[C++ Sorting: `std::sort` vs. Container's `sort()`](./Sort_Comparison.md)

// 查找
find(v.begin(), v.end(), val);               // 查找值，返回迭代器
binary_search(v.begin(), v.end(), val);      // 二分查找（需要已排序）
lower_bound(v.begin(), v.end(), val);        // 返回>=val的第一個元素的迭代器
upper_bound(v.begin(), v.end(), val);        // 返回>val的第一個元素的迭代器

// 其他
reverse(v.begin(), v.end());                 // 反轉
count(v.begin(), v.end(), val);              // 計數
max_element(v.begin(), v.end());             // 最大元素的迭代器
min_element(v.begin(), v.end());             // 最小元素的迭代器
```

## 數值運算 (`<numeric>`)

```cpp
// 求和: 基本用法
accumulate(v.begin(), v.end(), 0);           // 求和

// 求和: 高級用法 - 使用自定義二元操作符
// 將 vector<int> 轉換為字符串（用作哈希表的鍵）
string key = accumulate(
    std::next(v.begin()), // 從第二個元素開始
    v.end(),
    std::to_string(v[0]), // 初始值為第一個元素
    [](std::string a, int b) {
        return std::move(a) + '-' + std::to_string(b);
    }
);
```

## 常用工具函式

```cpp
// 最大值和最小值 (`<algorithm>`)
std::max(a, b);                              // 返回兩個值中的較大值
std::max({a, b, c, d});                      // 返回初始化列表中的最大值
std::max(a, b, cmp);                         // 使用自定義比較函數

std::min(a, b);                              // 返回兩個值中的較小值
std::min({a, b, c, d});                      // 返回初始化列表中的最小值
std::min(a, b, cmp);                         // 使用自定義比較函數

std::minmax(a, b);                           // 返回 pair<min, max>
std::minmax({a, b, c, d});                   // 返回初始化列表中的最小值和最大值

// 數學函數 (`<cmath>`)
std::abs(x);                                 // 絕對值
std::pow(x, y);                              // x的y次方
std::sqrt(x);                                // 平方根
std::ceil(x);                                // 向上取整
std::floor(x);                               // 向下取整
std::round(x);                               // 四捨五入