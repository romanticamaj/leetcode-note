# C++ Priority Queue (Heap) 貪心策略通用模板

這份模板總結了使用 `std::priority_queue` 來解決演算法問題的常見模式，特別適用於貪心 (Greedy) 策略。當問題可以被簡化為「重複地從一組元素中選取最大或最小值並進行處理」時，這個模板就能派上用場。

常見應用場景：

- **Top-K 問題**: 尋找第 K 大/小的元素，或頻率最高的前 K 個元素。
- **模擬/Greedy 選擇**: 在每一步都做出局部最優選擇，例如合併成本最小的物件、處理最緊急的任務等。
- **動態維護有序集合**: 當需要一個能高效插入元素並隨時取得極值的資料結構時。

---

## 模板結構

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <numeric>
#include <unordered_map>
#include <functional>

class SolutionTemplate {
public:
    // 根據題目需求調整回傳型別和參數
    ReturnType solve(vector<DataType>& data, OtherParams params) {

        // =================================================================
        // 區塊 1: 前處理與 Priority Queue 初始化 (Preprocessing & Initialization)
        // =================================================================
        // 根據問題特性，選擇最合適的初始化方式。

        // 方式 A: 直接從輸入資料建構 (Build from input data)
        // - Max Heap (預設): 每次都能取得最大值
        std::priority_queue<ValueType> maxHeap(begin(data), end(data)); // O(n)

        // - Min Heap: 每次都能取得最小值
        std::priority_queue<ValueType, std::vector<ValueType>, std::greater<ValueType>> minHeap(begin(data), end(data)); // O(n)

        // 方式 B: 頻率計數後再建構 (Build from frequency count)
        // 當處理的對象是元素的出現次數時使用。
        std::unordered_map<KeyType, int> counts;
        for (const auto& item : data) { // O(n)
            counts[item]++;
        }
        // 將計數結果放入 Priority Queue
        // 注意：這裡通常是空的 heap，在迴圈中逐一加入
        std::priority_queue<pair<int, KeyType>> freqHeap; // <頻率, 元素>
        for (const auto& [key, count] : counts) { // O(U), U 是唯一元素數量
            freqHeap.push({count, key}); // O(logU)
        }

        // 方式 C: 空的 Priority Queue，在迴圈中動態加入
        std::priority_queue<ValueType> emptyHeap;

        // 方式 D: 雙 Heap 初始化 (Two-Heap Initialization)
        // 當需要根據不同條件在兩組元素間移動時使用。
        // 通常一個 Heap 預先填入所有資料，另一個則為空，等待在主迴圈中接收符合條件的元素。
        std::priority_queue<ValueType, std::vector<ValueType>, std::greater<ValueType>> sourceHeap; // e.g., Min-heap by capital
        std::priority_queue<ValueType> destinationHeap; // e.g., Max-heap by profit
        for (const auto& item : data) { // O(n)
            sourceHeap.push(item); // O(logN)
        }


        // =================================================================
        // 區塊 2: 主處理迴圈 (Main Processing Loop)
        // =================================================================
        // 根據問題的終止條件選擇合適的迴圈。

        // 條件 A: 處理固定次數 (e.g., k 次操作)
        while (k > 0 && !heap.empty()) {
            // ... 執行核心邏輯 ...
            k--;
        }
        // 另一種寫法：將次數檢查與容器是否為空分開
        while (k > 0) {
            if (heap.empty()) break;
            // ... 執行核心邏輯 ...
            k--;
        }

        // 條件 B: 直到 Heap 中元素少於某個數量 (e.g., 合併問題)
        while (heap.size() > 1) {
            // ... 執行核心邏輯 ...
        }

        // 條件 C: 滿足某個累計條件 (e.g., 總和、總權重)
        ValueType accumulatedValue = 0;
        while (!heap.empty() && some_condition(accumulatedValue, heap.top())) {
            // ... 執行核心邏輯 ...
        }

        // 條件 D: 處理 Heap 內所有元素
        while (!heap.empty()) {
            // ... 執行核心邏輯 ...
        }


        // =================================================================
        // 區塊 3: 核心操作 (Core Heap Operation)
        // =================================================================
        // 在迴圈內部，根據貪心策略取出頂部元素並處理。

        // 操作 A: 取出極值 (Get min/max element)
        ValueType topElement = heap.top();
        heap.pop(); // O(logN)

        // (可選) 取出第二個極值
        ValueType secondTopElement = heap.top();
        heap.pop(); // O(logN)

        // 操作 B: 處理元素並將結果放回 (Process and push back)
        // 例如：石頭相撞、合併木棍、扣除石頭
        ValueType result = process(topElement, secondTopElement);
        if (is_valid(result)) {
            heap.push(result); // O(logN)
        }

        // 操作 C: 固定大小 Heap (Fixed-size heap for Top-K)
        // 維護一個大小為 k 的 heap，不斷淘汰不符合條件的元素。
        // 假設要找 Top-K 大的元素，會用一個 Min Heap
        minHeap.push(new_element); // O(logK)
        if (minHeap.size() > k) {
            minHeap.pop(); // O(logK), 移除當前最小的，留下較大的
        }

        // 操作 D: 累計結果 (Accumulate results)
        // 將取出的元素值累加到最終結果中。
        finalResult += topElement;

        // 操作 E: 雙 Heap 協作 (Two-Heap Strategy)
        // 用於需要將元素分為兩組並快速找到兩組邊界值的場景。
        // 典型應用：
        // 1. 動態找中位數 (MedianFinder): 一個 Max Heap 存較小的一半數字，一個 Min Heap 存較大的一半。
        // 2. 條件式選擇 (Conditional Selection): 一個 Min Heap 根據成本排序，一個 Max Heap 根據收益排序。
        // 範例：從 minCapitalHeap 中將所有 "負擔得起" 的項目，移到 maxProfitHeap 中，再從中選取利潤最高的。
        while (!minCapitalHeap.empty() && minCapitalHeap.top().capital <= current_w) {
            auto project = minCapitalHeap.top();
            minCapitalHeap.pop();
            maxProfitHeap.push(project); // O(logN)
        }
        if (!maxProfitHeap.empty()) {
            // ... 選擇利潤最高的項目 ...
        }


        // =================================================================
        // 區塊 4: 後處理與回傳結果 (Post-processing & Return Result)
        // =================================================================
        // 迴圈結束後，根據題目要求整理並回傳答案。

        // 結果 A: Heap 的頂部元素
        if (heap.empty()) return defaultValue;
        return heap.top();

        // 結果 B: Heap 的大小
        return heap.size();

        // 結果 C: 累計的變數
        return accumulatedValue;

        // 結果 D: 將 Heap 中剩餘元素轉換為 vector
        std::vector<ValueType> resultArray;
        while (!heap.empty()) {
            resultArray.push_back(heap.top());
            heap.pop();
        }
        // (可選) 如果需要，對結果進行排序
        // std::sort(begin(resultArray), end(resultArray));
        return resultArray;
    }
};
```
