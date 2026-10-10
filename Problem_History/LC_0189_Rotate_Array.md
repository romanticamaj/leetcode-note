# 189. Rotate Array：三次反轉的歷史與理解線索

**記憶線索：把 rotation 看成 `A|B → B|A`，用反轉交換區塊，再修復區塊內部順序。**

查證日期：2026-10-09。

## 題目情境：從搬移元素到搬移區塊

LC 189 要將陣列向右旋轉 `k` 格。先令 `k %= n`，把陣列分為 `A|B`，其中 `B` 是最後 `k` 個元素，目標就是 `B|A`。

這也對應文字編輯器的需求：把一段文字行搬到另一段之前，同時保持兩段各自的行序。歷史文獻中的應用不是只為了陣列練習題。

## 可確認的歷史

### 1971 年：已有文字編輯器使用記載，發明者仍未知

Jon Bentley 在《Programming Pearls》第 2 章、第 15 頁記載：Ken Thompson 在 **1971 年**寫下編輯器與 reversal 程式，並表示這個技巧當時已屬於 **folklore**，也就是程式設計圈內流傳的技巧。[來源 1]

這是 Bentley 對早期使用情形的記述，**不能推論 Thompson 是發明者，也不能把 1971 年當作發明年份**。目前查到的來源不足以確認最初發明者。

同一段文字也提到 Kernighan 與 Plauger 將這段 reversal 程式用在文字編輯器中。這說明它曾用於實際文字處理系統。[來源 1]

### 1981 年：相鄰區塊交換的研究文獻

David Gries 與 Harlan Mills 的 Cornell 技術報告 **《Swapping Sections》**，編號 `TR 81-452`，日期為 **1981 年 1 月**，是追溯區塊交換問題的重要原始文獻。[來源 2]

Bentley 在 rotation 的解答討論中，引用這份報告研究三種 rotation 演算法。**收錄或研究演算法，不等於首次發明它**；也不要把另稱 Gries–Mills 的 block-swap 方法與三次反轉混為一談。[來源 1]

### 1983 年：Bentley 的〈Aha! Algorithms〉

Bentley 的〈Aha! Algorithms〉刊於 **1983 年 9 月**的 *Communications of the ACM*，26(9)，623–628 頁，後來收進《Programming Pearls》第 2 章。[來源 3]

書中將三次反轉放在 **The Power of Primitives（基本操作的力量）**之下，用它展示如何組合簡單操作，解決看似需要複雜搬移的問題。[來源 1]

## 🧠 數學觀點：反轉同時改變兩種順序

令 `R(X)` 表示將序列 `X` 反轉，則：

```text
R(A|B) = R(B)|R(A)
R(R(A)) = A
```

整條反轉同時做了兩件事：**交換區塊的順序，並反轉每個區塊的內部順序**。再各自反轉一次，就能保留區塊交換、恢復內部順序。

```text
A|B
→ R(B)|R(A)     整條反轉
→ B|A           兩段各自反轉
```

這是演算法的推導與正確性理由，**不是已證實的最初發明者思考歷程**。

## 和解題方法的關係

- **先整條反轉**：右轉 `k` 格時，反轉後的第一段長度為 `k`，所以切在 `k`。
- **先兩段反轉，再整條反轉**：原陣列的 `B` 長度為 `k`，所以原切點是 `n-k`。
- 正確性與奇偶長度無關；交換操作順序時，切點也要跟著改。
- 三次反轉合計時間 **O(n)**、額外空間 **O(1)**。暴力右移一格做 `k` 輪，則是 **O(kn)**；先正規化 `k` 可省去完整圈數。

## 相關但不同的概念

Rotation 也能用循環搬移（juggling）或區塊交換（block swap）完成；它們不是三次反轉的別名。這篇聚焦 reversal 的歷史與理解線索。

重做目標見 [Problem Review](../Checklists/Essential%20Problems/Problem_Review.md)：先推導 `A|B → B|A`，再決定反轉順序與切點。

## 來源與延伸閱讀

1. **Jon Bentley，《Programming Pearls》，1986，第 2 章〈Aha! Algorithms〉，尤其第 14–15 頁。** [原書掃描 PDF](https://lib.ysu.am/disciplines_bk/5e1dd92a7b2277b80658a8823c937b8c.pdf)。支持三次反轉推導、文字編輯器應用、Thompson 在 1971 年使用及 folklore 的記述；rotation 的解答部分引用 Gries–Mills 報告。頁碼指書內頁碼。
2. **David Gries、Harlan Mills，〈Swapping Sections〉，1981 年 1 月，Cornell TR 81-452。** [作者網站原始 PDF](https://www.cs.cornell.edu/gries/TechReports/81-452.pdf)、[Cornell 館藏紀錄](https://ecommons.cornell.edu/entities/publication/ecd46103-0bf9-4859-a196-a0666d3927f8)。支持作者、報告名稱與日期。
3. **Jon Bentley，〈Programming Pearls: Aha! Algorithms〉，1983。** [ACM DOI](https://doi.org/10.1145/358172.358176)、[期刊卷期目錄](https://www.sigmod.org/publications/dblp/db/journals/cacm/cacm26.html)。支持專欄出版時間與頁碼。
