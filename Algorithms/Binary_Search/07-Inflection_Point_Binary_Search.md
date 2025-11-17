# Inflection Point 二分搜尋 / Inflection Point Binary Search

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

## ✅ 關鍵要點 / Key Points

- 問題核心：尋找唯一結構拐點
- 選擇清晰對稱的比較：右邊界或鄰居
- 維持不變式：拐點 ∈ [l, r]
- 每次收縮一半，O(log n) 時間，O(1) 空間

## 適用場景 / Use Cases

- LeetCode 153: Find Minimum in Rotated Sorted Array
- LeetCode 162: Find Peak Element
