# Iterative DFS 在 Tree 與 Graph 中的結構比較與觀察

---

## 🧠 核心觀察

雖然 DFS 在樹中多以遞迴實作，但在圖論中，**Iterative DFS（使用 stack）** 是常見且實用的替代方式。其結構與 tree 的 DFS 仍高度相似，差異主要在於：

- stack 的使用方式
- visited 的必要性
- 遍歷鄰接節點的方式

---

## 🔍 Iterative DFS 結構對比

| 元素             | Tree 中的 DFS（通常遞迴） | Graph 中的 Iterative DFS（stack）     |
| ---------------- | ------------------------- | ------------------------------------- |
| 起始點           | root                      | 任一未 visited 的節點                 |
| stack 初始內容   | root                      | 任一 component 的起點                 |
| while 條件       | 無（由 call stack 控制）  | `!s.empty()`                          |
| 拿出當前節點     | 由遞迴函式參數傳入        | `s.top(); s.pop();`                   |
| 加入鄰接節點條件 | left/right 存在           | `isConnected[node][i] && !visited[i]` |
| visited 處理     | 不一定需要                | 必須使用 visited 陣列                 |
| 結構             | 嚴格樹狀（無環）          | 可有環，需特別處理 visited            |

---

## 🧪 LeetCode 547 範例程式碼（Graph Iterative DFS）

```cpp
class Solution {
public:
    int findCircleNum(vector<vector<int>>& isConnected) {
        std::vector<bool> visited(isConnected.size(), false);
        int count = 0;

        // Iterate through all nodes to ensure all components are covered
        for (int i = 0; i < isConnected.size(); ++i) {
            if (!visited[i]) {
                iterativeDFS(isConnected, i, visited);
                count++;
            }
        }

        return count;
    }

    void iterativeDFS(const vector<vector<int>>& isConnected, const int node, vector<bool>& visited) {
        std::stack<int> s;

        // Initialize the stack with the starting element
        s.push(node);

        while (!s.empty()) {
            // Retrieve the next element from the stack for processing
            const int current = s.top();
            s.pop();

            // Mark the current element as visited
            visited[current] = true;

            // Explore all related elements
            // If a connection exists and the element hasn't been visited, push it onto the stack
            for (int i = 0; i < isConnected.size(); ++i) {
                if (isConnected[current][i] && !visited[i])
                    s.push(i);
            }
        }
    }
};
```

---

## 🧩 結構對應說明

| DFS 元素     | 程式碼對應行為                               |
| ------------ | -------------------------------------------- |
| 起始點選擇   | `for (int i = 0; i < n; ++i)` loop 中        |
| stack 初始化 | `s.push(node);`                              |
| while 條件   | `while (!s.empty())`                         |
| 拿出當前節點 | `vertex = s.top(); s.pop();`                 |
| 加入鄰接節點 | `if (isConnected[vertex][i] && !visited[i])` |
| visited 處理 | `visited[vertex] = true;`                    |

---

## 🧠 結論

- Iterative DFS 是遞迴 DFS 的顯式 stack 實作版本，結構與邏輯幾乎一致。
- 在圖論中，使用 stack 可避免遞迴過深造成的 stack overflow。
- 與 tree 的 DFS 相比，graph 的 Iterative DFS 需額外處理：
  - visited 陣列
  - 多起點（多 component）
  - 鄰接節點的遍歷方式

這種結構對應的理解，有助於你在面試與實作中靈活選擇 DFS 實作方式。

---

## 🧪 延伸補充：為何建議「加入 stack 時就標記 visited」

若你在「取出 stack 時」才標記 visited，可能會發生以下情況：

- 某節點 A 的鄰居 C 尚未被 visited，因此被加入 stack。
- 另一節點 B 也有鄰居 C，且 B 也在 stack 中。
- 此時 C 尚未被 pop，因此仍未被標記 visited，導致 B 也將 C 加入 stack。

這會導致 C 被重複加入 stack，造成空間浪費與重複處理。

### ✅ 正確做法：加入 stack 時就標記 visited（Mark-on-Push）

這樣可以保證每個節點最多只會被加入 stack 一次。

### 🔁 比較程式碼

**❌ 取出時標記（Mark-on-Pop）**

```cpp
while (!s.empty()) {
    const int cur = s.top();
    s.pop();

    // DFS basic: operate on current node
    // Here: Mark-on-Pop
    visited[cur] = true;

    for (int nei : graph[cur]) {
        if (!visited[nei]) {
            s.push(nei);
        }
    }
}
```

**✅ 加入時標記（Mark-on-Push）**

```cpp
// Mark-on-Push, for graph to optimize
visited[start] = true;
s.push(start);
while (!s.empty()) {
    int cur = s.top(); s.pop();
    for (int nei : graph[cur]) {
        if (!visited[nei]) {
            // Mark-on-Push, for graph to optimize
            visited[nei] = true;
            s.push(nei);
        }
    }
}
```
