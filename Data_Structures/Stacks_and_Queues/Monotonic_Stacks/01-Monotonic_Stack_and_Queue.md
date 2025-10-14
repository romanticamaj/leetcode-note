# 資料結構：單調棧與單調隊列 (Monotonic Stack & Queue)

## 核心概念

**單調棧 (Monotonic Stack)** 或 **單調隊列 (Monotonic Queue)** 是一種在演算法過程中，其內部元素始終保持**單調性**（單調遞增或單調遞增）的特殊資料結構。

它的核心機制是：**在一個新元素入棧/入隊之前，從棧頂/隊尾開始，持續移除所有「破壞」單調性的舊元素。**

這個「清理」操作確保了留在結構中的元素永遠是有序的，從而讓我們能夠在 O(1) 的時間內獲取到當前的極值（例如，棧頂或隊首元素）。

---

## 單調棧 (Monotonic Stack)

單調棧是解決「下一個更大/更小元素」 (Next Greater/Smaller Element) 問題的經典利器。

### C++ 基礎模板

以下模板展示了維護一個**單調非遞減棧 (non-decreasing)** 的核心邏輯。

```cpp
#include <vector>
#include <stack>

// T: 陣列和棧中元素的類型
template<typename T>
void monotonic_stack_template(const std::vector<T>& nums) {
    std::stack<T> s; // 儲存元素值或索引

    for (const T& current_element : nums) {
        // 1. 維護單調性
        //    當前元素「破壞」了棧的單調非遞減特性時...
        while (!s.empty() && s.top() > current_element) {
            // ...處理棧頂元素（例如，找到了它的下一個更小元素）
            T top_element = s.top();
            s.pop();
            // process(top_element, current_element);
        }

        // 2. 元素入棧
        //    將當前元素入棧，維持單調性
        s.push(current_element);
    }
}
```

### 比較條件的細微差別

- **嚴格單調遞增 (Strictly Increasing):** `[1, 3, 5, 7]`
  - 清理條件: `while (!s.empty() && s.top() >= nums[i])`
  - 當棧頂元素**大於或等於**當前元素時，彈出。
- **非遞減 (Non-decreasing):** `[1, 3, 3, 5]`
  - 清理條件: `while (!s.empty() && s.top() > nums[i])`
  - 僅當棧頂元素**嚴格大於**當前元素時，彈出。

> **反向思考：** 要維持一個「遞增」的棧，新元素 `num` 必須滿足 `stack.top() < num`。當這個條件不成立時（即 `stack.top() >= num`），就需要清理棧頂。

### 時間複雜度分析

儘管模板中有 `for` 和 `while` 的嵌套循環，但其**均攤時間複雜度 (Amortized Time Complexity)** 仍然是 **O(n)**。這是因為每個元素最多只會被**入棧一次**和**出棧一次**。所有操作的總數是線性的，因此效率非常高。

---

## 單調隊列 (Monotonic Queue / Deque)

當問題從「尋找下一個」變為「維護一個滑動窗口內的最值」時，單調隊列就派上了用場。它通常使用**雙端隊列 (Deque)** 來實現。

### 核心機制

- **從尾部進 (Push Back):** 新元素加入時，從隊尾開始，移除所有破壞單調性的舊元素，然後再將新元素加入隊尾。
- **從頭部出 (Pop Front):** 當窗口滑動，最左側的元素需要被移除時，檢查隊首元素是否是這個過期元素，如果是，則將其從隊首移除。
- **查詢最值 (Query Front):** 在任何時候，隊首元素都是當前窗口內的最值。

### C++ 基礎模板

以下模板展示了維護一個**單調非遞增隊列 (non-increasing)** 的核心邏輯。

```cpp
#include <vector>
#include <deque>

// T: 陣列和隊列中元素的類型
template<typename T>
void monotonic_queue_template(const std::vector<T>& nums, int k) {
    std::deque<T> dq; // 儲存元素值或索引

    for (int i = 0; i < nums.size(); ++i) {
        // 1. 移除過期元素 (窗口左邊界)
        //    (此步驟僅在滑動窗口問題中需要)
        if (!dq.empty() && dq.front() == /* element_to_remove */) {
            dq.pop_front();
        }

        // 2. 維護單調性 (從隊尾清理)
        //    當前元素「破壞」了隊列的單調非遞增特性時...
        while (!dq.empty() && dq.back() < nums[i]) {
            dq.pop_back();
        }

        // 3. 元素入隊 (從隊尾加入)
        dq.push_back(nums[i]);

        // 4. 處理當前窗口
        //    此時 dq.front() 是當前窗口的最值
        //    if (window_is_valid) { process(dq.front()); }
    }
}
```

---

## 總結

- **單調棧：** 專注於解決「**下一個更大/更小元素**」類型的問題。
- **單調隊列：** 專注於高效解決「**滑動窗口最值**」類型的問題。

理解它們各自的「清理」和「維護」機制，是掌握這兩種強大資料結構的關鍵。
