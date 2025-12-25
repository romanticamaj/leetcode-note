# Boundary-Driven Processing 心法（邊界驅動處理）

## 🧠 核心哲學

當處理**連續相同元素的區段**（如 run-length encoding、連續字元計數）時，採用「先找邊界，再處理」的策略。

核心洞察：**外層迴圈在「segment」層級迭代，而非「element」層級**。

| 思維           | 特徵                             | 問題                             |
| -------------- | -------------------------------- | -------------------------------- |
| **逐元素處理** | 每次 iteration 處理一個元素      | 需要額外狀態追蹤「當前 segment」 |
| **邊界驅動**   | 內層找邊界，外層處理完整 segment | 清晰、狀態自然封裝               |

---

## 核心概念

### 1️⃣ 雙層迴圈的職責分離

```
外層 while (i < n)     → 控制 segment 的迭代
內層 while (boundary)  → 找當前 segment 的邊界，推進 i
```

這與普通迴圈的關鍵差異：**內層迴圈負責推進 `i`**。

### 2️⃣ 處理時機：邊界確定後

內層迴圈結束時，我們擁有：

- `segment_value`：segment 的值（如字元）
- `count`：segment 的長度
- `i` 指向 segment 的最後一個元素

**所有處理邏輯都在邊界確定後執行**，不需要在過程中維護狀態。

### 3️⃣ 指針語義

```
i：當前處理位置（讀取指針）
k：寫入位置（若需要 in-place 修改）
```

In-place 修改時，讀寫指針分離是關鍵。

---

## 🧩 核心結構

```
while (i < n) {
    // Phase 1: Boundary Detection
    int count = 1;
    while (i + 1 < n && same_segment(i, i+1)) {
        i++;
        count++;
    }

    // Phase 2: Segment Processing
    // 此時 i 指向 segment 最後一個元素
    process(segment_value, count);

    i++;  // 移動到下一 segment 起始
}
```

---

## ⚠️ 與普通迭代的區別

**普通 for 迴圈**：

```cpp
for (int i = 0; i < n; i++) {
    // 外層控制 i 推進
    // 每次處理一個元素
}
```

**Boundary-Driven**：

```cpp
while (i < n) {
    while (boundary) { i++; count++; }  // 內層推進 i
    process(segment);
    i++;
}
```

**核心差異**：在 Boundary-Driven 模式中，**內層迴圈負責推進 `i`**，外層迴圈實際上是在「segment」層級迭代。

---

## ⚠️ 與 Sequential Phase Consumption 的區別

| 特徵     | Sequential Phase            | Boundary-Driven                 |
| -------- | --------------------------- | ------------------------------- |
| 結構     | Phase 1 → 2 → 3（執行一次） | Segment 1 → 2 → ... → N（重複） |
| 內層迴圈 | 消費當前 phase 的所有元素   | 尋找 segment 邊界               |
| 控制流   | Fall-through 到下一 phase   | 回到外層處理下一 segment        |
| 適用問題 | Parsing（atoi, version）    | 連續區間處理（壓縮、計數）      |

Sequential Phase 處理的是**不同類型的 token 序列**（spaces → sign → digits），每個 phase 只執行一次。

Boundary-Driven 處理的是**重複性的相同結構**，外層迴圈會執行多次。

---

## 📚 適用場景

- **LC 443. String Compression** - Run-length encoding
- **LC 38. Count and Say** - Look-and-say sequence
- **LC 830. Positions of Large Groups** - 找大群組位置
- **LC 1446. Consecutive Characters** - 最長連續字元
- **LC 1869. Longer Contiguous Segments of Ones than Zeros**
- **LC 228. Summary Ranges** - 連續區間合併

---

## ✅ 設計要點

- [ ] 內層邊界條件：`i + 1 < n && arr[i + 1] == arr[i]`（先檢查邊界）
- [ ] 外層結束時 `i++` 移動到下一 segment 起始
- [ ] Segment 處理在邊界確定後執行
- [ ] In-place 修改時：讀指針 `i` 與寫指針 `k` 分離
- [ ] 注意 `i` 在內層迴圈結束時指向 segment 的**最後一個元素**
