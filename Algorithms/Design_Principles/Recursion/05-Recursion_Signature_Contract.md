# 遞迴簽名契約：可變狀態 / 回傳值 / 輸出參數

遞迴寫起來很醜，通常不是邏輯錯，是**簽名沒設計好**。三個欄位各有職責，缺一個，另外兩個就會被迫兼差。

## 🧠 核心問題

> **「找到答案了，怎麼告訴上面的人？」**

答案有兩條路：**往回傳**（return value）或**寫到外面**（輸出參數）。選錯就會多出一堆賦值和判斷式。

## 三個欄位

```cpp
void f(Node* n, State& st, Result& out);
//              ^^^^^^^^^  ^^^^^^^^^^^
//              可變狀態     輸出參數
//   guard:  if (!n || 已經結束) return;
```

| 欄位 | 職責 | 沒有它會怎樣 |
| :--- | :--- | :--- |
| **可變狀態** `State&` | 邊走邊改的東西（計數、路徑、visited） | 得塞 member 變數 → 同物件呼叫兩次就壞 |
| **guard** | 提早停止遞迴 | 找到答案還繼續走完整棵樹 |
| **輸出參數** `Result&` | 放答案 | 得用 return value 把訊號一層層傳上來 |

**三者互相牽動**：一旦要 early return，就需要輸出參數；有了輸出參數，回傳值就空出來當控制訊號 — 或乾脆 `void`。

## 🔑 判準：早停訊號要不要穿過每一層 frame？

| | 用 **回傳值** | 用 **輸出參數** |
| :--- | :--- | :--- |
| 適合 | 答案是**由下往上合併**算出來的 | 答案在**某一個節點**上被撞見 |
| 早停 | 靠 sentinel（`-1` / `nullptr`）逐層往上傳 | `out` 直接寫，guard 直接擋 |
| 典型 | LC 110 Balanced（高度 `-1` 代表不平衡） | LC 230 Kth Smallest（中序撞到第 k 個） |

> **心法**：答案是「算出來的」→ 回傳值；答案是「撞到的」→ 輸出參數 + guard。

## ⚠️ 兩個常見陷阱

**1. 用資料值兼任控制訊號**

`return -1` 當「沒找到」，只在「-1 不可能是合法答案」時安全。題目值域一變就爆 — LC 230 第一版用 `NOT_FOUND = -1` 剛好安全（保證 `val >= 0`），但這是運氣不是設計。

**2. 可變狀態放成 member**

```cpp
class Solution {
    int count = 0;              // ❌ 同物件呼叫兩次，count 沒歸零
    vector<vector<int>> ans;    // ❌ 同上，結果會累加
};
```

改成 by-reference 參數，狀態的生命週期就跟著一次呼叫走。

> 註：舊說法「External State 無法 early termination」並不正確 — 只要在函式入口加 guard（`if (st.done()) return;`），外部狀態一樣能真正提早停。

## ✅ 檢查清單

- [ ] 遞迴中**真正在變**的是什麼？那個才該進參數（`k` 會變 → `int& k`；不變就別傳）
- [ ] 答案是「算出來」還是「撞到的」？決定用回傳值還是輸出參數
- [ ] 入口有沒有 guard？沒有的話 early return 是假的
- [ ] 有沒有東西該進參數卻放成 member？
- [ ] sentinel 值真的不可能是合法答案嗎？

## 🔗 相關筆記

- [01-Recursion_Design_Principles.md](01-Recursion_Design_Principles.md) — 狀態、邊界、遞迴關係的完整框架
- [04-Top_Down_vs_Bottom_Up_Recursion.md](04-Top_Down_vs_Bottom_Up_Recursion.md) — 參數往下傳 vs 回傳值往上合併
- [State_Design_Across_Recursive_Paradigms.md](State_Design_Across_Recursive_Paradigms.md) — 遞迴設計四大流派
- [06_External_State_Traversal_Order.md](../../Divide_and_Conquer/06_External_State_Traversal_Order.md) — 外部狀態配合遍歷順序
