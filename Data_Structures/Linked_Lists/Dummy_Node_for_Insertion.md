# 心法：使用虛擬頭節點 (Dummy Node) 簡化鏈結串列插入操作

## 1. 問題：惱人的邊界情況

在對鏈結串列進行插入操作時，最麻煩的邊界情況之一就是「在頭部插入」(Insert at Front)。

傳統的作法需要一個指標來追蹤目前節點的前一個節點 (previous pointer, `pp`)。但如果要插入的位置在串列的最前端，此時 `pp` 會是 `nullptr`。這就導致程式碼中需要一個額外的 `if` 判斷式來專門處理這種情況，使得邏輯變得複雜且容易出錯。

如下方的 `insertionSortList` 範例所示，`if (!pp)` 這個區塊就是專門用來處理插入到頭部的情況。

### 範例：沒有使用 Dummy Node 的版本

```cpp
class Solution {
public:
    ListNode* insertionSortList(ListNode* head) {
        ListNode *sorted = nullptr; // 已排序串列的頭部

        while (head) { // 遍歷未排序的節點
            // 1. 尋找插入點
            ListNode *p = sorted;
            ListNode *pp = nullptr; // p 的前一個節點

            while (p && p->val <= head->val) {
                pp = p;
                p = p->next;
            }

            // 2. 插入節點
            ListNode *headNext = head->next;
            head->next = p;

            // !! 邊界情況判斷 !!
            if (!pp) {
                // 如果 pp 是 nullptr，表示要插入到最前面
                sorted = head;
            } else {
                // 插入到中間或尾部
                pp->next = head;
            }

            // 3. 更新 head，處理下一個未排序節點
            head = headNext;
        }

        return sorted;
    }
};
```

## 2. 解決方案：Dummy Node 技巧

**核心思想**：建立一個「虛擬頭節點」(Dummy Node)，讓它指向真正已排序串列的頭部。

這個 Dummy Node 本身不儲存任何有效資料，它的唯一目的就是作為一個固定的「錨點」。

**優點**：
透過引入 Dummy Node，**「在頭部插入」這個邊界情況被完全消除**。原本的「在頭部插入」現在變成了「在 Dummy Node 之後插入」，這與在串列中任何其他位置插入的邏輯完全相同。

如此一來，我們就不再需要 `if (!pp)` 這個判斷式，程式碼變得更簡潔、更通用。

### 範例：使用 Dummy Node 的優化版本

在這個版本中，我們使用 `std::make_unique<ListNode>()` 來建立 Dummy Node。`unique_ptr` 會自動管理其生命週期，確保在函式結束時釋放記憶體，是現代 C++ 的良好實踐。

`pp` 的初始值永遠是 `dummy` 節點，`p` 的初始值是 `dummy->next`（即真正的已排序串列頭部）。這樣 `pp` 永遠不會是 `nullptr`，插入邏輯得到了統一。

```cpp
class Solution {
public:
    ListNode* insertionSortList(ListNode* head) {
        // 使用 unique_ptr 管理 dummy node 的生命週期
        auto dummy = std::make_unique<ListNode>();

        while (head) {
            // 1. 尋找插入點
            ListNode *p = dummy->next;
            ListNode *pp = dummy.get(); // pp 初始指向 dummy node

            // 為了 stable sort，使用 <=
            // 讓值相等的元素插入到其原始順序的後面
            while (p && p->val <= head->val) {
                pp = p;
                p = p.next;
            }

            // 2. 插入節點 (邏輯已統一)
            ListNode *headNext = head->next;
            head->next = p;
            pp->next = head; // pp 永遠有值，無需判斷

            // 3. 更新 head
            head = headNext;
        }

        return dummy->next; // 返回真正的頭部
    }
};
```

## 3. 總結與權衡

- **優點**：
  - **簡化邏輯**：消除處理頭部插入的 `if-else` 判斷，使程式碼更乾淨、更通用。
  - **降低錯誤率**：更少的邊界情況意味著更低的 bug 風險。

- **權衡**：
  - **空間成本**：需要額外配置一個 `ListNode` 的空間。在大多數情況下，這點額外的空間成本是完全值得的，因為它換來了程式碼的簡潔性和健壯性。

在解 LeetCode 或任何鏈結串列相關問題時，當意識到可能會修改到頭部節點時，應優先考慮使用 Dummy Node 技巧。
