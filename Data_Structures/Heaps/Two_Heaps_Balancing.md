# 心法：雙堆平衡模式 (Two-Heaps Balancing Pattern)

## 1. 適用場景

此模式適用於需要將一個動態的資料流劃分為**有序的兩組**，並在任何時候都能快速訪問這兩組邊界處的元素。最典型的應用是：

- **尋找中位數 (Median Finding)**：如 LeetCode 295. Find Median from Data Stream。
- **維護滑動窗口的中位數**：如 LeetCode 480. Sliding Window Median。
- **需要快速訪問分割點的問題**：任何需要將集合分為「Top N」和「Bottom M」並快速查詢邊界值的問題。

## 2. 核心思想：維護不變式 (Maintaining Invariants)

雙堆模式的核心是利用兩個堆（一個大根堆，一個小根堆）來共同維護兩個**不變式**：

1. **分割不變式 (Partition Invariant)**：定義兩組資料之間的**數值關係**。通常是：大根堆 `small_half` 中的所有元素，都小於或等於小根堆 `large_half` 中的所有元素。
2. **平衡不變式 (Balance Invariant)**：定義兩組資料之間的**數量關係**。通常是：兩個堆的大小相等，或其中一個只比另一個多一個元素。

為了在動態插入新元素時維持這兩個不變式，我們採用一個固定的三步操作序列：「**插入 → 轉移 → 再平衡**」。

## 3. 三步操作詳解 (Insert → Transfer → Rebalance)

這個固定的三步流程，是「先污染，後治理」思想的體現，它保證了在每次操作結束後，系統都能回到滿足不變式的穩定狀態。

| 步驟                      | 操作                                                                                       | 目的與效果                                                                                                   |
| :------------------------ | :----------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| **1. Insert (插入)**      | 將新元素 `num` 無條件插入其中一個堆（例如，主要組 `small_half`）。                         | 引入新元素。這一步**可能會暫時打破分割不變式**（如果 `num` 其實屬於另一組）。                                |
| **2. Transfer (轉移)**    | 從剛插入的堆中取出其極端值，轉移到另一個堆。                                               | **恢復「分割不變式」**。這是模式的精髓，它強制將不屬於該組的元素「校正」到正確的組，從而恢復了兩組間的順序。 |
| **3. Rebalance (再平衡)** | **有條件地**檢查兩個堆的大小，若不滿足平衡不變式，則從較大的堆中取出極端值，移回較小的堆。 | **恢復「平衡不變式」**。在不破壞分割的前提下，恢復兩組的大小關係。                                           |

## 4. 案例：動態資料流的中位數 (LeetCode 295)

- **結構**：
  - `small_half` (大根堆)：存放較小的一半數字。其堆頂是前半部分的最大值。
  - `large_half` (小根堆)：存放較大的一半數字。其堆頂是後半部分的最小值。
- **流程 `addNum(int num)`**：
  1. **Insert**: 將新元素 `num` 推入 `small_half` (大根堆)。
  2. **Transfer**: 立即將 `small_half` 的頂點（最大值）`pop` 出，並 `push` 到 `large_half` (小根堆)。這一步確保了任何新加入的數字，如果它真的很大，會被立刻送到 `large_half`。
  3. **Rebalance**: 檢查大小。如果 `small_half` 的大小變得比 `large_half` 小，就從 `large_half` 的頂點（最小值）`pop` 出，並 `push` 回 `small_half`，以維持大小平衡。

```cpp
class MedianFinder {
private:
    std::priority_queue<int> small_half; // Max-heap
    std::priority_queue<int, std::vector<int>, std::greater<int>> large_half; // Min-heap
public:
    void addNum(int num) {
        // 1. Insert into the "default" heap
        small_half.push(num);

        // 2. Transfer the largest from small_half to large_half
        // This move ensures the Partition Invariant is restored.
        large_half.push(small_half.top());
        small_half.pop();

        // 3. Rebalance the sizes if necessary
        // This move ensures the Balance Invariant is restored.
        if (small_half.size() < large_half.size()) {
            small_half.push(large_half.top());
            large_half.pop();
        }
    }

    double findMedian() {
        if (small_half.size() > large_half.size()) {
            return small_half.top();
        }
        return (small_half.top() + large_half.top()) / 2.0;
    }
};
```
