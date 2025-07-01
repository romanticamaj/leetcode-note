# C++ 常用數據結構 API 參考

## vector

```cpp
vector<int> v;                // 創建空向量
vector<int> v(10);            // 創建大小為10的向量，初始值為0
vector<int> v(10, 5);         // 創建大小為10的向量，初始值為5
vector<int> v = {1, 2, 3};    // 使用初始化列表

v.push_back(x);               // 在末尾添加元素
v.pop_back();                 // 移除末尾元素
v[i];                         // 訪問索引為i的元素（無邊界檢查）
v.at(i);                      // 訪問索引為i的元素（有邊界檢查）
v.front();                    // 第一個元素
v.back();                     // 最後一個元素
v.size();                     // 元素數量
v.empty();                    // 檢查是否為空
v.clear();                    // 清空向量
v.resize(n);                  // 調整大小為n
v.resize(n, val);             // 調整大小為n，新元素值為val
v.reserve(n);                 // 預留n個元素的空間

// 迭代
for (int i = 0; i < v.size(); i++) { /* 使用 v[i] */ }
for (auto it = v.begin(); it != v.end(); it++) { /* 使用 *it */ }
for (auto& x : v) { /* 使用 x */ }
```

## string

```cpp
string s;                     // 空字符串
string s = "hello";           // 初始化
string s(5, 'a');             // "aaaaa"

s += "world";                 // 連接字符串
s.append("world");            // 連接字符串
s.push_back('c');             // 添加字符
s.pop_back();                 // 移除最後一個字符
s[i];                         // 訪問索引為i的字符（無邊界檢查）
s.at(i);                      // 訪問索引為i的字符（有邊界檢查）
s.substr(pos, len);           // 子字符串，從pos開始，長度為len
s.find("pattern");            // 查找子字符串，返回位置或string::npos
s.length();                   // 字符串長度
s.size();                     // 字符串長度
s.empty();                    // 檢查是否為空
s.clear();                    // 清空字符串
s.erase(pos, len);            // 刪除從pos開始的len個字符
s.insert(pos, str);           // 在pos位置插入字符串str
```

## unordered_map

```cpp
unordered_map<string, int> map;  // 創建空映射
map["key"] = 1;                  // 插入或更新
map.insert({{"key1", 1}, {"key2", 2}}); // 批量插入
map.emplace("key", 1);           // 原地構造並插入

map["key"];                      // 訪問（如果不存在則創建）
map.at("key");                   // 訪問（如果不存在則拋出異常）
map.find("key");                 // 查找，返回迭代器
map.count("key");                // 計數（0或1）
map.contains("key");             // 檢查是否包含（C++20）
map.erase("key");                // 刪除
map.size();                      // 元素數量
map.empty();                     // 檢查是否為空
map.clear();                     // 清空

// 迭代
for (auto& [key, value] : map) { /* 使用 key 和 value */ }
for (auto it = map.begin(); it != map.end(); it++) {
    // 使用 it->first 和 it->second
}
```

## unordered_set

```cpp
unordered_set<int> set;          // 創建空集合
set.insert(1);                   // 插入元素
set.emplace(1);                  // 原地構造並插入
set.erase(1);                    // 刪除元素
set.find(1);                     // 查找，返回迭代器
set.count(1);                    // 計數（0或1）
set.contains(1);                 // 檢查是否包含（C++20）
set.size();                      // 元素數量
set.empty();                     // 檢查是否為空
set.clear();                     // 清空

// 迭代
for (auto& x : set) { /* 使用 x */ }
for (auto it = set.begin(); it != set.end(); it++) { /* 使用 *it */ }
```

## map (有序)

```cpp
map<string, int> map;            // 創建空映射（按鍵排序）
// 其他API與unordered_map類似，但保證按鍵排序
map.lower_bound("key");          // 返回>=key的第一個元素的迭代器
map.upper_bound("key");          // 返回>key的第一個元素的迭代器
```

## set (有序)

```cpp
set<int> set;                    // 創建空集合（按值排序）
// 其他API與unordered_set類似，但保證按值排序
set.lower_bound(1);              // 返回>=1的第一個元素的迭代器
set.upper_bound(1);              // 返回>1的第一個元素的迭代器
```

## queue

```cpp
queue<int> q;                    // 創建空隊列
q.push(1);                       // 入隊
q.pop();                         // 出隊
q.front();                       // 隊首元素
q.back();                        // 隊尾元素
q.size();                        // 元素數量
q.empty();                       // 檢查是否為空
```

## priority_queue (優先隊列/堆)

```cpp
// 最大堆（默認）
priority_queue<int> pq;
// 最小堆
priority_queue<int, vector<int>, greater<int>> min_pq;

pq.push(1);                      // 插入元素
pq.pop();                        // 移除頂部元素
pq.top();                        // 頂部元素
pq.size();                       // 元素數量
pq.empty();                      // 檢查是否為空
```

## stack

```cpp
stack<int> s;                    // 創建空棧
s.push(1);                       // 入棧
s.pop();                         // 出棧
s.top();                         // 棧頂元素
s.size();                        // 元素數量
s.empty();                       // 檢查是否為空
```

## deque (雙端隊列)

```cpp
deque<int> d;                    // 創建空雙端隊列
d.push_back(1);                  // 在末尾添加元素
d.push_front(1);                 // 在開頭添加元素
d.pop_back();                    // 移除末尾元素
d.pop_front();                   // 移除開頭元素
d[i];                            // 訪問索引為i的元素
d.front();                       // 第一個元素
d.back();                        // 最後一個元素
d.size();                        // 元素數量
d.empty();                       // 檢查是否為空
d.clear();                       // 清空
```

## list (雙向鏈表)

```cpp
list<int> l;                     // 創建空鏈表
l.push_back(1);                  // 在末尾添加元素
l.push_front(1);                 // 在開頭添加元素
l.pop_back();                    // 移除末尾元素
l.pop_front();                   // 移除開頭元素
l.front();                       // 第一個元素
l.back();                        // 最後一個元素
l.size();                        // 元素數量
l.empty();                       // 檢查是否為空
l.clear();                       // 清空
l.sort();                        // 排序
l.reverse();                     // 反轉
l.remove(val);                   // 移除所有值為val的元素
```

## 常用算法

```cpp
// 排序
sort(v.begin(), v.end());                    // 升序排序
sort(v.begin(), v.end(), greater<int>());    // 降序排序
sort(v.begin(), v.end(), [](int a, int b) {  // 自定義排序
    return a > b;
});

// 查找
find(v.begin(), v.end(), val);               // 查找值
binary_search(v.begin(), v.end(), val);      // 二分查找（需要已排序）
lower_bound(v.begin(), v.end(), val);        // 返回>=val的第一個元素的迭代器
upper_bound(v.begin(), v.end(), val);        // 返回>val的第一個元素的迭代器

// 其他
reverse(v.begin(), v.end());                 // 反轉
count(v.begin(), v.end(), val);              // 計數
max_element(v.begin(), v.end());             // 最大元素的迭代器
min_element(v.begin(), v.end());             // 最小元素的迭代器

// 求和: 基本用法
accumulate(v.begin(), v.end(), 0);           // 求和（需要 #include <numeric>）
// 求和: 高級用法 - 使用自定義二元操作符 [Medium]
// 將 vector<int> 轉換為字符串（用作哈希表的鍵）
string key = accumulate(v.begin(), v.end(), string(),
    [](string a, int b) {
        return std::move(a) + '-' + to_string(b);
    });
```

## 常用工具函數

```cpp
// 最大值和最小值
std::max(a, b);                              // 返回兩個值中的較大值
std::max({a, b, c, d});                      // 返回初始化列表中的最大值
std::max(a, b, cmp);                         // 使用自定義比較函數

std::min(a, b);                              // 返回兩個值中的較小值
std::min({a, b, c, d});                      // 返回初始化列表中的最小值
std::min(a, b, cmp);                         // 使用自定義比較函數

std::minmax(a, b);                           // 返回 pair<min, max>
std::minmax({a, b, c, d});                   // 返回初始化列表中的最小值和最大值

// 數學函數 (需要 #include <cmath>)
std::abs(x);                                 // 絕對值
std::pow(x, y);                              // x的y次方
std::sqrt(x);                                // 平方根
std::ceil(x);                                // 向上取整
std::floor(x);                               // 向下取整
std::round(x);                               // 四捨五入
