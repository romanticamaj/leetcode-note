# Binary Tree Canonical Forms 標準形式轉換 Playbook

## 🧠 核心哲學：先定義樹的等價，再設計簽章

**讓等價子樹得到相同簽章，再由子樹簽章構造父節點的簽章。** 正確的簽章必須滿足：兩棵樹等價，若且唯若它們的簽章相同。

本篇聚焦有根二元樹，節點值需要保留。通用框架與字串案例見 [Canonicalization](../../../Algorithms/Design_Principles/Canonicalization.md)。

## 1. 🧩 哪些差異可以消去？

| 題目的等價定義 | 必須保留 | 簽章組合方式 |
|---|---|---|
| **Ordered tree**：相同節點值與左右結構 | 左右順序 | `(value, left, right)` |
| **Flip-equivalent tree**：允許在任意節點交換左右子樹 | 子樹內容，不保留排列方向 | `(value, min(left,right), max(left,right))` |

LC 652. Find Duplicate Subtrees 屬於第一種；LC 951. Flip Equivalent Binary Trees 屬於第二種。交換左右子樹會改變第一種等價關係，不能在兩題中套用同一個交換規則。

若只判斷不含值的樹形，可從簽章中移除 value；若是無根樹，還需要處理 root 的選擇，不能直接拿任意兩個 root 比較。

## 2. 🧩 Post-Order：先取得完整的子樹表示

```text
取得左子樹簽章 → 取得右子樹簽章
→ 按等價定義保留／消去左右順序
→ 組合父節點值與子樹簽章
```

排序比較的是**完整子樹簽章**，因此必須先完成子問題。這裡 post-order 來自資料依賴，而不只是遍歷習慣。

## 3. 🧩 核心實作：用完整簽章比較

以下模板以 flip equivalence 為目標，不修改原樹。使用括號與空節點標記，避免不同結構得到相同編碼。

```cpp
std::string canonicalSignature(TreeNode* root) {
    if (!root) return "#";
    auto left = canonicalSignature(root->left);
    auto right = canonicalSignature(root->right);
    if (right < left) std::swap(left, right); // 子樹順序可交換
    return "(" + std::to_string(root->val) + "," + left + "," + right + ")";
}
// 判等：canonicalSignature(p) == canonicalSignature(q)
```

**遞迴契約**：返回時，簽章完整描述該子樹的節點值與結構，且不受左右翻轉影響。

葉節點的表示唯一；若子樹的正規表示已正確，排序後的兩個表示保留子樹的多重集合，再加上 root 值，就能唯一描述父節點的等價類。相同子簽章仍要保留兩份，不能改用 set 消掉重複。

### Ordered tree 的調整

若左右方向有意義，省去 `swap`，按原本左、右順序組合簽章即可。LC 652 在每次 post-order 返回時記錄簽章次數，第二次出現時收集一個代表 root；**不用重排原樹**。

## 4. ⚠️ 原先「比較子節點值」的適用邊界

只比較 `left->val`、`right->val` 來決定是否交換，在節點值互異且目標為 flip equivalence 時，可以固定子樹方向；但**不能保證含重複值的一般樹有唯一表示**。

```text
某節點的兩棵子樹：A 的 root 值為 2，B 的 root 值也為 2
A、B 的內部結構不同
(A,B) 與 (B,A) 可以翻轉得到彼此，但只比較 2 與 2 不會統一順序
```

因此，通用模板比較完整子樹簽章。只有右子樹時也會由空簽章參與排序，不需要另一個「把右子樹移到左邊」的特例。

## 5. 🧩 大量比較：將簽章 Intern 成整數 ID

完整字串方便理解，但會重複複製子樹內容。若要為每個節點保存簽章，可用共用字典將結構 key 編成 ID：

```text
null → ID 0
key = (value, leftID, rightID)
若允許翻轉，先將 leftID、rightID 排序
相同 key → 同一 ID；新 key → 新 ID
```

**兩棵樹必須共用字典。** ID 是字典內的代表，不是可以跨獨立執行任意比較的全域編碼。對 unordered rooted tree，將所有孩子 ID 排序後組成 key；保留每個 ID 的出現次數。

McGill 講義的 §1（pp. 2–5）以兩棵樹共同的逐層排序與編號，建立可比較的子樹標籤；此處的共用字典是相同設計觀點的實作形式。

## ⏱️ 複雜度

| 表示方式 | 時間 | 空間 |
|---|---|---|
| 完整字串簽章 | 最壞 O(n²)，鏈狀樹反覆串接長字串 | 單次判等的峰值 O(n)，另有 O(h) 堆疊 |
| 固定長度 key + 共用 hash dictionary（有根二元樹） | 平均 O(n) | O(n) 字典與 O(h) 堆疊 |

若保存每個節點的完整字串簽章，總字串空間也可能達 O(n²)。一般多子樹的 unordered tree 另有排序成本，不能直接套用二元樹的界限。

## ✅ 設計檢查

- [ ] 定義是否保留值、左右順序與 root。
- [ ] 簽章包含完整子樹與空節點資訊，編碼不產生歧義。
- [ ] 子簽章已完成後才組合父簽章。
- [ ] 允許排序時仍保留相同子樹的重複份數。
- [ ] ID 跨樹比較時，共用編號字典。
- [ ] 將字串建立／保存成本與遞迴堆疊計入複雜度。

## 📚 題目與參考

- LC 652. Find Duplicate Subtrees：保留左右順序，簽章分組。
- LC 951. Flip Equivalent Binary Trees：消去左右翻轉差異。
- [McGill：Tree Isomorphism，Assignment 5（2002）](../../../Reading/McGill_Tree_Isomorphism_Assignment_5_2002.pdf)：§1 說明有根樹的共同標籤；§2 說明無根樹的中心選擇。
- [Canonical Anchor Decomposition](../../../Algorithms/Divide_and_Conquer/08_Canonical_Anchor_Decomposition.md)：另一種唯一性設計，用於分解與列舉。
