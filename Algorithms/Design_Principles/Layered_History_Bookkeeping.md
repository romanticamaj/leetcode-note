# 狀態轉換與歷史保留（State Transitions + History Retention）解題心法

**難度：⭐⭐⭐｜核心設計：State Representation + Transition Rules + Retained History。**

設計演算法時，不只要問「下一個狀態怎麼算」，還要問：**狀態改變後，未來還需要哪些過去資訊？**
保存這些資訊，可以避免重算、重建答案，或在移除目前候選後找回先前候選。Stack 只是其中一種保存方式。
本文綜合既有概念整理設計流程，最後用 LC 895 示範；這個框架是本文的整理，不是單一標準演算法名稱。

## 1. 🧠 從狀態轉換切入

把資料結構的完整內部狀態記為 S，操作記為 op：

```text
S_next = transition(S, op)

設計 S 時，同時決定：
目前需要的摘要 + 未來仍會使用的資訊
```

例如「某個值目前出現 3 次」是摘要，但無法告訴我們移除一次後，同頻候選之間的先後順序。
**足以回答現在，不一定足以支援下一次操作。** 若覆寫會丟失未來需要的資訊，就必須先保存它，或設計可重建的方法。

這不表示所有操作都必須可逆。一般狀態轉換可能丟失資訊；只有需求包含恢復時，才需要保留足夠的恢復依據。

## 2. 歷史的用途，決定保留什麼

| 未來要做什麼？ | 保留的資訊 | 典型設計 |
|:---|:---|:---|
| 重用已算過的結果 | 子問題的答案 | DP table／memoization |
| 重建答案的選擇過程 | 到達答案的決策或前驅 | DP parent pointers／BFS predecessor |
| 比較現在與過去 | 過去的累計摘要、出現位置或次數 | Prefix sum／prefix frequency map |
| 偵測狀態重複 | 完整狀態的識別與出現時間 | Cycle detection + fast forwarding |
| 移除候選後找回下一個 | 尚未消耗的候選及其順序 | Frequency-indexed stacks，例如 895 |
| 撤回變更 | 足以恢復的舊值或反向操作資訊 | Backtracking／rollback log |

**共通的是「為未來保留資訊」，不是所有方法都在 undo。** DP 重用子問題答案；parent pointers 重建選擇；rollback 才是在恢復先前狀態。
MIT 6.006 的 DP 講義同時討論 memoization，以及額外保存 parent pointers 來重建答案，清楚區分「答案值」與「如何得到答案」。[Lecture 20，第 1、4–5 頁](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/9f38f5c9ff4172f8b58be390c89b61d2_MIT6_006F11_lec20.pdf)

## 3. 🧩 四步設計：需求 → 資訊 → 組織 → 生命週期

| 步驟 | 必須回答的問題 |
|:---|:---|
| **1. 定義未來操作** | 要查答案、重建路徑、移除候選，還是撤回更新？ |
| **2. 找出不能丟的資訊** | 只有目前摘要夠嗎？是否需要舊值、順序、決策或出現時間？ |
| **3. 按存取規則組織** | 用狀態作 key？用位置索引？最近優先？先選優先層再選層內順序？ |
| **4. 證明何時能刪除** | 已消耗、離開有效範圍，還是已無未來依賴？ |

先寫清楚紀錄的意義，再選容器。需要按狀態查詢才用 map，需要最近優先才用 stack；history 本身不指定資料結構。

**刪除條件尤其重要**：rolling-array DP 可覆寫已無未來依賴的值；backtracking 要在離開分支時撤銷局部修改；895 的低層紀錄則要保留，因為之後還可能成為候選。
暫時不是答案，不代表永遠不會再用到。

## 4. 範例：895 的推進與恢復

FreqStack 的 push 加入一個值；pop 移除最高頻率的值，同頻時選最近加入的那一次。保證非空時才 pop。
技巧摘要：**Hash Map Frequency Counting + Frequency-Indexed Stacks**。

| 資料 | 保存什麼？ |
|:---|:---|
| `counter[val]` | val 目前尚未移除的出現次數 |
| `store[f]` | 尚未消耗的「第 f 次達標」紀錄，依達標時間排列 |
| `maxFreq` | 目前最高頻率，決定從哪層取候選 |

```text
push(5), push(7), push(5)

目前頻率：5 → 2，7 → 1
第 2 層：[5]       ← 最近一次 push(5) 新增這筆
第 1 層：[5, 7]    ← 先前的紀錄仍然保留

pop() 取出第 2 層的 5：5 的頻率回到 1
第 1 層原本就在，因此下一次自然取 7，再取 5
```

**push 推進頻率，並新增一筆紀錄；pop 消耗最高層紀錄，讓較低層的舊候選重新可用。**
不用重新搜尋前一次出現，也不用降頻時把值搬回低層。

這裡的「恢復」是恢復某個值較低頻率時的候選資格，**不保證回到全域某個舊版本**。例如 push(5)、push(5)、push(7) 後，pop 取的是 5，並不是撤回最後一次 push(7)。

### Invariant：為什麼舊紀錄仍然正確？

1. 每個目前頻率為 c 的值，在第 1..c 層各有一筆未消耗紀錄；push 新增第 c+1 層，pop 消耗第 c 層。
2. 每層依達標時間排列，尾端就是該層最近的候選。最高層的尾端因此同時滿足頻率與先後規則。
3. 到達 f 必經 f-1，低層紀錄又未被消耗。因此最高層空掉後，f>1 時下一層必非空；f=1 時退到 0。

`store[f]` **不是目前頻率恰好等於 f 的值集合**。若升頻時刪掉低層紀錄，就丟失了未來需要的資訊；降頻時再新增，又會重複記帳。

## 5. C++：讓結構承載轉換規則

```cpp
#include <algorithm>
#include <unordered_map>
#include <vector>

class FreqStack {
    std::unordered_map<int, int> counter;
    std::unordered_map<int, std::vector<int>> store;
    int maxFreq = 0;

public:
    void push(int val) {
        const int freq = ++counter[val];
        store[freq].push_back(val);
        maxFreq = std::max(maxFreq, freq);
    }

    int pop() {
        auto& candidates = store[maxFreq];
        const int val = candidates.back();
        candidates.pop_back();
        --counter[val];
        if (candidates.empty()) --maxFreq;
        return val;
    }
};
```

Hashmap 操作平均 O(1)，vector 尾端新增均攤 O(1)：push 為平均、均攤 O(1)，pop 為平均 O(1)。總 push 次數 P 下，空間最壞 O(P)，包含保留容量、空 bucket 與零計數 key。

## 6. 文獻如何對應這個心法？

- **保存計算結果與決策**：上述 MIT DP 講義提供 memoization、table 與 parent pointers 的系統化說明。這支持資訊保留的不同用途，不表示 895 是 DP。
- **保存恢復所需的變更**：Demaine、Iacono、Langerman 的 *Retroactive Data Structures*（2007）§3.1 介紹 rollback method，例如寫入前保存舊值。這支持「操作前先保留恢復依據」，不表示 895 是 retroactive data structure。[作者版，第 7–8 頁](https://people.csail.mit.edu/edemaine/papers/Retroactive_TALG/paper.pdf#page=7)
- **按優先序組織候選**：Eppstein 的 *Integer Priority Queues* 講義介紹 bucket queues。一般 bucket queue 找極值仍可能掃描；895 的 `maxFreq--` 必須靠上方 invariant 另外證明。[UCI CS 261，第 7–8 頁](https://ics.uci.edu/~eppstein/261/lecture5b.pdf#page=7)
- **保留可查詢的舊版本**：Okasaki 的經典教材 *Purely Functional Data Structures*（1998）第 2 章討論 persistence。依據[出版社章節摘要](https://doi.org/10.1017/CBO9780511530104.003)，它保留可用的舊版本；895 只保留未消耗紀錄，沒有提供這種版本查詢能力。

## ✅ 設計檢查

- [ ] 目前狀態足以支援下一次操作，還是只夠回答現在？
- [ ] 每筆歷史的意義、存取順序與刪除條件是否明確？
- [ ] 能否由結構自然找到答案，省掉額外搜尋或重建？
- [ ] 若要壓縮歷史，是否已證明被丟掉的資訊不再需要？

**口訣：先定義轉換，再找會丟的資訊；按未來需求保存，證明何時能刪。**
