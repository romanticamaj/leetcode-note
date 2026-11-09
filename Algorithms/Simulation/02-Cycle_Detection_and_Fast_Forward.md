# 狀態循環與快速跳躍（Cycle Detection + Fast Forwarding）解題心法

**難度：⭐⭐⭐｜技巧：Simulation + Cycle Detection + Fast Forwarding｜程式相容 C++14。**

以 LC 957. Prison Cells After N Days 為例：狀態轉移容易寫，真正要省的是重複執行的輪數。

## 🧠 從 BUD 的 Duplicate，看到「整段未來重播」

先寫正確的一步模擬，再問：**狀態是否會重複？同一狀態會不會產生相同的下一步？**

這是 [BUD Optimization](../../Interview_Playbook/Problem_Solving_Strategies.md#bud-optimization) 的 D（Duplicated work）：重複的不一定是某個計算式，也可能是整段狀態序列。

```text
一般逐步模擬：做 N 次相同規則的轉移
發現循環之後：先走到重複點 → 跳過完整圈數 → 只模擬餘數
```

Memoization 可省掉同一子問題的重算；這裡更利用「一個狀態只通往唯一的下一個狀態」，直接跳過一整段重播。

## 1. 成立前提：有限狀態＋確定性轉移

設狀態序列為 `x[t+1] = F(x[t])`。如果 `x[a] == x[b]`，且 F 不隨外部條件改變：

```text
x[a+1] = F(x[a]) = F(x[b]) = x[b+1]
```

反覆套用便知之後全部相同，週期為 `λ = b-a`。沿同一次確定性演化，只會先經過一段前置狀態，再進入一個循環，不必另找越來越大的循環。

```text
前置：X → Y → A → B → C → A → B → C → …
             ↑           ↑
           第 a 步      第 b 步；λ = b-a
```

有限狀態保證持續走下去終將重複；**單看數量相同、位置相同或某個欄位相同，不能保證未來相同**。
若 F 取決於指令位置、方向或時間階段，這些也必須納入狀態；不能只記畫面。

## 2. 時間標記：狀態屬於哪一天？

固定一個定義：**第 0 天是輸入；做完一次 F 才是第 1 天。**
`firstDay[state]` 保存該完整狀態第一次出現的「已執行天數」，查重在下一次轉移之前進行。

| 資訊 | 定義 |
|:---|:---|
| `day` | 已執行幾天；目前 state 就是 x[day] |
| `days` | 固定的目標天數，不隨跳躍改寫 |
| `period` | `day - firstDay[state]`，必須大於 0 |
| `remaining` | `days-day`，還要前進多少天 |

目前狀態每走 period 天會回到自己，所以只需再走 `remaining % period` 天。**取餘的是剩餘天數，不是無條件對原始 N 取餘**，因為初始狀態可能在循環外。

例如第 5 天重遇第 2 天狀態，週期為 3；目標第 100 天，只需從目前狀態再走 `(100-5)%3 = 2` 天。

## 3. 🧩 一個模板：找到重複後，只模擬餘數並回傳

```cpp
#include <unordered_map>

template<class State, class Step>
State fastForward(State state, long long days, Step step) {
    std::unordered_map<State, long long> firstDay;
    long long day = 0;

    while (day < days) {
        auto it = firstDay.find(state);
        if (it != firstDay.end()) {
            const long long period = day - it->second;
            long long remaining = (days - day) % period;
            while (remaining > 0) {
                state = step(state);
                --remaining;
            }
            return state;
        }

        firstDay.emplace(state, day);
        state = step(state);
        ++day;
    }
    return state;
}
```

State 必須可比較且有 hash，key 應保存值；例如整數或完整字串，不是只存一個可能碰撞的 hash 數字。`step` 必須符合確定性轉移契約。

| 口訣 | 動作 |
|:---|:---|
| 先查現在 | state 對應 day，先判斷是否見過 |
| 沒見過才記 | 保存首次出現日，再前進一天 |
| 見過算圈長 | 現在的 day 減去首次出現日 |
| 整圈省掉 | 剩餘天數取餘，只模擬餘數後回傳 |

**Invariant／正確性**：查重前 state=x[day]，map 記錄此前各狀態的首次出現日；單步 F 維持此性質。遇到重複後，確定性保證每個完整週期回到原狀態，因此省略完整圈數不改變最終結果。

## 4. 表示法是另一個選擇：957 的 bitmask

**循環偵測不必用 bitmask，bitmask 也不必搭配循環。** 前者減少轉移次數，後者讓狀態表示、比較與轉移更便宜。

957 每格只有 0／1，因此可用第 i 個 bit 表示 `cells[i]`；8 格用一個整數即可：

```cpp
unsigned mask = 0;
for (int i = 0; i < 8; ++i) mask |= unsigned(cells[i]) << i;
// 還原第 i 格：(mask >> i) & 1u
```

初始最多有 2^8 種狀態；第一天後兩端固定為 0，只有 2^6=64 種。**保留完整 8-bit 編碼**，避免忽略初始端點對第一天內部格子的影響。
字串 key 也能正確偵測循環；改整數 key 省的是編碼／hash／儲存成本，不是循環成立的原因。

每個內部格子的下一天是「左右相等為 1」，可進一步改寫為 XOR 後取反；若定義 bit i 對應 cells[i]：

```cpp
unsigned nextMask = ~((mask << 1) ^ (mask >> 1)) & 0x7Eu;
// 0x7E = 01111110：只保留中間六格，兩端必為 0。
```

先確認每個 bit 的語義，再用位元運算批次計算；不要只因「狀態數少」就直接猜移位公式。見 [Bitmask 狀態壓縮](../Bit_Manipulation/03-State_Compression.md)。

## ⚠️ 陷阱與適用邊界

- 同步更新要讀舊值、寫新值；swap 後 next 是舊 buffer，每輪仍須覆寫所有輸出格，包含兩端。
- 保存「已執行日」或「剩餘日」都可算差，但不要跳躍後混用時間基準；本模板首次查重後直接處理餘數，不再更新 map。
- 跳到目標只適合直接求最終狀態；若求累積分數，要另算每圈貢獻；若輸出每一步，不能省掉必要的輸出成本。
- Floyd 也能偵測循環，但還需處理前置長度與週期；先掌握可直接查時間標記的 map 模板，不在此另背一套。

## ⏱️ 複雜度與面試話術

令 S 為可達狀態數、C 為單步成本、H 為一次 key hash／複製／比較成本，map 採平均查找分析：時間 `O(min(N,S)·(C+H))`；狀態長度 B 時，空間 `O(min(N,S)·B)`。查到循環後至多再走不足一圈，不改變此界。
957 固定 8 格，S 至多是初始狀態加 64 種後續狀態，單步與編碼也是常數，故時間、額外空間對 N 均為 O(1)。不要將此結論直接套到可變長度的 board。

「我先做一步模擬，再以完整狀態保存首次出現時間。相同狀態的未來確定相同，因此以兩次出現的時間差取得週期，將剩餘步數取餘，跳過整圈。」
