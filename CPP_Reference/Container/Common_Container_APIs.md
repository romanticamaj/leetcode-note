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
