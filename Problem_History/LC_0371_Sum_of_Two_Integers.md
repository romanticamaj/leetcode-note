# 371. Sum of Two Integers：加法器、二補數與位元加法的歷史

**記憶線索：XOR 交出不含進位的和，AND 找出進位；二補數讓正負數共用同一套固定位寬加法。**

查證日期：2026-11-03。依本次查閱的原始論文、官方教材與程式庫整理；實作見既有的 [位元加法筆記](../Algorithms/Bit_Manipulation/99-Case_Bitwise_Addition.md)。

## 1. 題目與出處：同型面試題存在，直接傳承未確認

[LeetCode 371 官方題面](https://leetcode.com/problems/sum-of-two-integers/) 要求不使用 `+`、`-` 計算兩整數之和。其概念根源是數位電路的二進位加法器，以及二補數的模數表示。

可直接確認的同型面試題，是 Gayle Laakmann McDowell 的 **Cracking the Coding Interview，第六版，17.1 Add Without Plus**。CareerCup 官方 repo 說明 Java 解答與書中相同；該題的 QuestionA 為遞迴版、QuestionB 為迭代版，兩者都使用 XOR／AND／左移分解加法。

- [官方 repo 與 Java 解答來源說明](https://github.com/careercup/CtCI-6th-Edition)
- [17.1 QuestionA：遞迴](https://github.com/careercup/CtCI-6th-Edition/blob/master/Java/Ch%2017.%20Hard/Q17_01_Add_Without_Plus/QuestionA.java)
- [17.1 QuestionB：迭代](https://github.com/careercup/CtCI-6th-Edition/blob/master/Java/Ch%2017.%20Hard/Q17_01_Add_Without_Plus/QuestionB.java)

**「書中收錄同型題」不等於「LeetCode 改編自該書」。** 本次未確認 LC 371 的直接命題來源、首次發布日期或競賽歸屬，也未確認這個 XOR／carry 迴圈的最初發明者。

## 2. 1937 年：Shannon 的二進位加法器

Claude Shannon 的 **A Symbolic Analysis of Relay and Switching Circuits** 論文，簽署日期為 1937-08-10；1938 年另有同名期刊文章。此處引用的是論文掃描版，其封面亦標示學位年份 1940，須區分研究、發表與學位時間。

正文第 **59 頁起**有一節：

> “Electric Adder to the Base Two”

這一節用繼電器與開關設計自動加起兩個二進位數字的電路，分別表示兩個輸入的各位、結果各位，以及由低位傳入的 carry，再推導輸出與進位的關係。[論文第 59 頁起，PDF 第 62 頁](https://fab.cba.mit.edu/classes/862.19/notes/computation/Shannon-1937.pdf#page=62)

這能確認早期電腦設計已有「用邏輯元件構造二進位加法」的實例；**不能因此宣稱 Shannon 發明了 LC 371 的程式迴圈，也不能將此文獻當作加法器的絕對最早來源。**

## 3. Full adder 的思路沒有錯：只是加法的組織方式不同

Nisan、Schocken 的 **The Elements of Computing Systems**（Nand to Tetris），第 2 章 **Boolean Arithmetic**，使用以下學習路線：

```text
HalfAdder → FullAdder → 多位元 Adder → ALU
```

該章 §2.3 明確指出 half adder 的 sum 與 carry 分別對應 XOR、AND；full adder 則額外接收低位傳入的 carry。[官方教材，第 2 章](https://www.nand2tetris.org/_files/ugd/44046b_89c60703ebfc4bf39acef13bdc050f5d.pdf#page=10)、[官方 Project 2](https://www.nand2tetris.org/project02)

以下是本次解題關係的推導，不是歷史作者發明過程的還原：

| 方式 | 輸入與進位的處理 |
|---|---|
| 單位元 half adder | 兩個 bits 得到 sum 與 carry，沒有 carry-in |
| 單位元 full adder | 兩個 bits 加上 carry-in，得到 sum 與 carry-out |
| 逐位加法 | 從低位向高位處理，每位接收前一位的 carry |
| XOR／carry 迴圈 | 整個 word 同時產生不含進位的部分和、進位，再把兩者作為下一輪輸入 |

所以最初列出 `(x,y,carry)` 真值表、推導 full adder，**方向成立**。後來學到的簡化，是利用整組 bitwise operations，不必逐位取出；不是 full adder 邏輯被推翻。

也不能由此聲稱現代 CPU 執行相同 while 迴圈來完成加法；硬體電路設計與軟體排程是不同層次。

## 4. 1945 年：EDVAC 報告解釋為何負數共用加法

John von Neumann 的 **First Draft of a Report on the EDVAC**，日期為 **1945-06-30**。在 **§8.1，正文第 15 頁**，已用模數關係解釋有符號數的表示與加減法；下一節 §8.2 說明如何以取反再加一，把減法交給加法器。[原文，PDF 第 23 頁](https://www.cs.sjsu.edu/~mak/archive/CS185C/EDVAC.pdf#page=23)

本次讀的是 Michael D. Godfrey 校訂、重排的版本；文首交代其與原始打字稿及 1993 年刊載版本的關係，不能把 PDF 的重排年代誤當成原報告年代。

用現代整數記號解釋：w-bit 二補數把負數 `-x` 編碼成 `2^w-x`。編碼與原整數只差 `2^w` 的倍數，加法後保留低 w bits，即保留相同的模數結果。

```text
4-bit：-3 的編碼為 13，即 1101
-3 + 5 → 編碼相加 13 + 5 = 18 → 只留低 4 bits：0010 → 2
3 + (-5) → 編碼相加 3 + 11 = 14 → 1110 → signed 解讀為 -2
```

**sign bit 不是另外貼上的負號；二補數最高位的數值權重是 -2^(w-1)。** 正負數能共用位元加法，是此編碼的重要優點。若數學答案超出 signed 範圍，只能保證模數結果，不能稱為原整數的精確和。

Nand to Tetris 第 2 章正文第 31–32 頁，也以二補數負數相加說明不需增加專門處理符號的加法硬體。[教材的 signed binary numbers 小節](https://www.nand2tetris.org/_files/ugd/44046b_89c60703ebfc4bf39acef13bdc050f5d.pdf#page=3)

## 5. 對應程式的正確性與界線

```text
newSum   = a XOR b
newCarry = (a AND b) << 1
```

每輪只是重新分解待加的兩個數；**a+b 在模 2^w 下保持不變**。carry 的最低有效位每輪至少左移一位，至多 w 輪後消失；當 carry 為 0，另一個值就是結果。時間 O(w)、額外空間 O(1)，固定 32-bit 可視為常數時間。

- 數學模型依賴固定位寬；任意精度整數語言處理負數時，不能不加限制地照搬。
- C++ 的 signed 左移與整數轉換規則須區分版本。二補數的演算法推理不會消除語言層面的 UB；unsigned 中間值的用途與版本表見 [Bit Shift UB 地雷](../Algorithms/Bit_Manipulation/99-Case_Shift_UB_Pitfall.md)。
- 實作與 `-1+1` 的逐輪追蹤見 [位元加法](../Algorithms/Bit_Manipulation/99-Case_Bitwise_Addition.md)，本篇不重複建立另一份模板。

## ✅ 閱讀順序與驗收問題

建議：先讀 Nand to Tetris 第 2 章的 half／full adder → EDVAC §8.1 → CtCI 17.1 迴圈 → 最後回看 C++ 型別規則。

- [ ] 為什麼 XOR 是不含進位的和、AND 是產生進位的位置？
- [ ] 逐位 full adder 與整組 XOR／carry 迴圈，如何處理同一個加法問題？
- [ ] 為什麼二補數負數不需另外處理 sign bit？為什麼捨棄超出位寬的進位合理？
- [ ] 為什麼終止條件是 carry 為 0，且最多 w 輪？
- [ ] 如何區分同型題收錄、數學關係與尚未證實的直接歷史傳承？
