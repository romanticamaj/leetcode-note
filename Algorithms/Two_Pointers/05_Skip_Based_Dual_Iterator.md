# Skip-Based Dual Iterator 解題心法

## 🧠 核心概念

**Ignore Noise, Compare Signal**

比對兩序列時，同步跳過「noise」元素，只比對「signal」元素。

```
Example: LR Swap (LC 777)
start  = "RXXLRXRXL"
result = "XRLXXRRLX"

Skip 'X' (noise), compare 'R'/'L' (signal):
start:  R X X L R X R X L
        ↓     ↓ ↓   ↓   ↓
result: X R L X X R R L X
          ↓ ↓     ↓ ↓ ↓

Signal sequence: R L R R L (matches ✓)
Position check: R can only move right, L can only move left
```

## 通用模板

```cpp
bool compare_with_skip(const string& seq1, const string& seq2) {
    int i = 0, j = 0;

    while (i < seq1.size() || j < seq2.size()) {
        // 步驟 1: Skip noise
        while (i < seq1.size() && is_noise(seq1[i])) i++;
        while (j < seq2.size() && is_noise(seq2[j])) j++;

        // 步驟 2: 邊界檢查
        if (i >= seq1.size() || j >= seq2.size()) break;

        // 步驟 3: 比對 signal
        if (seq1[i] != seq2[j]) return false;

        // 步驟 4: 位置驗證 (optional)
        if (!valid_position(i, j)) return false;

        i++; j++;
    }

    return i == seq1.size() && j == seq2.size();
}
```

## 關鍵洞察：Separation of Concerns

三個邏輯**各自獨立**，避免糾纏：

```cpp
// ✅ 清晰
while (i < size || j < size) {
    skip_noise(i, seq1);       // 1. 過濾
    skip_noise(j, seq2);

    if (seq1[i] != seq2[j])    // 2. 內容比對
        return false;

    if (!valid_pos(i, j))      // 3. 位置驗證
        return false;
}

// ❌ 混亂：邏輯糾纏
while (...) {
    if (is_noise(seq1[i]) || seq1[i] != seq2[j] || i > j) ...
}
```

## 變體 Patterns

### Pattern 1: Simple Skip (單一條件)

```cpp
while (i < seq1.size() && is_noise(seq1[i])) i++;  // O(1) 判斷
```

### Pattern 2: Stateful Skip (需要狀態追蹤)

```cpp
auto next_signal = [](const Sequence& seq, int pos) {
    int state = 0;  // Track skip count or balance

    while (pos is_valid) {
        if (!should_skip_with_state(seq[pos], state))
            break;

        state = update_state(state);
        advance(pos);
    }

    return pos;
};
```

### Pattern 3: Backward Skip (從尾部開始)

```cpp
int i = seq1.size() - 1, j = seq2.size() - 1;
while (i >= 0 || j >= 0) {
    while (i >= 0 && is_noise(seq1[i])) i--;  // 注意邊界 >= 0
    while (j >= 0 && is_noise(seq2[j])) j--;
    // ...
}
```

## 問題識別

此模式適用於：

- 序列含有「可忽略元素」需要過濾
- 元素間有「抵消/取消」關係
- 元素可「移動」但需驗證相對位置
- 關鍵字: "ignore X", "skip Y", "backspace", "swap adjacent"

## 實作要點

| 檢查項              | 說明                              |
| ------------------- | --------------------------------- |
| **嵌套 while**      | 外層控制迭代，內層專注 skip       |
| **Skip 後驗證邊界** | `if (i >= size) break;`           |
| **對稱終止**        | `return i == size && j == size;`  |
| **外層用 `\|\|`**   | `while (i < size \|\| j < size)`  |
| **內層用 `&&`**     | `while (i < size && is_noise(i))` |

## 複雜度

- **Time**: O(n + m) - 每個指標最多掃描一次
- **Space**: O(1) - 只需兩個指標
