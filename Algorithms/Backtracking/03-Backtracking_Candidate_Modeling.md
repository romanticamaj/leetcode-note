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

## 🛠️ 如何在新問題中套用此模型？

當你遇到一個新的回溯問題時，問自己以下四個問題：

先寫出一個完整答案，確認它的組成部分與每次選擇的單位，再回答：

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

## 🧠 String 題：從單一答案的結構倒推 Candidate

遇到 string 題，先寫出**一個完整答案**，看看它由哪些部分組成，再問：「這一步要完成其中哪個部分？」這能幫助你決定 candidate 是一個 character，還是一整段 substring。

| 問題 | 一個完整答案 | 每一步完成什麼 | Candidate |
| :--- | :--- | :--- | :--- |
| **String Permutation** | 一個排好順序的字串，如 `"aba"` | 決定下一個位置放誰 | 一個尚未使用的 character（以位置區分） |
| **Palindrome Partitioning** | 一組依序排列的回文段落，如 `["aa", "b"]` | 決定下一段是什麼 | 剩餘後綴的一段非空 prefix substring |

> **口訣：拆一個答案 → 決定一次選什麼 → 讓紀錄與還原對應這次選擇。**

### ⚠️ 分清單一答案與答案集合

「輸出有多個字串，所以 candidate 是字串」只能當線索，還要看**單一答案的內部結構**：

- Permutation 的 `vector<string>` 收集多個完整答案；每個答案是一個字串，這種建構方式每次填好一個字元位置。
- Partitioning 的 `vector<vector<string>>` 收集多個完整答案；每個答案本身就是 `vector<string>`，每個元素代表一段，這種建構方式每次選好一整段。

答案結構提供自然的選擇單位，仍要確認這些選擇能涵蓋所有合法答案；回傳型別本身不能證明建模正確。

### 🧩 131 的紀錄方式如何隨之變簡單

`solution` 保存已選好的完整回文段落；`start` 表示下一段的起點。Invariant：**`solution` 串接後恰好等於 `s[0:start)`，且每段都是回文**；未處理區是 `s[start:n)`。

從 `start` 枚舉下一段的結尾，candidate 用區域字串表示。選好合法的一段後，`solution.push_back(candidate)`，遞迴處理其後綴，返回時 `solution.pop_back()`。選擇與還原一一對應，完整解再複製進答案集合。

延長下一段的可能性已由結尾枚舉涵蓋；若又修改 `solution.back()` 來合併字元，就混入另一套決策方式，讓紀錄與還原難以追蹤。

這裡**選擇的單位是 substring，遞迴狀態則可用 start index 表示剩餘後綴**。位置與區間的讀法見 [Index as Cut](../../Data_Structures/Arrays_and_Strings/Index_as_Cut.md)。
