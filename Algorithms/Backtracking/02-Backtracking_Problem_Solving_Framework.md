# 心法：系統性建構回溯演算法的通用框架

所有看似複雜的回溯問題，無論是排列組合、N 皇后、還是數獨，都可以透過一個系統性的框架來拆解。這個框架將問題的建構過程分為三個核心支柱：**狀態設計**、**遞迴機制**和**解的組合**。掌握此框架，你就能在面對任何回溯問題時，有條不紊地進行分析與編碼。

---

## tl;dr: 回溯法精華

- **State Design**
  - **Decision Boundary**: 如何追蹤進度？ (例如: `index`, `row`)
  - **Constraint**: 我已使用哪些資源？ (例如: `visited`, `current_sum`)
- **Backtracking**
  - **Promising Check**: 這一步合法嗎？
  - **Choose, Explore, Unchoose**: 核心遞迴模式。
- **Solution Building**
  - **Base Case/Solution Reach**: 何時算是找到一個解？
  - **Combine or Collect**: 找到解後該做什麼？ (例如: 計數或加入列表)

## 1️⃣ 第一步：狀態設計 (State Design)

✅ **一個好的狀態設計，是解題成功的一半。**

這是最關鍵的一步，它定義了遞迴函式的「簽名」(signature)，並決定了我們如何在決策樹中追蹤進度。

**核心問題**：

- 我需要哪些資訊，才能唯一描述在決策樹中任何一個節點（即一個「部分解」）的狀態？

**常見的狀態組件**：

1. **進度指標 (Progress Indicator) / 已定與待定邊界**：
   - **`int index` 或 `int row`**: 這個指標的核心作用是作為 **「已定集 (Decided)」與「待定集 (Undecided)」之間的分界**。它告訴我們決策進行到了哪一步。
   - 例如，在排列問題中，`index` 前方的元素是「已定」的，`index` 及之後的則是「待定」的候選者。
   - 例如，在組合問題中，`index` 索引標記了「待定」候選池的 `起點`。
2. **可用資源與約束 (Resources & Constraints)**：
   - 這是一個廣義的類別，包含所有用於 **判斷一個選擇是否 `is_promising`** 的狀態。
   - **資源使用**: 如 `vector<bool>& visited` 或 `unordered_set<int>& used`，記錄哪些元素已被選擇。
   - **問題特定約束**: 如 N-Queens 中的 `cols`, `diagonals` 集合。
   - **剪枝輔助狀態**: 如組合總和問題中的 `int current_sum`，它本身不是解的一部分，但對 `current_sum > target` 這類剪枝判斷至關重要。
3. **部分解容器 (Partial Solution Container)**：
   - 用來儲存當前已經做出的選擇序列，例如，`vector<T>& path`

**狀態管理風格：函式參數 vs. 類別成員變數**：

這些狀態組件在程式碼中有兩種常見的管理風格：

- **作為函式參數**
  - 將狀態直接傳遞給遞迴函式（例如 `solve(row, visited, ...)`）。
  - 這種風格在獨立函式中很常見，也不容易造成資源共享導致錯誤。
- **作為類別成員變數**
  - 在物件導向的實作中（如 LeetCode 的 `Solution` class），可將 `results`, `path`, `visited` 等定義為類別的成員變數。
  - 遞迴函式作為一個私有輔助方法，直接存取這些成員，使得函式簽名變得非常簡潔（例如，`solve(row)`）。

---

## 2️⃣ 第二步：遞迴機制 (Recursion Mechanism)

✅ **這個「Promising, Choose, Explore, Unchoose」的四步模式是所有回溯問題的心臟。**

此階段的核心是 **定義選擇集 (Candidate Pool) 與選擇方式**，並透過 **剪枝 (Pruning)** 來過濾掉無效的選擇。

**核心問題**：

- 在當前狀態下，我的「選擇池」(candidate pool) 是什麼？
- 如何判斷一個候選者是「有希望的」，以避免無效的探索？

**思考：我需要剪枝嗎？(To Prune or Not to Prune?)**
在設計遞迴機制時，一個關鍵問題是判斷是否需要 `is_promising` 檢查。

- **無剪枝 (純粹窮舉)**：

  - **情境**：有些問題的結構保證了 **所有探索路徑** 都是有意義的，例如「子集 (Subsets)」。在該問題中，任何部分路徑都是一個合法的子集，因此不需要額外的合法性判斷。
  - **策略**：`for` 迴圈的邊界條件（如 `start` 索引）本身就構成了唯一的約束。

- **結構性剪枝 (Structural Pruning)**：

  - **情境**：為了演算法的 **正確性** 而必須進行的剪枝。例如，在「N 皇后」問題中，檢查當前 `(row, col)` 是否會與已放置的皇后在同一列或同一對角線，是確保任何部分解都滿足「皇后互不攻擊」這個核心定義的必要步驟。這不是為了優化，而是問題本身的規則。
  - **策略**：檢查當前的候選選擇 (`col`) 是否已存在於記錄「已用資源」的狀態集合中（`cols`, `diagonals`, `anti_diagonals`）。

- **約束性剪枝 (Constraint-based Pruning)**：
  - **情境**：為了**效率**而進行的剪枝，通常來自於題目給定的特定約束（例如，「總和不得超過 target」、「路徑長度必須小於 X」等）。
  - **策略**：這是 `is_promising` 函式最常見的用武之地。若缺少此類剪枝，演算法雖然可能仍然正確，但會因探索大量無效的「死亡分支」而導致「超時 (Time Limit Exceeded)」。

**通用模板：核心四部曲**
與其將剪枝看作一個可選步驟，不如將其整合為核心流程的一部分，形成更穩健的「四部曲」。

```cpp
// 偽代碼
void backtrack(State& state) {
    // (可選) 剪枝點 1: 在遞迴入口處剪枝
    if (is_unpromising_state(state)) {
        return;
    }
    // 檢查是否為解
    if (is_a_solution(state)) {
        process_solution(state);
        return;
    }

    // 遍歷當前狀態下的所有可能選擇
    for (Candidate& candidate : get_candidates(state)) {

        // --- 核心四部曲 ---
        // 1. Promising? (檢查)
        if (!is_promising_choice(state, candidate)) {
            continue;
        }
        // 2. Choose (選擇)
        state.add(candidate);

        // 3. Explore (探索)
        backtrack(new_state);

        // 4. Unchoose (撤銷選擇)
        state.remove(candidate);
    }
}
```

---

## 3️⃣ 第三步：解的組合 (Solution Construction)

這部分定義了遞迴的「出口」，以及如何處理找到的解。

**核心問題**：

- 我應該在何時停止遞迴？（即，終止條件是什麼？）
- 當滿足終止條件時，我應該如何處理找到的解？

**常見的終止與組合方式**：

1. **終止條件 (Base Case)**：
   - **找到解的終止條件**
     - 通常與進度指標相關，這意味著一個完整的決策序列已經完成。
     - 例如：`if (row == n)` 或 `if (path.size() == k)`。
   - **剪枝的終止條件**
     - 當前路徑已被證明不可能導向有效解時，也應終止。
     - 例如：`if (current_sum > target)`。
     - 最佳化：此類檢查作為遞迴入口的「防禦性」剪枝是可行的，但更清晰的結構是 **在 `for` 迴圈內、進行遞迴呼叫前** 就透過 `is_promising` 判斷，以避免不必要的函式呼叫開銷。
2. **解的處理**：
   - **計數問題**: 如果只要求解的數量，返回 `1`。
     - `if (row == n) return 1;`
   - **列舉問題**: 如果要求所有解的集合，將當前「部分解」的 **一份拷貝** 加入結果集。
     - `if (path.size() == k) { results.push_back(path); return; }`
3. **解的搜集形式**：
   - **Collect**: 例如，**計數問題**，上層函式需要累加下層返回的計數。
     - `int count = 0; ... count += backtrack(...); return count;`
   - **Collect**: 例如，**列舉問題**，通常使用傳參考的 `results` 容器來收集所有解，函式本身為 `void`。

---

## 🌟 一頁式 Backtracking 模板脈絡

| 支柱            | 核心問題                             | 關鍵字                                                                    |
| :-------------- | :----------------------------------- | :------------------------------------------------------------------------ |
| **1. 狀態設計** | 我需要哪些參數來描述一個「部分解」？ | `index` (邊界), `path`, `visited`, `constraints`                          |
| **2. 遞迴機制** | 如何探索所有下一步的可能？           | **Promising, Choose, Explore, Unchoose**                                  |
| **3. 解的組合** | 何時停止？如何收集結果？             | **解的 Base Case**, **剪枝的 Base Case**, `return 1`, `results.push_back` |

### 🧠 面試時如何講解

> 「針對這個問題，我會使用回溯法來系統性地探索所有可能的解。
> **首先，我會設計遞迴的狀態**，這包括進度指標如 `index`，部分解容器如 `path`，以及用於 **剪枝** 的約束條件，例如 `visited` 集合。
> **其次，在遞迴函式中**，我會遍歷所有可能的候選選擇，並對每個選擇執行經典的 **四步流程**：首先 **判斷選擇是否『有希望』(Promising)**，如果通過，才進行『選擇 (Choose)』、向下『探索 (Explore)』，最後『撤銷選擇 (Unchoose)』。
> **最後，我會定義遞迴的終止條件**，這包括找到完整解的條件，以及因違反約束而需要 **提前終止（剪枝）** 的條件。」
