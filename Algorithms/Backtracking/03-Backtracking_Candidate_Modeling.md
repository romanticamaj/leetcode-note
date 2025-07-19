# 心法：以「已定 vs. 待定」視角進行候選者建模

在回溯演算法中，一個極其有用的心智模型是將問題的選擇空間劃分為兩個集合：「**已定集 (Decided Set)**」和「**待定集 (Undecided Set)**」。

> **核心概念**：回溯的過程，就是不斷地從「待定集」中挑選一個候選者，將其加入「已定集」，直到「已定集」本身構成一個完整的解。

這個視角幫助我們清晰地定義狀態，並理解遞迴的本質。

---

## 🎯 什麼是「已定」與「待定」？

- **已定集 (Decided Set)**：

  - 代表當前正在建構的**部分解 (Partial Solution)**。
  - 是已經被選擇、採用的元素集合。
  - 在程式碼中，通常由 `path` 向量、`board` 狀態、或 `index` 指標隱含地表示。

- **待定集 (Undecided Set)**：
  - 代表在當前狀態下，**所有剩下可供選擇的候選者**。
  - 是下一層遞迴需要探索的選擇池。
  - 它可以是明確的（如 `nums` 陣列中未被 `visited` 的元素），也可以是隱含的（如 N-Queens 中所有不衝突的欄位）。

---

## 🎲 典型問題的「已定/待定」模型

| 問題類型                | 已定集 (Decided)            | 待定集 (Undecided)                | 終止條件                        |
| :---------------------- | :-------------------------- | :-------------------------------- | :------------------------------ |
| **子集 (Subsets)**      | 當前已選擇的元素 `path`     | `nums` 中 `start` 索引之後的元素  | 探索完所有 `start` 之後的選擇   |
| **排列 (Permutations)** | 已排好的前 `index` 個元素   | `nums` 中未被 `visited` 的元素    | `index` 到達 `n`                |
| **組合 (Combinations)** | 已選的 `k` 個元素 `path`    | `nums` 中 `start` 索引之後的元素  | `path` 的長度達到 `k`           |
| **N-Queens**            | 前 `row-1` 行皇后的擺放位置 | 第 `row` 行所有不衝突的欄位       | `row` 到達 `n` (所有行都已放置) |
| **數獨 (Sudoku)**       | 已填寫數字的格子            | 當前空格所有 `1-9` 中不衝突的數字 | 所有空格都被填滿                |

---

## 🟢 N-Queens 範例拆解

- **目標**：在 n x n 棋盤上放置 n 個皇后。
- **在第 `row` 層遞迴中**：
  - **已定集**: 前 `row-1` 行的皇后位置，以及它們所佔據的 `cols`, `diagonals`, `anti-diagonals`。
  - **待定集**: 第 `row` 行所有 `n` 個欄位中，未被「已定集」佔據的那些欄位。
- **流程**：
  1. 在當前 `row`，遍歷所有 `col` (待定集)。
  2. 若 `col` 合法，則將其加入「已定集」(更新 `cols` 等集合)。
  3. 遞迴到下一行 `row + 1`。
  4. 回溯時，將 `col` 從「已定集」中移除。

---

## 🛠️ 如何在新問題中套用此模型？

當你遇到一個新的回溯問題時，問自己以下四個問題：

1. **定義「已定集」**：什麼樣的狀態可以代表一個「部分解」？（e.g., 一個 `path` 向量）
2. **定義「待定集」**：基於當前的「已定集」，如何推導出下一步的所有合法選擇？
3. **定義「終止條件」**：什麼時候，「已定集」從一個部分解變成了一個完整解？
4. **定義「剪枝條件」**：在「待定集」中，有哪些候選者可以被提前證明無法導向有效解？

---

## ✨ 模板化思考流程

```cpp
void backtrack(DecidedSet& partial_solution, UndecidedSet& candidates) {
    // 步驟 3: 檢查終止條件
    if (is_complete_solution(partial_solution)) {
        add_to_results(partial_solution);
        return;
    }

    // 步驟 2: 遍歷待定集
    for (Candidate& candidate : candidates) {
        // 步驟 4 (可選): 剪枝
        if (!is_promising(partial_solution, candidate)) {
            continue;
        }

        // 步驟 1: 將候選者從「待定」移至「已定」
        add_to_decided(partial_solution, candidate);

        // 探索下一步
        backtrack(partial_solution, get_next_candidates(candidate, candidates));

        // 回溯：將候選者從「已定」移回「待定」
        remove_from_decided(partial_solution, candidate);
    }
}
```

這個「已定/待定」的視角，能幫助你更結構化地思考狀態的轉移，並清晰地劃分問題的探索空間，是**將抽象問題轉化為具體程式碼的關鍵橋樑**。
