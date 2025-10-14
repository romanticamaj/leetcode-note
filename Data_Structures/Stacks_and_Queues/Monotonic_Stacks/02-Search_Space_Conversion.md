# 單調棧：搜尋空間轉換 / Monotonic Stack Search Space Conversion

## TL;DR

**問題特徵**: 對每個元素找「下一個更大/更小」的元素 (暴力 O(n²) → 優化 O(n))

**核心思維**: 違規檢測 → 關係記錄 (當新元素破壞 stack 單調性 = 找到答案)

### 關鍵設計決策

#### 步驟 1: 判斷 Stack Invariant

- 找「下一個更大」→ **Monotonic Decreasing** Stack
- 找「下一個更小」→ **Monotonic Increasing** Stack

#### 步驟 2: 選擇輔助結構

- 全查詢 → `vector<int>` (每個元素都需要答案)
- 稀疏查詢 → `unordered_map<int,int>` (只查詢子集)

#### 口訣

「找大用遞減，找小用遞增，棧存索引，違規建圖，O(1) 查詢」

---

## 🧠 核心哲學

單調棧最強大的能力不僅僅是「找到下一個更大/更小元素」，更在於將 **O(n²) 的暴力搜尋空間轉換為 O(n) 的預處理 + O(1) 的查詢**。

當問題需要「對每個元素，找到它的下一個滿足某條件的元素」時，與其用雙重迴圈逐一比對，不如用單調棧**一次遍歷**建立完整的「元素關係圖」，再透過輔助資料結構實現快速查詢。

**核心洞察：當新元素破壞棧的單調性時，我們恰好找到了被彈出元素的「下一個更大/更小元素」！**

---

## 核心概念：違規檢測 → 關係記錄

### 搜尋空間轉換流程

```text
暴力搜尋 (Brute Force):
for i in 0..n:
    for j in i+1..n:  ← O(n²)
        if nums[j] satisfies condition for nums[i]:
            record relationship
            break

單調棧轉換 (Monotonic Stack Conversion):
for i in 0..n:           ← O(n)
    while stack violates monotonicity:
        record relationship  ← 違規即發現關係
        pop stack
    push(i)
```

### 狀態定義

```cpp
// 核心：棧中存儲「尚未找到答案」的元素索引
struct MonotonicStackState {
    stack<int> pending;      // 待處理的元素索引
    AuxiliaryStructure ans;  // 記錄結果 (vector 或 hashmap)
};
```

---

## 通用模板 / General Template

### 模式一：直接結果記錄 (Vector)

```cpp
// 適用：每個元素都需要記錄結果（如距離、值等）
template<typename T>
vector<int> nextGreaterWithVector(const vector<T>& nums) {
    int n = nums.size();
    vector<int> result(n, -1);  // 預設值：未找到
    stack<int> s;               // 存索引！

    for (int i = 0; i < n; ++i) {
        // 違規檢測：當前元素破壞單調性
        while (!s.empty() && nums[s.top()] < nums[i]) {
            int prevIdx = s.top();
            s.pop();

            // 關係記錄：prevIdx 的下一個更大元素是 i
            result[prevIdx] = i;  // 或 nums[i]，視題意而定
        }
        s.push(i);
    }

    return result;
}
```

### 模式二：間接查詢記錄 (HashMap)

```cpp
// 適用：查詢集合是輸入的子集，不需要為所有元素記錄結果
template<typename T>
unordered_map<T, T> nextGreaterWithHashMap(
    const vector<T>& nums,
    const vector<T>& querySet
) {
    unordered_map<T, T> result;
    stack<int> s;  // 存索引

    // 階段一：建立關係圖 (O(n))
    for (int i = 0; i < nums.size(); ++i) {
        while (!s.empty() && nums[s.top()] < nums[i]) {
            int prevIdx = s.top();
            s.pop();

            // 記錄值的對應關係
            result[nums[prevIdx]] = nums[i];
        }
        s.push(i);
    }

    // 階段二：查詢階段 (O(m))
    vector<T> answers;
    for (const T& query : querySet) {
        answers.push_back(result.count(query) ? result[query] : -1);
    }

    return result;
}
```

---

## ⚠️ 常見陷阱 / Common Pitfalls

### 1. 存值還是存索引？

```cpp
// ❌ 錯誤：存值無法追溯原位置
stack<int> s;
for (int num : nums) {
    s.push(num);  // 丟失了索引資訊！
}

// ✅ 正確：存索引，靈活處理
stack<int> s;
for (int i = 0; i < nums.size(); ++i) {
    s.push(i);    // 可通過 nums[i] 取值，也可計算距離
}

// ⚠️ 例外：當 search space 元素具有唯一性時
// 如果題目保證所有元素不重複，存值仍有辨識度
// 但通常仍建議存索引，以保持一致性和擴展性
```

### 2. Stack Invariant 設計決策 ⭐⭐⭐

**這是整個模式最關鍵的設計步驟！**

```cpp
// 設計流程：
// 1. 確認目標：想找「下一個更大」還是「下一個更小」？
// 2. 設計違規條件：當什麼情況發生時，表示找到答案？
// 3. 推導 stack invariant：要維持什麼單調性，才能正確觸發違規？

// 範例：找「下一個更大元素」
// 目標：當遇到 nums[i] > nums[某元素] 時，nums[i] 就是答案
// 違規條件：nums[s.top()] < nums[i]
// Stack invariant：維持單調遞減（從棧底到棧頂遞減）

while (!s.empty() && nums[s.top()] < nums[i]) {  // 違規 = 找到答案
    // 此時 nums[i] 是 nums[s.top()] 的「下一個更大元素」
    result[s.top()] = nums[i];
    s.pop();
}
s.push(i);  // 維持單調遞減 invariant
```

#### 核心思維：從違規條件反推 stack invariant

- 想找「更大」→ 違規條件是 `s.top() < current` → 需要**單調遞減**棧
- 想找「更小」→ 違規條件是 `s.top() > current` → 需要**單調遞增**棧

#### Strict vs Non-strict 單調性

```cpp
// Monotonic Decreasing (嚴格遞減)
while (!s.empty() && nums[s.top()] < nums[i])  // 不允許相等

// Monotonic Non-increasing (非遞增 = 允許相等)
while (!s.empty() && nums[s.top()] <= nums[i])  // 允許相等
```

根據題目需求選擇是否接受相等元素（影響是否記錄重複值）。

### 3. 邊界條件處理

```cpp
// ❌ 錯誤：忘記處理棧內剩餘元素
while (!s.empty() && nums[s.top()] < nums[i]) {
    result[s.top()] = nums[i];
    s.pop();
}
// 遍歷結束後，棧內剩餘元素無答案！

// ✅ 正確：初始化預設值
vector<int> result(n, -1);  // 預設為 -1 (未找到)
// 或在遍歷後顯式處理：
while (!s.empty()) {
    result[s.top()] = -1;  // 明確標記無答案
    s.pop();
}
```

### 4. HashMap 的值覆蓋問題

```cpp
// ⚠️ 注意：當 nums 有重複值時
vector<int> nums = {2, 1, 2, 4, 3};
unordered_map<int, int> nextGreater;

// 第一個 2 → 4
// 第二個 2 → 4
// HashMap 只能存一個映射！需額外處理重複值
```

---

## 適用場景 / Use Cases

此模式適用於以下**直覺問題特徵**：

### 問題特徵識別

- **「下一個更大/更小」**: 需要找序列中每個元素右側第一個滿足大小關係的元素
- **「前一個更大/更小」**: 需要找序列中每個元素左側第一個滿足大小關係的元素
- **「左右邊界查詢」**: 需要同時找到左右兩側第一個滿足條件的元素（雙向延伸）
- **「距離計算」**: 不只要找到目標元素，還要計算距離（索引差）
- **「子集查詢」**: 在大序列中建立關係圖，但只查詢其中部分元素

### 輔助結構選擇直覺

```text
全查詢場景 → Vector
- 每個元素都需要答案
- 結果按順序排列
- 例：計算每個位置到目標的距離

稀疏查詢場景 → HashMap
- 只查詢輸入的子集
- 查詢集合 << 建構集合
- 例：在大序列中查詢特定元素的關係
```

---

## ⏱️ 複雜度分析

| 操作         | 時間複雜度 | 空間複雜度 | 備註                       |
| ------------ | ---------- | ---------- | -------------------------- |
| 建立關係圖   | O(n)       | O(n)       | 每個元素最多入棧/出棧一次  |
| Vector 查詢  | O(1)       | O(n)       | 直接索引訪問               |
| HashMap 查詢 | O(1) avg   | O(k)       | k 為不同元素數量           |
| 整體流程     | O(n + m)   | O(n)       | n = 陣列長度，m = 查詢數量 |

**關鍵：均攤複雜度 O(n)** - 雖然有巢狀迴圈，但每個元素只會被處理常數次。

---

## ✅ 關鍵要點 / Key Checklist

- [ ] **明確目標**: 找「下一個」還是「前一個」？更大還是更小？
- [ ] **選擇單調性**: 找大用遞減棧，找小用遞增棧
- [ ] **決定遍歷方向**: 找「下一個」正向遍歷，找「前一個」逆向遍歷
- [ ] **存索引而非值**: 保留位置資訊以計算距離或處理重複值
- [ ] **選擇輔助結構**: 全查詢用 Vector，稀疏查詢用 HashMap
- [ ] **處理邊界**: 初始化預設值 (通常為 -1 或 0)
- [ ] **驗證違規條件**: 確保 `while` 條件正確觸發關係記錄

---

**最終心法：單調棧 = 暴力搜尋的優雅轉換，違規即答案，空間換時間。**
