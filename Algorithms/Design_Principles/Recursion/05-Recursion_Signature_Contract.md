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

## ⚠️ 診斷：需要全域變數 + guard 才能保正確時，先質疑回傳型別

> **遞迴需要全域變數 + guard 才能保正確時，先質疑回傳型別，不要去加固 guard。**

上面的判準（算出來 → 回傳值、撞到的 → 輸出參數）有一個常見的誤用：**拿「線索」怎麼取得來分類，而不是拿「答案」怎麼產生來分類。**

> **鑑別法：線索是撞到的、答案是合併出來的 → 仍然走回傳值。**

**反例：LC 236 Lowest Common Ancestor of a Binary Tree**

- `p`、`q` 是在遍歷中**撞到的**，於是直覺把整題歸進右欄 → 全域 `LCA`（輸出參數）+ guard。
- 但 LCA 不是撞到的：它是**左右子樹的證據在某個節點交匯時算出來的**。`p`、`q` 只是線索。
- 歸錯欄的代價：回傳值只剩 `pair<bool, bool>`（「子樹裡有沒有」），**答不出「是哪個節點」**，答案只能另外放進全域；而全域一旦能被寫第二次，就得補兩個 guard——找到後把回傳值 reset 成 `{false, false}`、入口 `if (LCA) return`——**兩個都在防同一件事：祖先把答案覆蓋掉。**
- 回傳型別換成**子問題的答案型別** `TreeNode*` 之後，全域、reset、早退三者同時消失。推導與程式碼見 [`Recursive_Design_Pattern_Pruning_and_Aggregation.md` §4](../../../Data_Structures/Trees/Recursive_Design_Pattern_Pruning_and_Aggregation.md)。

**症狀清單**——出現任一項，就回頭看回傳型別，而不是繼續補 guard：

| 症狀 | 通常代表 |
| :--- | :--- |
| 找到答案後要 reset 回傳值，免得上層再觸發一次 | 回傳值在回報「狀態」，不是「答案」 |
| 答案存在 member / 全域，入口要 `if (found) return` | 回傳型別裝不下答案，只好外包 |
| 回傳值是一堆 `bool` / flag 的組合 | 丟掉了身分資訊（是**哪個**節點、**多少**），上層只能再查 |

**什麼時候布林是對的**：當「回傳非空」不再保證等於「找到答案」時。LC 1644（LCA II，**不保證** `p`、`q` 都在樹裡）就需要回傳 `pair<TreeNode*, int>` 或另外驗證存在。**條件放寬才引入布林，不是反過來**——236 不需要它。

另見 [`Correct_by_Construction.md`](../Correct_by_Construction.md)：這是「選對承載結構的東西，特例就不存在」在遞迴簽名上的版本。

## ✅ 檢查清單

- [ ] 遞迴中**真正在變**的是什麼？那個才該進參數（`k` 會變 → `int& k`；不變就別傳）
- [ ] 答案是「算出來」還是「撞到的」？決定用回傳值還是輸出參數
- [ ] 入口有沒有 guard？沒有的話 early return 是假的
- [ ] 有沒有東西該進參數卻放成 member？
- [ ] sentinel 值真的不可能是合法答案嗎？
- [ ] 有沒有用全域 + guard 在防「答案被覆蓋」？有的話，回傳型別是不是子問題的**答案型別**？

## 🔗 相關筆記

- [01-Recursion_Design_Principles.md](01-Recursion_Design_Principles.md) — 狀態、邊界、遞迴關係的完整框架
- [04-Top_Down_vs_Bottom_Up_Recursion.md](04-Top_Down_vs_Bottom_Up_Recursion.md) — 參數往下傳 vs 回傳值往上合併
- [State_Design_Across_Recursive_Paradigms.md](State_Design_Across_Recursive_Paradigms.md) — 遞迴設計四大流派
- [Recursive_Design_Pattern_Pruning_and_Aggregation.md](../../../Data_Structures/Trees/Recursive_Design_Pattern_Pruning_and_Aggregation.md) — 回傳值當「證據」的樹遞迴骨架（LCA 案例）
- [Correct_by_Construction.md](../Correct_by_Construction.md) — 正確性掛在結構上，不掛在記憶上
- [06_External_State_Traversal_Order.md](../../Divide_and_Conquer/06_External_State_Traversal_Order.md) — 外部狀態配合遍歷順序
