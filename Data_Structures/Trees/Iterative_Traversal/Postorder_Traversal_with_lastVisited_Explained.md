# 深入解析：迭代 Postorder Traversal 中 `lastVisited` 的正確性

## 1. 核心難點：返回時的歧義

在迭代的 Postorder Traversal 中，當我們一路向左 (`root = root->left`) 到底，然後從堆疊 (`stack`) 中查看頂部節點 (`peekNode = s.top()`) 時，我們面臨一個關鍵的決策點。`peekNode` 是我們剛剛完成其左子樹探索的父節點。

此時，我們需要決定下一步是：
a. 探索 `peekNode` 的右子樹？
b. 還是處理 `peekNode` 本身？

如果我們沒有額外的資訊，這個決策是無法做出的。當我們的控制流第二次回到 `peekNode` 時（即從右子樹返回時），我們如何知道右子樹已經探索過了，而不是又一次從左子樹返回呢？這就是「返回時的歧義性」。

## 2. `lastVisited` 的角色：提供時間上下文

`lastVisited` 指標的作用就是為了解決這個歧義。它像一個「路標」，**永遠指向我們上一個完整處理（訪問、彈出堆疊）的節點**。

通過比較 `peekNode` 的右子節點 `peekNode->right` 和 `lastVisited`，我們可以精確地推斷出我們當前所處的「時間點」：

- **`peekNode->right == lastVisited`** 意味著什麼？

  - 它意味著我們**剛剛**完成了對 `peekNode` 右子樹的探索，並且 `lastVisited` 正是那個右子節點。
  - 這是一個明確的信號：`peekNode` 的左、右子樹都已探索完畢。現在輪到處理 `peekNode` 本身了。

- **`peekNode->right != lastVisited`** 意味著什麼？
  - 這涵蓋了兩種情況：
    1. 我們是**從左子樹返回**的。此時 `lastVisited` 是 `peekNode` 左子樹中的某個節點，因此它不等於 `peekNode->right`。
    2. `peekNode` 根本沒有右子樹 (`peekNode->right == nullptr`)。
  - 在這兩種情況下，下一步的決策都是不同的，但判斷式 `if (peekNode->right && peekNode->right != lastVisited)` 完美地處理了這一點。

## 3. 場景分析：`lastVisited` 如何確保正確性

讓我們通過一個例子來走一遍流程：

```
      A
     / \
    B   C
   / \
  D   E
```

Postorder 順序應該是：D, E, B, C, A。

**場景一：從左子樹返回 (以節點 B 為例)**

1. ... D 被訪問, `lastVisited` 指向 D。
2. ... E 被訪問, `lastVisited` 指向 E。
3. 控制流返回，`s.top()` 是 B。我們窺視 B (`peekNode = B`)。
4. 執行判斷：`if (B->right && B->right != lastVisited)`
   - `B->right` 是 E，存在。
   - `lastVisited` 是 E。
   - 所以 `B->right != lastVisited` 為 **false**。
5. **決策**: 條件不成立，進入 `else` 區塊。這意味著 B 的右子樹（E）剛剛被訪問完。
6. **動作**: 處理 B，將 B 從堆疊彈出，更新 `lastVisited = B`。

**正確性證明**: `lastVisited` 成功地告訴我們，我們是從右子節點 E 返回的，因此可以安全地處理節點 B。

**場景二：從右子樹返回 (以節點 A 為例)**

1. ... B 被訪問, `lastVisited` 指向 B。
2. 控制流返回，`s.top()` 是 A。我們窺視 A (`peekNode = A`)。
3. 執行判斷：`if (A->right && A->right != lastVisited)`
   - `A->right` 是 C，存在。
   - `lastVisited` 是 B。
   - 所以 `A->right != lastVisited` 為 **true**。
4. **決策**: 條件成立。這意味著 A 的右子樹（C）存在且尚未被訪問。
5. **動作**: 我們必須先探索右子樹。設置 `root = C`，然後 `continue` 或內嵌迴圈開始新一輪的向左深入。

---

**第二次回到 A**:

1. ... C 被訪問, `lastVisited` 指向 C。
2. 控制流再次返回，`s.top()` 又是 A。我們窺視 A (`peekNode = A`)。
3. 再次執行判斷：`if (A->right && A->right != lastVisited)`
   - `A->right` 是 C，存在。
   - `lastVisited` 現在是 C。
   - 所以 `A->right != lastVisited` 為 **false**。
4. **決策**: 條件不成立，進入 `else` 區塊。
5. **動作**: 處理 A，將 A 從堆疊彈出，更新 `lastVisited = A`。

**正確性證明**: `lastVisited` 再次成功地告訴我們，我們是從右子節點 C 返回的，因此可以安全地處理節點 A。

## 結論

`lastVisited` 就像一個記憶體，它記錄了迭代狀態機的上一個**終結狀態**（即一個節點連同其子樹被完全處理）。通過將當前決策點的右子節點與這個「記憶」進行比較，我們就能夠打破返回時的歧義，確保只有在左右子樹都處理完畢後，才處理父節點，從而完美地實現了 Postorder 的遍歷順序。
