# Interval Design in Divide and Conquer 區間設計心法

## 🧠 核心哲學

在分治法中，區間表示方式的選擇（閉區間 `[start, end]` vs 半開區間 `[start, end)`）會深刻影響整個算法的實現細節。**必須在開始前明確區間定義**，否則索引計算極易出錯。

## 核心概念：兩種區間表示法

### 閉區間 [start, end]

- **含義**：包含 start 和 end 兩個端點
- **大小計算**：`size = end - start + 1`
- **空區間**：`start > end`
- **單元素**：`start == end`

### 半開區間 [start, end)

- **含義**：包含 start，不包含 end
- **大小計算**：`size = end - start`
- **空區間**：`start >= end`
- **單元素**：`end - start == 1`

## 🧩 實現對比

### Base Case 設計差異

```cpp
// 閉區間 [start, end]
if (start > end) return nullptr;      // 空區間
if (start == end) return single(arr[start]);  // 單元素（可選優化）

// 半開區間 [start, end)
if (start >= end) return nullptr;     // 空區間
if (end - start == 1) return single(arr[start]);  // 單元素（可選優化）
```

### Mid 計算與遞迴調用

```cpp
// 閉區間 [start, end]
int mid = start + (end - start) / 2;
auto left = divide(arr, start, mid - 1);   // 左半：[start, mid-1]
auto right = divide(arr, mid + 1, end);    // 右半：[mid+1, end]
// 注意：mid 被排除在兩個子區間之外

// 半開區間 [start, end)
int mid = start + (end - start) / 2;
auto left = divide(arr, start, mid);       // 左半：[start, mid)
auto right = divide(arr, mid, end);        // 右半：[mid, end)
// 注意：mid 是右區間的起點
```

### 包含 Mid 的變體

```cpp
// 閉區間包含 mid 在左側
int mid = start + (end - start) / 2;
auto left = divide(arr, start, mid);       // [start, mid]
auto right = divide(arr, mid + 1, end);    // [mid+1, end]

// 半開區間包含 mid 在左側（更常見）
int mid = start + (end - start) / 2;
auto left = divide(arr, start, mid + 1);   // [start, mid+1)
auto right = divide(arr, mid + 1, end);    // [mid+1, end)
```

## 完整模板對比

### 閉區間模板

```cpp
template<typename T>
Result solve(vector<T>& arr, int start, int end) {
    // Base case
    if (start > end) return empty_result();
    if (start == end) return leaf_result(arr[start]);

    // Divide
    int mid = start + (end - start) / 2;

    // Conquer
    auto left = solve(arr, start, mid - 1);
    auto right = solve(arr, mid + 1, end);

    // Combine
    return combine(left, arr[mid], right);
}

// 初始調用
solve(arr, 0, n - 1);
```

### 半開區間模板

```cpp
template<typename T>
Result solve(vector<T>& arr, int start, int end) {
    // Base case
    if (start >= end) return empty_result();
    if (end - start == 1) return leaf_result(arr[start]);

    // Divide
    int mid = start + (end - start) / 2;

    // Conquer
    auto left = solve(arr, start, mid);
    auto right = solve(arr, mid, end);

    // Combine（注意 mid 的使用）
    return combine(left, arr[mid], right);
}

// 初始調用
solve(arr, 0, n);
```

## ⚠️ 常見陷阱

### 1. 混用不同區間表示

```cpp
// 錯誤：在閉區間設計中使用半開區間的邏輯
if (start >= end) return nullptr;  // 應該是 start > end
```

### 2. Mid 索引錯誤

```cpp
// 錯誤：閉區間中忘記調整 mid
auto left = divide(arr, start, mid);    // 應該是 mid - 1
auto right = divide(arr, mid, end);     // 應該是 mid + 1
```

### 3. 初始調用錯誤

```cpp
// 錯誤：半開區間使用 n-1
solve(arr, 0, n - 1);  // 應該是 solve(arr, 0, n)
```

## 選擇建議

### 使用閉區間的場景

- 處理具體索引的問題（如二分搜尋）
- 需要明確包含兩端的情況
- 符合直覺思維的場景

### 使用半開區間的場景

- STL 風格的迭代器操作
- 需要方便的區間拼接（`[a,b) + [b,c) = [a,c)`）
- 空區間表示更自然（`[a,a)` 表示空）

## ✅ 設計檢查清單

- [ ] 明確標註區間類型（函數名或註釋）
- [ ] Base case 與區間類型一致
- [ ] Mid 計算與遞迴調用匹配
- [ ] 初始調用使用正確的區間範圍
- [ ] 單元素情況處理正確
