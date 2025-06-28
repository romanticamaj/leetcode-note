# 解題前的確認與與考官溝通心法

在進入實作前，與考官進行有效的溝通不僅能釐清問題，也能展現你的工程思維與團隊合作能力。以下是一些常見的確認點與建議的溝通方式：

---

## ✅ 資料是否可以修改？（In-place vs. Copy）

> You should always discuss the possibility of overwriting the input with your interviewer and clarify what kind of environment your algorithm is expected to run in. Sometimes they won't care, sometimes they'll state it has to run in a multithreaded environment, or sometimes they'll have a particular preference as it impacts what they're trying to see from you.

### 建議提問方式

- 「這題我可以直接修改 input 嗎？還是需要保留原始資料？」
- 「這題會在 multi-threaded 環境下執行嗎？我需要考慮 thread safety 嗎？」

---

## ✅ 輸入資料的範圍與邊界條件

- 「這個 array 最多會有幾個元素？」
- 「有可能是空的嗎？有負數嗎？」
- 「有沒有重複值？是否保證排序？」

---

## ✅ 回傳格式與要求

- 「我需要回傳 index 還是值？」
- 「如果找不到解，應該回傳什麼？」
- 「可以回傳任意一組解嗎？還是要最小字典序？」

---

## ✅ 時間與空間限制

- 「這題有沒有特別要求時間或空間複雜度？」
- 「我可以用額外的資料結構嗎？」

---

## ✅ 多解情況與唯一性

- 「這題會有多組解嗎？還是保證唯一？」
- 「如果有多組解，我需要全部找出來嗎？」

---

## ✅ 額外假設與簡化條件

- 「我可以假設輸入都是合法的嗎？」
- 「我可以先不考慮 overflow 嗎？」

---

## ✅ 題目是否可以轉換為熟悉的模型？

- 「這題看起來像是 graph traversal，我可以用 BFS/DFS 解嗎？」
- 「這題可以轉換成 two pointer 或 sliding window 嗎？」

---

## ✅ 題目是否有 follow-up？

- 「這題有後續 follow-up 嗎？我可以先用簡單版本解，再優化嗎？」

---

## ✅ 願意 verbalize 思路

- 「我可以先講一下我的想法，再開始寫嗎？」
- 「我會先用 brute-force 解法，然後再優化成 O(n log n)」

---

這些確認不僅能幫助你釐清題意，也能讓考官看到你在意邊界、效能與可維護性，是非常加分的行為。