# 題目的歷史與出處 (Problem History)

每題一篇，沿著「題目情境 → 數學原型 → 關鍵觀察 → 解題方法」追溯來源，讓題目的記憶有故事，也有可查證的依據。

## 目錄

| 題目 | 歷史／數學原型 | 記憶線索 |
|---|---|---|
| [4. Median of Two Sorted Arrays](LC_0004_Median_of_Two_Sorted_Arrays.md) | 1976 年 Shamos 記載、Jefferson 私人通信；後續 selection／co-ranking 與平行合併研究 | 先固定前綴總數，再找兩個輸入各提供多少 |
| [15. 3Sum](LC_0015_3Sum.md) | 經典教材的暴力法改進；1995 年 3SUM-hard 框架與後續判定問題研究 | 固定部分選擇，再降低剩餘搜尋成本；合法性看 index、去重看 value |
| [31. Next Permutation](LC_0031_Next_Permutation.md) | 字典序排列生成；Sedgewick 回溯 1812 年文獻，1960 年代電腦演算法，1994 年 STL 提案 | 最長非遞增 suffix 已最大；最小幅度增加 pivot，再讓 suffix 最小 |
| [124. Binary Tree Maximum Path Sum](LC_0124_Binary_Tree_Maximum_Path_Sum.md) | 樹直徑與最大子陣列的相關原型；至少 2012 年已有 LeetCode 同題公開紀錄，最初來源未知 | 向上交出單支路徑，在最高點合併兩支 |
| [134. Gas Station](LC_0134_Gas_Station.md) | Gasoline Puzzle、Gasoline Lemma；相關的 Cycle Lemma | 從前綴和的最低谷出發 |
| [189. Rotate Array](LC_0189_Rotate_Array.md) | 文字編輯器的區塊搬移、三次反轉；Bentley 記載 1971 年已有使用 | 把 rotation 看成 A\|B → B\|A |
| [310. Minimum Height Trees](LC_0310_Minimum_Height_Trees.md) | Jordan 的樹中心、Harary 的剝葉證明、網路設施選址與 LeetCode 解答的術語混用 | 剝葉或取直徑中點，找最遠距離最小的 center |
| [371. Sum of Two Integers](LC_0371_Sum_of_Two_Integers.md) | CtCI 17.1 同型題；Shannon 1937 加法器、EDVAC 1945 的模數表示與 Nand to Tetris 教材；直接命題來源未確認 | XOR 交出部分和、AND 找進位；二補數讓正負數共用固定位寬加法 |
| [373. Find K Pairs with Smallest Sums](LC_0373_Find_K_Pairs_with_Smallest_Sums.md) | 磁帶外部排序、多路合併、heap 與 tournament tree；最初發明者與 LeetCode 直接來源未確認 | 每個有序來源只保留一個前端，取出誰就向誰補下一個 |
| [437. Path Sum III](LC_0437_Path_Sum_III.md) | CtCI 第六版 4.12 Paths with Sum，官方解答含雙遞迴與 prefix 頻率＋回溯；直接命題來源未確認 | 固定終點查 prefix 差，撤銷讓有效歷史只包含祖先鏈 |
| [545. Boundary of Binary Tree](LC_0545_Boundary_of_Binary_Tree.md) | EPI 收錄 Exterior 同型題；2012／2015 年公開討論；Euler Tour 為相關遍歷框架，直接命題來源未知 | 邊界身分向下傳，左邊界進入時輸出、右邊界返回時輸出 |
| [787. Cheapest Flights Within K Stops](LC_0787_Cheapest_Flights_Within_K_Stops.md) | Weekly Contest 72；Bellman 1958 的停留次數迭代、教科書邊數 DP、資源受限最短路徑與 2023 年條件下界 | 同城市的低費用與少邊數可能互不支配；先定義狀態，再選搜尋排程 |

## 檔名與組織

- 檔名使用 `LC_<四位題號>_<English_Title>.md`，例如 `LC_0134_Gas_Station.md`。題號是識別碼，不是筆記閱讀順序。
- 全部文章先放在同一層，以本頁索引連到題目；跨題目的關係用文章內的連結串接。
- 一篇聚焦一題的來源與理解線索，實作模板連到既有技巧筆記。

## 每篇固定回答的問題

1. **題目與記憶線索**：這題最值得記住的圖像或一句話是什麼？
2. **可確認的歷史**：在哪份文獻、哪一年能找到同型問題？是否確定是最早來源？
3. **背後的數學觀點**：去掉故事包裝後，真正的問題是什麼？
4. **和解題方法的關係**：這個觀點如何解釋核心操作或正確性？
5. **相關但不同的概念**：容易聯想到哪些方法？關聯的範圍到哪裡？
6. **來源與延伸閱讀**：列出作者、題名、年份、直接連結與支持的內容。

## 出處的寫法

**分清楚三種關係**：文獻確實收錄同型問題、兩者有數學關聯、已證實的直接傳承。

- 優先使用原著、作者提供的論文或出版社資料；歷史歸屬要有來源支持。
- 「某書收錄」不等於「某作者發明」；查不到最早來源，就直接保留未知。
- 數學上的等價或相似，可以用推導說明；不要把它寫成未經證實的發展歷史。
- 註明查證日期，讓後續補充或修正有依據。
