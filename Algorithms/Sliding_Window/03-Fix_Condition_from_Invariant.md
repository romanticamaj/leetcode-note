# 從不變量推 Fix 條件：被逼著走 vs. 能走就走

Sliding window 的節奏是 **擴張 → 修復 → 結算**（expand → fix → update）。入門寫法要記兩條規則：求最長時 update 在 fix **後**，求最短時 update 在 fix **中**。

這份筆記換一個角度：**不記 update 的位置，而是從不變量推出 fix 的條件**。這樣求最長、求最短的 update 都在 fix 後，只寫一次。

---

## 1. 🧠 核心不變量

> **fix 結束時，窗口 `[left, right]` = 以 `right` 結尾的最佳窗口**

- 求最長：以 `right` 結尾的**最長合法**窗口
- 求最短：以 `right` 結尾的**最短合法**窗口（若已出現過合法窗口）

只要每一輪 fix 後這句話成立，就可以在同一個位置更新答案。

## 2. 🧩 Fix 條件：left 是「被逼著走」還是「能走就走」？

| 目標 | `left` 什麼時候走 | fix 條件 | fix 後窗口 |
| :--- | :--- | :--- | :--- |
| **求最長** | **被逼著走**：不走就不合法 | `while (窗口不合法)` | 剛好合法，且最長 |
| **求最短** | **能走就走**：走了還合法 | `while (移掉左端後仍合法)` | 仍合法，且再走一步就不合法 |

忘了細節時，只要問自己：**「`left` 是被逼著走，還是能走就走？」** fix 條件就推得出來。

## 3. 通用骨架

```cpp
for (int left = 0, right = 0; right < n; right++) {
    add(data[right]);                     // 1. expand：data[right] 納入窗口

    while (should_move_left(left)) {      // 2. fix：把 left 推到以 right 結尾的最佳窗口
        remove(data[left]);               //    求最長：窗口不合法
        left++;                           //    求最短：移掉 data[left] 後仍合法
    }

    if (valid()) update(left, right);     // 3. update：永遠在 fix 後
}
```

- 求最長：fix 後必定合法，`if (valid())` 可省
- 求最短：前面可能還沒出現過合法窗口，update 前要先確認合法

## 4. 🧩 求最短時，怎麼設計「移掉左端後仍合法」

關鍵是把問題從「左端元素是什麼」換成：

> **「移掉它，窗口還合法嗎？」**

能用 O(1) 回答，這個寫法才成立。常見的兩種形態：

| constraint 形態 | 「移掉左端後仍合法」寫成 |
| :--- | :--- |
| **累加量達標**（sum、count ≥ 門檻） | 移掉後的累加量仍 ≥ 門檻：`total - value(left) >= threshold` |
| **頻率覆蓋**（窗口要包含某個需求集合） | 左端是**多餘的**：`window_count[x] > need_count[x]` |

頻率覆蓋時，左端元素直覺上有兩種情況：

1. 不在需求集合裡 → 對合法沒貢獻 → 可以丟
2. 在需求集合裡 → 看數量：窗口裡的數量超過需求 → 多的，可以丟

兩種可以合成一句 `window_count[x] > need_count[x]`：不在需求集合裡的元素，需求數量是 0，自動涵蓋。

## 5. 這個寫法帶來的性質

因為 fix 只移掉「移掉後仍合法」的元素，**窗口一旦合法，就一直合法**：

- **fix 管最佳（最短），計數器管合法**，兩件事分開
- 追蹤合法性的計數器（例如「已滿足的條件數」）**只增不減**，不需要寫「失去滿足」的狀態轉換
- 這個計數器實際上變成一個單向開關：「是否已經出現過合法窗口」

## 6. ⚠️ 前提：合法性在「往外擴」時保持

「能走就走」依賴：

> `[left, right]` 合法 ⇒ `[left, right + 1]` 也合法

- ✅ 成立：「包含某個集合」、「全正數的和 ≥ 門檻」、「至少 k 個某元素」
- ❌ 不成立：「剛好 k 個」、「含負數的和 == 門檻」。擴張可能破壞合法性，不能直接套本文「窗口一旦合法，就一直合法」的寫法。需另行論證或轉換問題；例如在「至多」可用窗口計數時，將「剛好 k」拆成「至多 k − 至多 k−1」。

這是本文**求最短覆蓋窗口**的前提，不是所有 sliding window 的共同條件。求最長合法窗口通常利用相反方向的性質：不合法時繼續擴張仍不合法。固定長度窗口則不需要上述合法性單調條件；完整區分見 [標準模板](00-Sliding_Window_Standard_Template.md)。

## 7. 與「update 在 fix 中」的對照

| | update 在 fix 中（入門寫法） | 本文寫法 |
| :--- | :--- | :--- |
| 求最短的 fix 條件 | `while (合法)` | `while (移掉左端後仍合法)` |
| fix 停在 | 剛砍到不合法 | 再砍一個就不合法 |
| update 位置 | 求最長在 fix 後、求最短在 fix 中 | 一律在 fix 後 |
| 合法性計數器 | 會增會減 | 只增不減 |

兩種都對、都是 O(n)。本文寫法的好處是 update 只有一個位置、計數器少一條狀態轉換；代價是要先想通「移掉後仍合法」的條件怎麼寫。

## 8. ⚠️ 常見陷阱

- **把合法性判斷寫進 fix 的 `while` 條件**：例如 `while (formed == required)`，但 fix 只丟多餘的元素，這個值在迴圈裡不會變 → 一路砍到空窗口。fix 條件要針對**左端那一個元素**
- **用 `unordered_map` 查需求數量**：`need[x]` 對不存在的 key 會**插入 0**，讓 `need.size()` 變大，連帶弄壞 `required` → 先存 `required = need.size()`、用 `contains` 短路，或字元集小時直接用陣列
- **update 沒比大小就覆寫答案** → 只在更優時更新
- **用迴圈結束時的 `left`/`right` 取答案** → 更新時記下 `start` + `length`，最後再取一次

## 9. ⏱️ 複雜度

`left`、`right` 都只往前走，各最多 n 步，總共 **O(n)**，前提是「移掉左端後仍合法」能 O(1) 判斷。

## 10. ✅ Checklist

- [ ] 能說出不變量：fix 後窗口 = 以 `right` 結尾的最佳窗口
- [ ] 能判斷 `left` 是「被逼著走」還是「能走就走」
- [ ] 求最短時，能把「移掉左端後仍合法」寫成 O(1) 的條件
- [ ] 確認題目的合法性在往外擴時保持
- [ ] update 前確認合法，並記下起點與長度

## 參考範例

- **76 Minimum Window Substring**：頻率覆蓋，「多餘」= `window_count[x] > need_count[x]`（推導過程見 `Checklists/Practice_Log.md` 2026-09-25）
- **209 Minimum Size Subarray Sum**：累加量達標，`sum - nums[left] >= target`

## 相關筆記

- **[00-Sliding_Window_Standard_Template.md](00-Sliding_Window_Standard_Template.md)** — 標準模板與入門的 update 時機
- **[01-Constraint_Tracking_and_Optimization.md](01-Constraint_Tracking_and_Optimization.md)** — 雙 Hashmap、Counter Variable
