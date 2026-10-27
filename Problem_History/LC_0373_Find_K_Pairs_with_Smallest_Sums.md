# 373. Find K Pairs with Smallest Sums：K-way Merge 與外部排序的歷史

**記憶線索：不必看見所有候選；每條有序來源只交出目前最前面的一個。取出誰，就向誰補下一個。**

查證日期：2026-10-28。

## 題目與查證結論

[LeetCode 373](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/) 的兩個陣列都已排序。固定 `nums1[i]`，依序搭配 `nums2[0], nums2[1], …`，就得到一條總和非遞減的**隱式序列**。因此題目可以轉為多條有序序列的前綴合併。

這是 **k-way merge / multiway merge（多路合併）** 的應用，而非必須列舉所有 pair 的 Top-k 問題。以下用 `r` 表示來源數、`N` 表示總項數、`q` 表示實際取出的項數，避免把「來源數 k」與題目要求的「答案數 k」混用。

可確認的歷史背景是**磁帶上的外部排序**；現代教材使用 heap 保存來源前端，但多路合併不等於 heap，也不能把 heap 的發表年份當成多路合併的起源。本次未確認多路合併的最初發明者，也未找到 LeetCode 373 直接承襲某篇文獻的證據。

## 1. 從 brute force 到 heap frontier

以下是解題推導，不是對歷史作者發明過程的還原。

### 先辨識哪些資訊已經有序

暴力法把所有配對列出、排序，忽略了每列原本就有序。固定大小 max-heap 雖可少存資料，但若仍枚舉所有配對，尚未省掉生成候選的成本。

例如兩個陣列 `[1,7,11]`、`[2,4,6]` 形成三列總和：

```text
來源 0： 3 →  5 →  7
來源 1： 9 → 11 → 13
來源 2：13 → 15 → 17
```

第一輪只需比較 `3,9,13`。取出 `3`，只補同來源的 `5`，其餘前端保留。來源可以是 linked list、檔案、陣列的一列，或由公式產生的序列；不必先實體化所有元素。

### Invariant：每個剩餘元素都被來源前端代表

每輪選取前，候選集合恰好包含每個未耗盡來源的第一個未輸出元素。

1. **初始化**：放入每個非空來源的第一項，invariant 成立。
2. **安全選取**：任意未輸出項目 `x` 都屬於某來源，其前端 `h` 滿足 `h <= x`。候選中最小的 `g` 又滿足 `g <= h`，因此 `g <= x`，是全域剩餘最小值。
3. **維持**：取出來源 s 的前端，只需把 s 的下一項放進候選；其他來源的前端沒有改變。
4. **終止**：每次輸出一項並推進其來源，直到取滿 q 項或來源全部耗盡。

有序性保證「只需比較前端」；min-heap 則讓比較 r 個前端更有效率。Sedgewick–Wayne 的 [Multiway 原始碼](https://algs4.cs.princeton.edu/code/edu/princeton/cs/algs4/Multiway.java.html) 正是對有序輸入流使用 indexed min-priority queue，取出後只讀取同一來源的下一項。

## 2. 不同方法的成本與適用範圍

以下假設比較與單項讀寫為 O(1)，r 為非空來源數，輸出儲存另計。

| 方法 | 主要成本 | 輔助資訊與限制 |
|---|---|---|
| 每次線性掃描所有前端 | q 次選取 O(qr) | r 個游標；適合來源極少時 |
| Binary heap | 線性建堆後 O(r + q log(r+1)) | O(r) 候選；可只取前綴 |
| 平衡的 winner / loser tree | 建立 O(r)，每次更新 O(log(r+1)) | O(r) 樹節點；沿來源到根的路徑更新 |
| 平衡的兩兩合併 | 全部 N 項為 O(N log(r+1)) 上界 | 緩衝與鏈結方式決定空間；不是每次選 r 個前端的同一種排程 |

空來源若尚未排除，須另計掃描來源清單的成本。任意順序逐一 `push` 的建堆上界是 O(r log(r+1))；O(r) 建堆需採 bottom-up heapify，或另外證明特定插入順序的成本。

本次 373 程式的初始 `(i,0)` 按 i 遞增，總和非遞減；對 binary min-heap，新項不需向上移動，因此這個特例可以線性初始化。其 heap 空間 O(m)，輸出另占 O(q)。還可只納入前 `min(m,q)` 列：對更後面的列首，前面已有至少 q 個列首不大於它，足以構成合法的前 q 組；同分時不要求挑固定索引。

### 為什麼一般不能期待所有情況都線性合併？

在 comparison model、各來源內部順序固定、key 互異時，來源長度 `n₁,…,nᵣ` 可能有 `N! / (n₁!…nᵣ!)` 種交錯。區分它們需要至少該數量的 log₂ 次比較。來源等長、r ≥ 2 時，這給出最壞 Ω(N log r) 的比較下界。

這是全量合併在適當輸入族上的最壞下界；來源長度極不均、只取前 q 項、或 key 有額外結構時，不能直接宣稱每個輸入都需要 N log r 次比較。另須計入實際輸出 N 項的成本。

## 3. 可確認的歷史：先有儲存與合併的需求，再看選取前端的工具

### 1946、1959、1960：磁帶 merge 的早期文獻鏈

Knuth 在 *The Dangers of Computer-Science Theory*（1973 年出版的論文）第 191 頁，將 balanced merge 連到 Mauchly（1946）、cascade merge 連到 Betz–Carter（1959）、polyphase merge 連到 Gilstad（1960），並明確描述後兩者使用多路合併。[Knuth 原文，第 191 頁與文末書目](https://gwern.net/doc/math/1973-knuth.pdf#page=3)

**證據邊界**：這是 Knuth 對早期工作的回顧，本次未直接讀到上述三份原始文獻全文；1946 年不能因此寫成「現代 heap k-way merge 的發明年」。Cascade / polyphase 主要還涉及 runs 在磁帶間如何分配與安排多輪合併，與單次如何選出最小前端分屬不同層次。

### 1964：直接可讀的 IBM 技術報告

J. W. Toner 的 *Sorting Technology in Programming*，IBM 報告 Z77-4469，封面日期 **1964-07-09**，描述先在主記憶體排序資料區段、寫出有序 sequences，再合併成更長序列，並研究 polyphase 等不平衡合併安排。[原始報告，封面與 Introduction](https://www.bitsavers.org/pdf/ibm/technical_information_exchange/Z77-4469_Toner_-_Sorting_Technology_in_Programming_19640709.pdf)

這份直接證據說明當時的問題背景是記憶體容量與外部儲存流程，不是面試中的 pair sum；不據此宣稱 Toner 發明多路合併。

### 1964：Williams 的 heap 是一個工具節點

J. W. J. Williams 的 *Algorithm 232: Heapsort* 發表於 *Communications of the ACM* 7(6)，347–348，1964 年 6 月。原文提供 heap 的建立、加入、移除最小值等操作。[原文重印集](https://bitsavers.trailing-edge.com/pdf/acm/collected_algorithms_from_acm/Collected_Algorithms_from_ACM_Volume_2_Algorithms_221-492_1980.pdf)、[Sedgewick–Wayne 參考文獻書目](https://algs4.cs.princeton.edu/references/)

它與今日用 binary heap 選出來源前端有技術關係，但 **heapsort 是對任意輸入排序；k-way merge 是合併已有序來源**。該論文不能作為 Williams 發明多路合併、或 LC 373 源自此文的證據。

### 教材整理：Knuth 的外部排序章

*The Art of Computer Programming, Volume 3: Sorting and Searching* 第二版（1998）的出版社目錄，將 **Multiway Merging and Replacement Selection** 放在 **External Sorting** 下，另列 polyphase、cascade 與磁帶合併的實務考量。[出版社書目與目錄](https://www.informit.com/store/art-of-computer-programming-volume-3-sorting-and-searching-9780201896855)

此處核對的是第二版的出版資訊與章節結構，沒有逐頁核讀整章，也不把教材收錄當成發明歸屬。Replacement selection 用於形成初始 runs；多路合併用於合併既有 runs，雖可共享選取資料結構，卻不是同一階段。

### 1988：從 CPU 比較次數轉向 I/O 複雜度

Aggarwal 與 Vitter 的 *The Input/Output Complexity of Sorting and Related Problems*，*CACM* 31(9)，1116–1127，研究主記憶體與次級儲存之間的 block transfers。論文 §5 描述每個輸入 run 保留一個 block，耗盡後再從同一 run 讀下一塊。[原文，第 1116 與 1123 頁](https://www.cse.wustl.edu/~angelee/archive/cse341/fall14/papers/AggarwalVi88.pdf)

這與「每來源保留前端」同方向，但外部排序還須為每路保留輸入 buffer 與輸出 buffer；能同時合併幾路受記憶體與 block 大小限制，不能只照面試版把 r 開到任意大。這是後續成本模型研究，不是多路合併的起源論文。

### 2022／2023：Multiway Powersort 與實作選擇

Cawley Gelling、Nebel、Smith、Wild 的 *Multiway Powersort*，2022 年提交預印本、2023 年發表於 ALENEX，研究利用既有 runs 的多路合併排序與合併次序。其 4-way 實作用 winner tree，並說明在小樹可留於 registers 的情況下，未必有理由改用 loser tree。[論文與版本資訊](https://arxiv.org/abs/2209.06909)、[全文，§4.1](https://arxiv.org/html/2209.06909v2)

這提醒我們：heap、winner tree、loser tree 共享候選前端的觀念，但常數成本取決於來源數、比較成本與記憶體布局，不能籠統宣稱 loser tree 永遠更快。GNU libstdc++ 的 parallel-mode 文件也直接列出 `multiway_merge_loser_tree`，提供實際工程用途的另一個例子；這不是 C++ 標準必備 API。[GNU 官方文件](https://gcc.gnu.org/onlinedocs/gcc-11.4.0/libstdc%2B%2B/api/a01669.html)

## 4. Heap、winner tree、loser tree：同一選取任務的不同表示

- **Heap**：維持局部父子順序，根是全域最小候選；取出後恢復 heap order。面試用標準 priority queue 即可表達。
- **Winner tree**：來源前端在葉端參賽，每個內部節點保留兩個子樹的勝者。某來源更新後，重算該葉到根的比賽。
- **Loser tree**：內部節點保留對戰的敗者，整體勝者另外保存；勝者來源換下一項後，沿其路徑與保存的對手重賽。

這些樹中的比較是**選取當前最小項**，不是先把所有輸入資料排進樹。來源單調性讓未暴露的元素能被前端代表，才是整個演算法能少存資料的理由。

## 5. 相近但不同的問題

| 概念 | 要解決的問題 | 與 k-way merge 的界線 |
|---|---|---|
| 固定大小 max-heap Top-q | 在任意已見候選中保留最小 q 項 | 不必有序來源，但可能仍需查看全部候選 |
| Heap frontier | 從各有序來源前端選下一項 | heap 大小由來源數決定，不是由答案數決定 |
| Merge scheduling | 多個 runs 應先合併哪些、每輪幾路 | 決定合併樹與總資料搬移量，不等於單次合併的選取器 |
| Replacement selection | 從原始資料產生初始有序 runs | 外部排序的 run formation，並非直接合併既有 runs |
| 一般二維 best-first search | 每個候選可能從多條路徑到達 | 可能需要 visited；373 的固定列分解只有同列前驅，故不用去重索引 |

**相關題型**：23 是顯式有序 lists；373 是隱式配對列；378 可把 sorted matrix 的每列當來源；355 的 k-way merge 版本把各作者貼文視為由新到舊的來源，以 max-heap 取最新候選；632 則在每來源一個候選之外，額外維護範圍上界。

題面參考：[23](https://leetcode.com/problems/merge-k-sorted-lists/)、[378](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/)、[355](https://leetcode.com/problems/design-twitter/)、[632](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/)。上述是演算法關係，不是聲稱題目之間有歷史傳承。

## 6. 閱讀路線與重練

1. 先讀本文的 frontier invariant，再看 [Sedgewick–Wayne 的 Multiway](https://algs4.cs.princeton.edu/code/edu/princeton/cs/algs4/Multiway.java.html)，對照「取出來源、只補同來源」。
2. 歷史背景讀 Toner 報告的 Introduction 與 Knuth 回顧的第 191 頁，區分磁帶合併排程與選取器。
3. 想理解超出記憶體的資料，讀 Aggarwal–Vitter §1、§5；想看現代常數成本與多路合併次序，讀 Multiway Powersort。
4. 重練見 [Problem Review](../Checklists/Lists/09_Problem_Review.md)；相關概念摘要見 [K-way Merge／Heap Frontier](../Meta_Frameworks/State_Transition_Algorithm_Atlas.md#merge-k) 與 [Heap 決策](../Data_Structures/Heaps/01-Heap_Decision_Making.md)。

## ✅ 閱讀後應能回答

- [ ] 為什麼尚未加入 heap 的元素，不會比所有來源前端都更小？
- [ ] 為什麼取出後只補同一來源？來源耗盡、key 同分如何處理？
- [ ] r 與 q 各代表什麼？heap 空間和輸出空間如何區分？
- [ ] 多路合併、heapsort、replacement selection、merge scheduling 的差別？
- [ ] 哪些歷史結論是直接閱讀的原文，哪些只由後人回顧得知？
