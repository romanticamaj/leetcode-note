# Trie (字典樹) 使用心法與設計模式

## 核心思想：空間換時間與預處理

Trie 是一種以空間換取時間的樹狀資料結構，專門用於高效處理字串集合的前綴相關操作。其核心思想是 **將查詢時間的複雜度與資料總量脫鉤，僅與查詢字串的長度相關**。

更進一步的設計心法是 **在建構 (insertion) 階段進行預處理**，將未來可能需要的資訊（如搜尋建議、計數等）儲存在節點上，從而將複雜的查詢操作簡化為快速的預處理結果讀取。

---

## 一、Trie 的建構邏輯

### 1. 標準 Trie 節點結構

一個泛用的 Trie 節點至少需要一個 `children` 結構來指向下一個字元節點。使用 `std::map` 具有最好的靈活性，而 `std::unique_ptr` 則能確保記憶體的自動化管理。

```cpp
#include <map>
#include <memory>
#include <string>
#include <vector>

struct TrieNode {
    // 子節點映射：從一個字元到對應的下一個 Trie 節點
    std::map<char, std::unique_ptr<TrieNode>> children;

    // 標記一個單字是否在此處結束
    bool isEndOfWord = false;
};
```

- **`children` 的選擇**:
  - `std::map`: 適用於任意字元集，寫法泛用。
  - `std::unordered_map`: 若不需按字元排序，平均效能可能更高。
  - `std::array<std::unique_ptr<TrieNode>, 26>`: 若字元集固定為小寫英文字母，效能最佳且空間開銷固定。

### 2. 帶有預處理資訊 (Pre-knowledge) 的節點

這是 Trie 強大之處的體現。我們可以在插入字串時，沿途更新節點上的資訊，將其作為未來查詢的快取。

```cpp
struct TrieNodeWithKnowledge {
    std::map<char, std::unique_ptr<TrieNodeWithKnowledge>> children;
    bool isEndOfWord = false;

    // --- 預處理資訊欄位 ---

    // 1. 計數器 (Counter)
    int passCount = 0; // 有多少個單字經過此節點 (即以此為前綴)

    // 2. 建議快取 (Suggestion Cache)
    // 儲存經過此節點的單字範例，可用於自動補全
    std::vector<std::string> suggestions;

    // 3. 其他聚合資訊 (Aggregated Data)
    // 例如：與此節點相關的資料 ID 列表、權重、最小值等
    std::vector<int> dataIDs;
};
```

**建構心法**: 在 `insert` 操作中，每經過一個節點，就必須更新該節點的預處理資訊。例如，`passCount` 加一，或將當前單字加入 `suggestions` 列表（可能需要維護一個固定大小的 Top-K 列表）。

---

## 二、Trie 的遍歷 (Walk) 策略

遍歷 Trie 主要有兩種策略，取決於查詢的資訊是否已在建構時預處理。

### 1. 動態遍歷 (Dynamic Traversal / On-the-fly DFS)

當查詢的資訊無法預處理，或需要取得某前綴下的 **所有** 對應單字時使用。

**作法**:

1. **Walk to Prefix**: 先沿著查詢前綴走到對應的節點。
2. **DFS from Node**: 從該節點開始，使用深度優先搜尋 (DFS) 遍歷其下的所有子樹，收集所有 `isEndOfWord` 為 `true` 的路徑。

**適用場景**:

- 取得前綴下的所有單字。
- 執行複雜的模糊搜尋 (e.g., `*` or `?` wildcards)，因為這需要動態探索多條路徑。

### 2. 預處理資訊查詢 (Querying Pre-processed Data)

這是最高效的查詢方式，直接利用建構時儲存的資訊。

**作法**:

1. **Walk to Prefix**: 沿著查詢前綴走到對應的節點。
2. **Direct Read**: 直接讀取該節點上的欄位，如 `passCount`, `suggestions`, `dataIDs`。

**適用場景**:

- 查詢前綴出現次數 (`prefixCount`)。
- 取得自動補全建議 (`getSuggestions`)。
- 獲取與前綴相關的資料 ID。

**心法**: **盡可能將查詢模型化為對預處理資訊的讀取**。如果一個查詢模式會被頻繁使用，就應該考慮在 `TrieNode` 中增加一個欄位來快取其結果。

---

## 三、時間與空間複雜度分析

### 變數定義

- **N**: 字典中的單字總數。
- **L**: 單字的平均長度。
- **k**: 查詢前綴的長度 (`k <= L`)。
- **Σ**: 字元集的大小 (e.g., 26 for lowercase English letters)。

---

### 時間複雜度 (Time Complexity)

下表展示了基本操作的複雜度。注意，複雜度主要取決於字串長度，而非單字總數 N。

| 操作                       | 時間複雜度 | 說明                                  |
| :------------------------- | :--------- | :------------------------------------ |
| **插入單字 (Insert)**      | `O(L)`     | 需沿著長度為 L 的路徑遍歷或創建節點。 |
| **搜尋單字 (Search)**      | `O(L)`     | 同上，沿著長度為 L 的路徑查找。       |
| **前綴查詢 (Prefix Walk)** | `O(k)`     | 僅需遍歷長度為 k 的前綴路徑。         |
| **建構整棵樹**             | `O(N * L)` | 將 N 個平均長度為 L 的單字全部插入。  |

**關於 `children` 實現的影響**:

- 上述分析基於使用 `std::array` (`O(1)` 查找) 的理想情況。
- 若使用 `std::map`，每次存取子節點會產生 `O(log|Σ|)` 的開銷。因此，所有操作的複雜度需乘上此因子，例如插入變為 `O(L * log|Σ|)`。

---

### 空間複雜度 (Space Complexity)

- **節點結構**: `O(N * L)`。在最壞情況下（所有單字沒有任何共同前綴），總節點數約等於所有單字的總字元數。在最佳情況下（大量單字共享長前綴），空間會被有效節省。
- **額外開銷**: 預處理資訊（如 `suggestions` 快取）會增加額外的空間複雜度，需另行計算。
