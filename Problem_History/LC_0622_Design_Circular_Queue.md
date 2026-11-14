# 622. Design Circular Queue：循環緩衝的歷史與教科書實作

**記憶線索：資料不用搬，索引繞回來；先定義索引語義，再決定如何區分空與滿。**

Technique summary：`Circular Array + Queue State Tracking`

來源查證日期：2026-11-14；整理日期：2026-11-15。依前次實際讀取的原始文獻、教科書節錄與作者公開程式整理。

## 1. 題目與歷史定位

[LeetCode 622 官方題面](https://leetcode.com/problems/design-circular-queue/)要求實作固定容量的 FIFO queue，並直接將 circular queue 稱為 **Ring Buffer**。滿時插入失敗，空時刪除失敗；它不要求多執行緒同步，也不採用滿時覆寫舊資料的規則。

這是經典循環緩衝資料結構的介面實作題。**可以確認這項技術遠早於 LeetCode；目前不能確認最初發明者、LC 622 的官方首次發布日期，或它直接改編自哪本教材。**

## 2. 1965 年的原始文獻證據

Edsger W. Dijkstra 的 **Cooperating Sequential Processes（EWD123）** 第 4.1 節，在 producer–consumer 的 FIFO buffer 情境下，提到文獻中兩種熟知的實作技術：

> “two well-known techniques … ‘cyclic buffering’ and ‘chaining’”

- [EWD123 原文，第 4.1 節](https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD123.html)
- [原始掃描 PDF，見文件頁碼 32](https://www.cs.utexas.edu/~EWD/ewd01xx/EWD123.PDF)

文件年代有本人回憶佐證：Dijkstra 在 **Twenty-eight years（EWD1000）** 中說明，EWD123 寫於 **1965 年**，並作為當年秋季課程的講義。[EWD1000 原文](https://www.cs.utexas.edu/~EWD/transcriptions/EWD10xx/EWD1000.html)

**這支持「cyclic buffering 至少在 1965 年已被當作熟知技術」，不支持「Dijkstra 於 1965 年發明 circular queue」。** EWD123 該段刻意不展開 buffer 的具體實作，也沒有提供可據以確認最初發明者的歸屬。

文中的情境是電腦產生待輸出的卡片資料、打卡機以不同節奏消費資料：buffer 用來吸收短時間的速度落差。這解釋了 FIFO buffer 的需求；循環陣列則是實現該抽象的一種方式。

## 3. LC 622 的公開紀錄與限制

| 紀錄 | 可確認的內容 | 不能推論的事 |
|---|---|---|
| [官方題面](https://leetcode.com/problems/design-circular-queue/) | 題號、名稱、介面與 Ring Buffer 用語 | 未交代最初出題者或歷史來源 |
| [liuyubobobo 的解題原始檔](https://github.com/liuyubobobo/Play-Leetcode/blob/master/0501-1000/0622-Design-Circular-Queue/cpp-0622/main.cpp) | 檔案註記日期為 2018-08-24，並連到官方題目 | 註記不是官方發布紀錄，也不是已核對的 Git 首次提交日期 |
| [第三方 leetcode.ca 頁面](https://leetcode.ca/2017-08-13-622-Design-Circular-Queue/) | 頁面標示 2017-08-13 | 未獨立驗證該日期的形成方式，不能當成官方上線日 |

上述資料是公開紀錄線索，不據此指定官方發布年份或直接命題來源。

## 4. 教科書實作比較

以下統一用 **0-based indexing**，`N` 表示底層陣列長度；公式是整理後的表示法，不是原書逐字轉錄。

| 教材 | 核心狀態 | 空／滿的區分 | 容量策略 |
|---|---|---|---|
| CLRS，Introduction to Algorithms，§10.1 Stacks and queues | `head`、`tail` | 保留一格 | 長度 `N` 最多放 `N−1` 個元素 |
| Goodrich、Tamassia、Mount、Goldwasser，Data Structures and Algorithms in C++，2024 zyBooks 版 | 隊首 `f`、元素數 `sz` | 直接檢查 `sz` | 固定容量，全部格子可用 |
| Pat Morin，Open Data Structures，§2.3 ArrayQueue | 隊首 `j`、元素數 `n` | 直接檢查 `n` | 動態擴縮陣列 |

### 4.1 CLRS：兩個索引，保留一格

- `head` 指向下一個要取出的元素。
- `tail` 指向下一次插入的位置，**不是最後一個元素**。
- 空：`head == tail`。
- 滿：`(tail + 1) % N == head`。
- 入隊：寫入 `a[tail]`，再令 `tail = (tail + 1) % N`。
- 出隊：讀取 `a[head]`，再令 `head = (head + 1) % N`。

Invariant：有效元素是從 `head` 開始、到 `tail` 之前的循環區間；元素數可由 `(tail - head + N) % N` 求得。

若允許放滿 `N` 個，`tail` 會再次追上 `head`，與空的表示相同。因此此版本保留一格，將可能長度限制在 `0..N−1`。套用 LC 622 的容量 `k` 時，配置 **`k + 1` 格**。

[本次查閱的 CLRS 原書節錄](https://itn-web.it.liu.se/~chrsc91/teaching/f17/tnsl20/readingmaterial/Cormen-datastructures.pdf)位於 §10.1、印刷頁 201–203。原文使用 1-based indexing，以條件分支在陣列末端繞回；ENQUEUE／DEQUEUE 主體省略 overflow／underflow 檢查，不能原樣當成 LC 的完整介面。不同版次應另核對頁碼。

### 4.2 Goodrich：隊首與元素數，推導插入位置

2024 年 C++ zyBooks 版的作者程式保存 `f`、`sz`、`capacity`，不另存尾端索引：

| 意義 | 公式／條件 |
|---|---|
| 空 | `sz == 0` |
| 滿 | `sz == capacity` |
| 下一次插入位置 | `(f + sz) % capacity` |
| 非空時的最後元素位置 | `(f + sz - 1) % capacity` |

Invariant：**第 `i` 個邏輯元素位於 `data[(f + i) % capacity]`，其中 `0 <= i < sz`。** 插入時延長邏輯序列；刪除時推進 `f` 並減少 `sz`，資料本身不用搬移。

這是最接近 LC 622 固定容量需求的教材版本。原書 `push` 在滿時丟出 `overflow_error`；LC 改為回傳 `false`。原始程式的 `pop`、`front`、`back` 未自行檢查空狀態，套用 LC 時必須補上題目要求的判斷。

- [作者提供的 array_queue.h 原始碼](https://github.com/goldwasser/DSAC/blob/main/stackqueue/array_queue.h)
- [官方 ArrayQueue API 文件](https://goldwasser.github.io/DSAC/classdsac_1_1stackqueue_1_1_array_queue.html)
- [官方書籍與程式網站](https://goldwasser.github.io/DSAC/)

### 4.3 Open Data Structures：相同循環索引，再加入 resize

Pat Morin 從「如果有無限陣列，就能一直往後寫」出發，再用有限陣列與取模運算模擬它：

- `j` 是隊首，`n` 是元素數。
- 入隊寫入 `a[(j + n) % a.length]`，再增加 `n`。
- 出隊讀取 `a[j]`，再推進 `j` 並減少 `n`。
- resize 時，將舊陣列中第 `i` 個邏輯元素複製到新陣列 `b[i]`，最後設 `j = 0`。

此書的 ArrayQueue 會自動擴縮，不能直接把「滿時擴容」帶入 LC 622；固定容量版本應改成拒絕插入。

[免費原書 §2.3：ArrayQueue — An Array-Based Queue](https://opendatastructures.org/ods-java/2_3_ArrayQueue_Array_Based_.html)，含完整操作、resize 程式與攤銷分析。

### 複雜度

| 版本 | 入隊／出隊 | 空間 |
|---|---|---|
| CLRS 保留一格、Goodrich 固定容量 | 最壞 O(1) | O(N) |
| Open Data Structures 動態擴縮 | 攤銷 O(1)；resize 的單次操作可達 O(n) | O(n + 1) |

## 5. 如何理解不同的狀態設計

兩個循環索引相等時，可能表示沒有元素，也可能表示剛好繞完一圈。實作必須用額外資訊或容量限制消除歧義：

- **保留一格**：用可用容量換取只保存兩個索引。
- **保存元素數**：所有格子可用，空／滿直接由計數決定。
- **保存剩餘容量 `available`**：固定容量下，與保存元素數等價，因為 `size = capacity - available`。

最後一項是狀態等價性的推導，**不是宣稱以上三本書都使用 `available`**。若同時保存隊首、下一個插入位置及計數，三者之間還須維持一致關係；尾端索引也可以由隊首與計數推導。

## 6. 相關但不同：producer–consumer 與執行緒安全

循環陣列解決的是儲存重用與 FIFO 位置管理，並不自動保證執行緒安全。滿時拒絕、阻塞等待、覆寫舊資料，是不同的介面契約。

[Linux 官方 Circular Buffers 文件](https://cdn.kernel.org/doc/html/latest/core-api/circular-buffers.html)進一步討論單一 producer／單一 consumer 的循環緩衝與 memory barriers。它是系統程式的延伸參考，**不是 LC 622 的直接歷史來源，也不能將其同步技巧不加條件套用到多 producer／多 consumer**。

## ✅ 閱讀後應能回答

- [ ] 為何 1965 年的文獻證據不能用來指定 circular queue 的發明者？
- [ ] `tail` 是最後一個元素，還是下一次插入位置？這如何影響公式？
- [ ] 只保存兩個循環索引時，為何需要區分空與滿？
- [ ] 為何容量 `k` 在保留一格版本要配置 `k + 1` 格？
- [ ] 如何只用隊首與元素數，推導插入位置與最後元素位置？
- [ ] 動態擴縮的教材版本與 LC 622 的固定容量契約有何差異？
- [ ] 為何循環陣列的正確性與多執行緒同步必須分別處理？
