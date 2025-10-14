# 單調棧：內部搜尋空間 / Stack Internal Search Pattern

## 🧠 核心哲學

當單調棧的 invariant 被違反時，**棧內殘留元素形成可查詢的搜尋空間**。除了使用 `popped` 和 `current` 的兩索引互動，你還能訪問**棧的深層元素** (`s.top()` after pop) 實現**三索引協作**，從而解決需要「邊界-中間-邊界」結構的問題。

**核心洞察**: Stack 不僅儲存「待處理元素」，更是一個**分層可查詢的索引庫**。

---

## 核心概念：分層索引互動

### 演進階段

```text
Level 1 (基礎): 雙索引互動
    popped ←→ current
    用途: 下一個更大/更小元素查詢

Level 2 (進階): 三索引協作  ← 本文重點
    s.top() ←→ popped ←→ current
    用途: 區域累積、邊界計算
```

### 狀態定義

```cpp
// 關鍵：Pop 後棧頂成為「第二邊界」
struct LayeredState {
    int current;       // 右邊界 (觸發違規的元素)
    int popped;        // 中間元素 (被彈出的元素)
    int leftBoundary;  // 左邊界 (pop 後的 s.top())
};
```

---

## 通用模板 / General Template

```cpp
template<typename T>
Result computeWithBoundaries(const vector<T>& arr) {
    stack<int> s;
    Result result = initResult();

    for (int i = 0; i < arr.size(); ++i) {
        while (!s.empty() && violatesInvariant(arr[s.top()], arr[i])) {
            int mid = s.top(); s.pop();  // 第一層：中間元素

            // 🔑 關鍵：查詢第二層
            if (!s.empty()) {
                int left = s.top();  // 第二層：左邊界（不 pop）

                // 三索引協作計算
                result += compute(left, mid, i, arr);
            }
        }
        s.push(i);
    }
    return result;
}
```

---

## ⚠️ 常見陷阱 / Common Pitfalls

### 1. 忘記雙重空檢查 ⭐

```cpp
// ❌ 錯誤：pop 後直接用 s.top()
int mid = s.top(); s.pop();
int left = s.top();  // 崩潰！Stack 可能已空

// ✅ 正確：pop 後再次檢查
int mid = s.top(); s.pop();
if (!s.empty()) {
    int left = s.top();  // 安全訪問第二層
}
```

**核心**：`while` 的空檢查保證「能 pop」，但不保證「pop 後還有元素」。

### 2. 寬度計算錯誤

```cpp
// ❌ 錯誤：包含邊界本身
int w = right - left;

// ✅ 正確：排除兩端邊界
int w = right - left - 1;

// 範例：left=1, right=4
// 中間元素索引: [2, 3] → 寬度 = 2
```

---

## 何時使用此模式？

**識別信號**：

- 需要**三個位置**協作計算（left-mid-right）
- 需要知道「被 pop 元素」與「Stack 內剩餘元素」的關係
- 計算公式包含 `f(left, mid, right)` 形式

**與 Level 1 的區別**：

| 特徵       | Search Space (L1) | Internal Search (L2) |
| ---------- | ----------------- | -------------------- |
| 索引數     | 2 個              | **3 個**             |
| Pop 後操作 | 記錄關係          | **查詢 Stack 深層**  |

---

## ✅ 檢查清單

- [ ] 問題需要三索引協作？
- [ ] Pop 後加上 `if (!s.empty())` 檢查？
- [ ] 寬度計算用 `right - left - 1`？

---

**心法**: 單調棧是分層可查的索引庫。違規時查詢深層 = 解鎖多索引協作。
