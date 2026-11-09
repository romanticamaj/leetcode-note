# 正負貢獻計數（Signed Contribution Counting）解題心法

**難度：⭐⭐⭐｜技巧摘要：Signed Contribution Counting｜範例相容 C++14。**
本篇使用這個描述性名稱，指把兩種相反類別編成 +1／-1，以淨差保存查詢所需資訊；不是宣稱所有教材都使用同一術語。

## 🧠 核心哲學：先問要判斷什麼，再決定要保存多少

LC 348. Design Tic-Tac-Toe 的原始設計為每條線維護兩份摘要：**落子總數＋出現過的玩家 bitmask**。
判斷 `count == n && mask == (1 << player)`，可以知道該線已滿，而且全屬同一玩家。

但題目只問是否有人占滿一條線，不要求回報兩位玩家各下幾格。可以將這兩個判斷合併成一個極值條件：

```text
玩家 1：每次 +1
玩家 2：每次 -1
lineSum = 玩家 1 的格數 − 玩家 2 的格數

lineSum ==  n → 玩家 1 占滿
lineSum == -n → 玩家 2 占滿
```

**不是把所有資訊無損壓成一個數，而是只保留足以回答目標問題的資訊。**
少一份需要同步更新的狀態，就少一種 count 已更新、mask 卻漏改或改錯範圍的機會。

## 1. 為什麼 ±n 足以證明占滿？

令 a、b 為兩位玩家在某條線上的格數。合法落子不重複，該線至多 n 格：

```text
a >= 0，b >= 0，a+b <= n
sum = a-b
```

如果 `a-b == n`，則 `n = a-b <= a+b <= n`，迫使 `a+b == n` 且 `b == 0`，所以 `a == n`。
反方向 `sum == -n` 對稱成立。**能判定的不只是正負，而是達到容量上界的極值。**

例如容量 n=3：

| 格子內容 | sum | 能否判定占滿？ |
|:---|:---:|:---|
| 1、1、空 | 2 | 否，尚未滿 |
| 1、1、2 | 1 | 否，兩位混合 |
| 1、1、1 | 3 | 是，玩家 1 |
| 2、2、2 | -3 | 是，玩家 2 |

## 2. 🧩 一個實作模板：每條線只存 signed sum

```cpp
#include <vector>

class TicTacToe {
    int n;
    std::vector<int> rows, cols;
    int diagonal = 0, antiDiagonal = 0;

public:
    explicit TicTacToe(int n) : n(n), rows(n, 0), cols(n, 0) {}

    int move(int row, int col, int player) {
        const int delta = player == 1 ? 1 : -1;
        rows[row] += delta;
        cols[col] += delta;
        if (row == col) diagonal += delta;
        if (row + col == n - 1) antiDiagonal += delta;

        const int winningSum = delta * n;
        if (rows[row] == winningSum || cols[col] == winningSum ||
            diagonal == winningSum || antiDiagonal == winningSum) {
            return player;
        }
        return 0;
    }
};
```

前提沿用題目保證：合法空格落子、player 為 1 或 2、有人獲勝後不再呼叫 move。

| 口訣 | 動作 |
|:---|:---|
| 先編正負 | 玩家映射成 +1／-1 |
| 只改相關線 | 一行、一列，以及確實經過的對角線 |
| 看有沒有滿幅 | 該玩家的 winningSum 為 delta*n |

**Invariant**：每條線的 sum 永遠等於其玩家 1 格數減玩家 2 格數。初始化全零；每次只對包含落子的線加 delta，保持此性質；達到 ±n 時由容量證明推出勝利。

兩個對角線條件是各自的 if，不能寫成 else if：奇數棋盤中心同時屬於兩條對角線，n=1 也同時成立。

## 3. 何時值得想到正負貢獻？

- 有兩類方向相反的事件／貢獻，而且答案只依賴它們的**差值**。
- 原本維護多份統計，只是為了判斷平衡、淨增加、領先或達到已知極值。
- 已有約束能證明摘要充分，例如「每條線最多 n 個合法落子」。

這與 [Running State](../Prefix_Sum/02_Running_State_Pattern.md) 相容：淨差可以逐步更新；也可與 prefix sum 結合，尋找兩類數量相等的區間。但區間查詢還需要歷史位置或頻率，不能只留目前一個 sum。

## ⚠️ 省掉資訊前，要知道什麼問題從此答不出來

- `sum == 0` 可能是空線，也可能雙方各一格；**淨差不能還原總數或每人的數量**。
- `sum > 0` 只表示玩家 1 較多，不代表占滿；勝利看 ±n。
- 沒有容量上界或允許同格重複累加時，±n 不足以證明整條線被占滿。
- 三個以上類別、不同權重或更複雜查詢，不能直接照搬兩類抵消的表示。
- 合併狀態沒有消除成員條件；非對角線落子仍不能更新 diagonal。
- 本方法沒有棋盤，無法自行驗證該格是否已被占用；若介面要求驗證，須另保留所需資料。

## ⏱️ 複雜度與面試話術

建構 O(n)，每次 move O(1)，額外空間 O(n)。與 count＋bitmask 版漸近複雜度相同；改善的是狀態數、更新成本與可讀性。

「我用 +1／-1 表示兩位玩家的貢獻，每條線只維護淨差。由於一條線最多 n 格，淨差達到 ±n 就只能是同一玩家占滿，因此不需要另外維護總數與玩家集合。」

這是 [Correct by Construction](Correct_by_Construction.md) 的狀態設計實例：讓較少的欄位直接承載判定依據，減少靠記憶維持一致的工作。
