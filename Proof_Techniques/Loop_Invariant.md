# 循環不變量 (Loop Invariant)

迭代演算法的設計工具，也是正確性的系統化證明工具。

---

## 核心概念

### 🧠 演算法設計的關鍵之一：先設計 Loop Invariant

**先想清楚「每輪開始時，哪些事情已經保證成立」，再推導要保存的狀態與允許的操作。** Loop invariant 可以在寫程式前引導設計，也可以在寫完後驗證正確性。

例如想到 `[已完成 | 未處理]`，就已找到區段設計的雛形；下一步是把「已完成」說精確：完成區保存了什麼結果？它和未處理區有什麼關係？只說「sorted」可能不夠，因為有序不代表元素已在最終位置。

| 設計步驟 | 要回答的問題 |
|---|---|
| **1. 定義 invariant** | 每輪開始時，完成區、未處理區或候選空間保證什麼？ |
| **2. 選擇狀態變數（state variables）** | 用哪些指標、邊界或累積值表示這些區段與資訊？ |
| **3. 推導更新規則** | 哪個操作能推進處理，同時維持 invariant？ |
| **4. 推導初始化與停止條件** | 如何讓 invariant 一開始成立？停止時，如何由它推出答案？ |
| **5. 確認進展與終止** | 每輪是否讓未處理量減少，或讓某個有界量朝終點前進？ |

**Invariant 是狀態必須滿足的性質；指標是用來表示與更新狀態的變數。**

以 LC 88. Merge Sorted Array 的從尾端合併為例：

- **區段**：`[未處理 | 已完成的 sorted suffix]`。兩個來源的剩餘部分各自有序，「未處理」比「unsorted」精確。
- **Invariant**：`nums1[k+1:m+n)` 已等於最終合併結果的對應後綴；兩個來源尚未使用的元素保留在 `nums1[0:i+1)` 與 `nums2[0:j+1)`，且 `k = i + j + 1`。
- **狀態變數**：`i`、`j` 是來源的 read pointers；`k` 是結果的 write pointer。
- **更新規則**：取剩餘來源尾端的較大值填到 `k`，再移動該來源指標與 `k`；當 `j >= 0` 時，`k > i`，因此寫入不會覆蓋 nums1 尚未讀取的元素。
- **停止條件**：`j < 0` 時，nums2 已用完，nums1 剩餘前綴已在正確位置；若 nums1 先用完，則繼續填入 nums2 剩餘元素。

口訣：**定性質 → 選狀態 → 推更新 → 驗起點與終點。** 想到可維持、又足以推出答案的 invariant，往往就完成了核心設計；仍需確認初始化、邊界與終止。

### 證明框架

```text
1. Initialization: 證明不變量在循環開始前成立
2. Maintenance: 證明若不變量在本輪開始時成立，則下輪開始時仍成立
3. Termination: 循環終止時，不變量 + 終止條件 ⟹ 演算法正確
```

**Loop Invariant**：在每輪迭代開始時都成立的性質。迴圈內的中間操作可以暫時破壞它，但必須在下一輪開始前恢復。

### 📚 CLRS 如何描述 Loop Invariant

來源：Cormen、Leiserson、Rivest、Stein，[*Introduction to Algorithms*, 第三版](../Reading/Cormen%20Introduction%20to%20Algorithms.pdf)，**§2.1 Insertion sort，書本頁碼 18–20（PDF 第 39–41 頁）**，小節 *Loop invariants and the correctness of insertion sort*。

> “We use loop invariants to help us understand why an algorithm is correct.”

書中用 insertion sort 示範：每輪開始時，`A[1..j−1]` 包含原本這段的所有元素，而且已排序。這同時描述了**元素保留**與**排序性質**，比單說「前綴 sorted」更完整。

- **Initialization**：第一次迭代前，前綴只有一個元素，因此 invariant 成立。
- **Maintenance**：把下一個元素插入適當位置後，前綴擴大一格；下一輪開始時，invariant 仍成立。
- **Termination**：停止時，已排序的前綴涵蓋整個陣列，因此得到正確結果。

CLRS 把前兩步對應到 mathematical induction 的 base case 與 inductive step；第三步則利用停止條件，將局部保證轉成整體答案。這裡的 Termination 是說明「停止時為何正確」；演算法確實會停止，也需要由迴圈的進展另行確認。

**本筆記延伸出的設計觀點**：先找出每輪要維持的 loop invariant，再據此設計狀態變數與更新規則，使演算法逐步走向正確答案。這是從 CLRS 的證明框架延伸出的用法；書中此段直接強調的是理解與證明正確性。

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

*最後更新: 2026-10-03*
