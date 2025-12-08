# 032. Longest Valid Parentheses

## 解題脈絡與練習路徑

### 1. Brute Force

- 檢查所有可能的子字串是否為有效括號序列。
- **Time:** O(n^3), **Space:** O(n) (or O(1) validation)

### 2. Dynamic Programming

- `dp[i]` 代表以 index `i` 結尾的最長有效括號長度。利用 `s[i] == ')'` 時回頭找對應的 `(` 更新長度。
- **Time:** O(n), **Space:** O(n)

### 3. Stack

- Stack 存儲未匹配的括號 index。遇到 `)` 嘗試 pop 匹配，計算當前長度 (`current_index - stack_top`)。
- **Stack Invariant:** Stack 頂端始終保持「最後一個無效括號的位置」(The last position of invalid parentheses)。利用此位置來計算有效長度。
- **Time:** O(n), **Space:** O(n)

### 4. Two Pointers (Left/Right Scan)

- 使用 `left` 和 `right` 計數器。掃描兩次（左到右、右到左）來解決單向掃描無法處理的邊界情況（如 `(()`）。
- **Time:** O(n), **Space:** O(1)
