# 正規化（Canonicalization）解題心法

## 🧠 核心哲學：先定義等價，再轉成共同表示

**把每個輸入各自轉成標準表示，再用相等比較判斷原本的等價關係。** 這讓兩個物件的同步比對，轉成兩次獨立轉換與一次比較；也能把多個等價物件放到同一個分組。

設 `x ~ y` 表示題目定義的等價關係，設計轉換 `C` 時必須滿足：

```text
x ~ y  ⇔  C(x) == C(y)
```

`C` 不需要在所有輸入之間一對一；等價輸入正是要得到相同結果。嚴格來說，選出同類物件的代表是 canonical form；產生可精確判等的編碼是 canonical encoding／complete invariant。本文統稱為「正規表示」。

## 1. 🧩 定義等價：哪些差異可以消去？

| 等價關係 | 必須保留 | 可以消去 |
|---|---|---|
| 字元可一對一改名後得到另一字串 | 位置與重複出現模式 | 字元名稱 |
| Anagram：重排後相同 | 每個字元的出現次數 | 字元順序 |
| Ordered tree：相同值與結構 | 節點值、左右方向、空節點 | 節點地址 |
| Flip-equivalent tree：可交換左右子樹 | 節點值、子樹結構與數量 | 左右子樹的排列方向 |

**沒有先定義等價，就無法判斷轉換是否正確。** 例如排序適合消去 anagram 的順序，卻會破壞 isomorphic strings 要保留的位置模式。

## 2. 🧩 設計表示：保留決定等價的資訊

| 問題特徵 | 可用的正規表示 |
|---|---|
| 字元名稱不重要，重複模式重要 | 按首次出現順序編號 |
| 順序不重要，頻率重要 | 字元計數向量；不一定要先排序 |
| 結構遞迴定義 | 由子問題正規表示組成父節點簽章 |
| 子問題順序不重要 | 將子問題簽章排序後再組合，保留重複項 |

```text
paper → 0,1,0,2,3
title → 0,1,0,2,3   → 相同模式
    ab → 0,1
    aa → 0,0         → 不同模式
```

每個字串各自建立「字元 → 編號」的一對一映射，但不同字串可以得到同一個編號序列。

## 3. 🧩 關鍵實作：首次出現編號

以下對 byte string 操作；若題目以 Unicode 字元為單位，需先解碼為該單位，再建立映射。

```cpp
std::vector<int> canonicalPattern(std::string_view s) {
    std::array<int, 256> id;
    id.fill(-1);
    int nextId = 0;
    std::vector<int> pattern;
    pattern.reserve(s.size());
    for (unsigned char c : s) {
        if (id[c] == -1) id[c] = nextId++;
        pattern.push_back(id[c]);
    }
    return pattern;
}
// 判等：canonicalPattern(s) == canonicalPattern(t)
```

**Loop invariant**：已處理字元中，每個不同字元都有唯一且依首次出現順序分配的編號；輸出前綴正確保留它們的相等關係。

新字元取得下一個編號，舊字元沿用編號。兩個字串若能一對一改名，首次出現順序與所有重複位置都一致；反過來，相同編號序列也能建立兩側字元的一對一對應。

### 與直接驗證 Mapping 的比較

| 方法 | 保存的狀態 | 思考方式 |
|---|---|---|
| Mapping + used set | 來源的對應，以及已使用的目標 | 檢查一致性與目標不被共用 |
| Forward + reverse mapping | 兩個方向的對應 | 直接維持一對一映射 |
| Last-seen | 兩側字元上次出現的位置 | 比較歷史位置，驗證重複模式 |
| Canonicalization | 各輸入的標準編碼 | 各自轉換，再比較或分組 |

Last-seen 不是 used set，也不必建出正規序列。若目標是通用的 1–1 mapping 實作，雙向 map 很直接；若要保存模式或對多個輸入分組，正規表示更方便。

## 4. 🧩 遞迴結構：子問題的表示決定父問題

樹的簽章可以由 `(節點值, 左簽章, 右簽章)` 組成。若允許交換左右子樹，就先將兩個子簽章排序；若方向有意義，就保留左右順序。

**先算子問題表示，再組成父表示**，自然得到 post-order。簽章也能透過共用字典編成整數 ID，但兩棵樹須使用同一套編號，不能把各自任意分配的 ID 直接比較。

詳見 [樹的 Canonical Forms](../../Data_Structures/Trees/Binary_Trees/Canonical_Forms_Transformation.md)。

### 與 Canonical Anchor Decomposition 的關係

兩者都固定一種表示／構造約定，但解決的問題不同：

- **正規表示**：讓等價物件取得相同 key，用於判等與分組。
- **唯一分解**：從每個結果反推出唯一的錨點與子結果，避免枚舉時重複生成。
- **唯一遍歷起點**：只由可辨識的錨點啟動遍歷，避免反覆處理同一結構。

它們共用「指定唯一代表或規則」的設計觀點；具體正確性須各自證明。枚舉分治與 memoization 見 [Canonical Anchor Decomposition](../Divide_and_Conquer/08_Canonical_Anchor_Decomposition.md)。

## ⚠️ 常見陷阱

- **只證明一個方向**：等價物件應有相同表示，不等價物件也必須被區分。
- **把正規化當作全域一對一函式**：等價物件刻意合併到同一表示。
- **消去題目要求保留的資訊**：例如 ordered tree 不能任意交換左右子樹。
- **只取局部資訊**：相同子節點值，不代表兩棵子樹等價；要保留完整結構簽章。
- **編碼產生歧義**：`[1,11]` 與 `[11,1]` 都串成 `111`；用結構化 key、分隔符或長度編碼。
- **把 hash 值當完整表示**：有限 hash 可能碰撞；精確判等仍需完整 key 或可靠的相等檢查。

## ⏱️ 複雜度

首次出現編號需要 `O(n)` 時間、`O(n)` 輸出空間，固定 byte 字元集的映射表為 `O(1)`。一般正規化的成本取決於表示設計，還須計入建立、保存與比較 key 的工作。

## 📚 題目與延伸閱讀

| 題目 | 新增的設計練習 |
|---|---|
| LC 205. Isomorphic Strings | 從一對一映射轉成首次出現模式 |
| LC 49. Group Anagrams | 改以頻率判等，並用 key 分組 |
| LC 890. Find and Replace Pattern | 重用一個模式，篩選多個輸入 |
| LC 652. Find Duplicate Subtrees | 保留方向的遞迴簽章與重複計數 |
| LC 951. Flip Equivalent Binary Trees | 允許交換時，消去子樹排列方向 |

- [McGill：Tree Isomorphism，Assignment 5（2002）](../../Reading/McGill_Tree_Isomorphism_Assignment_5_2002.pdf)：§1，pp. 2–5，從底向上建立子樹標籤，藉共同標籤比較兩棵樹；§2，pp. 5–7，處理無根樹。
- [Knuth：TAOCP Volume 4A 預覽](../../Reading/Knuth_The_Art_of_Computer_Programming_Volume_4A_Preview.pdf)：目錄在 PDF 第 17 頁列出 §7.2.1.6〈Generating all trees〉，書本 p. 440；此預覽未包含該節正文。這是結構枚舉的延伸來源，不是本模板的出處。
