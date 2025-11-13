# 解題 Follow-up 待辦清單

這個文件用來記錄在解題過程中遇到的各種 follow-up 問題、待優化項目、或下次需要深入練習的技巧。

---

## 🌳 樹 (Trees)

- [ ] **比較**：比較 Morris Traversal 與標準遞迴/迭代 traversal 的優缺點。
- [ ] **學習**：研究 Min-Max Heap 和 Deap (Double-ended heap) 資料結構，了解其如何同時高效支援查找最小和最大元素。

---

## 📈 圖 (Graphs)

- [ ] **研究**：研究 A\* 搜尋演算法，並比較它與 Dijkstra、BFS 的差異。

---

## 🔢 陣列與字串 (Arrays and Strings)

- [ ] **學習**：研究 Quickselect（Hoare 選擇演算法），它能在平均 O(n) 時間內找到無序列表中的第 k 小元素。

---

## 💡 動態規劃 (Dynamic Programming)

- [ ] **研究**：研究矩陣快速冪 (Matrix Exponentiation) 如何將線性遞迴的 DP 問題從 O(N) 優化到 O(logN)，以 Fibonacci 數為例。

---

## 🧮 數學 (Math)

- [ ] **複習**：複習 Catalan Number 的定義、遞迴關係、以及經典應用 (如括號匹配、唯一二元搜尋樹)。

---

## 🔄 回溯 (Backtracking)

- [ ] **重新建立與討論**：重新建立一份關於回溯演算法複雜度分析的完整文件。

---

## 🔑 雜湊表 (Hash Tables)

- [ ] **研究**：研究 hash function 的時間複雜度計算
- [ ] **學習**：深入理解 hash function 的設計原則與實作
- [ ] **研究 (collision handling)**：研究並比較不同的碰撞處理策略：
  - [Separate Chaining](https://en.wikipedia.org/wiki/Hash_table#Separate_chaining): for values with the same hash key, we keep them in a *bucket*, and each bucket is independent of each other.
  - [Open Addressing](https://en.wikipedia.org/wiki/Hash_table#Open_addressing): whenever there is a collision, we keep on *probing* on the main space with certain strategy until a free slot is found.
  - [2-Choice Hashing](https://en.wikipedia.org/wiki/2-choice_hashing): we use two hash functions rather than one, and we pick the generated address with fewer collision.
- [ ] **實作目標**：完成 **[705. Design HashSet](https://leetcode.com/problems/design-hashset/)** 的實作

---

## ⚙️ 其他

- [ ] **比較**: 在貪婪演算法的脈絡下，深入比較 Bucket Sort 與傳統比較排序 (如 `std::sort`) 和堆 (Heap) 的使用時機與複雜度。

- [ ] **研究 (Bucket Sort)**:
  - 如何根據資料分佈選擇最佳的 bucket 數量？
  - 如何高效地建構 bucket 列表？例如 `vector<vector<int>> bucket(k);` 的適用時機與限制。