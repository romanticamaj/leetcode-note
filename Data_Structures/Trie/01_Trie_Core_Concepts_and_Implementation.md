# Trie (前綴樹) 實作與分析

Trie，其名稱源於「re**trie**val」（檢索）一詞，凸顯了其在資料快速檢索方面的優勢。它也被廣泛稱為**前綴樹 (Prefix Tree)**，是一種專為高效處理字串集合而設計的樹狀資料結構。

## Trie 核心概念泛化分析

在深入探討具體實作之前，從一個更宏觀的角度來理解 Trie 的設計哲學至關重要。Trie 的核心由以下三個關鍵概念構成：

### 1. TrieNode 的鏈式結構

Trie 本質上是一種 N 元樹（N-ary Tree）。每個 `TrieNode` 代表序列中的一個字元或步驟。其設計的核心在於其子節點的集合，這個集合可被視為一個「鏈」。此鏈可以是固定大小的（如陣列），也可以是動態大小的（如雜湊表或平衡樹）。

### 2. 子節點集合的資料結構選擇

儲存子節點的方式是 Trie 設計中的一個關鍵決策，直接影響其性能、空間使用及功能。選擇取決於字母表的大小以及是否需要按字典序排序。

- **`std::vector` 或 C-style 陣列**：適用於固定且較小的字母表（例如，僅小寫英文字母 'a'-'z'）。透過字元值的直接索引提供 **O(1)** 的最快訪問速度。
- **`std::unordered_map`**：適用於龐大或動態的字母表（例如，所有 ASCII 或 Unicode 字元）。提供平均 **O(1)** 的訪問時間，但子節點之間不保證任何順序。
- **`std::map`**：當需要按字典序儲存子節點時使用。提供 **O(log k)** 的訪問時間，其中 `k` 是該節點的分支因子（子節點數量）。這對於需要按字母順序排序的自動完成功能特別有用。

### 3. 節點元數據：`isEndOfWord`

並非 Trie 中的每個節點都代表一個有效單字的結束；許多節點僅是某個前綴的一部分。為了區分這兩者，每個 `TrieNode` 都必須包含元數據（Metadata），最常見的就是一個布林標記，通常命名為 `isEndOfWord`。

- `isEndOfWord = true`：表示此節點為一個已插入的有效單字的最後一個字元。
- `isEndOfWord = false`：表示此節點僅為一個或多個單字路徑上的一部分，即一個「路徑節點」或「前綴節點」。

這種區分對於 `search` 操作至關重要，使其能夠正確地區分完整單字和單純的前綴。

---

## 核心實作 (動態字母表)

此實作採用 `std::unordered_map` 來儲存子節點，使其能靈活應對任何字元集，包括 ASCII、Unicode 等。

```cpp
#include <string>
#include <unordered_map>
#include <memory>

class Trie {
private:
    struct TrieNode {
        std::unordered_map<char, std::unique_ptr<TrieNode>> children;
        bool isEndOfWord;

        TrieNode() : isEndOfWord(false) {}
    };

    TrieNode root;

public:
    Trie() {}

    // 插入一個單字到 Trie 中
    void insert(const std::string& word) {
        TrieNode *current = &root;
        for (char w : word) {
            if (current->children.find(w) == current->children.end()) {
                current->children[w] = std::make_unique<TrieNode>();
            }
            current = current->children[w].get();
        }
        current->isEndOfWord = true;
    }

    // 搜尋一個單字是否存在於 Trie 中
    bool search(const std::string& word) {
        TrieNode *current = query(word);
        return current && current->isEndOfWord;
    }

    // 檢查是否有任何單字以指定的前綴開頭
    bool startsWith(const std::string& prefix) {
        return query(prefix) != nullptr;
    }

private:
    // 查詢前綴並返回其結尾節點
    TrieNode* query(const std::string& prefix) {
        TrieNode *current = &root;
        for (char p : prefix) {
            if (current && current->children.count(p)) {
                current = current->children[p].get();
            } else {
                return nullptr;
            }
        }
        return current;
    }
};
```

### 程式碼分析

- **`TrieNode`**: 此結構表示 Trie 中的每個節點。
  - `children`: 一個 `unordered_map`，其鍵是字元，值是指向子 `TrieNode` 的 `unique_ptr`，用於自動管理記憶體。
  - `isEndOfWord`: 一個布林標記，表示該節點是否為一個完整單字的結尾。
- **`root`**: Trie 的根節點，作為所有字串的起始點。
- **`insert(word)`**: 此函數遍歷輸入 `word` 的每個字元，並沿著樹向下遍歷。若路徑不存在，則創建新節點。最後，將字串的最終節點標記為 `isEndOfWord`。
- **`query(prefix)`**: 一個輔助函數，根據 `prefix` 遍歷 Trie。若前綴存在，則返回其結尾節點的指標；否則返回 `nullptr`。
- **`search(word)`**: 使用 `query` 尋找對應於 `word` 的節點，並檢查其 `isEndOfWord` 標記是否為 `true`。
- **`startsWith(prefix)`**: 使用 `query` 檢查前綴路徑是否存在於 Trie 中，不論其是否為完整單字。

### 時間複雜度分析

主要操作的時間複雜度取決於字串的長度 `L`。

- **`insert(word)`**: **O(L)**。對於單字中的每個字元（長度為 `L`），在 `unordered_map` 中執行一次平均 O(1) 的查找或插入。因此，總時間與單字長度成正比。
- **`search(word)`**: **O(L)**。與插入類似，遍歷樹 `L` 個字元，每一步平均是 O(1) 的雜湊表查找。
- **`startsWith(prefix)`**: **O(L)**。邏輯與搜索相同，其中 `L` 是前綴的長度。

值得注意的是，若 `children` 改用 `std::map` 實作，由於 `std::map` 的單次查找時間複雜度為 `O(log Σ)`（其中 `Σ` 為 map 中的字元分支數），則 `insert`、`search` 等操作的總時間複雜度將變為 **O(L \* log Σ)**。

## 固定字元集實作

當字元集已知且受限時（例如，僅小寫英文字母 'a'-'z'），我們可以用固定大小的陣列替換 `unordered_map`，以獲得更好的性能和空間效率。

```cpp
#include <string>
#include <vector>
#include <memory>

class TrieFixed {
private:
    static const int ALPHABET_SIZE = 26;

    struct TrieNode {
        std::vector<std::unique_ptr<TrieNode>> children;
        bool isEndOfWord;

        TrieNode() : children(ALPHABET_SIZE), isEndOfWord(false) {}
    };

    TrieNode root;

public:
    TrieFixed() {}

    void insert(const std::string& word) {
        TrieNode* current = &root;
        for (char ch : word) {
            int index = ch - 'a';
            if (!current->children[index]) {
                current->children[index] = std::make_unique<TrieNode>();
            }
            current = current->children[index].get();
        }
        current->isEndOfWord = true;
    }

    // search 和 startsWith 方法可依此類推進行修改
};
```

### 固定字元集版本分析

- **性能**: 由於直接使用陣列索引（`O(1)`）而非雜湊，此版本通常更快，並受益於更好的快取局部性。
- **空間**: 若 Trie 結構稀疏（即多數節點只有少量子節點），空間複雜度會更高，因為每個節點都為所有可能的字元預先分配了空間。然而，對於密集的 Trie，它可以透過避免 map 結構的額外開銷而更節省空間。

## 應用場景

Trie（前綴樹）是一種高效的樹狀資料結構，特別適用於從字串資料集中檢索鍵。以下是其一些關鍵應用：

- **自動完成 (Autocomplete)**: 如搜尋引擎的建議功能。
- **拼字檢查 (Spell Checker)**: 如文書處理器中的拼寫校正。
- **IP 路由 (最長前綴匹配)**: 用於網路路由表中，根據最長匹配前綴選擇路由。
- **T9 預測文本**: 用於舊式手機的九宮格鍵盤輸入法。
- **解決文字遊戲**: 如在 Boggle 遊戲中高效地尋找所有可能的單字。

雖然平衡樹和雜湊表等資料結構也可用於搜索單字，但 Tries 在特定操作中具有顯著優勢：

- **前綴搜索**: Tries 在尋找所有具有共同前綴的鍵方面表現卓越。
- **字典序排序**: 它們允許按字典序高效地枚舉所有鍵。
- **空間效率**: 對於具有大量共同前綴的鍵，Tries 比雜湊表使用更少的空間，後者可能因雜湊衝突而導致性能下降和空間浪費。
