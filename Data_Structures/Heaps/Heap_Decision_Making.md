# Heap 使用場景的關鍵決策點

在使用堆（Heap），特別是 C++ 中的 `std::priority_queue` 來解決問題時，通常需要回答以下兩個關鍵問題：

---

## 1. 該用 Min-Heap 還是 Max-Heap？

選擇的依據是「**你想淘汰什麼樣的元素**」。`top()` 操作是用來檢視「最不符合要求」或「最優先被淘汰」的那個元素。

- **Max-Heap (大根堆)**：`top()` 是最大值。適用於需要**淘汰最大元素**的場景。
  - **經典問題：Top K Smallest Elements (前 K 小元素)**
    - **目標**：維護一個大小為 K 的集合，其中包含目前為止遇到的最小的 K 個元素。
    - **策略**：使用 Max-Heap，並利用「Push-Pop」策略。無條件將新元素推入堆，然後檢查堆的大小。如果超過 K，就彈出堆頂元素（即當前 K+1 個元素中的最大值）。
    - **關鍵邏輯**：無條件地將新元素加入堆中，然後立即檢查堆的大小。如果大小超過 K，就移除堆頂的元素（即當前 K+1 個元素中的最大值），從而動態維護著整個資料流中最小的 K 個元素。

- **Min-Heap (小根堆)**：`top()` 是最小值。適用於需要**淘汰最小元素**的場景。
  - **經典問題：Top K Largest Elements (前 K 大元素)**
    - **目標**：維護一個大小為 K 的集合，其中包含目前為止遇到的最大的 K 個元素。
    - **策略**：同樣使用「Push-Pop」策略。無條件將新元素推入 Min-Heap，如果堆的大小超過 K，就彈出堆頂元素（即當前 K+1 個元素中的最小值）。
    - **關鍵邏輯**：與尋找最小 K 個元素相同，但方向相反。無條件加入新元素，若堆大小超過 K，則移除堆頂（即當前 K+1 個元素中的最小值），從而保留最大的 K 個元素。
  - **其他應用**：
    - **Dijkstra 演算法**：從所有待處理的節點中，找到距離源點最近（權重最小）的節點。
    - **事件驅動模擬**：從事件佇列中，找到最先發生（時間戳最小）的事件。
    - **合併 K 個排序好的串列 (Merge K Sorted Lists)**：從 K 個串列的頭部元素中，找到最小的那個。

---

## 2. Priority Key 和 Comparator 如何決定？

堆中元素的排序依據（Priority Key）和比較方式（Comparator）是解決問題的核心。

- **Priority Key 的選擇**：

  - Key 通常是**最佳化問題的衡量標準**。例如，在 Dijkstra 中，key 是「從起點到該節點的距離」；在 A\* 演算法中，key 是 `f(n) = g(n) + h(n)`。
  - 當排序標準是複合的，例如「按距離排序，若距離相同則按字母序」，可以使用 `std::pair` 或自訂結構體。

- **使用 `std::pair` 的技巧與陷阱 (C++)**：

  - `std::pair` 的預設比較器 `std::less` 會先比較 `first` 元素，如果 `first` 相同，再比較 `second` 元素。
  - **常見用法**：將主要的排序依據放在 `pair.first`。例如，`std::pair<int, char>`，預設會按 `int` 值排序。
  - **陷阱**：如果你的主要排序依據是 `pair.second`，或者你需要反向排序，那麼預設的比較器就不適用了。此時，你必須提供一個自訂的比較器（通常是 Lambda 或 Functor）。

  ```cpp
  // 範例：按 pair 的 second 元素（降序）排序
  auto cmp = [](const auto& a, const auto& b) {
      return a.second < b.second; // 產生 Max-Heap
  };
  std::priority_queue<
      std::pair<char, int>,
      std::vector<std::pair<char, int>>,
      decltype(cmp)
  > pq(cmp);

  pq.push({'A', 10});
  pq.push({'B', 30});
  pq.push({'C', 20});

  // top() 會是 {'B', 30}
  ```
