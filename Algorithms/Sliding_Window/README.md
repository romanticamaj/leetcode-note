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