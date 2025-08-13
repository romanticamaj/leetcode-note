# 心法: 三色節點著色 DFS (CLRS 風格)

源自經典教科書《Introduction to Algorithms》(CLRS) 的深度優先搜尋 (DFS) 演算法，透過為節點賦予三種顏色狀態，提供了一個比簡單 `visited` 陣列更強大、更富表達力的圖遍歷框架。

## 1. 核心演算法

演算法為每個節點 `u` 維護三個屬性：

- `u.color`: 節點的狀態 (WHITE, GRAY, BLACK)。
- `u.d`: 節點被首次發現的時間戳 (Discovery time)。
- `u.f`: 節點的所有鄰居都被訪問完畢的時間戳 (Finish time)。

**偽代碼**

```
DFS(G):
  for each vertex u in G.V:
    u.color = WHITE
    u.parent = NIL
  time = 0
  for each vertex u in G.V:
    if u.color == WHITE:
      DFS-VISIT(G, u)

DFS-VISIT(G, u):
  time = time + 1
  u.d = time
  u.color = GRAY  // 節點 u 進入遞迴堆疊，正在被訪問
  for each v in G.Adj[u]:
    if v.color == WHITE:
      v.parent = u
      DFS-VISIT(G, v)
  u.color = BLACK // 節點 u 的所有鄰居都已訪問完畢，離開遞迴堆疊
  time = time + 1
  u.f = time
```

## 2. 邊的分類 (Classification of Edges)

三色狀態讓我們可以在 DFS 過程中，根據遇到的鄰居節點 `v` 的顏色，對圖中的邊 `(u, v)` 進行分類：

1. **樹邊 (Tree Edge)**: 當 `v` 的顏色是 **WHITE** 時。這意味著我們在 DFS 過程中首次發現節點 `v`，`(u, v)` 構成 DFS 森林中的一條邊。

2. **返祖邊 (Back Edge)**: 當 `v` 的顏色是 **GRAY** 時。這意味著 `v` 是 `u` 在 DFS 森林中的一個祖先節點。`v` 仍在遞迴堆疊中，我們從 `u` 又「返回」訪問了它。**偵測到返祖邊，等同於在有向圖中偵測到環。**

3. **前向邊 (Forward Edge)** 或 **橫叉邊 (Cross Edge)**: 當 `v` 的顏色是 **BLACK** 時。
   - **前向邊**: `v` 是 `u` 在 DFS 森林中的一個後代。
   - **橫叉邊**: `v` 和 `u` 不存在祖先-後代關係，它們可能屬於同一個 DFS 樹的不同子樹，或屬於不同的 DFS 樹。

**關鍵洞察**: 一個簡單的 `bool visited[]` 陣列只能區分「已訪問」和「未訪問」，相當於只有 WHITE 和 (GRAY/BLACK) 的混合體。它無法區分一個已訪問的節點是「正在被訪問 (GRAY)」還是「已訪問完畢 (BLACK)」，因此無法可靠地辨別返祖邊和前向/橫叉邊。

## 3. 應用

### 應用一：環偵測 (Cycle Detection)

如上所述，在有向圖中，DFS 過程中遇到一個指向 GRAY 節點的邊，就意味著發現了一個返祖邊，從而證實了環的存在。

### 應用二：重複子問題與備忘錄 (Memoization)

三色狀態完美地對應了動態規劃中解決重複子問題的三種狀態：

- **WHITE (未計算)**: 這是一個全新的子問題，需要進行計算。
- **GRAY (正在計算)**: 這個子問題正在遞迴計算中。如果在此狀態下又遇到了它自己，說明出現了循環依賴（即圖中的環）。
- **BLACK (已計算完畢)**: 這個子問題已經有了確切的解，可以直接從備忘錄 (memo) 中返回結果，無需重複計算。

**延伸範例**: LeetCode 1059. All Paths from Source Lead to Destination，就是一個利用三色 DFS 來判斷所有路徑是否都通往終點且無環的經典應用。
