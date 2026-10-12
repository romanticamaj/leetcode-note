# 310. Minimum Height Trees：樹中心的出處與歷史

**記憶線索：題目要找的是最遠距離最小的根；從所有葉同時往內剝，或找直徑的中點，都會得到樹的 center。**

查證日期：2026-10-13。

## 題目情境與查證結論

[LC 310](https://leetcode.com/problems/minimum-height-trees/description/) 給 `n` 個節點（編號 `0..n-1`）與 `n-1` 條無向邊；輸入保證連通且無環，所以任兩點間恰有一條路徑。可以任選一個既有節點當根，題目要求列出**所有**使 rooted tree 高度最小的根。距離是路徑上的邊數，樹高是根到最遠節點的距離，因此：

```text
h(v) = max_{u ∈ V} dist(v, u)
答案 = argmin_{v ∈ V} h(v)
```

例如路徑 `0—1—2—3`：選端點作根時高度為 3；選 `1` 或 `2` 時高度為 2，所以答案是 `{1,2}`。單點樹 `n=1` 的答案是 `{0}`，兩點樹 `n=2` 的兩個節點都合格。

這是圖論中的 **tree center（樹中心）**，也可視為「設施必須設在節點上，讓最遠需求點的距離最小」的離散 1-center 問題。[來源 1、4] **可確認這個數學問題早於 LeetCode；目前沒有證據證明 LeetCode 直接取材自下列某一篇文獻，也未確認 LC 310 的首次上線日期。**

## 可確認的歷史

### 1869：Jordan 對樹的研究

Camille Jordan 的〈Sur les assemblages de lignes〉刊於 *Journal für die reine und angewandte Mathematik* 第 70 卷，185–190 頁，1869 年。[來源 2] Frank Harary 後來在《Graph Theory》第 4 章，把樹中心「一點或相鄰兩點」的結果歸給 Jordan，並提及 Sylvester 獨立發現同一結果；他也把樹重心的相應定理追溯到 Jordan。[來源 3]

這裡能確認的是 **Jordan 的原始文獻存在、後來的圖論著作將這兩個定理追溯到他**。不能進一步把今日的 queue 實作或 LeetCode 的題目敘述歸給 Jordan，也不把現代英文術語直接當作原文用語。

### 1962：Kahn 的拓撲排序是另一條技術脈絡

A. B. Kahn 的〈Topological sorting of large networks〉發表於 *Communications of the ACM* 5(11)，558–562 頁，1962 年。[來源 5] 它研究有向網路的拓撲序：反覆處理入度為零的節點。

LC 310 的常見解法也使用 queue、degree 與逐輪移除，但處理的是**無向樹的 degree = 1 葉節點**。稱它「Kahn-like」是在比較實作形式；**沒有來源支持說 Kahn 提出了樹中心剝葉法**，也沒有在無向樹上產生拓撲序。

### 1964：網路設施選址中的 center

S. L. Hakimi 在〈Optimum Locations of Switching Centers and the Absolute Centers and Medians of a Graph〉研究加權網路上的設施選址，並區分 center 與 median 目標。出版社摘要舉出通訊網路的 switching center、公路網路的警察局位置；論文刊於 *Operations Research* 12(3)，450–459 頁，1964 年。[來源 4]

它展示「讓最遠位置盡可能近」有實際選址背景；**Hakimi 研究的加權／absolute center 允許不同的設施位置與條件，並非 LC 310 的原題或剝葉演算法來源**。LC 310 限定無權樹，根只能是既有節點。

### 1969：Harary 已明確寫出剝葉證明

Frank Harary 的《Graph Theory》第 4 章〈Centers and Centroids〉分別定義兩個概念。其 **Theorem 4.2** 說樹中心是一點或相鄰兩點，證明直接採用「同時刪除全部葉，反覆做到只剩 `K₁` 或 `K₂`」；**Theorem 4.3** 才是樹重心的相應結果。[來源 3]

因此，LC 310 所用的剝葉觀察至少在 1969 年的教科書已有明確文字記載。這是**已查到的早期文字證據**，不是剝葉法的發明年份。

### 1984：分散式網路繼續研究樹中心

Ephraim Korach、Doron Rotem、Nicola Santoro 的〈Distributed Algorithms for Finding Centers and Medians in Networks〉刊於 *ACM Transactions on Programming Languages and Systems* 6(3)，380–401 頁，1984 年。論文研究如何在分散式網路中找 center／median，並給出樹網路的演算法。[來源 6]

這證明中心問題不只出現在面試題；在網路中，每個節點只掌握局部資訊時，也需要找出中心。但分散式訊息演算法的計算模型與 LC 310 的單機 adjacency list 不同，不能把兩者視為同一個實作。

### 2020：LeetCode 解答中的命名混用

[LeetCode 官方文章索引](https://leetcode.com/articles/?page=159&tag=linked-list)列出 310 的 editorial 日期為 **2020-10-17**；這是**解答文章日期，不能當成題目首次上線日期**。[來源 7]

依使用者提供的 [官方解答](https://leetcode.com/problems/minimum-height-trees/editorial/)〈Approach 1: Topological Sorting〉摘錄，它反覆把剝葉後留下的節點稱為 *centroids*，同時以「最小高度／到最遠節點的距離」定義目標。按標準圖論定義，這些節點是 **centers**。解答的 queue 剝葉方法可以得到正確答案；錯的是術語，且其中「若有三個就必形成三角形」不是有效的證明：三個候選點不必兩兩相連。

本次查到的官方 editorial 網頁未提供可直接讀取的完整正文，因此**用語與三角形段落的核對依據是使用者貼出的摘錄**；文章索引只支持日期與文章存在。也無法查明命名混用最初出現在哪一版解答。

## 🧠 數學觀點：三種「中間」回答不同問題

| 概念 | 最小化的量 | 對 LC 310 的關係 |
|---|---|---|
| **Center** | `max_u dist(v,u)`，最遠距離 | **題目所求**；有一或兩個相鄰節點 |
| **Centroid** | 移除 `v` 後最大連通分量的節點數 | 衡量分支是否均衡；可與 center 不同 |
| **Median** | `sum_u dist(v,u)`，總距離 | 衡量所有距離的總和；在無權樹上與 centroid 相應，目標仍不同 |

令 `M(v)` 為移除 `v` 後各連通分量的最大節點數；`centroid` 最小化 `M(v)`，等價的判準是每個分量大小都不超過 `n/2`。令 `S(v) = sum_u dist(v,u)`；`median` 最小化 `S(v)`。在**無權樹且只選既有節點**的條件下，median 與 centroid 恰好是同一組節點：沿邊從 `v` 移到 `w`，若 `w` 那側有 `s` 個節點，則其中 `s` 個距離各減 1，其餘 `n-s` 個各加 1，所以 `S(w)-S(v)=n-2s`。只有每側都 `s ≤ n/2` 時，往任何相鄰節點走都不能降低總距離；樹上沿著能降低總距離的邊前進，最後便達到全域最小值。這個等價**不會**讓兩者等於 center。[來源 3、8]

Harary 分別討論 center 與 centroid；[NetworkX 文件](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.tree.distance_measures.centroid.html)也明確區分 tree centroid 與 graph center，並指出無權樹上 centroid 對應總距離最小的 barycenter。[來源 3、8]

一個九點反例：取路徑 `0—1—2—3—4`，再把 `5、6、7、8` 四個葉接到 `0`。

```text
5  6  7  8
 \ |  | /
    0—1—2—3—4
```

以 **1 或 2** 為根的最大距離都是 3，最小，因此 centers 是 `{1,2}`。移除 **0** 後，最大連通分量 `{1,2,3,4}` 有 4 點，不超過 `9/2`；移除 1 則會留下 5 點分量，所以 centroid（也就是此例的 median）是 `{0}`。這也說明「兩種答案都至多兩個」不足以認定它們是同一概念。

## 🧩 解法一：逐層剝葉，從外向內找 center

在目前的樹中，**葉**是無向 degree 為 1 的節點。每輪同時刪除所有葉，剩下的圖仍是樹；原本的內部節點可能成為下一輪的葉。沿用 `0—1—2—3—4` 這條路徑，第一輪刪 `{0,4}`，第二輪刪 `{1,3}`，最後得到 center `{2}`。若路徑有偶數個節點，最後會剩相鄰的兩點。

**為什麼能刪？** 當樹超過兩點，葉 `x` 的唯一鄰居 `y` 到每個其他節點都比 `x` 近 1，因此 `x` 不可能是 center。對任何保留下來的節點 `v`，原樹的最遠節點可選在葉上；每個被刪的葉都只比其保留的鄰居遠 1，故刪後高度最多降低 1。另一方面，刪後離 `v` 最遠的節點可選為剩餘樹的葉；這個節點原先不是葉，至少連著一個剛刪除的葉，所以原高度至少比刪後大 1。因此每個保留節點的高度**恰好同減 1**，最小者保持不變。重複到只剩 `K₁`（一點）或 `K₂`（相鄰兩點），留下的全是原樹 center。這就是 Harary 書中的剝葉論證。[來源 3]

**每輪的狀態。** `remaining` 是目前仍在樹上的節點數；`degree[v]` 是 `v` 在**剩餘樹**中的度數；目前這一層的葉，是所有仍在樹上且 `degree = 1` 的節點。先用 adjacency list 建樹並計算初始 degree。當 `n=1` 時唯一節點的 degree 為 0，直接得到 `{0}`；當 `n=2` 時兩點都是葉，也都已是答案。

**迴圈不變量。** 每次進入剝葉迴圈（`remaining > 2`）時，剩餘樹恰是從原樹同時剝除前面各輪葉後的結果；待處理集合恰好包含這棵樹的全部葉；`remaining` 等於其節點數。若已剝 `r` 輪，任何剩餘節點 `v` 在原樹中的高度，都等於它在剩餘樹中的高度加 `r`。因此我們始終在同一組候選中心中繼續尋找。

**一步怎麼推進。** 只在 `remaining > 2` 時剝葉。先固定本輪葉的個數 `size`，把 `remaining` 減去 `size`；處理這 `size` 個葉時，將各鄰居的剩餘 degree 減 1，降到 1 者加入**下一輪**。以 queue 表示時，先記錄 `queue.size()` 再取出這麼多個葉；即使新葉在本輪被推入 queue，也不能立即取出。以 vector 表示時，用 `leaves` 保存本輪、`new_leaves` 收集下一輪，整輪結束後再交換。兩種容器表達的是同一個層次邊界；本輪葉之間無須特定順序。

**何時停止。** `remaining ≤ 2` 時不再剝；剩下一點就回傳該點，剩兩點就回傳相鄰的兩點。若某輪的最後三點形成路徑，中間點可能先因一側葉被移除而降到 degree 1、加入下一輪，隨後因另一側葉被移除而降到 0；它仍是唯一存活節點，直接回傳即可。若繼續移除，反而會丟失合法 center。每輪至少移除兩個葉，程序會終止。每個節點最多成為本輪葉一次，每條邊在更新度數時只被檢視常數次，因此 **O(n) 時間、O(n) 空間**；樹有 `n-1` 條邊。

這個逐輪工作集合與 [Kahn 的 DAG 拓撲排序](../Algorithms/Topological_Sort/02-Kahn_Algorithm_BFS.md)相似：一輪的移除會產生下一輪可處理的節點。但 Kahn 維護的是**有向入度 0**，此處維護的是**無向 degree 1**；LC 310 沒有產生拓撲序。

## 🧩 解法二：找直徑，再取路徑中點

樹的**直徑**是所有節點對中最長路徑的長度。取任一條直徑，設端點為 `a,b`、長度為 `D`。若一個節點 `v` 位於這條路徑外，令 `x` 為它接上路徑的節點、`t = dist(v,x)`；令 `x` 離 `a` 有 `p` 條邊。事實上：

```text
h(v) = max(dist(v,a), dist(v,b)) = t + max(p, D-p)
```

**為什麼只看 `a,b` 就夠？** 對任意節點 `u`，令它接上直徑路徑的位置為 `y`，距 `a` 為 `q`，離路徑深度為 `r`。因為 `a—b` 已是最長路徑，`u` 到 `a`、`b` 都不會超過 `D`，所以 `r ≤ min(q,D-q)`。若 `p ≤ q`，沿直徑經過 `x,y` 的走法給出 `dist(v,u) ≤ t+(q-p)+r ≤ t+D-p = dist(v,b)`；若 `p ≥ q`，同理 `dist(v,u) ≤ t+(p-q)+r ≤ t+p = dist(v,a)`。因此任何 `u` 都不會比 `a,b` 更遠，而 `a,b` 本身又確實在樹上，等式成立。

於是離直徑路徑越遠（`t>0`），高度只會增加；在路徑上，`max(p,D-p)` 於中點最小。**`D` 為偶數時有一個 center；`D` 為奇數時有兩個相鄰 center。** 這也獨立證明答案至多兩點。直徑中點求 center 的做法亦見 Leiserson 與 Maggs 的圖演算法章節。[來源 9]

實作只需兩次 BFS（樹無權，DFS 同樣可計距離）：從任意節點 `s` 找最遠點 `a`；從 `a` 找最遠點 `b`，並記下每點的 `parent`；再沿 `parent` 從 `b` 回溯到 `a`，取中間一或兩點。第一遍 BFS 找到的 `a` 必是**某條**直徑的端點：以上述任一直徑 `A—B` 為參照，任意起點 `s` 的最遠距離可由 `A` 或 `B` 達到。若另一個最遠點 `a` 與它們並列，前段不等式必取等號，因而 `a` 到直徑另一端的距離也等於 `D`；故 `a` 也是直徑端點。第二遍 BFS 才會取得真正的直徑，而非只是一條從 `s` 出發的長路徑。

先處理 `n=1`，其答案就是 `{0}`。否則從任意節點（例如 0）做第一次 BFS，選最遠點 `a`；從 `a` 做第二次 BFS，選最遠點 `b`，並記錄每點的前一節點。沿這些記錄從 `b` 回到 `a`，取得直徑路徑，再選路徑中間一點或兩點。

兩次 BFS 與回溯各走 `O(n)`，adjacency list、BFS queue、`parent` 及路徑共用 **O(n) 空間**。`n=2` 時直徑路徑恰有兩點，會回傳兩者。這兩種解法輸出相同是因為它們都求 center；**數學等價不代表一種方法在歷史上衍生自另一種**。

## ⚠️ 相關但不同，以及尚未查明的事

- **樹中心與樹重心**：兩者各自可能有一或兩個相鄰答案；要看最佳化目標，不能只看答案數量。
- **Kahn 演算法**：LC 310 共享「反覆處理當前低 degree 節點」的程式形狀，沒有 DAG 的拓撲排序語義。
- **LeetCode 直接取材來源**：尚無證據確認它改寫自 Jordan、Harary、Hakimi 或其他特定文獻。
- **最早發明者與題目首次上線時間**：本次未查明；1869、1969、2020 分別是早期論文、已查到的剝葉文字、官方解答文章日期，不能互換。

## 來源與延伸閱讀

1. **LeetCode，〈310. Minimum Height Trees〉。** [題面](https://leetcode.com/problems/minimum-height-trees/description/)：支持輸入條件、根只能選節點、最小樹高的目標。
2. **Camille Jordan，〈Sur les assemblages de lignes〉，1869，70：185–190。** [原文影像 PDF](https://sites.math.washington.edu/~mathcircle/circle/archive/2014-15/advanced/mc-14a-w5.pdf)、[EuDML 書目](https://eudml.org/doc/148084)：支持原始論文的存在與書目；其與 center／centroid 定理的關係另由 Harary 說明。
3. **Frank Harary，《Graph Theory》，1969，第 4 章〈Centers and Centroids〉，Theorem 4.2–4.3。** [原書數位版](https://djvu.online/file/lPZA2KxVv3wQd)：支持 center／centroid 分別定義、Jordan／Sylvester 的歸屬、剝葉證明。
4. **S. L. Hakimi，〈Optimum Locations of Switching Centers and the Absolute Centers and Medians of a Graph〉，*Operations Research* 12(3)：450–459，1964。** [出版社摘要與書目](https://pubsonline.informs.org/doi/10.1287/opre.12.3.450)：支持設施選址背景及其加權／absolute 問題設定。
5. **A. B. Kahn，〈Topological sorting of large networks〉，*Communications of the ACM* 5(11)：558–562，1962。** [ACM 論文紀錄](https://dl.acm.org/doi/10.1145/368996.369025)：支持原始 Kahn 論文的主題與年份。
6. **E. Korach、D. Rotem、N. Santoro，〈Distributed Algorithms for Finding Centers and Medians in Networks〉，*ACM TOPLAS* 6(3)：380–401，1984。** [IBM Research 作者／出版紀錄](https://research.ibm.com/publications/distributed-algorithms-for-finding-centers-and-medians-in-networks)、[作者機構保存的技術報告](https://cs.uwaterloo.ca/research/tr/1980/CS-80-44.pdf)：支持分散式樹中心研究與出版資訊。
7. **LeetCode，〈310. Minimum Height Trees〉editorial。** [解答](https://leetcode.com/problems/minimum-height-trees/editorial/)、[官方文章索引](https://leetcode.com/articles/?page=159&tag=linked-list)：後者支持 2020-10-17 的文章日期；對用語與論證的分析依使用者提供的正文摘錄。
8. **NetworkX，tree centroid／graph center 文件。** [centroid](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.tree.distance_measures.centroid.html)、[center](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.distance_measures.center.html)：支持今日實務上的明確術語區分。
9. **C. E. Leiserson、B. M. Maggs，〈Communication-Efficient Parallel Algorithms for Distributed Random-Access Machines〉，第 7 節〈Graph Algorithms〉。** [CMU 保存的原文](https://www.cs.cmu.edu/afs/cs.cmu.edu/project/phrensy/pub/papers/LeisersonM88/node17.html)：分別列出 diameter／center 與 centroid 的演算法；支持「直徑中點也是中心」的另一種求法。
