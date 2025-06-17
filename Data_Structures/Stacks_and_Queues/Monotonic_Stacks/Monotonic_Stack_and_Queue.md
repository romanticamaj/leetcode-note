# Monotonic Stack and Queue

## 定義

**Monotonic**: 指一個函數或數量變化的方式使其要麼永不減少，要麼永不增加。
**Monotonic Stack/Queue**: 一種元素始終保持有序的數據結構。它可以是升序排列或降序排列。

## 特性

以 Sorted Monotonic Stack/Queue 為例，通過在添加新元素之前移除會違反有序性質的元素來維持其排序特性。這意味著：

- 在 monotonic increasing stack/queue 中，所有元素從底到頂（或從前到後）保持非遞減順序
  - e.g., [1, 2, 3, 3, 4]
- 在 monotonic decreasing stack/queue 中，所有元素從底到頂（或從前到後）保持非遞增順序
  - e.g., [3, 2, 2, 1]

## 實現方式

以下是維護 monotonic increasing stack 的偽代碼示例：

```
// 給定一個整數數組 nums
stack = []
for num in nums:
    // 當棧不為空且棧頂元素大於等於當前元素時，彈出棧頂元素
    while stack.length > 0 AND stack.top >= num:
        stack.pop()

    // 根據問題需求執行一些邏輯
    // ...

    stack.push(num)
```

** 當 `stack.top >= num` 會成立，可以想成目前最上面的元素在 num 加入後，會違反 monotonic increasing，所以可以開始整理 stack，即 pop 元素

對於 monotonic decreasing stack，只需修改比較條件：

```
while stack.length > 0 AND stack.top <= num:
    stack.pop()
```

** 當 `stack.top <= num` 會成立，同理，可以想成目前最上面的元素在 num 加入後，會違反 monotonic decreasing stack，所以可以開始整理 stack，即 pop 元素

### top 跟 num 的比較

特別注意要 maintain 的特性是：

- **Monotonic increasing (嚴格遞增)**:
  - 判斷條件是 `stack.top >= num`
  - 結果: [1, 3, 5, 7] (每個元素嚴格大於前一個)
  - 當棧頂元素大於等於當前元素時，彈出棧頂元素

- **Monotonic non-decreasing (非遞減)**:
  - 判斷條件是 `stack.top > num`
  - 結果: [1, 3, 3, 5, 7] (元素可以等於前一個)
  - 當棧頂元素大於當前元素時，彈出棧頂元素

- **Monotonic decreasing (嚴格遞減)**:
  - 判斷條件是 `stack.top <= num`
  - 結果: [7, 5, 3, 1] (每個元素嚴格小於前一個)
  - 當棧頂元素小於等於當前元素時，彈出棧頂元素

- **Monotonic non-increasing (非遞增)**:
  - 判斷條件是 `stack.top < num`
  - 結果: [7, 5, 3, 3, 1] (元素可以等於前一個)
  - 當棧頂元素小於當前元素時，彈出棧頂元素

可以用反向思考來理解這些條件：

例如，要維持 monotonic increasing (嚴格遞增)，棧中元素必須滿足 `stack.top < num`。當這個條件不成立時 (即 `!(stack.top < num)` 或 `stack.top >= num`)，我們需要彈出棧頂元素，直到條件成立或棧為空。

同理，要維持 monotonic decreasing (嚴格遞減)，棧中元素必須滿足 `stack.top > num`。當這個條件不成立時 (即 `!(stack.top > num)` 或 `stack.top <= num`)，我們需要彈出棧頂元素。

## 時間複雜度分析

儘管上述代碼中有嵌套循環，但時間複雜度仍然是 O(n)，其中 n 是數組的長度。這是因為內部 while 循環在所有 for 循環迭代中只能對每個元素進行一次迭代，使 for 循環迭代的平攤時間複雜度為 O(1)。

具體來說：
- 每個元素最多入棧一次
- 每個元素最多出棧一次
- 因此，所有操作的總數不超過 2n，時間複雜度為 O(n)

## 使用時機

Monotonic stack 和 queue 在以下情況特別有用：

1. **尋找下一個更大/更小元素**：對於數組中的每個元素，找到其右側第一個更大或更小的元素
2. **維護動態窗口中的最大/最小值**：當窗口變化時，需要快速知道窗口內的最大或最小元素
3. **解決特定模式的問題**：如直方圖中最大矩形面積、雨水收集等問題
4. **作為更複雜算法的一部分**：在某些高級問題中，單調棧或隊列可能只是算法的一個組成部分

## 常見應用示例

1. **下一個更大元素問題** (Next Greater Element)：找出數組中每個元素右側第一個比它大的元素
2. **直方圖中的最大矩形** (Largest Rectangle in Histogram)：計算直方圖中可能的最大矩形面積
3. **接雨水問題** (Trapping Rain Water)：計算能夠收集多少雨水
4. **滑動窗口最大值** (Sliding Window Maximum)：使用 monotonic queue 在滑動窗口中維護最大值

## 實現技巧

1. 明確是需要 monotonic increasing 還是 monotonic decreasing 的數據結構
2. 決定是使用 stack 還是 queue（通常基於問題是否需要保留順序）
3. 在處理元素時，考慮是否需要存儲元素的索引而不僅僅是值
4. 對於滑動窗口問題，通常使用 monotonic queue 更為合適

## Monotonic Deque

### 定義

**Monotonic Deque**: 一種可以從兩端添加和刪除元素，並且維持元素有序的數據結構。它是雙端隊列（double-ended queue）的一種變體，其元素保持單調性（遞增或遞減）。

### 特性

Monotonic Deque 結合了 monotonic stack 和 monotonic queue 的特性：

1. **雙端操作**: 可以在兩端進行元素的添加和刪除
2. **維持單調性**: 通過移除違反單調性的元素來保持整個結構的有序性
3. **靈活性**: 比 monotonic stack 和 monotonic queue 更靈活，可以根據需要從任一端操作

### 實現方式

Monotonic Deque 的實現可以基於標準的 deque 數據結構，並添加維護單調性的邏輯

### 應用場景

Monotonic Deque 特別適用於以下場景：

1. **滑動窗口最大/最小值問題**: 當窗口滑動時，需要高效地維護窗口內的最大或最小值
2. **需要雙端操作的單調性問題**: 某些問題需要從兩端維護單調性
3. **動態範圍查詢**: 在動態變化的數據集上進行範圍最值查詢

### 與其他單調數據結構的比較

| 特性 | Monotonic Stack | Monotonic Queue | Monotonic Deque |
|------|----------------|-----------------|-----------------|
| 插入操作 | 一端 | 一端 | 兩端 |
| 刪除操作 | 一端 | 一端 | 兩端 |
| 靈活性 | 低 | 中 | 高 |
| 常見應用 | 下一個更大元素 | 滑動窗口最值 | 複雜的滑動窗口問題 |

## 總結

Monotonic stack、queue 和 deque 是解決特定類型問題的強大工具，尤其是那些涉及尋找下一個更大/更小元素或維護動態窗口中最值的問題。雖然它們的實現相對簡單，但理解其背後的原理和適用場景對於有效地應用這些數據結構至關重要。根據問題的具體需求，選擇合適的單調數據結構可以顯著提高算法的效率。