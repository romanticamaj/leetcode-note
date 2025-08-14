# 最小生成樹 (Minimum Spanning Tree) 核心理論：Cut Property

---

## 1. 什麼是最小生成樹 (MST)？

給定一個**連通的、帶權重的無向圖 (Connected, Weighted, Undirected Graph)**，一個最小生成樹 (MST) 是該圖的一個子圖，它滿足以下三個條件：

1. **包含圖中所有的頂點 (Vertices)**。
2. **是一棵樹 (Tree)**：子圖本身是無環的。
3. **權重總和最小**: 在所有可能的生成樹中，它的所有邊的權重之和是最小的。

MST 在網路設計、電路佈線、叢集分析等領域有著廣泛的應用，其目標是用最小的「成本」連接所有的點。

---

## 2. Cut Property：MST 的基石

**Cut Property** 是構建所有 MST 演算法（如 Prim's 和 Kruskal's）的基礎。它提供了一個**安全地**將一條邊加入到 MST 中的準則。

### 定義：什麼是「Cut」？

一個「Cut」是對圖中所有頂點的一個劃分 (Partition)，將其分為兩個**非空的、不相交的**集合，我們稱之為 `S` 和 `T`。

- `S` 和 `T` 的聯集 (Union) 包含圖中所有的頂點。
- `S` 和 `T` 的交集 (Intersection) 為空。

一條**跨越 (cross)** 這個 Cut 的邊，是指其兩個端點分別位於 `S` 和 `T` 中。

### Cut Property 定理

> 對於圖中的任意一個 Cut (`S`, `T`)，如果一條跨越這個 Cut 的邊 `e` 的權重**嚴格小於**所有其他跨越該 Cut 的邊的權重，那麼這條邊 `e` **必定屬於**該圖的每一個最小生成樹。

這條邊 `e` 被稱為**安全邊 (Safe Edge)**。

---

## 3. Cut Property 證明 (Proof by Contradiction)

我們使用反證法來證明這個定理。

1. **假設 (Assumption)**:

   - 假設存在一個 Cut (`S`, `T`)。
   - 假設邊 `e = (u, v)` 是跨越此 Cut 的權重**最輕**的邊。
   - 假設存在一個 MST，我們稱之為 `T_mst`，**且 `T_mst` 不包含邊 `e`**。

2. **推理 (Reasoning)**:

   - 因為 `T_mst` 是一棵生成樹，它連接了圖中所有的頂點。因此，在 `T_mst` 中，必定存在一條從 `u` 到 `v` 的路徑 (Path)。
   - 在這條路徑上，必然存在**至少一條**其他的邊，我們稱之為 `e' = (x, y)`，它也跨越了 Cut (`S`, `T`)。如果不存在這樣的邊，那麼從 `u` 到 `v` 的整條路徑都會在 `S` 或 `T` 的一側，這與 `u` 和 `v` 分屬不同集合矛盾。
   - 根據我們的初始定義，邊 `e` 是跨越 Cut 的最輕邊，所以 `weight(e) < weight(e')`。

3. **構造與矛盾 (Construction and Contradiction)**:

   - 現在，我們來構造一個新的生成樹 `T_new`。我們從 `T_mst` 中**移除**邊 `e'`，並**加入**邊 `e`。
   - **`T_new` 仍然是一棵樹嗎？**
     - 移除 `e'` 會將 `T_mst` 分裂成兩個不連通的部分。
     - 由於 `e'` 和 `e` 都跨越了同一個 Cut，加入 `e` 會重新連接這兩個部分，形成一棵新的樹。因此，`T_new` 仍然是一棵生成樹。
   - **`T_new` 的權重是多少？**
     - `weight(T_new) = weight(T_mst) - weight(e') + weight(e)`。
     - 因為 `weight(e) < weight(e')`，所以 `weight(T_new) < weight(T_mst)`。

4. **結論 (Conclusion)**:
   - 我們找到了一棵比 `T_mst` 權重更輕的生成樹 `T_new`。
   - 這與我們最初「`T_mst` 是最小生成樹」的假設相矛盾。
   - 因此，我們的初始假設「`T_mst` 不包含邊 `e`」是錯誤的。

**證明完畢**：任何跨越一個 Cut 的最輕邊 `e`，必定屬於圖的每一個 MST。
