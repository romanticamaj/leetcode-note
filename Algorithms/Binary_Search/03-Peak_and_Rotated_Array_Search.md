# 峰值與旋轉陣列的二分搜尋（Peak and Rotated Array Search）

## ℹ️ Inflection Point 定義 / Definition

拐點（Inflection Point）是指數組中**單調性改變**的那個位置，例如：

- 由遞增 → 遞減：峰值 (peak)
- 由遞減 → 遞增：谷值 (valley) 或旋轉最小值 (rotation point)

## 🧠 核心哲學

將「旋轉點、峰值、谷值」視為唯一結構拐點，二分搜尋通過 mid 判斷位置，並朝拐點方向收縮。

## 通用模板 / General Template

```cpp
int findInflection(vector<int>& nums) {
    int l = 0, r = nums.size() - 1;
    while (l < r) {
        int m = l + (r - l) / 2;
        if (beforeInflection(m, nums, l, r))
            l = m + 1;  // 拐點在右側
        else
            r = m;      // 拐點在左側或為 m
    }
    return l;
}
```

## 🧩 判斷方法 / Detection Method

- Minimum in Rotated Array (LeetCode 153):  
  `beforeInflection(m) → nums[m] > nums[r]`
- Peak Element (LeetCode 162):  
  `beforeInflection(m) → nums[m] < nums[m+1]`

## ⚠️ 對照：LC 33 不是找拐點 / Contrast: LC 33 Search in Rotated Sorted Array

LC 33 和 LC 153 長得很像，但是**兩種不同的 binary search**，混用是反覆做錯的主因。

| | LC 153 Find Minimum | LC 33 Search |
| :--- | :--- | :--- |
| 目標 | 找 inflection point | 找 target |
| 每輪的問題 | `nums[m] > nums[r]`？（跟右端比） | `[l, m]` 是否 sorted？（`nums[l] <= nums[m]`） |
| 動作 | 往拐點方向收縮 | sorted 那半做普通 range check → 在就進去，不在就 **prune 另一半** |
| 心智模型 | 逼近唯一結構點 | 每輪只問「哪半是正常的」 |

LC 33 **不是「先找 pivot 再二分」**（那是兩段），而是把兩段壓成一段：每一輪只需要知道哪半是 sorted，就能用普通的 `lo <= target < hi` 判斷 target 是否在裡面。

```cpp
int search(vector<int>& nums, int target) {
    int l = 0, r = nums.size() - 1;
    while (l <= r) {
        int m = l + (r - l) / 2;
        if (nums[m] == target) return m;

        if (nums[l] <= nums[m]) {              // 左半 [l, m] 是 sorted
            if (nums[l] <= target && target < nums[m]) r = m - 1;  // 在左半
            else                                       l = m + 1;  // prune 左半
        } else {                               // 右半 [m, r] 是 sorted
            if (nums[m] < target && target <= nums[r]) l = m + 1;  // 在右半
            else                                       r = m - 1;  // prune 右半
        }
    }
    return -1;
}
```

**⚠️ 必須是 `nums[l] <= nums[m]`，不是 `<`**：當 `l == m`（區間剩兩個元素）時，單元素也算 sorted；用 `<` 會把這種情況錯判成「右半 sorted」，然後漏掉 target。

**口訣**：153 問「拐點在哪」，33 問「哪半正常」。

## ✅ 關鍵要點 / Key Points

- 問題核心：尋找唯一結構拐點
- 選擇清晰對稱的比較：右邊界或鄰居
- 維持不變式：拐點 ∈ [l, r]
- 每次收縮一半，O(log n) 時間，O(1) 空間

## 適用場景 / Use Cases

- LeetCode 153: Find Minimum in Rotated Sorted Array
- LeetCode 162: Find Peak Element
- LeetCode 33: Search in Rotated Sorted Array（對照組：找 sorted 半邊，非找拐點）
