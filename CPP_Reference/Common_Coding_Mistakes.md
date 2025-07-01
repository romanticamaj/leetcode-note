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
