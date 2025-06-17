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

## Two Pointer 變體

Two Pointer 技巧有多種變體，每種變體適用於不同類型的問題：

- [Fast and Slow Pointers](./Fast_and_Slow_Pointers.md): 兩個指針以不同速度移動，常用於鏈表操作
- [K-Gap Pointers](./K_Gap_Pointers.md): 兩個指針保持固定距離，適用於需要處理相距 k 個位置的元素
- [Adjacent Pointers](./Adjacent_Pointers.md): 兩個相鄰指針（或 1-gap pointers），以相同速度移動，常用於反轉鏈表等就地修改操作

## Two Pointer 技巧的關鍵設計要素

在使用 Two Pointer 技巧時，有兩個關鍵設計要素需要特別注意：

### 1. While Condition (終止條件)

終止條件決定了循環何時結束，它必須確保：

- 所有指針操作都是安全的（避免空指針異常）
- 算法能夠正確處理所有有效輸入
- 不會導致無限循環

**設計原則**：

- 分析循環內部的指針操作，確保條件能防止任何不安全的訪問
- 考慮邊界情況，如空輸入、單節點輸入等
- 確保終止條件與問題的目標一致

**常見模式**：

```cpp
// 從兩端向中間移動的指針
while (left < right) {
    // 操作 array[left] 和 array[right]
    // ...
}

// 快慢指針
while (fast && fast->next) {
    slow = slow->next;
    fast = fast->next->next;
    // ...
}

// K-Gap 指針
while (right && n > 0) {
    right = right->next;
    n--;
}
while (right) {
    // 判斷題目條件
    // ...

    // 操作 left 和 right
    left = left->next;
    right = right->next;
}
```

### 2. While Loop Movement (前進條件)

前進條件決定了指針如何移動，它必須確保：

- 算法能夠向解決方案推進
- 不會跳過可能的解
- 最終會達到終止條件

**設計原則**：

- 指針移動必須與問題目標相關
- 每次迭代都應該縮小問題規模或接近目標
- 避免指針移動導致的無限循環
- **特別注意：前進條件直接會跟 While Condition 有關，例如 pointer nullity 判斷**

**常見模式**：

```cpp
// 相向移動
left++;
right--;

// 同向移動（不同速度）
slow = slow->next;         // 移動一步
fast = fast->next->next;   // 移動兩步

// 條件性移動
if (condition) {
    left++;
} else {
    right--;
}
```

### 兩者的關係

While Condition 和 While Loop Movement 是緊密相關的：

- 終止條件必須考慮指針的移動方式
- 指針的移動必須最終導致終止條件的滿足
- 兩者共同確保算法的正確性和效率
