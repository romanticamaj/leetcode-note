# Problem Specification Confirmation — 解題心法

> 在動手設計演算法之前，先確認「我到底在解什麼問題」，
> 避免隱含假設、誤讀規格，確保解法落在正確的問題空間。

> **📌 定位：這份是面試開場跟面試官對齊規格用的溝通清單。** 平常練習不用跑完五步，只要寫一行展開後的 `ANSWER`，見 [Problem_Solving_Process_and_Assumption_Checklist.md](../../Interview_Playbook/Problem_Solving_Process_and_Assumption_Checklist.md) 第 1 步。

---

## 核心精神

**先鎖定 Problem Space，再進入 Solution Space。**

演算法錯誤，通常不是寫錯邏輯，
而是「一開始解的就不是題目真正要的東西」。

---

## 🧭 五步確認流程

```
┌─────────────────────────────────────────────────────────┐
│  Step 0: Problem Specification Confirmation             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   1. Input    →  型別、範圍、性質、邊界                  │
│       ↓                                                 │
│   2. Output   →  型別、唯一性、格式、in-place?          │
│       ↓                                                 │
│   3. Edge     →  最小規模、極端結構、模糊區              │
│       ↓                                                 │
│   4. Constraints → 複雜度上限 → 解法提示                │
│       ↓                                                 │
│   5. Invariant → 用一句話描述解法必須維持的條件          │
│                                                         │
└─────────────────────────────────────────────────────────┘
              ↓ 確認完成後進入 Algorithm Design
```

---

## Step 1 — 明確定義 Input（輸入規格）

確認你對輸入沒有任何未說出口的假設：

| 面向     | 確認項目                               |
| -------- | -------------------------------------- |
| **型別** | array / string / tree / graph / stream |
| **範圍** | 大小、長度、值域                       |
| **性質** | 是否有重複？是否已排序？大小寫敏感？   |
| **特殊** | 是否可能包含非預期元素（負數、空值）？ |
| **邊界** | 是否允許空輸入或最小輸入？             |

> 問自己：**「我是不是默默假設了某些 input 特性？」**

### 💬 面試問句範本

```
"Can the input be empty or contain only one element?"
"Are there duplicates in the input?"
"Is the array sorted or can I assume any ordering?"
"What's the range of values? Can there be negative numbers?"
"Is the string case-sensitive?"
```

---

## Step 2 — 明確定義 Output（輸出條件）

確認「什麼樣的結果才算正確」：

| 面向       | 確認項目                                   |
| ---------- | ------------------------------------------ |
| **型別**   | 回傳什麼型別？                             |
| **唯一性** | 是否只存在唯一正確答案？                   |
| **多解**   | 是否允許多個合法解？回傳任一個還是全部？   |
| **修改**   | 是否允許修改原始輸入（in-place vs copy）？ |
| **格式**   | 是否有順序或格式要求？                     |

> 問自己：**「成功條件是否被完整定義？」**

### 💬 面試問句範本

```
"Should I return one valid answer or all possible answers?"
"Can I modify the input array in-place?"
"Does the order of the output matter?"
"What should I return if multiple valid answers exist?"
```

---

## Step 3 — 確認 Edge / Corner Cases（邊界條件）

快速掃描問題邊界，而不是列舉所有測試：

| 類型           | 範例                          |
| -------------- | ----------------------------- |
| **最小規模**   | 空輸入、單一元素              |
| **極端結構**   | 全部符合條件 / 全部不符合條件 |
| **重複元素**   | 所有元素相同                  |
| **邊界值**     | 最大值、最小值、零、負數      |
| **規格模糊區** | 容易產生不同解讀的地方        |

> 目的不是測試程式碼，而是**釐清規格邊界在哪裡畫線**。

### 💬 面試問句範本

```
"What should I return if the input is empty?"
"What if no valid answer exists?"
"How should I handle the case when all elements are the same?"
```

---

## Step 4 — Constraints 作為設計訊號

限制條件不是背景資訊，而是解法提示：

| n 範圍 | 允許複雜度 | 暗示技術                       |
| ------ | ---------- | ------------------------------ |
| ≤ 10   | O(n!)      | Backtracking, Permutations     |
| ≤ 20   | O(2ⁿ)      | Bitmask DP, Subset Enumeration |
| ≤ 100  | O(n³)      | Floyd-Warshall, 3D DP          |
| ≤ 1000 | O(n²)      | 2D DP, All Pairs               |
| ≤ 10⁵  | O(n log n) | Sort, Binary Search, Heap      |
| ≤ 10⁶  | O(n)       | Hash, Prefix Sum, Two Pointers |
| > 10⁶  | O(log n)   | Binary Search, Math            |

> 問自己：**「題目允許我使用哪些工具？」**

### 💬 面試問句範本

```
"What's the expected size of the input?"
"Are there any time or space constraints I should be aware of?"
```

---

## Step 5 — Solution Invariant（解法前的關鍵一步）

在寫任何程式碼之前，用一句話描述：

- 在解法執行過程中，**哪些條件必須一直成立？**
- 哪些資料已處理，哪些尚未處理？
- 指標/索引代表的意義是什麼？

> Invariant 是規格與解法之間的橋樑，能反向驗證你是否真的理解了問題。

### 範例

| 問題類型        | Invariant 描述                                        |
| --------------- | ----------------------------------------------------- |
| Two Sum         | `left` 指向未檢查的最小值，`right` 指向未檢查的最大值 |
| Sliding Window  | 窗口內的元素符合某個條件（如 sum ≤ k）                |
| Binary Search   | `[left, right]` 區間內一定包含答案                    |
| Monotonic Stack | Stack 內元素維持單調遞增/遞減                         |

---

## ⚡ 一句話版本（面試開場用）

> **「在解題前，我會先確認 input、output、edge cases 與 constraints，確保沒有任何隱含假設。」**

---

## 🎯 使用時機

- ✅ 面試白板題目開始前
- ✅ LeetCode 第一次閱讀題目
- ✅ 解到一半覺得「哪裡怪怪的」
- ✅ Debug 發現邏輯正確卻一直 WA

---

## ✅ Quick Checklist

```
☐ Input 型別與範圍確認？
☐ Input 有無隱含假設（排序、重複、正負）？
☐ Output 唯一性與格式確認？
☐ Edge cases 邊界畫線？
☐ Constraints 反推複雜度上限？
☐ Invariant 一句話描述？
```

---

## 結語

好的演算法解法，
不是從 code 開始，
而是從「問題定義是否清楚」開始。

**Rule of Thumb**: 如果你無法用一句話說出 invariant，代表你還沒真正理解問題或是解法。
