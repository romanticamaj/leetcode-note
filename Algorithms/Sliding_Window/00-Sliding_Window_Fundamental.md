# Sliding Window 技巧

## 要點

1. **window** 表示 subarray
2. 維持兩個 index - **left** and **right**
3. **right** 會增加，讓 window 變大; **left** 會增加，讓 window 變小
4. sliding window 長度是 **`right - left + 1`**
5. 因為 **right** 會不斷的增加，所以 window 會 **slide**
6. **constraint metric** 會決定要做什麼 window 的"特性"判斷, 例如 sum, 出現的數字個數等等
7. 通常問題會給一個 array，去找到滿足 **contraint metric** 某個特性的 subarray

## 通用模板

```
function fn(arr):
    for (int left, int right = 0; right < arr.length; right++):
        Do some logic to "add" element at arr[right] to window

        while WINDOW_IS_INVALID:
            Do some logic to "remove" element at arr[left] from window
            left++

        Do some logic to update the answer
```

## 特定類型

### Fixed window size

- 在右側添加一個元素，同時在左側移除一個元素以維持窗口長度不變。

**小訣竅**：

- 當添加位置 i 的元素時，被移除的元素一定在 `i-k` 位置（k 是窗口大小）
- 這樣就可以省略顯式追蹤 left 的 index

## 進階技巧

### Sliding Window 與 Hashmap 結合

Sliding Window 有機會跟 hashmap 結合，用於追蹤窗口內元素的頻率或其他特性，特別適用於需要統計窗口內不同元素出現次數的問題。

#### 實現方式

- Hashmap (e.g., unordered_map) 用於記錄窗口內的 **constraint metric**
- 這個 constraint metric 作為 `while WINDOW_IS_INVALID` 的比較來源
- 當右指針移動時，更新 hashmap 中的頻率計數
- 當窗口無效時，移動左指針並相應地更新 hashmap

#### 常見應用場景

- 限制窗口內不同字符的數量
- 限制窗口內元素出現的最大/最小頻率
- 要求窗口內的元素滿足特定的頻率分佈
- 查找包含特定元素集合的最小窗口
