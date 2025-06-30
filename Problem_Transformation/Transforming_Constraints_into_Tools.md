# 問題轉換心法：將「限制」轉化為「工具」

核心想法：**將問題的「限制」轉化為「工具」**

在演算法問題中，一個強大的高階技巧是**重塑狀態 (Reframing State)**
與其在遞迴或迭代中逐步累積狀態（例如，`currentSum`），不如反向思考，從目標狀態（`targetSum`）開始修改，讓狀態本身成為驗證條件的一部分，從而寫出更精煉、更高效的程式碼。

這個視角的轉換，其核心動機是為了**優化**：

- **空間優化**：減少需要傳遞的參數，或避免使用額外的資料結構。
- **邏輯簡化**：使狀態轉移和終止條件（Base Case）更為簡潔。

---

## 核心原則：加法 vs. 減法視角

這兩種視角是對立的，但能達成相同的目標。

- **加法視角 (標準作法)**：
  - **狀態**：維護一個 `currentState` 變數（如 `currentSum`）。
  - **過程**：在每一步中，將當前元素的值加入 `currentState`。
  - **終止條件**：檢查 `currentState` 是否等於 `targetState`。
  - **缺點**：通常需要同時追蹤 `currentState` 和 `targetState`，參數較多。

- **減法視角 (重塑後的作法)**：
  - **狀態**：直接使用 `targetState` 作為倒數計時器。
  - **過程**：在每一步中，從 `targetState` 中減去當前元素的值。
  - **終止條件**：檢查 `targetState` 是否等於 `0`。
  - **優點**：參數更少，終止條件更乾淨，且巧妙地利用了題目給定的輸入作為狀態本身。

---

## 案例研究：路徑總和 (Path Sum, LeetCode 112)

**問題**：給定一個二元樹的根節點 `root` 和一個目標整數 `targetSum`，判斷樹中是否存在一條從根到葉的路徑，使得路徑上所有節點值的總和等於 `targetSum`。

### 作法一：加法視角 (追蹤 `currentSum`)

這是最直觀的作法，我們在遞迴中傳遞目前為止累積的總和。

```cpp
class Solution {
public:
    bool hasPathSum(TreeNode* root, int targetSum) {
        return dfs(root, targetSum, 0);
    }

    bool dfs(TreeNode *root, const int targetSum, int sum) {
        if (root == nullptr) return false; // boundary condition

        // current node processing
        sum += root->val;
        if (!root->right && !root->left) return targetSum == sum; // leaf node

        // recursion
        return dfs(root->right, targetSum, sum) || dfs(root->left, targetSum, sum);
    }
};
```

- **評析**：此法可行，但 `dfs` 函式需要攜帶兩個與總和相關的參數 (`currentSum`, `targetSum`)。

### 作法二：減法視角 (追蹤 `remainingSum`)

我們重塑問題：與其問「路徑總和是否等於 `targetSum`？」，不如問「我能否用完 `targetSum` 的額度，不多不少地走到一個葉節點？」。

```cpp
class Solution {
public:
    bool hasPathSum(TreeNode* root, int targetSum) {
        if (root == nullptr) return false;

        // 將 targetSum 當作倒數計時器，每經過一個節點就扣掉該值
        // 這裡的技巧是：不額外創建 currentSum，而是直接修改目標值
        targetSum -= root->val;

        // 如果是葉節點，檢查是否剛好用完額度
        if (!root->left && !root->right) return targetSum == 0;

        // 將修改後的 targetSum 傳遞下去，讓它成為狀態本身
        return hasPathSum(root->left, targetSum) || hasPathSum(root->right, targetSum);
    }
};
```

- **優化成果**：
  - **空間**：`hasPathSum` 函式的參數從 2 個減少到 1 個，減少了遞迴堆疊的空間開銷。
  - **邏輯**：終止條件的判斷從 `currentSum == targetSum` 簡化為 `targetSum == 0`，更為簡潔。

---

## 總結與適用時機

- **高階心法**：當解法需要追蹤一個不斷變化的狀態以達成某個目標值時，問自己：「我能否不創建新變數，而是直接利用目標值本身來倒數？」
- **優化動機**：
  - **簡化狀態**：減少函式參數或迴圈中的變數。
  - **統一終點**：將複雜的目標比對，轉化為簡單的「是否為零」的判斷。
- **適用場景**：
  - 樹或圖中的路徑總和問題。
  - 子集合總和、組合總和等回溯問題。
  - 任何需要透過累積達成特定目標值的問題。
