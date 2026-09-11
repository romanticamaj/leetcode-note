# 演算法與資料結構的統一狀態框架（State–Transition Algorithm Atlas）

[HTML 閱讀版](State_Transition_Algorithm_Atlas.html) · [原始三連問](Problem_Classification_Framework/03-State_Transition_Traversal.md)

以同一套語言重新理解 leetcode-note 的演算法、資料結構、重要變體與組合模式。這是一份概念與正確性筆記，不提供逐題程式解答。

盤點日期：2026-09-10。來源快照：96da0e3865c116340a3c4843ef4eed38399f63b1。讀取 295 份非隱藏 Markdown；其中 Algorithms 與 Data_Structures 共 214 份，每份皆有來源對照。整理為 212 個條目；一個條目可包含同義別名或同一契約下的相關變體，這個數字不代表 212 種互斥算法。

## 01　統一框架：目標決定資訊，性質決定省略

演算法設計，是根據目標選擇資訊表示，定義可行的轉換，再利用問題的性質，安排並減少必要的計算，或讓操作變便宜。能用狀態轉換描述一個算法，不等於已證明算法正確，也不等於能自動推導最快解法。

| 框架層 | 需要明確交代的內容 | 本筆記的固定欄位 |
| --- | --- | --- |
| 目標 | 存在、計數、最佳值、構造或查詢；不同目標會改變可合併的資訊。 | 目標 |
| 表示 | 保留哪些歷史、位置、資源、結構與結果；哪些差異影響未來。 | 狀態 |
| 演進 | 合法動作、子問題依賴、結果組合，以及資料結構更新。 | 轉換 |
| 排程 | 誰先處理、何時可以使用結果、何時必須保留舊版本。 | 計算順序 |
| 保證與代價 | 不變量、完整性、最優性、進展與終止；總工作及空間。 | 正確性與終止＋成本 |

## 02　三種狀態，先分清楚

| 種類 | 描述 | 例子 |
| --- | --- | --- |
| 問題狀態 | 辨識一個後續任務所需的資訊。 | DP 的索引／剩餘容量；搜尋中的位置與鑰匙。 |
| 結果或標籤 | 目前對該問題知道多少，以及算出了什麼。 | 距離、方法數、最佳收益、前驅見證。 |
| 執行與表示狀態 | 為了安排與恢復工作而保存的資訊。 | call stack、queue、游標、DFS 顏色、lazy tag。 |

這三種角色可以同時存在。Dijkstra 的節點識別、目前最短距離與 heap 內的舊候選是三件不同的事。遞迴參數也未必包含整個程序狀態：外部環境、尚待返回的 frame 與部分結果都可能參與計算。

狀態充分性必須相對於目標判定。不同歷史映射到同一問題狀態後，應保留相同的合法後續，以及能正確組合的後續貢獻；已付出的成本可以另存標籤。計數時能共用後續計算，但不同抵達方式的貢獻不能直接刪除。

## 03　效率從哪裡來

| 操作 | 省下什麼 | 典型條目 | 不能省略的前提 |
| --- | --- | --- | --- |
| 等價合併 | 相同子問題的重複計算。 | Memoization、DP、Canonical Form。 | 未來行為及目標貢獻可正確共用。 |
| 支配淘汰 | 不可能比已保留候選更好的選擇。 | LIS tails、Top-K、部分資源剪枝。 | 所有相關成本與資源方向都不差。 |
| 整批排除 | 已證明不可能包含答案的候選。 | Binary Search、Pruning。 | 單調性、上下界或不可行性證明。 |
| 增量維護 | 相鄰查詢重複做的相同工作。 | Sliding Window、Frequency Counter。 | 能正確加入、移除或修復摘要。 |
| 索引與摘要 | 每次查詢都重新掃描原始資料。 | Hash、Heap、Prefix、Fenwick、Segment Tree。 | 查詢能力與預處理／更新成本匹配。 |
| 排程與生命週期 | 多餘中間版本與不必要的重算。 | Topological Order、Rolling DP、Offline。 | 依賴已完成，覆寫不會破壞尚待使用的值。 |
| 轉換合成 | 重複執行相同一步轉換。 | Fast Power、Matrix Exponentiation。 | 組合規則可結合，矩陣版本需線性固定轉移。 |
| 表示變緊湊 | 資料搬移、集合運算與控制資訊的成本。 | Bitmask、Morris、Swap、Index Mapping。 | 資訊未丟失且布局修改可正確維護／復原。 |

「壓縮」要指明是哪一種：bitmask 常只壓縮表示；滾動陣列縮短中間值的保存時間；memoization 合併重複計算；支配剪枝則保留較有利的候選。它們不能共用同一份正確性證明。

## 04　同一框架如何呈現不同算法

| 比較 | 共同部分 | 真正不同之處 |
| --- | --- | --- |
| DFS／BFS | 相同狀態圖與合法邊。 | 排程不同；等成本 BFS 的層序提供首次抵達最短保證。 |
| BFS／Dijkstra／SPFA | 傳播可達或距離資訊。 | FIFO、最小標籤定案、反覆改善三種排程與完成語義。 |
| Backtracking／DP | 決策與子問題關係。 | 列舉歷史與共用子問題結果；輸出目標影響是否能合併。 |
| DP／Greedy | 都需要狀態、合法選擇與目標。 | DP 聚合必要選項；Greedy 需證明選擇或替換安全。 |
| Prefix／Fenwick／Segment Tree | 保存區間摘要。 | 靜態逆運算、動態前綴分解、一般結合運算的區間分解。 |
| 雙堆中位數／雙堆貪婪 | 使用兩個 heap。 | 一者維持秩分割，另一者分離可行性與收益排序。 |
| Morris／Explicit Stack | 保存返回工作。 | 一者借用樹內連結，另一者使用外部 frame。 |
| Knuth／D&C DP Optimization | 利用最佳切點的單調性減少轉移枚舉。 | 適用遞推、單調界線與複雜度保證不同。 |

## 05　閱讀與範圍

每個條目都有相同六欄與一段「關鍵論述」。關鍵論述說明它利用了什麼性質，因此少記哪些資訊、少做哪些計算，或讓哪些操作更便宜。成本欄使用標準算法版本；未特別標明時，固定大小鍵與 machine-word 算術視為常數成本，圖的儲存成本另依表示說明。

n 為資料量、V/E 為圖的點／邊數、h 為樹高、w 在樹遍歷表示最大層寬，在 bitset 表示 machine-word 位寬；各條目會交代其局部參數。期望、攤銷與最壞成本不互換，輸出量、長字串複製／hash 與大整數運算必須另外計入。

來源範圍包括 Algorithms、Data_Structures、CPP_Reference、Cheatsheet、Checklists、Interview_Playbook、Meta_Frameworks、Proof_Techniques 與 Test_Case_Construction 中可辨識的算法與資料結構。Reading 的八本／份 PDF 是參考讀物，依 repo 慣例不當作作者筆記，這次未展開書內所有算法。純題目名稱不會被當成已記錄的完整解法；有明確命名的技巧與解法變體則納入。

「既有論述延伸」表示來源已有對應說明；「清單／提及延伸」表示來源主要是命名、比較或待學項，本次補上框架詮釋；「辨義補充」用於防止原筆記的相近概念被誤用。這些標籤描述來源深度，不表示已經練熟。少數條目由來源的解法描述抽象命名，未假裝原 repo 已有同名專篇。

## 分類索引

- [建模與控制（8）](#chapter-1)
- [搜尋與圖（18）](#chapter-2)
- [枚舉與分治（10）](#chapter-3)
- [動態規劃（21）](#chapter-4)
- [排序與搜尋（20）](#chapter-5)
- [指標與區間（12）](#chapter-6)
- [聚合與貪婪（17）](#chapter-7)
- [資料結構（48）](#chapter-8)
- [數學與表示（20）](#chapter-9)
- [進階延伸（23）](#chapter-10)
- [組合與證明（15）](#chapter-11)

<a id="chapter-1"></a>
## 建模與控制

<a id="recursion"></a>
### 001 · Recursion 遞迴

來源深度：既有論述延伸

**關鍵論述：** 遞迴把控制狀態交給 call stack 保存；尾呼叫不保證被 C++ 編譯器消除。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 求解可由較小子問題定義的任務。 |
| 狀態 State | 子問題參數、外部環境；執行上另含返回位置與局部值。 |
| 轉換 Transition | 建立子呼叫，接收回傳值，再依契約組合。 |
| 計算順序 Order | 依資訊需求選擇前序、中序、後序；尾遞迴可改迴圈。 |
| 正確性與終止 Correctness | 基底正確、子問題契約成立，且良基度量持續下降。 |
| 成本 Cost | 以遞迴樹的總工作計時；額外空間通常為深度乘每層資料量。 |

來源：

- [遞迴設計心法：狀態、邊界與遞迴關係](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Recursion/01-Recursion_Design_Principles.md)
- [演算法的時序模式 (Temporal Patterns in Algorithms)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Recursion/02-Temporal_Patterns_in_Algorithms.md)
- [進階遞迴設計心法 (Advanced Recursion Playbook)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Recursion/03-Advanced_Recursion_Playbook.md)
- [遞迴模式對比：Top-Down vs Bottom-Up Recursion](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Recursion/04-Top_Down_vs_Bottom_Up_Recursion.md)
- [遞迴設計四大流派：狀態設計心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Recursion/State_Design_Across_Recursive_Paradigms.md)
- [Orthogonality 解題心法（精華版）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Orthogonality-Problem-Solving.md)

<a id="iterative-traversal"></a>
### 002 · 遞迴轉迭代與 Explicit Stack

來源深度：既有論述延伸

**關鍵論述：** 只保存節點有時不夠；還要能分辨「剛進來」和「子問題已完成」。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 手動重現遞迴的處理與返回時機。 |
| 狀態 State | 目前節點、待辦堆疊、處理階段或 lastVisited。 |
| 轉換 Transition | 暫停父工作、處理子工作，再恢復對應階段。 |
| 計算順序 Order | stack 模擬 LIFO；N 元樹可保存下一個子節點索引。 |
| 正確性與終止 Correctness | 每個 frame 的語義必須與遞迴中的暫停點一致。 |
| 成本 Cost | 樹遍歷 O(n) 時間、O(h) stack；一次壓入所有孩子可占更多空間。 |

來源：

- [心法：將遞迴轉換為迭代](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Iterative_Traversal/01-Recursive_to_Iterative_Conversion.md)
- [Visit Nature 快速參考 / Quick Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Iterative_Traversal/02-Visit_Nature_Quick_Reference.md)
- [Current Pointer 實作模式 / Iterative Traversal Implementations](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Iterative_Traversal/03-Current_Pointer_Implementations.md)
- [深入解析：迭代 Postorder Traversal 中 lastVisited 的正確性](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Iterative_Traversal/04-Postorder_lastVisited_Deep_Dive.md)
- [統一心法：迭代遍歷的多重視角](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Iterative_Traversal/05-Unified_Framework.md)

<a id="simulation"></a>
### 003 · Simulation／Cellular Automaton

來源深度：清單／提及延伸

**關鍵論述：** Game of Life 的難點在狀態版本；原地編碼須同時容納更新前後資訊。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 依規則重現系統演進。 |
| 狀態 State | 盤面、時間、待執行事件，以及必要的舊版本。 |
| 轉換 Transition | 從當輪狀態計算下一輪，或跳到下一個事件。 |
| 計算順序 Order | 同步更新需先保留舊值；事件模擬依時間排序。 |
| 正確性與終止 Correctness | 所有讀取必須屬於正確時間版本，避免同輪新舊狀態混用。 |
| 成本 Cost | T 輪各處理 n 單位為 O(Tn)；事件版另計排程成本。 |

來源：

- [📘 DSA Design Pattern Roadmap](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/01-Interview_Timing_Framework.md)

<a id="dfa"></a>
### 004 · DFA／有限狀態機

來源深度：清單／提及延伸

**關鍵論述：** 複雜語法用轉移表表示；DFA 本身沒有回溯或同時多條執行路徑。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 辨識符合規則的輸入序列。 |
| 狀態 State | 目前語法狀態、輸入位置與必要累積值。 |
| 轉換 Transition | 依目前狀態及輸入符號，移到唯一下一狀態。 |
| 計算順序 Order | 按輸入順序讀取，結束後檢查接受狀態。 |
| 正確性與終止 Correctness | 每個狀態精確代表已讀前綴的語義；拒絕與結束條件分開。 |
| 成本 Cost | 固定狀態與字母表下 O(n) 時間、O(1) 控制空間。 |

來源：

- [Sequential Phase Consumption 心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Sequential_Phase_Consumption.md)
- [解題 Follow-up 待辦清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Learning_Roadmap.md)

<a id="phase"></a>
### 005 · Sequential Phase Consumption

來源深度：既有論述延伸

**關鍵論述：** 程式所在位置本身就在保存狀態，減少重複的布林旗標。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 解析具固定階段順序的輸入。 |
| 狀態 State | 輸入游標、目前程式階段、局部累積值。 |
| 轉換 Transition | 消耗符合當階段的符號，再移到下一階段。 |
| 計算順序 Order | 空白、符號、內容等按文法順序；可選階段消耗零次。 |
| 正確性與終止 Correctness | 每階段消耗且只消耗合法前綴；必要內容與結尾需驗證。 |
| 成本 Cost | 游標單調前進且每符號 O(1) 處理時，總 O(n)。 |

來源：

- [Sequential Phase Consumption 心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Sequential_Phase_Consumption.md)
- [🎯 Sequential Phase Consumption - 練習路徑](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Sequential_Phase_Consumption_Playbook.md)

<a id="boundary"></a>
### 006 · Boundary-Driven Processing

來源深度：既有論述延伸

**關鍵論述：** 把「何時結算」綁定邊界，使中途不完整狀態不外洩。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 按完整片段處理分段資料。 |
| 狀態 State | 片段起點、終點搜尋游標、片段摘要。 |
| 轉換 Transition | 先確定邊界，再結算整段，移往下一段。 |
| 計算順序 Order | 外層按段，內層只向前找段尾。 |
| 正確性與終止 Correctness | 各片段互斥且完整覆蓋待處理輸入。 |
| 成本 Cost | 每個元素被常數次掃描時 O(n)，不是看到兩層迴圈就 O(n²)。 |

來源：

- [Boundary-Driven Processing 心法（邊界驅動處理）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Boundary_Driven_Processing.md)

<a id="identity"></a>
### 007 · Entity Identity／Index as Reference

來源深度：既有論述延伸

**關鍵論述：** 先決定「什麼才算同一個東西」，才能安全設計 visited 與去重。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 保存正確的實體身份與來源。 |
| 狀態 State | 唯一 ID／索引及其屬性，避免只保存可能重複的值。 |
| 轉換 Transition | 透過 ID 查找、更新、連結或記錄位置。 |
| 計算順序 Order | 跟隨主算法；刪除與搬移時同步更新索引映射。 |
| 正確性與終止 Correctness | 同值不代表同實體；映射在結構變更後仍須一致。 |
| 成本 Cost | 索引直接存取 O(1)；map/hash 依實作另計。 |

來源：

- [心法：使用索引作為參考 (Index as Reference)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Common_Patterns/Index_as_Reference.md)
- [心法：實體身份原則 (Entity Identity Principle)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Entity_Identity_Principle.md)

<a id="implicit-graph"></a>
### 008 · Implicit Graph／Vertex Mapping

來源深度：既有論述延伸

**關鍵論述：** 圖不必先建好；節點的定義比輸入看起來像不像圖更重要。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 把操作問題表示成可搜尋的狀態圖。 |
| 狀態 State | 位置或盤面，加上會影響合法動作的條件。 |
| 轉換 Transition | 按規則即時產生鄰居；座標映射提供等價表示。 |
| 計算順序 Order | 交給 BFS、DFS 或最短路算法排程。 |
| 正確性與終止 Correctness | 表示不可合併未來不同的狀態；映射須保留邊與成本。 |
| 成本 Cost | 總成本包含產生鄰居、複製、比較與 hash；未必只是 O(V+E)。 |

來源：

- [BFS 解題模式：頂點映射 (Vertex Mapping)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/BFS_Vertex_Mapping_Pattern.md)
- [心法：隱性圖的節點建構 (Node Construction in Implicit Graphs)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Implicit_Graph_Node_Construction.md)
- [隱式圖 (Implicit Graphs)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Implicit_Graphs.md)


<a id="chapter-2"></a>
## 搜尋與圖

<a id="dfs"></a>
### 009 · DFS／Flood Fill／Connected Components

來源深度：既有論述延伸

**關鍵論述：** DFS 定義探索順序；短路回傳與 one-liner 只是相同邏輯的表達方式。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 探索可達節點、連通分量或遞迴結構。 |
| 狀態 State | 當前節點、visited、待返回工作；必要時加入路徑條件。 |
| 轉換 Transition | 探索未處理鄰居，完成後返回。 |
| 計算順序 Order | 深入一條分支後才探索兄弟分支。 |
| 正確性與終止 Correctness | 一般靜態可達性可每節點一次；路徑限制要擴充狀態。 |
| 成本 Cost | 鄰接表 O(V+E)；visited/stack O(V)，樹路徑 stack O(h)。 |

來源：

- [DFS 策略：從 Tree 到 Graph 的演進與對比](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/01-DFS_Tree_vs_Graph.md)
- [DFS 複雜度分析：通用模型（圖與樹的比較）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/02-DFS_Complexity_Analysis.md)
- [心法: 三色節點著色 DFS (CLRS 風格)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/03-Node_Coloring_DFS.md)
- [DFS 與遞迴設計：路徑查找與值的聚合](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/04-DFS_with_Recursion_Design.md)
- [Iterative DFS 在 Tree 與 Graph 中的結構比較與觀察](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/05-IterativeDFS_Tree_vs_Graph.md)
- [DFS 優化心法：「單行」DFS 模式 (The "One-Liner" DFS Pattern)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/06-One-Liner_DFS_Pattern.md)
- [Hierholzer's Algorithm 核心概念](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/Hierholzers/01-Hierholzers_Core_Concepts.md)
- [Node-Based vs Edge-Based Implementation](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/Hierholzers/02-Node_vs_Edge_Based_Implementation.md)
- [連通性問題：DFS vs. BFS 策略比較](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Traversal_Strategies/DFS_vs_BFS_for_Connectivity.md)
- [圖遍歷優化：當圖是樹時，省略 visited 集合](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Traversal_Strategies/Graph_as_Tree_Traversal.md)
- [深度優先搜索 (Depth-First Search, DFS)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/DFS.md)

<a id="node-color"></a>
### 010 · Node Coloring／有向環偵測

來源深度：既有論述延伸

**關鍵論述：** visited 的布林值不足以區分「算過」與「正在算」。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 分辨尚未探索、正在探索與已完成的依賴。 |
| 狀態 State | 白／灰／黑三色、DFS stack、完成順序。 |
| 轉換 Transition | 進入變灰；所有子依賴完成後變黑。 |
| 計算順序 Order | 深度優先；灰色集合代表仍在作用中的祖先鏈。 |
| 正確性與終止 Correctness | 遇到灰色邊才能推出有向環；遇黑色只代表已完成依賴。 |
| 成本 Cost | O(V+E) 時間、O(V) 空間。 |

來源：

- [心法: 三色節點著色 DFS (CLRS 風格)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/03-Node_Coloring_DFS.md)
- [基於 DFS 的拓撲排序](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Topological_Sort/03-DFS_Based_Implementation.md)

<a id="undirected-cycle"></a>
### 011 · 無向圖環偵測與 Graph-as-Tree

來源深度：既有論述延伸

**關鍵論述：** 把圖當樹走訪需要環與身份的條件，不能直接省掉狀態紀錄。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 判斷無向圖是否有環或是否為樹。 |
| 狀態 State | visited、父邊 ID、分量或邊數。 |
| 轉換 Transition | 走訪鄰居時排除進入本節點的那條邊。 |
| 計算順序 Order | DFS/BFS，或按邊做 DSU 合併。 |
| 正確性與終止 Correctness | 平行邊時須排除父邊而非所有父節點邊；連通且 E=V−1 才是樹。 |
| 成本 Cost | O(V+E)；DSU 版另計攤銷成本。 |

來源：

- [圖遍歷優化：當圖是樹時，省略 visited 集合](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Traversal_Strategies/Graph_as_Tree_Traversal.md)
- [LeetCode Tricks and Keywords](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/LeetCode_Tricks_and_Keywords.md)
- [圖與樹的比較：遍歷與實現差異](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Graph_vs_Tree.md)

<a id="bfs"></a>
### 012 · BFS／Level Order／Level in Queue

來源深度：既有論述延伸

**關鍵論述：** 層級可以存在隊列項或控制流程中；兩者不會改變最短路證明。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 計算等成本邊的最少步數或按層遍歷。 |
| 狀態 State | frontier、完整節點身份、已發現標記、距離。 |
| 轉換 Transition | 發現鄰居時入隊並標記，避免重複入隊。 |
| 計算順序 Order | FIFO；可逐層固定 queue 大小，或每項攜帶 level。 |
| 正確性與終止 Correctness | 等成本邊下首次發現的完整狀態具有最短步數。 |
| 成本 Cost | 鄰接表 O(V+E)、O(V) 空間；容器型節點另計表示成本。 |

來源：

- [BFS Level Order 優化：Level in Queue](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/01-Level_Ordering_Level_in_Queue.md)
- [BFS 在 Tree 與 Graph 中的結構比較與觀察](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/02-BFS_Tree_vs_Graph.md)
- [BFS 複雜度分析 (Complexity Analysis)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/03-BFS_Complexity_Analysis.md)
- [心法：容器型頂點的複雜度分析 (Complexity Analysis for Container Vertices)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/04-Container_Vertex_Complexity_Analysis.md)
- [BFS 解題模式：頂點映射 (Vertex Mapping)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/BFS_Vertex_Mapping_Pattern.md)
- [Multi-source BFS 心法與推導框架](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/MultiSource_BFS_Thinking_Framework.md)
- [狀態空間 BFS (State-Space BFS)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/State_Space_BFS.md)
- [廣度優先搜索 (Breadth-First Search, BFS)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/BFS.md)
- [DFS vs BFS 比較](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/DFS_vs_BFS.md)

<a id="multi-bfs"></a>
### 013 · Multi-source BFS／Super Source

來源深度：既有論述延伸

**關鍵論述：** 改變初始化即可合併多次搜尋，共享同一個距離波前。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 取得每個位置到最近來源的距離。 |
| 狀態 State | 所有來源距離為零，共用 frontier 與距離表。 |
| 轉換 Transition | 來源同時向外擴散，以先到者決定最短距離。 |
| 計算順序 Order | 所有零距離來源先入隊，再統一分層。 |
| 正確性與終止 Correctness | 等同加入零成本超級來源；若用一條普通邊表達需校正距離。 |
| 成本 Cost | O(V+E)，避免每個來源各做一次遍歷。 |

來源：

- [Multi-source BFS 心法與推導框架](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/MultiSource_BFS_Thinking_Framework.md)

<a id="state-bfs"></a>
### 014 · State-Space BFS／資源支配剪枝

來源深度：既有論述延伸

**關鍵論述：** 位置相同未必可合併；省略狀態維度需要額外的支配證明。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 求有限資源或歷史條件下的最少步數。 |
| 狀態 State | 位置、剩餘資源、鑰匙集合、前一步顏色等。 |
| 轉換 Transition | 只有滿足條件的狀態才能沿合法邊前進。 |
| 計算順序 Order | 對擴張後的完整狀態分層 BFS。 |
| 正確性與終止 Correctness | 支配剪枝需成本不大且資源不差，且資源單調有利；不能只比資源。 |
| 成本 Cost | O(V′+E′)，V′ 為擴張狀態數，可能是 V·K 或 V·2^k。 |

來源：

- [狀態空間 BFS (State-Space BFS)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/State_Space_BFS.md)

<a id="reverse-reach"></a>
### 015 · Destination-as-Source／反向可達性

來源深度：既有論述延伸

**關鍵論述：** 改變依賴方向，讓大量來源共享一次反向搜尋。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 判定哪些來源能到指定目標集合。 |
| 狀態 State | 反向圖、目標起始集合、各目標群的可達標記。 |
| 轉換 Transition | 把原邊反向，從目標向可能前驅探索。 |
| 計算順序 Order | 單源或多源 DFS/BFS；多個目標群分開保留結果。 |
| 正確性與終止 Correctness | 原圖 u 到 t 可達，等價於反圖 t 到 u 可達。 |
| 成本 Cost | 每目標群 O(V+E)；k 群為 O(k(V+E))。 |

來源：

- [問題轉換心法：目的地反轉為起點 (Destination-as-Source Reachability)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Transformation_Patterns/Destination_as_Source_Reachability.md)

<a id="constraint-reach"></a>
### 016 · Constraint Connectivity

來源深度：既有論述延伸

**關鍵論述：** 把最佳化轉成判定後，才可能安全忽略抵達歷史。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 判定固定門檻下是否存在合法路徑。 |
| 狀態 State | 通過局部邊條件的子圖與 visited。 |
| 轉換 Transition | 僅沿滿足門檻的邊探索。 |
| 計算順序 Order | 任意完整 DFS/BFS；外層可做單調答案二分。 |
| 正確性與終止 Correctness | 每條邊各自受限可轉成固定子圖；總路徑成本限制不能直接如此處理。 |
| 成本 Cost | 單次 O(V+E)；二分 K 個候選 O((V+E)log K)。 |

來源：

- [心法：尋找約束來套用二分搜尋 (Binary Search on Constraint)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Binary_Search/05-Binary_Search_on_Constraint.md)
- [心法：約束性連通問題 (Constraint Connectivity)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Constraint_Connectivity.md)

<a id="zero-one"></a>
### 017 · 0-1 BFS

來源深度：清單／提及延伸

**關鍵論述：** 權重結構允許用更便宜的排程取代一般 heap。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 求邊權僅為 0 或 1 的最短距離。 |
| 狀態 State | dist、deque、尚待鬆弛的節點。 |
| 轉換 Transition | 距離改善時，零權邊放隊首、一權邊放隊尾。 |
| 計算順序 Order | 以 deque 維持非遞減距離處理次序。 |
| 正確性與終止 Correctness | 利用兩種相鄰距離層；不能套用普通 BFS 的首次入隊定案。 |
| 成本 Cost | 標準實作 O(V+E) 時間、O(V+E) 儲存含圖。 |

來源：

- [狀態空間 BFS (State-Space BFS)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/State_Space_BFS.md)
- [LeetCode 高階心法（完整 MD + 一頁式速查表）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/04-Advanced_Problem_Solving_Cheatsheet.md)

<a id="dijkstra"></a>
### 018 · Dijkstra／Lazy Deletion

來源深度：既有論述延伸

**關鍵論述：** heap 保存候選，dist 保存目前事實；兩者角色不能混為一談。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 求非負邊權的單源最短路。 |
| 狀態 State | dist 標籤、優先佇列、可選的 parent。 |
| 轉換 Transition | 鬆弛出邊；改善距離後更新或新增佇列項。 |
| 計算順序 Order | 取最小有效距離；舊標籤出堆時跳過。 |
| 正確性與終止 Correctness | 非負邊保證取出的最小有效標籤不會再被改善。 |
| 成本 Cost | lazy heap O((V+E)log(V+E))；簡單圖常寫 O((V+E)log V)。 |

來源：

- [Dijkstra 演算法：從理論到 C++ 實踐深度解析](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Dijkstra%27s%20Algorithm/01-Dijkstra_Algorithm_Guide.md)
- [Dijkstra 演算法深度剖析](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Dijkstra%27s%20Algorithm/02-Dijkstra_Deep_Dive.md)

<a id="general-dijkstra"></a>
### 019 · 廣義 Dijkstra：Bottleneck／Probability

來源深度：既有論述延伸

**關鍵論述：** 更換成本運算前，必須重新證明標籤可以永久定案。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 最佳化瓶頸值或路徑成功機率。 |
| 狀態 State | 各節點最佳標籤、標籤組合規則與優先順序。 |
| 轉換 Transition | 瓶頸取沿途最大值；機率取沿途乘積。 |
| 計算順序 Order | 瓶頸由小到大；0 到 1 機率由大到小。 |
| 正確性與終止 Correctness | 延伸不能讓較差標籤超越較好標籤，且延伸不改善自身優先級。 |
| 成本 Cost | 條件成立時與 heap Dijkstra 同階；浮點機率另計精度。 |

來源：

- [心法：將 Dijkstra 視為一個通用的貪婪搜尋框架](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Dijkstra%27s%20Algorithm/03-Dijkstra_as_a_General_Search_Framework.md)

<a id="bellman-ford"></a>
### 020 · Bellman-Ford／負環偵測

來源深度：既有論述延伸

**關鍵論述：** 收斂型更新與嚴格分層 DP 意義不同，即使看起來都有輪數。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 處理可能有負邊的單源最短路。 |
| 狀態 State | 距離標籤；邊數受限版本另保存前一輪。 |
| 轉換 Transition | 反覆鬆弛全部邊；多一輪仍改善則檢查可達負環。 |
| 計算順序 Order | 最多 V−1 輪後檢測；原地版本允許當輪傳播多條邊。 |
| 正確性與終止 Correctness | 無可達負環的最短簡單路徑最多 V−1 邊；指定最多 k 邊須隔離輪次。 |
| 成本 Cost | 標準 O(VE) 時間、O(V) 額外空間。 |

來源：

- [Bellman-Ford 的動態規劃基礎](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/Bellman-Ford/01-DP_Foundations_of_Bellman-Ford.md)
- [標準 Bellman-Ford 最短路徑演算法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/Bellman-Ford/02-Standard_Bellman-Ford_Algorithm.md)
- [Bellman-Ford：演算法限制與負權重環檢測](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/Bellman-Ford/04-Negative_Cycle_Detection.md)

<a id="spfa"></a>
### 021 · SPFA

來源深度：既有論述延伸

**關鍵論述：** 這裡的 queue 是待更新工作清單，不提供 BFS 的首次抵達最短保證。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 減少 Bellman-Ford 中無效的鬆弛工作。 |
| 狀態 State | dist、待處理 queue、inQueue 與負環檢測資訊。 |
| 轉換 Transition | 只有標籤改善的節點才重新排入工作隊列。 |
| 計算順序 Order | 依改善事件排程；允許同節點多次回到 queue。 |
| 正確性與終止 Correctness | queue 清空代表沒有可傳播的改善；負環時需可靠的停止判準。 |
| 成本 Cost | 最壞仍 O(VE)，不能保證平均線性；額外空間 O(V)。 |

來源：

- [SPFA (Shortest Path Faster Algorithm)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/Bellman-Ford/03-SPFA_Optimization.md)

<a id="floyd-warshall"></a>
### 022 · Floyd-Warshall

來源深度：既有論述延伸

**關鍵論述：** 控制狀態是「允許哪些中繼點」，因此三層迴圈不能任意互換。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 取得所有點對的最短距離。 |
| 狀態 State | 點對距離及目前允許的中繼點集合。 |
| 轉換 Transition | 比較原路徑與經過新中繼點的路徑。 |
| 計算順序 Order | 中繼點 k 為外層，再枚舉起終點。 |
| 正確性與終止 Correctness | 每輪僅擴張允許的中繼集合；負環可由負對角線辨識。 |
| 成本 Cost | O(V³) 時間、O(V²) 空間。 |

來源：

- [Matrix DP 解題心法：從網格到圖論](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Problem_Types/Matrix_DP.md)
- [📘 DSA Design Pattern Roadmap](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/01-Interview_Timing_Framework.md)

<a id="topological"></a>
### 023 · Topological Sort／Kahn／DFS Postorder

來源深度：既有論述延伸

**關鍵論述：** 拓撲序為求值提供證明，不只是換一種走訪順序。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 產生先依賴後使用的順序，或檢查 DAG。 |
| 狀態 State | 未完成入度與 ready queue；或三色 DFS 與完成序列。 |
| 轉換 Transition | 移除 ready 節點的出邊；DFS 完成後記錄再反轉。 |
| 計算順序 Order | Kahn 只取零入度；DFS 使用反向完成序。 |
| 正確性與終止 Correctness | 每次輸出者無尚未處理的前置依賴；未能輸出全部表示有環。 |
| 成本 Cost | O(V+E)；要求字典序使用 heap，加入 O(Vlog V)。 |

來源：

- [拓撲排序：核心概念與應用](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Topological_Sort/01-Core_Concepts_and_Applications.md)
- [Kahn 演算法 (基於 BFS 的拓撲排序)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Topological_Sort/02-Kahn_Algorithm_BFS.md)
- [基於 DFS 的拓撲排序](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Topological_Sort/03-DFS_Based_Implementation.md)

<a id="leaf-peeling"></a>
### 024 · Leaf Peeling／樹中心

來源深度：清單／提及延伸

**關鍵論述：** 借用 Kahn 的消除機制，但依據的是樹的幾何結構。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 找樹的最小高度根或逐層剝除外圍。 |
| 狀態 State | 剩餘度數、當層葉子、剩餘節點數。 |
| 轉換 Transition | 整層移除葉子，更新下一層。 |
| 計算順序 Order | 同步剝葉直到剩一或兩點。 |
| 正確性與終止 Correctness | 對無向樹，剝葉保留中心；中心與重心 centroid 是不同概念。 |
| 成本 Cost | O(V+E) 時間、O(V) 空間。 |

來源：

- [Kahn 演算法的變體與應用](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Topological_Sort/04-Kahn_Algorithm_Variants.md)
- [LeetCode Tricks and Keywords](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/LeetCode_Tricks_and_Keywords.md)

<a id="hierholzer"></a>
### 025 · Hierholzer／Eulerian Path

來源深度：既有論述延伸

**關鍵論述：** 已使用的是邊；後序完成順序把局部迴路接成完整答案。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 構造每條邊恰好使用一次的路徑或迴路。 |
| 狀態 State | 未使用邊、目前行走 stack、完成序列。 |
| 轉換 Transition | 消耗一條邊前進，無剩餘出邊時回收節點。 |
| 計算順序 Order | 在退棧時組合，最後反轉。 |
| 正確性與終止 Correctness | 需滿足歐拉度數與連通條件；追蹤邊身份，容許重訪節點。 |
| 成本 Cost | 邊取用 O(1) 時 O(V+E)；字典序排序需額外 O(Elog E)。 |

來源：

- [Hierholzer's Algorithm 核心概念](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/Hierholzers/01-Hierholzers_Core_Concepts.md)
- [Node-Based vs Edge-Based Implementation](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/Hierholzers/02-Node_vs_Edge_Based_Implementation.md)

<a id="de-bruijn"></a>
### 026 · De Bruijn Graph／Sequence

來源深度：既有論述延伸

**關鍵論述：** 改變「字串是點還是邊」的建模，會直接改變所需搜尋任務。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 用最短循環覆蓋所有固定長度字串。 |
| 狀態 State | 長度 k−1 的字串作節點，長度 k 字串作邊。 |
| 轉換 Transition | 移除首字元並附加一個字元形成下一節點。 |
| 計算順序 Order | 以 Hierholzer 消耗所有邊，輸出序列。 |
| 正確性與終止 Correctness | 每條邊唯一對應一個長度 k 字串，Euler circuit 保證完整覆蓋。 |
| 成本 Cost | 字母表 σ 時有 σ^k 條邊；輸出本身即 Ω(σ^k)。 |

來源：

- [De Bruijn Graph 與 De Bruijn Sequence](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Advanced/De_Bruijn_Graph.md)


<a id="chapter-3"></a>
## 枚舉與分治

<a id="backtracking"></a>
### 027 · Backtracking／候選建模

來源深度：既有論述延伸

**關鍵論述：** 回溯的還原是語義要求；使用獨立副本時，不一定要顯式撤銷。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 枚舉合法選擇、構造答案或建立暴力基準。 |
| 狀態 State | 已定前綴、待定候選、限制摘要、輸出緩衝。 |
| 轉換 Transition | 選擇、探索、恢復，或複製分支狀態。 |
| 計算順序 Order | 依決策樹做 DFS；解的收集與狀態管理分開。 |
| 正確性與終止 Correctness | 分支覆蓋所有合法選擇，且分支之間不污染；不可行才剪枝。 |
| 成本 Cost | 搜尋節點總工作加輸出量；子集可有 2^n 葉、排列 n! 葉。 |

來源：

- [心法：回溯算法的通用模板與模式](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/01-Backtracking_Templates_and_Patterns.md)
- [心法：系統性建構回溯演算法的通用框架](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/02-Backtracking_Problem_Solving_Framework.md)
- [心法：以「已定 vs. 待定」視角進行候選者建模](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/03-Backtracking_Candidate_Modeling.md)
- [回溯法：狀態設計與解構建 (State and Solution Design)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/04-State_and_Solution_Design.md)
- [回溯法的數學化視角：狀態空間樹與 N 元組](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/05-State_Space_Tree_and_N_Tuple_Representation.md)
- [DFS、Backtracking 與 Pruning 的關係深度解析](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/06-DFS_vs_Backtracking_Pruning.md)

<a id="permutation-enumeration"></a>
### 028 · Permutation／Combination／Subset Enumeration

來源深度：清單／提及延伸

**關鍵論述：** 先定義答案的身份，才能決定哪些分支算重複。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 列舉排列、組合與子集。 |
| 狀態 State | 排列保存已用元素；組合保存候選起點；子集保存選或不選的進度。 |
| 轉換 Transition | 排列選未使用者；組合向較後索引延伸；子集分成取與不取。 |
| 計算順序 Order | 按固定決策次序展開；bitmask 可直接枚舉子集。 |
| 正確性與終止 Correctness | 不同問題的「解相同」定義不同；索引順序可消除組合排列重複。 |
| 成本 Cost | 含輸出時子集 O(n2^n)、全排列 O(n·n!)；組合至少 Ω(k·C(n,k))。 |

來源：

- [回溯法的數學化視角：狀態空間樹與 N 元組](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/05-State_Space_Tree_and_N_Tuple_Representation.md)
- [心法：以 std::vector 為核心的回溯策略：原地建構 vs. 輔助空間](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/Backtracking_on_cpp_vector_Playbook.md)

<a id="dedup"></a>
### 029 · Duplicate Removal／對稱去重

來源深度：既有論述延伸

**關鍵論述：** 去重省略的是相同答案的多次生成，不是所有重複數值。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 避免不同決策歷史輸出相同答案。 |
| 狀態 State | 排序候選、同層已選值或全域答案簽名。 |
| 轉換 Transition | 同一決策層只探索一個等價代表。 |
| 計算順序 Order | 通常先排序再 DFS；同層與跨層去重規則分開。 |
| 正確性與終止 Correctness | 只刪除等價分支；不能把同值的多個可用元素全部抹掉。 |
| 成本 Cost | 額外排序 O(nlog n)；最壞輸出仍可能指數級。 |

來源：

- [去重剪枝設計心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/Duplicate_Removal_Pruning_Design.md)

<a id="swap-state"></a>
### 030 · Swap 作為原地狀態管理

來源深度：既有論述延伸

**關鍵論述：** 一個交換同時完成選取、移除候選與保存部分答案。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在輸入中管理已定與待定集合。 |
| 狀態 State | 分界索引、分界前固定排列、分界後候選。 |
| 轉換 Transition | 把候選交換到分界，再前進；返回時交換還原。 |
| 計算順序 Order | DFS；每層處理一個固定位置。 |
| 正確性與終止 Correctness | 返回時陣列必須恢復成進入該分支前的排列。 |
| 成本 Cost | 每次交換 O(1)，遞迴 O(n) 空間；總時間仍受枚舉量限制。 |

來源：

- [心法：以 std::vector 為核心的回溯策略：原地建構 vs. 輔助空間](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/Backtracking_on_cpp_vector_Playbook.md)
- [Swap 作為通用 Backtracking 狀態操作心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/Swap_as_In_Place_State_Management.md)

<a id="branch-bound"></a>
### 031 · Pruning／Branch and Bound

來源深度：清單／提及延伸

**關鍵論述：** 剪枝是一項證明：這條分支無法提供目標所需的新資訊。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 略過不可能可行或不可能改善答案的分支。 |
| 狀態 State | 部分解、目前最佳值、可行性檢查與樂觀界限。 |
| 轉換 Transition | 不合法即停止；最佳可能結果仍不夠好也停止。 |
| 計算順序 Order | 可先探索看似有利分支，以較早收緊界限。 |
| 正確性與終止 Correctness | 界限必須樂觀且方向正確；列舉全部最優解時等號不可隨意剪掉。 |
| 成本 Cost | 最壞仍等同枚舉；實際節省量取決於界限品質。 |

來源：

- [DFS、Backtracking 與 Pruning 的關係深度解析](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/06-DFS_vs_Backtracking_Pruning.md)
- [LeetCode 高階心法（完整 MD + 一頁式速查表）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/04-Advanced_Problem_Solving_Cheatsheet.md)

<a id="divide-conquer"></a>
### 032 · Divide & Conquer：Divide／Combine-centric

來源深度：既有論述延伸

**關鍵論述：** 重點是子問題契約與跨界資訊，而非看見遞迴就叫分治。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 把工作拆成可解的子問題再重組。 |
| 狀態 State | 區間、子集合或子樹；明確的回傳摘要或輸出位置。 |
| 轉換 Transition | 分割、求解、合併；工作可主要發生在分割或合併階段。 |
| 計算順序 Order | 依依賴遞迴；開閉區間與基底一致。 |
| 正確性與終止 Correctness | 子問題覆盖原問題，合併包含跨界貢獻；每次分割確實縮小。 |
| 成本 Cost | 用 T(n)=ΣT(nᵢ)+分割合併成本；失衡可能退化 O(n²)。 |

來源：

- [Divide and Conquer 設計策略心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/01_Divide_and_Conquer_Design_Strategy.md)
- [Divide and Conquer vs Dynamic Programming 比較分析](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/02_Divide_and_Conquer_vs_Dynamic_Programming.md)
- [Interval Design in Divide and Conquer 區間設計心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/03_Interval_Design_in_Divide_and_Conquer.md)
- [分治結果累積策略](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/05_Conquer_Strategy_Comparison.md)

<a id="bottom-up-dc"></a>
### 033 · Bottom-up Divide & Conquer

來源深度：既有論述延伸

**關鍵論述：** 求值順序可以由子問題規模直接產生。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 用迭代完成逐層合併。 |
| 狀態 State | 目前區塊寬度、相鄰區塊邊界、工作緩衝。 |
| 轉換 Transition | 把同規模小區塊合成大區塊，再放大寬度。 |
| 計算順序 Order | 由小到大，依層處理。 |
| 正確性與終止 Correctness | 每一層開始時，所有較小區塊已滿足輸出契約。 |
| 成本 Cost | 合併排序例 O(nlog n) 時間、O(n) 緩衝；省去呼叫 stack。 |

來源：

- [Bottom-Up Divide and Conquer 解題策略](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/04_Bottom_Up_Divide_and_Conquer.md)

<a id="external-state"></a>
### 034 · External State／雙軌遍歷

來源深度：既有論述延伸

**關鍵論述：** 形狀進度和資料進度是兩份狀態；共享游標讓排程變成正確性的一部分。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 同步控制輸出形狀與資料消耗次序。 |
| 狀態 State | 結構遞迴區間、共享資料游標、累計結果。 |
| 轉換 Transition | 遞迴控制形狀，在指定時機消耗一筆來源或寫入輸出。 |
| 計算順序 Order | 必須固定前序、中序或後序的消耗時機。 |
| 正確性與終止 Correctness | 每筆資料恰好消耗一次，來源次序與輸出位置對應。 |
| 成本 Cost | 常見建樹 O(n) 時間、O(h) 控制空間。 |

來源：

- [分治結果累積策略](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/05_Conquer_Strategy_Comparison.md)
- [External State 遍歷順序心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/06_External_State_Traversal_Order.md)

<a id="merge-count"></a>
### 035 · Merge Sort Variants／跨區間計數

來源深度：既有論述延伸

**關鍵論述：** 排序是子問題提供給父問題的摘要能力，讓批次計數可行。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 計算逆序對、跨半部條件配對與範圍和數量。 |
| 狀態 State | 左右有序子序列、原索引、計數摘要。 |
| 轉換 Transition | 計算跨左右的合法配對，再合併排序結果。 |
| 計算順序 Order | 子區間先完成，跨界掃描使用單調指標。 |
| 正確性與終止 Correctness | 每對元素只在第一次分居左右的合併層計數。 |
| 成本 Cost | 跨界計數線性時 O(nlog n)、O(n) 空間；條件運算要防溢位。 |

來源：

- [Merge Sort Variants Pattern (Combine-centric D&C) 心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/07_Merge_Sort_Variants_Pattern.md)
- [🎯 Divide and Conquer - Hard 題終極練習路徑（按目標題分類）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Divide_and_Conquer_Hard_Problem_Playbook.md)

<a id="decision-tree"></a>
### 036 · Decision Tree 學習與推論

來源深度：既有論述延伸

**關鍵論述：** 這裡框架描述學習程序；泛化品質另以驗證資料衡量，不能當作算法最優性。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 由資料學習分類規則並分類新樣本。 |
| 狀態 State | 節點樣本集合、候選特徵、深度、類別統計。 |
| 轉換 Transition | 選 Gini／Entropy 改善最大的切分，遞迴建子樹；葉子保存預測。 |
| 計算順序 Order | 訓練逐節點切分；推論沿單一路徑。 |
| 正確性與終止 Correctness | 資料分區與停止條件需成立；局部 impurity 改善不保證全局最優樹。 |
| 成本 Cost | 訓練為各節點切分成本總和；推論 O(h)，評量 n 筆 O(nh)。 |

來源：

- [Decision Tree 定義](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/Decision_Tree/01-Definition.md)
- [Decision Tree 實作](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/Decision_Tree/02-Implementation.md)
- [Decision Tree 設計決策：Splitting Criterion](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/Decision_Tree/03-Splitting_Criterion.md)
- [Decision Tree 評量](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/Decision_Tree/04-Evaluation.md)


<a id="chapter-4"></a>
## 動態規劃

<a id="dp"></a>
### 037 · Dynamic Programming／Memoization／Tabulation

來源深度：既有論述延伸

**關鍵論述：** DP 共享的是後續計算；計數時不同到達方式仍需累加貢獻。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 求可行性、計數或最佳值，重用相同子問題。 |
| 狀態 State | 子問題 key 與 value 分開；key 含影響未來的一切條件。 |
| 轉換 Transition | 枚舉合法選擇，以 OR、加總或 min/max 組合子結果。 |
| 計算順序 Order | Top-down 按需求值；Tabulation 依依賴順序求值。 |
| 正確性與終止 Correctness | 轉移完整且不重複錯算；循環依賴不能只靠加 cache 解決。 |
| 成本 Cost | O(狀態數×每狀態轉移成本)；更精確為全部實際轉移與表示成本之和。 |

來源：

- [DP 問題形式：如何識別動態規劃問題](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Fundamentals/01-Problem_Forms.md)
- [動態規劃的黃金路徑：從回溯到最佳解的系統化推導](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Fundamentals/02-Problem_Solving_Framework.md)
- [從 Top-Down 到 Bottom-Up：DP 轉換的系統化指南](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Fundamentals/03-TopDown_to_BottomUp.md)
- [DP 遞迴關係的三大設計模式](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Fundamentals/04-Recurrence_Design_Patterns.md)
- [DP 的圖論統一視角：將動態規劃視為圖遍歷](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Fundamentals/Concept_DP_as_Graph_Traversal.md)
- [DP 邊界處理的設計模式與心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Implementation/Boundary_Condition_Handling.md)
- [DP 快取策略：Memoization 的實現與權衡](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Implementation/Caching_Strategies.md)
- [DP 常見陷阱與修正策略](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Implementation/Common_Pitfalls.md)
- [DP 狀態設計的兩大基石](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/State_Design/01-Essentials.md)
- [DP 狀態設計心法：從「解的性質」決定「狀態維度」](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/State_Design/02-From_Solution_Properties.md)
- [🧩 Algorithm Design Pattern – 思考三連問](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/03-State_Transition_Traversal.md)

<a id="rolling-dp"></a>
### 038 · Rolling Array／Space-Optimized DP

來源深度：既有論述延伸

**關鍵論述：** 這是縮短資料生命週期，子問題總數不一定減少。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 降低 DP 保存中間值的記憶體。 |
| 狀態 State | 仍有未來使用者的幾層資料，及當輪必要暫存。 |
| 轉換 Transition | 讀取舊值後，覆蓋已完成用途的欄位。 |
| 計算順序 Order | 正序或倒序由讀取版本决定。 |
| 正確性與終止 Correctness | 覆寫前所有依賴都已讀完；重建答案可能仍需前驅資訊。 |
| 成本 Cost | 時間通常不變；m×n 表可在依賴允許時降為 O(n)。 |

來源：

- [從 Top-Down 到 Bottom-Up：DP 轉換的系統化指南](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Fundamentals/03-TopDown_to_BottomUp.md)
- [狀態壓縮技巧](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/State_Design/04-State_Reduction.md)

<a id="state-reduction"></a>
### 039 · 維度吸收／State Decomposition

來源深度：既有論述延伸

**關鍵論述：** 狀態縮減需要保留可行性與目標，不能只因兩個數相關就刪掉一個。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 減少狀態維度或拆開可分離的約束。 |
| 狀態 State | 足以表達剩餘限制的摘要，或分方向的獨立子狀態。 |
| 轉換 Transition | 把被吸收維度納入 value，或分別求解再重組。 |
| 計算順序 Order | 依各子狀態依賴安排，可雙向掃描。 |
| 正確性與終止 Correctness | 須證明摘要充分與重組等價；AND 不普遍等於 max、OR 不普遍等於 min。 |
| 成本 Cost | 依可分離性決定；多維乘積不會自動降成維度之和。 |

來源：

- [雙向約束分解 / Bidirectional Constraint Decomposition](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Bidirectional_Constraint_Decomposition.md)
- [狀態空間分解 / State Space Decomposition](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/State_Decomposition.md)
- [狀態壓縮技巧](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/State_Design/04-State_Reduction.md)

<a id="value-dp"></a>
### 040 · Value-Space DP／Group by Value

來源深度：既有論述延伸

**關鍵論述：** 換掉索引的語義，可以把複雜位置問題變成值域上的簡單結構。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 處理與數值關係相關、與原位置無關的選擇。 |
| 狀態 State | 值域索引、同值總收益、值之間的衝突關係。 |
| 轉換 Transition | 先按值分組，再依值域上的依賴遞推。 |
| 計算順序 Order | 按數值排序；離散化後仍保留原值差距。 |
| 正確性與終止 Correctness | 同值元素須能等價合併；收益為負或額外限制時不可假設全部取。 |
| 成本 Cost | 稠密值域 O(n+U)；稀疏排序 O(nlog n)，依實際轉移另計。 |

來源：

- [心法：從索引到值域 — DP 狀態設計的躍遷](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/State_Design/03-On_Value_Space.md)

<a id="local-global"></a>
### 041 · 局部狀態與全域答案

來源深度：既有論述延伸

**關鍵論述：** 「到目前為止最好」與「必須在這裡結束」是不同的子問題。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 同時保存可延伸的局部結果與整體最佳答案。 |
| 狀態 State | 特定結尾／邊界的局部值，另有全域摘要。 |
| 轉換 Transition | 先更新受限制的局部值，再納入全域候選。 |
| 計算順序 Order | 依局部依賴求值；全域只在局部完整時更新。 |
| 正確性與終止 Correctness | 回傳給父層的可延伸結果，不能混入不再可延伸的全局答案。 |
| 成本 Cost | 取決於局部轉移；全域追蹤通常僅 O(1) 每步。 |

來源：

- [Kadane's Pattern DP](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/Kadanes_Pattern_DP.md)
- [局部狀態與全域追蹤設計心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/State_Design/05-Local_State_vs_Global_Optimum.md)
- [🎯 Kadane's Pattern DP - 練習路徑](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Kadanes_Pattern_DP_Playbook.md)

<a id="kadane"></a>
### 042 · Kadane／Ending-at-i Pattern

來源深度：既有論述延伸

**關鍵論述：** Kadane 的線性性來自常數大小轉移，不是所有 ending-at-i DP 都線性。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 求連續片段的最佳值或利用結尾狀態導航。 |
| 狀態 State | 當前結尾的最佳摘要，另存全域最佳。 |
| 轉換 Transition | 比較延伸舊片段與從當前重開；特殊模式依前段長度找接點。 |
| 計算順序 Order | 由左向右，先完成依賴的前段。 |
| 正確性與終止 Correctness | 任何以當前結尾的非空片段，要麼新開、要麼延伸；全負數基底要正確。 |
| 成本 Cost | 標準最大和 O(n) 時間、O(1) 空間；延伸模式依查詢成本決定。 |

來源：

- [Kadane's Algorithm 心法 / Running State with Conditional Reset](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/Kadane_Algorithm.md)
- [Kadane's Pattern DP](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/Kadanes_Pattern_DP.md)
- [032. Longest Valid Parentheses](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Super_Hard/032_Longest_Valid_Parentheses.md)
- [🎯 Kadane's Pattern DP - 練習路徑](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Kadanes_Pattern_DP_Playbook.md)

<a id="max-product"></a>
### 043 · Maximum Product／雙極值摘要

來源深度：清單／提及延伸

**關鍵論述：** 支配關係取決於未來運算；乘法有負數時，一個最大值不足以摘要歷史。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 保存可被正負乘數翻轉的連續乘積候選。 |
| 狀態 State | 以當前結尾的最大與最小乘積、全域最佳。 |
| 轉換 Transition | 從新開或延伸兩個舊極值產生下一對極值。 |
| 計算順序 Order | 按元素順序，必須同時基於更新前的極值。 |
| 正確性與終止 Correctness | 負數會反轉大小關係；只留最大值會丟失未來最佳候選。 |
| 成本 Cost | O(n) 時間、O(1) 額外空間；乘積需可表示。 |

來源：

- [🎯 Kadane's Pattern DP - 練習路徑](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Kadanes_Pattern_DP_Playbook.md)

<a id="sequence-dp"></a>
### 044 · 1D Sequence DP／固定與動態範圍依賴

來源深度：既有論述延伸

**關鍵論述：** 表格是一維，只表示狀態數量；轉移可能仍是二次成本。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 沿序列求解選擇、切分或鏈接問題。 |
| 狀態 State | 前綴長度、結尾索引或前一選擇類別。 |
| 轉換 Transition | 由固定數量前驅或一段合法歷史聚合。 |
| 計算順序 Order | 按前驅先於後繼的索引順序。 |
| 正確性與終止 Correctness | 固定窗口與全歷史依賴不同；缺少合法前驅會漏解。 |
| 成本 Cost | 常數前驅 O(n)；每項掃描全部歷史 O(n²)。 |

來源：

- [DP 遞迴關係的三大設計模式](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Fundamentals/04-Recurrence_Design_Patterns.md)
- [演算法心法：子序列問題攻略 (Subsequence Problem-Solving Strategies)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/Subsequence_Problem_Solving_Strategies.md)

<a id="state-machine-dp"></a>
### 045 · State Machine DP／Stock／Profile DP

來源深度：既有論述延伸

**關鍵論述：** 狀態機把耦合的多種局部結果明確列出，避免用一個最佳值抹掉必要差異。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 處理持有狀態、交易限制或鋪磚邊界等階段決策。 |
| 狀態 State | 時間／位置、模式、剩餘額度或未填滿邊界。 |
| 轉換 Transition | 在模式之間做合法轉移，附加收益或計數。 |
| 計算順序 Order | 按時間或掃描前沿前進；版本更新必須符合題目時序。 |
| 正確性與終止 Correctness | 模式需含影響未來的限制，例如冷卻與未完成的邊界。 |
| 成本 Cost | O(n×模式數×每模式分支)；模式數未必常數。 |

來源：

- [DP 遞迴關係的三大設計模式](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Fundamentals/04-Recurrence_Design_Patterns.md)
- [🎯 Archetype Problems (原型問題)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Archetype_Problems.md)
- [刷題日誌](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Practice_Log.md)

<a id="counting-dp"></a>
### 046 · Counting DP／排列與組合計數

來源深度：既有論述延伸

**關鍵論述：** 換聚合運算不夠，還要確認不同歷史在答案定義下是否算不同解。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 計算合法構造數量。 |
| 狀態 State | 剩餘量、處理到的候選索引，或足以區分解的條件。 |
| 轉換 Transition | 對互斥分支加總，獨立組合部分時相乘。 |
| 計算順序 Order | 組合固定候選順序；排列需保留不同選擇順序的貢獻。 |
| 正確性與終止 Correctness | 分解必須不重不漏；空構造通常是一種方式而非零種。 |
| 成本 Cost | O(S×D)，模數或大整數運算另計。 |

來源：

- [Counting DP 心法手冊：從可達性到路徑計數](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Problem_Types/Counting_DP.md)
- [DP 狀態設計心法：從「解的性質」決定「狀態維度」](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/State_Design/02-From_Solution_Properties.md)

<a id="knapsack01"></a>
### 047 · 0/1 Knapsack／Subset Sum

來源深度：既有論述延伸

**關鍵論述：** 容量是數值而非輸入位數，所以 O(nW) 不代表解掉 NP-complete 的多項式困難。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 每個物品最多一次，求容量下的可行性或最佳收益。 |
| 狀態 State | 物品前綴與容量；value 為可行性、收益或方法數。 |
| 轉換 Transition | 不取物品，或由扣除其費用的上一層轉入。 |
| 計算順序 Order | 二維按物品；一維容量倒序以避免同物品重用。 |
| 正確性與終止 Correctness | 兩種選擇覆蓋全部子集；倒序保存上一物品層語義。 |
| 成本 Cost | 非負整數容量 W 下 O(nW)、滾動空間 O(W)；屬偽多項式。 |

來源：

- [Subset Sum Problem 與 NP-Completeness](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Subset_Sum/01-Subset_Sum_and_NP_Completeness.md)
- [Subset Sum Problem 實作指南](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Subset_Sum/02-Implementation_Guide.md)
- [🎒 0/1 Knapsack 變形題整理](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Knapsack_Variations_Playbook.md)

<a id="unbounded-knapsack"></a>
### 048 · Unbounded Knapsack／Coin Change

來源深度：清單／提及延伸

**關鍵論述：** 同一個容量表，改變讀取版本與排程，就改變了允許的決策。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 允許同一物品重複使用的容量或金額問題。 |
| 狀態 State | 金額及必要的物品範圍，value 依目標選擇。 |
| 轉換 Transition | 使用物品後仍允許再次選它。 |
| 計算順序 Order | 一維正向容量可讀當層；外層選物品或金額決定組合／排列語義。 |
| 正確性與終止 Correctness | 必須有正費用或其他進展條件，避免無限選取。 |
| 成本 Cost | n 種物品、容量 W 常見 O(nW)、O(W) 空間。 |

來源：

- [Counting DP 心法手冊：從可達性到路徑計數](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Problem_Types/Counting_DP.md)
- [DP 狀態設計心法：從「解的性質」決定「狀態維度」](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/State_Design/02-From_Solution_Properties.md)

<a id="multi-knapsack"></a>
### 049 · Multi-dimensional Knapsack／差值狀態

來源深度：清單／提及延伸

**關鍵論述：** 額外維度來自真實耦合；差值是一種重新表示，不是無條件消除資訊。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 處理多種資源限制或兩組平衡。 |
| 狀態 State | 物品進度、各資源餘額，或兩組差值加最佳共同量。 |
| 轉換 Transition | 分配到不同組、取或不取，更新所有受影響限制。 |
| 計算順序 Order | 物品逐層；原地版本各資源方向都需檢查。 |
| 正確性與終止 Correctness | 被合併的歷史須有相同未來限制；差值相同時只保留最有利值需支配證明。 |
| 成本 Cost | 狀態數常為 n·Π容量，差值域亦可能很大。 |

來源：

- [多維動態規劃心法手冊](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Problem_Types/Multi_Dimensional_DP.md)
- [🎒 0/1 Knapsack 變形題整理](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Knapsack_Variations_Playbook.md)

<a id="matrix-dp"></a>
### 050 · 2D／Matrix／Grid DP

來源深度：既有論述延伸

**關鍵論述：** 二維輸入只是表示；DP 能成立靠的是依賴結構。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 聚合網格或兩序列上的局部依賴。 |
| 狀態 State | 格點或兩個前綴索引，另含題目所需條件。 |
| 轉換 Transition | 由上、左、對角等合法前驅聚合。 |
| 計算順序 Order | 按行列、對角或值排序，使前驅已完成。 |
| 正確性與終止 Correctness | 矩陣形狀不保證無環；可四向移動時要重新判定依賴。 |
| 成本 Cost | R×C 狀態且常數轉移時 O(RC)；空間可視依賴滾動。 |

來源：

- [Matrix DP 解題心法：從網格到圖論](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Problem_Types/Matrix_DP.md)

<a id="lcs-edit"></a>
### 051 · LCS／Edit Distance／雙序列 DP

來源深度：清單／提及延伸

**關鍵論述：** 兩條序列的進度不能合併成單一索引，因為後續可配對內容不同。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 比較或轉換兩個序列。 |
| 狀態 State | 兩個前綴長度，value 為最佳配對長度或轉換成本。 |
| 轉換 Transition | 依相等配對、略過、插入、刪除、替換等合法選擇轉移。 |
| 計算順序 Order | 先短前綴再長前綴；一維化需保存舊對角值。 |
| 正確性與終止 Correctness | 所有最後一步被完整分類；空前綴基底代表實際操作成本。 |
| 成本 Cost | 長度 n,m 時常見 O(nm) 時間，O(nm) 或滾動 O(min(n,m)) 空間。 |

來源：

- [LeetCode Tricks and Keywords](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/LeetCode_Tricks_and_Keywords.md)
- [演算法心法：子序列問題攻略 (Subsequence Problem-Solving Strategies)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/Subsequence_Problem_Solving_Strategies.md)
- [📘 DSA Design Pattern Roadmap](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/01-Interview_Timing_Framework.md)

<a id="interval-dp"></a>
### 052 · Interval DP／Palindrome DP

來源深度：清單／提及延伸

**關鍵論述：** 把最後一步固定，常能讓原本互相干擾的左右部分變成獨立子問題。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 求区間拆分、合併、回文與邊界相依問題。 |
| 狀態 State | 左右端點及合併所需附加條件。 |
| 轉換 Transition | 枚舉切點或最後操作，組合更短區間。 |
| 計算順序 Order | 按區間長度遞增或遞迴求依賴。 |
| 正確性與終止 Correctness | 切點與最後操作的分類需覆盖全部答案；邊界值須不受未記錄歷史影響。 |
| 成本 Cost | O(n²) 狀態；常數轉移 O(n²)，枚舉切點常 O(n³)。 |

來源：

- [🎯 Kadane's Pattern DP - 練習路徑](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Kadanes_Pattern_DP_Playbook.md)
- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)

<a id="tree-dp"></a>
### 053 · Tree DP／Subtree Aggregation

來源深度：既有論述延伸

**關鍵論述：** 資訊向上流動與 Top-down 呼叫是兩件事，不應混用命名。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 聚合子樹答案並處理節點選擇。 |
| 狀態 State | 節點、父方向條件、可向上回傳的摘要與全域候選。 |
| 轉換 Transition | 收集子樹結果，再計算節點結果與跨子樹候選。 |
| 計算順序 Order | 後序為主；父條件可先向下傳遞。 |
| 正確性與終止 Correctness | 回傳值須可被父節點接續；整體答案可能在任意節點形成。 |
| 成本 Cost | 固定狀態、線性合併時 O(n)；子樹背包等合併可能更高。 |

來源：

- [樹狀遞迴設計心法：從基本結構到優雅解](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Recursive_Design_Pattern_Pruning_and_Aggregation.md)
- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)

<a id="rerooting"></a>
### 054 · Rerooting DP

來源深度：清單／提及延伸

**關鍵論述：** 把「換根重算」改為「共享邊兩側摘要」，避免每個根各掃一次樹。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 求每個節點作根時的結果。 |
| 狀態 State | 每條有向邊兩側的摘要與各節點聚合。 |
| 轉換 Transition | 先求子樹貢獻，再把父方向貢獻傳回孩子。 |
| 計算順序 Order | 一次後序、一次前序；排除某孩子可用前後綴聚合。 |
| 正確性與終止 Correctness | 向孩子傳遞時不能把該孩子自身貢獻重複帶入。 |
| 成本 Cost | 可常數組合每條邊摘要時 O(n)；另計狀態大小。 |

來源：

- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)

<a id="bitmask-dp"></a>
### 055 · Bitmask DP／Subset DP

來源深度：清單／提及延伸

**關鍵論述：** bitmask 降低表示成本，2^n 種不同集合仍然存在。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 處理已選集合會影響未來的排列與分配。 |
| 狀態 State | 集合 mask，必要時另有最後位置或餘額。 |
| 轉換 Transition | 加入未選元素，或把集合拆成子集組合。 |
| 計算順序 Order | 按集合大小或遞迴依賴求值。 |
| 正確性與終止 Correctness | mask 只保留集合；若順序或終點影响未來，必須另存。 |
| 成本 Cost | 常見 O(n2^n) 或 O(n²2^n)；枚舉所有子集分割可達 O(3^n)。 |

來源：

- [進階技巧：使用位元遮罩進行狀態壓縮](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Bit_Manipulation/03-State_Compression.md)
- [狀態壓縮技巧](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/State_Design/04-State_Reduction.md)
- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)

<a id="digit-dp"></a>
### 056 · Digit DP

來源深度：清單／提及延伸

**關鍵論述：** 巨大值域被轉成短位數序列；只保留上界對未來的影響。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 計算數值上界內滿足位數限制的數。 |
| 狀態 State | 位數位置、tight、leading-zero 與限制摘要。 |
| 轉換 Transition | 枚舉本位合法數字，更新是否仍貼住上界。 |
| 計算順序 Order | 由高位到低位，記憶化同等後續狀態。 |
| 正確性與終止 Correctness | 前導零是否算有效數位、零本身是否納入必須明確。 |
| 成本 Cost | d 位、b 進位、K 種限制摘要，常見 O(d·b·K)。 |

來源：

- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)

<a id="probability-dp"></a>
### 057 · Probability／Expectation DP

來源深度：清單／提及延伸

**關鍵論述：** 狀態保存的是對未來分布足夠的資訊，聚合改成加權運算。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 求隨機過程的機率或期望。 |
| 狀態 State | 位置、剩餘輪數或其他足夠描述分布的狀態。 |
| 轉換 Transition | 以轉移機率加權子結果；期望另加入當步成本。 |
| 計算順序 Order | 無環依賴可 DP；有循環可能需解方程或證明迭代收斂。 |
| 正確性與終止 Correctness | 機率需正規化，吸收與停止條件正確；不能任意把期望代入非線性函數。 |
| 成本 Cost | 有限 DAG 為狀態與轉移成本；循環系統依求解方法決定。 |

來源：

- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)


<a id="chapter-5"></a>
## 排序與搜尋

<a id="binary-search"></a>
### 058 · Binary Search／Lower Bound／Upper Bound

來源深度：既有論述延伸

**關鍵論述：** 二分的核心是可證明的整批排除；不只適用於無重複的陣列。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 定位有序範圍中的值或判斷分界。 |
| 狀態 State | 尚未排除的區間、目標與開閉邊界語義。 |
| 轉換 Transition | 測試中點，排除不可能包含目標分界的一側。 |
| 計算順序 Order | 區間長度每輪嚴格縮小。 |
| 正確性與終止 Correctness | 答案或插入位置始終保留；lower 與 upper 對等號的定義不同。 |
| 成本 Cost | 隨機存取 O(log n) 比較與移動；非隨機迭代器的移動可能 O(n)。 |

來源：

- [二分搜尋法範本與插入點解釋](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Binary_Search/01-Binary_Search_Template.md)
- [🟢 二分搜尋全面心法整理](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Binary_Search/02-Binary_Search_Comprehensive_Guide.md)
- [二分搜尋實現分析：存在性、定位與重複值的深度探討](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Binary_Search/03-Deep_Dive_Existence_Positioning_Duplicates.md)
- [C++ STL 心法：深入理解 lowerbound 與 upperbound](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Lower_Upper_Bound_Explained.md)
- [快速決策地圖 (Quick Decision Map)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/02-Quick_Decision_Map.md)

<a id="binary-answer"></a>
### 059 · Binary Search on Answer／Constraint

來源深度：既有論述延伸

**關鍵論述：** 改變的是目標的求解方式；判定器本身仍要另行證明。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 尋找最小或最大可行的參數。 |
| 狀態 State | 答案候選範圍與可行性判定器。 |
| 轉換 Transition | 對中間參數驗證，再縮小可能的分界。 |
| 計算順序 Order | 外層二分；內層可使用 greedy、圖搜尋或 DP。 |
| 正確性與終止 Correctness | 可行集合須對參數單調，初始上下界包含答案。 |
| 成本 Cost | K 個候選、檢查 C 時為 O(C log K)，不能忽略檢查成本。 |

來源：

- [演算法心法：答案空間上的二分搜尋 (Binary Search on Solution Space)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Binary_Search/04-Binary_Search_on_Solution_Space.md)
- [心法：尋找約束來套用二分搜尋 (Binary Search on Constraint)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Binary_Search/05-Binary_Search_on_Constraint.md)
- [🔍 Binary Search on Answer 題型整理](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Binary_Search_on_Answer_Playbook.md)

<a id="inflection"></a>
### 060 · Peak／Rotated Search／結構二分

來源深度：既有論述延伸

**關鍵論述：** 局部結構也能支持排除，但不能把所有此類問題都假設成唯一拐點。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在峰值或旋轉有序結構中定位候選。 |
| 狀態 State | 候選區間與可辨識的有序側或上升方向。 |
| 轉換 Transition | 藉局部斜率或有序半部判斷縮區間。 |
| 計算順序 Order | 每轮按結構證據保留至少一個合法答案。 |
| 正確性與終止 Correctness | 找任一峰不需唯一峰；旋轉陣列遇大量相等可能無法對半排除。 |
| 成本 Cost | 可對半排除 O(log n)；重複值模糊方向時最壞 O(n)。 |

來源：

- [Inflection Point 二分搜尋 / Inflection Point Binary Search](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Binary_Search/07-Inflection_Point_Binary_Search.md)

<a id="binary-partition"></a>
### 061 · Binary Search on Partition

來源深度：既有論述延伸

**關鍵論述：** 搜尋對象是分割位置，狀態包含兩側共同必須滿足的不變量。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在兩個有序序列間找到滿足秩與邊界的切分。 |
| 狀態 State | 一側切點、由總秩決定的另一側切點、邊界值。 |
| 轉換 Transition | 依左右跨界關係調整切點。 |
| 計算順序 Order | 在較短序列的合法切點範圍二分。 |
| 正確性與終止 Correctness | 切分兩側大小與跨界有序性同時成立；空側用語義明確的界值。 |
| 成本 Cost | O(log min(n,m)) 時間、O(1) 空間。 |

來源：

- [004. Median of Two Sorted Arrays](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Super_Hard/004_Median_of_Two_Sorted_Arrays.md)

<a id="selection-sort"></a>
### 062 · Selection Sort

來源深度：既有論述延伸

**關鍵論述：** 每輪多花掃描成本，換取一個位置永久定案。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 逐位置確定全域排序。 |
| 狀態 State | 已定前綴、未定後綴與當輪極值位置。 |
| 轉換 Transition | 掃描未定區找最小值，交換到邊界。 |
| 計算順序 Order | 由左至右擴大已排序前綴。 |
| 正確性與終止 Correctness | 前綴已包含全體最小的指定數量元素。 |
| 成本 Cost | O(n²) 比較、O(n) 交換、O(1) 空間；通常不穩定。 |

來源：

- [選擇排序 (Selection Sort)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/01-Selection_Sort.md)

<a id="bubble-sort"></a>
### 063 · Bubble Sort

來源深度：既有論述延伸

**關鍵論述：** 轉換只改相鄰次序，以局部修復逐步建立全局順序。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 以相鄰交換消除逆序。 |
| 狀態 State | 未定邊界、游標與本輪是否交換。 |
| 轉換 Transition | 比較相鄰元素，交換局部逆序。 |
| 計算順序 Order | 每轮把極值送到一端；無交換可提早停止。 |
| 正確性與終止 Correctness | 完整掃描後一個極值位置定案；只交換嚴格逆序可維持穩定性。 |
| 成本 Cost | 最壞 O(n²)、最佳有早停 O(n)、O(1) 空間。 |

來源：

- [氣泡排序 (Bubble Sort)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/02-Bubble_Sort.md)

<a id="insertion-sort"></a>
### 064 · Insertion Sort

來源深度：既有論述延伸

**關鍵論述：** 排序進度是一個可維護的前綴契約，接近有序時修復工作較少。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 把新元素插入已排序前綴。 |
| 狀態 State | 有序前綴、待插元素、插入搜尋位置。 |
| 轉換 Transition | 右移較大元素或重新接鏈，再插入新元素。 |
| 計算順序 Order | 依輸入順序逐個擴張有序區。 |
| 正確性與終止 Correctness | 每步完成後前綴有序，且元素集合不變。 |
| 成本 Cost | O(n+逆序數) 時間、最壞 O(n²)；陣列版 O(1) 額外空間。 |

來源：

- [插入排序 (Insertion Sort)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/03-Insertion_Sort.md)
- [心法：使用虛擬頭節點 (Dummy Node) 簡化鏈結串列插入操作](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Linked_Lists/Dummy_Node_for_Insertion.md)

<a id="merge-sort"></a>
### 065 · Merge Sort／穩定合併

來源深度：既有論述延伸

**關鍵論述：** 父問題只需要孩子提供有序性，即可在線性時間組合。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 把有序子序列合成完整排序。 |
| 狀態 State | 左右讀取位置、輸出位置、有序子區間。 |
| 轉換 Transition | 每次取兩個未處理前端的較小者。 |
| 計算順序 Order | 先處理子區間，再合併；也可寬度倍增。 |
| 正確性與終止 Correctness | 兩端前端足以代表各自剩餘最小值；相等先取左側可穩定。 |
| 成本 Cost | O(nlog n)，陣列輔助緩衝 O(n)；鏈結版可用重接指標。 |

來源：

- [Bottom-Up Divide and Conquer 解題策略](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/04_Bottom_Up_Divide_and_Conquer.md)
- [合併排序 (Merge Sort)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/05-Merge_Sort.md)

<a id="quick-sort"></a>
### 066 · Quicksort／Pivot Selection

來源深度：既有論述延伸

**關鍵論述：** 效率取決於分割形狀；有分治形式不代表自然得到對數深度。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 透過分區逐步確定元素的相對位置。 |
| 狀態 State | 待排區間、pivot、分區邊界。 |
| 轉換 Transition | 將元素分到 pivot 兩側，再處理子區間。 |
| 計算順序 Order | 先 partition 後遞迴；隨機 pivot 降低惡劣切分風險。 |
| 正確性與終止 Correctness | 分區關係正確且子區間縮小；分區回傳值語義依 scheme 不同。 |
| 成本 Cost | 期望 O(nlog n)、最壞 O(n²)；控制小側遞迴可限制 stack。 |

來源：

- [快速排序 (Quicksort)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/06-Quicksort.md)
- [快速排序進階與優化 (Quicksort Advanced & Optimizations)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/07-Quicksort_Advanced.md)

<a id="heap-sort"></a>
### 067 · Heap Sort

來源深度：既有論述延伸

**關鍵論述：** 只維護極值可達性，就足以逐步完成全序。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 從堆中反覆取出極值形成排序。 |
| 狀態 State | 有效 heap 範圍與已排序後綴。 |
| 轉換 Transition | 交換堆頂與末項，縮小 heap 並向下修復。 |
| 計算順序 Order | 先建堆，再逐次移出極值。 |
| 正確性與終止 Correctness | 有效區維持 heap property，後綴已定案。 |
| 成本 Cost | O(nlog n) 最壞時間、O(1) 額外空間；不穩定。 |

來源：

- [堆積排序 (Heap Sort)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/04-Heap_Sort.md)

<a id="lomuto"></a>
### 068 · Lomuto Partition

來源深度：既有論述延伸

**關鍵論述：** 分界索引是分類進度；等號策略會影響重複元素時的分割品質。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 按 pivot 分割陣列。 |
| 狀態 State | 小值區邊界、掃描游標與隔離的 pivot。 |
| 轉換 Transition | 掃描時把符合比較條件者交換進小值區。 |
| 計算順序 Order | 單向掃描後把 pivot 放到分界。 |
| 正確性與終止 Correctness | 已掃區被正確分類，未掃區尚無假設；pivot 最終位置確定。 |
| 成本 Cost | O(n) 時間、O(1) 空間。 |

來源：

- [Lomuto 分割方案 (Lomuto Partition Scheme)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Partition/01-Lomuto_Partition_Scheme.md)

<a id="hoare"></a>
### 069 · Hoare Partition

來源深度：既有論述延伸

**關鍵論述：** 相同 partition 目的可以有不同契約；遞迴區間必須配合回傳語義。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 用雙向掃描建立 pivot 的兩側分區。 |
| 狀態 State | 左右游標、pivot 值與已分類兩端。 |
| 轉換 Transition | 兩側找到錯放元素後交換，直到交錯。 |
| 計算順序 Order | 左右向中央推進，注意相等值也要保證前進。 |
| 正確性與終止 Correctness | 回傳的是分割邊界，未必是 pivot 最終位置。 |
| 成本 Cost | O(n) 時間、O(1) 空間。 |

來源：

- [Partition Schemes](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Partition/README.md)
- [快速排序 (Quicksort)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/06-Quicksort.md)
- [快速排序進階與優化 (Quicksort Advanced & Optimizations)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/07-Quicksort_Advanced.md)

<a id="three-way"></a>
### 070 · Dutch National Flag／3-way Partition

來源深度：既有論述延伸

**關鍵論述：** 把「等值」獨立成已完成狀態，可以一次排除整批重複工作。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 同時分出小於、等於與大於 pivot 的三區。 |
| 狀態 State | 三區邊界與尚未分類區。 |
| 轉換 Transition | 分類一個元素，交換後依來源决定是否再檢查目前位置。 |
| 計算順序 Order | 縮小未分類區直到空。 |
| 正確性與終止 Correctness | 每區的大小關係恆成立；等值區不需再次排序。 |
| 成本 Cost | partition O(n)、O(1) 空間；可減少大量重複值的遞迴工作。 |

來源：

- [Partition Schemes](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Partition/README.md)
- [快速排序進階與優化 (Quicksort Advanced & Optimizations)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/07-Quicksort_Advanced.md)

<a id="quickselect"></a>
### 071 · Quickselect／Hoare Selection

來源深度：清單／提及延伸

**關鍵論述：** 目標只問一個秩，因此不用求解另一半的內部順序。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 找第 k 小／大，無需全部排序。 |
| 狀態 State | 候選區間、目標秩與 partition 結果。 |
| 轉換 Transition | 分區後只保留包含目標秩的一側。 |
| 計算順序 Order | 沿單一子問題前進。 |
| 正確性與終止 Correctness | 分區指出可排除的元素數量；秩需與原區間定義一致。 |
| 成本 Cost | 隨機選 pivot 期望 O(n)，最壞 O(n²)；迭代版 O(1) 額外空間。 |

來源：

- [快速排序進階與優化 (Quicksort Advanced & Optimizations)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/07-Quicksort_Advanced.md)
- [算法技巧清單 (Algorithm Techniques Checklist)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Algorithm_Techniques_Checklist.md)
- [解題 Follow-up 待辦清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Learning_Roadmap.md)

<a id="counting-sort"></a>
### 072 · Counting Sort

來源深度：既有論述延伸

**關鍵論述：** 用值域資訊取代比較，因此不受比較排序下界的同一前提限制。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在可負擔值域中排序或建立秩。 |
| 狀態 State | 各值頻率、累計位置與輸出陣列。 |
| 轉換 Transition | 計數，再以前綴和定位每個值的輸出區。 |
| 計算順序 Order | 值域順序輸出；穩定版本按一致方向分配同值位置。 |
| 正確性與終止 Correctness | 頻率保留重數；累計界線確定各值的互斥輸出區。 |
| 成本 Cost | n 筆、值域 U 時 O(n+U)；穩定版本空間 O(n+U)。 |

來源：

- [心法：使用前綴和實現計數排序 (Counting Sort)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Prefix_Sum/04_Prefix_Sum_for_Counting_Sort.md)
- [計數排序 (Counting Sort)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Non_Comparison_Based_Sorting/01-Counting_Sort.md)

<a id="radix-sort"></a>
### 073 · Radix Sort

來源深度：既有論述延伸

**關鍵論述：** 多輪局部排序的資訊必須保留下來，才能組成完整鍵順序。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 按位數分解排序鍵。 |
| 狀態 State | 當前位、已處理低位的順序與桶。 |
| 轉換 Transition | LSD 每輪對一位做穩定分配。 |
| 計算順序 Order | 由低位到高位；MSD 則先高位再桶內遞迴。 |
| 正確性與終止 Correctness | LSD 的穩定性保留先前低位順序；正負數與變長字串需明確編碼。 |
| 成本 Cost | d 位、基底 b 時 O(d(n+b))，空間依分配法。 |

來源：

- [基數排序 (Radix Sort)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Non_Comparison_Based_Sorting/02-Radix_Sort.md)

<a id="bucket-sort"></a>
### 074 · Bucket Sort

來源深度：清單／提及延伸

**關鍵論述：** 分布假設決定是否真能減少比較；不能把桶排序一律寫 O(n)。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 利用資料分布先粗分類再局部排序。 |
| 狀態 State | 有序桶區間、桶內元素與局部排序狀態。 |
| 轉換 Transition | 分桶、桶內排序、按桶次序接合。 |
| 計算順序 Order | 先建立區域順序，再處理區內細節。 |
| 正確性與終止 Correctness | 桶的值域順序不重疊；桶內排序正確。 |
| 成本 Cost | 成本 O(n+b+Σ桶內排序成本)；均勻分布才有常見期望線性界。 |

來源：

- [算法技巧清單 (Algorithm Techniques Checklist)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Algorithm_Techniques_Checklist.md)
- [解題 Follow-up 待辦清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Learning_Roadmap.md)

<a id="introsort"></a>
### 075 · Introsort／std::sort 常見實作

來源深度：既有論述延伸

**關鍵論述：** 控制狀態也能包含「資源預算」，用來決定何時換算法。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 結合快速常數與最壞比較次數保證。 |
| 狀態 State | 待排區間、深度預算、區間大小。 |
| 轉換 Transition | 正常 partition；深度耗盡切 heap sort，小區間用 insertion sort。 |
| 計算順序 Order | 由區間規模與深度選子策略。 |
| 正確性與終止 Correctness | 各子策略滿足排序契約，切換不改變結果。 |
| 成本 Cost | 典型 O(nlog n) 最壞比較；std::sort 規範不綁定某個實作。 |

來源：

- [內省排序 (Introsort) - C++ std::sort 的核心](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/cpp-introsort.md)
- [C++ 排序演算法比較：std::sort, std::stablesort, 與 container.sort()](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Sort_Comparison.md)

<a id="timsort"></a>
### 076 · Timsort／Natural Runs

來源深度：清單／提及延伸

**關鍵論述：** 輸入已完成的工作也是可重用狀態，無需從單元素全部重建。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 利用現成有序片段做穩定排序。 |
| 狀態 State | 有序 runs、待合併 stack 與 run 長度。 |
| 轉換 Transition | 偵測並整理 runs，按合併策略建立較長 run。 |
| 計算順序 Order | 適應輸入既有順序，再進行受控合併。 |
| 正確性與終止 Correctness | 合併維持穩定性；run 排程需防止過度失衡。 |
| 成本 Cost | 最壞 O(nlog n)、已序可 O(n)，常用 O(n) 緩衝。 |

來源：

- [合併排序 (Merge Sort)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/05-Merge_Sort.md)
- [C++ 排序演算法比較：std::sort, std::stablesort, 與 container.sort()](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Sort_Comparison.md)

<a id="next-permutation"></a>
### 077 · Next Permutation

來源深度：清單／提及延伸

**關鍵論述：** 利用後綴已達最大排列的證據，一次排除所有無效的小改動。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 構造字典序下一個排列。 |
| 狀態 State | 最長非遞增後綴、前一位置與替換候選。 |
| 轉換 Transition | 讓最靠右可增加的位置做最小增加，再把後綴最小化。 |
| 計算順序 Order | 由右找可改進邊界，再整理後綴。 |
| 正確性與終止 Correctness | 保持更長前綴不變並最小增加，可保證是緊鄰的下一排列。 |
| 成本 Cost | O(n) 時間、O(1) 額外空間。 |

來源：

- [C++ One-Liners for LeetCode](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/CPP_One_Liners.md)
- [LeetCode Tricks and Keywords](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/LeetCode_Tricks_and_Keywords.md)


<a id="chapter-6"></a>
## 指標與區間

<a id="two-pointers"></a>
### 078 · Two Pointers／對向與同向指標

來源深度：既有論述延伸

**關鍵論述：** 兩個指標本身不保證線性或正確；被跳過的候選需要理由。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 以單調邊界代替重複枚舉。 |
| 狀態 State | 兩個索引、已排除區域、必要局部摘要。 |
| 轉換 Transition | 按比較結果移動一端，或同步前進。 |
| 計算順序 Order | 相向收斂或同向推進，依問題性質選擇。 |
| 正確性與終止 Correctness | 每次移動必須證明跳過的配對無需再檢查。 |
| 成本 Cost | 每指標只走 n 次且每步 O(1) 時總 O(n)。 |

來源：

- [雙指針核心模式與模板 (Two Pointers: Core Patterns & Templates)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Two_Pointers/01-Two_Pointers_Core_Patterns_and_Templates.md)

<a id="fast-slow"></a>
### 079 · Fast–Slow／Floyd Cycle Detection

來源深度：既有論述延伸

**關鍵論述：** 利用進度差摘要路徑資訊，避免保存全部 visited。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 找中點或確定性後繼關係中的環。 |
| 狀態 State | 不同速度的位置；找環入口時另有第二階段的位置。 |
| 轉換 Transition | 按不同速率移動；相遇後利用距離關係定位入口。 |
| 計算順序 Order | 遵循同一個後繼函數，先檢查空節點。 |
| 正確性與終止 Correctness | 有環時相對位置在有限環中追上；中點與找環是不同停止契約。 |
| 成本 Cost | 鏈長或前導長 μ 加環長 λ 的 O(μ+λ) 時間、O(1) 空間。 |

來源：

- [雙指針核心模式與模板 (Two Pointers: Core Patterns & Templates)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Two_Pointers/01-Two_Pointers_Core_Patterns_and_Templates.md)
- [雙指針模式：快慢指針 (Fast & Slow Pointers)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Two_Pointers/02_Fast_and_Slow_Pointers.md)

<a id="k-gap"></a>
### 080 · K-Gap Pointers

來源深度：既有論述延伸

**關鍵論述：** 用空間上的距離保存「距離結尾還有幾步」的資訊。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在終點未知時取得相隔 k 個位置的元素。 |
| 狀態 State | 前後指標與固定距離。 |
| 轉換 Transition | 前指標先走 k 步，再同步移動。 |
| 計算順序 Order | 建立距離後一路走到前端停止。 |
| 正確性與終止 Correctness | 兩指標間距維持指定定義，dummy 是否計入需一致。 |
| 成本 Cost | O(n) 時間、O(1) 空間。 |

來源：

- [雙指針模式：固定間距指針 (K-Gap Pointers)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Two_Pointers/03_K_Gap_Pointers.md)

<a id="adjacent"></a>
### 081 · Adjacent Pointers／Read–Write Compaction

來源深度：既有論述延伸

**關鍵論述：** 把輸出區直接放在輸入前綴，省下新的容器。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 比較鄰接關係或原地濾除、去重。 |
| 狀態 State | 讀取游標、已保留前綴末端或相鄰元素。 |
| 轉換 Transition | 符合保留條件才寫入並移動寫入端。 |
| 計算順序 Order | 讀取從左至右，寫入不能覆蓋未讀資料。 |
| 正確性與終止 Correctness | 已寫區精確等於已讀資料的合法結果。 |
| 成本 Cost | O(n) 時間、O(1) 額外空間。 |

來源：

- [雙指針核心模式與模板 (Two Pointers: Core Patterns & Templates)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Two_Pointers/01-Two_Pointers_Core_Patterns_and_Templates.md)
- [雙指針子模式：相鄰指針 (Adjacent Pointers)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Two_Pointers/04_Adjacent_Pointers.md)

<a id="skip-iterator"></a>
### 082 · Skip-Based Dual Iterator

來源深度：既有論述延伸

**關鍵論述：** 隱式產生轉換後的序列，避免把完整中間結果存出來。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 比較經過忽略、刪除或轉換後的兩序列。 |
| 狀態 State | 兩個游標與各自的跳過數量／規則。 |
| 轉換 Transition | 各自找到下一個有效元素，再比較與同步前進。 |
| 計算順序 Order | 依跳過規則正向或逆向掃描。 |
| 正確性與終止 Correctness | 只有有效元素被比較，跳過操作的影響需完全消耗。 |
| 成本 Cost | 兩序列長 n,m 時 O(n+m)、常數額外空間。 |

來源：

- [Skip-Based Dual Iterator 解題心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Two_Pointers/05_Skip_Based_Dual_Iterator.md)

<a id="center-expand"></a>
### 083 · Expand Around Center

來源深度：既有論述延伸

**關鍵論述：** 以中心重新參數化區間，使合法性可以增量檢查。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 枚舉回文或中心對稱結構。 |
| 狀態 State | 中心、左右邊界與目前最佳摘要。 |
| 轉換 Transition | 兩端符合對稱條件就同時向外擴張。 |
| 計算順序 Order | 分別處理奇數與偶數中心。 |
| 正確性與終止 Correctness | 每個回文有唯一中心；擴張失敗後更大同中心區間也不合法。 |
| 成本 Cost | 最壞 O(n²) 時間、O(1) 額外空間（不計輸出）。 |

來源：

- [Expand Around Center 心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Two_Pointers/06_Expand_Around_Center.md)

<a id="fixed-window"></a>
### 084 · Fixed Sliding Window

來源深度：既有論述延伸

**關鍵論述：** 相鄰查詢只有兩個元素不同，因此可以重用大部分工作。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 取得每個固定長度區間的摘要。 |
| 狀態 State | 左右界線、區間大小、可增刪摘要。 |
| 轉換 Transition | 加入新元素並移除離開元素。 |
| 計算順序 Order | 窗口逐格前進，完整長度時結算。 |
| 正確性與終止 Correctness | 摘要必須精確對應目前窗口，邊界不足長度時不結算。 |
| 成本 Cost | 每次摘要更新 O(1) 時總 O(n)；空間依摘要。 |

來源：

- [Sliding Window 標準模板](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sliding_Window/00-Sliding_Window_Standard_Template.md)
- [Sliding Window 進階技巧：Constraint 追蹤與優化](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sliding_Window/01-Constraint_Tracking_and_Optimization.md)
- [Sorted Sliding Window](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sliding_Window/02-Sorted_Sliding_Window.md)
- [🎯 Sliding Window Frequency Matching - 練習路徑](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Sliding_Window_Frequency_Matching_Playbook.md)

<a id="variable-window"></a>
### 085 · Variable Sliding Window／Sorted Window

來源深度：既有論述延伸

**關鍵論述：** Expand–Fix–Update 有適用目標；不能把最短覆蓋套成最長可行窗口的同一時機。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 找具有可單調修復條件的最長或最短連續區間。 |
| 狀態 State | 左右界線、可行性摘要、答案。 |
| 轉換 Transition | 擴張與收縮，使窗口到達目標所需的可行邊界。 |
| 計算順序 Order | 最長可行常先修復再結算；最短覆蓋常在仍可行時縮小並結算。 |
| 正確性與終止 Correctness | 必須證明移動左界不會漏掉更好候選；負數可能破壞和的單調性。 |
| 成本 Cost | 單調指標與常數更新時 O(n)；若先排序另加 O(nlog n)。 |

來源：

- [Sliding Window 標準模板](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sliding_Window/00-Sliding_Window_Standard_Template.md)
- [Sliding Window 進階技巧：Constraint 追蹤與優化](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sliding_Window/01-Constraint_Tracking_and_Optimization.md)
- [Sorted Sliding Window](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sliding_Window/02-Sorted_Sliding_Window.md)

<a id="frequency-window"></a>
### 086 · Frequency Matching／Counting Invariant

來源深度：既有論述延伸

**關鍵論述：** 把「每次重比整張表」轉成「只維修變動的那一項」。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 快速判定窗口與需求的頻率是否匹配。 |
| 狀態 State | 需求表、窗口頻率、滿足條件的項目數。 |
| 轉換 Transition | 元素更新前移除舊貢獻，更新後加入新貢獻。 |
| 計算順序 Order | 配合窗口增刪；初始化需納入零頻項語義。 |
| 正確性與終止 Correctness | matchedCount 始終等於被滿足的需求維度數。 |
| 成本 Cost | 固定字母表或期望 O(1) hash 下每步 O(1)，總 O(n)。 |

來源：

- [🎯 Sliding Window Frequency Matching - 練習路徑](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Sliding_Window_Frequency_Matching_Playbook.md)
- [Frequency Matching Counting Invariant 心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Hash_Tables/Frequency_Matching_Counting_Invariant.md)

<a id="at-most"></a>
### 087 · Exactly K = At Most K − At Most K−1

來源深度：清單／提及延伸

**關鍵論述：** 透過改寫目標，讓原本不易維護的等號條件變成單調門檻。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 計算恰好具有 k 個離散特徵的區間數。 |
| 狀態 State | 兩個累計可行數，或兩個對應門檻的窗口。 |
| 轉換 Transition | 分別計算 ≤k 與 ≤k−1 的數量後相減。 |
| 計算順序 Order | 各自按可行性單調的窗口算法掃描。 |
| 正確性與終止 Correctness | 精確 k 集合等於兩個巢狀集合之差；窗口條件另需可維護。 |
| 成本 Cost | 兩次線性窗口仍 O(n)，空間依頻率表。 |

來源：

- [🎯 Technique Integration Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Technique_Integration_Problems.md)
- [🎯 Sliding Window Frequency Matching - 練習路徑](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Sliding_Window_Frequency_Matching_Playbook.md)

<a id="ksum"></a>
### 088 · K-Sum／Rolling Hash Lookup

來源深度：既有論述延伸

**關鍵論述：** 少一層枚舉，來自把「搜尋另一半」改成具有索引的查詢。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 尋找或計數和為目標的不同元素組合。 |
| 狀態 State | 固定前綴、剩餘目標、候選後綴或已見值表。 |
| 轉換 Transition | 固定一項降成較小 K-Sum；2-Sum 用補數查找或有序雙指標。 |
| 計算順序 Order | 先查後插可避免使用同一索引；排序版按層去重。 |
| 正確性與終止 Correctness | 索引不可重用；同值不同身份與相同輸出需區分。 |
| 成本 Cost | 2-Sum hash 期望 O(n)；固定 k 的排序枚舉常 O(n^(k−1))。 |

來源：

- [1. Two Sum (兩數之和)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/K-Sum_Problems/01-Two_Sum.md)
- [2. Three Sum (三數之和)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/K-Sum_Problems/02-Three_Sum.md)

<a id="backward-fill"></a>
### 089 · Backward Fill／逆序批次修改

來源深度：既有論述延伸

**關鍵論述：** 改變處理順序可以消除保存舊資料的需求。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 原地變換資料且避免覆蓋未讀來源。 |
| 狀態 State | 來源末端、輸出末端、批次修改索引。 |
| 轉換 Transition | 從後方讀寫，或由最大索引向前套用修改。 |
| 計算順序 Order | 逆向處理，必要時先算最終長度。 |
| 正確性與終止 Correctness | 每次寫入不能破壞尚待讀取的來源；批次索引語義需固定。 |
| 成本 Cost | 搬移線性時 O(n)；批次需另計排序及實際搬移。 |

來源：

- [逆序處理模式 / Reverse Processing Patterns](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/Reverse_Processing_Patterns.md)


<a id="chapter-7"></a>
## 聚合與貪婪

<a id="prefix"></a>
### 090 · Prefix Sum／2D–3D Prefix／Prefix XOR

來源深度：既有論述延伸

**關鍵論述：** 資料結構預先保存可逆摘要，以空間換取大量重複查詢的時間。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 加速靜態區間聚合查詢。 |
| 狀態 State | 各前綴的和或 XOR；多維保存區域前綴。 |
| 轉換 Transition | 建構時納入新值；查詢時以差或容斥消掉區間外貢獻。 |
| 計算順序 Order | 依前綴依賴順序預處理。 |
| 正確性與終止 Correctness | 摘要運算需支持相應逆運算；min 不能直接相減求區間最小。 |
| 成本 Cost | 一維 O(n) 預處理、O(1) 查詢；固定維度查詢需 2^d 項。 |

來源：

- [演算法技巧：前綴和 (Prefix Sum)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Prefix_Sum/01_Prefix_Sum_Intro.md)
- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)

<a id="running-state"></a>
### 091 · Running State／Prefix–Suffix Aggregation

來源深度：既有論述延伸

**關鍵論述：** 只保存未來會使用的聚合資訊，避免反覆掃描同一前綴。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 掃描時持續維護和、乘積、極值或雙側約束。 |
| 狀態 State | 已掃前綴摘要；必要時另存後綴摘要與答案。 |
| 轉換 Transition | 把當前元素折入摘要，再按正確版本回答查詢。 |
| 計算順序 Order | 左至右或兩次反向掃描。 |
| 正確性與終止 Correctness | 每個摘要精確表示對應前綴／後綴；雙側組合式須由題意推導。 |
| 成本 Cost | 常數大小摘要為 O(n)；需要逐位置雙側結果時 O(n) 空間。 |

來源：

- [雙向約束分解 / Bidirectional Constraint Decomposition](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Bidirectional_Constraint_Decomposition.md)
- [設計模式：滾動狀態 (Design Pattern: Running State)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Prefix_Sum/02_Running_State_Pattern.md)

<a id="prefix-hash"></a>
### 092 · Prefix Sum + Hash Map

來源深度：既有論述延伸

**關鍵論述：** 區間條件被改寫為兩個前綴的關係，枚舉左端改成索引查詢。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 計算符合和或餘數關係的連續區間。 |
| 狀態 State | 目前前綴摘要與歷史摘要的頻率或最早位置。 |
| 轉換 Transition | 查找相差指定值的歷史摘要，再保存當前摘要。 |
| 計算順序 Order | 依原序列掃描；空前綴先初始化。 |
| 正確性與終止 Correctness | 先查後插與頻率語義須符合空區間及重複計數要求。 |
| 成本 Cost | hash 期望 O(n)、O(n) 空間；最壞成本依碰撞。 |

來源：

- [🎯 Technique Integration Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Technique_Integration_Problems.md)
- [Hash Tables, Hash Maps, and Sets](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Hash_Tables/README.md)

<a id="prefix-binary"></a>
### 093 · Prefix Sum + Binary Search

來源深度：既有論述延伸

**關鍵論述：** 摘要和搜尋可組合，但搜尋所需的順序性必須另行成立。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在前綴摘要中定位達到門檻的位置。 |
| 狀態 State | 有序前綴表、查詢起點與目標累計值。 |
| 轉換 Transition | 把區間條件轉成前綴門檻，再二分定位。 |
| 計算順序 Order | 先預處理，再按查詢執行二分。 |
| 正確性與終止 Correctness | 前綴和須單調，例如元素非負；負數時不可直接二分原前綴表。 |
| 成本 Cost | O(n) 建表、每查詢 O(log n)，空間 O(n)。 |

來源：

- [演算法組合拳：前綴和 + 二分搜尋](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Prefix_Sum/03_Prefix_Sum_with_Binary_Search.md)

<a id="difference"></a>
### 094 · Difference Array／多維差分

來源深度：既有論述延伸

**關鍵論述：** 把整段重複更新轉成少量邊界事件，延後實際展開。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 加速批次區間加減。 |
| 狀態 State | 各位置相較前一位置的變化量，多維為邊界角點。 |
| 轉換 Transition | 把區間更新寫成起點與終點後的事件。 |
| 計算順序 Order | 累積完所有更新，再前綴還原。 |
| 正確性與終止 Correctness | 差分還原後等於所有區間更新的疊加；端點開閉一致。 |
| 成本 Cost | 一維 q 次更新加還原 O(q+n)，單次記錄 O(1)。 |

來源：

- [Difference Array 演算法心法 (基於半開區間 left, right))](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Prefix_Sum/05_Difference_Array.md)
- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)

<a id="sweep"></a>
### 095 · Sweep Line／重疊區間／Heap Simulation

來源深度：既有論述延伸

**關鍵論述：** 狀態只會在事件點改變，因此不用逐單位模擬時間。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 追蹤時間線上的活躍區間與資源。 |
| 狀態 State | 有序事件、活躍集合、重疊數或資源釋放時間。 |
| 轉換 Transition | 開始加入、結束移除，事件間沿用狀態。 |
| 計算順序 Order | 按時間掃描；同時刻依開閉區間定義排序或分批結算。 |
| 正確性與終止 Correctness | 活躍集合恰好對應當前時間點或時間段。 |
| 成本 Cost | 事件排序 O(nlog n)；每事件 O(1) 或 O(log n) 更新。 |

來源：

- [掃描線算法 解題心法 / Sweep Line Algorithm](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sweep_Line/01-Sweep_Line_Core_Concepts.md)
- [最大併發區間 解題心法 / Maximum Concurrent Intervals](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sweep_Line/02-Maximum_Concurrent_Intervals.md)
- [🎯 Technique Integration Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Technique_Integration_Problems.md)

<a id="sweep2d"></a>
### 096 · 2D Sweep／Rectangle Union／Skyline

來源深度：既有論述延伸

**關鍵論述：** 把一個維度改成時間，剩下的幾何關係交給可更新的摘要。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 聚合平面覆蓋或輪廓。 |
| 狀態 State | 掃描座標、另一軸活躍區間、覆蓋長度或最大高度。 |
| 轉換 Transition | 事件改變活躍集合；相鄰事件間累積面積或輸出高度變化。 |
| 計算順序 Order | 排序 x 事件，同 x 事件須一致結算。 |
| 正確性與終止 Correctness | 覆蓋長度計聯集而非重複加總；heap 過期項需刪除或驗證。 |
| 成本 Cost | 配合 segment tree／heap 常見 O(nlog n)，空間 O(n)。 |

來源：

- [2D Sweep Line 解題心法 / 2D Sweep Line Pattern](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sweep_Line/03-2D_Sweep_Line.md)
- [🎯 Technique Integration Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Technique_Integration_Problems.md)

<a id="greedy"></a>
### 097 · Greedy／Sort vs Heap

來源深度：既有論述延伸

**關鍵論述：** 貪婪的核心是安全縮減選擇，資料結構只負責便宜地找出該選擇。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 逐步選擇且維持存在最佳完成方案。 |
| 狀態 State | 已選集合、可用候選、剩餘資源與目標摘要。 |
| 轉換 Transition | 作出可證明安全的選擇，或替換較差的已選項。 |
| 計算順序 Order | 固定全域順序可排序；動態可用性可用 heap。 |
| 正確性與終止 Correctness | 需要交換、領先或割性質等證明；貪婪選擇仍可能影響未來。 |
| 成本 Cost | 由排序與總候選更新次數決定，常見 O(nlog n)。 |

來源：

- [心法：貪婪演算法的辨識與應用框架](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Greedy_Identification_and_Application.md)
- [心法：貪婪演算法的實現策略：排序 vs. 堆 (Sort vs. Heap)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Greedy_Sort_vs_Heap.md)

<a id="interval-greedy"></a>
### 098 · Interval Merge／Intersection／Scheduling

來源深度：既有論述延伸

**關鍵論述：** 相同區間輸入因目標不同，需要保存與排序的資訊也不同。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 合併覆盖、求交集或最多選取互斥區間。 |
| 狀態 State | 目前合併區間、兩序列游標，或最後選取終點。 |
| 轉換 Transition | 合併更新邊界；求交取共同範圍；排程選最早結束者。 |
| 計算順序 Order | 合併依起點；最大數量排程依終點；交集用雙指標。 |
| 正確性與終止 Correctness | 三種目標有不同不變量；帶權收益不能直接用最早結束貪婪。 |
| 成本 Cost | 排序後掃描 O(n)，整體 O(nlog n)；已序交集 O(n+m)。 |

來源：

- [Interval 問題解題心法 (Playbook)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Interval_Problem_Solving_Playbook.md)
- [🎯 Technique Integration Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Technique_Integration_Problems.md)

<a id="weighted-scheduling"></a>
### 099 · Weighted Interval Scheduling／DP + Binary Search

來源深度：清單／提及延伸

**關鍵論述：** 二分加速前驅查詢，DP 負責收益取捨；不能只靠排序替代後者。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 選互不衝突的工作以最大化總收益。 |
| 狀態 State | 排序後工作前綴、最佳收益、前一相容工作位置。 |
| 轉換 Transition | 比較不取目前工作與取它加相容前綴收益。 |
| 計算順序 Order | 按終點排序，用二分查相容邊界。 |
| 正確性與終止 Correctness | 最後一份工作把答案分成取與不取；端點相接是否合法需固定。 |
| 成本 Cost | O(nlog n) 時間、O(n) 空間。 |

來源：

- [🎯 Technique Integration Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Technique_Integration_Problems.md)

<a id="pivotal"></a>
### 100 · Pivotal-Element-First／關鍵限制優先

來源深度：既有論述延伸

**關鍵論述：** 先確定「誰支配可行性」，有助於找到安全的決策單位。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 以最限制可行性的元素決定處理次序。 |
| 狀態 State | 關鍵元素、可選對象、剩餘限制。 |
| 轉換 Transition | 優先安排極值或最受限者，再處理殘餘問題。 |
| 計算順序 Order | 順序由可交換或配對性質決定。 |
| 正確性與終止 Correctness | 須證明優先處理不破壞最佳完成可能；只是辨識啟發不等於證明。 |
| 成本 Cost | 常由排序或 heap 主導 O(nlog n)。 |

來源：

- [心法：關鍵元素優先貪婪法 (Pivotal-Element-First Greedy)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Pivotal_Element_First_Greedy.md)

<a id="topk-greedy"></a>
### 101 · Greedy Sweep + Top-K／Push–Pop Replacement

來源深度：既有論述延伸

**關鍵論述：** 把多維取捨拆成「固定一維」與「高效維護其餘候選」。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 掃描門檻時維護最佳固定數量候選。 |
| 狀態 State | 目前門檻、選中集合、heap 與收益／成本和。 |
| 轉換 Transition | 加入候選，超量或違反限制時移除可證明最差者。 |
| 計算順序 Order | 沿某一維排序掃描，另一維用 heap 維護。 |
| 正確性與終止 Correctness | 對每個門檻保留的集合確為其子問題最佳；複合目標需額外單調條件。 |
| 成本 Cost | 每項常數次進出時 O(nlog k)，另加排序。 |

來源：

- [Greedy Sweep Cost Optimization with Top-K](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Greedy_Sweep_Cost_Optimization_with_Top_K.md)
- [心法：固定大小堆模式 (Fixed-Size Heap Pattern)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/03-Push_Pop_Fixed_Size_Heap.md)
- [心法：堆與貪婪策略的時間複雜度：聚合分析 (Aggregate Analysis)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/06-Amortized_Analysis.md)

<a id="twoheap-selection"></a>
### 102 · Two Heaps：可行性與收益選擇

來源深度：既有論述延伸

**關鍵論述：** 兩個 heap 分別回答「能選誰」與「選誰較好」，不負責中位數平衡。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在限制逐步變化下選當前最佳可用項。 |
| 狀態 State | 未解鎖 heap、可用 heap、資源與已選次數。 |
| 轉換 Transition | 先把新可行候選搬入，再取最佳收益項。 |
| 計算順序 Order | 可行性檢查先於收益選擇；固定輸入可排序取代第一堆。 |
| 正確性與終止 Correctness | 資源變化與安全選擇需證明；非負收益常用來支持可用集合單調擴張。 |
| 成本 Cost | 每項最多搬移一次時 O(nlog n)，空間 O(n)。 |

來源：

- [心法：關鍵元素優先貪婪法 (Pivotal-Element-First Greedy)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Pivotal_Element_First_Greedy.md)
- [心法：雙堆貪婪選擇模式 (Two-Heap Greedy Selection Pattern)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Two_Heaps_Greedy_Selection.md)

<a id="range-greedy"></a>
### 103 · Reachable Range／Greedy Frontier

來源深度：清單／提及延伸

**關鍵論述：** 用整個可行集合的邊界取代逐狀態列舉，需要集合形狀的證明。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 以區間摘要維護可達位置或可行計數。 |
| 狀態 State | 目前可達範圍、下一輪最遠界線或可行值下上界。 |
| 轉換 Transition | 掃描範圍內候選擴張下一範圍。 |
| 計算順序 Order | 依位置或層邊界結算，可能類似隱式 BFS。 |
| 正確性與終止 Correctness | 可達集合須真的能用連續區間表示；有空洞時只記 min/max 會錯。 |
| 成本 Cost | 單向掃描常見 O(n)、O(1) 空間。 |

來源：

- [LeetCode Tricks and Keywords](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/LeetCode_Tricks_and_Keywords.md)

<a id="boyer-moore"></a>
### 104 · Boyer–Moore Voting／Majority Cancellation

來源深度：既有論述延伸

**關鍵論述：** 抵消保留的是超門檻者的存在，不是一般 mode 的精確頻率。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 找出出現次數超過門檻的候選。 |
| 狀態 State | 候選值與抵消後計數；n/k 版本保存 k−1 個候選。 |
| 轉換 Transition | 相同累加，不同互相抵消，必要時替換零計數候選。 |
| 計算順序 Order | 一輪選候選；若未保證存在，再掃描驗證頻率。 |
| 正確性與終止 Correctness | 真正超過 n/k 的元素不能被 k 種不同元素等量抵消掉。 |
| 成本 Cost | 多數 >n/2 為 O(n)、O(1)；一般 k 的直接實作依 k 計成本。 |

來源：

- [Boyer-Moore Voting Algorithm 解題心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Boyer_Moore_Voting/Boyer_Moore_Voting_Algorithm.md)

<a id="kruskal"></a>
### 105 · Kruskal／Minimum Spanning Forest

來源深度：既有論述延伸

**關鍵論述：** 最優性靠割性質，DSU 只負責摘要「會不會形成環」。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 以最小總邊權連接所有可連通節點。 |
| 狀態 State | 已選森林、DSU 分量、有序邊。 |
| 轉換 Transition | 按權重取邊，若跨分量就合併並選入。 |
| 計算順序 Order | 由小到大處理邊。 |
| 正確性與終止 Correctness | 割性質支持安全邊；同分量邊只會形成環。 |
| 成本 Cost | O(Elog E)+DSU 成本，圖與邊儲存 O(V+E)。 |

來源：

- [Kruskal's Algorithm for Minimum Spanning Tree](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/MST_Algorithms/01-Kruskals_Algorithm.md)
- [最小生成樹 (Minimum Spanning Tree) 核心理論：Cut Property](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Minimum_Spanning_Tree/01-Cut_Property_and_MST_Intro.md)

<a id="prim"></a>
### 106 · Prim／切割前沿

來源深度：既有論述延伸

**關鍵論述：** Prim 與 Dijkstra 可用同類排程工具，但標籤語義和證明不同。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 逐步擴張最小生成樹。 |
| 狀態 State | 已連接集合、跨割候選邊或各外點最便宜連接成本。 |
| 轉換 Transition | 選最輕跨割邊，把新點納入並更新邊界。 |
| 計算順序 Order | 按連接到樹的邊權選擇，與起點路徑距離不同。 |
| 正確性與終止 Correctness | 割性質保證安全；不連通圖需對各分量重新啟動。 |
| 成本 Cost | binary heap 常見 O(Elog V)；稠密陣列版 O(V²)。 |

來源：

- [Prim's Algorithm for Minimum Spanning Tree](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/MST_Algorithms/02-Prims_Algorithm.md)
- [最小生成樹 (Minimum Spanning Tree) 核心理論：Cut Property](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Minimum_Spanning_Tree/01-Cut_Property_and_MST_Intro.md)


<a id="chapter-8"></a>
## 資料結構

<a id="array"></a>
### 107 · Array／Vector／String

來源深度：既有論述延伸

**關鍵論述：** 表示讓「位置查詢」便宜；內容搬移與複製不會因此消失。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 保存有順序、可隨機存取的序列。 |
| 狀態 State | 連續元素、長度；動態版本另有容量。 |
| 轉換 Transition | 按索引讀寫、尾部追加，必要時搬移或重新配置。 |
| 計算順序 Order | 由使用者算法決定；搬移需保持未處理資料。 |
| 正確性與終止 Correctness | 索引有效且順序符合契約；vector 重新配置可能使參照失效。 |
| 成本 Cost | 索引 O(1)，vector 尾插攤銷 O(1)，中間插刪 O(n)，字串複制 O(length)。 |

來源：

- [C++ 常用數據結構 API 參考](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Common_Container_APIs.md)
- [String Building Patterns](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/String_Building_Patterns.md)
- [數組問題解題策略](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/Array_Problem_Strategies.md)

<a id="linked-list"></a>
### 108 · Singly／Doubly Linked List

來源深度：既有論述延伸

**關鍵論述：** 局部更新便宜的前提是已經找到位置，不能省略定位成本。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 以局部接鏈支持序列插刪。 |
| 狀態 State | 節點身份、前後連結、頭尾指標。 |
| 轉換 Transition | 建立或解除鄰接關係，保留未處理鏈段。 |
| 計算順序 Order | 依連結走訪；雙向連結須同步更新兩側。 |
| 正確性與終止 Correctness | 所有剩餘節點可達且不意外成環；記憶體所有權正確。 |
| 成本 Cost | 已知位置插刪 O(1)；搜尋或第 k 項 O(n)，儲存 O(n)。 |

來源：

- [C++ 常用數據結構 API 參考](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Common_Container_APIs.md)
- [鏈表 (Linked List)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Linked_Lists/README.md)

<a id="dummy-reverse"></a>
### 109 · Dummy Node／Linked List Reversal

來源深度：既有論述延伸

**關鍵論述：** 哨兵擴充表示以減少分支；反轉靠保存即將被覆蓋的連結。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 統一頭部操作並改變鏈方向。 |
| 狀態 State | dummy、前驅、目前與下一節點，或區段邊界。 |
| 轉換 Transition | 先保存下一節點，再重接指向；dummy 提供一致前驅。 |
| 計算順序 Order | 沿原鏈逐步轉換，最後接回區段兩端。 |
| 正確性與終止 Correctness | 處理前綴與未處理後綴均保持可達，頭部邊界與一般位置同契約。 |
| 成本 Cost | 反轉 O(n)、O(1)；dummy 本身只增加常數空間。 |

來源：

- [算法技巧清單 (Algorithm Techniques Checklist)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Algorithm_Techniques_Checklist.md)
- [心法：使用虛擬頭節點 (Dummy Node) 簡化鏈結串列插入操作](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Linked_Lists/Dummy_Node_for_Insertion.md)
- [鏈表 (Linked List)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Linked_Lists/README.md)

<a id="stack"></a>
### 110 · Stack／Min Stack

來源深度：清單／提及延伸

**關鍵論述：** stack 不只記資料，也記錄「返回後要繼續什麼」。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 保存最近未完成的工作，或支持當前最小值查詢。 |
| 狀態 State | LIFO 元素序列；Min Stack 另保存每層最小摘要。 |
| 轉換 Transition | push 建立新層，pop 恢復上一層摘要。 |
| 計算順序 Order | 後進先出。 |
| 正確性與終止 Correctness | 頂部代表最近未完成項；Min Stack 摘要隨整層一起還原。 |
| 成本 Cost | push/pop/top 常見 O(1) 或攤銷 O(1)；空間 O(n)。 |

來源：

- [C++ 常用數據結構 API 參考](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Common_Container_APIs.md)
- [NeetCode 150 (150 題)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Lists/NeetCode_150.md)

<a id="queue-deque"></a>
### 111 · Queue／Deque

來源深度：既有論述延伸

**關鍵論述：** 容器提供操作能力，正確性來自算法對順序的使用。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 保存先到先處理或雙端排程的待辦集合。 |
| 狀態 State | 有序待辦項、首尾位置。 |
| 轉換 Transition | queue 尾入首出；deque 允許兩端增刪。 |
| 計算順序 Order | FIFO 或由算法選擇兩端優先級。 |
| 正確性與終止 Correctness | 容器順序需對應排程語義；deque 本身不保證最短路或單調性。 |
| 成本 Cost | 常見雙端操作 O(1)；儲存 O(n)。 |

來源：

- [C++ 常用數據結構 API 參考](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Common_Container_APIs.md)
- [C++ deque vs queue 完整比較與使用指南](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Deque_vs_Queue.md)

<a id="hash"></a>
### 112 · Hash Table／Hash Map／Hash Set

來源深度：既有論述延伸

**關鍵論述：** hash 把搜尋轉成索引，保證是期望性的，不能假設 C++ 碰撞必轉紅黑樹。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 依鍵快速查找、計數或保存子問題結果。 |
| 狀態 State | 鍵值、hash buckets、等值判斷與負載資訊。 |
| 轉換 Transition | hash 定位候選桶，再比對完整鍵並增刪。 |
| 計算順序 Order | 沒有排序保證；查詢是否插入需明確區分。 |
| 正確性與終止 Correctness | 相等鍵必有相等 hash；相等 hash 不代表相等鍵。 |
| 成本 Cost | 理想 hash 下期望 O(1) 查找，最壞 O(n)；長鍵 hash 成本另計。 |

來源：

- [C++ 容器陷阱：const map/unorderedmap 與 operator](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Const_Map_and_Operator_Bracket.md)
- [C++ STL 容器的遍歷順序與有序性詳解](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Container_Iteration_Order.md)
- [C++ 資料結構選用心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Container_Selection_Guide.md)
- [如何為 unordered 容器的複合鍵提供自訂雜湊 (Custom Hasher)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Custom_Hasher_For_Unordered_Containers.md)
- [C++ 容器陷阱：vector vs. map 的 operator 行為差異](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Operator_Bracket_Behavior_Vector_vs_Map.md)
- [Hash Tables, Hash Maps, and Sets](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Hash_Tables/README.md)

<a id="hash-collision"></a>
### 113 · Chaining／Open Addressing／2-Choice Hashing

來源深度：既有論述延伸

**關鍵論述：** 碰撞策略是狀態布局的選擇，决定平均成本、最壞成本與刪除語義。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 處理多個鍵映射到相同位置。 |
| 狀態 State | 桶鏈／探測表、空位與 tombstone，或兩個候選桶。 |
| 轉換 Transition | 鏈結保存衝突、按規則探測，或選負載較小的候選桶。 |
| 計算順序 Order | 查詢沿與插入一致的候選路徑。 |
| 正確性與終止 Correctness | 刪除不能切斷 open addressing 的探測鏈；2-choice 查詢要查可能位置。 |
| 成本 Cost | 低負載與合適 hash 下常有期望常數成本；最壞仍需分析碰撞。 |

來源：

- [解題 Follow-up 待辦清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Learning_Roadmap.md)

<a id="ordered-map"></a>
### 114 · Ordered Map／Set／Multiset

來源深度：既有論述延伸

**關鍵論述：** 為順序能力支付對數更新成本，換取 hash 沒有的區間導航。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 維護有序鍵，支援前驅、後繼與範圍查詢。 |
| 狀態 State | 有序節點、鍵的重數、結構平衡資訊。 |
| 轉換 Transition | 查找與插刪後維護排序及平衡不變量。 |
| 計算順序 Order | 按鍵導航；range query 再沿序迭代。 |
| 正確性與終止 Correctness | 比較器須形成嚴格弱序；multiset 刪一項與刪所有同值需區分。 |
| 成本 Cost | 平衡樹查改 O(log n)，輸出 k 筆範圍 O(log n+k)。 |

來源：

- [C++ STL 容器的遍歷順序與有序性詳解](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Container_Iteration_Order.md)
- [C++ 資料結構選用心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Container_Selection_Guide.md)
- [動態排序容器選擇指南](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Advanced/Dynamic_Sorted_Container_Selection.md)

<a id="heap"></a>
### 115 · Binary Heap／Priority Queue／Heapify

來源深度：既有論述延伸

**關鍵論述：** 建堆的線性成本來自多數節點接近葉子，不能逐節點都算完整樹高。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 反覆取得當前最優先候選。 |
| 狀態 State | 完全二元樹的陣列表示與比較器。 |
| 轉換 Transition | 插入向上修復，取頂後向下修復。 |
| 計算順序 Order | 每次依極值優先；建堆由內部節點自底向上。 |
| 正確性與終止 Correctness | 父子 heap property 成立；不保證所有元素全排序。 |
| 成本 Cost | 看頂 O(1)、插入取出 O(log n)、Floyd 建堆 O(n)。 |

來源：

- [C++ STL: std::priorityqueue 使用詳解](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Priority_Queue_Usage.md)
- [C++ Priority Queue (Heap) 貪心策略通用模板](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/00-Priority_Queue_Greedy_Template.md)
- [Heap 使用場景的關鍵決策點](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/01-Heap_Decision_Making.md)
- [建堆 (Heapify) 的 O(N) 時間複雜度解析](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/05-Make_Heap_Complexity_Analysis.md)

<a id="top-k"></a>
### 116 · Bounded Heap／Top-K／Push–Pop

來源深度：既有論述延伸

**關鍵論述：** 目標只需要 k 個候選，所以不必保存所有輸入。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在資料流中保存前 k 大或前 k 小。 |
| 狀態 State | 最多 k 項的候選 heap，頂部為集合中最差者。 |
| 轉換 Transition | 新項較有利才替換，或先加入再移除最差者。 |
| 計算順序 Order | 逐項處理，結束後集合含前 k 項。 |
| 正確性與終止 Correctness | 每個前綴的 heap 都是該前綴最佳 k 項；平手策略需一致。 |
| 成本 Cost | O(nlog k)、O(k) 空間；建前 k 項可 O(k)。 |

來源：

- [心法：使用 Priority Queue 解決 Top-K 問題](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/02-Top_K_Problems.md)
- [心法：固定大小堆模式 (Fixed-Size Heap Pattern)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/03-Push_Pop_Fixed_Size_Heap.md)

<a id="twoheap-median"></a>
### 117 · Two-Heaps Balancing／Streaming Median

來源深度：既有論述延伸

**關鍵論述：** 兩堆保存秩的分界；同時需要「大小平衡」與「值域分離」。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 線上維護中位數。 |
| 狀態 State | 較小半部 max-heap、較大半部 min-heap。 |
| 轉換 Transition | 插入正確半部，再搬移堆頂修復大小差。 |
| 計算順序 Order | 每次更新後再查詢中位數。 |
| 正確性與終止 Correctness | 兩半大小差最多一，且左最大不大於右最小。 |
| 成本 Cost | 插入 O(log n)、查中位數 O(1)、空間 O(n)。 |

來源：

- [心法：雙堆平衡模式 (Two-Heaps Balancing Pattern)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/04-Two_Heaps_Balancing.md)

<a id="merge-k"></a>
### 118 · K-way Merge／Heap Frontier

來源深度：既有論述延伸

**關鍵論述：** 用每個來源一個代表壓縮搜尋前沿，避免一次把全部資料放入 heap。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 合併多個已排序來源或枚舉最小候選。 |
| 狀態 State | 每個來源目前前端的 heap 項，包含來源索引。 |
| 轉換 Transition | 取最小前端，再放入該來源的下一项。 |
| 計算順序 Order | 全局依 heap 順序，來源內依原次序。 |
| 正確性與終止 Correctness | 各來源前端是其剩餘極值，所有未處理項均被某前端代表。 |
| 成本 Cost | 總 N 項、k 來源為 O(Nlog k)、O(k) 輔助空間。 |

來源：

- [LeetCode Tricks and Keywords](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/LeetCode_Tricks_and_Keywords.md)
- [🎯 Technique Integration Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Technique_Integration_Problems.md)

<a id="monostack"></a>
### 119 · Monotonic Stack／Next Greater–Smaller

來源深度：既有論述延伸

**關鍵論述：** 單調性整理的是未解決問題的集合，不只是為了隨時讀一個最大值。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 為元素找最近邊界或等待下一個解答。 |
| 狀態 State | 按索引順序排列的未完成候選，值維持單調。 |
| 轉換 Transition | 新項使部分舊項得出答案，或令其失去候選資格而 pop。 |
| 計算順序 Order | 單向掃描，每項入棧至多一次。 |
| 正確性與終止 Correctness | pop 的意義依題型是「答案已完成」或「已被支配」，需分開證明。 |
| 成本 Cost | 總 O(n)、O(n) 空間；單步可 O(n) 但總出入有限。 |

來源：

- [資料結構：單調棧與單調隊列 (Monotonic Stack & Queue)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Stacks_and_Queues/Monotonic_Stacks/01-Monotonic_Stack_and_Queue.md)
- [單調棧：搜尋空間轉換 / Monotonic Stack Search Space Conversion](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Stacks_and_Queues/Monotonic_Stacks/02-Search_Space_Conversion.md)

<a id="monoqueue"></a>
### 120 · Monotonic Deque／Window Extremum

來源深度：既有論述延伸

**關鍵論述：** 過期與支配是兩種不同刪除原因，兩端各負責一種。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在滑動範圍內維護極值或有利前綴候選。 |
| 狀態 State | 依索引排列且值單調的候選 deque。 |
| 轉換 Transition | 隊尾移除被支配者，隊首移除過期者或已完成者。 |
| 計算順序 Order | 窗口向右前進，極值通常讀隊首。 |
| 正確性與終止 Correctness | 新者值更好且更晚過期，才可支配舊者；其他題型需重證條件。 |
| 成本 Cost | 各項一次入出時 O(n)，空間 O(k) 或 O(n)。 |

來源：

- [🎯 Technique Integration Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Technique_Integration_Problems.md)
- [資料結構：單調棧與單調隊列 (Monotonic Stack & Queue)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Stacks_and_Queues/Monotonic_Stacks/01-Monotonic_Stack_and_Queue.md)

<a id="stack-boundary"></a>
### 121 · Stack Internal Search／三索引邊界

來源深度：既有論述延伸

**關鍵論述：** stack 的剩餘內容是可查詢的邊界索引庫。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 利用左右邊界和被彈出元素計算貢獻。 |
| 狀態 State | current、popped、pop 後的新 top。 |
| 轉換 Transition | 彈出中間元素後，以殘留 top 作另一側邊界。 |
| 計算順序 Order | 當新項形成邊界時結算，結尾可用哨兵清算。 |
| 正確性與終止 Correctness | 寬度與嚴格／非嚴格比較决定重複值的歸屬，避免漏算或重算。 |
| 成本 Cost | 典型 O(n)、O(n) 空間。 |

來源：

- [單調棧：內部搜尋空間 / Stack Internal Search Pattern](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Stacks_and_Queues/Monotonic_Stacks/03-Stack_Internal_Search.md)

<a id="bst"></a>
### 122 · Binary Search Tree／Inorder／Duplicates

來源深度：既有論述延伸

**關鍵論述：** 有序性允許整棵子樹被排除，但對數成本還需要高度保證。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 維護可按鍵導航的階層結構。 |
| 狀態 State | 節點鍵、左右子樹與明確的重複值規則。 |
| 轉換 Transition | 比較後選子樹；插刪重接但維持區間契約。 |
| 計算順序 Order | 查詢走單一路徑；inorder 產生有序序列。 |
| 正確性與終止 Correctness | 左、根、右的全子樹約束成立；僅比較直接孩子不夠。 |
| 成本 Cost | 操作 O(h)，退化 h=n；inorder O(n)、stack O(h)。 |

來源：

- [BST 核心操作與屬性](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Search_Trees/01-Core_Operations_and_Properties.md)
- [BST 解題心法：利用 In-order Traversal 的有序性](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Search_Trees/02-In-order_Traversal_Strategy.md)
- [關於 BST 中重複值的討論](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Search_Trees/Duplicates_in_BST.md)

<a id="avl"></a>
### 123 · AVL Tree

來源深度：清單／提及延伸

**關鍵論述：** 在表示中加入可局部維護的高度限制，避免搜尋路徑退化。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 給搜尋樹最壞對數高度保證。 |
| 狀態 State | BST 節點、高度或平衡因子。 |
| 轉換 Transition | 插刪後更新高度，使用單／雙旋轉修復失衡。 |
| 計算順序 Order | 沿變更路徑向上修復。 |
| 正確性與終止 Correctness | 每節點左右高度差最多一，旋轉保持 inorder 順序。 |
| 成本 Cost | 查改最壞 O(log n)、空間 O(n)。 |

來源：

- [Augmented BST for Order Statistics 心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Search_Trees/Augmented_BST_for_Order_Statistics.md)
- [Height-Balanced BST 解題心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Height_Balanced_BST.md)

<a id="red-black"></a>
### 124 · Red–Black Tree

來源深度：清單／提及延伸

**關鍵論述：** 顏色是控制結構高度的摘要；不要求每節點左右高度差最多一。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 以較寬鬆平衡規則維護有序集合。 |
| 狀態 State | BST 結構與紅黑顏色。 |
| 轉換 Transition | 插刪後旋轉、重新著色以恢復規則。 |
| 計算順序 Order | 沿局部受影響路徑修復。 |
| 正確性與終止 Correctness | 無相鄰紅節點且到空葉黑高度一致，導出對數高度。 |
| 成本 Cost | 查改最壞 O(log n)、空間 O(n)。 |

來源：

- [Augmented BST for Order Statistics 心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Search_Trees/Augmented_BST_for_Order_Statistics.md)
- [Height-Balanced BST 解題心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Height_Balanced_BST.md)

<a id="splay"></a>
### 125 · Splay Tree

來源深度：清單／提及延伸

**關鍵論述：** 保證落在整段操作序列，不能聲稱每次都有最壞對數時間。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 讓存取具有自調整效果的搜尋樹。 |
| 狀態 State | BST 連結與目前存取路徑。 |
| 轉換 Transition | 以 zig、zig-zig、zig-zag 把存取節點移到根。 |
| 計算順序 Order | 每次存取後沿路徑旋轉。 |
| 正確性與終止 Correctness | 旋轉保持鍵順序；成本由勢能攤銷證明，不靠永久平衡。 |
| 成本 Cost | 每操作攤銷 O(log n)，單次最壞 O(n)，空間 O(n)。 |

來源：

- [Height-Balanced BST 解題心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Height_Balanced_BST.md)

<a id="treap"></a>
### 126 · Treap

來源深度：清單／提及延伸

**關鍵論述：** 用隨機控制資訊維持良好形狀，與 AVL 的確定性保證不同。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 結合鍵順序與隨機平衡。 |
| 狀態 State | 節點鍵與獨立隨機優先級。 |
| 轉換 Transition | 依鍵插入，再旋轉或 split/merge 維持 heap 次序。 |
| 計算順序 Order | 鍵控制搜尋，優先級控制形狀。 |
| 正確性與終止 Correctness | 同時保持 BST 與 heap 性質；期望界需隨机優先級假設。 |
| 成本 Cost | 查改期望 O(log n)，最壞 O(n)，空間 O(n)。 |

來源：

- [Height-Balanced BST 解題心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Height_Balanced_BST.md)

<a id="ost"></a>
### 127 · Augmented BST／Order Statistic Tree

來源深度：既有論述延伸

**關鍵論述：** 增加一份可組合摘要，讓「數過多少元素」變成直接跳過子樹。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 支援動態第 k 小／大與 rank 查詢。 |
| 狀態 State | BST 與各子樹大小，重複值可另存 multiplicity。 |
| 轉換 Transition | 依子樹大小選方向並調整剩餘秩。 |
| 計算順序 Order | 單一路徑導航；插刪和旋轉後更新 metadata。 |
| 正確性與終止 Correctness | size 等於子樹元素總數；局部 rank 需加祖先方向的偏移。 |
| 成本 Cost | O(h)，平衡後 O(log n)，空間 O(n)。 |

來源：

- [Augmented BST for Order Statistics 心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Search_Trees/Augmented_BST_for_Order_Statistics.md)

<a id="tree-structure"></a>
### 128 · Binary／N-ary／Complete／Perfect Tree

來源深度：既有論述延伸

**關鍵論述：** 結構限制本身提供可省略的狀態；轉成雙向圖後必須排除回走父邊。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 表達階層關係與子問題分解。 |
| 狀態 State | 節點、孩子集合、父關係或陣列索引表示。 |
| 轉換 Transition | 沿孩子或父方向移動，必要時把樹轉為無向圖。 |
| 計算順序 Order | 前中後序或層序；N 元樹迭代需保存孩子進度。 |
| 正確性與終止 Correctness | 樹無環且連通；complete/perfect 的形狀不能套到一般樹。 |
| 成本 Cost | 走訪 O(n)，DFS O(h)、BFS O(w) 輔助空間；h 最壞 n。 |

來源：

- [Binary Tree Traversal](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Trees/Binary_Tree_Traversal.md)
- [Perfect Binary Tree（完美二元樹）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Trees/Perfect_Binary_Tree.md)
- [N-ary Tree 解題心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/N-ary_Tree.md)
- [將 Tree 問題轉換為等價 Graph 解法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Tree_As_Equivalent_Graph.md)

<a id="path-aggregation"></a>
### 129 · Path-Based Aggregation／Ancestor Constraints

來源深度：既有論述延伸

**關鍵論述：** 傳遞的是與未來判斷相關的祖先資訊，而不必傳整條歷史。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 沿祖先鏈維護條件與路徑摘要。 |
| 狀態 State | 目前節點、祖先範圍、極值、計數或必要路徑容器。 |
| 轉換 Transition | 父摘要加入本節點後傳给孩子。 |
| 計算順序 Order | 通常前序傳遞；共享可變容器在返回時復原。 |
| 正確性與終止 Correctness | 摘要必須對應正確 root-to-node 路徑；答案不一定只在葉節點更新。 |
| 成本 Cost | 摘要常數大小時 O(n)、O(h)；完整路徑複製可能更貴。 |

來源：

- [🌲 Path-Based Thinking & Aggregation in Tree Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Path_Based_Thinking_Aggregation.md)

<a id="lca"></a>
### 130 · LCA／子樹見證聚合

來源深度：既有論述延伸

**關鍵論述：** 返回值是一份「子樹內找到什麼」的見證摘要。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 尋找目標節點共同的最低祖先。 |
| 狀態 State | 當前子樹、目標存在性與局部候選。 |
| 轉換 Transition | 聚合左右是否含目標；BST 可利用鍵區間縮小。 |
| 計算順序 Order | 一般樹後序；BST 可單一路徑。 |
| 正確性與終止 Correctness | 是否保證目標存在需明確；存在性不足時不能直接回傳某個找到的目標。 |
| 成本 Cost | 一般單次 O(n)、O(h) stack；BST O(h)。 |

來源：

- [樹狀遞迴設計心法：從基本結構到優雅解](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Recursive_Design_Pattern_Pruning_and_Aggregation.md)
- [Problem Transformation Framework](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Transformation.md)

<a id="morris"></a>
### 131 · Morris Traversal

來源深度：既有論述延伸

**關鍵論述：** 控制資訊仍存在，只是從外部 stack 搬到了輸入結構內。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 以常數額外空間遍歷二元樹。 |
| 狀態 State | 目前節點與寫入空指標的臨時返回線索。 |
| 轉換 Transition | 第一次建立 thread，第二次沿 thread 返回並移除。 |
| 計算順序 Order | 以樹內暫存連結模擬 inorder 返回。 |
| 正確性與終止 Correctness | 每條臨時連結最後都復原；中途提前退出須處理尚存 thread。 |
| 成本 Cost | O(n) 時間、O(1) 額外空間，不計輸出。 |

來源：

- [Morris Traversal for Inorder](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Morris_Traversal.md)

<a id="dfs-level"></a>
### 132 · DFS + Depth Bucketing

來源深度：既有論述延伸

**關鍵論述：** 計算順序與輸出排列可以分離，輸出像 BFS 不代表過程是 BFS。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 產生按層分組的結果。 |
| 狀態 State | DFS 位置、depth 與按 depth 存放的輸出容器。 |
| 轉換 Transition | 走訪節點時寫入其深度所屬桶。 |
| 計算順序 Order | 實際是 DFS 次序，最後容器呈現層序分組。 |
| 正確性與終止 Correctness | 左到右走訪保留同層次序；DFS 不保證全局先淺層再深層。 |
| 成本 Cost | O(n) 時間、O(h) stack 加 O(n) 輸出。 |

來源：

- [使用 DFS + Preordering + Level 變數實作層序遍歷](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/DFS_for_Level_Order_Traversal.md)

<a id="canonical-tree"></a>
### 133 · Tree Canonical Form／Merkle Hashing

來源深度：既有論述延伸

**關鍵論述：** 正規化合併等價表示，但必須保留題目要求的全部結構差異。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 比較結構等價、識別重複子樹。 |
| 狀態 State | 節點值與完整子樹簽名或唯一編號。 |
| 轉換 Transition | 後序組合孩子簽名；若允許左右翻轉，可規範化孩子順序。 |
| 計算順序 Order | 孩子先完成，再產生父簽名。 |
| 正確性與終止 Correctness | 重複值時僅比較孩子根值不够；hash 相同需考慮碰撞。 |
| 成本 Cost | 以固定長度 ID intern 常見期望 O(n)；完整字串拼接可退化 O(n²)。 |

來源：

- [解題 Follow-up 待辦清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Learning_Roadmap.md)
- [Binary Tree Canonical Forms 標準形式轉換 Playbook](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Trees/Canonical_Forms_Transformation.md)

<a id="serialization"></a>
### 134 · Tree Serialization／Deserialization

來源深度：清單／提及延伸

**關鍵論述：** 狀態表示是否可逆，取決於是否保存足以辨別結構的界線。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 可逆保存與重建樹。 |
| 狀態 State | 遍歷游標、節點值、空子樹標記或長度／孩子數。 |
| 轉換 Transition | 依約定語法輸出，再按同一語法消耗與重建。 |
| 計算順序 Order | 前序或層序等固定順序。 |
| 正確性與終止 Correctness | 表示必須無歧義，重複值與空結構不可丟失。 |
| 成本 Cost | O(n) 節點操作，實際字串成本依輸出長度。 |

來源：

- [🎯 Technique Integration Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Technique_Integration_Problems.md)

<a id="bst-iterator"></a>
### 135 · BST Iterator／受控遍歷

來源深度：清單／提及延伸

**關鍵論述：** 把一次性遍歷暫停成可恢復的狀態，按需求分批計算。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 按需提供下一個有序元素。 |
| 狀態 State | 尚未完成的左鏈 stack 或預先展平的陣列位置。 |
| 轉換 Transition | 取下個元素，再展開其右子樹的左鏈。 |
| 計算順序 Order | 每次 next 只推進必要的 inorder 工作。 |
| 正確性與終止 Correctness | stack 頂部是下一個尚未輸出的節點。 |
| 成本 Cost | 惰性版 next 攤銷 O(1)、最壞 O(h)、空間 O(h)；展平版 O(n) 空間。 |

來源：

- [LeetCode Tricks and Keywords](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/LeetCode_Tricks_and_Keywords.md)

<a id="trie"></a>
### 136 · Trie／Prefix Tree／Bitwise Trie

來源深度：既有論述延伸

**關鍵論述：** 把共同前綴實體化，讓許多字串共享同一段查詢工作。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 按前綴查字串，或按位元導航 XOR 候選。 |
| 狀態 State | 前綴節點、字元／位元分支、終止標記與 metadata。 |
| 轉換 Transition | 逐符號走邊，插入缺少分支；查詢按條件選分支。 |
| 計算順序 Order | 字串順序或位元由高到低。 |
| 正確性與終止 Correctness | 到達節點只代表前綴存在，完整詞需終止標記；XOR 貪婪需位權證明。 |
| 成本 Cost | 總字元 L 建構 O(L)，單次查詢 O(字長)；分支容器成本另計。 |

來源：

- [Trie (前綴樹) 實作與分析](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trie/01_Trie_Core_Concepts_and_Implementation.md)
- [Trie (字典樹) 使用心法與設計模式](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trie/02_Trie_Design_Patterns_and_Usage.md)
- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)

<a id="dynamic-trie"></a>
### 137 · Dynamic Trie／Backtracking + Trie

來源深度：清單／提及延伸

**關鍵論述：** 資料結構也能隨答案完成而縮小，前提是其資訊確實不再需要。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 搜尋多個模式並減少已無用途的分支。 |
| 狀態 State | Trie 計數／終止標記，另有搜尋路徑 visited。 |
| 轉換 Transition | 匹配延伸；結果可去重後清標記，空分支才可移除。 |
| 計算順序 Order | DFS 跟隨 Trie 前綴；每條路徑維護獨立使用限制。 |
| 正確性與終止 Correctness | 刪除不得影響尚未找到的單字或未來查詢；多重次數需求另存。 |
| 成本 Cost | 仍可能有指數搜尋分支；Trie 減少無效前綴，不保證線性。 |

來源：

- [LeetCode Tricks and Keywords](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/LeetCode_Tricks_and_Keywords.md)
- [算法技巧清單 (Algorithm Techniques Checklist)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Algorithm_Techniques_Checklist.md)
- [Trie (字典樹) 使用心法與設計模式](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trie/02_Trie_Design_Patterns_and_Usage.md)

<a id="dsu"></a>
### 138 · Union-Find／Disjoint Set Union

來源深度：既有論述延伸

**關鍵論述：** DSU 摘要的是等價類，常規版本不支持任意刪邊後拆分。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 維護逐步合併的連通分量。 |
| 狀態 State | 代表元、parent、size/rank 與分量數。 |
| 轉換 Transition | find 查代表，union 合併不同代表。 |
| 計算順序 Order | 通常按新邊或關係事件處理；需要列群組時最後按代表分桶。 |
| 正確性與終止 Correctness | 代表相同等價於目前已加入關係下連通；不保存原路徑。 |
| 成本 Cost | rank/size 加壓縮為攤銷 O(α(n)) 每操作；儲存 O(n)。 |

來源：

- [Disjoint Set (Union-Find) - 核心概念](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/01-Core_Concepts.md)
- [Ultimate Design: Path Compression + Union by Rank](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/06-Optimized_Implementation_and_Analysis.md)
- [Union-Find 解題技巧](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/07-LeetCode_Tips.md)
- [連通性問題的演算法選擇策略：DFS/BFS vs. Disjoint Set](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/08-Connectivity_Problem_Strategy_Guide.md)
- [心法：從並查集還原連通分量 (Reconstructing Connected Components)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/09-Reconstructing_Connected_Components.md)

<a id="quick-find"></a>
### 139 · Quick-Find

來源深度：既有論述延伸

**關鍵論述：** 把更新工作預先做到全部成員，換取查詢便宜。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 用直接分量標籤支持常數查詢。 |
| 狀態 State | 每元素保存其當前分量 ID。 |
| 轉換 Transition | 合併時掃描所有元素，替換其中一組 ID。 |
| 計算順序 Order | 關係逐次加入。 |
| 正確性與終止 Correctness | 同分量元素始終擁有同一標籤。 |
| 成本 Cost | find O(1)、union O(n)、空間 O(n)。 |

來源：

- [Design 1: Quick Find](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/02-Quick_Find.md)

<a id="quick-union"></a>
### 140 · Quick-Union

來源深度：既有論述延伸

**關鍵論述：** 用間接表示省掉整組重標，但成本可能轉移到日後查詢。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 透過代表樹延後分量標籤的更新。 |
| 狀態 State | parent 森林。 |
| 轉換 Transition | 沿 parent 找根，合併時接上一個根。 |
| 計算順序 Order | 查詢時才沿鏈解析代表。 |
| 正確性與終止 Correctness | 根代表分量，合併只能連接不同根。 |
| 成本 Cost | 未平衡時單次 O(n)，空間 O(n)。 |

來源：

- [Design 2: Quick Union](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/03-Quick_Union.md)

<a id="union-rank"></a>
### 141 · Union by Rank／Size

來源深度：既有論述延伸

**關鍵論述：** 把合併方向變成成本控制，避免任意接鏈造成退化。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 限制 DSU 代表樹增長。 |
| 狀態 State | parent 加 rank 或 size。 |
| 轉換 Transition | 把較矮或較小的根接到另一根。 |
| 計算順序 Order | 每次 union 前先找根並比較 metadata。 |
| 正確性與終止 Correctness | 未壓縮時節點深度增加意味所屬集合至少倍增。 |
| 成本 Cost | 單獨使用時 find O(log n)，空間 O(n)。 |

來源：

- [Design 3: Union by Rank Optimization](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/04-Union_by_Rank.md)

<a id="path-compression"></a>
### 142 · Path Compression

來源深度：既有論述延伸

**關鍵論述：** 一次查詢的結果可回寫結構，讓後續同類工作更便宜。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 加速後續代表元查詢。 |
| 狀態 State | find 路徑與根。 |
| 轉換 Transition | 找到根後把沿途 parent 改指向更近根的位置。 |
| 計算順序 Order | 查詢時順便修正表示。 |
| 正確性與終止 Correctness | 只縮短同分量內部路徑，不改變分量身份；rank 不再等於真實高度。 |
| 成本 Cost | 與 rank/size 合用才採常見 O(α(n)) 攤銷界。 |

來源：

- [Design 4: Path Compression Optimization](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/05-Path_Compression.md)

<a id="weighted-dsu"></a>
### 143 · Weighted Union-Find／Potential DSU

來源深度：既有論述延伸

**關鍵論述：** 代表元之外再保存可組合的相對量，便能回答超過布林連通性的查詢。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 維護實體間比值、差值或相對關係。 |
| 狀態 State | parent 與節點相對父節點的權重。 |
| 轉換 Transition | 壓縮時組合權重；合併根時推導根間關係。 |
| 計算順序 Order | 沿 find 路徑先解析父關係再更新目前權重。 |
| 正確性與終止 Correctness | 權重方向始終一致；矛盾關係與浮點誤差需明確處理。 |
| 成本 Cost | 常數權重運算下與優化 DSU 同階，空間 O(n)。 |

來源：

- [加權並查集與路徑壓縮 (Weighted Union-Find with Path Compression)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/10-Weighted_Union_Find_with_Path_Compression.md)

<a id="fenwick"></a>
### 144 · Fenwick Tree／Binary Indexed Tree

來源深度：既有論述延伸

**關鍵論述：** 保存有重疊但精心安排的摘要，讓每次查改只碰對數個區塊。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 支援動態前綴和及區間和。 |
| 狀態 State | 按 lowbit 分解的區塊摘要。 |
| 轉換 Transition | 更新沿包含該點的區塊傳播；查詢拼接互斥前綴區塊。 |
| 計算順序 Order | 索引以 lowbit 跳躍，通常採 1-based。 |
| 正確性與終止 Correctness | 各節點摘要對應固定區間；區間和相減需要可逆聚合。 |
| 成本 Cost | 建構可 O(n)，更新與查詢 O(log n)，空間 O(n)。 |

來源：

- [Binary Indexed Tree (Fenwick Tree) 核心概念](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Advanced/Binary_Indexed_Tree/01-Core_Concepts.md)
- [Binary Indexed Tree 實作版本](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Advanced/Binary_Indexed_Tree/02-Implementations.md)

<a id="segment-tree"></a>
### 145 · Segment Tree

來源深度：清單／提及延伸

**關鍵論述：** 以區間分解避免掃描每個元素，比前綴相減適用更多聚合運算。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 支持動態區間聚合。 |
| 狀態 State | 區間樹與每節點的 sum/min/max 等摘要。 |
| 轉換 Transition | 更新葉子後回算祖先；查詢拆成若干完整覆蓋區間。 |
| 計算順序 Order | 自頂向下定位，自底向上聚合。 |
| 正確性與終止 Correctness | 合併運算具結合性與正確單位元；不必支持逆運算。 |
| 成本 Cost | 常數摘要下建樹 O(n)，點改與區間查 O(log n)，空間 O(n)。 |

來源：

- [算法技巧清單 (Algorithm Techniques Checklist)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Algorithm_Techniques_Checklist.md)
- [Binary Indexed Tree (Fenwick Tree) 核心概念](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Advanced/Binary_Indexed_Tree/01-Core_Concepts.md)
- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)

<a id="lazy-segment"></a>
### 146 · Lazy Propagation

來源深度：清單／提及延伸

**關鍵論述：** 把尚未執行的計算本身表示成狀態。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 使整段更新不必立即下達每個葉子。 |
| 狀態 State | 區間摘要加尚未下推的操作標記。 |
| 轉換 Transition | 完整覆蓋時更新摘要並合成標記，必要時才下推。 |
| 計算順序 Order | 延遲到子區間被查詢或修改時展開。 |
| 正確性與終止 Correctness | 標記組合順序需正確，且能由區間長度等資訊更新摘要。 |
| 成本 Cost | 標準可合成操作的區間改查 O(log n)；不是任意更新皆能如此。 |

來源：

- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)
- [LeetCode 高階心法（完整 MD + 一頁式速查表）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/04-Advanced_Problem_Solving_Cheatsheet.md)

<a id="sqrt-decomp"></a>
### 147 · Sqrt Decomposition／分塊

來源深度：清單／提及延伸

**關鍵論述：** 選擇中等粒度的摘要，避開全展開與全局重算兩端。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 折衷預處理與區間查改成本。 |
| 狀態 State | 原始資料與每塊摘要。 |
| 轉換 Transition | 完整區塊直接用摘要，邊角逐元素處理。 |
| 計算順序 Order | 按塊處理，更新時只修受影響區塊。 |
| 正確性與終止 Correctness | 塊摘要必須反映資料；是否支持逆操作影响更新成本。 |
| 成本 Cost | 常見塊大小 √n，查詢 O(√n)；加總點改可 O(1)。 |

來源：

- [Binary Indexed Tree (Fenwick Tree) 核心概念](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Advanced/Binary_Indexed_Tree/01-Core_Concepts.md)
- [LeetCode 高階心法（完整 MD + 一頁式速查表）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/04-Advanced_Problem_Solving_Cheatsheet.md)

<a id="mo"></a>
### 148 · Mo's Algorithm／離線窗口重排

來源深度：清單／提及延伸

**關鍵論述：** 不改變每個查詢的答案，而是改變計算順序以共享中間狀態。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 減少大量靜態區間查詢之間的狀態搬移。 |
| 狀態 State | 目前區間、可增刪摘要與原查詢 ID。 |
| 轉換 Transition | 將窗口移到下一筆查詢範圍。 |
| 計算順序 Order | 按左端分塊與右端排序，可奇偶反向。 |
| 正確性與終止 Correctness | 重排不影響各查詢語義；需能正確加入與移除元素。 |
| 成本 Cost | 標準塊寬 √n，約 O((n+q)√n) 次指標移動，另乘增刪成本。 |

來源：

- [LeetCode 高階心法（完整 MD + 一頁式速查表）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/04-Advanced_Problem_Solving_Cheatsheet.md)

<a id="graph-representation"></a>
### 149 · Edge List／Adjacency List／Matrix／Grid

來源深度：既有論述延伸

**關鍵論述：** 抽象上同一張圖，換表示就會改變實際搜尋與更新成本。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 按主要操作選擇圖的儲存方式。 |
| 狀態 State | 點、邊身份、權重、方向；grid 可只保存格子與鄰居規則。 |
| 轉換 Transition | 掃描所有邊、列舉鄰居，或查兩點是否相鄰。 |
| 計算順序 Order | 由主算法決定，表示會影響每次轉移成本。 |
| 正確性與終止 Correctness | 無向邊可能存兩次；多重邊不可無條件去重，矩陣須定義聚合語義。 |
| 成本 Cost | list O(V+E) 空間、列鄰居 O(deg)；matrix O(V²)、查邊 O(1)。 |

來源：

- [圖的表示法 (2): 鄰接列表](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Adjacency_List_Representation.md)
- [圖的表示法 (1): 邊列表與邊集合](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Edge_List_Representation.md)
- [圖論問題解題關鍵概念](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Graph_Problem_Solving_From_Leetcode.md)
- [通用 Graph 解題邏輯](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Graph_Problem_Solving_Principles.md)
- [格狀圖（Lattice Graph / Grid Graph）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Lattice_Graph.md)
- [圖 (Graph) 的表示與遍歷](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/README.md)

<a id="swap-delete"></a>
### 150 · Swap-to-End／Randomized Set

來源深度：既有論述延伸

**關鍵論述：** 放棄順序需求後，搬移一項就足以取代整段位移。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 同時支持隨機讀取與快速刪除。 |
| 狀態 State | 連續 vector 與值到索引的 map。 |
| 轉換 Transition | 待刪項與尾項交換，同步修 map 後刪尾。 |
| 計算順序 Order | 每次修改後立刻恢復雙向映射。 |
| 正確性與終止 Correctness | 元素順序不重要；重複值需值到索引集合而非單一位置。 |
| 成本 Cost | 唯一值版增刪期望 O(1)，均勻索引抽樣 O(1)，空間 O(n)。 |

來源：

- [Vector O(1) 刪除：Swap-to-End 技巧](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/Vector_O1_Deletion_Swap_to_End.md)

<a id="lru"></a>
### 151 · LRU Cache

來源深度：清單／提及延伸

**關鍵論述：** 一份索引回答「在哪」，一份順序回答「誰最久沒用」。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 以最近使用時間决定淘汰。 |
| 狀態 State | 鍵到節點的 hash map、雙向串列與容量。 |
| 轉換 Transition | 命中或寫入把節點移到最近端，超量淘汰最舊端。 |
| 計算順序 Order | 按請求時間維護順序。 |
| 正確性與終止 Correctness | map 與串列一一對應，串列順序反映最近使用次序。 |
| 成本 Cost | 平均 O(1) 每操作，空間 O(capacity)。 |

來源：

- [LeetCode Tricks and Keywords](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/LeetCode_Tricks_and_Keywords.md)
- [🎯 Technique Integration Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Technique_Integration_Problems.md)

<a id="lfu"></a>
### 152 · LFU Cache

來源深度：清單／提及延伸

**關鍵論述：** 多個摘要共同描述淘汰優先級，更新時必須原子地維持彼此一致。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 先依頻率、再依近期程度淘汰。 |
| 狀態 State | 鍵索引、頻率桶串列、最低頻率。 |
| 轉換 Transition | 每次使用把節點移到下一頻率桶，維護最低非空桶。 |
| 計算順序 Order | 請求順序更新，同頻桶內保持 LRU 次序。 |
| 正確性與終止 Correctness | 頻率與桶一致，minFreq 指向真正最低頻率。 |
| 成本 Cost | 標準 hash+雙向串列設計平均 O(1)，空間 O(capacity)。 |

來源：

- [🎯 Technique Integration Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Technique_Integration_Problems.md)

<a id="minmax-heap"></a>
### 153 · Min-Max Heap

來源深度：清單／提及延伸

**關鍵論述：** 用一個結構同時維護兩個極值方向，不等同於中位數雙堆。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 同時快速取得最小與最大元素。 |
| 狀態 State | 完全二元樹，層級交替保存 min／max 約束。 |
| 轉換 Transition | 沿同類層祖父或子孫修復插刪後的關係。 |
| 計算順序 Order | 依節點所在層決定上浮或下沉規則。 |
| 正確性與終止 Correctness | min 層小於其後代、max 層大於其後代。 |
| 成本 Cost | 兩端查詢 O(1)，插入與刪端 O(log n)，空間 O(n)。 |

來源：

- [解題 Follow-up 待辦清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Learning_Roadmap.md)
- 補充核對：[Sartaj Sahni：雙端優先佇列背景](https://www.cise.ufl.edu/~sahni/dsaac/enrich/c13/double.htm)

<a id="deap"></a>
### 154 · Deap／Double-Ended Heap

來源深度：清單／提及延伸

**關鍵論述：** 除了兩側自己的次序，還要保存跨側關係才能保證全局兩端極值。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在同一完全樹形布局支持雙端優先佇列。 |
| 狀態 State | 空根、左 min-heap、右 max-heap 與對應關係。 |
| 轉換 Transition | 插入先檢查左右對應，再於適合的一側修復。 |
| 計算順序 Order | 依兩側 heap 與 correspondence 規則更新。 |
| 正確性與終止 Correctness | 左側對應項不大於右側；沒有直接對應項時依規則找替代對應。 |
| 成本 Cost | 兩端查詢 O(1)，插入刪端 O(log n)，空間 O(n)。 |

來源：

- [解題 Follow-up 待辦清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Learning_Roadmap.md)
- 補充核對：[Sartaj Sahni：雙端優先佇列背景](https://www.cise.ufl.edu/~sahni/dsaac/enrich/c13/double.htm)


<a id="chapter-9"></a>
## 數學與表示

<a id="bitwise"></a>
### 155 · Bit Manipulation／Bitmask Set／Bitset

來源深度：既有論述延伸

**關鍵論述：** 並行處理多個布林資訊可以降低操作成本，狀態數目可能完全不變。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 以位元表示集合、旗標與奇偶特性。 |
| 狀態 State | 固定寬度位元串，每一位對應成員或局部資訊。 |
| 轉換 Transition | AND/OR/XOR、移位、清最低設定位等操作。 |
| 計算順序 Order | 逐位、逐設定位，或整個 machine word 同步處理。 |
| 正確性與終止 Correctness | 位寬、符號與位移範圍需合法；位元打包不代表可合併不同集合。 |
| 成本 Cost | 單 word 常 O(1)；B 位 bitset 操作約 O(⌈B/w⌉)。 |

來源：

- [位元操作 (Bit Manipulation) Playbook](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Bit_Manipulation/01-Bit_Manipulation_Playbook.md)
- [Bitmask 集合運算](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Bit_Manipulation/02-Bitmask_Set_Operations.md)
- [⚠️ Sign Extension 陷阱](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Bit_Manipulation/05-Sign_Extension_Trap.md)
- [C++ STL 中的位元運算](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Bit_Manipulation/06-Bit_Manipulation_CPP_STL.md)
- [Bit Shift UB 地雷](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Bit_Manipulation/99-Case_Shift_UB_Pitfall.md)

<a id="bit-add"></a>
### 156 · Bitwise Addition

來源深度：既有論述延伸

**關鍵論述：** 把算術拆成兩個可局部更新的狀態，直到未完成工作為空。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 以位元規則實現固定寬度加法。 |
| 狀態 State | 未進位的和與待傳播進位。 |
| 轉換 Transition | XOR 合成無進位和，交集產生下一位進位。 |
| 計算順序 Order | 反覆傳播直到進位消失。 |
| 正確性與終止 Correctness | 固定無符號位寬下保存模 2^w 的總和；signed overflow 不可假設合法。 |
| 成本 Cost | 最壞 O(w) 輪、O(1) machine words。 |

來源：

- [位元加法 (Bitwise Addition)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Bit_Manipulation/99-Case_Bitwise_Addition.md)

<a id="gcd"></a>
### 157 · Euclidean Algorithm／GCD／LCM

來源深度：既有論述延伸

**關鍵論述：** 典型的狀態等價縮小：數字變小，但所求的共同因子資訊不變。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 計算共同因子、共同周期或化簡比例。 |
| 狀態 State | 兩個非負整數與當前餘數。 |
| 轉換 Transition | 以較小數與除法餘數取代原數對。 |
| 計算順序 Order | 餘數嚴格縮小直至零；LCM 先除 GCD 再乘。 |
| 正確性與終止 Correctness | 共同因子集合在每次餘數替換後不變。 |
| 成本 Cost | 單次 GCD O(log min(a,b)) 次除法；整數位元成本另計。 |

來源：

- [數論實用工具：GCD 與 LCM](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Number_Theory/03-GCD_and_LCM.md)
- [數論應用：LeetCode 實戰模式](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Number_Theory/04-Number_Theory_Applications.md)

<a id="prime-test"></a>
### 158 · Trial Division／Primality Test

來源深度：既有論述延伸

**關鍵論述：** 利用因數對稱性，省掉一半以上的候選範圍。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 判定一個整數是否為質數。 |
| 狀態 State | 待測數與尚未排除的因數範圍。 |
| 轉換 Transition | 測試因數並排除，找到整除者即停止。 |
| 計算順序 Order | 只需測至平方根，可略過已知不可能因數。 |
| 正確性與終止 Correctness | 合數必有至少一個不大於平方根的非平凡因數。 |
| 成本 Cost | O(√N) 次試除、O(1) 空間。 |

來源：

- [數論基礎：質數判斷](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Number_Theory/01-Primality_Test.md)

<a id="factorization"></a>
### 159 · Prime Factorization／Divisor Count–Sum

來源深度：既有論述延伸

**關鍵論述：** 完整因數集合可由少量質因數與次數生成，不必一個個枚舉。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 取得質因數分解並計算因數統計。 |
| 狀態 State | 尚未分解的餘數、候選質因子及其指數。 |
| 轉換 Transition | 整除時反覆取出因子，再處理剩餘值。 |
| 計算順序 Order | 候選由小到大；測至目前餘數的平方根。 |
| 正確性與終止 Correctness | 已取因子乘剩餘值等於原數；結束時大於一的餘數為質數。 |
| 成本 Cost | 試除最壞 O(√N)；因數數量/和可由指數摘要組合。 |

來源：

- [數論核心：質因數分解](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Number_Theory/02-Prime_Factorization.md)
- [數論應用：LeetCode 實戰模式](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Number_Theory/04-Number_Theory_Applications.md)

<a id="sieve"></a>
### 160 · Sieve of Eratosthenes

來源深度：清單／提及延伸

**關鍵論述：** 一次標記整個倍數集合，讓多筆質數判定共享工作。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 批次取得上界內所有質數。 |
| 狀態 State | 候選布林表、當前質數與其倍數。 |
| 轉換 Transition | 將質數的倍數標為合數。 |
| 計算順序 Order | 由小到大，通常從 p² 開始標記。 |
| 正確性與終止 Correctness | 較小倍數已由較小質因子處理；未被標記者在掃描時為質數。 |
| 成本 Cost | O(Nlog log N) 時間、O(N) 空間。 |

來源：

- [數論基礎：質數判斷](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Number_Theory/01-Primality_Test.md)
- [📘 DSA Design Pattern Roadmap](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/01-Interview_Timing_Framework.md)

<a id="modular"></a>
### 161 · Modular Arithmetic／餘數狀態

來源深度：既有論述延伸

**關鍵論述：** 這是按目標建立的等價類壓縮，前提是後續操作尊重同餘關係。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 只保存題目所需的模數結果。 |
| 狀態 State | 各值在模 M 下的等價類。 |
| 轉換 Transition | 每次加減乘後正規化餘數。 |
| 計算順序 Order | 跟隨原依賴順序，先確保中間運算不溢位。 |
| 正確性與終止 Correctness | 加減乘保留同餘；大小比較與一般除法不直接保留。 |
| 成本 Cost | 固定寬度安全運算常 O(1)；大整數依位數計。 |

來源：

- [模組化算術在程式設計中的實用指南](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Modular_Arithmetic_A_Practical_Guide.md)

<a id="fast-power"></a>
### 162 · Fast Power／Binary Exponentiation

來源深度：清單／提及延伸

**關鍵論述：** 把多次相同轉換先合成大步，一次跳過成批計算。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 加速重複乘法或可結合操作。 |
| 狀態 State | 目前底數冪、剩餘指數、累積結果。 |
| 轉換 Transition | 指數奇數時合入結果，底數平方，指數折半。 |
| 計算順序 Order | 按指數二進位處理。 |
| 正確性與終止 Correctness | 累積結果與剩餘冪的乘積始終等於目標；運算須具結合性。 |
| 成本 Cost | O(log k) 次組合，乘法成本另計。 |

來源：

- [Divide and Conquer vs Dynamic Programming 比較分析](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/02_Divide_and_Conquer_vs_Dynamic_Programming.md)
- [📘 DSA Design Pattern Roadmap](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/01-Interview_Timing_Framework.md)

<a id="matrix-power"></a>
### 163 · Matrix Exponentiation

來源深度：清單／提及延伸

**關鍵論述：** 優化的是轉換的重複執行次數；「O(log k)」省略了維度成本。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 快速推進固定維度線性遞推。 |
| 狀態 State | 狀態向量、固定轉移矩陣與剩餘步數。 |
| 轉換 Transition | 將多步轉換合成矩陣冪，再作用於初始向量。 |
| 計算順序 Order | 二進位快速冪。 |
| 正確性與終止 Correctness | 矩陣必須忠實表示線性且固定的轉移；一般 DP 不能直接套。 |
| 成本 Cost | d 維普通矩陣乘法為 O(d³log k)、O(d²) 空間。 |

來源：

- [解題 Follow-up 待辦清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Learning_Roadmap.md)
- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)

<a id="combinatorics"></a>
### 164 · Binomial／Factorial／Catalan Counting

來源深度：清單／提及延伸

**關鍵論述：** 數學公式把大量狀態的聚合化簡成少量運算，但仍有計數證明。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 用結構分類直接計算構造數。 |
| 狀態 State | 規模、已選數量，或左右子結構大小。 |
| 轉換 Transition | 二項係數按選與不選分解；Catalan 按根的左右規模分解。 |
| 計算順序 Order | 規模遞增 DP，或在數域條件成立下用公式。 |
| 正確性與終止 Correctness | 分解須互斥且完備；模數除法要有逆元，不能直接整除餘數。 |
| 成本 Cost | Pascal 表 O(nk)；Catalan 卷積 DP O(n²)，公式法成本依算術。 |

來源：

- [解題 Follow-up 待辦清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Learning_Roadmap.md)
- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)
- [📘 DSA Design Pattern Roadmap](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/01-Interview_Timing_Framework.md)

<a id="nim"></a>
### 165 · Nim／有限取石遊戲的勝負狀態

來源深度：清單／提及延伸

**關鍵論述：** 勝負摘要依玩家視角轉換，規則才決定可否用餘數或 XOR 化簡。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 判斷輪到目前玩家時是否有必勝策略。 |
| 狀態 State | 剩餘石子或多堆狀態，value 為勝／負。 |
| 轉換 Transition | 存在一步把對手送入敗態即為勝；否則為敗。 |
| 計算順序 Order | 先小規模再大規模，或用已證明的不變量化簡。 |
| 正確性與終止 Correctness | 本 repo 的單堆每次取 1–3 與多堆 Nim 規則不同；終局與取最後者勝負要固定。 |
| 成本 Cost | 直接 DP 依狀態與分支；1–3 單堆可由模 4 分類成 O(1)。 |

來源：

- [LeetCode Tricks and Keywords](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/LeetCode_Tricks_and_Keywords.md)
- [📘 DSA Design Pattern Roadmap](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/01-Interview_Timing_Framework.md)

<a id="min-second"></a>
### 166 · Min／Second Min／Running Extremum

來源深度：既有論述延伸

**關鍵論述：** 只保留未來能進入答案的少數代表，避免完整排序。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 一次掃描取得少數極值。 |
| 狀態 State | 已掃前綴最小與次小值，必要時含索引。 |
| 轉換 Transition | 新值插入兩個候選，移除多餘者。 |
| 計算順序 Order | 依輸入掃描。 |
| 正確性與終止 Correctness | 要先定義次小是第二個元素還是第二種不同值；初始化需容納全值域。 |
| 成本 Cost | O(n) 時間、O(1) 額外空間。 |

來源：

- [一次遍歷找出最小值與次小值的技巧](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Find_Min_and_Second_Min_Trick.md)
- [C++ STL 心法：minelement 與 maxelement 使用指南](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Min_Max_Element_Usage.md)

<a id="integer-boundaries"></a>
### 167 · 整數邊界／Ceiling／Median Index

來源深度：既有論述延伸

**關鍵論述：** 表示範圍是狀態契約的一部分；數學式正確不代表機器運算一定正確。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 以精確算術表示取整、索引與累積邊界。 |
| 狀態 State | 商餘數、索引、數值型別及其可表示範圍。 |
| 轉換 Transition | 以商餘關係計算進位；乘加前檢查是否超界。 |
| 計算順序 Order | 每次算術更新前驗證中間值；浮點整數判定要考量誤差。 |
| 正確性與終止 Correctness | 常用 ceiling 公式需非負分子與正分母；中位數索引需非空且有序。 |
| 成本 Cost | 固定 machine word 運算 O(1)，不是把任意大數當常數。 |

來源：

- [演算法技巧：整數除法的無條件進位 (Ceiling Trick)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Integer_Division_Ceiling_Trick.md)
- [心法：利用整數除法統一計算中位數索引](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Median_Index_Calculation_with_Integer_Division.md)
- [LeetCode ASCII 必備知識](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Type/ASCII_for_LeetCode.md)
- [C++ 心法：字元與整數互轉 (char <-> int)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Type/Char_Int_Conversion.md)
- [C++ 型別陷阱：字元 vs. 整數在條件判斷中的差異](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Type/Char_vs_Int_in_Conditionals.md)
- [Double to Integer Verification (浮點數轉整數驗證)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Type/Double_to_Integer_Verification.md)
- [C++ 浮點數與科學記號 (Floating-Point and Scientific Notation)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Type/Floating_Point_and_Scientific_Notation.md)
- [整數溢位防範心法 (Integer Overflow Prevention)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Type/Integer_Overflow_Prevention.md)
- [C++ 最大值/最小值初始化技巧](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Type/Min_Max_Initialization.md)

<a id="coordinate"></a>
### 168 · Coordinate Mapping／Matrix In-place Marking

來源深度：既有論述延伸

**關鍵論述：** 資料布局本身可承載控制資訊，但必須明確區分原資料與暫存語義。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 重排矩陣或以輸入儲存輔助標記。 |
| 狀態 State | 座標映射、邊界、行列標記與首行首列原狀態。 |
| 轉換 Transition | 映射位置後搬移，或先標记再依標记修改。 |
| 計算順序 Order | 置換按循環/對稱分組；標記與套用分階段。 |
| 正確性與終止 Correctness | 映射需一對一並避免覆蓋；共用首格不能丟失兩個獨立旗標。 |
| 成本 Cost | R×C 全掃 O(RC)，某些原地方案 O(1) 額外空間。 |

來源：

- [LeetCode Tricks and Keywords](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/LeetCode_Tricks_and_Keywords.md)
- [矩陣問題工具箱：三大核心思維](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/Matrix_Problem_Solving_Toolkit.md)

<a id="validation-map"></a>
### 169 · Validation–Transformation Map

來源深度：既有論述延伸

**關鍵論述：** 一份關係表示同時支援判斷與轉換，減少重複的 set 與條件分支。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 统一表示合法符號及其轉換對象。 |
| 狀態 State | 來源到目標的映射，必要時雙向映射。 |
| 轉換 Transition | 查表同時判斷是否合法與取得轉換結果。 |
| 計算順序 Order | 依輸入或對稱位置掃描。 |
| 正確性與終止 Correctness | 單向函數不自動是雙射；需要一對一時必須檢查反向唯一性。 |
| 成本 Cost | 固定字母表 O(n)、O(1) 表；hash 表則期望成本。 |

來源：

- [Map as Unified Validation-Transformation 心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Hash_Tables/Validation_Transformation_Duality.md)

<a id="movement"></a>
### 170 · Movement Constraint Transformation

來源深度：既有論述延伸

**關鍵論述：** 用可達性的必要且充分條件，取代枚舉所有中間配置。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 判定兩配置能否在受限移動下互相轉換。 |
| 狀態 State | 保序實體、來源與目標位置、方向限制。 |
| 轉換 Transition | 對照各實體的相對次序與允許位移。 |
| 計算順序 Order | 跳過空位後以雙指標配對。 |
| 正確性與終止 Correctness | 不變量通常只是必要條件；還須證明满足條件可構造合法移動序列。 |
| 成本 Cost | 具此結構的序列問題可 O(n)，一般移動問題不保證。 |

來源：

- [Movement Constraint Transformation 解題心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Transformation_Patterns/Movement_Constraint_Transformation.md)

<a id="remaining-budget"></a>
### 171 · Remaining Budget／限制吸收

來源深度：既有論述延伸

**關鍵論述：** 重新表示可讓終止條件更直接，但不會自動創造新的剪枝保證。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 用剩餘量統一目標判定。 |
| 狀態 State | 尚未達成的目標或剩餘資源。 |
| 轉換 Transition | 消耗一步便扣除當步貢獻。 |
| 計算順序 Order | 跟隨原 traversal 或遞迴。 |
| 正確性與終止 Correctness | 剩餘值與原目標減累積量恆等；有負貢獻時剩餘負數不代表可剪枝。 |
| 成本 Cost | 通常不改變漸近成本，只減少冗餘參數與判斷。 |

來源：

- [問題轉換心法：將「限制」轉化為「工具」](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Transformation_Patterns/Transforming_Constraints_into_Tools.md)

<a id="preprocess"></a>
### 172 · Preprocessing／Offline／Coordinate Compression

來源深度：既有論述延伸

**關鍵論述：** 以整批工作的總成本選表示，單次更慢的建構可能讓整體更快。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 讓多次查詢共享整理過的資料。 |
| 狀態 State | 排序索引、摘要表、值到排名映射、原始查詢 ID。 |
| 轉換 Transition | 先建立表示，再回答查詢或依方便順序處理。 |
| 計算順序 Order | 離線可重排查詢，最後依 ID 還原輸出次序。 |
| 正確性與終止 Correctness | 排名保留順序與相等，不保留原數值距離；線上限制可能不允許重排。 |
| 成本 Cost | 總成本為預處理 P 加 q 次查詢成本，另計儲存。 |

來源：

- [演算法優化心法：透過預處理加速重複查詢](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Time_Space_Tradeoff_Patterns.md)
- [STL 容器轉換心法：以迭代器為橋樑](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Container_Conversion_Techniques.md)
- [🎯 Technique Integration Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Technique_Integration_Problems.md)
- [Problem Transformation Framework](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Transformation.md)

<a id="linear-stl"></a>
### 173 · Linear Scan／Find／Count／Transform／Fold

來源深度：既有論述延伸

**關鍵論述：** STL 函數隐藏的是迴圈；狀態、順序與每次操作成本仍需理解。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 進行逐項搜尋、映射、折疊與集合整理。 |
| 狀態 State | 游標、累积值或輸出位置。 |
| 轉換 Transition | 讀一項後查找、計數、轉換、複製、去重或聚合。 |
| 計算順序 Order | accumulate 固定左折疊；reduce 可重排分組，需相應運算性質。 |
| 正確性與終止 Correctness | unique 只處理相鄰等值並回傳邏輯末端；擦除容器尾段才縮短長度。reduce 可重排時，操作需滿足允許重排的代數條件。 |
| 成本 Cost | 多數線性掃描 O(n)，但字串反覆複製或非 O(1) 操作可能放大成本。 |

來源：

- [排序基礎](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/01-Fundamentals_of_Sorting.md)
- [C++ STL 心法：std::accumulate vs. std::reduce 比較](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Accumulate_vs_Reduce.md)
- [C++ 常用演算法與工具函式](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Common_Algorithms_and_Utilities.md)
- [C++ 技巧：使用 Lambda 與 decltype 實現自訂比較器](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Custom_Comparators_with_Decltype.md)
- [C++ STL 演算法中的自訂操作：謂詞與函式物件深度解析](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Custom_Operation_Types.md)
- [C++ STL 心法：深入理解 lowerbound 與 upperbound](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Lower_Upper_Bound_Explained.md)
- [C++ STL 心法：minelement 與 maxelement 使用指南](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Min_Max_Element_Usage.md)
- [std::partialsum: 高效計算前綴和](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Partial_Sum_Usage.md)
- [C++ 排序演算法比較：std::sort, std::stablesort, 與 container.sort()](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Sort_Comparison.md)
- [C++ 使用 std::transform](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Transform_Usage_Tip.md)
- [C++ One-Liners for LeetCode](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/CPP_One_Liners.md)

<a id="fisher-yates"></a>
### 174 · Fisher–Yates Shuffle

來源深度：清單／提及延伸

**關鍵論述：** 狀態空間沒有減少；隨機策略是在所有排列間提供正確的取樣分布。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 均勻隨機產生排列。 |
| 狀態 State | 已固定區域、未處理區域與隨機來源。 |
| 轉換 Transition | 從剩餘位置均勻選一個與邊界交換。 |
| 計算順序 Order | 每輪固定一個新位置。 |
| 正確性與終止 Correctness | 每步須在正確範圍均勻抽樣，才讓每個排列機率相同。 |
| 成本 Cost | O(n) 時間、O(1) 額外空間。 |

來源：

- [C++ One-Liners for LeetCode](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/CPP_One_Liners.md)


<a id="chapter-10"></a>
## 進階延伸

<a id="lis-tails"></a>
### 175 · LIS：Greedy Tails + Binary Search

來源深度：既有論述延伸

**關鍵論述：** 將每種長度的所有歷史壓成最有利結尾，這是支配關係的具體應用。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 求最長遞增子序列長度。 |
| 狀態 State | 每種長度可達到的最小結尾值。 |
| 轉換 Transition | 新值替換第一個不小於它的結尾，或延長最長長度。 |
| 計算順序 Order | 按原索引順序讀取，於 tails 二分。 |
| 正確性與終止 Correctness | 同長度下較小結尾不妨礙未來延伸；tails 本身未必是一條真實子序列。 |
| 成本 Cost | O(nlog n) 時間、O(n) 空間；重建需另存前驅。 |

來源：

- [演算法心法：子序列問題攻略 (Subsequence Problem-Solving Strategies)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/Subsequence_Problem_Solving_Strategies.md)

<a id="a-star"></a>
### 176 · A* Search

來源深度：清單／提及延伸

**關鍵論述：** 啟發式改變探索順序；估計與已證明的真實成本必須分開。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在有啟發式估計時優先探索有希望的路徑。 |
| 狀態 State | 已走成本 g、剩餘估計 h、open queue 與最佳標籤。 |
| 轉換 Transition | 鬆弛鄰居，依 g+h 排序待處理項。 |
| 計算順序 Order | 取最小估計總成本；必要時重新打開改善的節點。 |
| 正確性與終止 Correctness | h 不高估且正確重開可支持最優性；永久關閉通常需一致性。 |
| 成本 Cost | 取決於啟發式與重開次數；最壞仍可能探索整個巨大狀態空間。 |

來源：

- [解題 Follow-up 待辦清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Learning_Roadmap.md)
- [格狀圖（Lattice Graph / Grid Graph）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Lattice_Graph.md)
- [Heap 使用場景的關鍵決策點](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/01-Heap_Decision_Making.md)
- 補充核對：[NetworkX：A* heuristic 與最短路條件](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.astar.astar_path.html)

<a id="kmp"></a>
### 177 · KMP／Prefix Function

來源深度：既有論述延伸

**關鍵論述：** 失配不需重讀全部歷史，因為已匹配結構提供下一個充分狀態。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在線性掃描中找固定模式。 |
| 狀態 State | 目前匹配前綴長度、模式的 prefix/failure 表。 |
| 轉換 Transition | 匹配則延伸，失配沿最長可行 border 回退。 |
| 計算順序 Order | 文字游標不倒退，模式狀態按 failure link 調整。 |
| 正確性與終止 Correctness | 保留的是已讀文字後綴中仍可接續的最長模式前綴。 |
| 成本 Cost | 文字 n、模式 m 時 O(n+m)，額外空間 O(m)。 |

來源：

- [🎯 KMP String Matching (字串匹配) - 練習路徑](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/KMP_String_Matching_Playbook.md)

<a id="z-function"></a>
### 178 · Z-function／Z-algorithm

來源深度：清單／提及延伸

**關鍵論述：** 用已確認的重複區間作證據，跳過必然相等的比較。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 求各位置起始字串與整體前綴的最長匹配。 |
| 狀態 State | Z 值與最右已知匹配區間。 |
| 轉換 Transition | 區間內重用對應 Z 值，再只比較未知邊界外部分。 |
| 計算順序 Order | 位置由左至右，右邊界單調擴張。 |
| 正確性與終止 Correctness | 重用長度不能超出已證實匹配區間。 |
| 成本 Cost | O(n) 時間、O(n) 空間。 |

來源：

- [🎯 KMP String Matching (字串匹配) - 練習路徑](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/KMP_String_Matching_Playbook.md)
- [📘 DSA Design Pattern Roadmap](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/01-Interview_Timing_Framework.md)

<a id="rolling-hash"></a>
### 179 · Rolling Hash／Rabin–Karp

來源深度：清單／提及延伸

**關鍵論述：** 摘要可大幅減少比較工作，但有限 hash 不是無碰撞的等價關係。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 快速比較子字串或篩出模式匹配候選。 |
| 狀態 State | 前綴 polynomial hash、冪表，或滾動窗口 hash。 |
| 轉換 Transition | 加入新字元、移除舊貢獻，或由前綴取得子字串 hash。 |
| 計算順序 Order | 預處理後查詢，或沿窗口掃描。 |
| 正確性與終止 Correctness | hash 相等只是候選相等；要確定正確需核對內容或明確接受碰撞風險。 |
| 成本 Cost | 預處理 O(n)，摘要查詢 O(1)；逐候選核對最壞可 O(nm)。 |

來源：

- [📘 DSA Design Pattern Roadmap](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/01-Interview_Timing_Framework.md)

<a id="manacher"></a>
### 180 · Manacher

來源深度：清單／提及延伸

**關鍵論述：** 重用對稱區間內的計算，將重複中心擴張壓到線性總工作。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 求每個中心的最長回文半徑。 |
| 狀態 State | 各中心半徑、最右回文邊界及中心。 |
| 轉換 Transition | 利用鏡像位置已知半徑，再向未確認區域擴張。 |
| 計算順序 Order | 由左至右，使最右邊界持續前進。 |
| 正確性與終止 Correctness | 鏡像資訊只在已知回文内部可靠，超出部分仍要比較。 |
| 成本 Cost | O(n) 時間與空間；列出所有回文仍受 O(n²) 輸出量限制。 |

來源：

- [LeetCode Tricks and Keywords](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/LeetCode_Tricks_and_Keywords.md)
- [📘 DSA Design Pattern Roadmap](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/01-Interview_Timing_Framework.md)
- 補充核對：[Manacher：半徑摘要與線性計算](https://cp-algorithms.com/string/manacher.html)

<a id="aho"></a>
### 181 · Aho–Corasick／多模式自動機

來源深度：清單／提及延伸

**關鍵論述：** 把 KMP 的後綴回退擴充到共享前綴的整個字典。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 同時尋找多個模式字串。 |
| 狀態 State | Trie 節點、failure links、output links 與目前狀態。 |
| 轉換 Transition | 讀字元後走轉移；失配回退到可用後綴，輸出命中模式。 |
| 計算順序 Order | 建構通常 BFS；文字只向前掃描。 |
| 正確性與終止 Correctness | 目前節點代表已讀文字的最長可用字典前綴後綴。 |
| 成本 Cost | 固定字母表下建構 O(L)、匹配 O(n+z)；轉移表方式另有字母表因子。 |

來源：

- [📘 DSA Design Pattern Roadmap](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/01-Interview_Timing_Framework.md)
- 補充核對：[Aho–Corasick：自動機建構](https://cp-algorithms.com/string/aho_corasick.html)

<a id="bipartite"></a>
### 182 · Bipartite Check／二染色

來源深度：清單／提及延伸

**關鍵論述：** 顏色保存可行分組的約束，而非 DFS 的白灰黑完成階段。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 判斷無向圖能否分成兩個無內部邊的集合。 |
| 狀態 State | 每節點二色標記與待探索 frontier。 |
| 轉換 Transition | 沿每條邊要求鄰居顏色相反。 |
| 計算順序 Order | 每個連通分量各啟動 DFS/BFS。 |
| 正確性與終止 Correctness | 同色相鄰代表奇環矛盾；二染色不是求最大匹配。 |
| 成本 Cost | O(V+E) 時間、O(V) 空間。 |

來源：

- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)

<a id="hopcroft-karp"></a>
### 183 · Hopcroft–Karp／Maximum Bipartite Matching

來源深度：清單／提及延伸

**關鍵論述：** 舊決策可以被翻轉；殘餘的替代路徑讓局部配對可逐步改善。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 求二分圖最大基數匹配。 |
| 狀態 State | 左右配對、交替路徑、分層距離。 |
| 轉換 Transition | 找一批最短增廣路徑，翻轉其匹配與非匹配邊。 |
| 計算順序 Order | BFS 建層，DFS 在層圖尋找互不衝突的增廣路。 |
| 正確性與終止 Correctness | 增廣路使匹配數增加；不存在增廣路等價於最大匹配。 |
| 成本 Cost | 標準 O(E√V) 時間、O(V+E) 空間（非孤立部分）。 |

來源：

- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)
- 補充核對：[NetworkX：Hopcroft–Karp 與原始論文](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bipartite.matching.hopcroft_karp_matching.html)

<a id="tarjan"></a>
### 184 · Tarjan SCC／Lowlink

來源深度：清單／提及延伸

**關鍵論述：** 延遲分組，直到目前節點能證明是一個完整 SCC 的邊界。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 分解有向圖的強連通分量。 |
| 狀態 State | DFS 序號、lowlink、尚未歸屬分量的 stack 與 onStack。 |
| 轉換 Transition | 由子樹與仍在 stack 的可達邊更新 lowlink，遇分量根時彈出整組。 |
| 計算順序 Order | 一次 DFS，子節點先回傳再完成分量。 |
| 正確性與終止 Correctness | 只能把尚未結算 SCC 的 stack 關係用於相應 lowlink 更新。 |
| 成本 Cost | O(V+E) 時間、O(V) 額外空間。 |

來源：

- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)

<a id="kosaraju"></a>
### 185 · Kosaraju SCC

來源深度：清單／提及延伸

**關鍵論述：** 先算出的順序是一份摘要，讓下一次搜尋能安全劃分群組。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 以兩次走訪分解強連通分量。 |
| 狀態 State | 原圖、反圖、第一次完成順序與分量標記。 |
| 轉換 Transition | 先記完成序，再在反圖依反完成序搜尋各分量。 |
| 計算順序 Order | 兩次 DFS，第二次順序不可任意。 |
| 正確性與終止 Correctness | SCC 縮成 DAG 後，完成序保證第二次不跨進尚未處理的其他分量。 |
| 成本 Cost | O(V+E) 時間與空間。 |

來源：

- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)

<a id="bridges"></a>
### 186 · Lowlink Bridges／Articulation Points

來源深度：辨義補充

**關鍵論述：** 把「是否有繞路」壓成一個可回達的最早時間摘要。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 判定無向圖刪邊或刪點後是否失去連通性。 |
| 狀態 State | 發現時間、low、父邊與 DFS 孩子數。 |
| 轉換 Transition | 聚合子樹可回到的最早祖先，檢查是否存在替代連通路。 |
| 計算順序 Order | DFS 回傳時結算；根節點的割點條件獨立處理。 |
| 正確性與終止 Correctness | 橋與 SCC 雖都用 lowlink，但比較條件及 stack 語義不同；平行邊要保留 ID。 |
| 成本 Cost | O(V+E) 時間、O(V) 額外空間。 |

來源：

- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)

<a id="flow"></a>
### 187 · Maximum Flow／Minimum Cut／Residual Network

來源深度：清單／提及延伸

**關鍵論述：** 狀態轉換允許修正過去的分配；殘餘圖保存所有尚可調整的餘地。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在容量限制下最大化源到匯的流量。 |
| 狀態 State | 可行流、正反向殘餘容量與可達集合。 |
| 轉換 Transition | 沿增廣路增加流，同時保留反向撤銷能力。 |
| 計算順序 Order | 反覆改善，直到殘餘圖不存在源匯路徑。 |
| 正確性與終止 Correctness | 容量與流量守恆維持；無增廣路時可達割提供最優證書。 |
| 成本 Cost | 依路徑選擇策略決定，不能只寫一次圖遍歷。 |

來源：

- [LeetCode 高階心法（完整 MD + 一頁式速查表）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/04-Advanced_Problem_Solving_Cheatsheet.md)
- [Problem Transformation Framework](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Transformation.md)
- 補充核對：[Maximum Flow／Minimum Cut](https://cp-algorithms.com/graph/edmonds_karp.html)

<a id="edmonds-karp"></a>
### 188 · Edmonds–Karp

來源深度：清單／提及延伸

**關鍵論述：** BFS 在這裡控制總增廣次數，與原圖的最短成本路徑是不同目標。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 用最少邊數增廣路計算最大流。 |
| 狀態 State | 殘餘容量、BFS parent 與路徑瓶頸。 |
| 轉換 Transition | BFS 找增廣路，再按瓶頸更新正反容量。 |
| 計算順序 Order | 每次重新在殘餘圖 BFS。 |
| 正確性與終止 Correctness | 最短增廣路長度的單調性限制關鍵邊反覆飽和次數。 |
| 成本 Cost | O(VE²) 時間、O(V+E) 儲存（鄰接表表示）。 |

來源：

- [LeetCode 高階心法（完整 MD + 一頁式速查表）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/04-Advanced_Problem_Solving_Cheatsheet.md)
- 補充核對：[Edmonds–Karp：殘餘網路](https://cp-algorithms.com/graph/edmonds_karp.html)

<a id="dinic"></a>
### 189 · Dinic／Blocking Flow

來源深度：清單／提及延伸

**關鍵論述：** 一次排程處理整批同層改善，避免每送一條路都重建全部搜尋資訊。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 批次消耗同一層次的增廣可能。 |
| 狀態 State | 殘餘圖、level、當前弧索引。 |
| 轉換 Transition | 在 level graph 推送阻塞流，再重新分層。 |
| 計算順序 Order | BFS 建層，DFS 搭配 current arc 消耗當層。 |
| 正確性與終止 Correctness | 每輪堵住所有最短層路徑，之後有效源匯距離增加。 |
| 成本 Cost | 一般容量網路 O(V²E)，特殊網路有更好界。 |

來源：

- [LeetCode 高階心法（完整 MD + 一頁式速查表）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/04-Advanced_Problem_Solving_Cheatsheet.md)
- 補充核對：[Dinic：分層與阻塞流](https://cp-algorithms.com/graph/dinic.html)

<a id="hungarian"></a>
### 190 · Hungarian／加權指派

來源深度：清單／提及延伸

**關鍵論述：** 狀態同時保存可行解與最優性證書；中文「匈牙利」有時也指無權增廣法，需辨義。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 求方陣指派的最小總成本。 |
| 狀態 State | 匹配、行列 potentials、slack 與等號邊。 |
| 轉換 Transition | 調整 potentials 產生可用等號邊，再增廣匹配。 |
| 計算順序 Order | 逐步擴張可行匹配直到完整指派。 |
| 正確性與終止 Correctness | 勢能提供成本下界；完整匹配與下界相等即證明最優。 |
| 成本 Cost | n×n 標準改良版 O(n³) 時間、矩陣 O(n²) 儲存。 |

來源：

- [LeetCode 高階心法（完整 MD + 一頁式速查表）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/04-Advanced_Problem_Solving_Cheatsheet.md)
- 補充核對：[Hungarian Algorithm：勢能與指派](https://cp-algorithms.com/graph/hungarian-algorithm.html)

<a id="dc-optimization"></a>
### 191 · Divide-and-Conquer DP Optimization／Monge

來源深度：清單／提及延伸

**關鍵論述：** 保留所有 DP 狀態，減少的是每個狀態要看的候選轉移。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 減少分層 DP 每項枚舉的切點數。 |
| 狀態 State | 一層 DP 值、各位置最佳切點的合法範圍。 |
| 轉換 Transition | 先求中點最佳切點，再用其單調性限制左右搜尋。 |
| 計算順序 Order | 外層依 DP 層，層內分治求值。 |
| 正確性與終止 Correctness | 需要 argmin 單調；Monge／四邊形不等式可在相應遞推下提供條件。 |
| 成本 Cost | m 層 n 點，常數成本函數下常見 O(mnlog n)，不是通用 O(n²)。 |

來源：

- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)
- 補充核對：[Divide and Conquer DP：條件與複雜度](https://cp-algorithms.com/dynamic_programming/divide-and-conquer-dp.html)

<a id="knuth"></a>
### 192 · Knuth Optimization

來源深度：清單／提及延伸

**關鍵論述：** 與一般分治 DP 優化的條件與界不同，不能因同樣有切點就互換。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 加速特定區間切分 DP。 |
| 狀態 State | 區間最佳值與最佳切點 opt。 |
| 轉換 Transition | 只在鄰近區間 opt 夾出的範圍枚舉切點。 |
| 計算順序 Order | 先短區間再長區間。 |
| 正確性與終止 Correctness | 需 opt(i,j−1)≤opt(i,j)≤opt(i+1,j)；常用充分條件包含成本單調與四邊形不等式。 |
| 成本 Cost | 符合指定遞推時由 O(n³) 到 O(n²)，空間 O(n²)。 |

來源：

- [Hard Techniques Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md)
- 補充核對：[Knuth Optimization：適用遞推與條件](https://cp-algorithms.com/dynamic_programming/knuth-optimization.html)

<a id="closest-pair"></a>
### 193 · Closest Pair 分治

來源深度：清單／提及延伸

**關鍵論述：** 幾何結構提供「只有附近候選可能改善」的證明。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 找平面中距離最近的點對。 |
| 狀態 State | 按座標排序的半部、目前最短距離與中線窄帶。 |
| 轉換 Transition | 取兩半最小值，再檢查可能更近的跨界點。 |
| 計算順序 Order | 分治後以 y 順序處理窄帶。 |
| 正確性與終止 Correctness | 平面 packing 界限制窄帶內每點需比較的鄰近候選；排序需跨層重用。 |
| 成本 Cost | 標準平面版本 O(nlog n)、O(n) 空間。 |

來源：

- [Divide and Conquer 設計策略心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/01_Divide_and_Conquer_Design_Strategy.md)
- [Divide and Conquer vs Dynamic Programming 比較分析](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/02_Divide_and_Conquer_vs_Dynamic_Programming.md)

<a id="convex-hull"></a>
### 194 · Convex Hull／凸包建構

來源深度：清單／提及延伸

**關鍵論述：** 用凸性支配候選，讓內部點退出後續邊界搜尋。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 取得包住點集的最外層邊界。 |
| 狀態 State | 候選邊界链、方向或左右子凸包。 |
| 轉換 Transition | 移除不符合凸性的中間點，或用公切線合併子凸包。 |
| 計算順序 Order | 常見先排序再掃描上下鏈；也可分治合併。 |
| 正確性與終止 Correctness | 剔除點不可能成為目標外邊界；共線點是否保留需固定。 |
| 成本 Cost | 平面排序法 O(nlog n)、O(n) 空間。 |

來源：

- [Divide and Conquer vs Dynamic Programming 比較分析](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/02_Divide_and_Conquer_vs_Dynamic_Programming.md)

<a id="calipers"></a>
### 195 · Rotating Calipers／旋轉卡尺

來源深度：清單／提及延伸

**關鍵論述：** 幾何版本的雙指標，省略配對的理由來自凸性。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在凸多邊形上找極端距離或支撐配對。 |
| 狀態 State | 目前邊、支撐點與單調移動的對向索引。 |
| 轉換 Transition | 旋轉支撐方向，將對向點推到對應極值。 |
| 計算順序 Order | 沿凸包邊依序推進，两端索引只向前。 |
| 正確性與終止 Correctness | 凸性使最優對向位置具有單調進展；一般無序點集不能直接用。 |
| 成本 Cost | 凸包已給定時典型 O(h)，含建包 O(nlog n)。 |

來源：

- [LeetCode 高階心法（完整 MD + 一頁式速查表）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/04-Advanced_Problem_Solving_Cheatsheet.md)

<a id="fibonacci-heap"></a>
### 196 · Fibonacci Heap

來源深度：清單／提及延伸

**關鍵論述：** 延遲維護改變操作成本分配，不能把它的界套到普通 binary heap。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 降低大量 decrease-key 的攤銷成本。 |
| 狀態 State | heap-ordered 森林、最小根、degree 與 mark。 |
| 轉換 Transition | 插入延後整併；delete-min 合併同 degree 樹；減鍵可級聯切割。 |
| 計算順序 Order | 用延遲工作與勢能管理整段操作序列。 |
| 正確性與終止 Correctness | heap 次序維持，標記與切割限制樹 degree 增長。 |
| 成本 Cost | 插入與 decrease-key 攤銷 O(1)，delete-min 攤銷 O(log n)。 |

來源：

- [Dijkstra 演算法：從理論到 C++ 實踐深度解析](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Dijkstra%27s%20Algorithm/01-Dijkstra_Algorithm_Guide.md)

<a id="fractional-knapsack"></a>
### 197 · Fractional Knapsack

來源深度：清單／提及延伸

**關鍵論述：** 允許分割使局部交換可行，這項條件才是貪婪成立的關鍵。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在可分割物品中最大化有限容量收益。 |
| 狀態 State | 剩餘容量、依收益密度排序的候選與已取份額。 |
| 轉換 Transition | 優先取較高密度，最後可只取一部分。 |
| 計算順序 Order | 依單位容量收益由高到低。 |
| 正確性與終止 Correctness | 任意低密度份額可被高密度可用份額替換而不變差；不可分割時證明失效。 |
| 成本 Cost | 排序 O(nlog n)、掃描 O(n)。 |

來源：

- [心法：貪婪演算法的辨識與應用框架](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Greedy_Identification_and_Application.md)
- [Greedy Algorithm Proofs：交換論證 (Exchange Argument)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Proof_Techniques/Exchange_Argument.md)


<a id="chapter-11"></a>
## 組合與證明

<a id="brute-force"></a>
### 198 · Brute Force／Exhaustive Enumeration

來源深度：既有論述延伸

**關鍵論述：** 暴力法提供清楚的狀態與轉換基準，優化再逐項說明省掉什麼工作。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 建立不漏候選的基準解法。 |
| 狀態 State | 目前候選索引或完整選擇、驗證結果與答案。 |
| 轉換 Transition | 生成下一候選、完整驗證、聚合結果。 |
| 計算順序 Order | 依可枚舉的固定順序。 |
| 正確性與終止 Correctness | 候選集合覆蓋全部答案且驗證正確；成本含每個候選的驗證與輸出。 |
| 成本 Cost | 候選數乘驗證成本；不一定指數，也可能 O(n²) 或 O(n³)。 |

來源：

- [Essential Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Essential_Problems.md)
- [032. Longest Valid Parentheses](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Super_Hard/032_Longest_Valid_Parentheses.md)

<a id="bit-fsm"></a>
### 199 · Bitwise State Machine／Modulo Counter

來源深度：清單／提及延伸

**關鍵論述：** 把許多相同小狀態機打包運算，從位元層級共享控制流程。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在重複次數有規律時按位追蹤計數餘數。 |
| 狀態 State | 每個 bit 的有限計數狀態，打包成少量 machine words。 |
| 轉換 Transition | 新值各 bit 同步推進計數循環。 |
| 計算順序 Order | 逐數掃描，狀態更新需使用正確的舊版本。 |
| 正確性與終止 Correctness | 各 bit 的狀態都等價於目前出現次數對指定模數的餘數。 |
| 成本 Cost | 固定 word 寬與固定循環長度下 O(n) 時間、O(1) 額外空間。 |

來源：

- [Essential Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Essential_Problems.md)
- [演算法題目複習清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Problem_Review.md)

<a id="bit-prefix"></a>
### 200 · Bitwise Prefixes + Hash Set

來源深度：清單／提及延伸

**關鍵論述：** 把數值最佳化拆成逐位可行性判定，hash 加速每次存在性檢查。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 由高位逐步建立可行的最大 XOR 前綴。 |
| 狀態 State | 目前位、已選答案前綴與輸入數的遮罩前綴集合。 |
| 轉換 Transition | 試著把下一位設為一，再檢查是否存在可組成目標的前綴對。 |
| 計算順序 Order | 由最高位到最低位。 |
| 正確性與終止 Correctness | 高位優先決定大小；候選前綴可由某對輸入實現才可保留。 |
| 成本 Cost | w 位、n 數為期望 O(wn)，O(n) 空間。 |

來源：

- [演算法題目複習清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Problem_Review.md)

<a id="fenwick2d"></a>
### 201 · 2D Fenwick Tree

來源深度：清單／提及延伸

**關鍵論述：** 一維摘要分解可以作乘積擴充，成本也相乘。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 維護可更新的矩形區域和。 |
| 狀態 State | 兩個維度都以 lowbit 分解的區域摘要。 |
| 轉換 Transition | 點更新沿兩軸祖先传播；前綴查詢按兩軸分解。 |
| 計算順序 Order | 每個維度分別按 Fenwick 跳躍。 |
| 正確性與終止 Correctness | 矩形和由四個二維前綴容斥取得；索引與數值版本一致。 |
| 成本 Cost | 點改與矩形查 O(log R·log C)，空間 O(RC)。 |

來源：

- [演算法題目複習清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Problem_Review.md)
- [Binary Indexed Tree (Fenwick Tree) 核心概念](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Advanced/Binary_Indexed_Tree/01-Core_Concepts.md)
- [Binary Indexed Tree 實作版本](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Advanced/Binary_Indexed_Tree/02-Implementations.md)

<a id="bucket-window"></a>
### 202 · Bucket Window／值差限制

來源深度：清單／提及延伸

**關鍵論述：** 值域分桶让可能的配對只存在少數鄰近位置，取代全窗口搜尋。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 在線上窗口中找位置與數值都接近的元素。 |
| 狀態 State | 依值域切分的桶、窗口範圍與桶中代表。 |
| 轉換 Transition | 新值檢查同桶及相鄰桶，再移除離開窗口的值。 |
| 計算順序 Order | 按輸入順序，索引窗口同步滑動。 |
| 正確性與終止 Correctness | 桶寬與允許值差一致；負數需要數学向下取整，同桶可行性要證明。 |
| 成本 Cost | 適用條件下期望 O(n)、O(k) 窗口空間。 |

來源：

- [演算法題目複習清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Problem_Review.md)

<a id="two-stack-postorder"></a>
### 203 · Two-Stack Postorder

來源深度：清單／提及延伸

**關鍵論述：** 用完整保存並反轉結果，換掉逐 frame 的返回階段判斷。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 以反向輸出次序模擬後序走訪。 |
| 狀態 State | 待探索 stack 與反向結果 stack。 |
| 轉換 Transition | 先依根右左的相應堆疊次序记录，再反轉輸出。 |
| 計算順序 Order | 第一階段遍歷，第二階段逆序讀結果。 |
| 正確性與終止 Correctness | 反轉後子節點都先於父節點；左右壓入順序必須與反轉方向一致。 |
| 成本 Cost | O(n) 時間、O(n) 額外空間。 |

來源：

- [演算法題目複習清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Problem_Review.md)
- [心法：將遞迴轉換為迭代](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Iterative_Traversal/01-Recursive_to_Iterative_Conversion.md)
- [Visit Nature 快速參考 / Quick Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Iterative_Traversal/02-Visit_Nature_Quick_Reference.md)
- [Current Pointer 實作模式 / Iterative Traversal Implementations](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Iterative_Traversal/03-Current_Pointer_Implementations.md)
- [深入解析：迭代 Postorder Traversal 中 lastVisited 的正確性](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Iterative_Traversal/04-Postorder_lastVisited_Deep_Dive.md)
- [統一心法：迭代遍歷的多重視角](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Iterative_Traversal/05-Unified_Framework.md)

<a id="parser-stack"></a>
### 204 · Nested Parsing／Two Stacks

來源深度：清單／提及延伸

**關鍵論述：** stack 保存被暫停的語法工作，與遞迴 frame 有相同角色。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 解析具有巢狀括號與局部重複規則的字串。 |
| 狀態 State | 未完成的外層字串、倍數與目前片段。 |
| 轉換 Transition | 開括號暫存外層；閉括號完成當層並接回。 |
| 計算順序 Order | 由左至右，巢狀部分 LIFO 完成。 |
| 正確性與終止 Correctness | 每次返回都恢復正確外層上下文，片段與倍數必須配對。 |
| 成本 Cost | 至少 Ω(輸出長度)；反覆字串複制可超過線性。 |

來源：

- [演算法題目複習清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Problem_Review.md)

<a id="parenthesis-stack"></a>
### 205 · Parenthesis Matching／Invalid Boundary Stack

來源深度：既有論述延伸

**關鍵論述：** 保存足以決定下一次匹配與區間起點的索引，不需保存每段完整文字。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 匹配括號並追蹤有效區間邊界。 |
| 狀態 State | 未匹配開括號索引與最近不可跨越的邊界。 |
| 轉換 Transition | 合法匹配時 pop，無法匹配時更新邊界。 |
| 計算順序 Order | 由左至右，最近未匹配開括號優先配對。 |
| 正確性與終止 Correctness | stack 頂在不同階段有不同語義；未匹配開括號不等於永久無效。 |
| 成本 Cost | O(n) 時間、O(n) 空間。 |

來源：

- [032. Longest Valid Parentheses](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Super_Hard/032_Longest_Valid_Parentheses.md)
- [快速決策地圖 (Quick Decision Map)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/02-Quick_Decision_Map.md)

<a id="parenthesis-two-scan"></a>
### 206 · Bidirectional Balance Scan

來源深度：既有論述延伸

**關鍵論述：** 兩次不同方向的計算，能替代一次掃描中保存完整索引歷史。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 用常數空間識別括號平衡區段。 |
| 狀態 State | 左右括號數、目前掃描段與最大長度。 |
| 轉換 Transition | 累計兩種括號，失衡時丟棄不可能跨越的段。 |
| 計算順序 Order | 正向與逆向各掃一次，分別處理不同方向的多餘括號。 |
| 正確性與終止 Correctness | 單向看不到的邊界由反向補足；規則適用於對應括號模型。 |
| 成本 Cost | O(n) 時間、O(1) 額外空間。 |

來源：

- [032. Longest Valid Parentheses](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Super_Hard/032_Longest_Valid_Parentheses.md)

<a id="circular-kadane"></a>
### 207 · Circular Subarray／補集最佳化

來源深度：清單／提及延伸

**關鍵論述：** 把跨邊界構造改成補集，便可重用已知的線性狀態設計。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 求環狀連續片段的最大和。 |
| 狀態 State | 總和、普通最大片段、最小片段。 |
| 轉換 Transition | 分別維護不跨界最佳值與由總和扣去最小中段的候選。 |
| 計算順序 Order | 一次掃描同步聚合。 |
| 正確性與終止 Correctness | 跨界片段對應其線性補集；不得用整個最小片段產生非法空答案。 |
| 成本 Cost | O(n) 時間、O(1) 空間。 |

來源：

- [演算法題目複習清單](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Problem_Review.md)

<a id="median-cost"></a>
### 208 · Median + Prefix Sum／L1 Cost

來源深度：清單／提及延伸

**關鍵論述：** 幾何／算術性質先決定最佳位置，摘要再讓成本評估變便宜。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 最小化點到共同位置的絕對距離和。 |
| 狀態 State | 排序位置、中位數與左右前綴和。 |
| 轉換 Transition | 以中位數作候選，用兩側摘要計算距離總和。 |
| 計算順序 Order | 先排序或維護窗口秩，再回答成本查詢。 |
| 正確性與終止 Correctness | 絕對距離和在中位數最小；加權版需加權中位數，相鄰交換題可能先變換座標。 |
| 成本 Cost | 排序 O(nlog n)；前綴建立後固定區間成本 O(1)。 |

來源：

- [🎯 Technique Integration Problems](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Technique_Integration_Problems.md)

<a id="proof-invariant"></a>
### 209 · Loop Invariant／契約與測試

來源深度：既有論述延伸

**關鍵論述：** 不變量解釋「轉換為何可靠」，而不只是複述程式變數值。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 證明每一步之後仍保留目標所需性質。 |
| 狀態 State | 可達程式狀態與命名清楚的不變量。 |
| 轉換 Transition | 證明初始化及每種更新都維持性質。 |
| 計算順序 Order | 按初始化、維持、終止展開。 |
| 正確性與終止 Correctness | 不變量加停止條件須推出目標；另需證明進展才能得到總正確性。 |
| 成本 Cost | 不改變原算法成本；測試只能找反例，不能替代全域證明。 |

來源：

- [C++ 常見編程錯誤與心法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Common_Coding_Mistakes.md)
- [C++ 陷阱：非 const 左值引用無法綁定到臨時物件](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Common_Coding_Mistakes/Binding_Temporaries_to_LValue_References.md)
- [C++ 陷阱：條件運算子（?:）中無法使用 {} 初始化列表](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Common_Coding_Mistakes/Conditional_Operator_Braced_Init_List.md)
- [C++ 陷阱：std::min 與 std::max 的型別不匹配問題](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Common_Coding_Mistakes/Std_Min_Max_Type_Mismatch.md)
- [Code Review 心法：從口訣到實踐](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Code_Review.md)
- [循環不變量 (Loop Invariant)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Proof_Techniques/Loop_Invariant.md)
- [圖結構的系統化測試案例設計](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Test_Case_Construction/Graph_Test_Case_Strategies.md)
- [Test Case Construction: The Engineer's Litmus Test](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Test_Case_Construction/README.md)
- [ChatGPT's Guide to Building Test Cases Under Pressure](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Test_Case_Construction/Test_Case_Generation_Advice_ChatGPT.md)
- [Effective Test Case Construction for Coding Interviews](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Test_Case_Construction/Test_Case_Generation_Advice_Gemini.md)
- [Claude Sonnet's Approach to Test Case Generation Under Interview Pressure](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Test_Case_Construction/Test_Case_Generation_Advice_Sonnet.md)
- [樹結構 Test Case 的高效標記法](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Test_Case_Construction/Tree_Test_Case_Notation.md)
- [樹結構的系統化測試案例設計](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Test_Case_Construction/Tree_Test_Case_Types.md)

<a id="proof-induction"></a>
### 210 · Structural Induction／遞迴正確性

來源深度：既有論述延伸

**關鍵論述：** 函式簽名是子問題契約，歸納法讓你能可信地使用其回傳值。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 證明所有規模或結構的子問題契約。 |
| 狀態 State | 結構大小、基底與子結構假設。 |
| 轉換 Transition | 從孩子契約推導父契約。 |
| 計算順序 Order | 依良基大小或結構關係歸納。 |
| 正確性與終止 Correctness | 歸納假設只適用於較小子問題；仍須檢查分解與合併完整性。 |
| 成本 Cost | 證明本身不改變執行成本；總時間仍須加總分解與合併工作。 |

來源：

- [結構歸納法 (Structural Induction)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Proof_Techniques/Structural_Induction.md)

<a id="proof-exchange"></a>
### 211 · Exchange Argument／Staying Ahead／Cut Property

來源深度：既有論述延伸

**關鍵論述：** 貪婪不是忽略未來，而是證明未來總能配合這次選擇。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 證明可以安全選取或替換候選。 |
| 狀態 State | 某個最優解、目前選擇與可交換部分。 |
| 轉換 Transition | 把最優解改成包含算法選擇且不變差的解。 |
| 計算順序 Order | 逐決策延伸證明，或逐前綴比較領先指標。 |
| 正確性與終止 Correctness | 交換必須保持可行性；指標領先還要能推到最终目標。 |
| 成本 Cost | 證明本身不增加執行成本，算法成本仍由實際操作計。 |

來源：

- [最小生成樹 (Minimum Spanning Tree) 核心理論：Cut Property](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Minimum_Spanning_Tree/01-Cut_Property_and_MST_Intro.md)
- [Problem Transformation Framework](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Transformation.md)
- [Greedy Algorithm Proofs：交換論證 (Exchange Argument)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Proof_Techniques/Exchange_Argument.md)

<a id="proof-amortized"></a>
### 212 · Aggregate／Amortized Analysis

來源深度：既有論述延伸

**關鍵論述：** 一輪可能很貴，但同一筆工作不會在每輪都重複發生。

| 框架 | 關鍵論述 |
| --- | --- |
| 目標 Goal | 計算整段執行中的總工作量。 |
| 狀態 State | 操作計數、未結算工作或勢能。 |
| 轉換 Transition | 為昂貴步驟配置先前儲存的信用，或直接數總次數。 |
| 計算順序 Order | 觀察完整操作序列而非只看單次最壞。 |
| 正確性與終止 Correctness | 每項進出次數須有界；攤銷保證與平均／隨機期望不同。 |
| 成本 Cost | 單調棧總 O(n)、堆 O(nlog n) 等界由總操作數推導。 |

來源：

- [BFS 複雜度分析 (Complexity Analysis)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/03-BFS_Complexity_Analysis.md)
- [心法：容器型頂點的複雜度分析 (Complexity Analysis for Container Vertices)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/04-Container_Vertex_Complexity_Analysis.md)
- [DFS 複雜度分析：通用模型（圖與樹的比較）](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/02-DFS_Complexity_Analysis.md)
- [心法：堆與貪婪策略的時間複雜度：聚合分析 (Aggregate Analysis)](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/06-Amortized_Analysis.md)

## 適用條件校正與概念邊界

以下是本次重新詮釋時補上的條件；原始筆記保留，未在此工作中逐篇改寫。

| 主題 | 本筆記採用的精確說法 | 原始筆記 |
| --- | --- | --- |
| Constraint Connectivity | 每條邊各自符合門檻可形成固定子圖；路徑總成本限制需要成本標籤、資源狀態或相應最短路證明。 | [Constraint_Connectivity](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Constraint_Connectivity.md) |
| State-Space BFS 支配 | 同位置剩餘資源較多，只有在抵達成本不大且多資源不會傷害未來時才構成支配。 | [State_Space_BFS](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/State_Space_BFS.md) |
| Greedy 的未來影響 | 貪婪決策仍會影響未來；安全性由交換或其他證明支持。 | [01-Problem_Forms](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Fundamentals/01-Problem_Forms.md) |
| 樹高與平衡 | 一般二元樹最壞高度為 n−1 條邊。AVL、紅黑樹、Treap、Splay 的平衡與成本保證不同。 | [Height_Balanced_BST](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Height_Balanced_BST.md) |
| C++ hash 的碰撞 | 不能把其他語言的桶樹化實作當成 C++ unordered 容器保證；一般最壞查找仍可為線性。 | [Height_Balanced_BST](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Height_Balanced_BST.md) |
| DFS 分層輸出 | 用 depth 分桶可產生層序結果，但 DFS 的實際訪問順序不會因此先完成所有淺層節點。 | [DFS_for_Level_Order_Traversal](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/DFS_for_Level_Order_Traversal.md) |
| 樹的規範化 | 子節點根值相同不代表子樹相同；要用完整結構簽名、排序規則或可靠的唯一編號。 | [Canonical_Forms_Transformation](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Trees/Canonical_Forms_Transformation.md) |
| 狀態分解 | AND 對應 max、OR 對應 min 只適用於某些門檻／成本模型，並非布林與最佳化的通則。 | [State_Decomposition](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/State_Decomposition.md) |
| 名詞邊界 | 樹中心 center 與重心 centroid 不同；無向橋問題與有向 SCC 不同；Knuth 優化與一般 D&C DP 優化也不同。 | [Hard_Techniques_Reference](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md) |
| 窗口模板 | 最長可行窗與最短覆蓋窗的答案更新時機不同，需按目標決定。 | [00-Sliding_Window_Standard_Template](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sliding_Window/00-Sliding_Window_Standard_Template.md) |

## 覆蓋對照表

盤點固定於 `96da0e3865c116340a3c4843ef4eed38399f63b1`。所有 214 份 Algorithms／Data_Structures 筆記都有至少一個對應條目。檔案覆蓋不等於每個程式變體都有獨立章節；同契約變體、別名與 API 包裝依主題整併。下表列出全部 295 份 Markdown 的去向，讓遺漏與未來新增項目可被檢查。

| 來源筆記 | 本文對應／處理方式 |
| --- | --- |
| [Algorithms/BFS/01-Level_Ordering_Level_in_Queue.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/01-Level_Ordering_Level_in_Queue.md) | [BFS／Level Order／Level in Queue](#bfs) |
| [Algorithms/BFS/02-BFS_Tree_vs_Graph.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/02-BFS_Tree_vs_Graph.md) | [BFS／Level Order／Level in Queue](#bfs) |
| [Algorithms/BFS/03-BFS_Complexity_Analysis.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/03-BFS_Complexity_Analysis.md) | [BFS／Level Order／Level in Queue](#bfs)、[Aggregate／Amortized Analysis](#proof-amortized) |
| [Algorithms/BFS/04-Container_Vertex_Complexity_Analysis.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/04-Container_Vertex_Complexity_Analysis.md) | [BFS／Level Order／Level in Queue](#bfs)、[Aggregate／Amortized Analysis](#proof-amortized) |
| [Algorithms/BFS/BFS_Vertex_Mapping_Pattern.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/BFS_Vertex_Mapping_Pattern.md) | [Implicit Graph／Vertex Mapping](#implicit-graph)、[BFS／Level Order／Level in Queue](#bfs) |
| [Algorithms/BFS/MultiSource_BFS_Thinking_Framework.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/MultiSource_BFS_Thinking_Framework.md) | [BFS／Level Order／Level in Queue](#bfs)、[Multi-source BFS／Super Source](#multi-bfs) |
| [Algorithms/BFS/State_Space_BFS.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/BFS/State_Space_BFS.md) | [BFS／Level Order／Level in Queue](#bfs)、[State-Space BFS／資源支配剪枝](#state-bfs)、[0-1 BFS](#zero-one) |
| [Algorithms/Backtracking/01-Backtracking_Templates_and_Patterns.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/01-Backtracking_Templates_and_Patterns.md) | [Backtracking／候選建模](#backtracking) |
| [Algorithms/Backtracking/02-Backtracking_Problem_Solving_Framework.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/02-Backtracking_Problem_Solving_Framework.md) | [Backtracking／候選建模](#backtracking) |
| [Algorithms/Backtracking/03-Backtracking_Candidate_Modeling.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/03-Backtracking_Candidate_Modeling.md) | [Backtracking／候選建模](#backtracking) |
| [Algorithms/Backtracking/04-State_and_Solution_Design.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/04-State_and_Solution_Design.md) | [Backtracking／候選建模](#backtracking) |
| [Algorithms/Backtracking/05-State_Space_Tree_and_N_Tuple_Representation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/05-State_Space_Tree_and_N_Tuple_Representation.md) | [Backtracking／候選建模](#backtracking)、[Permutation／Combination／Subset Enumeration](#permutation-enumeration) |
| [Algorithms/Backtracking/06-DFS_vs_Backtracking_Pruning.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/06-DFS_vs_Backtracking_Pruning.md) | [Backtracking／候選建模](#backtracking)、[Pruning／Branch and Bound](#branch-bound) |
| [Algorithms/Backtracking/Backtracking_on_cpp_vector_Playbook.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/Backtracking_on_cpp_vector_Playbook.md) | [Permutation／Combination／Subset Enumeration](#permutation-enumeration)、[Swap 作為原地狀態管理](#swap-state) |
| [Algorithms/Backtracking/Duplicate_Removal_Pruning_Design.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/Duplicate_Removal_Pruning_Design.md) | [Duplicate Removal／對稱去重](#dedup) |
| [Algorithms/Backtracking/Swap_as_In_Place_State_Management.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Backtracking/Swap_as_In_Place_State_Management.md) | [Swap 作為原地狀態管理](#swap-state) |
| [Algorithms/Binary_Search/01-Binary_Search_Template.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Binary_Search/01-Binary_Search_Template.md) | [Binary Search／Lower Bound／Upper Bound](#binary-search) |
| [Algorithms/Binary_Search/02-Binary_Search_Comprehensive_Guide.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Binary_Search/02-Binary_Search_Comprehensive_Guide.md) | [Binary Search／Lower Bound／Upper Bound](#binary-search) |
| [Algorithms/Binary_Search/03-Deep_Dive_Existence_Positioning_Duplicates.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Binary_Search/03-Deep_Dive_Existence_Positioning_Duplicates.md) | [Binary Search／Lower Bound／Upper Bound](#binary-search) |
| [Algorithms/Binary_Search/04-Binary_Search_on_Solution_Space.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Binary_Search/04-Binary_Search_on_Solution_Space.md) | [Binary Search on Answer／Constraint](#binary-answer) |
| [Algorithms/Binary_Search/05-Binary_Search_on_Constraint.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Binary_Search/05-Binary_Search_on_Constraint.md) | [Constraint Connectivity](#constraint-reach)、[Binary Search on Answer／Constraint](#binary-answer) |
| [Algorithms/Binary_Search/07-Inflection_Point_Binary_Search.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Binary_Search/07-Inflection_Point_Binary_Search.md) | [Peak／Rotated Search／結構二分](#inflection) |
| [Algorithms/Bit_Manipulation/01-Bit_Manipulation_Playbook.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Bit_Manipulation/01-Bit_Manipulation_Playbook.md) | [Bit Manipulation／Bitmask Set／Bitset](#bitwise) |
| [Algorithms/Bit_Manipulation/02-Bitmask_Set_Operations.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Bit_Manipulation/02-Bitmask_Set_Operations.md) | [Bit Manipulation／Bitmask Set／Bitset](#bitwise) |
| [Algorithms/Bit_Manipulation/03-State_Compression.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Bit_Manipulation/03-State_Compression.md) | [Bitmask DP／Subset DP](#bitmask-dp) |
| [Algorithms/Bit_Manipulation/05-Sign_Extension_Trap.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Bit_Manipulation/05-Sign_Extension_Trap.md) | [Bit Manipulation／Bitmask Set／Bitset](#bitwise) |
| [Algorithms/Bit_Manipulation/06-Bit_Manipulation_CPP_STL.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Bit_Manipulation/06-Bit_Manipulation_CPP_STL.md) | [Bit Manipulation／Bitmask Set／Bitset](#bitwise) |
| [Algorithms/Bit_Manipulation/99-Case_Bitwise_Addition.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Bit_Manipulation/99-Case_Bitwise_Addition.md) | [Bitwise Addition](#bit-add) |
| [Algorithms/Bit_Manipulation/99-Case_Shift_UB_Pitfall.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Bit_Manipulation/99-Case_Shift_UB_Pitfall.md) | [Bit Manipulation／Bitmask Set／Bitset](#bitwise) |
| [Algorithms/Boyer_Moore_Voting/Boyer_Moore_Voting_Algorithm.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Boyer_Moore_Voting/Boyer_Moore_Voting_Algorithm.md) | [Boyer–Moore Voting／Majority Cancellation](#boyer-moore) |
| [Algorithms/DFS/01-DFS_Tree_vs_Graph.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/01-DFS_Tree_vs_Graph.md) | [DFS／Flood Fill／Connected Components](#dfs) |
| [Algorithms/DFS/02-DFS_Complexity_Analysis.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/02-DFS_Complexity_Analysis.md) | [DFS／Flood Fill／Connected Components](#dfs)、[Aggregate／Amortized Analysis](#proof-amortized) |
| [Algorithms/DFS/03-Node_Coloring_DFS.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/03-Node_Coloring_DFS.md) | [DFS／Flood Fill／Connected Components](#dfs)、[Node Coloring／有向環偵測](#node-color) |
| [Algorithms/DFS/04-DFS_with_Recursion_Design.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/04-DFS_with_Recursion_Design.md) | [DFS／Flood Fill／Connected Components](#dfs) |
| [Algorithms/DFS/05-IterativeDFS_Tree_vs_Graph.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/05-IterativeDFS_Tree_vs_Graph.md) | [DFS／Flood Fill／Connected Components](#dfs) |
| [Algorithms/DFS/06-One-Liner_DFS_Pattern.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/06-One-Liner_DFS_Pattern.md) | [DFS／Flood Fill／Connected Components](#dfs) |
| [Algorithms/DFS/Hierholzers/01-Hierholzers_Core_Concepts.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/Hierholzers/01-Hierholzers_Core_Concepts.md) | [DFS／Flood Fill／Connected Components](#dfs)、[Hierholzer／Eulerian Path](#hierholzer) |
| [Algorithms/DFS/Hierholzers/02-Node_vs_Edge_Based_Implementation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/DFS/Hierholzers/02-Node_vs_Edge_Based_Implementation.md) | [DFS／Flood Fill／Connected Components](#dfs)、[Hierholzer／Eulerian Path](#hierholzer) |
| [Algorithms/Design_Principles/Bidirectional_Constraint_Decomposition.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Bidirectional_Constraint_Decomposition.md) | [維度吸收／State Decomposition](#state-reduction)、[Running State／Prefix–Suffix Aggregation](#running-state) |
| [Algorithms/Design_Principles/Boundary_Driven_Processing.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Boundary_Driven_Processing.md) | [Boundary-Driven Processing](#boundary) |
| [Algorithms/Design_Principles/Recursion/01-Recursion_Design_Principles.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Recursion/01-Recursion_Design_Principles.md) | [Recursion 遞迴](#recursion) |
| [Algorithms/Design_Principles/Recursion/02-Temporal_Patterns_in_Algorithms.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Recursion/02-Temporal_Patterns_in_Algorithms.md) | [Recursion 遞迴](#recursion) |
| [Algorithms/Design_Principles/Recursion/03-Advanced_Recursion_Playbook.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Recursion/03-Advanced_Recursion_Playbook.md) | [Recursion 遞迴](#recursion) |
| [Algorithms/Design_Principles/Recursion/04-Top_Down_vs_Bottom_Up_Recursion.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Recursion/04-Top_Down_vs_Bottom_Up_Recursion.md) | [Recursion 遞迴](#recursion) |
| [Algorithms/Design_Principles/Recursion/State_Design_Across_Recursive_Paradigms.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Recursion/State_Design_Across_Recursive_Paradigms.md) | [Recursion 遞迴](#recursion) |
| [Algorithms/Design_Principles/Sequential_Phase_Consumption.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Sequential_Phase_Consumption.md) | [DFA／有限狀態機](#dfa)、[Sequential Phase Consumption](#phase) |
| [Algorithms/Design_Principles/Time_Space_Tradeoff_Patterns.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Time_Space_Tradeoff_Patterns.md) | [Preprocessing／Offline／Coordinate Compression](#preprocess) |
| [Algorithms/Design_Principles/Transformation_Patterns/Destination_as_Source_Reachability.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Transformation_Patterns/Destination_as_Source_Reachability.md) | [Destination-as-Source／反向可達性](#reverse-reach) |
| [Algorithms/Design_Principles/Transformation_Patterns/Movement_Constraint_Transformation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Transformation_Patterns/Movement_Constraint_Transformation.md) | [Movement Constraint Transformation](#movement) |
| [Algorithms/Design_Principles/Transformation_Patterns/Transforming_Constraints_into_Tools.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Design_Principles/Transformation_Patterns/Transforming_Constraints_into_Tools.md) | [Remaining Budget／限制吸收](#remaining-budget) |
| [Algorithms/Divide_and_Conquer/01_Divide_and_Conquer_Design_Strategy.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/01_Divide_and_Conquer_Design_Strategy.md) | [Divide & Conquer：Divide／Combine-centric](#divide-conquer)、[Closest Pair 分治](#closest-pair) |
| [Algorithms/Divide_and_Conquer/02_Divide_and_Conquer_vs_Dynamic_Programming.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/02_Divide_and_Conquer_vs_Dynamic_Programming.md) | [Divide & Conquer：Divide／Combine-centric](#divide-conquer)、[Fast Power／Binary Exponentiation](#fast-power)、[Closest Pair 分治](#closest-pair)、[Convex Hull／凸包建構](#convex-hull) |
| [Algorithms/Divide_and_Conquer/03_Interval_Design_in_Divide_and_Conquer.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/03_Interval_Design_in_Divide_and_Conquer.md) | [Divide & Conquer：Divide／Combine-centric](#divide-conquer) |
| [Algorithms/Divide_and_Conquer/04_Bottom_Up_Divide_and_Conquer.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/04_Bottom_Up_Divide_and_Conquer.md) | [Bottom-up Divide & Conquer](#bottom-up-dc)、[Merge Sort／穩定合併](#merge-sort) |
| [Algorithms/Divide_and_Conquer/05_Conquer_Strategy_Comparison.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/05_Conquer_Strategy_Comparison.md) | [Divide & Conquer：Divide／Combine-centric](#divide-conquer)、[External State／雙軌遍歷](#external-state) |
| [Algorithms/Divide_and_Conquer/06_External_State_Traversal_Order.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/06_External_State_Traversal_Order.md) | [External State／雙軌遍歷](#external-state) |
| [Algorithms/Divide_and_Conquer/07_Merge_Sort_Variants_Pattern.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/07_Merge_Sort_Variants_Pattern.md) | [Merge Sort Variants／跨區間計數](#merge-count) |
| [Algorithms/Divide_and_Conquer/Decision_Tree/01-Definition.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/Decision_Tree/01-Definition.md) | [Decision Tree 學習與推論](#decision-tree) |
| [Algorithms/Divide_and_Conquer/Decision_Tree/02-Implementation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/Decision_Tree/02-Implementation.md) | [Decision Tree 學習與推論](#decision-tree) |
| [Algorithms/Divide_and_Conquer/Decision_Tree/03-Splitting_Criterion.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/Decision_Tree/03-Splitting_Criterion.md) | [Decision Tree 學習與推論](#decision-tree) |
| [Algorithms/Divide_and_Conquer/Decision_Tree/04-Evaluation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Divide_and_Conquer/Decision_Tree/04-Evaluation.md) | [Decision Tree 學習與推論](#decision-tree) |
| [Algorithms/Dynamic_Programming/Advanced_Techniques/Bellman-Ford/01-DP_Foundations_of_Bellman-Ford.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/Bellman-Ford/01-DP_Foundations_of_Bellman-Ford.md) | [Bellman-Ford／負環偵測](#bellman-ford) |
| [Algorithms/Dynamic_Programming/Advanced_Techniques/Bellman-Ford/02-Standard_Bellman-Ford_Algorithm.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/Bellman-Ford/02-Standard_Bellman-Ford_Algorithm.md) | [Bellman-Ford／負環偵測](#bellman-ford) |
| [Algorithms/Dynamic_Programming/Advanced_Techniques/Bellman-Ford/03-SPFA_Optimization.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/Bellman-Ford/03-SPFA_Optimization.md) | [SPFA](#spfa) |
| [Algorithms/Dynamic_Programming/Advanced_Techniques/Bellman-Ford/04-Negative_Cycle_Detection.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/Bellman-Ford/04-Negative_Cycle_Detection.md) | [Bellman-Ford／負環偵測](#bellman-ford) |
| [Algorithms/Dynamic_Programming/Advanced_Techniques/Kadane_Algorithm.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/Kadane_Algorithm.md) | [Kadane／Ending-at-i Pattern](#kadane) |
| [Algorithms/Dynamic_Programming/Advanced_Techniques/Kadanes_Pattern_DP.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/Kadanes_Pattern_DP.md) | [局部狀態與全域答案](#local-global)、[Kadane／Ending-at-i Pattern](#kadane) |
| [Algorithms/Dynamic_Programming/Advanced_Techniques/State_Decomposition.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Advanced_Techniques/State_Decomposition.md) | [維度吸收／State Decomposition](#state-reduction) |
| [Algorithms/Dynamic_Programming/Fundamentals/01-Problem_Forms.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Fundamentals/01-Problem_Forms.md) | [Dynamic Programming／Memoization／Tabulation](#dp) |
| [Algorithms/Dynamic_Programming/Fundamentals/02-Problem_Solving_Framework.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Fundamentals/02-Problem_Solving_Framework.md) | [Dynamic Programming／Memoization／Tabulation](#dp) |
| [Algorithms/Dynamic_Programming/Fundamentals/03-TopDown_to_BottomUp.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Fundamentals/03-TopDown_to_BottomUp.md) | [Dynamic Programming／Memoization／Tabulation](#dp)、[Rolling Array／Space-Optimized DP](#rolling-dp) |
| [Algorithms/Dynamic_Programming/Fundamentals/04-Recurrence_Design_Patterns.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Fundamentals/04-Recurrence_Design_Patterns.md) | [Dynamic Programming／Memoization／Tabulation](#dp)、[1D Sequence DP／固定與動態範圍依賴](#sequence-dp)、[State Machine DP／Stock／Profile DP](#state-machine-dp) |
| [Algorithms/Dynamic_Programming/Fundamentals/Concept_DP_as_Graph_Traversal.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Fundamentals/Concept_DP_as_Graph_Traversal.md) | [Dynamic Programming／Memoization／Tabulation](#dp) |
| [Algorithms/Dynamic_Programming/Implementation/Boundary_Condition_Handling.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Implementation/Boundary_Condition_Handling.md) | [Dynamic Programming／Memoization／Tabulation](#dp) |
| [Algorithms/Dynamic_Programming/Implementation/Caching_Strategies.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Implementation/Caching_Strategies.md) | [Dynamic Programming／Memoization／Tabulation](#dp) |
| [Algorithms/Dynamic_Programming/Implementation/Common_Pitfalls.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Implementation/Common_Pitfalls.md) | [Dynamic Programming／Memoization／Tabulation](#dp) |
| [Algorithms/Dynamic_Programming/Problem_Types/Counting_DP.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Problem_Types/Counting_DP.md) | [Counting DP／排列與組合計數](#counting-dp)、[Unbounded Knapsack／Coin Change](#unbounded-knapsack) |
| [Algorithms/Dynamic_Programming/Problem_Types/Matrix_DP.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Problem_Types/Matrix_DP.md) | [Floyd-Warshall](#floyd-warshall)、[2D／Matrix／Grid DP](#matrix-dp) |
| [Algorithms/Dynamic_Programming/Problem_Types/Multi_Dimensional_DP.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Problem_Types/Multi_Dimensional_DP.md) | [Multi-dimensional Knapsack／差值狀態](#multi-knapsack) |
| [Algorithms/Dynamic_Programming/State_Design/01-Essentials.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/State_Design/01-Essentials.md) | [Dynamic Programming／Memoization／Tabulation](#dp) |
| [Algorithms/Dynamic_Programming/State_Design/02-From_Solution_Properties.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/State_Design/02-From_Solution_Properties.md) | [Dynamic Programming／Memoization／Tabulation](#dp)、[Counting DP／排列與組合計數](#counting-dp)、[Unbounded Knapsack／Coin Change](#unbounded-knapsack) |
| [Algorithms/Dynamic_Programming/State_Design/03-On_Value_Space.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/State_Design/03-On_Value_Space.md) | [Value-Space DP／Group by Value](#value-dp) |
| [Algorithms/Dynamic_Programming/State_Design/04-State_Reduction.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/State_Design/04-State_Reduction.md) | [Rolling Array／Space-Optimized DP](#rolling-dp)、[維度吸收／State Decomposition](#state-reduction)、[Bitmask DP／Subset DP](#bitmask-dp) |
| [Algorithms/Dynamic_Programming/State_Design/05-Local_State_vs_Global_Optimum.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/State_Design/05-Local_State_vs_Global_Optimum.md) | [局部狀態與全域答案](#local-global) |
| [Algorithms/Dynamic_Programming/Subset_Sum/01-Subset_Sum_and_NP_Completeness.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Subset_Sum/01-Subset_Sum_and_NP_Completeness.md) | [0/1 Knapsack／Subset Sum](#knapsack01) |
| [Algorithms/Dynamic_Programming/Subset_Sum/02-Implementation_Guide.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Dynamic_Programming/Subset_Sum/02-Implementation_Guide.md) | [0/1 Knapsack／Subset Sum](#knapsack01) |
| [Algorithms/Greedy/Dijkstra's Algorithm/01-Dijkstra_Algorithm_Guide.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Dijkstra%27s%20Algorithm/01-Dijkstra_Algorithm_Guide.md) | [Dijkstra／Lazy Deletion](#dijkstra)、[Fibonacci Heap](#fibonacci-heap) |
| [Algorithms/Greedy/Dijkstra's Algorithm/02-Dijkstra_Deep_Dive.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Dijkstra%27s%20Algorithm/02-Dijkstra_Deep_Dive.md) | [Dijkstra／Lazy Deletion](#dijkstra) |
| [Algorithms/Greedy/Dijkstra's Algorithm/03-Dijkstra_as_a_General_Search_Framework.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Dijkstra%27s%20Algorithm/03-Dijkstra_as_a_General_Search_Framework.md) | [廣義 Dijkstra：Bottleneck／Probability](#general-dijkstra) |
| [Algorithms/Greedy/Greedy_Identification_and_Application.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Greedy_Identification_and_Application.md) | [Greedy／Sort vs Heap](#greedy)、[Fractional Knapsack](#fractional-knapsack) |
| [Algorithms/Greedy/Greedy_Sort_vs_Heap.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Greedy_Sort_vs_Heap.md) | [Greedy／Sort vs Heap](#greedy) |
| [Algorithms/Greedy/Greedy_Sweep_Cost_Optimization_with_Top_K.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Greedy_Sweep_Cost_Optimization_with_Top_K.md) | [Greedy Sweep + Top-K／Push–Pop Replacement](#topk-greedy) |
| [Algorithms/Greedy/Interval_Problem_Solving_Playbook.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Interval_Problem_Solving_Playbook.md) | [Interval Merge／Intersection／Scheduling](#interval-greedy) |
| [Algorithms/Greedy/MST_Algorithms/01-Kruskals_Algorithm.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/MST_Algorithms/01-Kruskals_Algorithm.md) | [Kruskal／Minimum Spanning Forest](#kruskal) |
| [Algorithms/Greedy/MST_Algorithms/02-Prims_Algorithm.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/MST_Algorithms/02-Prims_Algorithm.md) | [Prim／切割前沿](#prim) |
| [Algorithms/Greedy/Pivotal_Element_First_Greedy.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Pivotal_Element_First_Greedy.md) | [Pivotal-Element-First／關鍵限制優先](#pivotal)、[Two Heaps：可行性與收益選擇](#twoheap-selection) |
| [Algorithms/Greedy/Two_Heaps_Greedy_Selection.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Greedy/Two_Heaps_Greedy_Selection.md) | [Two Heaps：可行性與收益選擇](#twoheap-selection) |
| [Algorithms/Math/Find_Min_and_Second_Min_Trick.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Find_Min_and_Second_Min_Trick.md) | [Min／Second Min／Running Extremum](#min-second) |
| [Algorithms/Math/Integer_Division_Ceiling_Trick.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Integer_Division_Ceiling_Trick.md) | [整數邊界／Ceiling／Median Index](#integer-boundaries) |
| [Algorithms/Math/Median_Index_Calculation_with_Integer_Division.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Median_Index_Calculation_with_Integer_Division.md) | [整數邊界／Ceiling／Median Index](#integer-boundaries) |
| [Algorithms/Math/Modular_Arithmetic_A_Practical_Guide.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Modular_Arithmetic_A_Practical_Guide.md) | [Modular Arithmetic／餘數狀態](#modular) |
| [Algorithms/Math/Number_Theory/01-Primality_Test.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Number_Theory/01-Primality_Test.md) | [Trial Division／Primality Test](#prime-test)、[Sieve of Eratosthenes](#sieve) |
| [Algorithms/Math/Number_Theory/02-Prime_Factorization.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Number_Theory/02-Prime_Factorization.md) | [Prime Factorization／Divisor Count–Sum](#factorization) |
| [Algorithms/Math/Number_Theory/03-GCD_and_LCM.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Number_Theory/03-GCD_and_LCM.md) | [Euclidean Algorithm／GCD／LCM](#gcd) |
| [Algorithms/Math/Number_Theory/04-Number_Theory_Applications.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Math/Number_Theory/04-Number_Theory_Applications.md) | [Euclidean Algorithm／GCD／LCM](#gcd)、[Prime Factorization／Divisor Count–Sum](#factorization) |
| [Algorithms/Partition/01-Lomuto_Partition_Scheme.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Partition/01-Lomuto_Partition_Scheme.md) | [Lomuto Partition](#lomuto) |
| [Algorithms/Partition/README.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Partition/README.md) | [Hoare Partition](#hoare)、[Dutch National Flag／3-way Partition](#three-way) |
| [Algorithms/Prefix_Sum/01_Prefix_Sum_Intro.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Prefix_Sum/01_Prefix_Sum_Intro.md) | [Prefix Sum／2D–3D Prefix／Prefix XOR](#prefix) |
| [Algorithms/Prefix_Sum/02_Running_State_Pattern.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Prefix_Sum/02_Running_State_Pattern.md) | [Running State／Prefix–Suffix Aggregation](#running-state) |
| [Algorithms/Prefix_Sum/03_Prefix_Sum_with_Binary_Search.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Prefix_Sum/03_Prefix_Sum_with_Binary_Search.md) | [Prefix Sum + Binary Search](#prefix-binary) |
| [Algorithms/Prefix_Sum/04_Prefix_Sum_for_Counting_Sort.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Prefix_Sum/04_Prefix_Sum_for_Counting_Sort.md) | [Counting Sort](#counting-sort) |
| [Algorithms/Prefix_Sum/05_Difference_Array.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Prefix_Sum/05_Difference_Array.md) | [Difference Array／多維差分](#difference) |
| [Algorithms/Sliding_Window/00-Sliding_Window_Standard_Template.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sliding_Window/00-Sliding_Window_Standard_Template.md) | [Fixed Sliding Window](#fixed-window)、[Variable Sliding Window／Sorted Window](#variable-window) |
| [Algorithms/Sliding_Window/01-Constraint_Tracking_and_Optimization.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sliding_Window/01-Constraint_Tracking_and_Optimization.md) | [Fixed Sliding Window](#fixed-window)、[Variable Sliding Window／Sorted Window](#variable-window) |
| [Algorithms/Sliding_Window/02-Sorted_Sliding_Window.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sliding_Window/02-Sorted_Sliding_Window.md) | [Fixed Sliding Window](#fixed-window)、[Variable Sliding Window／Sorted Window](#variable-window) |
| [Algorithms/Sorting/01-Fundamentals_of_Sorting.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/01-Fundamentals_of_Sorting.md) | [Linear Scan／Find／Count／Transform／Fold](#linear-stl) |
| [Algorithms/Sorting/Comparison_Based_Sorting/01-Selection_Sort.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/01-Selection_Sort.md) | [Selection Sort](#selection-sort) |
| [Algorithms/Sorting/Comparison_Based_Sorting/02-Bubble_Sort.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/02-Bubble_Sort.md) | [Bubble Sort](#bubble-sort) |
| [Algorithms/Sorting/Comparison_Based_Sorting/03-Insertion_Sort.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/03-Insertion_Sort.md) | [Insertion Sort](#insertion-sort) |
| [Algorithms/Sorting/Comparison_Based_Sorting/04-Heap_Sort.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/04-Heap_Sort.md) | [Heap Sort](#heap-sort) |
| [Algorithms/Sorting/Comparison_Based_Sorting/05-Merge_Sort.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/05-Merge_Sort.md) | [Merge Sort／穩定合併](#merge-sort)、[Timsort／Natural Runs](#timsort) |
| [Algorithms/Sorting/Comparison_Based_Sorting/06-Quicksort.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/06-Quicksort.md) | [Quicksort／Pivot Selection](#quick-sort)、[Hoare Partition](#hoare) |
| [Algorithms/Sorting/Comparison_Based_Sorting/07-Quicksort_Advanced.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Comparison_Based_Sorting/07-Quicksort_Advanced.md) | [Quicksort／Pivot Selection](#quick-sort)、[Hoare Partition](#hoare)、[Dutch National Flag／3-way Partition](#three-way)、[Quickselect／Hoare Selection](#quickselect) |
| [Algorithms/Sorting/Non_Comparison_Based_Sorting/01-Counting_Sort.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Non_Comparison_Based_Sorting/01-Counting_Sort.md) | [Counting Sort](#counting-sort) |
| [Algorithms/Sorting/Non_Comparison_Based_Sorting/02-Radix_Sort.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/Non_Comparison_Based_Sorting/02-Radix_Sort.md) | [Radix Sort](#radix-sort) |
| [Algorithms/Sorting/cpp-introsort.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sorting/cpp-introsort.md) | [Introsort／std::sort 常見實作](#introsort) |
| [Algorithms/Sweep_Line/01-Sweep_Line_Core_Concepts.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sweep_Line/01-Sweep_Line_Core_Concepts.md) | [Sweep Line／重疊區間／Heap Simulation](#sweep) |
| [Algorithms/Sweep_Line/02-Maximum_Concurrent_Intervals.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sweep_Line/02-Maximum_Concurrent_Intervals.md) | [Sweep Line／重疊區間／Heap Simulation](#sweep) |
| [Algorithms/Sweep_Line/03-2D_Sweep_Line.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Sweep_Line/03-2D_Sweep_Line.md) | [2D Sweep／Rectangle Union／Skyline](#sweep2d) |
| [Algorithms/Topological_Sort/01-Core_Concepts_and_Applications.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Topological_Sort/01-Core_Concepts_and_Applications.md) | [Topological Sort／Kahn／DFS Postorder](#topological) |
| [Algorithms/Topological_Sort/02-Kahn_Algorithm_BFS.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Topological_Sort/02-Kahn_Algorithm_BFS.md) | [Topological Sort／Kahn／DFS Postorder](#topological) |
| [Algorithms/Topological_Sort/03-DFS_Based_Implementation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Topological_Sort/03-DFS_Based_Implementation.md) | [Node Coloring／有向環偵測](#node-color)、[Topological Sort／Kahn／DFS Postorder](#topological) |
| [Algorithms/Topological_Sort/04-Kahn_Algorithm_Variants.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Topological_Sort/04-Kahn_Algorithm_Variants.md) | [Leaf Peeling／樹中心](#leaf-peeling) |
| [Algorithms/Traversal_Strategies/DFS_vs_BFS_for_Connectivity.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Traversal_Strategies/DFS_vs_BFS_for_Connectivity.md) | [DFS／Flood Fill／Connected Components](#dfs) |
| [Algorithms/Traversal_Strategies/Graph_as_Tree_Traversal.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Traversal_Strategies/Graph_as_Tree_Traversal.md) | [DFS／Flood Fill／Connected Components](#dfs)、[無向圖環偵測與 Graph-as-Tree](#undirected-cycle) |
| [Algorithms/Two_Pointers/01-Two_Pointers_Core_Patterns_and_Templates.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Two_Pointers/01-Two_Pointers_Core_Patterns_and_Templates.md) | [Two Pointers／對向與同向指標](#two-pointers)、[Fast–Slow／Floyd Cycle Detection](#fast-slow)、[Adjacent Pointers／Read–Write Compaction](#adjacent) |
| [Algorithms/Two_Pointers/02_Fast_and_Slow_Pointers.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Two_Pointers/02_Fast_and_Slow_Pointers.md) | [Fast–Slow／Floyd Cycle Detection](#fast-slow) |
| [Algorithms/Two_Pointers/03_K_Gap_Pointers.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Two_Pointers/03_K_Gap_Pointers.md) | [K-Gap Pointers](#k-gap) |
| [Algorithms/Two_Pointers/04_Adjacent_Pointers.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Two_Pointers/04_Adjacent_Pointers.md) | [Adjacent Pointers／Read–Write Compaction](#adjacent) |
| [Algorithms/Two_Pointers/05_Skip_Based_Dual_Iterator.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Two_Pointers/05_Skip_Based_Dual_Iterator.md) | [Skip-Based Dual Iterator](#skip-iterator) |
| [Algorithms/Two_Pointers/06_Expand_Around_Center.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Two_Pointers/06_Expand_Around_Center.md) | [Expand Around Center](#center-expand) |
| [Algorithms/Union_Find/01-Core_Concepts.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/01-Core_Concepts.md) | [Union-Find／Disjoint Set Union](#dsu) |
| [Algorithms/Union_Find/02-Quick_Find.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/02-Quick_Find.md) | [Quick-Find](#quick-find) |
| [Algorithms/Union_Find/03-Quick_Union.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/03-Quick_Union.md) | [Quick-Union](#quick-union) |
| [Algorithms/Union_Find/04-Union_by_Rank.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/04-Union_by_Rank.md) | [Union by Rank／Size](#union-rank) |
| [Algorithms/Union_Find/05-Path_Compression.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/05-Path_Compression.md) | [Path Compression](#path-compression) |
| [Algorithms/Union_Find/06-Optimized_Implementation_and_Analysis.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/06-Optimized_Implementation_and_Analysis.md) | [Union-Find／Disjoint Set Union](#dsu) |
| [Algorithms/Union_Find/07-LeetCode_Tips.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/07-LeetCode_Tips.md) | [Union-Find／Disjoint Set Union](#dsu) |
| [Algorithms/Union_Find/08-Connectivity_Problem_Strategy_Guide.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/08-Connectivity_Problem_Strategy_Guide.md) | [Union-Find／Disjoint Set Union](#dsu) |
| [Algorithms/Union_Find/09-Reconstructing_Connected_Components.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/09-Reconstructing_Connected_Components.md) | [Union-Find／Disjoint Set Union](#dsu) |
| [Algorithms/Union_Find/10-Weighted_Union_Find_with_Path_Compression.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Algorithms/Union_Find/10-Weighted_Union_Find_with_Path_Compression.md) | [Weighted Union-Find／Potential DSU](#weighted-dsu) |
| [CLAUDE.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CLAUDE.md) | 組織與範圍依據；不另當作算法。 |
| [CPP_Reference/Algorithm/Accumulate_vs_Reduce.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Accumulate_vs_Reduce.md) | [Linear Scan／Find／Count／Transform／Fold](#linear-stl) |
| [CPP_Reference/Algorithm/Common_Algorithms_and_Utilities.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Common_Algorithms_and_Utilities.md) | [Linear Scan／Find／Count／Transform／Fold](#linear-stl) |
| [CPP_Reference/Algorithm/Custom_Comparators_with_Decltype.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Custom_Comparators_with_Decltype.md) | [Linear Scan／Find／Count／Transform／Fold](#linear-stl) |
| [CPP_Reference/Algorithm/Custom_Operation_Types.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Custom_Operation_Types.md) | [Linear Scan／Find／Count／Transform／Fold](#linear-stl) |
| [CPP_Reference/Algorithm/Lower_Upper_Bound_Explained.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Lower_Upper_Bound_Explained.md) | [Binary Search／Lower Bound／Upper Bound](#binary-search)、[Linear Scan／Find／Count／Transform／Fold](#linear-stl) |
| [CPP_Reference/Algorithm/Min_Max_Element_Usage.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Min_Max_Element_Usage.md) | [Min／Second Min／Running Extremum](#min-second)、[Linear Scan／Find／Count／Transform／Fold](#linear-stl) |
| [CPP_Reference/Algorithm/Partial_Sum_Usage.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Partial_Sum_Usage.md) | [Linear Scan／Find／Count／Transform／Fold](#linear-stl) |
| [CPP_Reference/Algorithm/Sort_Comparison.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Sort_Comparison.md) | [Introsort／std::sort 常見實作](#introsort)、[Timsort／Natural Runs](#timsort)、[Linear Scan／Find／Count／Transform／Fold](#linear-stl) |
| [CPP_Reference/Algorithm/Transform_Usage_Tip.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Algorithm/Transform_Usage_Tip.md) | [Linear Scan／Find／Count／Transform／Fold](#linear-stl) |
| [CPP_Reference/Common_Coding_Mistakes.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Common_Coding_Mistakes.md) | [Loop Invariant／契約與測試](#proof-invariant) |
| [CPP_Reference/Common_Coding_Mistakes/Binding_Temporaries_to_LValue_References.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Common_Coding_Mistakes/Binding_Temporaries_to_LValue_References.md) | [Loop Invariant／契約與測試](#proof-invariant) |
| [CPP_Reference/Common_Coding_Mistakes/Conditional_Operator_Braced_Init_List.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Common_Coding_Mistakes/Conditional_Operator_Braced_Init_List.md) | [Loop Invariant／契約與測試](#proof-invariant) |
| [CPP_Reference/Common_Coding_Mistakes/Std_Min_Max_Type_Mismatch.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Common_Coding_Mistakes/Std_Min_Max_Type_Mismatch.md) | [Loop Invariant／契約與測試](#proof-invariant) |
| [CPP_Reference/Container/Common_Container_APIs.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Common_Container_APIs.md) | [Array／Vector／String](#array)、[Singly／Doubly Linked List](#linked-list)、[Stack／Min Stack](#stack)、[Queue／Deque](#queue-deque) |
| [CPP_Reference/Container/Const_Map_and_Operator_Bracket.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Const_Map_and_Operator_Bracket.md) | [Hash Table／Hash Map／Hash Set](#hash) |
| [CPP_Reference/Container/Container_Conversion_Techniques.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Container_Conversion_Techniques.md) | [Preprocessing／Offline／Coordinate Compression](#preprocess) |
| [CPP_Reference/Container/Container_Iteration_Order.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Container_Iteration_Order.md) | [Hash Table／Hash Map／Hash Set](#hash)、[Ordered Map／Set／Multiset](#ordered-map) |
| [CPP_Reference/Container/Container_Selection_Guide.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Container_Selection_Guide.md) | [Hash Table／Hash Map／Hash Set](#hash)、[Ordered Map／Set／Multiset](#ordered-map) |
| [CPP_Reference/Container/Custom_Hasher_For_Unordered_Containers.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Custom_Hasher_For_Unordered_Containers.md) | [Hash Table／Hash Map／Hash Set](#hash) |
| [CPP_Reference/Container/Deque_vs_Queue.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Deque_vs_Queue.md) | [Queue／Deque](#queue-deque) |
| [CPP_Reference/Container/Operator_Bracket_Behavior_Vector_vs_Map.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Operator_Bracket_Behavior_Vector_vs_Map.md) | [Hash Table／Hash Map／Hash Set](#hash) |
| [CPP_Reference/Container/Priority_Queue_Usage.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/Priority_Queue_Usage.md) | [Binary Heap／Priority Queue／Heapify](#heap) |
| [CPP_Reference/Container/String_Building_Patterns.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Container/String_Building_Patterns.md) | [Array／Vector／String](#array) |
| [CPP_Reference/Type/ASCII_for_LeetCode.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Type/ASCII_for_LeetCode.md) | [整數邊界／Ceiling／Median Index](#integer-boundaries) |
| [CPP_Reference/Type/Char_Int_Conversion.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Type/Char_Int_Conversion.md) | [整數邊界／Ceiling／Median Index](#integer-boundaries) |
| [CPP_Reference/Type/Char_vs_Int_in_Conditionals.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Type/Char_vs_Int_in_Conditionals.md) | [整數邊界／Ceiling／Median Index](#integer-boundaries) |
| [CPP_Reference/Type/Double_to_Integer_Verification.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Type/Double_to_Integer_Verification.md) | [整數邊界／Ceiling／Median Index](#integer-boundaries) |
| [CPP_Reference/Type/Floating_Point_and_Scientific_Notation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Type/Floating_Point_and_Scientific_Notation.md) | [整數邊界／Ceiling／Median Index](#integer-boundaries) |
| [CPP_Reference/Type/Integer_Overflow_Prevention.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Type/Integer_Overflow_Prevention.md) | [整數邊界／Ceiling／Median Index](#integer-boundaries) |
| [CPP_Reference/Type/Min_Max_Initialization.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/CPP_Reference/Type/Min_Max_Initialization.md) | [整數邊界／Ceiling／Median Index](#integer-boundaries) |
| [Cheatsheet/CPP_One_Liners.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/CPP_One_Liners.md) | [Next Permutation](#next-permutation)、[Linear Scan／Find／Count／Transform／Fold](#linear-stl)、[Fisher–Yates Shuffle](#fisher-yates) |
| [Cheatsheet/Gary's DSA Cheatsheet.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/Gary%27s%20DSA%20Cheatsheet.md) | 已盤點；題單／索引中的同名技巧併入本文對應算法，不替未說明的題目推定解法。 |
| [Cheatsheet/LeetCode_Tricks_and_Keywords.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Cheatsheet/LeetCode_Tricks_and_Keywords.md) | [無向圖環偵測與 Graph-as-Tree](#undirected-cycle)、[Leaf Peeling／樹中心](#leaf-peeling)、[LCS／Edit Distance／雙序列 DP](#lcs-edit)、[Next Permutation](#next-permutation)、[Reachable Range／Greedy Frontier](#range-greedy)、[K-way Merge／Heap Frontier](#merge-k)、[BST Iterator／受控遍歷](#bst-iterator)、[Dynamic Trie／Backtracking + Trie](#dynamic-trie)、[LRU Cache](#lru)、[Nim／有限取石遊戲的勝負狀態](#nim)、[Coordinate Mapping／Matrix In-place Marking](#coordinate)、[Manacher](#manacher) |
| [Checklists/Algorithm_Techniques_Checklist.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Algorithm_Techniques_Checklist.md) | [Quickselect／Hoare Selection](#quickselect)、[Bucket Sort](#bucket-sort)、[Dummy Node／Linked List Reversal](#dummy-reverse)、[Dynamic Trie／Backtracking + Trie](#dynamic-trie)、[Segment Tree](#segment-tree) |
| [Checklists/Essential Problems/Archetype_Problems.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Archetype_Problems.md) | [State Machine DP／Stock／Profile DP](#state-machine-dp) |
| [Checklists/Essential Problems/Essential_Problems.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Essential_Problems.md) | [Brute Force／Exhaustive Enumeration](#brute-force)、[Bitwise State Machine／Modulo Counter](#bit-fsm) |
| [Checklists/Essential Problems/Problem_Review.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Problem_Review.md) | [Bitwise State Machine／Modulo Counter](#bit-fsm)、[Bitwise Prefixes + Hash Set](#bit-prefix)、[2D Fenwick Tree](#fenwick2d)、[Bucket Window／值差限制](#bucket-window)、[Two-Stack Postorder](#two-stack-postorder)、[Nested Parsing／Two Stacks](#parser-stack)、[Circular Subarray／補集最佳化](#circular-kadane) |
| [Checklists/Essential Problems/Technique_Integration_Problems.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Essential%20Problems/Technique_Integration_Problems.md) | [Exactly K = At Most K − At Most K−1](#at-most)、[Prefix Sum + Hash Map](#prefix-hash)、[Sweep Line／重疊區間／Heap Simulation](#sweep)、[2D Sweep／Rectangle Union／Skyline](#sweep2d)、[Interval Merge／Intersection／Scheduling](#interval-greedy)、[Weighted Interval Scheduling／DP + Binary Search](#weighted-scheduling)、[K-way Merge／Heap Frontier](#merge-k)、[Monotonic Deque／Window Extremum](#monoqueue)、[Tree Serialization／Deserialization](#serialization)、[LRU Cache](#lru)、[LFU Cache](#lfu)、[Preprocessing／Offline／Coordinate Compression](#preprocess)、[Median + Prefix Sum／L1 Cost](#median-cost) |
| [Checklists/Learning_Roadmap.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Learning_Roadmap.md) | [DFA／有限狀態機](#dfa)、[Quickselect／Hoare Selection](#quickselect)、[Bucket Sort](#bucket-sort)、[Chaining／Open Addressing／2-Choice Hashing](#hash-collision)、[Tree Canonical Form／Merkle Hashing](#canonical-tree)、[Min-Max Heap](#minmax-heap)、[Deap／Double-Ended Heap](#deap)、[Matrix Exponentiation](#matrix-power)、[Binomial／Factorial／Catalan Counting](#combinatorics)、[A* Search](#a-star) |
| [Checklists/Lists/00_Master_Union.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Lists/00_Master_Union.md) | 已盤點；題單／索引中的同名技巧併入本文對應算法，不替未說明的題目推定解法。 |
| [Checklists/Lists/01_Grind75_Easy_Warmup.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Lists/01_Grind75_Easy_Warmup.md) | 已盤點；題單／索引中的同名技巧併入本文對應算法，不替未說明的題目推定解法。 |
| [Checklists/Lists/Grind_75.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Lists/Grind_75.md) | 已盤點；題單／索引中的同名技巧併入本文對應算法，不替未說明的題目推定解法。 |
| [Checklists/Lists/NeetCode_150.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Lists/NeetCode_150.md) | [Stack／Min Stack](#stack) |
| [Checklists/Lists/Top_100_Liked.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Lists/Top_100_Liked.md) | 已盤點；題單／索引中的同名技巧併入本文對應算法，不替未說明的題目推定解法。 |
| [Checklists/Lists/Top_Interview_150.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Lists/Top_Interview_150.md) | 已盤點；題單／索引中的同名技巧併入本文對應算法，不替未說明的題目推定解法。 |
| [Checklists/Practice_Log.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Practice_Log.md) | [State Machine DP／Stock／Profile DP](#state-machine-dp) |
| [Checklists/Super_Hard/004_Median_of_Two_Sorted_Arrays.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Super_Hard/004_Median_of_Two_Sorted_Arrays.md) | [Binary Search on Partition](#binary-partition) |
| [Checklists/Super_Hard/032_Longest_Valid_Parentheses.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Super_Hard/032_Longest_Valid_Parentheses.md) | [Kadane／Ending-at-i Pattern](#kadane)、[Brute Force／Exhaustive Enumeration](#brute-force)、[Parenthesis Matching／Invalid Boundary Stack](#parenthesis-stack)、[Bidirectional Balance Scan](#parenthesis-two-scan) |
| [Checklists/Trick Practice/Binary_Search_on_Answer_Playbook.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Binary_Search_on_Answer_Playbook.md) | [Binary Search on Answer／Constraint](#binary-answer) |
| [Checklists/Trick Practice/Divide_and_Conquer_Hard_Problem_Playbook.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Divide_and_Conquer_Hard_Problem_Playbook.md) | [Merge Sort Variants／跨區間計數](#merge-count) |
| [Checklists/Trick Practice/KMP_String_Matching_Playbook.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/KMP_String_Matching_Playbook.md) | [KMP／Prefix Function](#kmp)、[Z-function／Z-algorithm](#z-function) |
| [Checklists/Trick Practice/Kadanes_Pattern_DP_Playbook.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Kadanes_Pattern_DP_Playbook.md) | [局部狀態與全域答案](#local-global)、[Kadane／Ending-at-i Pattern](#kadane)、[Maximum Product／雙極值摘要](#max-product)、[Interval DP／Palindrome DP](#interval-dp) |
| [Checklists/Trick Practice/Knapsack_Variations_Playbook.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Knapsack_Variations_Playbook.md) | [0/1 Knapsack／Subset Sum](#knapsack01)、[Multi-dimensional Knapsack／差值狀態](#multi-knapsack) |
| [Checklists/Trick Practice/Sequential_Phase_Consumption_Playbook.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Sequential_Phase_Consumption_Playbook.md) | [Sequential Phase Consumption](#phase) |
| [Checklists/Trick Practice/Sliding_Window_Frequency_Matching_Playbook.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Checklists/Trick%20Practice/Sliding_Window_Frequency_Matching_Playbook.md) | [Fixed Sliding Window](#fixed-window)、[Frequency Matching／Counting Invariant](#frequency-window)、[Exactly K = At Most K − At Most K−1](#at-most) |
| [Data_Structures/Advanced/Binary_Indexed_Tree/01-Core_Concepts.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Advanced/Binary_Indexed_Tree/01-Core_Concepts.md) | [Fenwick Tree／Binary Indexed Tree](#fenwick)、[Segment Tree](#segment-tree)、[Sqrt Decomposition／分塊](#sqrt-decomp)、[2D Fenwick Tree](#fenwick2d) |
| [Data_Structures/Advanced/Binary_Indexed_Tree/02-Implementations.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Advanced/Binary_Indexed_Tree/02-Implementations.md) | [Fenwick Tree／Binary Indexed Tree](#fenwick)、[2D Fenwick Tree](#fenwick2d) |
| [Data_Structures/Advanced/De_Bruijn_Graph.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Advanced/De_Bruijn_Graph.md) | [De Bruijn Graph／Sequence](#de-bruijn) |
| [Data_Structures/Advanced/Dynamic_Sorted_Container_Selection.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Advanced/Dynamic_Sorted_Container_Selection.md) | [Ordered Map／Set／Multiset](#ordered-map) |
| [Data_Structures/Arrays_and_Strings/Array_Problem_Strategies.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/Array_Problem_Strategies.md) | [Array／Vector／String](#array) |
| [Data_Structures/Arrays_and_Strings/K-Sum_Problems/01-Two_Sum.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/K-Sum_Problems/01-Two_Sum.md) | [K-Sum／Rolling Hash Lookup](#ksum) |
| [Data_Structures/Arrays_and_Strings/K-Sum_Problems/02-Three_Sum.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/K-Sum_Problems/02-Three_Sum.md) | [K-Sum／Rolling Hash Lookup](#ksum) |
| [Data_Structures/Arrays_and_Strings/Matrix_Problem_Solving_Toolkit.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/Matrix_Problem_Solving_Toolkit.md) | [Coordinate Mapping／Matrix In-place Marking](#coordinate) |
| [Data_Structures/Arrays_and_Strings/Reverse_Processing_Patterns.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/Reverse_Processing_Patterns.md) | [Backward Fill／逆序批次修改](#backward-fill) |
| [Data_Structures/Arrays_and_Strings/Subsequence_Problem_Solving_Strategies.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/Subsequence_Problem_Solving_Strategies.md) | [1D Sequence DP／固定與動態範圍依賴](#sequence-dp)、[LCS／Edit Distance／雙序列 DP](#lcs-edit)、[LIS：Greedy Tails + Binary Search](#lis-tails) |
| [Data_Structures/Arrays_and_Strings/Vector_O1_Deletion_Swap_to_End.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Arrays_and_Strings/Vector_O1_Deletion_Swap_to_End.md) | [Swap-to-End／Randomized Set](#swap-delete) |
| [Data_Structures/Common_Patterns/Index_as_Reference.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Common_Patterns/Index_as_Reference.md) | [Entity Identity／Index as Reference](#identity) |
| [Data_Structures/Graphs/Adjacency_List_Representation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Adjacency_List_Representation.md) | [Edge List／Adjacency List／Matrix／Grid](#graph-representation) |
| [Data_Structures/Graphs/Constraint_Connectivity.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Constraint_Connectivity.md) | [Constraint Connectivity](#constraint-reach) |
| [Data_Structures/Graphs/Edge_List_Representation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Edge_List_Representation.md) | [Edge List／Adjacency List／Matrix／Grid](#graph-representation) |
| [Data_Structures/Graphs/Entity_Identity_Principle.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Entity_Identity_Principle.md) | [Entity Identity／Index as Reference](#identity) |
| [Data_Structures/Graphs/Graph_Problem_Solving_From_Leetcode.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Graph_Problem_Solving_From_Leetcode.md) | [Edge List／Adjacency List／Matrix／Grid](#graph-representation) |
| [Data_Structures/Graphs/Graph_Problem_Solving_Principles.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Graph_Problem_Solving_Principles.md) | [Edge List／Adjacency List／Matrix／Grid](#graph-representation) |
| [Data_Structures/Graphs/Graph_vs_Tree.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Graph_vs_Tree.md) | [無向圖環偵測與 Graph-as-Tree](#undirected-cycle) |
| [Data_Structures/Graphs/Implicit_Graph_Node_Construction.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Implicit_Graph_Node_Construction.md) | [Implicit Graph／Vertex Mapping](#implicit-graph) |
| [Data_Structures/Graphs/Implicit_Graphs.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Implicit_Graphs.md) | [Implicit Graph／Vertex Mapping](#implicit-graph) |
| [Data_Structures/Graphs/Lattice_Graph.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Lattice_Graph.md) | [Edge List／Adjacency List／Matrix／Grid](#graph-representation)、[A* Search](#a-star) |
| [Data_Structures/Graphs/Minimum_Spanning_Tree/01-Cut_Property_and_MST_Intro.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/Minimum_Spanning_Tree/01-Cut_Property_and_MST_Intro.md) | [Kruskal／Minimum Spanning Forest](#kruskal)、[Prim／切割前沿](#prim)、[Exchange Argument／Staying Ahead／Cut Property](#proof-exchange) |
| [Data_Structures/Graphs/README.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Graphs/README.md) | [Edge List／Adjacency List／Matrix／Grid](#graph-representation) |
| [Data_Structures/Hash_Tables/Frequency_Matching_Counting_Invariant.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Hash_Tables/Frequency_Matching_Counting_Invariant.md) | [Frequency Matching／Counting Invariant](#frequency-window) |
| [Data_Structures/Hash_Tables/README.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Hash_Tables/README.md) | [Prefix Sum + Hash Map](#prefix-hash)、[Hash Table／Hash Map／Hash Set](#hash) |
| [Data_Structures/Hash_Tables/Validation_Transformation_Duality.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Hash_Tables/Validation_Transformation_Duality.md) | [Validation–Transformation Map](#validation-map) |
| [Data_Structures/Heaps/00-Priority_Queue_Greedy_Template.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/00-Priority_Queue_Greedy_Template.md) | [Binary Heap／Priority Queue／Heapify](#heap) |
| [Data_Structures/Heaps/01-Heap_Decision_Making.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/01-Heap_Decision_Making.md) | [Binary Heap／Priority Queue／Heapify](#heap)、[A* Search](#a-star) |
| [Data_Structures/Heaps/02-Top_K_Problems.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/02-Top_K_Problems.md) | [Bounded Heap／Top-K／Push–Pop](#top-k) |
| [Data_Structures/Heaps/03-Push_Pop_Fixed_Size_Heap.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/03-Push_Pop_Fixed_Size_Heap.md) | [Greedy Sweep + Top-K／Push–Pop Replacement](#topk-greedy)、[Bounded Heap／Top-K／Push–Pop](#top-k) |
| [Data_Structures/Heaps/04-Two_Heaps_Balancing.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/04-Two_Heaps_Balancing.md) | [Two-Heaps Balancing／Streaming Median](#twoheap-median) |
| [Data_Structures/Heaps/05-Make_Heap_Complexity_Analysis.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/05-Make_Heap_Complexity_Analysis.md) | [Binary Heap／Priority Queue／Heapify](#heap) |
| [Data_Structures/Heaps/06-Amortized_Analysis.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Heaps/06-Amortized_Analysis.md) | [Greedy Sweep + Top-K／Push–Pop Replacement](#topk-greedy)、[Aggregate／Amortized Analysis](#proof-amortized) |
| [Data_Structures/Linked_Lists/Dummy_Node_for_Insertion.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Linked_Lists/Dummy_Node_for_Insertion.md) | [Insertion Sort](#insertion-sort)、[Dummy Node／Linked List Reversal](#dummy-reverse) |
| [Data_Structures/Linked_Lists/README.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Linked_Lists/README.md) | [Singly／Doubly Linked List](#linked-list)、[Dummy Node／Linked List Reversal](#dummy-reverse) |
| [Data_Structures/Stacks_and_Queues/Monotonic_Stacks/01-Monotonic_Stack_and_Queue.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Stacks_and_Queues/Monotonic_Stacks/01-Monotonic_Stack_and_Queue.md) | [Monotonic Stack／Next Greater–Smaller](#monostack)、[Monotonic Deque／Window Extremum](#monoqueue) |
| [Data_Structures/Stacks_and_Queues/Monotonic_Stacks/02-Search_Space_Conversion.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Stacks_and_Queues/Monotonic_Stacks/02-Search_Space_Conversion.md) | [Monotonic Stack／Next Greater–Smaller](#monostack) |
| [Data_Structures/Stacks_and_Queues/Monotonic_Stacks/03-Stack_Internal_Search.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Stacks_and_Queues/Monotonic_Stacks/03-Stack_Internal_Search.md) | [Stack Internal Search／三索引邊界](#stack-boundary) |
| [Data_Structures/Trees/BFS.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/BFS.md) | [BFS／Level Order／Level in Queue](#bfs) |
| [Data_Structures/Trees/Binary_Search_Trees/01-Core_Operations_and_Properties.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Search_Trees/01-Core_Operations_and_Properties.md) | [Binary Search Tree／Inorder／Duplicates](#bst) |
| [Data_Structures/Trees/Binary_Search_Trees/02-In-order_Traversal_Strategy.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Search_Trees/02-In-order_Traversal_Strategy.md) | [Binary Search Tree／Inorder／Duplicates](#bst) |
| [Data_Structures/Trees/Binary_Search_Trees/Augmented_BST_for_Order_Statistics.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Search_Trees/Augmented_BST_for_Order_Statistics.md) | [AVL Tree](#avl)、[Red–Black Tree](#red-black)、[Augmented BST／Order Statistic Tree](#ost) |
| [Data_Structures/Trees/Binary_Search_Trees/Duplicates_in_BST.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Search_Trees/Duplicates_in_BST.md) | [Binary Search Tree／Inorder／Duplicates](#bst) |
| [Data_Structures/Trees/Binary_Trees/Binary_Tree_Traversal.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Trees/Binary_Tree_Traversal.md) | [Binary／N-ary／Complete／Perfect Tree](#tree-structure) |
| [Data_Structures/Trees/Binary_Trees/Canonical_Forms_Transformation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Trees/Canonical_Forms_Transformation.md) | [Tree Canonical Form／Merkle Hashing](#canonical-tree) |
| [Data_Structures/Trees/Binary_Trees/Perfect_Binary_Tree.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Binary_Trees/Perfect_Binary_Tree.md) | [Binary／N-ary／Complete／Perfect Tree](#tree-structure) |
| [Data_Structures/Trees/DFS.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/DFS.md) | [DFS／Flood Fill／Connected Components](#dfs) |
| [Data_Structures/Trees/DFS_for_Level_Order_Traversal.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/DFS_for_Level_Order_Traversal.md) | [DFS + Depth Bucketing](#dfs-level) |
| [Data_Structures/Trees/DFS_vs_BFS.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/DFS_vs_BFS.md) | [BFS／Level Order／Level in Queue](#bfs) |
| [Data_Structures/Trees/Height_Balanced_BST.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Height_Balanced_BST.md) | [AVL Tree](#avl)、[Red–Black Tree](#red-black)、[Splay Tree](#splay)、[Treap](#treap) |
| [Data_Structures/Trees/Iterative_Traversal/01-Recursive_to_Iterative_Conversion.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Iterative_Traversal/01-Recursive_to_Iterative_Conversion.md) | [遞迴轉迭代與 Explicit Stack](#iterative-traversal)、[Two-Stack Postorder](#two-stack-postorder) |
| [Data_Structures/Trees/Iterative_Traversal/02-Visit_Nature_Quick_Reference.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Iterative_Traversal/02-Visit_Nature_Quick_Reference.md) | [遞迴轉迭代與 Explicit Stack](#iterative-traversal)、[Two-Stack Postorder](#two-stack-postorder) |
| [Data_Structures/Trees/Iterative_Traversal/03-Current_Pointer_Implementations.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Iterative_Traversal/03-Current_Pointer_Implementations.md) | [遞迴轉迭代與 Explicit Stack](#iterative-traversal)、[Two-Stack Postorder](#two-stack-postorder) |
| [Data_Structures/Trees/Iterative_Traversal/04-Postorder_lastVisited_Deep_Dive.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Iterative_Traversal/04-Postorder_lastVisited_Deep_Dive.md) | [遞迴轉迭代與 Explicit Stack](#iterative-traversal)、[Two-Stack Postorder](#two-stack-postorder) |
| [Data_Structures/Trees/Iterative_Traversal/05-Unified_Framework.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Iterative_Traversal/05-Unified_Framework.md) | [遞迴轉迭代與 Explicit Stack](#iterative-traversal)、[Two-Stack Postorder](#two-stack-postorder) |
| [Data_Structures/Trees/Morris_Traversal.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Morris_Traversal.md) | [Morris Traversal](#morris) |
| [Data_Structures/Trees/N-ary_Tree.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/N-ary_Tree.md) | [Binary／N-ary／Complete／Perfect Tree](#tree-structure) |
| [Data_Structures/Trees/Path_Based_Thinking_Aggregation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Path_Based_Thinking_Aggregation.md) | [Path-Based Aggregation／Ancestor Constraints](#path-aggregation) |
| [Data_Structures/Trees/Recursive_Design_Pattern_Pruning_and_Aggregation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Recursive_Design_Pattern_Pruning_and_Aggregation.md) | [Tree DP／Subtree Aggregation](#tree-dp)、[LCA／子樹見證聚合](#lca) |
| [Data_Structures/Trees/Tree_As_Equivalent_Graph.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trees/Tree_As_Equivalent_Graph.md) | [Binary／N-ary／Complete／Perfect Tree](#tree-structure) |
| [Data_Structures/Trie/01_Trie_Core_Concepts_and_Implementation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trie/01_Trie_Core_Concepts_and_Implementation.md) | [Trie／Prefix Tree／Bitwise Trie](#trie) |
| [Data_Structures/Trie/02_Trie_Design_Patterns_and_Usage.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Data_Structures/Trie/02_Trie_Design_Patterns_and_Usage.md) | [Trie／Prefix Tree／Bitwise Trie](#trie)、[Dynamic Trie／Backtracking + Trie](#dynamic-trie) |
| [Interview_Playbook/Code_Review.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Code_Review.md) | [Loop Invariant／契約與測試](#proof-invariant) |
| [Interview_Playbook/Hard_Problem_Learning_Strategy.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Problem_Learning_Strategy.md) | 面試流程與學習／review 方法；作框架背景，不當作新的算法。 |
| [Interview_Playbook/Hard_Techniques_Reference.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Hard_Techniques_Reference.md) | [Interval DP／Palindrome DP](#interval-dp)、[Tree DP／Subtree Aggregation](#tree-dp)、[Rerooting DP](#rerooting)、[Bitmask DP／Subset DP](#bitmask-dp)、[Digit DP](#digit-dp)、[Probability／Expectation DP](#probability-dp)、[Prefix Sum／2D–3D Prefix／Prefix XOR](#prefix)、[Difference Array／多維差分](#difference)、[Trie／Prefix Tree／Bitwise Trie](#trie)、[Segment Tree](#segment-tree)、[Lazy Propagation](#lazy-segment)、[Matrix Exponentiation](#matrix-power)、[Binomial／Factorial／Catalan Counting](#combinatorics)、[Bipartite Check／二染色](#bipartite)、[Hopcroft–Karp／Maximum Bipartite Matching](#hopcroft-karp)、[Tarjan SCC／Lowlink](#tarjan)、[Kosaraju SCC](#kosaraju)、[Lowlink Bridges／Articulation Points](#bridges)、[Divide-and-Conquer DP Optimization／Monge](#dc-optimization)、[Knuth Optimization](#knuth) |
| [Interview_Playbook/Leetcode_Stages_of_an_Interview.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Leetcode_Stages_of_an_Interview.md) | 面試流程與學習／review 方法；作框架背景，不當作新的算法。 |
| [Interview_Playbook/Pre_Solve_Interview_Checklist.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Pre_Solve_Interview_Checklist.md) | 面試流程與學習／review 方法；作框架背景，不當作新的算法。 |
| [Interview_Playbook/Problem_Solving_Process_and_Assumption_Checklist.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Problem_Solving_Process_and_Assumption_Checklist.md) | 面試流程與學習／review 方法；作框架背景，不當作新的算法。 |
| [Interview_Playbook/Problem_Solving_Strategies.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Interview_Playbook/Problem_Solving_Strategies.md) | 面試流程與學習／review 方法；作框架背景，不當作新的算法。 |
| [Meta_Frameworks/Orthogonality-Problem-Solving.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Orthogonality-Problem-Solving.md) | [Recursion 遞迴](#recursion) |
| [Meta_Frameworks/Problem_Classification_Framework/00-Problem_Specification_Confirmation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/00-Problem_Specification_Confirmation.md) | 統一框架的來源；對照本文前五節。 |
| [Meta_Frameworks/Problem_Classification_Framework/01-Interview_Timing_Framework.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/01-Interview_Timing_Framework.md) | [Simulation／Cellular Automaton](#simulation)、[Floyd-Warshall](#floyd-warshall)、[LCS／Edit Distance／雙序列 DP](#lcs-edit)、[Sieve of Eratosthenes](#sieve)、[Fast Power／Binary Exponentiation](#fast-power)、[Binomial／Factorial／Catalan Counting](#combinatorics)、[Nim／有限取石遊戲的勝負狀態](#nim)、[Z-function／Z-algorithm](#z-function)、[Rolling Hash／Rabin–Karp](#rolling-hash)、[Manacher](#manacher)、[Aho–Corasick／多模式自動機](#aho) |
| [Meta_Frameworks/Problem_Classification_Framework/02-Quick_Decision_Map.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/02-Quick_Decision_Map.md) | [Binary Search／Lower Bound／Upper Bound](#binary-search)、[Parenthesis Matching／Invalid Boundary Stack](#parenthesis-stack) |
| [Meta_Frameworks/Problem_Classification_Framework/03-State_Transition_Traversal.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/03-State_Transition_Traversal.md) | [Dynamic Programming／Memoization／Tabulation](#dp) |
| [Meta_Frameworks/Problem_Classification_Framework/04-Advanced_Problem_Solving_Cheatsheet.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Classification_Framework/04-Advanced_Problem_Solving_Cheatsheet.md) | [0-1 BFS](#zero-one)、[Pruning／Branch and Bound](#branch-bound)、[Lazy Propagation](#lazy-segment)、[Sqrt Decomposition／分塊](#sqrt-decomp)、[Mo's Algorithm／離線窗口重排](#mo)、[Maximum Flow／Minimum Cut／Residual Network](#flow)、[Edmonds–Karp](#edmonds-karp)、[Dinic／Blocking Flow](#dinic)、[Hungarian／加權指派](#hungarian)、[Rotating Calipers／旋轉卡尺](#calipers) |
| [Meta_Frameworks/Problem_Transformation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Meta_Frameworks/Problem_Transformation.md) | [LCA／子樹見證聚合](#lca)、[Preprocessing／Offline／Coordinate Compression](#preprocess)、[Maximum Flow／Minimum Cut／Residual Network](#flow)、[Exchange Argument／Staying Ahead／Cut Property](#proof-exchange) |
| [Proof_Techniques/Exchange_Argument.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Proof_Techniques/Exchange_Argument.md) | [Fractional Knapsack](#fractional-knapsack)、[Exchange Argument／Staying Ahead／Cut Property](#proof-exchange) |
| [Proof_Techniques/Loop_Invariant.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Proof_Techniques/Loop_Invariant.md) | [Loop Invariant／契約與測試](#proof-invariant) |
| [Proof_Techniques/Structural_Induction.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Proof_Techniques/Structural_Induction.md) | [Structural Induction／遞迴正確性](#proof-induction) |
| [README.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/README.md) | 組織與範圍依據；不另當作算法。 |
| [Test_Case_Construction/Graph_Test_Case_Strategies.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Test_Case_Construction/Graph_Test_Case_Strategies.md) | [Loop Invariant／契約與測試](#proof-invariant) |
| [Test_Case_Construction/README.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Test_Case_Construction/README.md) | [Loop Invariant／契約與測試](#proof-invariant) |
| [Test_Case_Construction/Test_Case_Generation_Advice_ChatGPT.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Test_Case_Construction/Test_Case_Generation_Advice_ChatGPT.md) | [Loop Invariant／契約與測試](#proof-invariant) |
| [Test_Case_Construction/Test_Case_Generation_Advice_Gemini.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Test_Case_Construction/Test_Case_Generation_Advice_Gemini.md) | [Loop Invariant／契約與測試](#proof-invariant) |
| [Test_Case_Construction/Test_Case_Generation_Advice_Sonnet.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Test_Case_Construction/Test_Case_Generation_Advice_Sonnet.md) | [Loop Invariant／契約與測試](#proof-invariant) |
| [Test_Case_Construction/Tree_Test_Case_Notation.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Test_Case_Construction/Tree_Test_Case_Notation.md) | [Loop Invariant／契約與測試](#proof-invariant) |
| [Test_Case_Construction/Tree_Test_Case_Types.md](https://github.com/romanticamaj/leetcode-note/blob/96da0e3865c116340a3c4843ef4eed38399f63b1/Test_Case_Construction/Tree_Test_Case_Types.md) | [Loop Invariant／契約與測試](#proof-invariant) |

## 後續維護

新增技巧時沿用六欄，先比對是否只是既有條目的別名、不同表示或排程變體。若正確性條件、狀態語義或複雜度保證不同，補獨立條目。更新來源快照與對照表後，同步更新 HTML；避免把本次盤點標記當成永久全覆蓋。
