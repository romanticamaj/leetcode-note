# Engineering Problem-Solving Playbook

這個 repository 是一份結構化的筆記集合，收錄解題模式（心法）、設計原則與思考框架，目標是準備技術面試與培養工程問題解決能力。

它刻意**不收錄題解**。價值在於 **"how" 與 "why"** — 那些可以跨題目重複使用的策略、設計原則與測試框架。

> 目前約 300 篇筆記。語言以繁體中文為主，技術術語保留英文。

---

## 統一狀態框架總覽

[演算法與資料結構的統一狀態框架](Meta_Frameworks/State_Transition_Algorithm_Atlas.md) · [HTML 閱讀版](Meta_Frameworks/State_Transition_Algorithm_Atlas.html)

用「目標、狀態、轉換、計算順序、正確性與終止、成本」重新詮釋筆記中的算法與資料結構：212 個條目、11 個分類，附關鍵論述、適用條件與來源覆蓋對照。HTML 支援搜尋、分類篩選與展開閱讀；下載後可直接用瀏覽器開啟。

---

## 核心理念

1. **Pattern Extraction（模式萃取）** — 把具體題目蒸餾成抽象、可複用的模式（如 "One-Liner DFS"、"Vertex Mapping"、"Destination-as-Source Reachability"）
2. **Systematic Thinking（系統化思考）** — 對測試設計、演算法設計等複雜任務套用結構化框架
3. **Best Practices Documentation** — 記錄語言慣用法、常見陷阱與效能考量（C++ STL 實作細節、integer overflow 等）

---

## Repository 結構

### 📐 標準模板慣例

每個技法資料夾底下，`00-` 這個編號**保留給該技法的標準模板**：

```
Algorithms/<技法>/00-<技法>_Standard_Template.md
```

例：`Algorithms/Sliding_Window/00-Sliding_Window_Standard_Template.md`

這樣任何技法的「就背這個」模板永遠排在第一個，也能一次列出全部：

```bash
find . -name '00-*_Standard_Template.md'
```

標準模板文件包含：**唯一要背的 C++ 模板 · 步驟口訣表 · 循環不變量 · ⚠️ 被淘汰的寫法與原因 · 面試話術**。

> 原則：當一個技法有明顯較優的寫法時，**砍掉其他選項，不要並列**。目標是每個技法只有一個模板，內化成肌肉記憶。

---

### 🧠 核心知識

| 目錄 | 篇數 | 內容 |
|---|---|---|
| **`Algorithms/`** | 152 | 20 個技法分類的心法與模板：Two Pointers、Sliding Window、Binary Search、DFS/BFS、DP、Greedy、Divide & Conquer、Union Find、Topological Sort、Sweep Line、Bit Manipulation… |
| **`Data_Structures/`** | 63 | 實作細節、trade-off 與使用模式：Trees、Graphs、Heaps、Trie、Monotonic Stack、BIT… |
| **`CPP_Reference/`** | 30 | C++ 慣用法、STL 容器行為、型別陷阱、常見編碼錯誤 |

### 🚀 策略與框架

| 目錄 | 篇數 | 內容 |
|---|---|---|
| **`Interview_Playbook/`** | 7 | 面試全流程策略：解題前 checklist、面試階段拆解、Hard 題學習法、code review 原則 |
| **`Meta_Frameworks/`** | 7 | 問題分類框架、Quick Decision Map、問題轉換（Problem Transformation）、正交性思考 |
| **`Test_Case_Construction/`** | 7 | 測試案例設計框架，含 tree/graph 專用策略與記法 |
| **`Proof_Techniques/`** | 3 | Exchange Argument、Loop Invariant、Structural Induction — 用來證明貪心與迴圈正確性 |

### 📋 清單與速查

| 目錄 | 內容 |
|---|---|
| **`Checklists/`** | 技法檢查表、學習 roadmap、刷題清單、刷題日誌（見下方「刷題準備途徑」） |
| **`Cheatsheet/`** | `Gary's DSA Cheatsheet`、`LeetCode_Tricks_and_Keywords`、`CPP_One_Liners` |
| **`Reading/`** | 參考書 PDF（CLRS、Kleinberg & Tardos、EPI、CtCI、劉汝佳） |

---

## 📈 刷題準備途徑

### 清單體系 — `Checklists/Lists/`

四份主流面試清單，全部附 LeetCode 題號、難度、連結，Premium 題標 🔒：

| 檔案 | 內容 |
|---|---|
| **`00_Master_Union.md`** | **四份清單去重母集合（250 題）**，按「出現在幾份清單」分四層排序 — 共識度越高越該先刷 |
| `01_Grind75_Easy_Warmup.md` | Grind 75 的 24 題 Easy 暖身組，附技法覆蓋檢查表 |
| `NeetCode_150.md` | NeetCode 150（18 分類） |
| `Grind_75.md` | Grind 75（官方 8 週順序） |
| `Top_Interview_150.md` | LeetCode 官方 Top Interview 150（19 分類） |
| `Top_100_Liked.md` | LeetCode 官方 Hot 100 |

**共識分層**：🔥🔥🔥🔥 四份都有 37 題 · 🔥🔥🔥 三份 35 題 · 🔥🔥 兩份 44 題 · 🔥 單份 134 題

### 建議路徑

```
1. 暖身    Lists/01_Grind75_Easy_Warmup.md  (24 題 Easy，找回手感)
2. 核心    Lists/00_Master_Union.md 的 🔥🔥🔥🔥 + 🔥🔥🔥  (72 題，社群鐵共識)
3. 主線    Lists/NeetCode_150.md 全通
4. 補強    Top_Interview_150 的實作繁瑣型題目
5. 衝刺    公司 tag + Last 6 months（面試前 2 週）
```

### 個人題庫 — `Checklists/Essential Problems/`

- `Essential_Problems.md` — 個人精選必做題，按技法分類
- `Archetype_Problems.md` — 各領域的原型問題
- `Technique_Integration_Problems.md` — 需要組合多種技法的題目
- `Problem_Review.md` — 待複習題目追蹤

### 進階練習

- `Checklists/Trick Practice/` — 7 份專題 playbook（Binary Search on Answer、Kadane、KMP、Knapsack、D&C Hard…）
- `Checklists/Super_Hard/` — 單題深度拆解
- `Checklists/Algorithm_Techniques_Checklist.md` — 技法總表，含難度評級與複雜度
- `Checklists/Learning_Roadmap.md` — 解題時遇到的 follow-up 待辦

### 刷題日誌 — `Checklists/Practice_Log.md`

極簡格式，每天一個日期區塊：題目列表 + 本日心得。

---

## 🤖 Claude Code 整合

`.claude/agents/` 內建三個 subagent：

| Agent | 用途 |
|---|---|
| **`google-interviewer`** | 模擬 Google L5 技術面試（繁體中文）。**貼上 LeetCode 題目時會自動觸發** — 不直接給解法，只在要求時給最小提示 |
| **`playbook-extractor`** | 從解法萃取模式，產出結構化 playbook 文件 |
| **`pattern-trick-extractor`** | 從多題解法中萃取共通心法，產出精簡版 playbook |

專案慣例（文件風格、命名、章節模板）記錄在 `CLAUDE.md`。

---

## 如何使用

1. **先讀 Playbook** — 從 `Interview_Playbook/` 和 `Meta_Frameworks/` 建立解題流程的基礎
2. **照清單刷題** — 依上方「建議路徑」，用 `Checklists/Lists/` 追蹤進度
3. **卡住就回查心法** — 到 `Algorithms/<技法>/` 或 `Data_Structures/` 找對應筆記
4. **語言問題查 Reference** — `CPP_Reference/` 與 `Cheatsheet/`
5. **解完就抽象化** — 不要只存解法。想清楚底層模式，用 `playbook-extractor` 寫進對應章節

---

這是一份持續演進的文件。它的價值來自「學習 → 抽象 → 精煉」的循環，而不是題目數量。
