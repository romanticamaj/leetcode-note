<div align="center">

# DSA Pattern Playbook

**學會推導演算法、辨識 Pattern，並說清楚為什麼正確。**

從解題框架出發，學習資料結構與演算法。<br>
可複用心法 · C++ 模板 · 精選題庫 · 正確性推導

[English](README.md) · **繁體中文**

[開始學習](#開始學習) · [核心解題框架](#核心解題框架) · [Pattern 導覽](#pattern-導覽) · [精選題庫](#有目的地練習) · [有趣的延伸](#演算法之外的延伸)

</div>

---

一個演算法該記住什麼資訊？哪些工作可以省掉？為什麼可以安全地排除某個候選？

**DSA Pattern Playbook 把這些問題，連結到具體的解題模式與練習題。** 這份持續整理自 Gary Hsieh 學習筆記的資源，以可複用的推理為主軸：定義答案、建立正確的基準解、找出浪費的工作，再推導出能說明理由的優化。

> **閱讀語言：** 英文與繁中 README 都提供完整學習導覽。內文目前以**繁體中文**為主，保留英文技術術語，實作以 **C++** 為主；整個筆記庫尚未全面英文化。

## 開始學習

建議先具備基本程式能力，理解陣列、迴圈、函式與遞迴，再依目前的需求選擇入口：

| 你目前的狀況 | 從這裡開始 | 接下來怎麼做 |
|---|---|---|
| 正在學習 DSA Pattern | [Two Pointers 核心模式](Algorithms/Two_Pointers/01-Two_Pointers_Core_Patterns_and_Templates.md)＋[Grind 75](Checklists/Lists/Grind_75.md) | 按自己的速度練習，先理解每題的模式，再考慮計時。 |
| 會寫程式，但常常沒有思路 | [解題流程與假設檢查](Interview_Playbook/Problem_Solving_Process_and_Assumption_Checklist.md)＋[優化指北星](Interview_Playbook/Problem_Solving_Strategies.md) | 先說清楚正確的暴力解，再指出要省掉哪些工作。 |
| 學過演算法，想把概念串起來 | [State → Transition → Traversal](Meta_Frameworks/Problem_Classification_Framework/03-State_Transition_Traversal.md) | 用[統一狀態框架](Meta_Frameworks/State_Transition_Algorithm_Atlas.md)比較熟悉的技法。 |
| 正在準備技術面試 | [解題前 Checklist](Interview_Playbook/Pre_Solve_Interview_Checklist.md)＋[四大清單母集合](Checklists/Lists/00_Master_Union.md) | 從四份清單共同收錄的題目起步，再練習 [follow-up](Checklists/Lists/02_Followup_Problems.md)。 |

**第一次閱讀可以這樣做：** 打開 [Binary Search 標準模板](Algorithms/Binary_Search/00-Binary_Search_Standard_Template.md)，從[題庫](Checklists/Lists/)挑一道對應題目，先說明單調 predicate、區間不變量與終止條件，再開始實作。

## 學習循環

```text
定義答案 → 建立正確的基準解 → 找出浪費的工作
   ↑                              ↓
遷移到類題 ← 證明與測試 ← 推導解題模式
```

每題練完，留下四個之後能重新推導的重點：

1. **答案定義：** 寫成能直接檢查的條件或公式。
2. **基準解與成本：** 枚舉什麼、如何求值、時間花在哪裡。
3. **Pattern 與適用前提：** 省掉哪些工作，利用什麼性質才能這樣做。
4. **正確性與遷移：** 不變量或證明、邊界測試，以及 follow-up 改變了什麼。

## 核心解題框架

這些文件是整份 repo 的思考骨架。搭配題目閱讀即可，不需要先把所有筆記讀完。

| 框架 | 幫你回答的問題 |
|---|---|
| [先定義答案，再開始寫程式](Interview_Playbook/Problem_Solving_Process_and_Assumption_Checklist.md) | 能不能把題目展開成明確、可驗證的一行 `ANSWER`？ |
| [Brute Force → BUD ↔ BCR](Interview_Playbook/Problem_Solving_Strategies.md) | 瓶頸、不必要與重複工作在哪？合理的時間目標有什麼依據？ |
| [Problem Transformation](Meta_Frameworks/Problem_Transformation.md) | 如何把故事轉成實體、關係、限制與計算模型？ |
| [Quick Decision Map](Meta_Frameworks/Problem_Classification_Framework/02-Quick_Decision_Map.md) | 輸出目標、資料結構、限制與輸入規模，如何縮小技法選擇？ |
| [State → Transition → Traversal](Meta_Frameworks/Problem_Classification_Framework/03-State_Transition_Traversal.md) | 要記住什麼、如何改變、哪些結果必須先算？ |
| [Orthogonality 正交性](Meta_Frameworks/Orthogonality-Problem-Solving.md) | 哪些設計決策可以先分開思考，再確認彼此如何配合？ |
| [Loop Invariant](Proof_Techniques/Loop_Invariant.md) · [結構歸納法](Proof_Techniques/Structural_Induction.md) · [交換論證](Proof_Techniques/Exchange_Argument.md) | 如何說明迴圈、遞迴組合與貪心選擇的正確性？ |

### 用一張地圖串起演算法

**[演算法與資料結構的統一狀態框架](Meta_Frameworks/State_Transition_Algorithm_Atlas.md)**，用同一組問題理解不同技法：**目標、狀態、轉換、計算順序、正確性、終止與成本**。

2026 年 9 月的整理快照包含 **11 個分類、212 個條目**，附來源筆記對照。條目包含變體與組合模式，不代表 212 種互斥的演算法。

[閱讀 Markdown 版](Meta_Frameworks/State_Transition_Algorithm_Atlas.md) · [可下載的 HTML 閱讀版](Meta_Frameworks/State_Transition_Algorithm_Atlas.html)

HTML 版支援搜尋、分類篩選與展開閱讀。下載後可直接用瀏覽器開啟。

## Pattern 導覽

每一列都提供一個實作入口，以及值得往下追問的建模觀念。

| 主題 | 入門入口 | 深入理解 |
|---|---|---|
| Two Pointers | [核心模式與模板](Algorithms/Two_Pointers/01-Two_Pointers_Core_Patterns_and_Templates.md) | [快慢指標](Algorithms/Two_Pointers/02_Fast_and_Slow_Pointers.md) |
| Sliding Window | [擴張 → 修復 → 結算](Algorithms/Sliding_Window/00-Sliding_Window_Standard_Template.md) | [Constraint 追蹤與優化](Algorithms/Sliding_Window/01-Constraint_Tracking_and_Optimization.md) |
| Binary Search | [找第一個成立的 predicate](Algorithms/Binary_Search/00-Binary_Search_Standard_Template.md) | [在答案空間搜尋](Algorithms/Binary_Search/04-Binary_Search_on_Solution_Space.md) |
| Prefix Sum | [前綴和基礎](Algorithms/Prefix_Sum/01_Prefix_Sum_Intro.md) | [Running State 模式](Algorithms/Prefix_Sum/02_Running_State_Pattern.md) |
| Recursion & Trees | [遞迴設計原則](Algorithms/Design_Principles/Recursion/01-Recursion_Design_Principles.md) | [遞迴四大流派的狀態設計](Algorithms/Design_Principles/Recursion/State_Design_Across_Recursive_Paradigms.md) |
| Backtracking | [模板與模式](Algorithms/Backtracking/01-Backtracking_Templates_and_Patterns.md) | [已定 vs. 待定的候選者建模](Algorithms/Backtracking/03-Backtracking_Candidate_Modeling.md) |
| Dynamic Programming | [從暴力搜尋推導 DP](Algorithms/Dynamic_Programming/Fundamentals/02-Problem_Solving_Framework.md) | [狀態設計](Algorithms/Dynamic_Programming/State_Design/01-Essentials.md) |
| Graph Search | [圖論解題原則](Data_Structures/Graphs/Graph_Problem_Solving_Principles.md) | [隱性圖的節點建構](Data_Structures/Graphs/Implicit_Graph_Node_Construction.md) |
| Greedy & Heaps | [辨識與運用貪心](Algorithms/Greedy/Greedy_Identification_and_Application.md) | [Heap 決策心法](Data_Structures/Heaps/01-Heap_Decision_Making.md) |
| Monotonic Stack & Queue | [核心概念](Data_Structures/Stacks_and_Queues/Monotonic_Stacks/01-Monotonic_Stack_and_Queue.md) | [搜尋空間轉換](Data_Structures/Stacks_and_Queues/Monotonic_Stacks/02-Search_Space_Conversion.md) |
| 連通性與依賴關係 | [Union Find](Algorithms/Union_Find/01-Core_Concepts.md) | [Topological Sort](Algorithms/Topological_Sort/01-Core_Concepts_and_Applications.md) |

瀏覽完整的[演算法筆記](Algorithms/)、[資料結構筆記](Data_Structures/)，或用[技法檢查表](Checklists/Algorithm_Techniques_Checklist.md)找出需要補強的主題。

**模板慣例：** `00-<Technique>_Standard_Template.md` 代表該技法的標準模板，包含口訣、不變量、陷阱與面試話術。可以先讀上面的 Binary Search 與 Sliding Window。

## 有目的地練習

用題庫選題，再回到 Pattern 筆記說清楚學到了什麼。

| 題庫 | 學習用途 |
|---|---|
| [四大清單母集合 — 250 題](Checklists/Lists/00_Master_Union.md) | 四份清單合併去重的快照，按重疊程度分層。四份共同收錄的 37 題適合當起點；重疊程度是選題參考。 |
| [NeetCode 150](Checklists/Lists/NeetCode_150.md) | 依 Pattern 分類練習。 |
| [Grind 75](Checklists/Lists/Grind_75.md) | 依週次安排練習順序。 |
| [Top Interview 150](Checklists/Lists/Top_Interview_150.md) · [Top 100 Liked](Checklists/Lists/Top_100_Liked.md) | 用整理收錄的 LeetCode 學習清單擴充題型覆蓋。 |
| [Essential Problems](Checklists/Essential%20Problems/Essential_Problems.md) | 依技法探索維護者挑選的精選題目。 |
| [Technique Integration](Checklists/Essential%20Problems/Technique_Integration_Problems.md) | 練習組合多種技法、比較不同思路。 |
| [Follow-up 題型](Checklists/Lists/02_Followup_Problems.md) | 改變限制、處理變形，或口述 trade-off；頻率標記是編輯判斷。 |
| [專題練習 Playbook](Checklists/Trick%20Practice/) | 集中練習答案二分、Kadane、Knapsack、KMP 等技巧。 |

> 清單中的勾選、完成日期與進度總數，是**維護者的練習狀態**，不是讀者的先修要求。`✅` 表示也收錄於個人精選集，`🔒` 表示 Premium 題目。你可以用自己的副本記錄學習進度。

**Hard 題卡住時：** 用 [Hard 題學習策略](Interview_Playbook/Hard_Problem_Learning_Strategy.md)與[技巧參考表](Interview_Playbook/Hard_Techniques_Reference.md)，分辨是缺少一個 insight，還是尚未學過該技巧；需要時先回到較簡單的前置題型。

## 演算法之外的延伸

這些文章把實作、建模、數學與歷史連起來，也是這份筆記值得探索的部分。

| 推薦閱讀 | 值得帶走的觀念 |
|---|---|
| [Correct by Construction](Algorithms/Design_Principles/Correct_by_Construction.md) | 把正確性放進命名、型別與結構，讓它在忘記細節時仍然成立。 |
| [目的地反轉為起點](Algorithms/Design_Principles/Transformation_Patterns/Destination_as_Source_Reachability.md) | 反向搜尋，讓多個起點共用可達性計算。 |
| [Multi-source BFS 推導框架](Algorithms/BFS/MultiSource_BFS_Thinking_Framework.md) | 所有來源一起擴散，省掉反覆尋找最近來源的工作。 |
| [錨點分解](Algorithms/Divide_and_Conquer/08_Canonical_Anchor_Decomposition.md) | 用結構決定的錨點，推理分解的唯一性。 |
| [雙向約束分解](Algorithms/Design_Principles/Bidirectional_Constraint_Decomposition.md) | 分別處理單向約束，再組合結果。 |
| [Gas Station：歷史與前綴和的最低谷](Problem_History/LC_0134_Gas_Station.md) | 把程式題連回數學謎題與可查證的文獻。 |
| [Linked List Cycle II 互動圖解](Visualizations/142-Linked_List_Cycle_II.html) | 用視覺追蹤快慢指標；下載 HTML 後可在本機開啟。 |

繼續探索[題目的歷史與出處](Problem_History/README.md)、[C++ Reference](CPP_Reference/)、[Pattern 與關鍵字速查](Cheatsheet/LeetCode_Tricks_and_Keywords.md)，以及 [C++ One-liners](Cheatsheet/CPP_One_Liners.md)。

## 資料夾地圖

| 目錄 | 內容 |
|---|---|
| [`Meta_Frameworks/`](Meta_Frameworks/) | 建模、分類與跨技法連結 |
| [`Algorithms/`](Algorithms/) · [`Data_Structures/`](Data_Structures/) | Pattern、實作與取捨 |
| [`Proof_Techniques/`](Proof_Techniques/) | 正確性推理工具 |
| [`Checklists/`](Checklists/) | 題庫與技法覆蓋檢查 |
| [`Interview_Playbook/`](Interview_Playbook/) | 溝通、測試、複盤與學習策略 |
| [`CPP_Reference/`](CPP_Reference/) · [`Cheatsheet/`](Cheatsheet/) | 語言細節與速查 |
| [`Problem_History/`](Problem_History/README.md) · [`Visualizations/`](Visualizations/) | 歷史脈絡與獨立圖解 |

<details>
<summary><strong>維護者的學習紀錄與 AI 輔助流程</strong></summary>

[練習日誌](Checklists/Practice_Log.md)、[學習 Roadmap](Checklists/Learning_Roadmap.md)與[複習清單](Checklists/Essential%20Problems/Problem_Review.md)會繼續保留，記錄這份資源如何從實際練習持續演進。

專案 Skills 支援[模擬面試](.agents/skills/mock-interview/SKILL.md)、[Pattern 萃取](.agents/skills/extract-pattern/SKILL.md)、[Hard 題學習教練](.agents/skills/hard-coach/SKILL.md)與[練習紀錄](.agents/skills/practice-log/SKILL.md)。文件慣例收錄於 [AGENTS.md](AGENTS.md)，Claude Code 透過 [CLAUDE.md](CLAUDE.md)讀取。

</details>

## 一起改善這份 Playbook

歡迎修正錯誤、改善說明、補充反例、翻譯，以及串連既有筆記。提出修改時，請指出對應文件與問題；適合時附上小範例或正確性理由。

如果這份資源幫你理解了一個 Pattern，歡迎給它一顆 Star，或分享那篇幫到你的筆記。
