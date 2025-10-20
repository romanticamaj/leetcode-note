# 結構歸納法 (Structural Induction)

遞歸演算法正確性的系統化證明工具。

---

## 核心概念

### 證明框架

```
1. Base Case: 證明 P 對最簡結構成立
2. Inductive Hypothesis (IH): 假設 P 對所有子結構成立
3. Inductive Step: 基於 IH，證明 P 對整體結構成立
4. Termination: 證明遞歸終止
5. 結論: P 對所有結構成立
```

---

## 與數學歸納法的關係

### 本質：同一證明原理的不同應用

| 維度 | 數學歸納法 | 結構歸納法 |
|------|-----------|-----------|
| **對象** | 自然數 ℕ (線性) | 遞歸結構 (樹狀/圖狀) |
| **Base** | P(0) | 空結構/最小單元 |
| **Step** | P(n) → P(n+1) | P(子結構) → P(整體) |
| **遞歸定義** | ℕ ::= 0 \| succ(n) | Tree ::= Empty \| Node(Tree, Tree) |

**統一視角**: 
```
數學歸納法 (線性):  0 → 1 → 2 → 3 → ...
結構歸納法 (分叉):      root
                       /   \
                    left   right
```

**結論**: 數學歸納法 = 結構歸納法在自然數（最簡遞歸結構）上的特例

---

## Template 0: 通用證明框架

```cpp
ReturnType solve(Structure* s, ...params) {
    /* === Structural Induction 證明 === */
    
    // 1. Base Case
    if (isBaseCase(s)) {
        return baseValue;
        // 證明: baseValue 對基本結構的正確性
    }
    
    // 2. Inductive Hypothesis (IH)
    // 假設: solve(sub) 對所有子結構 sub 都正確
    ReturnType r1 = solve(substructure_1);  // IH₁
    ReturnType r2 = solve(substructure_2);  // IH₂
    
    // 3. Inductive Step
    // 證明: aggregate 從子結果正確計算當前結果
    return aggregate(r1, r2, current_data);
    
    /* 證明檢查點:
       □ Base 正確性
       □ 聚合邏輯的數學/邏輯理由
       □ 終止性 (遞歸深度有界)
       □ 完整性 (涵蓋所有情況)
    */
}
```

---

## Template 1: 樹結構

### Post-order Pattern

```cpp
ReturnType treePostOrder(TreeNode* root) {
    // Base
    if (!root) return nullValue;
    
    // IH: 子樹調用正確
    ReturnType L = treePostOrder(root->left);
    ReturnType R = treePostOrder(root->right);
    
    // Step: 證明 combine 正確聚合
    return combine(L, R, root->val);
    
    /* 證明:
       1. Base: nullValue 對空樹的意義
       2. IH: 子樹結果的正確性
       3. Step: combine(L, R, val) 的邏輯
       4. Termination: 樹高有限
    */
}
```

### Pre-order Pattern

```cpp
ReturnType treePreOrder(TreeNode* root, Constraint c) {
    // Base
    if (!root) return nullValue;
    
    // Pre-order 檢查 (可選剪枝)
    if (earlyTerminate(root, c)) return value;
    
    // IH: 子樹在更新約束下正確
    return combine(
        treePreOrder(root->left, update(c, root)),
        treePreOrder(root->right, update(c, root))
    );
    
    /* 證明:
       - earlyTerminate 剪枝的正確性
       - update 約束更新的正確性
    */
}
```

---

## Template 2: 回溯 (搜索樹歸納)

```cpp
void backtrack(State& state, Results& results) {
    // Base 1: 解
    if (isSolution(state)) {
        results.collect(state);
        return;
    }
    
    // Base 2: 剪枝
    if (shouldPrune(state)) return;
    
    // IH: 每個擴展的子搜索樹完整
    for (Candidate c : getCandidates(state)) {
        if (!isPromising(c, state)) continue;
        
        state.add(c);
        backtrack(state, results);  // IH
        state.remove(c);
    }
    
    /* 證明:
       1. isSolution 正確識別解
       2. shouldPrune 只剪無效分支
       3. Step: 遍歷所有候選 → 覆蓋所有可能解
          證明策略: ∀解S, ∃迭代能找到S
       4. Termination: 狀態空間縮小
    */
}
```

---

## Template 3: 動態規劃

### 單向 DP

```cpp
vector<T> dpSolve(Input& input) {
    int n = input.size();
    vector<T> dp(n);
    
    // Base
    dp[0] = initValue;
    
    // IH + Step
    for (int i = 1; i < n; i++) {
        // IH: dp[j] (j < i) 都正確
        dp[i] = transition(dp, i, input);
        
        /* Step 證明 (窮舉最後一步):
           - 列出所有可能的前驅狀態
           - 對每個前驅，根據 IH 假設正確
           - 證明 transition 正確選擇/計算
        */
    }
    return dp;
}
```

### 雙向分解 DP

```cpp
vector<T> bidirectionalDP(Input& input) {
    // IH: 左右 DP 各自正確
    vector<T> left = computeLeft(input);
    vector<T> right = computeRight(input);
    
    // Step: 證明 merge 正確結合雙向信息
    vector<T> result(n);
    for (int i = 0; i < n; i++) {
        result[i] = merge(left[i], right[i]);
    }
    return result;
}
```

---

## Template 4: 鏈表遞歸

```cpp
ListNode* listRecursion(ListNode* head) {
    // Base
    if (!head || !head->next) {
        return handleBase(head);
    }
    
    // IH: 尾部鏈表處理正確
    ListNode* processedRest = listRecursion(head->next);
    
    // Step: 證明如何結合當前節點與處理後尾部
    return combineWithCurrent(head, processedRest);
    
    /* 證明:
       - handleBase 對空/單節點的正確性
       - combineWithCurrent 的合併邏輯
       - Termination: 鏈表長度遞減
    */
}
```

---

## 證明檢查清單

```markdown
### Phase 1: 結構識別
- [ ] 確認遞歸定義的數據結構
- [ ] 識別最小單元（Base Case）
- [ ] 明確「部分-整體」遞歸關係

### Phase 2: Base Case
- [ ] 列舉所有基本情況
- [ ] 證明每個基本情況正確
- [ ] 確認完整性（無遺漏）

### Phase 3: Inductive Hypothesis
- [ ] 明確陳述: "假設對所有子結構，演算法正確"
- [ ] 識別依賴 IH 的遞歸調用
- [ ] 確保 IH 涵蓋所有子結構

### Phase 4: Inductive Step
- [ ] 證明聚合邏輯的數學/邏輯正確性
- [ ] 檢查是否窮舉所有子結構組合
- [ ] 處理特殊情況
- [ ] 確認聚合操作保持性質 P

### Phase 5: Termination
- [ ] 證明遞歸深度有界
- [ ] 確認每次遞歸處理「更小」問題
- [ ] 排除無限遞歸可能
```

---

## 程式碼註釋模板

```cpp
/*
Correctness Proof (Structural Induction):

1. Base Case(s):
   - [結構類型] → [返回值] ✓
   - 理由: [...]

2. Inductive Hypothesis:
   - 假設對所有子結構 S'，solve(S') 正確返回 [性質]

3. Inductive Step:
   - 給定 [子結果] (by IH)
   - [聚合邏輯] 正確因為: [數學推導/窮舉論證]
   - 因此 solve(S) 正確 ✓

4. Termination:
   - [遞歸深度有界的理由] ✓

5. Completeness (可選):
   - [涵蓋所有輸入/情況]
*/
```

---

## 常見誤區

### 誤區 1: "Structural Induction = Post-order"
- **錯誤**: 只有 post-order 需要證明
- **正確**: Post-order 是執行順序，Structural Induction 是證明技術；Pre-order、In-order 也能用

### 誤區 2: IH 範圍不清
- **錯誤**: "假設 n-1 成立"
- **正確**: "假設所有子結構（規模 < n）成立" (Strong Induction)

### 誤區 3: 忽略終止性
- **錯誤**: 只證明 Base + Step
- **正確**: 必須證明遞歸會終止

### 誤區 4: 聚合邏輯不嚴謹
- **錯誤**: 直覺認為「看起來對」
- **正確**: 需明確數學/邏輯推導

---

## 實戰心智檢查

寫完遞歸代碼後的 5 個問題：

1. ✅ Base Case 完整嗎？
2. ✅ 每個遞歸調用都處理「更小」問題嗎？
3. ✅ 聚合邏輯有明確數學理由嗎？
4. ✅ 有無特殊情況讓邏輯失效？
5. ✅ 遞歸一定會終止嗎？

---

## 與 Repo 其他文件的關聯

- **樹遞歸**: [`Recursive_Design_Pattern_Pruning_and_Aggregation.md`](../Data_Structures/Trees/Recursive_Design_Pattern_Pruning_and_Aggregation.md)
- **回溯框架**: [`Backtracking_Problem_Solving_Framework.md`](../Algorithms/Backtracking/02-Backtracking_Problem_Solving_Framework.md)
- **DP 狀態分解**: [`State_Decomposition.md`](../Algorithms/Dynamic_Programming/Advanced_Techniques/State_Decomposition.md)

---

## 總結

### 三要素
1. **Base Case**: 最簡結構的正確性
2. **IH + Step**: 從子結構到整體的邏輯推導
3. **Termination**: 遞歸必然終止

### 核心價值
> **Structural Induction = 遞歸演算法正確性的系統化證明工具**
>
> 養成「寫遞歸 = 寫證明」的思維，能大幅提升代碼正確性！

### 何時使用
- ✅ 設計遞歸演算法
- ✅ 驗證遞歸邏輯
- ✅ Debug 遞歸錯誤
- ✅ 展現嚴謹思維（面試）

---

*最後更新: 2025-10-21*