# 循環不變量 (Loop Invariant)

迭代演算法正確性的系統化證明工具。

---

## 核心概念

### 證明框架

```
1. Initialization: 證明不變量在循環開始前成立
2. Maintenance: 證明若不變量在迭代前成立，則迭代後仍成立
3. Termination: 循環終止時，不變量 + 終止條件 ⟹ 演算法正確
```

**Loop Invariant**: 循環每次迭代前後都保持為真的性質。

---

## 與其他證明技巧的關係

| 維度 | Loop Invariant | Structural Induction |
|------|----------------|---------------------|
| **對象** | 迭代/循環 | 遞歸結構 |
| **結構** | 線性（i → i+1） | 樹狀（子 → 整體） |
| **步驟** | Init + Maint + Term | Base + IH + Step |

**統一視角**: Loop Invariant 是 Mathematical Induction 在循環上的應用

---

## Template 0: 通用框架

```cpp
ReturnType solve(Input input) {
    // 定義不變量 P(i): [迭代 i 開始時的性質]
    
    // 1. Initialization: 證明 P(0)
    initialize();
    
    // 2. Maintenance: P(i) → 操作 → P(i+1)
    for (int i = 0; i < n; i++) {
        process(i);
    }
    
    // 3. Termination: P(n) + (i==n) ⟹ 正確
    return result;
}
```

---

## Template 1: 單指針遍歷

```cpp
ReturnType singlePointer(vector<T>& arr) {
    // P(i) = "arr[0..i-1] 已處理"
    
    for (int i = 0; i < n; i++) {
        process(arr[i]);
    }
    return result;
}
```

---

## Template 2: 雙指針

```cpp
void twoPointers(vector<T>& arr) {
    // P(L,R) = "arr[0..L) 和 arr(R..n-1] 已處理"
    
    int left = 0, right = n - 1;
    while (left < right) {
        if (condition()) {
            process(arr[left++]);
        } else {
            process(arr[right--]);
        }
    }
}
```

---

## Template 3: 搜索空間縮減

```cpp
int search(vector<T>& arr, T target) {
    // P(L,R) = "若 target 存在，必在 [L,R]"
    
    int left = 0, right = n - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (found(mid)) return mid;
        if (shouldGoLeft(mid)) {
            right = mid - 1;
        } else {
            left = mid + 1;
        }
    }
    return -1;
}
```

---

## Template 4: 累積狀態

```cpp
ReturnType accumulative(Input& input) {
    // P(i) = "state 正確反映 input[0..i-1]"
    
    State state = init();
    for (int i = 0; i < n; i++) {
        updateState(state, input[i]);
    }
    return extractResult(state);
}
```

---

## 證明檢查清單

```markdown
- [ ] 明確定義不變量 P
- [ ] P 足夠強？（能推導正確性）
- [ ] P 不太強？（能維護）
- [ ] 證明 Initialization: P(0) 成立
- [ ] 證明 Maintenance: P(i) → P(i+1)
- [ ] 證明 Termination: 循環終止
- [ ] P + 終止條件 ⟹ 正確性
```

---

## 程式碼註釋模板

```cpp
/*
Loop Invariant Proof:

1. Invariant: P(i) = [性質]

2. Initialization: P(0) 成立因為 [...] ✓

3. Maintenance: 
   假設 P(i) → 操作 → P(i+1) 因為 [...] ✓

4. Termination: 
   P(n) + [終止條件] ⟹ [正確性] ✓
*/
```

---

## 常見誤區

### 誤區 1: 不變量選擇不當
- **問題**: 過弱（無法推導）或過強（難維護）
- **解決**: 剛好足夠強推導正確性

### 誤區 2: 忽略 Initialization
- **問題**: 假設「顯然成立」
- **解決**: 明確證明初始狀態

### 誤區 3: Maintenance 邏輯跳躍
- **問題**: 缺少推導過程
- **解決**: 明確說明為何操作維護 P

### 誤區 4: 忽略 Termination
- **問題**: 只證明 Init + Maintenance
- **解決**: 證明循環終止且正確

---

## 不變量設計策略

```cpp
// 策略 1: 已處理 vs 未處理
P(i) = "arr[0..i-1] 已處理"

// 策略 2: 部分解性質
P(i) = "state 正確表示前 i 項"

// 策略 3: 搜索空間
P(L,R) = "答案在 [L,R] 中"

// 策略 4: 相對關係
P(i,j) = "維持指針間關係"
```

---

## 實戰心智檢查

1. ✅ P 定義清晰？
2. ✅ 初始 P 成立？
3. ✅ 迭代維護 P？
4. ✅ 循環終止？
5. ✅ 終止時正確？

---

## 與 Repo 的關聯

- [`Binary_Search_Template.md`](../Algorithms/Binary_Search/01-Binary_Search_Template.md)
- [`Monotonic_Stack.md`](../Data_Structures/Stacks_and_Queues/Monotonic_Stacks/01-Monotonic_Stack_and_Queue.md)
- [`Structural_Induction.md`](Structural_Induction.md)

---

## 總結

### 三要素
1. **Initialization**: 初始正確
2. **Maintenance**: 不變量維護
3. **Termination**: 終止 ⟹ 正確

### 核心價值
> **養成「寫循環 = 定義不變量」的思維**

### 何時使用
- ✅ 設計/驗證迭代演算法
- ✅ Debug 循環邏輯
- ✅ 展現嚴謹思維（面試）

---

*最後更新: 2025-10-21*
