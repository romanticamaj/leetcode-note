# 787. Cheapest Flights Within K Stops：限制邊數的最短路徑與歷史

**記憶線索：抵達同一城市，便宜但用邊多、昂貴但用邊少，可能都要保留；先定義狀態，再決定搜尋順序。**

查證日期：2026-11-03；根據本次查閱的官方題面、原始論文與教材整理。

## 1. 題目出處與可確認的界線

[LeetCode 787 官方題面](https://leetcode.com/problems/cheapest-flights-within-k-stops/) 標註 **Weekly Contest 72**，可確認競賽歸屬；未找到出題者說明直接改編自哪一本書或論文，不能把模型相同當成直接傳承。

去掉航班情境後，這是 **hop-constrained / hop-bounded shortest path**：在帶權圖中，求最多使用 `H` 條邊的最小費用路徑。本題 `H = k+1`，因為 `k` 個中繼站代表最多 `k+1` 段航班。

## 2. 歷史脈絡：1950 年代已有邊數迭代的觀點

| 年份 | 文獻 | 可支持的結論 |
|---|---|---|
| 1956 | L. R. Ford，*Network Flow Theory*，RAND P-923 | Bellman-Ford 所屬的早期網路最佳化脈絡；出版紀錄不能單獨證明 LC 787 的直接來源 |
| 1958 | Richard Bellman，*On a Routing Problem*，Quarterly of Applied Mathematics 16(1):87–90 | 以城市間旅行時間推導 DP；第 89 頁明確用最多一次停留解釋一次迭代 |
| 2005 | Stefan Irnich、Guy Desaulniers，*Shortest Path Problems with Resource Constraints*，收於 *Column Generation*，33–65 頁 | 更一般的資源受限最短路徑框架，可用於理解路徑 label 與資源限制 |
| 2023 | Tomasz Kociumaka、Adam Polak，*Bellman-Ford Is Optimal for Shortest Hop-Bounded Paths*，ESA 2023 | 直接研究最多 H 條邊的最短路徑，以及有條件的時間下界 |

Ford 的年份與報告編號見 [RAND 出版紀錄](https://www.rand.org/pubs/papers/P923.html)。Bellman 原文第 89 頁、Section 5，將一次迭代的意義寫為：

> “the minimum time for a path with at most one stop”

原始策略直接抵達目的地，之後允許更多中途停留。這與本題的狀態模型直接相關，但原文要解的是整體最短路徑，不是聲稱當時已出現完全相同的 LeetCode 題面。[Bellman 原文，第 89 頁](https://www.cs.yale.edu/homes/lans/readings/routing/bellman-routing-1958.pdf#page=3)

## 3. 教科書在哪裡？

- **Jeff Erickson，Algorithms**：Chapter 8、§8.7，*Dynamic Programming Formulation*；書上第 294–295 頁，章節 PDF 第 22–23 頁。直接把最大邊數加入狀態。[免費教材](https://jeffe.cs.illinois.edu/teaching/algorithms/book/08-sssp.pdf#page=22)
- **Jon Kleinberg、Éva Tardos，Algorithm Design**：§6.8 *Shortest Paths*，位於 Dynamic Programming 章。可對照 Kevin Wayne 的 [配套投影片](https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pearson/06BellmanFord-2x2.pdf)。

Erickson 的狀態是 `D_i(v)`：從 s 到 v，**至多使用 i 條邊**的最小費用。

```text
D_i(v) = min(D_(i-1)(v), min over edges (u,v) of D_(i-1)(u) + w(u,v))
answer = D_(k+1)(dst)
```

這是 Bellman-Ford 的 DP 根源。**負權重不是它與本題相關的唯一理由；逐層限制邊數，才是直接對應。**

既有技巧筆記：[Bellman-Ford 的動態規劃基礎](../Algorithms/Dynamic_Programming/Advanced_Techniques/Bellman-Ford/01-DP_Foundations_of_Bellman-Ford.md)。

## 4. 三種解法：同一個限制，不同的搜尋排程

以下是解題關係的推導，不是歷史作者發明過程的還原。三種方法分開練習，**尚未獨立完成**的版本見 [Problem Review](../Checklists/Lists/09_Problem_Review.md)。

| 重練版本 | 核心 invariant／驗收重點 |
|---|---|
| Bellman-Ford／邊數 DP | 第 i 輪得到至多 i 條邊的最小費用；每輪只讀上一層快照，避免同輪連走多條邊 |
| BFS with condition k／按邊數分層的 relaxation | queue 按已用邊數分層，每層只擴展一條邊；同層同城市保留最低費用，再擴展下一層，最多 H 層 |
| Better Dijkstra／cost-ordered dominance pruning | 非負權重下按費用出隊；先前接受的同城市候選費用不更高，若其邊數也不更多，即可淘汰目前候選 |

### Bellman-Ford：快照是限制的一部分

若在同一陣列原地更新，`s→a` 的新結果可能立刻被 `a→b` 使用，導致一輪走了兩條邊。原地 Bellman-Ford 可用來求不受邊數限制的最短路徑，但不能把第 i 輪解讀成「恰好只考慮至多 i 條邊」。

### BFS：層數保證邊數，不保證費用

這裡的 BFS 是按邊數排程的 weighted relaxation，並非普通無權圖 BFS：不能首次 visited 就永久封鎖城市，也不能第一次抵達 dst 就回傳。先把同層同城市的費用合併，再讓下一層讀取固定的上一層結果，可避免列舉大量重複路徑；與邊數 DP 的轉移相同，只掃描當層可達城市的出邊。

### Better Dijkstra：出隊順序替費用比較提供保證

在同一城市，若 A 的 `cost <= B.cost` 且 `edgesUsed <= B.edgesUsed`，B 就沒有優勢。原始反例的兩條路徑則互不支配：

| 到 node 4 的路徑 | 費用 | 已用邊數 | H=3 時能否再走到 node 2？ |
|---|---:|---:|---|
| 0→3→1→4 | 5 | 3 | 否 |
| 0→1→4 | 6 | 2 | 可以，最後費用 7 |

二維 `dist[city][edgesUsed]` 是直接保存擴展狀態的方式，值代表**恰好**使用指定邊數的最小費用；與前述「至多 i 條邊」的 DP 定義不同。

精簡版本在 pop 時維護 `minEdges[city]`：因為較早 pop 的費用不更高，所以只需再比較邊數。若 `edgesUsed >= minEdges[city]` 即可剪枝，否則更新並擴展。**不能把相同判斷直接搬到 push 時**，入隊順序沒有費用排序保證。先檢查邊數合法，再做 dominance 檢查；合法 dst 第一次被接受時可回傳，H 條邊的狀態不能再擴展。

這是對本次精簡程式的分類，未確認該份實作的最初作者。更一般的 labeling 研究可參考 [Irnich–Desaulniers，2005](https://link.springer.com/chapter/10.1007/0-387-25486-2_2) 與 [Boland、Dethridge、Dumitrescu，2006](https://www.sciencedirect.com/science/article/pii/S0167637705000040)；後者處理更一般的 elementary resource-constrained 模型，不能直接等同本題。

## 5. 為什麼使用 heap 不一定更快？

二維 distance 修正的是錯誤剪枝，也增加需要處理的狀態；heap 另外帶來排序成本。若搜尋到 queue 清空，又未有效剪枝，實際時間未必改善，不能只根據一次平台耗時判定優劣。

令 V 為城市數、E 為航班數、H=k+1；以下計入初始化，空間計入圖與 queue／heap，不含輸入本身。

| 具體實作 | 時間上界 | 額外空間上界 |
|---|---|---|
| 每輪複製 V 格快照的 Bellman-Ford | O(V + H(V+E)) | O(V) |
| 每層同城市先合併、再掃出邊的 BFS | O(V+E+H(V+E)) | O(V+E) |
| 二維 distance＋lazy heap 的 Dijkstra | O(V(H+1)+HE log(HE+2)) | O(V(H+1)+HE) |
| pop 時 minEdges 剪枝的精簡 Dijkstra，合法邊數才入隊 | O(V+E+HE log(HE+2)) | O(V+E+HE) |

精簡 Dijkstra 每城市接受的邊數嚴格下降，最多 H+1 種；每個可擴展狀態掃一次出邊，heap 仍可能保存 O(HE) 個候選，不能只因 `minEdges` 是一維便宣稱總空間 O(V)。上述 BFS 界線依賴層內合併；只用 queue 枚舉路徑不具備此保證。

2023 年的 [Kociumaka–Polak 論文](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2023.72) 研究 O(HE) 的邊數受限最短路徑界線：在 APSP Hypothesis 下給出部分參數範圍的下界；在更強的 Min-Plus Convolution Hypothesis 下涵蓋完整參數範圍，容許次多項式因子差距。這是一般問題的**有條件、最壞情況**結論，不代表每組測資 Bellman-Ford 都最快。

## ✅ 重練時應能回答

- [ ] 為什麼 city 不足以定義狀態？為什麼有些較貴路徑仍不能丟？
- [ ] `k stops`、`H edges`、陣列 H+1 格的關係？
- [ ] 「恰好 i 條邊」與「至多 i 條邊」的初始化、轉移與取答案差異？
- [ ] Bellman-Ford 的快照、BFS 的層界、Dijkstra 的費用出隊順序，各保證什麼？
- [ ] 為什麼 BFS 不能首次抵達 dst 就回傳，而此題的 Dijkstra 可以？
- [ ] 哪些歷史來源已確認，哪些只是數學關係或尚未證實的直接傳承？

建議閱讀順序：Erickson 第 294–295 頁 → Bellman 第 89 頁 → 實作三種排程 → 最後讀 2023 年論文摘要與下界的適用範圍。
