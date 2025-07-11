# DFS、Backtracking 與 Pruning 的關係深度解析

在演算法中，深度優先搜索 (DFS)、回溯法 (Backtracking) 和剪枝 (Pruning) 這三個概念緊密相關，但其目標和實現細節有著關鍵的區別。理解它們的關係是掌握複雜搜索問題的基礎。

## tl;dr: 核心觀念速覽

- **DFS**：是一種**遍歷策略**，目標是走訪所有節點。
- **Backtracking**：是一種**解題範式**，它使用 DFS 策略來智能地窮舉所有可能的**解**。
- **Pruning**：是 Backtracking 的**優化技巧**，用來提前放棄不可能產生有效解的路徑。
- **State Restoration (狀態還原)**：是 Backtracking 的**必要機制**。沒有它，就無法在探索完一條分支後，退回到之前的狀態去探索另一條分支。

---

## 1. 標準 DFS Traversal (遍歷)

- **目標**：訪問一個圖或樹中的每一個節點，且只訪問一次。
- **核心機制**：通常只需要一個 `visited` 集合來記錄已訪問過的節點，以避免在有環的圖中陷入無限循環。
- **狀態還原**：**通常不需要**。一旦節點被標記為 `visited`，此狀態在整個遍歷中保持不變。

### 基本 Template

```cpp
// 寫法一：在遞迴進入點檢查
void dfs_traversal_v1(Node* node, unordered_set<Node*>& visited) {
    if (!node || visited.count(node)) return; // base case and cycle detection

    visited.insert(node);
    process(node);

    for (Node* neighbor : node->neighbors) {
        dfs_traversal_v1(neighbor, visited);
    }
}

// 寫法二：在遞迴呼叫前檢查 (更常見)
void dfs_traversal_v2(Node* node, unordered_set<Node*>& visited) {
    if (!node) return;

    visited.insert(node);
    process(node);

    for (Node* neighbor : node->neighbors) {
        if (!visited.count(neighbor)) { // cycle detection
            dfs_traversal_v2(neighbor, visited);
        }
    }
}
```

---

## 2. Backtracking (回溯)

- **目標**：在一個龐大的搜索空間中，系統性地找出所有（或部分）滿足特定條件的解。
- **核心機制**：它採用 DFS 的探索策略，但在每一步都伴隨著「選擇」與「撤銷選擇」，即**狀態的修改與還原**。

### 基本 Template

```cpp
void backtrack(State& path, Choices& choices) {
    if (is_a_solution(path)) {
        add_to_results(path);
        return;
    }

    for (auto& choice : get_available_choices(path, choices)) {
        // 1. 做出選擇 (Choose)
        make_choice(path, choice);
        // 2. 繼續探索 (Explore)
        backtrack(path, choices);
        // 3. 撤銷選擇 (Unchoose / State Restoration)
        unmake_choice(path, choice);
    }
}
```

---

## 3. Pruning (剪枝)

- **目標**：在回溯法的基礎上，進一步提升效率。
- **核心機制**：在深入探索（`Explore`）之前，增加一個判斷，用來**提前終止**那些明顯無法產生有效解的搜索路徑。

### 帶有 Pruning 的 Backtracking Template

```cpp
void backtrack_with_pruning(State& path, Choices& choices) {
    if (is_a_solution(path)) {
        add_to_results(path);
        return;
    }

    for (auto& choice : get_available_choices(path, choices)) {
        // Pruning: 在深入探索前，判斷這一步是否值得
        if (!is_promising(path, choice)) {
            continue; // 放棄這個選擇，剪掉這個分支
        }
        make_choice(path, choice);
        backtrack_with_pruning(path, choices);
        unmake_choice(path, choice);
    }
}
```

這個 `is_promising` 的判斷，就是剪枝的精髓所在。

---

## 4. 深度辨析：`visited` 檢查 vs. 問題約束剪枝

在理解了以上概念後，我們可以回頭深入探討一個問題：標準 DFS 中的 `visited` 檢查，算是 Pruning 嗎？

答案是：**從廣義上講，是的，但它們的目的和層次不同。**

- **`visited` 檢查 (結構性剪枝)**：

  - **目的**：保證 **DFS 演算法本身的正確性**，主要是在有環的圖中避免無限循環。
  - **剪掉的對象**：結構上無效或冗餘的路徑（回到已訪問節點）。
  - **層次**：屬於圖遍歷演算法的**基本組成部分**。

- **Backtracking Pruning (語義剪枝)**：
  - **目的**：提升**求解特定問題的效率**。
  - **剪掉的對象**：結構上可能有效，但根據**問題的約束條件**判斷，內容上無效的路徑。
  - **層次**：屬於應用層的**優化策略**。

簡單來說，`visited` 檢查是為了**演算法能跑完**，而回溯法中的 Pruning 是為了**演算法能跑得更快**。

---

## 5. 總結：三者的關係

| 特性         | DFS Traversal  | Backtracking                        | Backtracking with Pruning                       |
| :----------- | :------------- | :---------------------------------- | :---------------------------------------------- |
| **本質**     | 一種遍歷策略   | 一種解題範式                        | 回溯法的優化技巧                                |
| **目標**     | 訪問所有節點   | 找出所有有效解                      | 更快地找出所有有效解                            |
| **狀態還原** | 通常不需要     | **必要**                            | **必要**                                        |
| **核心操作** | 標記 `visited` | `Choose` -> `Explore` -> `Unchoose` | `Prune?` -> `Choose` -> `Explore` -> `Unchoose` |

**最終心法**：你可以將回溯法看作是**一種需要進行狀態還原的 DFS**。而剪枝是在這個基礎上，增加的**一個提前退出的判斷條件**，它讓你的 DFS 更加智能，但它**絕對離不開狀態還原**這個基礎。
