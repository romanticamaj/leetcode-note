# Frequency Matching Counting Invariant 心法

## 🧠 核心哲學

當 Sliding Window 需要比較兩個頻率表是否「匹配」時，**不要每次都遍歷整個頻率表比較**。改用 `matchedCount` 追蹤「有多少 key 的頻率已經匹配」，將 O(k) 比較降為 O(1) 判斷。

---

## 🎯 TL;DR

```
matchedCount = 頻率完全相等的 key 數量
當 matchedCount == total keys → 兩個頻率表完全匹配
```

**更新口訣**：「先查舊、更頻率、再查新」

---

## 核心 Invariant 定義

### Invariant Statement

```
matchedCount 代表 windowFreq[key] == targetFreq[key] 的 key 數量
```

- 當 `matchedCount == targetFreq.size()` → 窗口完全匹配目標
- 窗口滑動時，只有 **進入** 和 **離開** 的元素會影響 `matchedCount`

### 為什麼需要這個 Invariant？

| 方法                 | 每次滑動的比較成本 | 總時間複雜度 |
| -------------------- | ------------------ | ------------ |
| Naive 比較整個頻率表 | O(k)               | O(n × k)     |
| matchedCount 追蹤    | O(1)               | O(n)         |

---

## 🧩 更新 matchedCount 的正確邏輯

### 核心原則：Before-Update-After Pattern

```cpp
// 當元素 c 進入窗口時
if (windowFreq[c] == targetFreq[c]) matchedCount--;  // Before: 舊狀態是匹配的，即將破壞
windowFreq[c]++;                                      // Update: 更新頻率
if (windowFreq[c] == targetFreq[c]) matchedCount++;  // After: 新狀態變成匹配

// 當元素 c 離開窗口時
if (windowFreq[c] == targetFreq[c]) matchedCount--;  // Before: 舊狀態是匹配的，即將破壞
windowFreq[c]--;                                      // Update: 更新頻率
if (windowFreq[c] == targetFreq[c]) matchedCount++;  // After: 新狀態變成匹配
```

### 為什麼是這個順序？

```
狀態轉換只有四種可能：
  matched → unmatched  (matchedCount--)
  unmatched → matched  (matchedCount++)
  unmatched → unmatched (no change)
  matched → matched    (不可能，因為頻率改變了)

Before-Update-After 能正確處理所有情況：
  - 如果舊狀態 matched，先減
  - 更新頻率
  - 如果新狀態 matched，後加
```

---

## 📦 Generic Template

### Fixed Window Frequency Matching

```cpp
bool hasMatch(const string& target, const string& source) {
    if (target.size() > source.size()) return false;

    unordered_map<char, int> targetFreq, windowFreq;
    int matchedCount = 0;
    const int windowSize = target.size();

    // Build target frequency
    for (char c : target) targetFreq[c]++;

    // Initialize: count keys with freq == 0 as "matched" initially
    // (keys not in target that also have 0 in window)
    // Simpler: only track keys that exist in target
    matchedCount = 0;

    for (int i = 0; i < source.size(); i++) {
        char in = source[i];

        // Element entering window
        if (targetFreq.count(in)) {
            if (windowFreq[in] == targetFreq[in]) matchedCount--;
            windowFreq[in]++;
            if (windowFreq[in] == targetFreq[in]) matchedCount++;
        }

        // Element leaving window (when window is full)
        if (i >= windowSize) {
            char out = source[i - windowSize];
            if (targetFreq.count(out)) {
                if (windowFreq[out] == targetFreq[out]) matchedCount--;
                windowFreq[out]--;
                if (windowFreq[out] == targetFreq[out]) matchedCount++;
            }
        }

        // Check match (when window is full)
        if (i >= windowSize - 1 && matchedCount == targetFreq.size()) {
            return true;
        }
    }
    return false;
}
```

### 簡化版：使用 Fixed-Size Array

```cpp
// 當字元集是 26 個小寫字母時
bool hasMatch(const string& s1, const string& s2) {
    if (s1.size() > s2.size()) return false;

    array<int, 26> target{}, window{};
    int matched = 0;

    // Initialize
    for (int i = 0; i < s1.size(); i++) {
        target[s1[i] - 'a']++;
        window[s2[i] - 'a']++;
    }
    for (int i = 0; i < 26; i++) {
        if (target[i] == window[i]) matched++;
    }

    // Slide
    for (int i = 0; i <= s2.size() - s1.size(); i++) {
        if (matched == 26) return true;

        if (i + s1.size() < s2.size()) {
            int in = s2[i + s1.size()] - 'a';
            int out = s2[i] - 'a';

            // Process entering element
            if (window[in] == target[in]) matched--;
            window[in]++;
            if (window[in] == target[in]) matched++;

            // Process leaving element
            if (window[out] == target[out]) matched--;
            window[out]--;
            if (window[out] == target[out]) matched++;
        }
    }
    return false;
}
```

---

## ⚠️ 常見陷阱

### 1. 更新順序錯誤

```cpp
// ❌ 錯誤：先更新頻率再檢查
windowFreq[c]++;
if (windowFreq[c] == targetFreq[c]) matchedCount++;
// 漏掉了「原本是匹配的，更新後不匹配」的情況

// ✅ 正確：Before-Update-After
if (windowFreq[c] == targetFreq[c]) matchedCount--;
windowFreq[c]++;
if (windowFreq[c] == targetFreq[c]) matchedCount++;
```

### 2. 忘記檢查 key 是否在 target 中

```cpp
// ❌ 錯誤：對所有字元都更新 matchedCount
windowFreq[c]++;
if (windowFreq[c] == targetFreq[c]) matchedCount++;  // targetFreq[c] 可能是 0

// ✅ 正確：只處理 target 中存在的 key
if (targetFreq.count(c)) {
    // ... update logic
}
```

### 3. 初始化 matchedCount 錯誤

```cpp
// 方法 A：初始化後遍歷檢查
for (int i = 0; i < 26; i++) {
    if (target[i] == window[i]) matched++;
}

// 方法 B：只追蹤 target 中的 key
// matchedCount 初始為 0，逐一加入元素時更新
// 最終檢查 matchedCount == targetFreq.size()
```

### 4. Fixed Array vs HashMap 的 matchedCount 判斷

```cpp
// Fixed Array (26 letters): matched == 26
// HashMap: matched == targetFreq.size()
```

---

## 🔄 Variable Window 的變體

當窗口大小可變時（如 LC 76 Minimum Window Substring），invariant 稍有不同：

```cpp
// Invariant: matchedCount >= requiredCount 表示窗口有效
// 注意：這裡是「至少」而非「恰好」

// 進入窗口
if (windowFreq[c] == targetFreq[c]) matchedCount++;
// 當 windowFreq[c] 從 targetFreq[c]-1 變成 targetFreq[c]

// 離開窗口
if (windowFreq[c] == targetFreq[c]) matchedCount--;
// 當 windowFreq[c] 從 targetFreq[c] 變成 targetFreq[c]-1
```

---

## ⏱️ 複雜度分析

| 操作                | 時間複雜度 | 說明            |
| ------------------- | ---------- | --------------- |
| 建立 targetFreq     | O(m)       | m = target 長度 |
| 初始化 matchedCount | O(k)       | k = 字元種類數  |
| 每次滑動更新        | O(1)       | 固定操作數      |
| 總時間              | O(n + m)   | n = source 長度 |
| 空間                | O(k)       | 頻率表大小      |

---

## ✅ 關鍵要點

- [ ] **Invariant 定義**：`matchedCount` = 頻率完全相等的 key 數量
- [ ] **更新順序**：Before-Update-After pattern
- [ ] **判斷條件**：
  - Fixed array (26 letters): `matched == 26`
  - HashMap: `matched == targetFreq.size()`
- [ ] **只處理 target 中的 key**：避免錯誤計算不存在的 key
- [ ] **Variable window**：判斷「至少」匹配，而非「恰好」匹配

---

## 相關題目

- LeetCode 567. Permutation in String
- LeetCode 438. Find All Anagrams in a String
- LeetCode 76. Minimum Window Substring
- LeetCode 30. Substring with Concatenation of All Words
