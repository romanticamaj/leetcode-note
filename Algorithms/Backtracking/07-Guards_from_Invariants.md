# 從 Invariant 設計 Guard（Guards from Invariants）

**先定義遞迴狀態應維持的性質，再問加入一個 choice 後如何維持它。** Guard 就是允許這次操作的條件，不必先列一堆 `if`，再試哪些組合能通過。

## 🧠 設計框架：定狀態 → 寫 Invariant → 推操作與 Guard

| 步驟 | 要回答的問題 |
|---|---|
| **1. 定狀態** | `path` 保存什麼？參數表示哪個未完成部分？ |
| **2. 寫 invariant** | 每次進入遞迴時，這些狀態必須滿足什麼性質？ |
| **3. 推操作與 guard** | 加入候選後，什麼條件能讓性質繼續成立？ |
| **4. 定收集與停止** | 何時已構成答案？何時沒有下一個選擇？ |
| **5. 還原與前進** | 返回時如何恢復狀態？每次遞迴是否朝終點前進？ |

這裡的 invariant 是**每次遞迴進入時都成立的性質**，可能描述部分解的合法性、覆蓋範圍或去重順序。它不代表每個部分解都一定能完成；合法前綴仍可能走到無解的分支。

## 1. 🧩 從一條 Invariant 推出操作條件

假設正在生成 `n` 對括號，狀態是已用的左括號數 `left`、右括號數 `right`，以及字串 `path`：

```text
Invariant：0 <= right <= left <= n
           path 有 left 個 '('、right 個 ')'，且每個前綴的右括號不多於左括號
```

從候選操作推導，而不是先猜 guard：

| 操作 | 操作後必須成立 | 推出的 guard |
|---|---|---|
| 加入 `(` | `left + 1 <= n` | `left < n` |
| 加入 `)` | `right + 1 <= left` | `right < left` |

```cpp
if (left < n) {
    path.push_back('(');
    dfs(left + 1, right, path);
    path.pop_back();
}
if (right < left) {
    path.push_back(')');
    dfs(left, right + 1, path);
    path.pop_back();
}
```

當 `path.size() == 2 * n`，由 `right <= left <= n` 可推出 `left == right == n`，因此可以收集答案。每次增加一個字元，長度有上界，也能證明遞迴終止。

**完成條件要結合題目目標與 invariant 推導**，不一定是「所有不等式取等號」。例如 subsets 的每個遞迴節點都可收集答案，卻仍能繼續向下探索。

## 2. 🧩 遞迴參數與候選範圍，也由 Invariant 決定

有些約束用 guard 表達，有些直接編進候選範圍或下一層參數，不必全部寫成 `if`。

| 想維持的性質 | 候選與下一層的設計 |
|---|---|
| 選取的索引嚴格遞增，同一元素不能重用 | 從 `start` 枚舉 `i`，下一層傳 `i + 1` |
| 選取的索引非遞減，同一元素可重用 | 從 `start` 枚舉 `i`，下一層傳 `i` |
| 排列中，每個輸入位置最多使用一次 | 每層枚舉全部索引，用 `!used[i]` 篩選 |
| 切出的合法段落恰好覆蓋 `s[0:start)` | 枚舉 `[start, end)`，下一層傳 `end` |
ㄣ
`i + 1` 表示下一層的候選下界，不代表每次選擇必定只前進一格；本層可能選到任意 `i >= start`。切段則由此次 choice 的結尾決定下一段起點。

```cpp
// path 串接後恰好等於 s[0:start)，且每段皆合法
for (int end = start + 1; end <= s.size(); ++end) {
    if (!legal(s, start, end)) continue;
    path.push_back(s.substr(start, end - start));
    dfs(end, path); // 保持連續覆蓋，不留洞也不重疊
    path.pop_back();
}
```

去重也要守住完整性：組合可固定索引順序，排列卻必須保留不同順序。額外限制必須只刪除重複生成路徑，不能刪除不同的合法答案。

## 3. 🧩 把框架落到遞迴流程

```cpp
void backtrack(State& st, Path& path) {
    // 契約：進入時 invariant 成立；返回時恢復呼叫前的狀態
    if (isAnswer(st, path)) collect(path);
    if (noMoreChoices(st)) return;
    for (const auto& c : candidates(st)) {
        if (!allowed(st, c)) continue; // 推導加入 c 的合法條件
        apply(st, path, c);
        backtrack(st, path);
        undo(st, path, c);
    }
}
```

`isAnswer` 與 `noMoreChoices` 可以重合，也可以不同。`allowed` 保證子呼叫符合 invariant；`undo` 讓下一個分支回到相同起點。某些「必定無法完成」的分支還能提前剪掉，但須另外證明不會漏解。

## ⚠️ 常見陷阱

- **只寫合法性，忘記狀態關係**：例如 palindrome partitioning 除了每段是回文，還要保證各段連續覆蓋已處理前綴。
- **把合法當成必有解**：局部條件成立不一定能延伸到完整答案，搜尋仍可能失敗。
- **把收集答案等同停止搜尋**：subsets 可在每層收集後繼續；括號生成達到完整長度後則停止。
- **去重限制刪掉不同答案**：排列不能套用組合的索引遞增限制。
- **沒有進展**：允許重用同一索引時，要靠剩餘量等其他狀態前進；不能只看參數是否加一。

### 避免重複檢查已由構造保證的條件

```cpp
// 假設初始 count = 0，每次只加一，且所有子呼叫都經過下方 guard
if (count > limit) return; // 不會觸發，可省略
if (count < limit) {
    dfs(count + 1);
}
```

判斷一個 `if` 是否多餘，要檢查初始化與所有進入路徑是否已保證該性質；不能只因某條路徑有 guard 就刪掉。需要開發期檢查契約時，也可用 assertion 表達。

## 📚 題型索引

| 題目 | 關鍵 invariant／狀態關係 | 對應操作限制 |
|---|---|---|
| LC 22. Generate Parentheses | 所有前綴合法，`right <= left <= n` | `left < n`、`right < left` |
| LC 51. N-Queens | 已放皇后互不攻擊 | 欄與兩條斜線未被占用 |
| LC 79. Word Search | 路徑匹配目標前綴，同一格不重走 | 界內、字元相符、未使用 |
| LC 131. Palindrome Partitioning | 回文段連續覆蓋 `s[0:start)` | 檢查 `[start, end)`，遞迴傳 `end` |
| LC 39. Combination Sum | 索引非遞減，總和不超 target | 正整數候選不超剩餘量，下一層傳 `i` |
| LC 46. Permutations | 每個輸入位置最多使用一次 | `!used[i]` |
| LC 78. Subsets | 選取索引嚴格遞增 | 下一層傳 `i + 1`，每層收集 |
| LC 47. Permutations II | 相同值的輸入位置固定使用順序 | 排序後跳過前一個相同值尚未使用的候選 |
| LC 40 / 90. Combination Sum II / Subsets II | 同層每個候選值只分支一次 | 排序後，`i > start && a[i] == a[i-1]` 時跳過 |

## ✅ 設計檢查

- [ ] 狀態與 path 的意義清楚，初始狀態符合 invariant。
- [ ] 每個 choice 都能維持 invariant，下一層參數符合狀態定義。
- [ ] 收集條件能推出完整答案，停止條件與進展能解釋終止。
- [ ] 還原所有共享狀態，並確認剪枝與去重不會漏解。

相關筆記：[State and Solution Design](04-State_and_Solution_Design.md)、[去重設計](Duplicate_Removal_Pruning_Design.md)、[Correct by Construction](../Design_Principles/Correct_by_Construction.md)。
