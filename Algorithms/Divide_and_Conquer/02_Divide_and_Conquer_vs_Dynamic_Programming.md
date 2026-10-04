# Divide and Conquer vs Dynamic Programming 比較分析

## 🧠 核心差異：看子問題是否重複，不只看大小怎麼變

兩者都透過子問題的解計算當前答案。典型分治把工作分成互不重疊的子問題，各自求解再 combine；DP 則**定義可重用的狀態，保存其答案，避免同一個子問題被反覆計算**。

判斷時先問：「這些呼叫是否在求同一個狀態的答案？」`n/2` 或 `n-1` 描述的是規模變化，不能單獨決定演算法分類。

## 1. 🧩 子問題重疊性：遞迴樹還是共享狀態圖？

### Divide and Conquer：分解後各自求解

```cpp
// 半開區間 [left, right)，merge 的實作省略
void mergeSort(vector<int>& a, int left, int right) {
    if (right - left <= 1) return;
    int mid = left + (right - left) / 2;
    mergeSort(a, left, mid);
    mergeSort(a, mid, right);
    merge(a, left, mid, right);
}
```

兩段可能長度相同，但輸入區間不同，因此是不同子問題。每個區間在這次遞迴中只需求解一次，沒有用記憶化重用答案的必要。

### Dynamic Programming：同一狀態只計算一次

```cpp
// memo 初值為 -1；示意小 n，忽略數值溢位
int fibDP(int n, vector<int>& memo) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    return memo[n] = fibDP(n - 1, memo) + fibDP(n - 2, memo);
}
```

未記憶化時，`fib(n-2)` 會由不同路徑被重複呼叫。DP 把它們視為同一個狀態，計算一次後重用結果。

## 2. 🧩 查表的重點：狀態定義與依賴順序

把 DP 理解成「查表」很實用，但**表格不要求只能往前查固定距離，也不限一維或二維**。重點是索引能完整表示子問題，而且被依賴的答案已經算好。

例如定義 `F(0) = F(1) = 1`，對 `i >= 2` 有 `F(i) = F(i/2) + F(i/3)`，其中除法取整數商：

```cpp
vector<long long> dp(n + 1, 1); // 示意小 n，忽略數值溢位
for (int i = 2; i <= n; ++i)
    dp[i] = dp[i / 2] + dp[i / 3];
```

這仍是合法的 DP：`i/2`、`i/3` 都小於 `i`，從小到大填表即可；若用遞迴求解，相同狀態也可能重複出現。依賴不連續並不妨礙查表。

| 比較面向 | 典型 Divide and Conquer | Dynamic Programming |
|---|---|---|
| 子問題身分 | 常以輸入區間或資料子集表示 | 以足以決定答案的狀態表示 |
| 規模變化 | 常見切半，也可以不均分 | 可減一、切半，或依其他狀態轉移 |
| 答案如何使用 | 子問題各自求解後合併 | 保存狀態答案，供多個依賴者重用 |
| 計算安排 | Top-down 遞迴，也能 bottom-up 合併 | Top-down 記憶化或 bottom-up 填表 |

注意 `T(n) = 2T(n/2) + O(n)` 是**執行時間**的 recurrence；`dp[i] = dp[i-1] + dp[i-2]` 是**答案**的 recurrence。兩者描述不同事物，不宜直接拿來當分類依據。

## 3. 🧩 正確的合併關係：DP 不一定求最優解

兩者都需要證明：子問題的解足以構造當前答案。分治排序要證明 merge 能產生有序結果；DP 要證明狀態轉移涵蓋正確的選擇或計數。

**最優子結構是最佳化 DP 的重點，但 DP 也能處理計數與可行性問題。** Fibonacci、路徑計數沒有「取最優」的操作，仍可用 DP。

```cpp
// 只允許向右、向下移動的網格；假設前驅存在且邊界已初始化
minCost[i][j] = min(minCost[i - 1][j], minCost[i][j - 1]) + cost[i][j];
ways[i][j] = ways[i - 1][j] + ways[i][j - 1];
```

第一行依賴前驅的最小成本；第二行加總互不重複的兩類路徑。兩者都查表，但合併的語意不同。

## ✅ 設計時的判斷流程

1. **定義子問題**：它的答案由哪些輸入或狀態完整決定？
2. **定義依賴與合併**：需要哪些更小的解，如何推出當前答案？
3. **檢查重複**：不同路徑是否會求解同一個狀態？會，就考慮保存結果。
4. **安排計算順序**：按需遞迴並記憶化，或依依賴順序填表；獨立區段也可逐層合併。

| 問題 | 核心觀察 | 常見方法 |
|---|---|---|
| Merge Sort | 左右區間獨立，結果可合併 | Divide and Conquer |
| Quick Sort | Partition 後，兩側可各自排序 | Divide and Conquer |
| Fibonacci | 多條路徑依賴相同的 n | DP |
| 0-1 Knapsack | 相同的物品位置、剩餘容量反覆出現 | DP |
| Edit Distance | 相同的兩個前綴長度反覆出現 | DP |

口訣：**先定狀態，再看依賴；有重複就重用，按依賴安排計算順序。**

延伸閱讀：[Bottom-Up 分治框架](04_Bottom_Up_Divide_and_Conquer.md)、[分治設計策略](01_Divide_and_Conquer_Design_Strategy.md)。
