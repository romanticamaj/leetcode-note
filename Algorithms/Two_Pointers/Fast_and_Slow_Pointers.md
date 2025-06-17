# Fast and Slow Pointers

Fast and Slow Pointers 是 Two Pointers 技巧的一種特殊實現，主要用於鏈表和數組操作。

## 核心概念

- Fast and Slow Pointers 是 Two Pointers 技巧的一種實現
- 兩個指針以不同的「速度」移動
- 通常情況下，「快」指針每次迭代移動兩個節點，而「慢」指針每次迭代移動一個節點 (兩倍速的意思，間接可以找到 Linked List 的 Middle Node)

## 基本模板

```cpp
// head 是鏈表的頭節點
ListNode* fn(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    
    while (fast && fast->next) {
        // 在這裡執行操作
        slow = slow->next;
        fast = fast->next->next;
    }
    
    return slow;  // 根據需要返回適當的節點
}
```

**while 循環條件說明**：
- 條件 `fast && fast->next` 是為了確保安全訪問 `fast->next` 和 `fast->next->next`

## 常見應用

### 1. 檢測鏈表中的環 (Cycle Detection)
### 2. 找到鏈表的中間節點 (Finding Middle Node)
### 3. 判斷鏈表是否為回文 (Palindrome Linked List)

## 關鍵設計要素

### 1. While Condition (終止條件)

Fast and Slow Pointers 的終止條件通常基於快指針的有效性：

```cpp
while (fast && fast->next) {
    // 操作...
}
```

這個條件確保：
- `fast` 不為 nullptr，所以可以安全地訪問 `fast->next`
- `fast->next` 不為 nullptr，所以可以安全地訪問 `fast->next->next`

**設計原則**：
- 分析循環內部的指針操作，確保條件能防止任何不安全的訪問
- 考慮邊界情況，如指標是否已為空
- 確保終止條件與問題的目標一致

### 2. While Loop Movement (前進條件)

Fast and Slow Pointers 的前進條件通常是：

```cpp
slow = slow->next;        // 移動一步
fast = fast->next->next;  // 移動兩步
```

這個移動模式確保：
- 慢指針以正常速度移動
- 快指針以兩倍速度移動
- 如果存在環，兩個指針最終會相遇
- 如果是線性鏈表，快指針會先到達末尾

**設計原則**：
- 指針移動必須與問題目標相關
- 每次迭代都應該縮小問題規模或接近目標
- 移動速度的差異應該能夠幫助解決特定問題（如檢測環、找中點等）

## 優勢

- **空間效率**：通常只需要 O(1) 的額外空間
- **時間效率**：通常只需要一次遍歷，時間複雜度為 O(n)
- **簡潔性**：代碼簡潔易懂，實現簡單