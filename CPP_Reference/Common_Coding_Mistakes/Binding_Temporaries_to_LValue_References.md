# C++ 陷阱：非 const 左值引用無法綁定到臨時物件

這是一個在 C++ 中非常經典且常見的編譯錯誤，它根植於 C++ 對於左值 (l-value) 和右值 (r-value) 的嚴格區分，以及為了防止意外修改臨時物件而設立的安全機制。

## tl;dr

- **錯誤**：你不能將一個臨時產生的值（例如 `"{}"`、`vector<int>{1, 2}` 或函式返回的物件）傳遞給一個型別為 `T&`（非 `const` 左值引用）的函式參數。
- **原因**：`T&` 意味著「我需要一個具名的、可被修改的物件」。而臨時值是匿名的、即將被銷毀的，修改它通常是無意義且危險的。
- **解法**：
  1. **創建一個具名變數**，然後將該變數傳入。這是最直接的解決方案。
  2. 如果函式**不需要修改**傳入的物件，將參數型別改為 `const T&`。
  3. 如果**確實需要一份副本**，將參數型別改為傳值 `T`。

---

## 錯誤重現

讓我們分析一個在回溯法中常見的例子：

```cpp
class Solution {
public:
    vector<vector<int>> permutations;

    void permuteHelper(unordered_set<int>& current, unordered_set<int>& left) {
        // ... 函式內部會修改 current 和 left ...
    }

    vector<vector<int>> permute(vector<int>& nums) {
        // 試圖將一個臨時物件 {} 傳遞給一個 T& 參數
        permuteHelper({}, unordered_set<int>(begin(nums), end(nums))); // ❌ COMPILE ERROR
        return permutations;
    }
};
```

編譯器會給出類似以下的錯誤訊息：

> non-const lvalue reference to type 'unordered_set<int>' cannot bind to an initializer list temporary

### 錯誤解析

- **`unordered_set<int>& current`**：函式 `permuteHelper` 的第一個參數是一個**非 const 的左值引用**。它期望得到一個具體的、可以被修改的 `unordered_set` 物件。
- **`{}`**：在呼叫點，`{}` 是一個初始化列表，它會創建一個**臨時的、匿名的 `unordered_set` 物件**。這個物件是一個**右值 (r-value)**。
- **核心衝突**：C++ 語言規則禁止將一個右值（臨時物件）綁定到一個非 const 的左值引用上。

---

## 為什麼會有這個規則？左值 (l-value) vs. 右值 (r-value)

- **左值 (l-value)**：可以把它想像成**有名字、有固定記憶體位置**的物件。你可以對它取址 (`&`)。例如：`int x = 10;`，`x` 就是一個左值。
- **右值 (r-value)**：通常是**沒有名字、即將被銷毀的臨時值**。例如：`10`、`x + 5` 的計算結果、`MyObject()` 創建的臨時物件。

**黃金法則**：`T&` 只能綁定到 `T` 型別的左值。

**背後的原因：安全性**
想像一下如果 C++ 允許這樣做：

```cpp
void modify(int& val) { val = 100; }
modify(5); // 假設這可以通過編譯
```

`modify` 函式試圖修改 `5` 這個臨時值。這個修改是沒有意義的，因為 `5` 這個臨時值在 `modify(5);` 這行程式碼結束後就消失了。函式內部的修改會被立即丟棄，這幾乎可以肯定是程式設計師不想要的結果。為了防止這種邏輯錯誤，C++ 編譯器直接禁止了這種行為。

---

## 如何修正

### 解決方案一：創建具名變數 (最推薦)

這是最清晰、最能表達意圖的修正方式。既然函式需要一個可以修改的物件，我們就創建一個給它。

```cpp
vector<vector<int>> permute(vector<int>& nums) {
    // 創建具名的、持久的物件
    unordered_set<int> current_permutation;
    unordered_set<int> remaining_elements(begin(nums), end(nums));

    // 將這些具名物件（左值）傳入
    permuteHelper(current_permutation, remaining_elements);

    return permutations;
}
```

### 解決方案二：修改函式簽名

#### A. 使用 `const` 引用 (`const T&`)

- **作法**：將參數改為 `const unordered_set<int>& current`。
- **可行性**：**可以通過編譯**。C++ 允許將臨時物件綁定到 `const` 左值引用，並會延長該臨時物件的生命週期到引用的生命週期結束。
- **問題**：在這個特定的回溯問題中，`permuteHelper` **需要修改** `current`。將其改為 `const` 會導致函式內部無法編譯。因此，這個選項**不適用於此場景**，但對於那些只需要讀取、不需要修改的函式來說，這是一個很好的選擇。

#### B. 使用傳值 (`T`)

- **作法**：將參數改為 `unordered_set<int> current`。
- **可行性**：**可以通過編譯**。`{}` 會被用來初始化一個新的 `unordered_set` 物件，這個物件是 `permuteHelper` 函式的局部變數。
- **問題**：這違背了使用引用來避免複製的初衷，會導致效能下降，尤其是在遞迴中。

## 總結心法

當你遇到「non-const lvalue reference cannot bind to temporary」這個錯誤時，問自己一個問題：

> 「這個函式是否需要**修改**我傳入的物件，並讓這個修改在函式外部也**可見**？」

- 如果答案是**是**，那麼你就必須提供一個**具名的、非臨時的物件**（解決方案一）。
- 如果答案是**否**（函式只是讀取），那麼將函式參數改為 `const T&` 是更好的設計。
