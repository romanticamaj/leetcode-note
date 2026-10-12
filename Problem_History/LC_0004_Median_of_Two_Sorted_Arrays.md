# 4. Median of Two Sorted Arrays：從排名選擇到平行合併

**記憶線索：不必真的合併，就能找出「合併結果的前半段，分別來自兩個輸入的多少元素」。**

查證日期：2026-10-12。

## 題目情境與查證結論

LC 4 給兩個可不等長的 sorted arrays，要求 O(log(m+n)) 時間求中位數；總數為偶數時，回傳中央兩值的平均。[LeetCode 原題](https://leetcode.com/problems/median-of-two-sorted-arrays/)

這個問題有遠早於現今 LeetCode 題面的文獻紀錄。本次找到的直接早期證據是 **Shamos 於 1976 年發表的 Theorem 3.3**；後來也出現在平行合併研究與演算法課程。

必須分開三件事：**問題已有早期紀錄、某個演算法的作者歸屬、LeetCode 從哪裡取題**。目前無法確認最初發明者、LeetCode 的直接來源或首次收錄日期。

## 可確認的歷史

### 1976：Shamos 記載等長版本，歸屬 Jefferson 的私人通信

Michael Ian Shamos 的〈Geometry and Statistics: Problems at the Interface〉收錄於 J. F. Traub 編的 *Algorithms and Complexity: New Directions and Recent Results*，1976，251–280 頁。作者的出版清單確認年份。[作者出版清單](https://euro.ecom.cmu.edu/people/faculty/mshamos/index.shtml)

書內第 256 頁的 **Theorem 3.3 [Jefferson (76)]** 指出：兩個各有 N 個元素的排序集合，其共同中位數可在 O(log N) 時間求得。第 278 頁將該引用列為 **Jefferson, D.，private communication**。[原文 PDF，第 256、278 頁](https://euro.ecom.cmu.edu/people/faculty/mshamos/1976Stat.pdf)

文中比較兩側各自的中位數，以排名論證排除兩端，再遞迴求更小的同型問題，得到 T(N) = T(N/2) + O(1)。這是等長版本的概要，不是今日不等長陣列的 sentinel／切點程式。

因此可寫「Shamos 在 1976 年記載並歸屬於 D. Jefferson」，不能寫成「Jefferson 在 1976 年首次發明 LC 4」。私人通信也不是可另行查閱的正式論文。

### 1987：Co-ranking 的早期歸屬，來自後續作者明確回溯

Selim G. Akl 與 Nicola Santoro 發表〈Optimal Parallel Merging and Sorting Without Memory Conflicts〉，*IEEE Transactions on Computers*，C-36(11)，1367–1369，1987 年 11 月。[作者研究群出版紀錄](https://research.cs.queensu.ca/Parallel/publications.html)、[DOI](https://doi.org/10.1109/TC.1987.5009478)

Siebert 與 Träff 的 2013 年論文在 Introduction 明確把 **co-ranking 的引入歸給這篇 1987 年論文**。這是後續研究者的歷史歸屬；本次未取得 1987 年全文，不把它寫成已逐式核對原始演算法，也不把 co-ranking 的歸屬擴大成整個中位數問題的發明權。[2013 年論文，Introduction](https://arxiv.org/html/1303.4312)

### 1994：選擇指定排名，用來切分平行合併工作

Narsingh Deo、Amit Jain、Muralidhar Medidi 的〈An Optimal Parallel Algorithm for Merging Using Multiselection〉刊於 *Information Processing Letters*，50(2)，81–87，1994 年 4 月 22 日。[出版社紀錄](https://www.sciencedirect.com/science/article/abs/pii/0020019094000093)

論文直接定義：從兩個排序序列的合併結果，選出第 k 小元素，但不必實際合併。接著選出多個排名，把輸入分成可交給不同處理器合併的子問題。第 2 節也專門討論 Selection in Two Sorted Arrays。[論文全文，第 1–2 節](https://www.cs.ucdavis.edu/~amenta/f15/merging.pdf)

這證明中位數／排名選擇不只是獨立練習題，也是平行合併的工具；不能據此斷言這就是問題最初被提出的用途。

### 2005–2007：可查證的課程與教材使用

- **MIT 2005 年 12 月 5 日的 Problem Set 9，Problem 9-1(a)**：要求從兩個合計 N 個元素的排序陣列，以 Θ(log N) 求中位數；(b) 用它設計平行合併，(c) 再推廣成任意 order statistic。[MIT 原始作業](https://ocw.mit.edu/courses/6-046j-introduction-to-algorithms-sma-5503-fall-2005/87b244e363192122fbd8892b4dea4a8f_ps9.pdf)
- **UIC 2007 年課程解答的 Exercise 9.3-8**：對應 CLRS 的等長雙排序陣列問題，以遞迴排除兩端說明；示範另假設長度為 2^k−1，且採 lower median，不能直接當成 LeetCode 偶數平均版本。[UIC 原始解答](https://homepages.math.uic.edu/~leon/cs-mcs401-f07/exercises/exer8-9-solutions.pdf)

這些是課程使用紀錄，不是題目的誕生年份，也沒有證明 LeetCode 直接取自 CLRS。

### 2013：與目前數量不變量最直接對照的文獻

Christian Siebert 與 Jesper Larsson Träff 的〈Perfectly Load-Balanced, Optimal, Stable, Parallel Merge〉於 2013 年 3 月 18 日提交 arXiv，11 月 12 日修訂。第 2 節以輸出前綴長度決定兩個輸入前綴，維持兩者長度總和固定，並比較跨陣列邊界；文中也使用概念上的 ±∞ sentinel。[論文與版本日期](https://arxiv.org/abs/1303.4312)、[第 2 節全文](https://arxiv.org/html/1303.4312)

這篇提供清楚、可核對的 co-ranking 定義與實作，但作者已明言想法有更早來源；不能把 2013 當作切點思路的發明年份。

## 🧠 數學觀點：先定義答案，再固定數量

以下是理解 LC 4 的推導，不是聲稱還原最初作者的思考歷程。

中位數分界需要兩個條件：

1. **數量**：偶數時左右一樣多；奇數時左側多一個。
2. **順序**：左側所有元素 <= 右側所有元素。

先設定左側所需數量，再讓兩個輸入提供相應前綴：

```text
leftSize = (m + n + 1) / 2
i + j = leftSize
j = leftSize - i
```

數量條件由構造維持，於是只需搜尋 i，使跨陣列順序也成立。切點 i 表示 `[0,i)` 與 `[i,m)`，也就是左段拿 i 個；空段可表示，因此候選包含 0 與 m。

這次學習的核心是 **答案定義 → 數量不變量 → 消去一個自由度 → 依順序違反排除候選**。Cut position 是承載這個設計的表示法，通用概念見 [Index as Cut](../Data_Structures/Arrays_and_Strings/Index_as_Cut.md)。

## 和實際用途的關係

若要把合併工作平均分給處理器，直接把兩個輸入各切一半，不保證每份能產生合併輸出的連續一段。
反過來先指定輸出要切在哪個排名，再找兩個輸入各自應提供多少前綴，就能建立相應的合併工作；這正是上述 multiselection／co-ranking 文獻研究的用途。
Median 可視為只關心中央分界的特例，但這是數學關係，不是已證實的 LeetCode 傳承路徑。

## ⚠️ 相關但不同的概念與未解問題

- **早期 median 定義**：文獻可能選 lower median 或 upper median；LeetCode 偶數時取兩個中央值的平均，應先核對定義。
- **Stable merge**：2013 年 co-ranking 為固定相等元素的先後，跨界條件一個用 <=、另一個用 <；LC 4 只求數值，兩側皆允許 <=，合法切點可能不唯一。
- **X+Y 不是合併**：Frederickson 與 Johnson 的 1982 年論文研究 Cartesian sum 與排序欄矩陣；X+Y 表示所有 x+y，可能有 mn 個值，不是本題的 m+n 個輸入元素。[1982 年出版社紀錄與摘要](https://www.sciencedirect.com/science/article/pii/0022000082900484)
- **LeetCode 收錄時間未知**：網路留下帶 `/2011/03/` 的舊站網址線索，但本次未取得原頁或可信存檔，不把網址中的年月當成已確認的上線日期。現行 editorial 的日期也不能代替題目首次收錄日期。
- **最早來源仍未知**：本次最早直接核對到的是 1976 年記載；未找到更早證據，不等於證明此前不存在。今日常見的單一切點 binary search 程式，也未確認唯一原作者。

## 來源閱讀順序

1. **Shamos 1976，第 256、278 頁**：先看同型問題與 Jefferson 的歸屬，注意不是完整現代程式。
2. **Deo、Jain、Medidi 1994，第 1–2 節**：看 selection 為何與 parallel merge 相連。
3. **MIT 2005，Problem 9-1**：看中位數如何成為下一個演算法的子程序。
4. **Siebert、Träff 2013，第 1–2 節**：對照前綴長度、不變量、跨界比較與歷史引用。

各來源直接連結與支持範圍已列在對應段落；以上構成可查證的問題背景，不代表一條已完整證實的直接傳承鏈。
