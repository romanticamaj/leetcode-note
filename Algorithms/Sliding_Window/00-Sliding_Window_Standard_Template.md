# Sliding Window 標準模板

Sliding Window 的唯一標準寫法：**閉區間 `[left, right]`**，節奏是**擴張 → 修復 → 結算**。

進階的 constraint 追蹤與優化見 [01-Constraint_Tracking_and_Optimization.md](01-Constraint_Tracking_and_Optimization.md)。

---

## 1. 🧠 核心心法

> **Sliding Window 最難的不是指針移動，是 constraint check 的資料結構設計與優化**

成功運用 Sliding Window 的關鍵在於：

1. **識別 constraint metric** — 窗口需要滿足什麼條件？
2. **設計狀態追蹤** — 用什麼資料結構追蹤窗口狀態？
3. **優化驗證邏輯** — 如何 O(1) 判斷窗口是否有效？

指針怎麼移動是機械的（就是下面那個模板）；真正的難度在第 2、3 點。

## 2. 要點

1. **window** 表示 subarray
2. 維持兩個 index — **left** and **right**
3. **right** 會增加，讓 window 變大；**left** 會增加，讓 window 變小
4. sliding window 長度是 **`right - left + 1`**
5. 因為 **right** 會不斷增加，所以 window 會 **slide**
6. **constraint metric** 決定要做什麼窗口「特性」判斷，例如 sum、出現的數字個數等
7. 通常問題會給一個 array，去找到滿足 constraint metric 某個特性的 subarray

## 3. 為什麼是閉區間 `[left, right]`

**核心思想**：窗口 `[left, right]` 始終包含 `left` 和 `right` 指針所指向的元素。`for` 迴圈的索引 `right` 代表**當前正在處理並已納入窗口的元素**。

- **邏輯直觀**：「先擴張，再修復」的節奏清晰，易於理解和實現
- **更新時機統一**：總是在循環體末尾，窗口恢復合法後才更新答案，不易出錯
- **模板高度機械化**：`for` 迴圈結構固定，可作為通用「肌肉記憶」
- **邊界處理簡單**：無需在循環外進行額外處理，降低出錯概率

> ⚠️ **不要用半開區間 `[left, right)`**。它雖然與 STL `[begin, end)` 一致而看似親切，但需要 `if/continue` 區分兩條路徑，且 `ans` 的更新會**分散在「遇到衝突時」和「迴圈結束後」兩處** — 極易遺漏後者，漏掉以陣列結尾的最優解。

## 4. 標準模板

```cpp
template<typename T, typename Container>
ResultType solve(const Container& data) {
    // `Window` 可以是 hash map, set, 或其他用於追蹤窗口狀態的數據結構
    Window window_state;
    int left = 0;
    int right = 0; // as the input index, also

    // Target answer
    ResultType ans = 0;

    for (; right < data.size(); ++right) {
        // 1. 擴張窗口：將 data[right] 的狀態更新到 window_state 中
        window_state.add(data[right]);

        // 2. 檢查並修復：當窗口不滿足約束時，從左側收縮，直到恢復合法
        while (is_window_invalid(window_state)) {
            window_state.remove(data[left]);
            left++;
        }

        // 3. 更新結果：此時窗口 [left, right] 必定滿足約束
        ans = max(ans, calculate_result(left, right));
    }
    return ans;
} // 最經典，就背這個
```

### 三步節奏（口訣）

> **擴張 → 修復 → 結算**

| 步驟 | 動作 | 保證 |
| :--- | :--- | :--- |
| 1. 擴張 | `window_state.add(data[right])` | `data[right]` 已納入窗口 |
| 2. 修復 | `while (invalid) { remove(data[left]); left++; }` | 迴圈結束後窗口必定合法 |
| 3. 結算 | `ans = max(ans, f(left, right))` | 在合法窗口上更新答案 |

### ⏱️ 複雜度

`while` 迴圈內嵌於 `for` 迴圈中，形成嵌套結構。但因為 `left` 只會單調前進、總移動次數不超過 `n`，**整體時間複雜度仍為 O(n)**，不是 O(n²)。

## 5. 循環不變量

在每次 `for` 迴圈體結束時，恆有：

- 窗口 `[left, right]` 是**合法的**（滿足題目約束）
- 窗口 `[left, right]` 是**以 `right` 結尾的最長合法窗口**

正因為這個不變量在每輪結束時都成立，答案才能安全地在單一位置統一更新。

## 6. Update 時機的統一框架

```cpp
for (right...) {
    expand window

    while (invalid) {
        // Fix 階段
        // 求最小窗口：在有效時 update（嘗試縮小）
        if (valid before shrinking) update_min_answer();
        shrink left
    }

    // 求最大窗口：Fix 後 update（窗口此時有效且盡量大）
    update_max_answer();
}
```

**判斷規則**：

| 目標 | update 位置 | 理由 |
| :--- | :--- | :--- |
| **求最大窗口** | fix **後** | 窗口有效且已最大化 |
| **求最小窗口** | fix **中** | 找到有效窗口後嘗試縮小 |

## 7. 特定類型：Fixed Window Size

固定長度窗口：在右側添加一個元素，同時在左側移除一個元素以維持窗口長度不變。

**小訣竅**：

- 當添加位置 `i` 的元素時，被移除的元素一定在 `i-k` 位置（`k` 是窗口大小）
- 這樣就可以**省略顯式追蹤 `left`**

## 8. 面試溝通策略

**關鍵原則**：清晰和一致性壓倒一切。先講清楚區間定義，後面所有邊界討論都會變容易，面試官也能立刻對齊你的心智模型。

**推薦話術**：

> "我將採用滑動窗口方法，並定義窗口為一個**閉區間 `[left, right]`**。`right` 指針負責擴張窗口，`left` 指針在窗口違反約束時進行收縮。在每次 `right` 指針移動後，我都會確保窗口恢復合法狀態，然後統一更新最終結果。"

## 9. ✅ 總結

- **只背一個模板**：閉區間 `[left, right]`，節奏是**擴張 → 修復 → 結算**
- **答案只在一個地方更新**：迴圈體末尾，窗口已恢復合法之後
- **不要用半開區間**：結果結算分散的陷阱在壓力下極易出錯
- **難度在 constraint 設計**，不在指針移動

## 相關筆記

- **[01-Constraint_Tracking_and_Optimization.md](01-Constraint_Tracking_and_Optimization.md)** — 雙 Hashmap 設計、Counter Variable 優化（O(n×k) → O(n)）
- **[02-Sorted_Sliding_Window.md](02-Sorted_Sliding_Window.md)** — 窗口內需維持有序時的變體（Ordered Set）
