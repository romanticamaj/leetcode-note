# Trie (字典樹) 使用心法與設計模式

## 核心思想：空間換時間與預處理

Trie 是一種以空間換取時間的樹狀資料結構，專為高效處理字串集合的前綴相關操作而設計。其核心思想是 **將查詢時間的複雜度與資料總量脫鉤，使其僅與查詢字串的長度相關**。

更進階的設計心法是 **在建構 (insertion) 階段進行預處理**，將未來查詢可能需要的資訊（如搜尋建議、計數等）預先計算並儲存在節點上。這種策略將複雜的查詢操作簡化為對預處理結果的快速讀取。

---

## 一、Trie 的建構邏輯

### 🧠 建構口訣 (Insertion Mantra)

> **「從根出發，逐字前進；無路則建，有路則行；抵達終點，標記完成。」**

> **traverse along the string and linked list**

**核心流程**:

1. **從 root 開始**，將當前節點指標初始化為 `root`
2. **逐字元遍歷字串**，對每個字元 `c`:
   - 檢查 `children[c]` 是否存在
   - **若不存在** → 創建新節點
   - **若存在** → 沿著指標前進
3. **字串結束時**，標記 `isEndOfWord = true` 或設定 `word` 欄位

**實作模板**:

```cpp
void insert(const string& word) {
    TrieNode* curr = root;                    // 1. 從根出發

    for (char c : word) {                     // 2. 逐字前進
        if (!curr->children[c]) {             //    無路則建
            curr->children[c] = make_unique<TrieNode>();
        }
        curr = curr->children[c].get();       //    有路則行
    }

    curr->isEndOfWord = true;                 // 3. 標記完成
    // 或使用進階設計: curr->word = word;
}
```

---

### 1. 標準 Trie 節點結構

一個泛用的 Trie 節點至少需要一個 `children` 結構來指向下一個字元節點。`std::unique_ptr` 能確保記憶體的自動化管理，而 `children` 的容器選擇則影響性能與彈性。

```cpp
#include <map>
#include <memory>
#include <string>
#include <vector>

struct TrieNode {
    // 子節點映射：從一個字元到對應的下一個 Trie 節點
    std::unordered_map<char, std::unique_ptr<TrieNode>> children;

    // 標記一個單字是否在此處結束
    bool isEndOfWord = false;
};
```

- **`children` 的容器選擇**:
  - `std::array<std::unique_ptr<TrieNode>, 26>`: 若字元集固定（如小寫英文字母），效能最佳且空間開銷固定。
  - `std::unordered_map`: 若不需按字元排序，平均效能更高（O(1)），是靈活性與性能的良好平衡。
  - `std::map`: 適用於任意字元集，寫法泛用，但有對數時間的開銷。

### 2. 帶有預處理資訊 (Pre-knowledge) 的節點

這是 Trie 強大之處的體現。我們可以在插入字串時，沿途更新節點上的資訊，將其作為未來查詢的快取。

```cpp
struct TrieNodeWithKnowledge {
    std::unordered_map<char, std::unique_ptr<TrieNodeWithKnowledge>> children;
    bool isEndOfWord = false;

    // --- 進階設計：預處理資訊欄位 ---

    // 1. 完整單字 (word):
    // 直接儲存完整單字而非只用布林值標記
    // 優點：在需要回傳完整單字時，無需重新建構路徑
    std::string word = "";  // 若非空字串，表示此節點為某單字的結尾

    // 2. 計數器 (Counter)
    int passCount = 0; // 有多少個單字經過此節點 (即以此為前綴)

    // 3. 建議快取 (Suggestion Cache)
    // 儲存經過此節點的單字範例，可用於自動補全
    std::vector<std::string> suggestions;

    // 4. 其他聚合資訊 (Aggregated Data)
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
- 執行複雜的模糊搜尋（例如，包含 `*` 或 `?` 的萬用字元匹配），因為這需要動態探索多條路徑。

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

### 3. Trie 與狀態空間探索的結合 (Trie + State Space Traversal)

這是一種進階技巧，將 Trie 作為**狀態導航器**，結合其他資料結構（如矩陣、圖）進行同步遍歷。

**核心思想**:

1. **建構 Trie**: 將所有目標字串預先建構成 Trie。
2. **同步遍歷**: 從 Trie 的 `root` 節點出發，在探索問題空間（如矩陣的 DFS）時，同步追蹤當前在 Trie 中的位置。
3. **狀態轉移**: 每次移動到新位置時，根據當前字元嘗試在 Trie 中前進。若無法前進（子節點不存在），則提前剪枝；若到達 `isEndOfWord` 或 `word` 非空的節點，則找到一個匹配。

**類似概念**: 可以將 Trie 想像成一個**多分支的鏈表**，在遍歷問題空間時，我們同步沿著 Trie 的指針前進，利用 Trie 的結構來高效地過濾無效路徑。

參考範例：

- **LeetCode 212. Word Search II**

### 4. 動態 Trie：遍歷時修剪搜尋空間 (Dynamic Trie - Pruning While Traversing)

當問題只需檢查 **存在性** 而非收集所有結果時，可以在找到答案後立即從 Trie 中移除該路徑，避免重複搜尋。

需搭配 `unordered_map<char, unique_ptr<TrieNode>>` 來做 erase

**核心思想**:

> **「Trie 即搜尋空間；找到即刪除；已訪問不再訪。」**

- **Trie 作為動態搜尋空間**: 將 Trie 視為待搜尋的候選集合
- **找到後立即剪枝**: 一旦匹配成功，清空該節點的 `word` 欄位或刪除該 TrieNode

```cpp
    node->word = "";  // ✂️ 剪枝：清空 word，避免重複收集`
```

```cpp
// ✂️ 進階剪枝：若子樹已空且無單字結尾，可刪除整個節點
if (node->children.empty() && node->word.empty()) {
    parent->children.erase(c);  // 需額外追蹤 parent
}
```

- **避免重複檢查**: 已找到的路徑不會在後續遍歷中被重複訪問

**適用場景**:

- 在矩陣/圖中搜尋多個不重複的字串（如 LeetCode 212）
- 需要去重的字串匹配問題
- 搜尋空間會隨著找到答案而縮小的情境

**剪枝策略比較**:

| 策略         | 實作方式         | 效果                         | 複雜度    |
| ------------ | ---------------- | ---------------------------- | --------- |
| **輕量剪枝** | 清空 `word` 欄位 | 避免重複收集，但節點仍存在   | O(1)      |
| **完全剪枝** | 刪除整個子樹節點 | 釋放記憶體，減少後續遍歷分支 | O(節點數) |

**口訣**: **「找到即標記，用過即捨棄。」**

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

- 上述分析基於使用 `std::array` 或 `std::unordered_map` (`O(1)` 查找) 的理想情況。
- 若使用 `std::map`，每次存取子節點會產生 `O(log|Σ|)` 的開銷。因此，所有操作的複雜度需乘上此因子，例如插入變為 `O(L * log|Σ|)`。

---

### 空間複雜度 (Space Complexity)

- **節點結構**: `O(N * L)`。在最壞情況下（所有單字沒有任何共同前綴），總節點數約等於所有單字的總字元數。在最佳情況下（大量單字共享長前綴），空間會被有效節省。
- **額外開銷**: 預處理資訊（如 `suggestions` 快取）會增加額外的空間複雜度，需另行計算。
