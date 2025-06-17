# Two Pointers 技巧

## 要點

- 涉及使用兩個整數變量（指針），這兩個指針都沿著可迭代數據結構移動
- 從輸入的邊緣開始放置指針（一個在開始，一個在結尾）。讓它們朝彼此移動直到相遇
- 特別注意 **sorted** 的 array 可以用，尤其是 **Partially Sorted**，例如，雙邊方向個別 sorted
- **快慢 pointer** 也是一個使用時機，例如 一個走 **1x**，一個走 **0.5x**，去找到中心位置，或是類似變形

## 常見問題

- **Reverse String**: 反轉字符串，使用兩個指針從字符串的兩端向中間移動
- **Squares of a Sorted Array**: 對排序數組中的元素進行平方，並保持結果有序
- **Linked List Cycle Detection**: 使用快慢指針檢測鏈表中是否存在環
- **Find Middle of Linked List**: 使用快慢指針找到鏈表的中間節點

## Fast and Slow Pointers

Fast and Slow Pointers 是 Two Pointers 技巧的一種特殊實現，主要用於鏈表和數組操作。

### 核心概念

- Fast and Slow Pointers 是 Two Pointers 技巧的一種實現
- 兩個指針以不同的「速度」移動，或從不同的位置開始迭代，或具有其他抽象差異
- 常見使用方式，「快」指針每次迭代移動兩個節點，而「慢」指針每次迭代移動一個節點

### 基本模板

```python
# head 是鏈表的頭節點
def fn(head):
    slow = head
    fast = head
    
    while fast and fast.next:
        # 在這裡執行操作
        slow = slow.next
        fast = fast.next.next
```

**while 循環條件說明**：
- 我們需要檢查 `fast` 和 `fast.next` 的非空性，因為在循環內部會使用 `fast.next.next`

### 常見應用

1. **檢測鏈表中的環 (Cycle Detection)**
2. **找到鏈表的中間節點 (Finding Middle Node)**
3. **判斷鏈表是否為回文 (Palindrome Linked List)**

### 優勢

- **空間效率**：通常只需要 O(1) 的額外空間
- **時間效率**：通常只需要一次遍歷，時間複雜度為 O(n)
- **簡潔性**：代碼簡潔易懂，實現簡單