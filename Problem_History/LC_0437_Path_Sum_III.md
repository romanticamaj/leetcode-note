# 437. Path Sum III：Paths with Sum 與祖先路徑的 Prefix Sum

**記憶線索：prefix sum 把路徑和轉成差值查詢；backtracking 讓有效歷史只包含目前祖先鏈。**

查證日期：2026-11-03。依本次查閱的官方題面、作者公告與 CareerCup 官方 Java 解答整理。

## 1. 可確認的教材出處

[LeetCode 437 官方題面](https://leetcode.com/problems/path-sum-iii/) 計算和為 target 的向下路徑數；起點與終點不限定 root／leaf，但方向只能由 parent 到 child。

Gayle Laakmann McDowell 的 **Cracking the Coding Interview，第六版，4.12 Paths with Sum** 收錄同型問題。作者於 2015 年公告第六版準備出版；官方 CareerCup repo 說明其中 Java 解答與書中相同。

- [作者第六版公告，2015-05-31](https://www.gayle.com/blog/2015/5/31/its-coming-at-last-cracking-the-coding-interview-6th-edition)
- [官方解答庫與來源說明](https://github.com/careercup/CtCI-6th-Edition)

**可確認「教材收錄同型題與解法」，未確認「LeetCode 直接改編自該書」。** 本次也未確認 LC 437 的首次發布日期、競賽歸屬、最初出題者，或這個技巧的首次發表文獻；不把第六版年代當作問題發明年代。

## 2. 官方兩份解答，對應本次的推導路線

| 官方版本 | 方法 | 本次練習的對應 |
|---|---|---|
| [QuestionA](https://github.com/careercup/CtCI-6th-Edition/blob/master/Java/Ch%2004.%20Trees%20and%20Graphs/Q4_12_Paths_with_Sum/QuestionA.java) | 外層枚舉起點，內層搜尋該起點向下的所有路徑 | 先完成的雙遞迴版本；教材累加 currentSum，本次遞減 remaining |
| [QuestionB](https://github.com/careercup/CtCI-6th-Edition/blob/master/Java/Ch%2004.%20Trees%20and%20Graphs/Q4_12_Paths_with_Sum/QuestionB.java) | running sum＋prefix 頻率表，遞迴後撤銷目前 prefix | 後續經提示完成的 preorder＋prefix sum＋backtracking 版本 |

兩份原始碼均已實際查閱。以下對照是演算法的關係，不是對歷史作者發明過程的還原。

**優化關鍵：從「固定起點，枚舉終點」改成「固定終點，一次查詢所有合法起點」。** 樹中起終點確定後路徑唯一，但同一終點仍可對應多個起點，故需要 frequency，不能只記是否存在。

## 3. 數學觀點：陣列的 prefix 差，放進祖先鏈

令 S 是 root 到目前節點的 running sum，P 是某個起點之前的 prefix：

```text
S - P = target
P = S - target
```

查詢 `freq[S-target]`，就得到以目前節點為終點的合法路徑數。這與 LC 560 的陣列 prefix sum 有相同差值關係，但有效歷史的範圍不同：

| 陣列掃描 | 樹的 DFS |
|---|---|
| 先前位置皆可作為前綴 | 只有目前祖先鏈的前綴有效 |
| 歷史通常持續保留 | 完成分支後必須撤銷 |
| 重複 prefix 代表不同起點 | 同樣需要計數；例如 0→0、target=0，第二個節點有兩條路徑結束於此 |

查詢前，頻率表須精確代表 root 前空前綴與目前節點的嚴格祖先。更新 running sum 後，**先查詢、再加入目前 prefix**，避免 target=0 時把目前 prefix 減掉自己，算入空路徑。左右子樹完成後撤銷，避免兄弟分支互相影響。

既有概念筆記：[Running State／歷史狀態查詢](../Algorithms/Prefix_Sum/02_Running_State_Pattern.md)。

## 4. 原書與本次版本的差異

- **Root 起始路徑**：官方 QuestionB 使用空 map，另外判斷 `runningSum == targetSum`；本次以 `freq[0]=1` 代表 root 前的空前綴。兩者等價，不能同時使用，否則重複計數。
- **數值型別**：官方 Java 範例用 int；LC 437 現行條件最多 1,000 個節點、節點值可達 ±10^9，本次用 long long 保存 running sum 與 map key 才足夠，不能照搬教材型別。[官方限制](https://leetcode.com/problems/path-sum-iii/)
- **撤銷與空間**：官方 helper 在次數歸零時移除 key。本次 C++ 的 `map[key]` 查詢會插入不存在的 key，`--` 後也保留零次數 key；邏輯上有效歷史仍正確，實體 map 卻可能累積 O(n) 個項目。

## 5. 複雜度與驗收

雙遞迴的工作量是所有子樹大小之和，即 `Θ(n + Σ depth(v))`：平衡樹 Θ(n log n)，鏈狀樹 Θ(n²)，stack O(h)。

prefix 頻率版每個節點只做固定次數的 hash 操作，**平均時間 O(n)**；hash 碰撞下最壞可能 O(n²)。一般樹的遞迴關係是 `T(n)=T(leftSize)+T(rightSize)+平均 O(1)`，`2T(n/2)` 只適用於平衡切分。

本次保留零次數與查詢插入 key 的版本，空間為 `O(U+h)=O(n)`，U 是實際保留的 key 數，不是數值範圍。若查詢使用 find、避免插入，且撤銷至 0 時 erase，map 加上 stack 才可界為 O(h)。

## ✅ 閱讀後應能回答

- [ ] 雙遞迴為何重掃？如何將起點枚舉改成終點查詢？
- [ ] 路徑唯一為何仍需要 prefix 的出現次數？
- [ ] map 的有效歷史是哪些節點？為何必須在離開子樹時撤銷？
- [ ] 先查再加入、空前綴初始化，各防止或涵蓋哪種情況？
- [ ] 邏輯上只有祖先 prefix，為什麼實體 map 仍可能占 O(n) 空間？
- [ ] 教材收錄同型題，與已證實的直接命題來源，有何不同？
