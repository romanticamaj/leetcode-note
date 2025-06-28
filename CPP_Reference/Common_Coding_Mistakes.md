# 常見編程錯誤記錄

這個文件用於記錄編程過程中常見的錯誤，以便日後參考和避免。

## 函數和遞歸相關錯誤

### 1. 遞歸函數名稱錯誤

**問題描述**：在編寫遞歸函數時，調用自身時使用了錯誤的函數名稱。

**錯誤示例**：

```cpp
// 錯誤示例
void dfs(TreeNode* node) {
    if (!node) return;

    // 處理當前節點
    cout << node->val << " ";

    // 遞歸調用 - 錯誤的函數名稱
    DFS(node->left);  // 大小寫錯誤
    dFs(node->right); // 大小寫錯誤
}
```

**正確示例**：

```cpp
// 正確示例
void dfs(TreeNode* node) {
    if (!node) return;

    // 處理當前節點
    cout << node->val << " ";

    // 遞歸調用 - 正確的函數名稱
    dfs(node->left);  // 正確複製函數名稱
    dfs(node->right); // 正確複製函數名稱
}
```

**避免方法**：

1. 定義函數後，複製函數名稱而不是重新輸入
2. 使用一致的命名規範（如全部小寫或駝峰式命名）
3. 代碼審查時特別注意函數名稱的一致性

### 2. 遞歸基本情況遺漏

**問題描述**：忘記處理遞歸的基本情況（終止條件），導致無限遞歸和棧溢出。

**錯誤示例**：

```cpp
// 錯誤示例 - 缺少基本情況
int factorial(int n) {
    return n * factorial(n - 1);  // 無終止條件
}
```

**正確示例**：

```cpp
// 正確示例
int factorial(int n) {
    if (n <= 1) return 1;  // 基本情況
    return n * factorial(n - 1);
}
```

**避免方法**：

1. 始終先考慮並處理基本情況
2. 確保基本情況能夠覆蓋所有可能的終止條件
3. 考慮邊界情況和特殊輸入

## 數組和索引相關錯誤

### 1. 數組越界訪問

**問題描述**：訪問數組範圍之外的元素。

**錯誤示例**：

```cpp
// 錯誤示例
vector<int> nums = {1, 2, 3};
for (int i = 0; i <= nums.size(); i++) {  // 使用 <= 而不是 <
    cout << nums[i] << " ";  // 當 i = 3 時越界
}
```

**正確示例**：

```cpp
// 正確示例
vector<int> nums = {1, 2, 3};
for (int i = 0; i < nums.size(); i++) {  // 使用 < 而不是 <=
    cout << nums[i] << " ";
}
```

**避免方法**：

1. 使用 `<` 而不是 `<=` 作為循環條件
2. 使用範圍基於的 for 循環 (range-based for loop)
3. 在訪問前檢查索引是否有效

### 2. 索引計算錯誤

**問題描述**：在計算數組索引時出錯，特別是在二分搜索或滑動窗口等算法中。

**錯誤示例**：

```cpp
// 錯誤示例 - 二分搜索中間點計算
int mid = (left + right) / 2;  // 可能導致整數溢出
```

**正確示例**：

```cpp
// 正確示例
int mid = left + (right - left) / 2;  // 避免整數溢出
```

**避免方法**：

1. 使用安全的索引計算方法
2. 注意整數溢出問題
3. 在複雜索引計算中添加註釋說明

## 其他常見錯誤

### 1. 未初始化變數

**問題描述**：使用未初始化的變數，導致未定義行為。

**錯誤示例**：

```cpp
// 錯誤示例
int sum;
for (int i = 0; i < 10; i++) {
    sum += i;  // sum 未初始化
}
```

**正確示例**：

```cpp
// 正確示例
int sum = 0;  // 初始化變數
for (int i = 0; i < 10; i++) {
    sum += i;
}
```

**避免方法**：

1. 在聲明變數時進行初始化
2. 使用編譯器警告檢測未初始化變數
3. 遵循變數最小作用域原則

### 2. C++ 型別陷阱

- **型別不匹配導致的非預期結果**：不同的型別（如 int、unsigned int、long long）進行加減法可能導致非預期結果
- **溢出問題**：使用不適當的型別可能導致計算過程中出現溢出（overflow）
- **常見陷阱**：
  - 有符號與無符號整數混合運算
  - 整數除法截斷
  - 陣列索引使用錯誤型別（如使用 int 而非 size_t）
  - 比較不同型別的值

## C++ 資料結構選用心法

### 1. 有序 vs 無序容器的選擇

**問題描述**：在選擇容器類型時，經常默認使用有序容器（如 `set`、`map`），而忽略了無序容器（如 `unordered_set`、`unordered_map`）可能提供的性能優勢。

**心法**：

- 如果不需要元素有序，優先考慮使用無序容器
- 當看到需要使用 `set` 時，先問自己：「排序重要嗎？」如果不重要，立即考慮 `unordered_set`
- 同理，對於 `map` vs `unordered_map` 也是如此

**性能比較**：

- `set`/`map`: 插入、刪除、查找操作的時間複雜度為 O(log n)
- `unordered_set`/`unordered_map`: 平均情況下，這些操作的時間複雜度為 O(1)

**使用 `set`/`map` 的情況**：

- 需要元素按特定順序排列
- 需要範圍查詢（如找出所有大於 x 且小於 y 的元素）
- 需要使用自定義比較器
- 需要穩定的性能保證（無論數據分佈如何）

**使用 `unordered_set`/`unordered_map` 的情況**：

- 只需要快速查找、插入和刪除
- 不關心元素順序
- 數據分佈較為均勻（避免哈希衝突）
- 優先考慮平均性能而非最壞情況

**代碼示例**：

```cpp
// 不需要排序時，使用無序容器
unordered_set<int> seen;  // 而不是 set<int> seen;
unordered_map<string, int> counts;  // 而不是 map<string, int> counts;

// 需要排序時，使用有序容器
set<int> sortedNums;  // 元素自動排序
map<string, int> sortedCounts;  // 按鍵排序
```

### 2. 其他容器選擇心法

- **`vector` vs `list`**: 除非需要頻繁在中間插入/刪除元素，否則優先使用 `vector`
- **`deque` vs `vector`**: 需要在兩端高效插入/刪除時，考慮 `deque`
- **`priority_queue` vs 自行排序**: 需要維護「最大/最小元素」時，使用 `priority_queue`
- **`array` vs C 風格數組**: 優先使用 `std::array`，它提供了大小信息和邊界檢查

### 3. 處理重複元素的注意事項

**問題描述**：在使用 `set` 或 `unordered_set` 記錄狀態時，如果可能有重複元素，執行 `erase` 操作會移除所有相同的元素，因為這些容器不保存元素的數量信息。

**錯誤示例**：

```cpp
// 錯誤示例 - 使用 set 處理可能有重複元素的情況
set<int> elements = {1, 2, 3, 4, 5};
// ... 某些操作後可能添加了重複元素 ...
elements.insert(2);  // set 不允許重複，所以仍然只有一個 2
elements.erase(2);   // 移除了唯一的 2，而不是最近添加的那個
```

**正確示例**：

```cpp
// 正確示例 - 使用 multiset 處理重複元素
multiset<int> elements = {1, 2, 3, 4, 5};
elements.insert(2);  // 現在有兩個 2
elements.erase(elements.find(2));  // 只移除一個 2
// 或者使用 map/unordered_map 記錄元素出現次數
unordered_map<int, int> counter;
counter[2]++;  // 增加 2 的計數
counter[2]--;  // 減少 2 的計數
if (counter[2] == 0) counter.erase(2);  // 只在計數為 0 時移除
```

**避免方法**：

1. 如果需要處理重複元素，考慮使用 `multiset` 或 `multimap`
2. 或者使用 `map<Key, Count>` 手動記錄元素出現次數
3. 使用 `erase(iterator)` 而不是 `erase(value)` 來精確控制要移除的元素
4. 在算法題中，明確考慮是否需要處理重複元素的情況

**總結原則**：

1. 先考慮操作需求（查找、插入、刪除、排序等）
2. 再考慮性能需求（時間複雜度、空間複雜度）
3. 最後考慮特殊需求（如迭代器穩定性、內存布局等）
4. 特別注意數據中是否有重複元素，以及如何正確處理它們

## ✅ 資料結構操作的成對原則（Add/Delete Pairing）

在使用任何額外的資料結構（如 stack, queue, set, map 等）時，務必注意「加入」與「移除」操作是否成對出現，否則容易導致狀態殘留、記憶體洩漏或邏輯錯誤。

### 常見資料結構操作對應

| 資料結構        | 加入操作                       | 移除操作                     |
| --------------- | ------------------------------ | ---------------------------- |
| `stack`         | `push()`                       | `pop()`                      |
| `queue`         | `push()`                       | `pop()`                      |
| `deque`         | `push_back()` / `push_front()` | `pop_back()` / `pop_front()` |
| `vector`        | `push_back()`                  | `pop_back()`                 |
| `set`           | `insert()`                     | `erase()`                    |
| `map`           | `insert()` / `[]`              | `erase()`                    |
| `unordered_set` | `insert()`                     | `erase()`                    |
| `unordered_map` | `insert()` / `[]`              | `erase()`                    |

### 心法

- 在 DFS / Backtracking / 模擬類型題目中，若使用資料結構記錄 path 或狀態，**務必在遞迴結束後清除該狀態**。
- 每次 `add` 後，應思考何時 `remove`，以維持資料結構的正確性與乾淨狀態。
- 若使用 `set` / `map` 等無序容器，注意 `erase()` 是否會影響迭代器或造成邏輯錯誤。

### 範例

```cpp
// 錯誤：只加不刪，導致狀態殘留
vector<int> path;
void dfs(TreeNode* node) {
    if (!node) return;
    path.push_back(node->val);
    dfs(node->left);
    dfs(node->right);
    // 缺少 path.pop_back();
}

// 正確：加完記得刪除
vector<int> path;
void dfs(TreeNode* node) {
    if (!node) return;
    path.push_back(node->val);
    dfs(node->left);
    dfs(node->right);
    path.pop_back();  // 清除狀態
}
```

這個原則適用於所有需要追蹤狀態的遞迴與模擬問題，幫助你避免常見的資料結構殘留錯誤。

## ✅ 資料結構交互操作的注意事項

在處理複雜資料結構（如樹、圖、鏈結串列）時，常會將其部分資訊轉存到其他容器中（如陣列、佇列、堆疊等）。此時需特別注意「**放入的是值還是指標/物件本身**」。

### 常見錯誤：誤將 TreeNode 放入回傳陣列

```cpp
vector<TreeNode*> result;  // ❌ 錯誤：不應該回傳 TreeNode*
void dfs(TreeNode* node) {
    if (!node) return;
    result.push_back(node);  // ❌ 錯誤：應該只取值
}
```

### 正確做法：只取出需要的值

```cpp
vector<int> result;
void dfs(TreeNode* node) {
    if (!node) return;
    result.push_back(node->val);  // ✅ 正確：只取值
}
```

### 心法

- **回傳陣列/結果容器中應只包含必要資訊（如 int、string）**
- **避免將原始物件指標放入結果中，除非題目明確要求**
- **若需保留物件，應考慮深拷貝或轉換為簡化結構**

這類錯誤常見於樹的遍歷、圖的記錄、或模擬類型題目中，務必在設計資料流時明確區分「資料來源」與「資料輸出」的型別與內容。

## ❗ Character vs Integer in Conditionals

### Problem

In C++, the character literal `'0'` represents the ASCII character `'0'`, which has an ASCII value of **48**. This is **not** the same as the integer literal `0`.

### Consequence

Using a character directly in a conditional like `if ('0')` will evaluate to `true`, because `'0'` is 48, which is a non-zero value.

```cpp
if ('0') {
    // This block WILL execute
}
```

However, the null character `'\0'` has an ASCII value of 0, so:

```cpp
if ('\0') {
    // This block will NOT execute
}
```

### ✅ Best Practice

- **Never use a `char` directly in a boolean condition unless you explicitly mean to check for null or non-null.**
- Always compare explicitly:

```cpp
if (c != '0') { ... }   // Correct: checks if c is not the character '0'
if (c == '\0') { ... }  // Correct: checks for null terminator
```

### 🔍 Summary

| Expression | Evaluates to | Meaning        |
| ---------- | ------------ | -------------- |
| `'0'`      | `true`       | ASCII 48       |
| `'\0'`     | `false`      | ASCII 0 (null) |
| `0`        | `false`      | Integer zero   |

---

This is a subtle but common mistake, especially when working with character arrays or parsing input. Always be explicit when comparing characters in conditionals.

---

## ❗ `const`容器與`operator[]`的陷阱

### 問題描述

當你試圖使用 `operator[]`（中括號運算子）來存取一個被 `const` 修飾的 `std::map` 或 `std::unordered_map` 時，編譯器會報錯。

```cpp
// 錯誤範例
void processGraph(const unordered_map<string, unordered_map<string, double>>& graph) {
    string current = "A";
    // ...
    // 下面這行會導致編譯錯誤
    for (auto const& [neighbor, weight] : graph[current]) {
        // ...
    }
}
```

**錯誤訊息**: `no viable overloaded operator[] for type 'const ...'`

### 核心原因

`std::map` 和 `std::unordered_map` 的 `operator[]` 不是一個 `const` 成員函數。這是因為它被設計為具有「如果鍵不存在，就插入一個預設值」的副作用。這個插入操作會修改容器，這與 `const` 的承諾（不修改物件）相違背。

### ✅ 正確做法

當你需要從一個 `const` 的 map 中讀取資料時，必須使用保證不會修改容器的方法。

#### 方法一：使用 `.at()` (推薦)

`.at()` 成員函數會回傳鍵對應的值，且它有 `const` 版本。如果鍵不存在，它會拋出一個 `std::out_of_range` 例外。

```cpp
// 正確範例
void processGraph(const unordered_map<string, unordered_map<string, double>>& graph) {
    string current = "A";
    try {
        for (auto const& [neighbor, weight] : graph.at(current)) {
            // ...
        }
    } catch (const std::out_of_range& e) {
        // 處理 'current' 節點不存在於圖中的情況
    }
}
```

#### 方法二：使用 `.find()`

`.find()` 會回傳一個指向鍵值對的迭代器。如果鍵不存在，它會回傳指向 `.end()` 的迭代器。這個方法不會拋出例外，因此通常更安全、更常用。

```cpp
// 正確範例
void processGraph(const unordered_map<string, unordered_map<string, double>>& graph) {
    string current = "A";
    auto it = graph.find(current);

    if (it != graph.end()) {
        // it->first 是鍵 (current)
        // it->second 是值 (鄰居 map)
        for (auto const& [neighbor, weight] : it->second) {
            // ...
        }
    } else {
        // 處理 'current' 節點不存在於圖中的情況
    }
}
```

### 🔍 總結

| 方法         | `const` 安全性 | 鍵不存在時的行為         | 適用場景                                 |
| :----------- | :------------- | :----------------------- | :--------------------------------------- |
| `operator[]` | ❌ 否          | 插入預設值               | 非 `const` map，且希望鍵不存在時自動插入 |
| `.at()`      | ✅ 是          | 拋出 `std::out_of_range` | `const` map，且你預期鍵一定存在          |
| `.find()`    | ✅ 是          | 回傳 `end()` 迭代器      | `const` map，最安全通用的讀取方式        |

**心法**：當處理 `const` map 或 `const` unordered_map 時，永遠用 `.find()` 或 `.at()` 取代 `[]` 來存取元素。

---

## ❗ `vector` vs `map` 的 `operator[]` 行為差異

`vector` 和 `map`/`unordered_map` 都支援 `operator[]`，但其行為和約束截然不同，混淆它們是常見的錯誤來源。

### `std::vector` 的 `operator[]`

- **行為**: 提供對**已存在**元素的直接存取。它**不會**自動新增元素。
- **約束**: 使用 `[]` 存取一個**超出範圍 (out-of-bounds)** 的索引是**未定義行為 (Undefined Behavior)**。程式可能會崩潰，也可能讀寫無關的記憶體。
- **初始化**: 在使用 `operator[]` 賦值前，必須確保 `vector` 的大小足夠，或者使用 `push_back` 來新增元素。

```cpp
// ❌ 錯誤：對一個空的 vector 使用索引賦值
std::vector<int> vec;
vec[0] = 100; // 未定義行為！vec 的大小是 0。

// ✅ 正確做法 1：先指定大小
std::vector<int> vec_sized(10);
vec_sized[0] = 100; // 正確，因為索引 0 是合法的。

// ✅ 正確做法 2：使用 push_back
std::vector<int> vec_pushed;
vec_pushed.push_back(100); // 正確，新增一個元素並賦值。
```

### `std::map` / `std::unordered_map` 的 `operator[]`

- **行為**: 提供對鍵 (key) 所對應的值 (value) 的存取。
- **特殊功能**: 如果鍵**不存在**，`operator[]` 會**自動插入**一個新的鍵值對，其中值是預設建構的 (例如，`int` 為 `0`，`string` 為 `""`)。
- **`const` 限制**: 正因為有自動插入的副作用，所以 `operator[]` 不能被用於 `const` 的 map (詳見上一節)。

```cpp
std::unordered_map<std::string, int> word_count;

// ✅ 正確：如果 "hello" 不存在，會自動新增 "hello" -> 0，然後再 ++ 變成 1。
word_count["hello"]++;

// ✅ 正確：可以直接賦值，即使 "world" 不存在。
word_count["world"] = 5;
```

### 總結心法

| 容器                              | `operator[]` 行為 | 使用前提                            |
| :-------------------------------- | :---------------- | :---------------------------------- |
| `std::vector`                     | **僅存取**        | 索引必須在 `[0, size() - 1]` 範圍內 |
| `std::map` / `std::unordered_map` | **存取或插入**    | 無，若鍵不存在則自動插入            |

> **心法**: 對 `vector` 用 `[]` 前，先確保**空間已分配**；對 `map` 用 `[]`，則可放心寫入，它會**自動處理**鍵的存在與否。
