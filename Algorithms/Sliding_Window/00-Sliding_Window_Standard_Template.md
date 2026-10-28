# Sliding Window 標準模板

Sliding Window 的唯一標準寫法：**閉區間 `[left, right]`**，節奏是**擴張 → 修復 → 結算**。

進階的 constraint 追蹤與優化見 [01-Constraint_Tracking_and_Optimization.md](01-Constraint_Tracking_and_Optimization.md)。

---

## 1. 🧠 核心心法

> **先證明邊界可以安全前進，再設計 constraint check。**

1. **驗證適用性與識別 constraint metric** — 為什麼 `left` 不必回頭？窗口需要滿足什麼條件？
2. **設計狀態追蹤** — 用什麼資料結構追蹤窗口狀態？
3. **優化驗證邏輯** — 如何 O(1) 判斷窗口是否有效？

### ⚠️ 套模板前：檢查單調性（monotonicity）

**可變長度窗口必須證明：`right` 前進時，已排除的起點不需要重新考慮，`left` 只往右仍不漏解。** 指標單調前進只能用來分析成本；能安全排除候選才是正確性的依據。

| 目標 | 常見的單調條件 | 例子 |
| :--- | :--- | :--- |
| 最長合法窗口 | 不合法時繼續擴張仍不合法；縮小可修復 | 非負數 `sum <= k`、至多 k 種元素 |
| 最短覆蓋窗口 | 合法時繼續擴張仍合法；縮小可尋找最短邊界 | 非負數 `sum >= k`（正門檻）、包含所有需求字元 |
| 固定長度窗口 | 邊界由長度決定，不需要上述合法性單調條件 | 固定 k 個元素的和，允許負數 |

負數會破壞「和隨擴張不減、隨縮小不增」：`[4, -3]`、門檻 3，`[4]` 的和超標，擴張後卻恢復合法，不能因超標就永久丟掉起點。**有負數不代表所有 sliding window 都失效，要看約束是否仍有可利用的單調性。**

「剛好等於 k」也不能直接套最長合法窗口模板；計數時還要確認是否有多個合法起點，不能每個 `right` 只加一。需另行論證或轉換問題，見 [Fix 條件的適用前提](03-Fix_Condition_from_Invariant.md#6-️-前提合法性在往外擴時保持)。

## 2. 要點

`window` 表示連續 subarray，閉區間 `[left, right]` 的長度為 `right - left + 1`。`right++` 擴張，`left++` 收縮；**constraint metric** 追蹤窗口特性，例如 sum、不同元素個數。

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

> 進階：求最小窗口也可以把 update 放在 fix **後**，改成「移掉左端仍合法就縮」，見 [03-Fix_Condition_from_Invariant.md](03-Fix_Condition_from_Invariant.md)。

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
- **先驗證單調性與安全排除，再設計 constraint**；固定長度窗口另看長度條件

## 相關筆記

- **[01-Constraint_Tracking_and_Optimization.md](01-Constraint_Tracking_and_Optimization.md)** — 雙 Hashmap 設計、Counter Variable 優化（O(n×k) → O(n)）
- **[02-Sorted_Sliding_Window.md](02-Sorted_Sliding_Window.md)** — 窗口內需維持有序時的變體（Ordered Set）
- **[03-Fix_Condition_from_Invariant.md](03-Fix_Condition_from_Invariant.md)** — 進階：從不變量推 fix 條件，求最短也能 update 在 fix 後
