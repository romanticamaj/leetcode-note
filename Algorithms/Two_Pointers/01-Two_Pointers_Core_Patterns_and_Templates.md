# 雙指針核心模式與模板 (Two Pointers: Core Patterns & Templates)

雙指針是一種極其強大且高效的演算法技巧，其核心思想是**透過兩個或多個指針在資料結構中的協同移動，來系統性地縮小問題的「搜尋空間」或「關注範圍」，從而以線性時間複雜度解決問題。**

這與二分搜尋法 (Binary Search) 的哲學有異曲同工之妙：兩者都是透過定義和縮小搜尋空間來逼近答案。

---

## 共通設計框架 (General Framework)

無論哪種雙指針模式，其設計都遵循四個基本步驟：

1. **指針初始化 (Pointer Initialization):**

   - **定義初始搜尋空間 (Defining Initial Search Space):** 對於「對向雙指針」，初始化是為了定義整個問題的初始邊界，例如 `[0, n-1]`。
   - **定義遍歷起點 (Defining Traversal Start):** 對於「同向」或「快慢」指針，初始化是為了設定遍歷的共同起點，而搜尋空間是動態變化的（如窗口大小或相對距離）。

2. **循環條件 (Loop Condition):**

   - 定義指針可以持續移動的條件。這通常代表著「搜尋空間仍然有效」。
   - 例如：`left < right`、`fast != nullptr && fast->next != nullptr`、`i < arr1.size() && j < arr2.size()`。

3. **移動邏輯 (Movement Logic):**

   - 在循環內部，根據特定條件來決定如何移動一個或兩個指針。
   - 這是演算法的核心，每一次移動都意味著排除了部分搜尋空間。

4. **終止狀態 (Termination State):**
   - 循環結束時，指針所在的狀態。答案可能在終止的位置，也可能在循環過程中已經計算完畢。

---

## 三大核心模式與模板

接下來，我們將深入探討三種最常見的雙指針模式。

### --- 模式一：對向雙指針 (Opposite Ends) ---

此模式通常用於**已排序**的陣列，一個指針從頭開始，另一個從尾開始，相互逼近，共同定義一個逐漸縮小的搜尋窗口。

**適用場景：**

- 在已排序陣列中尋找滿足特定條件的數對 (e.g., Two Sum)。
- 反轉陣列或字串。
- 檢查迴文。

**C++ 模板：**

```cpp
// T: return type, U: array element type
template<typename T, typename U>
T opposite_ends_template(vector<U>& arr) {
    // 1. 指針初始化 (Pointer Initialization): 定義初始搜尋空間
    int left = 0;
    int right = arr.size() - 1;
    T ans = 0; // Or other initial value

    // 2. 循環條件 (Loop Condition): 搜尋空間有效
    while (left < right) {
        // 3. 移動邏輯 (Movement Logic): 根據條件縮小一端
        if (CONDITION(arr[left], arr[right])) {
            left++;
        } else {
            right--;
        }
    }

    // 4. 終止狀態 (Termination State): left == right
    return ans;
}
```

**框架分析：**

- **初始化：** `left` 在頭，`right` 在尾，明確定義了初始搜尋空間 `[0, n-1]`。
- **移動邏輯：** 根據 `arr[left]` 和 `arr[right]` 的關係，我們總能確定性地排除一端，從而將搜尋空間縮小一格。

**設計心法：排序陣列中的隱含屬性**

> 當「對向雙指針」應用於**已排序**的陣列時，由 `left` 和 `right` 指針定義的窗口 `[left, right]` 天然地包含了該窗口內的**最小值 (`arr[left]`)** 和**最大值 (`arr[right]`)**。

這個特性極大地簡化了需要同時考慮子序列極值的問題，因為我們無需額外遍歷來尋找最值。

**泛化模板應用：**

這個心法可以被泛化，用來處理任何需要根據窗口內極值來做決策的問題。

```cpp
// 在已排序陣列中，根據窗口極值來尋找解
while (left < right) {
    // 利用隱含屬性直接獲取窗口的最小值和最大值
    auto& min_val = arr[left];
    auto& max_val = arr[right];

    // 根據問題的具體邏輯，對當前窗口的狀態進行評估
    auto evaluation_result = evaluate_state(min_val, max_val);

    // 根據評估結果，決定如何縮小搜尋空間
    if (evaluation_result == TARGET_MET) {
        // 找到解或更新答案
        // ...
        // 可能需要同時移動兩個指針，或只移動一個
        left++;
        right--;
    } else if (evaluation_result < TARGET_STATE) {
        // 當前狀態小於目標，需要增大窗口內的最小值
        left++;
    } else { // evaluation_result > TARGET_STATE
        // 當前狀態大於目標，需要減小窗口內的最大值
        right--;
    }
}
```

### --- 模式二：同向雙指針 (Same Direction) ---

此模式的指針朝同一方向移動，但通常有不同的職責，用於定義一個動態的「關注範圍」或在多個序列間同步推進。

#### 子模式 2a：滑動窗口 (Sliding Window)

這是「同向雙指針」在單一陣列上最經典的應用。`left` 和 `right` 指針定義了一個「窗口」，通常用於尋找滿足特定條件的最長或最短子陣列。

**C++ 模板 (動態窗口):**

```cpp
// T: return type, U: array element type
template<typename T, typename U>
T sliding_window_template(vector<U>& arr) {
    // 1. 指針初始化 (Pointer Initialization): 定義窗口的起始點
    int left = 0;
    T ans = 0; // Or other initial value
    auto curr_state; // 用於追踪窗口內的狀態 (e.g., sum, character count)

    // 2. 循環條件 (Loop Condition): 右指針遍歷整個陣列以擴展窗口
    for (int right = 0; right < arr.size(); ++right) {
        add_to_state(curr_state, arr[right]);

        // 3. 移動邏輯 (Movement Logic): 根據條件收縮窗口
        while (WINDOW_CONDITION_BROKEN(curr_state)) {
            remove_from_state(curr_state, arr[left]);
            left++;
        }

        // 4. 終止狀態 (部分): 在每個有效的窗口狀態下更新最終答案
        update_ans(ans, curr_state);
    }

    return ans;
}
```

#### 子模式 2b：雙序列迭代 (Two-Sequence Iteration)

兩個指針在**兩個不同**的資料結構上各自同向移動，通常用於合併或比較。

**C++ 模板:**

```cpp
// T: return type, U1/U2: array element types
template<typename T, typename U1, typename U2>
T two_sequence_template(vector<U1>& arr1, vector<U2>& arr2) {
    // 1. 指針初始化 (Pointer Initialization): 定義遍歷起點
    int i = 0, j = 0;
    T ans = 0; // Or other initial value

    // 2. 循環條件 (Loop Condition): 共同的搜尋空間有效
    while (i < arr1.size() && j < arr2.size()) {
        // 3. 移動邏輯 (Movement Logic): 根據條件推進其中一個指針
        if (CONDITION(arr1[i], arr2[j])) {
            i++;
        } else {
            j++;
        }
    }

    // 4. 終止狀態 (Termination State): 處理剩餘元素
    while (i < arr1.size()) { /* Logic for remaining arr1 */ i++; }
    while (j < arr2.size()) { /* Logic for remaining arr2 */ j++; }

    return ans;
}
```

### --- 模式三：快慢指針 (Fast & Slow Pointers) ---

此模式在同一個資料結構上，讓兩個指針以不同速度移動，利用速度差來探測特定結構，最常用於鏈表。

**適用場景：**

- 檢測鏈表是否有環 (Floyd's Tortoise and Hare algorithm)。
- 尋找鏈表的中點或倒數第 k 個節點。

**C++ 模板:**

```cpp
// Assuming a standard ListNode definition
bool fast_slow_template(ListNode* head) {
    // 1. 指針初始化 (Pointer Initialization): 定義共同遍歷起點
    ListNode* slow = head;
    ListNode* fast = head;

    // 2. 循環條件 (Loop Condition): 快指針的搜尋空間有效
    while (fast != nullptr && fast->next != nullptr) {
        // 3. 移動邏輯 (Movement Logic): 指針以不同速度移動
        slow = slow->next;
        fast = fast->next->next;

        // 4. 終止狀態 (部分): 檢查是否滿足特定條件 (e.g., 相遇)
        if (slow == fast) {
            return true; // Condition met (e.g., cycle detected)
        }
    }

    // Loop finished, condition not met (e.g., no cycle)
    return false;
}
```

---

## 總結心法

> **雙指針是將 O(N^2) 的暴力窮舉優化為 O(N) 的利器。當你發現問題可以透過定義一個「有效區間」或「相對位置」，並根據某些條件單向地縮小這個區間來求解時，就應該考慮雙指針。**

- **排序是前提嗎？** 對於「對向雙指針」通常是，但對於「同向」和「快慢」則不一定。
- **如何選擇模式？**
  - 需要從兩端逼近找答案？ -> **對向雙指針**。
  - 需要維護一個連續的區間或比較兩個序列？ -> **同向雙指針**。
  - 需要在鏈表或序列中利用速度差？ -> **快慢指針**。
