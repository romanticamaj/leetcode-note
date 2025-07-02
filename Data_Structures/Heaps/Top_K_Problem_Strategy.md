# 心法：使用 Priority Queue 解決 Top-K 問題

「Top-K」問題（例如，找到最大的 K 個元素）是面試和競賽中非常常見的題型。使用 `std::priority_queue`（堆）是解決這類問題最優雅、最高效的方法之一。本文件將深入探討其核心策略、複雜度分析以及如何利用「Push-Pop」技巧寫出簡潔的程式碼。

---

## 1. 核心思想：維護一個大小為 K 的「擂台」

解決 Top-K 問題的關鍵，不是對整個資料集進行完全排序，而是只維護一個大小為 K 的「候選區」。這個候選區就像一個擂台，只有最強的 K 個選手能留在上面。每當一個新的挑戰者出現時，我們將其與擂台上「最弱」的選手進行比較，以決定挑戰者是否有資格上場。

`std::priority_queue` 正是實現這個「擂台」的完美工具。

## 2. 關鍵決策：Min-Heap 還是 Max-Heap？

這是最核心的策略點，選擇取決於你的目標是「最大的 K 個」還是「最小的 K 個」。

### 場景一：找到「最大的 K 個」元素 (Top K Largest)

- **擂台規則**：我們需要淘汰掉擂台上「最小」的選手，以便為更強的（更大的）選手騰出位置。
- **對應工具**：**Min-Heap (小根堆)**。
- **運作方式**：
  1. 建立一個 Min-Heap，`top()` 會是當前 K 個元素中最小的那個（即擂台上最弱的選手）。
  2. 遍歷資料流，對於每個新元素 `num`：
     - 如果堆的大小還不到 K，直接將 `num` 推入。
     - 如果堆的大小已滿（為 K），將 `num` 與堆頂 `minHeap.top()` 比較。
     - 如果 `num` 比堆頂更大，表示 `num` 比擂台上最弱的選手還強，有資格上場。因此，彈出堆頂（淘汰最弱者），並推入 `num`。

### 場景二：找到「最小的 K 個」元素 (Top K Smallest)

- **擂台規則**：我們需要淘汰掉擂台上「最大」的選手，以便為更強的（更小的）選手騰出位置。
- **對應工具**：**Max-Heap (大根堆)**。
- **運作方式**：
  1. 建立一個 Max-Heap，`top()` 會是當前 K 個元素中最大的那個。
  2. 遍歷資料流，對於每個新元素 `num`：
     - 如果 `num` 比堆頂更小，表示 `num` 比擂台上最弱的（即最大的）選手還強，有資格上場。因此，彈出堆頂，推入 `num`。

---

## 3. 「Push-Pop」策略：簡化程式碼的藝術

上述的條件判斷邏輯（`if (heap.size() < k)`... `else if (num > heap.top())`...）雖然直觀，但可以被一個更簡潔的模式取代：「Push-Pop」。

這個策略的核心是：**先無條件加入，再淘汰**。

### 實現方式

以「Top K Largest」（使用 Min-Heap）為例：

```cpp
#include <queue>
#include <vector>
#include <functional>

std::vector<int> findTopKLargest(const std::vector<int>& nums, int k) {
    // 使用 Min-Heap 來找到最大的 K 個元素
    std::priority_queue<int, std::vector<int>, std::greater<int>> minHeap;

    for (int num : nums) {
        // Push-Pop 策略
        minHeap.push(num);
        if (minHeap.size() > k) {
            minHeap.pop(); // 淘汰掉當前 K+1 個元素中最小的那個
        }
    }

    // 將結果從 heap 轉移到 vector
    std::vector<int> result;
    while (!minHeap.empty()) {
        result.push_back(minHeap.top());
        minHeap.pop();
    }
    return result;
}
```

**優點**：

- **程式碼極簡**：消除了複雜的 `if-else` 分支，邏輯更清晰。
- **職責單一**：迴圈只負責將元素送入堆，堆自身則負責維護大小為 K 的候選區。

---

## 4. 複雜度分析

假設資料集大小為 N。

- **時間複雜度**：**O(N log K)**
  - 我們需要遍歷 N 個元素。
  - 對於每個元素，我們執行一次 `push` 操作，其時間複雜度為 O(log K)，因為堆的大小最多為 K+1。
  - `pop` 操作同樣是 O(log K)。
  - 因此，總時間複雜度為 O(N * log K)。這遠比完全排序的 O(N log N) 要高效。

- **空間複雜度**：**O(K)**
  - 我們需要一個大小為 K 的堆來儲存候選元素。

## 總結

使用 `priority_queue` 搭配「Push-Pop」策略是解決 Top-K 問題的標準最佳實踐。它在時間和空間效率上取得了絕佳的平衡，同時程式碼極其簡潔，易於在面試等高壓環境下正確實現。
