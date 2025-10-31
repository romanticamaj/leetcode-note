# 遞迴模式對比：Top-Down vs Bottom-Up Recursion

## 🧠 核心哲學

遞迴有兩種資訊流動方向，對應兩種截然不同的設計模式：

- **Top-Down Recursion**: 狀態向下傳遞 → **Backtracking Pattern** (pre-order processing)
- **Bottom-Up Recursion**: 結果向上合併 → **Top-Down DP Pattern** (post-order processing)

## 核心概念：Information Flow Direction

### Pattern 1: Pre-order Recursion (Backtracking)

```cpp
// External state for accumulating results
GlobalState external_state;

void pre_order_recursion(TreeNode* node, PassedState& state) {
    // Pruning: Early termination
    if (!node || !is_valid(node, state)) return;

    // Base Case: Leaf or terminal condition
    if (is_leaf_or_terminal(node)) {
        external_state.update(state);  // Collect result
        return;
    }

    // Pre-order: Process BEFORE recursion
    // Update state based on current node
    state = transform(state, node->val);

    // Recurse: Pass state DOWN to children
    for (auto child : node->children) {
        top_down_recursion(child, state);
    }
}
```

**核心特徵**：

- 狀態透過**函數參數向下傳遞**
- 使用**外部變數累積結果**
- **Pre-order processing**: 先處理當前節點，再遞迴
- Base case 通常在 **leaf node** 處理
- 遍歷方向：Root → Leaf (top-down)

### Pattern 2: Bottom-Up Recursion (Top-Down DP)

```cpp
ReturnType bottom_up_recursion(TreeNode* node) {
    // Base Case: Null node (bottom of recursion)
    if (!node) return base_value;

    // Recurse FIRST - go to bottom
    vector<ReturnType> child_results;
    for (auto child : node->children) {
        child_results.push_back(bottom_up_recursion(child));
    }

    // Post-order: Combine AFTER recursion
    // Build current solution from children's solutions
    return combine(child_results, node->val);
}
```

**核心特徵**：

- 結果透過**返回值向上傳遞**
- **先遞迴到底**，再建構解
- **Post-order processing**: 先遞迴，再處理當前節點
- Base case 在 **null node** 定義
- 遍歷方向：Leaf → Root (bottom-up)

## 設計模式對比

| 特徵      | Top-Down (Backtracking)    | Bottom-Up (Top-Down DP)            |
| --------- | -------------------------- | ---------------------------------- |
| 資訊流向  | 參數向下傳遞               | 返回值向上合併                     |
| 外部狀態  | 需要 (global/class member) | 不需要                             |
| 處理時機  | Pre-order (遞迴前)         | Post-order (遞迴後)                |
| Base Case | Leaf node                  | Null node                          |
| 遍歷方向  | Root → Leaf                | Leaf → Root                        |
| 狀態表示  | `dfs(node, params)`        | `dp(node) = combine(dp(children))` |
| 心智模型  | "帶著資訊往下走"           | "從底部建構答案"                   |

## 適用場景

### 使用 Top-Down Pattern 當：

- ✅ 需要從 root 累積資訊到 leaf (如路徑和)
- ✅ 需要在遍歷過程中維護全局狀態
- ✅ 答案在 leaf 節點收集 (如找所有路徑)
- ✅ Tree 場景幾乎等價於 Backtracking

**Examples**: Path Sum, Binary Tree Paths, DFS ordering

### 使用 Bottom-Up Pattern 當：

- ✅ 子問題的解可以合併成父問題的解
- ✅ 需要從 leaf 聚合資訊到 root
- ✅ 符合 DP 性質：`dp[node] = f(dp[children])`
- ✅ 可定義明確的 recurrence relation

**Examples**: Max Depth, Diameter, Lowest Common Ancestor

## ⏱️ 複雜度分析

兩種模式的時間和空間複雜度通常相同：

| Complexity | Top-Down | Bottom-Up | Note              |
| ---------- | -------- | --------- | ----------------- |
| Time       | O(n)     | O(n)      | 每個節點訪問一次  |
| Space      | O(h)     | O(h)      | 遞迴棧深度 = 樹高 |

**差異**：Bottom-Up 返回值可能更節省空間 (不需 external state)

## ✅ 關鍵要點

- [ ] Top-Down 用於**狀態傳遞** (parameters down) → Pre-order processing
- [ ] Bottom-Up 用於**結果聚合** (return values up) → Post-order processing
- [ ] Top-Down 在 Tree 上幾乎等價於 Backtracking
- [ ] Bottom-Up 本質是 Top-Down DP（從 children 建構父節點的解）
- [ ] Graph 場景下，Top-Down 需額外 `visited` pruning
- [ ] 選擇依據：問「資訊從哪裡來？往哪裡去？」

## 混合模式：Pre-order + Post-order

當需要同時向下傳遞狀態與向上合併結果：

```cpp
ReturnType hybrid_pattern(TreeNode* node, PassedState& from_parent) {
    // Base case
    if (!node) return base_value;

    // Pre-order: Process with parent's state
    CurrentState current = combine_with_parent(from_parent, node);

    // Recurse: Pass down and collect up
    vector<ReturnType> child_results;
    for (auto child : node->children) {
        child_results.push_back(hybrid_pattern(child, current));
    }

    // Post-order: Combine children's results
    return aggregate(current, child_results);
}
```

**應用**: 需要同時「向下傳遞約束/狀態」與「向上合併子問題解」
