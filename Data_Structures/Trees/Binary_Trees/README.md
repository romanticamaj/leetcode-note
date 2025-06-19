# Binary Tree Traversal

## 基本概念

二叉樹（Binary Tree）是一種樹形數據結構，其中每個節點最多有兩個子節點，通常稱為左子節點和右子節點。二叉樹是計算機科學中最常用的樹形結構之一。

一個典型的二叉樹節點定義如下：

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};
```

## 遍歷方法

二叉樹有四種主要的遍歷方式：

1. **前序遍歷（Preorder Traversal）**：根節點 -> 左子樹 -> 右子樹
2. **中序遍歷（Inorder Traversal）**：左子樹 -> 根節點 -> 右子樹
3. **後序遍歷（Postorder Traversal）**：左子樹 -> 右子樹 -> 根節點
4. **層序遍歷（Level Order Traversal）**：按層從上到下，每層從左到右

遍歷方法的名稱描述了當前節點的處理邏輯何時執行：

Pre -> before children (在處理子節點之前)
In -> in the middle of children (在處理子節點之間)
Post -> after children (在處理子節點之後)


如果我們參考前面提到的 DFS 通用結構：

```
1. Handle the base case(s). Usually, an empty tree (node = null) is a base case.
2. Do some logic for the current node
3. Recursively call on the current node's children
4. Return the answer
```

三種遍歷類型的區別僅在於它們執行步驟 2（處理當前節點）和步驟 3（遞歸調用子節點）的順序不同：

- **前序遍歷**：步驟 2 → 步驟 3（先處理當前節點，再遞歸子節點）
- **中序遍歷**：步驟 3（左子節點）→ 步驟 2 → 步驟 3（右子節點）
- **後序遍歷**：步驟 3 → 步驟 2（先遞歸子節點，再處理當前節點）

這種理解方式使得三種遍歷方法之間的關係更加清晰，它們本質上都是 DFS，只是處理節點的時機不同。

## 為什麼樹的遍歷通常使用遞歸？

Linked List 通常使用 iterative 方式遍歷，而 Binary Tree 則通常使用 recursive 方式遍歷。

這種差異主要源於這兩種數據結構的本質特性。

### 樹的遞歸特性

樹的結構天然具有遞歸特性，這是因為：

1. **子樹概念**：每個樹節點及其子節點形成一個子樹，而這個子樹本身也是一棵完整的樹。這種"樹中樹"的結構非常適合遞歸處理。
2. **問題分解**：樹的問題通常可以分解為對左子樹和右子樹的相同操作，然後合併結果。這正是遞歸的核心思想。
3. **代碼簡潔性**：使用遞歸處理樹可以使代碼非常簡潔和易於理解，而迭代方法通常需要顯式使用棧或隊列來模擬遞歸過程。
4. **自然的終止條件**：樹的遞歸有明確的終止條件（空節點），使得遞歸邊界清晰。

### 葉節點與遞歸終止 (超重要!!!)

**特別注意**：為什麼遞歸在樹結構中能夠正確工作？葉節點（Leaf Node）在這裡扮演著關鍵角色！

葉節點是沒有子節點的節點，它有以下重要特性：

1. **葉節點也是子樹**：每個葉節點本身也是一個子樹，只是這個子樹沒有更多的分支。
2. **通往基本情況的橋樑**：葉節點的左右子節點都是 `null`，這意味著當遞歸到葉節點時，對其子節點的遞歸調用會直接進入基本情況（base case）。
3. **遞歸終止的保證**：正是因為葉節點的存在，遞歸才能夠有保證地終止。沒有葉節點，遞歸將無法到達基本情況。

****重要**** `Leaf Node 也是一個 subtree (可以走到 base case 的 subtree)`

這個理解對於掌握樹的遞歸至關重要。當我們遞歸地處理一棵樹時，我們實際上是在處理一系列嵌套的子樹，最終到達葉節點，然後通過葉節點的 `null` 子節點進入基本情況，從而開始回溯過程。

## 鏈表與樹的比較

鏈表通常使用迭代而不是遞歸的原因：

1. **線性結構**：鏈表是線性結構，沒有分支，遍歷路徑唯一，使用 iterative 更為直觀。
2. **空間效率**：對於長鏈表，recursive 可能導致 stack overflow，而 iterative 不會有這個問題。
3. **操作簡單**：鏈表的 iterative 操作通常只需要一個 pointer，實現簡單。

linked list 如果要用 recursive，終止條件不外乎是 next pointer 是 nullptr，而且只會遇到一次
tree 終止條件會是 children 是 nullptr，可以遇到很多次