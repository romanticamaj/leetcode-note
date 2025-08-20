# 深度案例研究：LeetCode 3 的兩種滑動窗口實現

本文檔深入分析 LeetCode 3「最長不含重複字符的子字符串」的兩種不同滑動窗口實現，旨在揭示模板選擇背後的性能和風格差異。

## 版本一：半開區間變體 (`unordered_set`)

這是一個邏輯正確，但控制流較為複雜的實現，體現了半開區間 `[left, right)` 的思想。

```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        unordered_set<char> hashMap; // 使用 set 檢查重複

        int max_len = 0;
        int left = 0;
        int right = 0;

        for (; right < s.size(); right++) {
            // 情況一：當前字符不重複，直接加入並擴張
            if (!hashMap.contains(s[right])) { // C++11 count, C++20 contains
                hashMap.insert(s[right]);
                continue;
            }

            // 情況二：遇到重複字符
            // 1. 先結算遇到重複前的最長長度
            max_len = std::max(max_len, right - left);

            // 2. 收縮窗口，直到移除造成重複的那個字符
            while (hashMap.contains(s[right])) {
                hashMap.erase(s[left++]);
            }

            // 3. 將當前字符加入，使窗口再次合法
            hashMap.insert(s[right]);
        }

        // 迴圈結束後，結算最後一個窗口
        max_len = std::max(max_len, right - left);

        return max_len;
    }
};
```

### 邏輯評估

- **正確性**: 邏輯正確，遵循了「擴張-收縮」的核心思想。
- **風格**: 可視為半開區間 `[left, right)` 的一種變體，但實現較為繁瑣。
- **複雜度**:
  - `if/continue` 結構使主循環邏輯分支變多，可讀性稍差。
  - 需要在循環外進行一次額外的 `max` 計算，容易遺忘。

## 版本二：標準閉區間模板 (`unordered_map`)

這是更為標準和高效的實現，也是我們在 LeetCode 實戰中推薦的黃金模板。

```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        unordered_map<char, int> window; // 使用 map 來計數

        int ans = 0;
        int left = 0;

        for (int right = 0; right < s.size(); right++) {
            // 1. 將當前元素加入窗口 (計數+1)
            window[s[right]]++;

            // 2. 如果計數 > 1，說明重複了，收縮窗口
            while (window[s[right]] > 1) {
                window[s[left]]--;
                left++;
            }

            // 3. 此時窗口 [left, right] 必定合法，更新答案
            ans = std::max(ans, right - left + 1);
        }

        return ans;
    }
};
```

### 邏輯評估

- **正確性**: 經典的閉區間 `[left, right]` 實現，邏輯無懈可擊。
- **簡潔性**:
  - 沒有 `if/continue` 分支，主循環邏輯統一。
  - 總是在循環的最後一步更新答案，無需額外處理。
  - `right - left + 1` 的長度計算非常直觀。

## 性能差異分析：為什麼版本二更快？

1. **數據結構選擇 (`unordered_set` vs `unordered_map`)**:

   - `map` 允許窗口內有重複計數，其收縮條件 `while (window[s[right]] > 1)` 比 `set` 的 `while (window.count(s[right]))` 更精確，收縮目標更明確。

2. **程式碼結構與分支預測**:

   - 版本二的代碼路徑非常統一，每次循環都執行相同的「加入 -> 檢查 -> 更新」序列，這種可預測性對 CPU 的分支預測更友好。
   - 版本一的 `if/continue` 創建了兩個主要的執行路徑，可能導致輕微的性能損失。

3. **控制流**:
   - 版本二的邏輯更為流暢和精煉，避免了版本一中較為繁瑣的 `continue` 和循環外結算。

## 結論

版本二（閉區間 `map` 計數法）因其**邏輯更統一、代碼更簡潔、收縮條件更精確**而成為解決此類問題的黃金標準模板，特別適合在有時間壓力的 LeetCode 或面試場景中。

儘管版本一在性能上稍遜一籌，但它所體現的半開區間思想與 C++ STL 的迭代器風格一脈相承，對於資深的 C++ 開發者而言可能感覺更為自然。然而，在追求快速、穩定解題的場景下，我們仍然優先推薦版本二。
