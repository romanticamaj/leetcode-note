# Bottom-Up Divide and Conquer 解題心法

Bottom-up 的出發點是**已解好的最小子問題**：先把相鄰的小問題解 combine 成較大的解，再讓它成為下一輪的輸入。當每次合併兩段時，子問題規模依序倍增。先定義每輪處理什麼，再選擇 index 或 pointer 表達狀態。

## 🧠 設計框架：規模 → 邊界 → 合併 → 前進

| 設計步驟 | 要回答的問題 | 對應狀態／操作 |
|---|---|---|
| **1. 子問題規模** | 哪個 base case 已解好？本輪拿多大的解來合併？ | `interval` 的初值、成長與停止條件 |
| **2. 子問題邊界** | 左右段從哪開始、在哪結束？右段不存在或不足怎麼辦？ | index 邊界或 split 後的 `nullptr` |
| **3. 合併與接回** | combine 需要什麼輸入、產生什麼結果？ | 結果區間，或結果 head／tail |
| **4. 前進與換輪** | 下一組從哪開始？整輪完成後怎麼重啟掃描？ | 下一組起點、整體入口與規模倍增 |

## 1. 🧩 子問題規模：從 base case 決定 interval

**`interval` 是 combine 的輸入子問題大小。** 排序的 base case 是單一元素天然有序，因此初值 1；最後一段允許較短。

直覺上可能會用「合併後的大小」作為狀態，但定位左右子問題時，又得不斷除以 2，推回輸入大小。直接以 **subproblem size 作為 `interval`**，就能讓狀態定義與操作所需的大小一致，程式碼也更簡潔。

```cpp
// 以下索引使用 long long，假設 n 在 int 範圍內
for (long long interval = 1; interval < n; interval *= 2) {
    // interval：本輪輸入的單段大小
    // 將相鄰、各自已解好的子問題配對合併，結果大小最多為 2 * interval
}
```

當 `interval >= n`，整體已成為單一已解好的段。因此**停止條件是 `interval >= n`，繼續迭代的條件是 `interval < n`**。每次 combine 兩個子問題，下一輪的單段規模便加倍。

### 兩層迭代：外層控制規模，內層走訪配對

**外層控制合併的層次**：每輪固定一個 `interval`，處理完這個規模的所有配對，再進入下一個規模。

```text
輸入單段大小：1 → 2 → 4 → 8 → …
interval = 2：[已解 2][已解 2] | [已解 2][已解 1]
合併後：     [    已解 4    ] | [    已解 3    ]
```

**內層負責子問題的 traversal**：依照 `interval` 找出相鄰兩段，執行 combine，再前進到下一組。Combine 內部如何讀取兩段，則由具體操作決定。

| 迴圈條件 | 意義 |
|---|---|
| `interval < n` | 整體尚未成為單一已解好的段，還需要合併 |
| `start + interval < n` | 這一組的右段存在，可以配對 |

兩個條件回答不同問題：**外層管規模，內層管配對。** `n = 0` 或 `n = 1` 不需要合併；`n = 5` 則必須執行 `interval = 4`，把長度 4 與長度 1 的段合起來。

## 2. 🧩 子問題邊界：抽象相同，表示方式不同

一組包含左段與右段，需要知道**左段起點、右段起點、下一組起點**。選擇邊界表示時，同時決定 merge 如何判斷「某一段已用完」。

| 邊界責任 | Random access：array | Sequential access：linked list |
|---|---|---|
| 左段起點 | `start` | `head` |
| 右段起點 | `mid = start + interval` | 往前走最多 `interval` 個節點 |
| 下一組起點 | `end = min(start + 2 * interval, n)` | 再往前走最多 `interval` 個節點 |
| 單段結束 | 讀取 index 抵達 exclusive end | split 後，讀取指標變成 `nullptr` |
| 右段不存在／不足 | 檢查起點、用 `n` 截斷終點 | 起點可能為空，走到 `nullptr` 就停 |

### Array：用半開區間表達邊界

```cpp
for (long long start = 0; start + interval < n; start += 2 * interval) {
    auto mid = start + interval; // 內層條件已保證右段存在
    auto end = min(start + 2 * interval, static_cast<long long>(n));
    combine(start, mid, end); // 左段 [start, mid)，右段 [mid, end)
}
```

Index 能直接定位；`end` 同時是右段的 exclusive end 與下一組起點。`end == n` 合法，但不能讀取 `data[n]`。若只剩左段，保留它，等下一輪配對即可。

### Linked list：用 split 把區段邊界轉成 nullptr

原始 list 的 `nullptr` 只表示整條鏈的結尾。Split 走最多 `interval` 個節點，把段尾的 `next` 清空，讓每段都有自己的結尾；不建立新節點，merge 就能用空指標判斷段是否耗盡。段長不足時保留現有節點，後續入口為空。

```cpp
ListNode* split(ListNode* head, int interval) {
    if (!head) return nullptr;

    for (int i = 1; i < interval && head->next; ++i)
        head = head->next;

    ListNode* nextHead = head->next; // 先保存後續入口
    head->next = nullptr;           // 再建立本段邊界
    return nextHead;
}
```

這裡的關鍵是**讓指標停在段尾，而不是走到段尾之後**。先排除空的 `head`，再用 `head->next` 提前判斷是否還能前進，迴圈結束時就能直接修改段尾的 `next`。

若採用「先走一步，再檢查目前指標是否為空」的方式，走到 `nullptr` 時就無法直接取得段尾，通常還要用 `prev` 保存前一個節點。提前看 `next` 能省去這個狀態，也符合 split 需要修改段尾連結的目的。

## 3. 🧩 合併與前進：結果出口、後續入口都要保留

Array 的合併結果仍位於 `[start, end)`，下一組直接從 `end` 開始。

Linked list 的 merge 逐次接出兩段中較小的節點；其中一段耗盡後，接上另一段剩餘的節點。外層則負責接回合併結果，並繼續處理後面的子問題。

這裡有三個介面設計要點：

- **Split 建立邊界**：呼叫兩次，準備好兩個 subproblem，將各段尾節點的 `next` 設成 `nullptr`，讓 merge 的耗盡判斷保持簡單。
- **Split 回傳後續入口**：第一次取得右段起點，第二次取得下一組起點。先保存入口再斷鏈，同一個 split 就能重複使用，也不會遺失後續工作。
- **Merge 回傳結果 head／tail**：head 用來接到上一組的尾端，tail 用來接下一組的結果。

因此，外層需要明確保存**整體入口、已完成前綴的尾端，以及下一組起點**。連結可以暫時斷開，但不能失去取得這些區段的指標。

使用區域變數 `ListNode dummy(0, originalHead)` 作為 dummy head，可以統一第一組與後續組的串接。每輪開始重設 `curr = &dummy`、`head = dummy.next`；整輪完成後，`dummy.next` 就是更新後的整體入口。

## 🔑 Loop Invariant：為什麼可以一輪接一輪？

通用的保證是：**本輪開始時，各段已具有 combine 所需的解；整輪結束後，較大的各段也已解好。** 對排序，這個「解」就是各段有序。

- **Initialization**：長度 1 的段天然有序，最後一段可以較短。
- **外層每輪開始**：整體由相鄰有序段組成，除最後一段外，段長皆為 `interval`。
- **內層每組開始**：已完成前綴由合併後的有序段組成；未處理後綴仍是原規模的有序段。
- **Maintenance**：合併相鄰兩段，整輪結束後得到規模最多 `2 * interval` 的有序段，供下一輪使用。
- **Termination**：`interval >= n` 時只剩一個有序段，因此整體已排序。

已完成前綴**不一定全域有序**；只有各段有序。Split 與接回期間也可能暫時斷鏈，但保存的入口必須讓所有未處理節點仍可取得。更多證明觀點見 [Loop Invariant](../../Proof_Techniques/Loop_Invariant.md)。

## ⏱️ Bottom-Up 與 Top-Down 比較

| 面向 | Bottom-Up 配對合併 | Top-Down 二分後合併 |
|---|---|---|
| 思考方向 | 從 base case 的解逐層組合 | 先切半，遞迴求解後組合 |
| 規模與邊界 | 明確設計 interval、配對與尾段 | 由每次呼叫的範圍決定子問題 |
| 狀態管理 | 明確保存本輪結果、下一組入口 | 呼叫堆疊保存返回位置與局部狀態 |
| 控制空間 | O(1) | O(log n) 堆疊，假設平衡二分 |
| 學習難點 | 規模成長、邊界與接回 | 遞迴契約、base case 與返回結果 |

每輪若合計 `O(n)`，配對倍增共 `O(log n)` 輪，總時間才是 `O(n log n)`。List 的定位與 merge 即使各走一次，整輪仍為 `O(n)`；單次則為 `O(interval)`。

**控制空間與 combine 空間要分開算**：array merge sort 通常另需 `O(n)` buffer 做 merge；list 使用迭代 merge 重接節點，可做到總額外空間 `O(1)`。兩種遍歷都可能連續存取 array，不能只因 bottom-up 就斷言快取表現一定較好。

## 📚 實際範例索引

| 題目 | 對照框架的練習重點 |
|---|---|
| LC 21. Merge Two Sorted Lists | 單次 combine：兩個輸入如何耗盡，結果如何接出來 |
| LC 912. Sort an Array | Index 邊界、右段截斷與逐輪規模成長 |
| LC 148. Sort List | Split 邊界、結果 head／tail、下一組入口與整輪重啟 |
| LC 23. Merge k Sorted Lists | 將子問題單位換成「一條已排序 list」；按 list 數量配對合併 |

延伸閱讀：[區間設計](03_Interval_Design_in_Divide_and_Conquer.md)、[Merge Sort](../Sorting/Comparison_Based_Sorting/05-Merge_Sort.md)、[Dummy Node](../../Data_Structures/Linked_Lists/Dummy_Node_for_Insertion.md)。
