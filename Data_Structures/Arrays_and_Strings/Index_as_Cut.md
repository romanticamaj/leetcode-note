# i 是切點，不是元素 (Index as Cut)

字串 / 陣列題裡，`i` 常常同時被讀成「長度」和「index」，混在一起就搞不清楚 base case 是「長度到了」還是「index 越界」。解法是換一個圖像：**`i` 指的是兩個字元之間的縫，不是某個字元**。

---

## 🧠 核心概念

```
s:   a  a  b  c  c
    ↑  ↑  ↑  ↑  ↑  ↑
    0  1  2  3  4  5      ← 切點，共 m + 1 個（0..m）
```

切點 `i` 把字串切成兩半：

| 讀法 | 區間 | 意義 |
|---|---|---|
| **已用 / 已完成** | `[0, i)` | 長度 = `i` |
| **剩下 / 未處理** | `[i, m)` | 從 `s[i]` 開始 |

「已用的長度」和「剩下的起點」是**同一個數字的兩面**，不需要二選一。

> ⚠️ 這不是巧合，是 **0-indexed + 半開區間** 兩個約定一起造成的：`[0, i)` 的長度是 `i − 0 = i`。換一個約定就會分開，例如從後往前走，`i` = 下一個要用的 index：剩下的是 `s[0..i]`（長度 `i + 1`），已用的長度是 `m − 1 − i`。所以**不要背「i 就是長度」，要背「i 是切點」**。

---

## 🧩 怎麼用：一個讀法只負責一件事

1. **狀態定義只挑一邊講**。Top-down 講剩下的（suffix），bottom-up 講已完成的（prefix）。
2. **長度只拿來定邊界**。「用完 m 個」就是 `i == m`，所以 `i` 有 `m + 1` 種值，cache / dp 表開 `m + 1`。

**試金石：`i` 可不可以等於 `m`？** 可以的話 `i` 就是切點，狀態空間是 `m + 1`，`i == m` 是**合法狀態**（空的剩餘），不是越界。

---

## 🧩 Top-down vs Bottom-up 對照

以 [97. Interleaving String](https://leetcode.com/problems/interleaving-string/) 為例（`m = s1.size()`、`n = s2.size()`）：

| | Top-down（往前 traverse） | Bottom-up（填表） |
|---|---|---|
| 狀態講哪一邊 | **Suffix**：剩下的 | **Prefix**：已完成的 |
| 定義 | `dp(i, j)`：`s1[i:]` 和 `s2[j:]` 能否交錯成 `s3[i+j:]` | `dp[i][j]`：`s1` 前 `i` 個和 `s2` 前 `j` 個能否交錯成 `s3` 前 `i+j` 個 |
| Base case | 兩個剩餘都空：`i == m && j == n` | 兩個已用都空：`dp[0][0] = true` |
| 讀的字元 | `s1[i]`（下一個要用的） | `s1[i-1]`（最後用掉的） |
| 表的大小 | `(m+1) × (n+1)` | `(m+1) × (n+1)` |

兩邊的表一樣大，因為都是在切點上定義狀態。Bottom-up 的 off-by-one 就來自那一欄：狀態用長度 `i`，存取字元要寫 `s1[i-1]`。

---

## ⚠️ 兩種檢查不要混

| 檢查 | 問的是 | 97 的寫法 |
|---|---|---|
| **終止狀態**（base case） | 還有沒有剩下的？ | `i == m && j == n`（開頭已檢查 `m + n == s3.size()`，等價於 `i + j == s3.size()`） |
| **轉移守衛** | 還能不能再拿一個？ | 讀 `s1[i]` 前先確認 `i < m` |

「index 越界」只出現在**轉移守衛**，它不是 base case。

---

## ✅ 同一個圖像出現在哪

- 半開區間二分搜尋：[00-Binary_Search_Standard_Template.md](../../Algorithms/Binary_Search/00-Binary_Search_Standard_Template.md)
- 荷蘭國旗 `[0, left)` 是 0：`left` 既是 0 的個數，也是下一個放 0 的位置，見 [02-Dutch_National_Flag.md](../../Algorithms/Partition/02-Dutch_National_Flag.md)
- 雙序列 DP（LCS、Edit Distance、Interleaving String）：`dp[i][j]` 定義在切點上，表都是 `(m+1) × (n+1)`
- Top-down 的邊界放法：[Boundary_Condition_Handling.md](../../Algorithms/Dynamic_Programming/Implementation/Boundary_Condition_Handling.md)

---

## ✅ Checklist

- [ ] 寫狀態前先問：`i` 可不可以等於 `m`？
- [ ] 狀態定義只講一邊：top-down 講剩下的，bottom-up 講已完成的
- [ ] Base case 是「空的剩餘 / 空的已完成」，不是「index 越界」
- [ ] 轉移前的 `i < m` 是守衛，跟 base case 分開寫
- [ ] Bottom-up 讀字元時記得是 `s[i-1]`
