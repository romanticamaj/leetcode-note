# Bitmask 集合運算

Bitmask 可以直接對應集合論的操作，用整數的位元代表集合中的元素。

## 集合運算對照表

| 集合操作 | Bitmask 公式 | 說明 |
|----------|--------------|------|
| 聯集 (Union) | `A \| B` | A 或 B 中的元素 |
| 交集 (Intersection) | `A & B` | A 且 B 中的元素 |
| 差集 (Subtraction) | `A & ~B` | 在 A 但不在 B |
| 補集 (Complement) | `~A` 或 `ALL ^ A` | 不在 A 中的元素 |
| 對稱差 (Symmetric Diff) | `A ^ B` | 只在 A 或只在 B |

其中 `ALL = (1 << n) - 1` 代表全集（n 個元素都選取）。

## 遍歷所有子集合

### 遍歷 0 到 2^n - 1 的所有子集

```cpp
int n = 3;
for (int mask = 0; mask < (1 << n); mask++) {
    // mask 依序為 000, 001, 010, 011, 100, 101, 110, 111
}
```

### 遍歷特定集合的所有子集合

給定一個 bitmask `superset`，遍歷它的所有非空子集：

```cpp
for (int sub = superset; sub > 0; sub = (sub - 1) & superset) {
    // sub 是 superset 的子集
}
```

**原理：** `sub - 1` 會清除最低位的 1 並把更低位設為 1，`& superset` 確保只保留 superset 中存在的位元。

**範例：** `superset = 0b1010`

```text
sub = 1010 → 處理
sub = (1010 - 1) & 1010 = 1001 & 1010 = 1000 → 處理
sub = (1000 - 1) & 1010 = 0111 & 1010 = 0010 → 處理
sub = (0010 - 1) & 1010 = 0001 & 1010 = 0000 → 結束
```

**注意：** 這個迴圈不包含空集 `0`。如果需要包含空集，可以用 do-while：

```cpp
int sub = superset;
do {
    // 處理 sub（包含空集 0）
    sub = (sub - 1) & superset;
} while (sub != superset);  // 0 - 1 會 underflow 回到全 1，& superset 後回到 superset
```
