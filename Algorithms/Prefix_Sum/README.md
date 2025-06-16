# Prefix Sum 技巧

## 要點

- 創建一個前綴和數組 **prefix**，其中 **prefix[i]** 是所有元素到索引 i（包含）的總和
- Prefix Sums 允許我們在 **O(1)** 時間內找到任何子數組的和
- 如果我們想要從索引 i 到 j（包含）的子數組的和，答案是 **prefix[j] - prefix[i - 1]**
- 有時會遇到 i - 1 越界的情況，可以用 **prefix[j] - prefix[i] + nums[i]**
- 用線條來畫出 sum，會比較好想像

## 常用情境

- 尋找特定和的子數組
- 計算滿足特定條件的子數組數量
- 需要與哈希表結合使用的情況

## 效率分析

建立前綴和是一種預處理形式：
- 只需 **O(n)** 時間來建立
- 允許所有未來的子數組查詢在 **O(1)** 時間內完成

## 前綴和建構方式

### 方式一：prefix[0] = nums[0]

在這種建構方式中，前綴和數組的索引與原數組的索引對齊：

```cpp
// 方式一：prefix[0] = nums[0]
vector<int> prefix(nums.size());
prefix[0] = nums[0];
for (int i = 1; i < nums.size(); i++) {
    prefix[i] = prefix[i-1] + nums[i];
}
```

**優點**：
- 索引直觀，prefix[i] 對應 nums[0...i] 的和
- 實現簡單

**缺點**：
- 計算子數組和時需要特別處理起始索引為 0 的情況
- 計算 nums[i...j] 的和：
  - 當 i > 0 時：prefix[j] - prefix[i-1]
  - 當 i = 0 時：prefix[j]（需要特別處理以避免 i-1 越界）

### 方式二：prefix[0] = 0

在這種建構方式中，前綴和數組比原數組多一個元素，且 prefix[0] = 0：

```cpp
// 方式二：prefix[0] = 0
vector<int> prefix(nums.size() + 1, 0);
for (int i = 0; i < nums.size(); i++) {
    prefix[i + 1] = prefix[i] + nums[i];
}
```

**優點**：
- 計算任意子數組和時，可以統一使用 prefix[j] - prefix[i-1] 公式
- 不需要處理邊界情況

**缺點**：
- nums[i] 對應 prefix[i+1]，索引差 1
- 需要額外的一個元素空間

## 優化技巧

### 邊建構，邊操作

在建構前綴和數組的同時，可以進行比較和計算，而不需要等到整個前綴和數組建立完成後再進行操作。

```cpp
// 傳統方法：先建構，再操作
// 步驟 1: 建構前綴和
vector<int> prefix(nums.size() + 1, 0);
for (int i = 0; i < nums.size(); i++) {
    prefix[i + 1] = prefix[i] + nums[i];
}
// 步驟 2: 使用前綴和進行操作
for (int i = 0; i < prefix.size(); i++) {
    // 使用 prefix[i] 進行計算
}

// 優化方法：邊建構，邊操作
int prefixSum = 0;
for (int i = 0; i < nums.size(); i++) {
    prefixSum += nums[i];
    // 直接使用 prefixSum 進行計算
    // 例如，檢查是否存在特定和、更新結果等
}
```