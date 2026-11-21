# 224. Basic Calculator：表達式解析、Shunting Yard 與遞迴求值

**記憶線索：括號定義子問題；先保存尚未完成的運算，再決定何時求值。**

Technique summary：`Recursive Descent Parsing + Direct Evaluation + Shared Cursor`

來源查證與整理日期：2026-11-21。本文記錄本次實際查閱的作者網站、官方教材程式、課程講義與歷史文獻紀錄；不是對所有版次原書的逐頁核對。

## 1. 題目與歷史定位

[LC 224 官方題面](https://leetcode.com/problems/basic-calculator/)要求求出合法算式字串的值，涉及整數、加減、括號、空白與 unary minus，不能使用直接求值的內建函式。

它屬於經典的 **expression parsing／evaluation**：不只辨認字元，還要根據結合性、優先級與括號決定運算結構。字串讀取是輸入處理；保存尚未完成的計算、定義子表達式的返回契約，才是設計核心。

**經典教材確實收錄同類問題，但目前沒有證據確認 LC 224 直接改編自哪本書。** 本次也未確認官方首次發布日期或原始出題者；下列歷史證據不代表某位作者首創所有表達式解析方法。

## 2. 早期歷史：ALGOL 表達式翻譯

E. W. Dijkstra 的 **ALGOL 60 Translation（1961）** 是早期相關文獻：它處理 ALGOL 翻譯，包含算術表達式轉換的背景。[CWI 原始文獻紀錄](https://ir.cwi.nl/pub/9251)、[UT Austin 保存的原始報告 MR35](https://www.cs.utexas.edu/~EWD/MCReps/MR35.PDF)

這支持「表達式轉換是早期編譯器的實際問題，遠早於 LeetCode」。本次取得原報告掃描，但沒有完成全文逐頁辨讀，因此不指定其中某頁為本次遞迴版本的直接來源。

本次使用者提供的 [Shunting-yard algorithm 百科條目](https://en.wikipedia.org/wiki/Shunting_yard_algorithm)將該演算法歸於 Dijkstra，並記載首次發表於 1961 年 11 月。**精確月份在此保留為二手資料的說法，不當成已獨立核對的原始文獻結論。**

## 3. 經典教材中的計算機

| 教材／章節 | 本次確認的內容 | 與 LC 224 的差異 |
|---|---|---|
| Bjarne Stroustrup，The C++ Programming Language，第三版 §6.1 A Desk Calculator | 作者網站列出原書 107–117 頁的 desk calculator 程式；第四版目錄也保留 §10.2 A Desk Calculator | 是較完整的計算機教材，不宣稱為 LC 224 題面或特定實作的直接來源 |
| Robert Sedgewick、Kevin Wayne，Algorithms，第四版 §1.3 Stacks and Queues | 官方 Evaluate.java 展示 Dijkstra 雙 stack 求值；教材頁另列 shunting yard 轉 postfix 的練習 | Evaluate.java 要求完整括號化且 tokens 以空白分隔，不可直接當作 LC 224 完整解法 |
| Aho、Lam、Sethi、Ullman，Compilers: Principles, Techniques, and Tools，第二版 §2.5 A Translator for Simple Expressions | NYU 對應課程講義說明加減算式的 infix → postfix、文法改寫與遞迴下降轉譯 | 最初簡化文法只含單位數與 binary 加減，不是含全部 LC 邊界的 codec |
| Robert Nystrom，Crafting Interpreters，第 6 章 Parsing Expressions | 作者原始章節將文法轉為 recursive-descent 函式，處理優先級、unary operator 與括號 | 書中 parser 建立語法樹；本次實作直接回傳數值，不建立 AST |

## 4. 三條路線：同一問題，不同保存方式

```text
算式字串
   ├─ Shunting yard → postfix → 求值
   ├─ Parser → AST → 求值
   └─ Recursive descent → 解析時直接求值（本次版本）
```

### Shunting yard：決定 operator 何時可以輸出

本次最初提出的「先轉 postfix，再 evaluate」正是這條經典路線。

**核心：數值直接輸出；尚不能決定位置的 operator 暫存在 stack，依優先級、結合性與括號再輸出。**

```text
Infix：   1 - (2 + 3)
Postfix： 1 2 3 + -
```

- 遇新 operator，先輸出 stack 中優先級更高的 operator；同優先級且新 operator 左結合時，也先輸出舊的。
- `(` 是邊界；遇 `)` 時輸出到對應 `(`，並移除該括號。
- 每個 token 只進出 stack 常數次，因此轉換為 O(n) 時間、最壞 O(n) 空間。
- Unary minus 必須另外辨識並定義處理方式，不能把每個 `-` 都當 binary subtraction。

官方教材明確列出 shunting yard 轉 postfix 的練習，支持兩者的直接技術關聯。[Algorithms §1.3](https://algs4.cs.princeton.edu/13stacks/)

### 雙 stack 直接求值：保存 operands 與 operators

《Algorithms》的 Evaluate.java 分別保存數值與 operator，遇到右括號就取出 operator 和所需 operands，算完再放回數值 stack。

它展示「運算尚未完成時要保存什麼」，但不是所有 stack 計算機都可一概稱為 shunting yard；應看是否實作相應的優先級與輸出／歸約規則。[官方程式與輸入限制](https://algs4.cs.princeton.edu/13stacks/Evaluate.java.html)

### 本次遞迴版本：每層保存自己的計算狀態

**核心：括號裡的式子可回傳一個值，外層將它視為普通 operand。** 同層只有左結合、同優先級的加減，因此取得完整 operand 後就能更新累積結果。

| 狀態 | 意義 |
|---|---|
| `value`，初值 0 | 此層已完成部分的累積結果 |
| `operation`，初值 +1 | 下一個完整 operand 要套用的符號 |
| 共用 `index` | 下一個尚未處理的字元位置 |

只列實作關鍵行，不提供完整解法：

```cpp
// 每次公開入口重設；遞迴 helper 以 const string& 讀取相同輸入
index = 0;
// 取得數字或括號子問題的完整值後，統一處理
value += operation * operand;
// 讀到符號只更新，不立即求值
operation = s[index] == '+' ? 1 : -1;
```

本次位置契約：遇 `(` 先前進再遞迴；內層消耗 `)` 後回傳，外層不再重複前進。每個 call frame 自動保留外層的 `value` 與 `operation`。

Leading minus 可用 `0 - operand` 理解；這利用題目的語法限制，不代表對任意 unary／binary 混合文法，只更新一個符號就一定足夠。若加入乘除，也不能把 `1+2*3` 讀到 2 時直接定案為 3。

這是 recursive descent 的直接求值形式；**沒有產生 postfix，也沒有實作 shunting-yard operator stack 規則，因此不應把本次程式命名為 shunting yard。**

## 5. 這次最值得帶走的設計

- 先問「下一個 operand 來時需要什麼資訊」，再選資料結構；加減可由累積結果與下一個符號承接。
- 遞迴不是沒有 stack，而是用 call stack 保存尚未完成的外層計算。
- 判斷求值時機：**取得完整 operand 時計算；讀到 operator 時記住符號。**
- `substr(start, end-start)` 的第二參數是長度；讀完整段數字後，index 已指向下一個未處理字元。
- 遞迴輸入以 reference 傳遞，避免每層複製整個字串；共用 index 在公開入口重設。

可對照既有 [遞迴函式契約](../Algorithms/Design_Principles/Recursion/05-Recursion_Signature_Contract.md)。

## 6. 參考資料與查證範圍

1. **Dijkstra，ALGOL 60 Translation，1961。** [CWI 紀錄](https://ir.cwi.nl/pub/9251)、[原報告掃描](https://www.cs.utexas.edu/~EWD/MCReps/MR35.PDF)。歷史背景；未據此指定 LC 出處或遞迴版本發明者。
2. **Stroustrup，The C++ Programming Language。** [第三版官方程式索引](https://stroustrup.com/3rd_code.html)、[第三版目錄](https://www.stroustrup.com/3rd_long_tbl.html)、[第四版目錄](https://stroustrup.com/4thContents.html)。確認 Desk Calculator 的章節與範例存在；作者索引的程式連結為 dc.c，本次瀏覽工具未能解析該原始碼內容。
3. **Sedgewick／Wayne，Algorithms，第四版 §1.3。** [教材頁](https://algs4.cs.princeton.edu/13stacks/)、[Evaluate.java](https://algs4.cs.princeton.edu/13stacks/Evaluate.java.html)。支持雙 stack 求值、輸入限制與 shunting yard 練習；教材頁有時回傳 403，本次亦核對搜尋取得的頁面內容。
4. **NYU，Compilers Lecture #3，對應 Dragon Book §2.5。** [講義](https://cs.nyu.edu/~gottlieb/courses/compilers/lectures/lecture-03.html)。支持簡單加減式、infix／postfix 與遞迴下降轉譯的教材脈絡。
5. **Nystrom，Crafting Interpreters，第 6 章。** [作者原始章節](https://github.com/munificent/craftinginterpreters/blob/master/book/parsing-expressions.md)。支持 recursive descent、函式與文法規則的對應、括號、unary operator 與 call stack；與直接求值的比較為本文推導。
6. **Wikipedia，Shunting yard algorithm。** [使用者提供的頁面](https://en.wikipedia.org/wiki/Shunting_yard_algorithm)。作為問題線索及規則總覽；精確首次發表月份保留二手歸屬，非獨立確認。
