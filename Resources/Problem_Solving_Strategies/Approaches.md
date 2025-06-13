# 解題思路、觀念與想法

本文件收集各種解題的關鍵思路、觀念和想法，幫助更有效地解決算法問題。

## 問題模式識別

### 常見問題類型與對應技巧

- **Subarray 問題**：當遇到子數組相關問題時，應該考慮使用 **Prefix Sum** 或 **Sliding Window** 技巧
  * Prefix Sum 適合需要快速計算任意子數組和的問題
  * Sliding Window 適合尋找滿足特定條件的連續子數組 (`連續`很重要)

## 語言特定注意事項

### C++ 型別陷阱

- **型別不匹配導致的非預期結果**：不同的型別（如 int、unsigned int、long long）進行加減法可能導致非預期結果
- **溢出問題**：使用不適當的型別可能導致計算過程中出現溢出（overflow）
- **常見陷阱**：
  * 有符號與無符號整數混合運算
  * 整數除法截斷
  * 陣列索引使用錯誤型別（如使用 int 而非 size_t）
  * 比較不同型別的值

## 1. 使用不同的視角切入題目

有時候，重新表述或轉換問題的角度可以讓難題變得更容易解決。通過改變我們看待問題的方式，可以發現更直接的解決方案。

### 例子

**原始問題**：
```
You are given a binary string s (a string containing only "0" and "1").
You may choose up to one "0" and flip it to a "1".
What is the length of the longest substring achievable that contains only "1"?

For example, given s = "1101100111", the answer is 5.
If you perform the flip at index 2, the string becomes 1111100111.
```

**轉換視角**：
此問題可轉成 `what is the longest substring that contains at most one "0"?"`

通過這種轉換，我們可以使用 **Sliding Window** 技術來解決問題，維護一個最多包含一個"0"的窗口，並找出最長的這樣的窗口。

## 2. 練習心法：設計 test case 很重要！！！

解題時遵循結構化的思考過程可以幫助我們更系統地解決問題，而設計良好的測試用例是確保解決方案正確性的關鍵。

### 思路步驟

1. **OBSERVATION**
   - 仔細觀察問題，理解問題的本質和特點
   - 尋找問題中的模式、規律或特殊情況
   - 注意回傳值的定義

2. **BRUTE FORCE + 時間分析**
   - 首先考慮最直接的解決方案
   - 分析暴力解法的時間和空間複雜度
   - 識別可能的瓶頸和優化機會

3. **使用技巧優化, 指出實作重點**
   - 應用適當的算法技巧（如 **Sliding Window**、**Prefix Sum**、**Two Pointers** 等）來優化解決方案
   - 強調實現中的關鍵點和潛在的陷阱
   - 考慮邊界情況和特殊輸入

4. **使用 test case 確認**
   - **TEST CASE 是你的守護神**
   - 設計多樣化的測試用例，包括：
     * 基本/簡單情況
     * 邊界情況（空輸入、最小/最大值等）
     * 特殊情況（重複元素、排序/未排序等）
   - 使用測試用例驗證解決方案的正確性
   - 通過測試用例找出並修復潛在問題