# K-Gap Pointers

K-Gap Pointers 是 Two Pointers 技巧的一種變體，其中兩個指針之間保持固定的 k 個距離。

## 核心概念

- 兩個指針之間保持固定的 k 個距離 (the two pointers by a gap of k)
- 兩個指針以相同的速度移動，它們始終保持 k 個距離 (move them at the same speed, they will always be k apart)
- 這種技巧特別適用於需要操作第 k 個位置的元素的問題

## 基本模板

```cpp
// 在數組中使用 k-gap pointers
void kGapPointers(vector<int>& nums, int k) {
    if (nums.size() <= k) return;
    
    int left = 0;
    int right = k;  // 初始間隔為 k
    
    while (right < nums.size()) {
        // 處理 nums[left] 和 nums[right]
        
        // 同時向前移動兩個指針，保持 k 間隔
        left++;
        right++;
    }
}

// 在鏈表中使用 k-gap pointers
ListNode* kGapPointersInList(ListNode* head, int k) {
    ListNode* slow = head;
    ListNode* fast = head;
    
    // 先將 fast 指針向前移動 k 步
    while (fast && k > 0) {
        fast = fast->next;
        k--;
    }
    
    if (k > 0) return nullptr;  // 鏈表長度小於 k
    
    while (fast) {
        // 處理 slow 和 fast 指向的節點
        
        // 同時向前移動兩個指針，保持 k 間隔
        slow = slow->next;
        fast = fast->next;
    }
    
    return slow;  // 返回特定位置的節點
}
```

## 關鍵設計要素

### 1. While Condition (終止條件)

K-Gap Pointers 的終止條件通常基於快指針的有效性：

```cpp
while (fast) {
    // 操作...
}
```

這個條件確保：
- `fast` 不為 nullptr，所以可以安全地訪問 `fast->next`
- 當 `fast` 到達鏈表末尾時，`slow` 正好位於倒數第 k 個位置

**設計原則**：
- 分析循環內部的指針操作，確保條件能防止任何不安全的訪問
- 考慮邊界情況，如鏈表長度小於 k 的情況
- 確保終止條件與問題的目標一致

### 2. While Loop Movement (前進條件)

K-Gap Pointers 的前進條件通常是：

```cpp
slow = slow->next;
fast = fast->next;
```

這個移動模式確保：
- 兩個指針以 `相同的速度` 移動
- 兩個指針之間始終保持 k 個距離
- 當 fast 到達末尾時，slow 正好位於倒數第 k 個位置

**設計原則**：
- 指針移動必須與問題目標相關
- 保持兩個指針之間的固定距離
- 確保移動方式能夠幫助解決特定問題（如找到倒數第 k 個節點）

## 常見應用

### 1. 刪除鏈表的倒數第 N 個節點
### 2. 找到鏈表的倒數第 K 個節點

## 優勢

- **單次遍歷**：只需要遍歷一次數據結構
- **固定距離**：可以輕鬆處理相距 k 個位置的元素
- **空間效率**：只需要 O(1) 的額外空間