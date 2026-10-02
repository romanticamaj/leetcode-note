# 🧩 Algorithm Design Pattern – 思考三連問

> 🎯 **核心目標**
> 以最小的語言單位，捕捉所有演算法設計的骨架。
> 「狀態（State）→ 轉移（Transition）→ 遍歷（Traversal）」
> 是從暴力到最優化的共同底層結構。

> **🧭 使用順序：先用 State／Transition／Traversal 描述一個正確的 brute force，再分析成本，用 BUD 找可省的工作、用 BCR 判斷優化空間。** 三連問先幫你建出可驗證的基準；優化要能說明相對這個基準省了什麼。詳見 [解題指北星](../../Interview_Playbook/Problem_Solving_Strategies.md)。

---

## 🧠 一、三連問核心概念

| 問題                        | 說明                 | 範例（Longest Palindromic Substring）         |
| ------------------------- | ------------------ | ----------------------------------------- |
| **1️⃣ 狀態是什麼？（State）**     | 要記錄哪些資訊，才能唯一描述子問題？ | `dp[i][j]` 表示 s[i..j] 是否為回文               |
| **2️⃣ 怎麼轉移？（Transition）** | 狀態如何由子問題推出？        | `dp[i][j] = (s[i]==s[j]) && dp[i+1][j-1]` |
| **3️⃣ 遍歷順序？（Traversal）**  | 子問題的依賴順序是什麼？       | 由短區間 → 長區間（對角線填表）                         |

> 💬 用一句話說：
> 「我在什麼狀態？ → 我要怎麼變？ → 我要先算誰？」

---

## 🔍 二、為什麼它是通用框架

這三問不只是 DP 模板，而是所有演算法範式的共通抽象層。
任何解法都可還原為「狀態、轉移、遍歷」。

| 範式                     | State（狀態）        | Transition（轉移）      | Traversal（遍歷）        |
| ---------------------- | ---------------- | ------------------- | -------------------- |
| **DP**                 | dp[i][j] / dp[k] | 遞推方程                | bottom-up / top-down |
| **DFS / Backtracking** | path, index      | 選擇 → 遞迴 → 回溯        | pre/post-order       |
| **BFS / Graph**        | (node, dist)     | 擴展鄰居                | queue (層序)           |
| **Greedy**             | 當前決策點            | 選最優 → 前進            | sort + scan          |
| **Two Pointers**       | (l, r)           | 擴張 / 收縮             | while (l < r)        |
| **Binary Search**      | 區間 [low, high]   | mid = (l+r)/2 → 判斷  | 迴圈收斂                 |
| **Divide & Conquer**   | 區間或節點            | combine(sub1, sub2) | 遞迴結構                 |
| **Sliding Window**     | (l, r) 範圍        | 加入右邊 / 移除左邊         | 線性遍歷                 |
| **Union-Find**         | parent[], rank[] | find / union 操作     | lazy update          |
| **Graph DP / Tree DP** | 子樹節點集合           | 結合子結果               | 後序遍歷                 |

---

## 🧩 三、思維升級：從三連問 → 五連問

> 當題目變複雜時，可擴充為「五連問」進行更深層分析。

| 問題           | 目標                            | 提示                      |
| ------------ | ----------------------------- | ----------------------- |
| 1️⃣ 狀態是什麼？   | 找出最小子問題單位                     | index, 範圍, 子集, mask     |
| 2️⃣ 怎麼轉移？    | 子問題間的關聯式                      | 遞推、決策、合併                |
| 3️⃣ 遍歷順序？    | 子問題計算順序                       | 左→右、上→下、層序              |
| 4️⃣ 有無重疊子問題？ | 若有 → DP；若無 → Divide & Conquer |                         |
| 5️⃣ 可否壓縮狀態？  | 空間/時間優化                       | 滾動陣列、hash cache、bitmask |

---

## ⚙️ 四、實際應用步驟（30 秒設計模板）

> 解題前先問自己以下問題，寫在草稿紙上：

```
state = ?
transition = ?
traversal = ?
```

然後：
1️⃣ 用 pseudo-code 驗證 transition 是否自洽。
2️⃣ 標出依賴方向箭頭（確保 traversal 正確）。
3️⃣ 若發現子問題重疊 → 可改 DP。
4️⃣ 若 state 太複雜 → 嘗試壓縮。
5️⃣ 完成後再推導 time / space complexity。

---

## 🧩 五、應用案例對照表

| 類型                                 | State         | Transition                        | Traversal |
| ---------------------------------- | ------------- | --------------------------------- | --------- |
| **Fibonacci**                      | n             | f(n) = f(n-1)+f(n-2)              | bottom-up |
| **Longest Increasing Subsequence** | i             | dp[i] = max(dp[j]+1) if a[j]<a[i] | i 由左至右    |
| **Word Ladder (BFS)**              | (word, depth) | 擴展相差一字的鄰居                         | queue     |
| **Subset Sum (DP)**                | dp[i][sum]    | 選 or 不選                           | i 增加      |
| **N-Queens (Backtracking)**        | row / col     | 放 / 拿掉 → 遞迴                       | row 順序    |
| **Binary Search (Decision)**       | [l,r]         | mid → 判斷 → 收縮                     | while     |
| **Minimum Window Substring**       | (l,r)         | 擴張右指針 + 收縮左                       | 連續線掃描     |

---

## 🚧 六、常見錯誤與修正

| 錯誤類型            | 現象             | 修正思考                   |
| --------------- | -------------- | ---------------------- |
| 狀態定義錯誤          | 子問題不唯一、重疊過多    | 「我需要哪些資訊才能唯一決定子問題？」    |
| 轉移方向錯           | 依賴未算完的子問題      | 確認 traversal 是否符合依賴關係  |
| transition 過度複雜 | 維度爆炸、超時        | 壓縮維度或抽象成決策型 DP         |
| 忘記邊界條件          | dp[-1], i>j 失效 | 明確列出 base cases        |
| 思考卡住            | 不知從哪開始         | 嘗試改成「暴力法 + 找重複 + 優化」流程 |

---

## ✨ 七、總結心法

> * 「設計演算法」的核心是找出**狀態變化規律**。
> * 三連問讓你**從直覺轉為模型思考**。
> * 任何解法都可以用 State–Transition–Traversal 語言描述。
> * 真正的高手不是會寫 DP，而是會「看出 DP」。
> * 當你能用這三詞描述任何演算法，你已進入設計者的層次。
