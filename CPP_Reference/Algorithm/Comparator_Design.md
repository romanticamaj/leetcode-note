# Comparator 回傳值與多條件排序設計心法

**難度：⭐⭐⭐｜範例相容 C++14。** 以 LC 937. Reorder Data in Log Files 的 comparator 為例，理解排序關係，再設計多個排序順位。

## 🧠 核心觀念：true 是「嚴格優先」，不是「維持原位置」

`cmp(a, b)` 回答：**依照我的排序規則，a 是否應嚴格排在 b 前面？**

- `true`：a 必須優先；`false`：沒有要求 a 優先，不代表 b 一定優先。
- 參數 a／b 沒有「原本左邊／右邊」的保證；演算法自行選擇比較對象與順序。
- 這是在定義整個值域的關係，不是在指揮某一次交換；也不保證演算法會雙向呼叫來驗證。

| `cmp(a,b)` | `cmp(b,a)` | 意義 |
|:---:|:---:|:---|
| true | false | a 優先 |
| false | true | b 優先 |
| false | false | **同順位／等價**，未必 `a == b` |
| true | true | 規則矛盾，不合法 |

例如只按字串長度排序，"cat" 與 "dog" 值不同，卻是同順位。

## 合法條件：Strict Weak Ordering

`sort`／`stable_sort` 的 comparator 必須形成**嚴格弱序**，不只是回傳 bool 即可。規範見 [C++ 標準草案：排序關係](https://eel.is/c++draft/alg.sorting.general)。

- **自己不優先於自己**：`cmp(a,a)` 必須為 false，不能用 `<=`。
- **不能互相優先**：`cmp(a,b)` 為 true，則 `cmp(b,a)` 必須為 false。
- **優先關係可傳遞**：a 優先於 b、b 優先於 c，則 a 優先於 c。
- **同順位也可傳遞**：定義 `equiv(a,b) = !cmp(a,b) && !cmp(b,a)`；a 與 b、b 與 c 同順位，則 a 與 c 也必須同順位。

違反要求屬於 undefined behavior：可能錯序、看似正常或崩潰，不保證編譯或執行時會報錯。

## 🧩 多條件排序：前一順位相等，才比較下一順位

假設要求「primary 升序，primary 相同再依 secondary 升序」，排序 key 是 `(primary, secondary)`。

**背這個分支式模板，先判斷能否由主要欄位決定順序：**

```cpp
#include <algorithm>
#include <string>
#include <vector>

struct Record {
    std::string primary;
    std::string secondary;
};

bool before(const Record& a, const Record& b) {
    if (a.primary != b.primary) {
        return a.primary < b.primary;
    }
    return a.secondary < b.secondary;
}

// std::sort(records.begin(), records.end(), before);
```

| 口訣 | 動作 |
|:---|:---|
| 主鍵不同，就定輸贏 | 回傳主鍵的嚴格比較 |
| 主鍵相同，才比下一個 | 交給次鍵決定 |
| 所有鍵都同順位 | 回傳 false |

**正確性理由**：次鍵只在同一主鍵群組內決定順序，不可能推翻主鍵已決定的先後。對此處的字串欄位，就是 lexicographic ordering。

三個以上順位也是逐層處理：前兩鍵相等才比第三鍵。各欄位的升／降序可分別用 `<`／`>`，但仍須嚴格比較。

### 對照你寫的 `string::compare`

```cpp
int comp = contentA.compare(contentB);
return comp < 0 || (comp == 0 && identifierA < identifierB);
```

這是相同規則的壓縮寫法：`compare` 回傳負值／0／正值，分別表示小於／相等／大於；不保證剛好是 -1／0／1。

`&&` 比 `||` 優先，但保留括號讓 tie-break 的範圍清楚。**主要欄位不是原始值相等、而是由自訂關係定義同順位時，應用雙向比較都為 false 判斷，不能一概用 `==`。**

## LC 937：同順位交給 stable_sort 保留原順序

| log1 類型 | log2 類型 | comparator 回傳 |
|:---|:---|:---|
| letter | digit | true，letter 優先 |
| digit | letter | false |
| digit | digit | **false，兩者視為同順位** |
| letter | letter | 依 content，再依 identifier 比較 |

數字 log 不比較值，也不比較 identifier。雙向皆為 false 後，由 **stable_sort** 保留它們原本的相對順序；普通 sort 沒有這項保證。見 [C++ 標準草案：穩定性](https://eel.is/c++draft/algorithm.stable)。

因此你的註解應是「兩個 digit 同順位，由 stable_sort 保留原順序」，不是「log1 < log2」。

**多條件 comparator 本身不要求 stable_sort**：一般多鍵排序可用 sort；只有還需要保留所有排序鍵都同順位之元素的原始相對順序時，才要求穩定排序。

## ⚠️ 這次遇到的陷阱

- **兩個 digit 一律 true**：甚至 `cmp(a,a)` 也是 true，並不表示保留順序。
- **直接 OR 各欄位的小於**：`primaryA < primaryB || secondaryA < secondaryB`，可能互相優先。例如 a=("apple","z")、b=("banana","a")，雙向比較都為 true。
- **回傳 `a-b` 或直接回傳 `string::compare`**：int 可轉成 bool，負數與正數都變 true；這通常是排序關係錯誤，不是型別造成的編譯錯誤。整數相減還可能溢位。
- **參數寫成 `T&`**：可能無法接受演算法內部傳入的 const 值。物件型別使用 `const T&`，比較時不修改元素。

## ⏱️ 複雜度：比較次數 × 單次比較成本

令 n 為元素數、C 為 comparator 最壞成本；不要只看到 sort 就忽略 C。

| 操作 | 比較成本 |
|:---|:---|
| sort | `O(n log n · C)` |
| stable_sort，有足夠額外記憶體 | `O(n log n · C)` |
| stable_sort，記憶體不足的後備情況 | `O(n log² n · C)` |

937 每次 find／substr／compare 最壞與 log 長度 L 成正比，故 C=O(L)。stable_sort 的緩衝通常容納 O(n) 個元素，不可只算遞迴堆疊；string 的物件、其字元儲存與 comparator 的暫存字串應分開考量。比較次數規範見 [stable_sort](https://eel.is/c++draft/stable.sort)。

## ✅ 自我檢查與面試話術

- [ ] `cmp(a,a)` 是 false；不能出現雙向 true。
- [ ] 主鍵大於時，不會讓次鍵反過來推翻結果。
- [ ] 所有排序鍵同順位時回傳 false；需要保留原順序就用 stable_sort。
- [ ] const reference 可接受比較對象；沒有修改元素。
- [ ] 複雜度有計入字串處理成本。

「我先定義主鍵與次鍵。主鍵不同直接決定順序，相同才比較下一鍵。數字 log 彼此視為同順位，由 stable_sort 保留原始順序。」

相關：[排序 API 比較](Sort_Comparison.md) · [Predicate 與 Operation](Custom_Operation_Types.md) · [Lambda 與 decltype](Custom_Comparators_with_Decltype.md)。
