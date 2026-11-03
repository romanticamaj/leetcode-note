# 均勻亂數取樣（Uniform Random Sampling）解題心法

**核心：範圍正確不代表機率均勻。** 從 n 個元素選一個，每個索引都應有 `1/n` 的機率。

適用於 LC 380. Insert Delete GetRandom O(1) 等需要等機率選取元素的問題。

## 1. 提問：為什麼不能直接用 `rand() % n`？

`% n` 能將非負整數映射到 `[0, n-1]`，但不保證每個索引獲得相同數量的來源。

假設亂數來源等機率產生 `0～7`，希望抽出 `0～2`：

```text
原始亂數：0 1 2 3 4 5 6 7
取 % 3： 0 1 2 0 1 2 0 1
```

| 結果 | 來源 | 機率 |
| :--- | :--- | :--- |
| 0 | 0、3、6 | 3/8 |
| 1 | 1、4、7 | 3/8 |
| 2 | 2、5 | 2/8 |

8 個等機率來源不能平均分給 3 個結果，這就是 **modulo bias（取模偏差）**。
即使假設 `rand()` 本身均勻，只有來源數量 `RAND_MAX + 1` 可被 n 整除時，直接取模才均勻。

**均勻分布描述每次抽樣的機率，不保證有限次抽樣的次數完全相同。**

## 2. 說明：Rejection Sampling（拒絕採樣）

只接受 `0～5`；抽到 `6、7` 就重抽，再做 `% 3`：

```text
接受的亂數：0 1 2 3 4 5
取 % 3：   0 1 2 0 1 2
```

每個結果都有兩個來源，接受條件下的機率都是 `1/3`。重抽採相同規則，因此最終結果也均勻。

一般化：來源等機率產生 `[0, M-1]`，且 `1 <= n <= M`：

```text
limit = M - (M % n)
重抽直到 r < limit
回傳 r % n
```

`limit` 是 n 的倍數，所以每個餘數都有 `limit/n` 個來源。
這是原理示意；標準函式庫可採不同的均勻映射實作，不必假定它逐字使用此流程。

## 3. 解法：C++ `<random>` 標準用法

| 工具 | 角色 |
| :--- | :--- |
| `std::mt19937` | 有內部狀態的偽亂數引擎；以 seed 初始化，之後持續產生序列 |
| `std::random_device` | 用來提供初始化 seed；是否有非決定性來源取決於實作 |
| `std::uniform_int_distribution` | 將引擎輸出映射為指定閉區間的均勻整數分布 |

```cpp
#include <cassert>
#include <random>

class UniformIndexPicker {
public:
    int pick(int n) {
        assert(n > 0);
        // 包含兩端：[0, n-1]
        std::uniform_int_distribution<int> dist(0, n - 1);
        return dist(rng);
    }

private:
    // 引擎初始化一次，持續使用；不在每次 pick 時重設 seed
    std::mt19937 rng{std::random_device{}()};
};
```

在 RandomizedSet 中，保留同樣的 `rng` 成員，依當前 `store.size()` 建立分布，再用抽出的索引存取 vector。前提是集合非空，且大小可用所選整數型別表示。

**口訣：引擎留著用，分布定範圍，抽出值當索引。**

## 4. ⚠️ 常見陷阱

- **只換範圍，沒有證明均勻**：直接 `% n` 或浮點縮放再截斷，不能自動消除分配偏差。
- **每次呼叫都設 seed**：相同 seed 會重啟相同序列；時間 seed 可能在短時間重複。
- **固定 seed 不等於失去用途**：測試時可固定 seed 以重現結果；跨標準庫的 distribution 映射不保證相同。
- **空集合**：`[0, size-1]` 沒有合法範圍，unsigned 的 `size-1` 還可能下溢。
- **手寫來源總數溢位**：例如計算 `RAND_MAX + 1` 時，要先提升成足夠寬的型別。
- **安全用途混用**：`mt19937` 不適合密碼、token 等需要不可預測性的用途。

## 5. ⏱️ 複雜度與檢查

固定字長下，上述拒絕採樣每輪 O(1)，接受率 `limit/M > 1/2`，所以期望 O(1) 時間、O(1) 空間；重抽次數沒有固定上限，不能稱最壞 O(1)。標準 distribution 的具體引擎呼叫數由實作決定。

- [ ] 每個索引的目標機率是 `1/n`，而非只確認索引不越界。
- [ ] 知道引擎與 distribution 的分工，保留引擎狀態。
- [ ] 確認閉區間端點、非空前提與整數型別。
- [ ] 測試次數不均只是觀察；正確性依賴映射原理，不以小樣本頻率代替證明。

## 相關筆記

- [Vector O(1) 刪除與 RandomizedSet 組合](../../Data_Structures/Arrays_and_Strings/Vector_O1_Deletion_Swap_to_End.md)
- [C++ One-Liners](../../Cheatsheet/CPP_One_Liners.md)
