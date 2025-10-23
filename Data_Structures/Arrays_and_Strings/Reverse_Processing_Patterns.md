# 逆序處理模式 / Reverse Processing Patterns

## 🧠 核心哲學

當操作會**改變索引或覆蓋資料**時，從右到左處理可避免問題。根據情境不同，有兩種主要應用模式。

## 模式分類

| 模式             | 問題類型        | 避免的問題 | 核心技巧        |
| ---------------- | --------------- | ---------- | --------------- |
| **原地向後填充** | 單陣列擴展/收縮 | 資料覆蓋   | 雙指針          |
| **逆序批次修改** | 多操作批次處理  | 索引失效   | 索引映射 + 排序 |

---

## 模式 1：原地向後填充 (Backward Fill)

### 適用情境

在**同一個陣列**內進行原地修改，涉及：

- 元素複製（擴展）
- 元素刪除（收縮）
- 陣列合併

### 核心問題

```cpp
// ❌ 順序填充會覆蓋未處理資料
// 從左開始處理會覆蓋右側尚未讀取的元素
```

### 三步驟模板

```cpp
// 步驟 1：預計算新長度
int writeIdx = 0;
for (int i = 0; i < n; i++) {
    writeIdx += calculateNewSize(arr[i]);
}

// 步驟 2：處理邊界
if (writeIdx > capacity) {
    // 處理最後元素只能部分處理的情況
    handleBoundary(arr, writeIdx);
    writeIdx--;
}

// 步驟 3：向後填充
int readIdx = n - 1;
writeIdx--;
while (readIdx >= 0) {
    // 根據元素特性決定如何填充
    fillBackward(arr, readIdx, writeIdx);
    readIdx--;
}
```

### 關鍵要點

- [x] **雙指針維護**：`readIdx` 讀取原始資料，`writeIdx` 寫入最終位置
- [x] **writeIdx ≥ readIdx 保證**：寫入位置永遠在讀取位置右側或相同
- [x] **預計算必要**：確定新長度才知道從哪裡開始寫

---

## 模式 2：逆序批次修改 (Reverse-Order Batch Modification)

### 適用情境

對序列執行**多個獨立的修改操作**：

- 字串批次替換
- 批次刪除元素
- 批次插入操作

### 核心問題

```cpp
// ❌ 順序處理導致索引失效
// 先處理低索引的操作會改變後續操作的目標位置
```

### 索引映射模板

```cpp
// 步驟 1：建立索引映射（位置 -> 操作資料）
vector<pair<int, int>> sorted;  // {position, operation_index}
for (int i = 0; i < operations.size(); i++) {
    sorted.push_back({positions[i], i});
}

// 步驟 2：逆序排序
sort(sorted.rbegin(), sorted.rend());

// 步驟 3：從右到左處理
for (auto [pos, opIdx] : sorted) {
    // 應用操作 opIdx 在位置 pos
    // 不影響左側未處理位置
    applyOperation(sequence, pos, operations[opIdx]);
}
```

### HashMap 變體（需要隨機存取時）

```cpp
// 步驟 1：建立位置到操作的映射
unordered_map<int, OperationData> ops;
for (int i = 0; i < operations.size(); i++) {
    if (isValid(operations[i])) {
        ops[positions[i]] = extractData(operations[i]);
    }
}

// 步驟 2：從右到左遍歷並處理
for (int i = sequence.size() - 1; i >= 0; i--) {
    if (ops.count(i)) {
        applyOperation(sequence, i, ops[i]);
    }
}
```

### 關鍵要點

- [x] **索引映射關鍵**：`pair<position, data_index>` 追蹤位置和資料
- [x] **排序開銷小**：O(k log k) 換取正確性
- [x] **操作獨立性**：每個操作有自己的位置和資料

---

## 模式選擇指南

### 使用 Backward Fill 當：

- ✅ 在**同一陣列**內調整元素位置
- ✅ 需要**原地操作**（O(1) 額外空間）
- ✅ 涉及元素複製/刪除/合併
- ✅ 問題：避免覆蓋未處理資料

### 使用 Reverse-Order Batch 當：

- ✅ 處理**多個獨立操作**
- ✅ 每個操作有**明確的位置**
- ✅ 操作會改變序列長度
- ✅ 問題：避免索引失效

## 複雜度對比

| 模式          | 時間                 | 空間 |
| ------------- | -------------------- | ---- |
| Backward Fill | O(n)                 | O(1) |
| Reverse-Order | O(n + k log k + k·m) | O(k) |

_n = 序列長度, k = 操作數, m = 平均操作大小_

## 統一心法

> **從右到左 = 保護左側**
>
> 無論是避免資料覆蓋（Backward Fill）還是索引失效（Reverse-Order），
> 逆序處理都確保已處理部分不影響未處理部分。
