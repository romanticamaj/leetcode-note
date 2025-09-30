# De Bruijn Graph 與 De Bruijn Sequence

## 🧠 核心概念

De Bruijn Graph 是一種特殊的有向圖，用於表示所有可能的 k 進制長度為 n 的序列之間的重疊關係。它的應用包括密碼破解、DNA 序列組裝、通訊編碼等。

## 圖的構建

### 節點定義

- **節點**：所有長度為 `n-1` 的 k 進制字串
- **節點數量**：`k^(n-1)` 個

### 邊定義

- **邊**：從節點 u 到節點 v，如果 u 的後 `n-2` 位 + 某個數字 = v
- **邊的標籤**：添加的數字（0 到 k-1）
- **邊數量**：每個節點有 k 條出邊，總共 `k^n` 條邊

### 構建算法

```cpp
struct DeBruijnGraph {
    int n, k;  // n: 密碼長度, k: 字符集大小
    unordered_map<string, vector<pair<string, char>>> adj;

    DeBruijnGraph(int n, int k) : n(n), k(k) {
        buildGraph();
    }

    void buildGraph() {
        // 使用 lambda 生成所有長度為 n-1 的節點
        auto generateNodes = [&](auto& self, string& cur, int pos) -> void {
            if (pos == n - 1) {
                // 為每個節點建立 k 條出邊
                for (int i = 0; i < k; i++) {
                    char digit = '0' + i;
                    string next = cur.substr(1) + digit;
                    adj[cur].push_back({next, digit});
                }
                return;
            }

            for (int i = 0; i < k; i++) {
                cur[pos] = '0' + i;
                self(self, cur, pos + 1);
            }
        };

        string start(n - 1, '0');
        if (n == 1) {
            // 特殊情況：單一節點自環
            for (int i = 0; i < k; i++) {
                adj[""].push_back({"", '0' + i});
            }
        } else {
            generateNodes(generateNodes, start, 0);
        }
    }
};
```

## De Bruijn Sequence

### 定義

De Bruijn Sequence B(k,n) 是一個循環序列，其中每個長度為 n 的 k 進制字串都恰好出現一次作為子序列。

### 性質

- **長度**：`k^n` (作為循環序列) 或 `k^n + n - 1` (作為線性序列)
- **存在性**：對所有 n ≥ 1, k ≥ 1 都存在
- **數量**：共有 `(k!)^(k^(n-1)) / k^n` 個不同的 De Bruijn Sequence

### 與 Euler Path 的關係

De Bruijn Graph 有一個關鍵性質：**所有節點的入度 = 出度 = k**，這保證了存在 Euler Circuit。

**核心關係**：

- De Bruijn Graph 的 Euler Path = 訪問所有邊恰好一次
- Euler Path 上的邊標籤串接 = De Bruijn Sequence
- 每條邊代表一個 n 位密碼，Euler Path 確保所有密碼都出現

**算法連結**：
使用 [Hierholzer's Algorithm](../../Algorithms/DFS/Hierholzers/01-Hierholzers_Core_Concepts.md) 找出 Euler Path：
- 採用 [Edge-Based 實現](../../Algorithms/DFS/Hierholzers/02-Node_vs_Edge_Based_Implementation.md#edge-based-implementation)
- 收集邊的標籤（數字）而非節點
- Post-order DFS 確保正確的訪問順序

## 相關題目

### LeetCode 題目

- **753. Cracking the Safe** - 經典 De Bruijn Sequence 應用
- **332. Reconstruct Itinerary** - Euler Path 問題（可對比學習）

### 其他應用場景

- DNA 序列組裝 - 尋找最短超字串包含所有 k-mer
- 通訊編碼 - 生成測試序列
- 密碼學測試 - 窮舉所有可能的 n 位組合

## 複雜度分析

| 操作          | 時間複雜度  | 空間複雜度  | 說明              |
| ------------- | ----------- | ----------- | ----------------- |
| 建圖          | O(k^n)      | O(k^n)      | 需要生成所有邊    |
| 找 Euler Path | O(k^n * n) | O(k^n * n) | DFS + substr 操作 |
| 總體          | O(k^n * n) | O(k^n * n) | 被 substr 主導    |

## ✅ 關鍵要點

- De Bruijn Graph 中，**邊**代表密碼，**節點**代表狀態
- 所有節點入度 = 出度 = k，保證存在 Euler Circuit
- Euler Path 的邊序列即為 De Bruijn Sequence
- 使用 post-order DFS（Hierholzer's Algorithm）構建
- 反轉可省略（De Bruijn Sequence 的對稱性）
