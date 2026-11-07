# C++ 技巧：使用 Lambda 與 decltype 實現自訂比較器

比較器如何回傳、判定同順位及設計多條件排序，見 [Comparator 設計心法](Comparator_Design.md)。

在 C++ 中，當我們需要為 STL 容器（如 `std::priority_queue`, `std::set`, `std::map`）提供自訂的排序邏輯時，通常會使用比較函式物件（Functor）或 Lambda。然而，Lambda 的型別是匿名的，這在模板編程中帶來了一個挑戰。本文件將深入探討如何使用 `decltype` 關鍵字來解決這個問題。

---

## 1. 問題背景：模板型別的需求

像 `std::priority_queue` 這樣的容器，其比較邏輯是作為模板參數傳入的。這意味著在**編譯時期**，編譯器就必須知道比較器的**確切型別**。

```cpp
template<
    class T,
    class Container = std::vector<T>,
    class Compare = std::less<typename Container::value_type> // <-- 這裡需要一個型別
> class priority_queue;
```

## 2. 傳統作法：自訂 Functor (函式物件)

在 C++11 之前，最常見的作法是定義一個結構體（struct）並重載 `operator()`，使其行為像一個函式。

```cpp
struct MyComparator {
    bool operator()(const int& a, const int& b) const {
        return a > b; // 實現 Min-Heap
    }
};

// 使用時，可以直接將型別傳入模板
std::priority_queue<int, std::vector<int>, MyComparator> pq;
```

這種方法清晰易懂，因為 `MyComparator` 是一個明確的型別名稱。

---

## 3. 現代作法：Lambda 與 `decltype` 的結合

C++11 引入的 Lambda 運算式提供了更簡潔的語法，但它帶來一個新問題：**Lambda 的型別是匿名的**，由編譯器在內部生成，我們無法直接寫出它的型別名稱。

這就是 `decltype` (declare type) 發揮作用的地方。`decltype` 是一個在編譯時期推導表達式型別的運算子。

### 運作原理

1. **定義 Lambda**：我們先定義一個 Lambda 物件。

   ```cpp
   auto cmp = [](const int& a, const int& b) {
       return a > b;
   };
   ```

2. **推導型別**：使用 `decltype(cmp)` 來取得這個 Lambda 的唯一、匿名的型別。
3. **傳入模板**：將這個推導出來的型別作為模板參數傳給容器。
4. **傳入物件**：在創建容器物件時，將 Lambda **物件本身** (`cmp`) 傳入建構函式。

### 完整範例：`std::priority_queue`

```cpp
#include <queue>
#include <vector>
#include <iostream>

int main() {
    // 1. 定義 Lambda 比較邏輯
    auto cmp = [](int left, int right) {
        // 實現 Min-Heap
        return left > right;
    };

    // 2. 使用 decltype 推導 Lambda 的型別，並作為模板參數
    std::priority_queue<
        int,
        std::vector<int>,
        decltype(cmp) // <-- 在這裡傳入型別
    > minHeap(cmp);   // <-- 在這裡傳入物件

    minHeap.push(3);
    minHeap.push(1);
    minHeap.push(4);

    // 輸出 1
    std::cout << "Min-Heap top: " << minHeap.top() << std::endl;

    return 0;
}
```

### 為什麼需要傳入物件？

- **模板參數 (`decltype(cmp)`)**：告訴 `priority_queue` 類別：「我將會使用一個這種型別的比較器」。這讓類別知道該如何儲存比較器，以及它的 `operator()` 長什麼樣子。
- **建構函式參數 (`cmp`)**：實際創建 `priority_queue` 物件時，需要一個比較器物件的實例來進行比較操作。對於無捕獲（stateless）的 Lambda，編譯器通常能最佳化掉這個物件的儲存，但語法上仍需提供。

---

## 總結

| 方法                    | 優點                               | 缺點                                                     |
| :---------------------- | :--------------------------------- | :------------------------------------------------------- |
| **Functor**             | 型別明確，語法直觀，相容舊版 C++。 | 程式碼較為冗長，需要定義一個完整的 struct。              |
| **Lambda + `decltype`** | 語法簡潔，邏輯與實作緊密結合。     | 需要理解 `decltype` 的概念，建構時需同時傳入型別和物件。 |

在現代 C++ 中，Lambda 搭配 `decltype` 是實現自訂比較器（尤其是在函式內部臨時定義時）的靈活且強大的標準作法。
