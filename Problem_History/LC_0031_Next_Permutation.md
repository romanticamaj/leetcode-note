# 31. Next Permutation：字典序後繼的歷史

**記憶線索：右側已經排到最大，就向左找最後一個還能增加的位置；只讓它增加一點，再把右側降到最小。**

查證日期：2026-10-16。

## 題目情境與查證結論

[LeetCode 31](https://leetcode.com/problems/next-permutation/) 要在原陣列上找下一個字典序更大的排列；若目前已是最大排列，就回到最小排列。允許重複數值，且要求 O(1) 額外空間。

這是**字典序排列生成**的單步問題，早於 LeetCode 與 C++ 的 STL。可核對的文獻鏈包括：Sedgewick 在 1977 年的研究綜述回溯到 1812 年的 Fischer–Krause 著作，並列出 1962–1967 年的電腦演算法；Stepanov 與 Lee 在 1994 年的 STL 提案中列出 `nextPermutation`。**這些文獻不能證明 LeetCode 題面直接取自其中任何一本，也不能確定最初發明者。**

## 可確認的歷史

### 1356：更早的排列組合背景，精確演算法歸屬仍需保留

數學史研究者 Kim Plofker 記載：Nārāyaṇa Paṇḍita 的《Gaṇita-kaumudī》完成於 **1356 年**，書中有關於排列與組合的一節。[Plofker 原書 PDF，第 208 頁](https://sanskrit.uohyd.ac.in/Algorithms_in_Ancient_India/Material/Kim_Plofkar_Maths_in_India.pdf)

今日常見資料會把「下一個字典序排列」歸給 Nārāyaṇa，但本次直接核對的 Plofker 段落只支持**他的著作討論排列組合**；它不足以逐步核對與現代 pivot／swap／reverse 程序完全相同，更不足以證明他是最初發明者。因此這裡把 1356 年列為較早的數學背景，**不當作現代程式步驟的確定首發年**。

### 1812：Fischer–Krause 的早期文字記載

Robert Sedgewick 在 1977 年的〈Permutation Generation Methods〉記載：Hall 與 Knuth 將一種字典序前後繼生成方法回溯到 **Fischer 與 Krause 於 1812 年出版的著作**，並指出此法多次被重新發現。[Sedgewick 原論文，第 153 頁及參考文獻](https://sedgewick.io/wp-content/themes/sedgewick/papers/1977Permutation.pdf)

Sedgewick 展示的 Fischer–Krause 版本沿著**反向字典序**操作，從左邊掃描並處理 prefix；今日 LC 31 通常從右邊掃描並處理 suffix。兩者有鏡像的設計結構，但不能把 1812 年的敘述寫成「那時已有今日 LeetCode 題面的逐行程式」。本次未直接查閱 1812 年原書；1812 年的歸屬是**根據 Sedgewick 對早期文獻的回溯**。

### 1962–1977：電腦演算法文獻中的字典序生成

Sedgewick 記載，Schrack 與 Shimrat 的 **Algorithm 102** 刊於 *Communications of the ACM* 1962 年 6 月；Mok-Kong Shen 的 1962 年文章給出較完整的表述，1963 年又刊出 **Algorithm 202: Generation of Permutations in Lexicographical Order**；J. P. N. Phillips 於 1967 年發表最佳化版本。[Sedgewick 原論文，第 153 頁及參考文獻](https://sedgewick.io/wp-content/themes/sedgewick/papers/1977Permutation.pdf)、[Shen 1963 年原文 DOI](https://doi.org/10.1145/367593.367604)

Sedgewick 的例子直接從右側已達最大排列的區段推導下一步：`BACFHGED` 的尾端 `HGED` 已不能自行變得更大，所以要改動更左方的位置，再把後續部分排成最小可能結果 `BACGDEFH`。這與本題最重要的推理完全同型；這是**問題與方法的對照**，不是 LeetCode 的取題來源證據。[Sedgewick 原論文，第 153 頁](https://sedgewick.io/wp-content/themes/sedgewick/papers/1977Permutation.pdf)

### 1994–1998：從 STL 提案到 C++ 標準函式庫

Stepanov 與 Lee 在 **1994 年 3 月 7 日**的 *The Standard Template Library* 簡報中，把 `nextPermutation` 與 `prevPermutation` 列為 permutation generators。這至少證實，LC 31 所考的操作在 LeetCode 出現之前，已被當作泛型程式庫的演算法介面。[Stepanov–Lee 原始簡報，第 16–17 頁](https://www.stepanovpapers.com/Stepanov-The_Standard_Template_Library-1994.pdf)

目前查到**可直接閱讀的早期 C++ 實作**是作者保存的 **1995 年 10 月 31 日 HP STL 發行包**中的 [`ALGO.H`](https://www.stepanovpapers.com/butler.hpl.hp/stl/stl/ALGO.H)。檔頭標有 Hewlett-Packard 1994 年版權，這與發行包的 1995 年日期是不同資訊；版權年本身不能證明此份檔案在 1994 年哪一天已公開。[Stepanov 原始資料集的發行包索引](https://www.stepanovpapers.com/)

同一發行包的**文件封面日期為 1995 年 10 月 31 日**，在 §10.3.9 列出 `next_permutation(first, last)` 與比較器版本：成功回傳 `true`，若已是最後一個排列，則改成最小排列並回傳 `false`。[Stepanov–Lee 原始文件，封面與第 54 頁](https://www.stepanovpapers.com/STL/DOC.PDF) 作者資料集另列一份 **1995 年 11 月 14 日**的修訂技術報告，稱其修訂了 **1994 年 5 月的 C++ 標準委員會提案 N0482**；資料集提供的連結卻通往封面標示 10 月 31 日的文件，因此不把 11 月 14 日當成此 PDF 的日期。[作者資料集的版本說明](https://www.stepanovpapers.com/)

後來的 C++ 標準程式庫提供 `std::next_permutation`，C++98 的標準參照已列有它。**LeetCode 31 只要求改動陣列，沒有回傳布林值。**[Apache C++ 標準程式庫文件與 C++98 標準參照](https://stdcxx.apache.org/doc/stdlibref/next-permutation.html)、[LeetCode 原題](https://leetcode.com/problems/next-permutation/)

## 原始 C++ 實作怎麼對應本題

1995 年 HP STL 的 [`ALGO.H`，`next_permutation` 定義](https://www.stepanovpapers.com/butler.hpl.hp/stl/stl/ALGO.H) 使用 `BidirectionalIterator`，只要求迭代器能前進、後退與交換元素。它先處理空區間與單一元素，再由 `last` 往左走：

| 原始碼中的動作 | 意義 |
|---|---|
| `ii = i--`、檢查 `*i < *ii` | 從尾端找最右邊的嚴格上升 pair；左邊的 `i` 是 pivot，`ii` 是 suffix 起點 |
| 從 `last` 反向移動 `j`，直到 `*i < *j` | 在非遞增 suffix 找到最小的較大值；嚴格比較同時處理重複值 |
| `iter_swap(i, j)`，再 `reverse(ii, last)` | 讓 pivot 增加最少，並把 suffix 設為最小 |
| 找不到 pivot 時 `reverse(first, last)`、回傳 `false` | 最大排列回到最小排列 |

這也回答「主流做法是不是從 `n - 2` 看 `i + 1`」：1995 年函式庫是**由尾端往左比較相鄰元素**，只是用雙向迭代器表示，不用整數索引。它採「先 swap、再 reverse」；日誌中的「先 reverse、再從左找較大值 swap」是等價變形。[HP 原始碼](https://www.stepanovpapers.com/butler.hpl.hp/stl/stl/ALGO.H)、[刷題日誌](../Checklists/Practice_Log.md)

這份來源能證明 HP STL 的實作**長什麼樣**，但原始碼沒有註明它直接改寫自 Shen、Phillips 或其他哪篇排列生成論文。因此「演算法有較早文獻」與「特定 C++ 程式碼從哪份文獻承襲」要分開說。

## 🧠 數學觀點：為什麼是 pivot、最小增量、最小 suffix

以下是本題的解題推導，不是聲稱還原歷史作者的發明過程。

字典序比較先看**最左邊不同的位置**。要找「恰好下一個」，就應盡量讓前面的數字保持不變。

1. 從右往左找到最長的**非遞增 suffix**。它已是這些元素在當前 prefix 下能形成的最大排列；只重排這段，不可能得到更大的整體排列。
2. suffix 左邊的元素就是 pivot。要讓整體稍微變大，選 suffix 中**嚴格大於 pivot 的最小值**來交換。因 suffix 非遞增，這是從右往左找到的第一個較大值。
3. pivot 增大後，把 suffix 變成當前元素的最小排列。交換後 suffix 仍非遞增，反轉即可變成非遞減；**相等元素也因此得到正確處理**。

若找不到 pivot，整列非遞增，已是最大排列；反轉整列就回到最小排列。每一步至多掃描、交換、反轉陣列，故單次時間 **O(n)**、額外空間 **O(1)**。

例如 `1 4 3 2 → 2 1 3 4`：`4 3 2` 已最大化；把 pivot `1` 換成可用的最小較大值 `2`，再把 suffix 調到最小。

先反轉 suffix、再從左找到第一個嚴格較大值交換，也能得到同一結果：反轉後 suffix 非遞減，找到的就是最小較大值。這是 [2026-10-16 刷題日誌](../Checklists/Practice_Log.md) 中實作順序與常見順序的關係。重練目標見 [Problem Review](../Checklists/Lists/09_Problem_Review.md)。

## ⚠️ 相關但不同的概念與證據界線

- **排列組合的古代記載 ≠ 現代程式逐步同源**：1356 年著作中的排列討論是較早背景；目前未以原文逐步確認今日 pivot／swap／reverse 算法。
- **字典序生成 ≠ 所有排列生成**：此題要求緊接的字典序後繼。只要求列舉所有排列的其他方法，即使也能生成所有答案，順序可能不同。
- **重複值**：LeetCode 允許相等元素；pivot 的比較需用嚴格 `<`，suffix 的掃描需把相等留在非遞增區段。Sedgewick 的該段研究示例先假設元素互異，不可把其示例直接當成重複值的證明。
- **最初發明與 LeetCode 上線日期未知**：本次沒有找到能證明最初發明者、LC 31 直接來源或首次上線日期的一手材料。
- **最早的 C++ 實作版本未知**：1994 年簡報證實介面存在，1995 年發行包提供可讀實作；目前資料不足以判定是否還有更早的 C++ 原始碼版本，或該函式最初寫成程式碼的日期。

## 來源與延伸閱讀

1. **Kim Plofker，*Mathematics in India*，2009，第 208 頁。** [書籍 PDF](https://sanskrit.uohyd.ac.in/Algorithms_in_Ancient_India/Material/Kim_Plofkar_Maths_in_India.pdf)。支持《Gaṇita-kaumudī》的完成日期與排列組合章節；不直接證明現代演算法步驟。
2. **Robert Sedgewick，〈Permutation Generation Methods〉，*ACM Computing Surveys* 9(2)，1977，第 153–154 頁及參考文獻。** [作者網站 PDF](https://sedgewick.io/wp-content/themes/sedgewick/papers/1977Permutation.pdf)。支持 1812 年回溯、1960 年代相關著作及 suffix 已最大化的推導；1812 年資訊是作者的歷史回溯。
3. **Mok-Kong Shen，〈Algorithm 202: Generation of Permutations in Lexicographical Order〉，*Communications of the ACM* 6(9)，1963，第 517 頁。** [原文 DOI](https://doi.org/10.1145/367593.367604)。支持演算法題名、作者與刊載年份；本次未取得原文全文。
4. **Alexander Stepanov、Meng Lee，*The Standard Template Library*，1994 年 3 月 7 日，第 16–17 頁。** [作者保存的簡報 PDF](https://www.stepanovpapers.com/Stepanov-The_Standard_Template_Library-1994.pdf)。支持 `nextPermutation` 已是 STL 提案的泛型演算法介面。
5. **Alexander Stepanov、Meng Lee，HP STL，1995 年 10 月 31 日發行包。** [原始 `ALGO.H`](https://www.stepanovpapers.com/butler.hpl.hp/stl/stl/ALGO.H)、[作者資料集](https://www.stepanovpapers.com/)。支持目前可直接核對的早期 C++ 實作、雙向迭代器寫法與 pivot／swap／reverse 流程；檔案標示 1994 年版權，不等於這份發行包的日期。
6. **Alexander Stepanov、Meng Lee，*The Standard Template Library*，1995 年 10 月 31 日發行包文件，§10.3.9。** [原始文件 PDF](https://www.stepanovpapers.com/STL/DOC.PDF)。支持 `next_permutation` 的介面、回傳值與 wrap-around 語意；日期依 PDF 封面。
7. **Apache C++ 標準程式庫文件。** [`next_permutation` 文件](https://stdcxx.apache.org/doc/stdlibref/next-permutation.html)。支持 C++98 標準參照與函式行為，不代表 HP 版實作的來源。
8. **LeetCode，〈31. Next Permutation〉。** [原題](https://leetcode.com/problems/next-permutation/)。支持當前題意與限制；不提供可核對的首次出題日期。
