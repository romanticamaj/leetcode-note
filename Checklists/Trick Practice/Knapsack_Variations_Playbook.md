# 🎒 0/1 Knapsack 變形題整理

0/1 背包問題是所有 DP 的基石之一。這類題目的核心是「每個物品只能選一次 (0 或 1)」，透過狀態設計來追蹤「前 i 個物品」在「某個限制下」能達成的最優解。

---

## 🎯 終極目標題

- LC 879. Profitable Schemes (雙限制 + 變形)
- LC 956. Tallest Billboard (狀態設計極致)
- LC 1751. Maximum Number of Events That Can Be Attended II (區間 + 背包)

---

## 🧪 練習路徑

### ✅ 推薦學習順序

#### 1. **核心概念理解**

**關鍵技巧：**

- **狀態定義**: `dp[i][w]` = 前 `i` 個物品，容量 `w` 下的最大價值
- **轉移方程**: `dp[i][w] = max(dp[i-1][w], dp[i-1][w - weight[i]] + value[i])`
- **空間優化**: 1D Array (Rolling Array)，內層迴圈必須 **倒序遍歷** 避免重複選取

**Archetype Problem (原型問題):**

- 📙 **LC 494. Target Sum** ← 最純粹的 0/1 背包 Counting DP
  - **為何是原型**: 這題體現了最核心的背包思想：透過數學轉化 `(Sum + Target) / 2`，將問題變成「湊出特定和的方法數」
  - **練習重點**: 理解如何從「加減符號分配」轉化為「子集和計數」

#### 2. **標準 0/1 背包應用**

這些題目是背包的直接應用，必須練到「看到題目能直接反應出背包模型」。

- 📙 **LC 416. Partition Equal Subset Sum** (⭐⭐⭐ 經典判定題)
  - **轉化**: 背包容量 = `sum / 2`，物品價值 = 物品重量 = `nums[i]`
  - **目標**: Boolean DP - 能否填滿背包
  - **與 LC 494 的關係**: LC 494 問「有幾種方法」，LC 416 問「是否可行」

- 📙 **LC 1049. Last Stone Weight II** (⭐⭐ 最小差值)
  - **轉化**: 將石頭分成兩堆，使差值最小
  - **本質**: 和 LC 416 相同，都是在找「最接近 sum/2 的子集和」

#### 3. **多維度費用背包**

背包不只有「容量」一個限制，可能有多個維度的約束。

- 📙 **LC 474. Ones and Zeroes** (⭐⭐ 二維費用)
  - **狀態**: `dp[i][j]` = i 個 0 和 j 個 1 能組成的最大字串數
  - **練習重點**: 理解如何處理多個維度的限制

#### 4. **進階應用 (Hard 挑戰)**

Hard 題通常將背包作為子問題，或加上特殊的狀態定義。

- 📕 **LC 879. Profitable Schemes** (⭐⭐⭐ 雙限制 + at least 語義)
  - **特點**: LC 474 的進階版
  - **難點**: 處理「至少 (at least)」利潤的狀態定義
    - `dp[k]` 通常代表「恰好」利潤 k
    - 這題需要 `k` 代表 `minProfit`，超過的部分都算在 `dp[minProfit]` 裡
  - **前置技能**: 必須先理解 LC 474 的雙維度費用

- 📕 **LC 956. Tallest Billboard** (⭐⭐⭐⭐ 狀態設計)
  - **特點**: LC 1049 的 Hard 版
  - **難點**: 狀態不能只存一邊的高度，要存「高度差」
    - `dp[diff]` = 差值為 `diff` 時的最大公共高度
  - **前置技能**: 必須先掌握 LC 1049 的「分兩堆最小差值」思想
  - **關鍵洞察**: 這題非常考驗對背包狀態定義的深刻理解

- 📕 **LC 1751. Maximum Number of Events That Can Be Attended II** (⭐⭐⭐ 區間 + 背包)
  - **特點**: 結合區間調度 (Interval) 和背包思想
  - **難點**: 物品有時間限制，需先排序，再配合 Binary Search 找前一個不重疊的區間
  - **前置技能**: 理解標準背包 + Binary Search + 區間處理

---

## 🧠 技巧重點

### ⭐ 判準：這個 choice 該不該進 state？

> **問：「這個 choice 會不會改變未來可用的選項？」**

| 答案 | 結果 | 例子 |
| :--- | :--- | :--- |
| **會** | 必須進 state，維度消不掉 | **0/1 背包**（494、416）：用過的物品不能再用，所以「處理到第 i 個」必須記住 |
| **不會** | 只是每輪枚舉的候選 | **完全背包**（322 Coin Change）：這輪用了 coin i，下輪還能再用，所以 `i` 不用記 |

這一句同時決定三件事：

1. **維度** — 不影響未來 → 物品/硬幣那一維直接消失，`dp[k] = min(dp[k - coins[i]] + 1)`
2. **每輪要不要全掃** — 選項集合不隨歷史改變 → 每個 state 都要枚舉全部候選
3. **能不能只存最佳值** — 不用記「靠哪個 choice 達成」，一個值就夠

⚠️ **常見錯誤**：把 choice 寫成維度，轉移卻鎖在同一個 `i`（`dp[k][i] = min(dp[k][i], dp[k-coins[i]][i] + 1)`）。這樣 `dp[k][i]` 的語意會變成「**只用第 i 種**湊出 k」——`coins=[1,2,5], amount=11` 會得到 11 而不是 3。

### 核心模式識別

當你看到以下特徵時，應該想到 0/1 背包：

1. **選或不選**: 每個元素只能用一次
2. **優化目標**: 最大/最小化某個值，或計數方法數
3. **限制條件**: 有容量、數量、成本等限制
4. **子集問題**: 從集合中選出子集達成目標

### 必備技能清單

- ✅ 能快速識別「背包容量」是什麼（可能需要數學轉化）
- ✅ 區分「判定型 DP」(Boolean) vs「計數型 DP」(Count) vs「優化型 DP」(Max/Min)
- ✅ 熟練掌握 1D 空間優化及倒序遍歷的原因
- ✅ 理解「at least」vs「exactly」在狀態定義上的差異
- ✅ 能設計抽象狀態（如 LC 956 的「高度差」）

### 常見陷阱

1. **忘記倒序遍歷**: 1D 優化時如果正序會重複選取同一物品
2. **邊界條件**: `dp[0]` 的初始化（通常 `dp[0] = 1` 或 `dp[0] = 0` 取決於題意）
3. **整數除法**: 檢查 `(sum + target) % 2 != 0` 等無解情況
4. **狀態定義錯誤**: 混淆「路徑依賴參數」和「狀態定義參數」（參考 [`State_Design/01-Essentials.md`](../../Algorithms/Dynamic_Programming/State_Design/01-Essentials.md)）

---

## 📚 相關資源

- **DP 狀態設計**: [`Algorithms/Dynamic_Programming/State_Design/01-Essentials.md`](../../Algorithms/Dynamic_Programming/State_Design/01-Essentials.md)
- **DP 框架**: [`Algorithms/Dynamic_Programming/Fundamentals/02-Problem_Solving_Framework.md`](../../Algorithms/Dynamic_Programming/Fundamentals/02-Problem_Solving_Framework.md)
- **Hard 題技巧參考**: [`Interview_Playbook/Hard_Techniques_Reference.md`](../../Interview_Playbook/Hard_Techniques_Reference.md)
