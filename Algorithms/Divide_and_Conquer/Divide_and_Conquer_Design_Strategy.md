# Divide and Conquer 設計策略心法

## 🧠 核心哲學

Divide and Conquer 的本質是將大問題遞迴分解為獨立的子問題，關鍵在於識別問題的 **主要工作位置**：是在分割階段（Divide-centric）還是合併階段（Combine-centric）。這決定了算法的設計重點和優化方向。

## 三步設計框架

### Step 1: 子問題分割策略

判斷問題是否可分割及分割方式：

```cpp
// 常見分割模式
T(n) = a * T(n/b) + f(n)
// a: 子問題數量
// b: 問題規模縮減比例
// f(n): divide/combine 的工作量
```

**分割原則：**

- 子問題必須**獨立**（無重疊），否則考慮 Dynamic Programming
- 常見分割：二分（n/2）、三分（n/3）、或 a 個子問題（n/b）
- 分割點的選擇影響算法效率

### Step 2: 識別算法類型

#### Divide-centric（分割主導型）

**特徵：** 主要邏輯在分割階段，合併簡單或無需合併

```cpp
template<typename T>
void divideCentric(vector<T>& arr, int left, int right) {
    if (left >= right) return;

    // 核心工作：精心設計的分割
    int pivot = partition(arr, left, right);  // O(n) work

    // 遞迴處理（合併是 trivial 的）
    divideCentric(arr, left, pivot - 1);
    divideCentric(arr, pivot + 1, right);
}
```

**典型例子：** QuickSort、QuickSelect

- 分割工作：O(n) - 選擇 pivot 並分區
- 合併工作：O(1) - 無需合併

#### Combine-centric（合併主導型）

**特徵：** 分割簡單，主要邏輯在合併階段

```cpp
template<typename T>
Result combineCentric(vector<T>& arr, int left, int right) {
    if (left >= right) return baseCase();

    // 簡單分割
    int mid = left + (right - left) / 2;

    // 遞迴求解
    auto leftResult = combineCentric(arr, left, mid);
    auto rightResult = combineCentric(arr, mid + 1, right);

    // 核心工作：精心設計的合併
    return merge(leftResult, rightResult);  // O(n) work
}
```

**典型例子：** MergeSort、計算逆序對

- 分割工作：O(1) - 簡單對半分
- 合併工作：O(n) - 合併已排序數組

### Step 3: 優化工作複雜度

根據 Master Theorem 優化：

```
T(n) = a * T(n/b) + f(n)

Case 1: f(n) = O(n^c), c < log_b(a)
        => T(n) = O(n^log_b(a))

Case 2: f(n) = O(n^log_b(a))
        => T(n) = O(n^log_b(a) * log n)

Case 3: f(n) = O(n^c), c > log_b(a)
        => T(n) = O(f(n))
```

**優化目標：**

- 原本暴力法 O(n²) → 優化到 O(n log n)：divide/combine 做 O(n) 工作
- 原本 O(n log n) → 優化到 O(n)：divide/combine 做 O(1) 工作

## 🧩 設計模式對比

| 特性     | Divide-centric            | Combine-centric         |
| -------- | ------------------------- | ----------------------- |
| 主要工作 | Partition/Select          | Merge/Combine           |
| 分割策略 | 智能選擇（pivot, median） | 簡單對半                |
| 合併策略 | Trivial 或無需合併        | 複雜的合併邏輯          |
| 典型算法 | QuickSort, Selection      | MergeSort, Closest Pair |
| 效能瓶頸 | Pivot 選擇品質            | 合併效率                |
| 空間需求 | 通常 O(log n)             | 通常 O(n) 輔助空間      |

## ⚠️ 設計陷阱

### 1. 子問題重疊

```cpp
// 錯誤：Fibonacci 的分治實現
int fib(int n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);  // 子問題重疊！
}
// 應該使用 Dynamic Programming
```

### 2. 分割不均衡

```cpp
// 錯誤：總是選擇第一個元素作為 pivot
int pivot = arr[left];  // 最壞情況 O(n²)

// 正確：隨機或 median-of-three
int pivot = medianOfThree(arr, left, right);
```

### 3. 過度分割

```cpp
// 效率低下：對小數組仍遞迴
if (right - left <= 10) {
    insertionSort(arr, left, right);  // 小數組用簡單算法
    return;
}
```

## ✅ 設計檢查清單

- [ ] 子問題是否獨立（無重疊）？
- [ ] 識別主要工作在 divide 還是 combine？
- [ ] divide/combine 的複雜度是否低於暴力法？
- [ ] 是否滿足 Master Theorem 的優化條件？
- [ ] 對小規模問題是否有優化（如切換到簡單算法）？
- [ ] 空間複雜度是否可接受？
