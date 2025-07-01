# 心法：堆的設計模式 (Heap Design Patterns)

`std::priority_queue`（堆）不僅僅是一個找到最大/最小值的工具，更是實現複雜邏輯的優雅基石。本文件從基礎的「Push-Pop」模式出發，延伸至更高級的「雙堆不變式」模式，展示如何利用堆的自平衡特性簡化程式碼。

## 模式一：Push-Pop 簡化模式

**適用場景**：需要動態維護一個**固定大小**的有界集合（例如 Top-K 問題）。

**核心思想**：**`信任並利用堆的自平衡特性`**，將「有條件的插入」轉化為固定的「**先插入，後平衡**」操作序列。

- **傳統思路 (條件式插入)**：先檢查集合大小和元素優劣，再決定是否替換。邏輯分支多，易出錯。
- **Push-Pop 模式 (無條件插入與平衡)**：
  1. **`push` 新元素**：無條件將新元素推入堆中 (`O(log k)`)。
  2. **`pop` 多餘元素**：若堆的大小超過 `k`，立即 `pop` 堆頂 (`O(log k)`)。

這個模式用固定的兩步操作取代了複雜的 `if-else`，程式碼更簡潔、可讀性更高。

### 案例：Top K Frequent Elements (LeetCode 347)

使用一個大小為 `k` 的小根堆 (min-heap) 來維護頻率最高的 `k` 個元素。

```cpp
// Push-Pop 模式：先操作，後平衡
std::priority_queue<std::pair<int, int>,
                    std::vector<std::pair<int, int>>,
                    std::greater<std::pair<int, int>>> q;

for (auto [num, frequency] : countingMap) {
    // 步驟 1: 無條件 push，讓 heap 維護順序
    q.push({frequency, num});

    // 步驟 2: 如果超出大小，無條件 pop，移除當前集合中頻率最小的元素
    if (q.size() > k) {
        q.pop();
    }
}
```

---

## 模式二：雙堆不變式模式 (Two Heaps Invariant Pattern)

這是 Push-Pop 模式的延伸，適用於需要將資料流動態劃分為**兩組**，並同時維護兩組間**順序關係**和**大小平衡**的場景。

**核心思想**：將單一的「Push-Pop」擴展為跨越兩個堆的「**Insert → Transfer → Rebalance**」三步固定流程，用以維護兩個核心不變式。

### 兩個不變式 (Invariants)

1. **分割不變式 (Partition Invariant)**：定義兩組資料之間的**數值關係**（例如，A 組所有元素 ≤ B 組所有元素）。
2. **平衡不變式 (Balance Invariant)**：定義兩組資料之間的**數量關係**（例如，A 組與 B 組大小差距 ≤ 1）。

### 三步操作詳解

| 步驟                      | 操作                                                   | 目的與效果                                                         |
| :------------------------ | :----------------------------------------------------- | :----------------------------------------------------------------- |
| **1. Insert (插入)**      | 將新元素 `num` 無條件插入「主要組」。                  | 引入新元素，可能會**暫時打破不變式**。                                 |
| **2. Transfer (轉移)**    | 從「主要組」取出其極端值，轉移到「次要組」。           | **恢復「分割不變式」**。這是模式的精髓，強制恢復了兩組間的順序。   |
| **3. Rebalance (再平衡)** | **有條件地**從「次要組」取出其極端值，移回「主要組」。 | **恢復「平衡不變式」**。在不破壞分割的前提下，恢復兩組的大小關係。 |

### 案例：動態資料流的中位數 (LeetCode 295)

- **結構**：
  - `small_half` (大根堆)：存放較小的一半數字。
  - `large_half` (小根堆)：存放較大的一半數字。
- **流程**：
  1. **Insert**: 將新元素推入主要組（大根堆）。(`O(log N)`)
  2. **Transfer**: 將主要組的頂點（最大值）轉移至次要組（小根堆）。(`O(log N)`)
  3. **Rebalance**: 若次要組大小超過主要組，將次要組的頂點（最小值）移回主要組。(`O(log N)`)

```cpp
class MedianFinder {
private:
    std::priority_queue<int> small_half; // Max-heap
    std::priority_queue<int, std::vector<int>, std::greater<int>> large_half; // Min-heap
public:
    void addNum(int num) {
        // Insert
        small_half.push(num);

        // Transfer
        large_half.push(small_half.top());
        small_half.pop();

        // Rebalance
        if (small_half.size() < large_half.size()) {
            small_half.push(large_half.top());
            large_half.pop();
        }
    }
    // ... findMedian() ...
};
```

### 總結

「Push-Pop」模式是利用堆自平衡簡化邏輯的基礎。

當問題從維護一個集合擴展到維護兩個有關聯的集合時，「Insert → Transfer → Rebalance」三步法提供了一個強大、通用且優雅的解決方案。

這種「先污染，後治理」的策略，是演算法設計中一種非常高級的技巧。
