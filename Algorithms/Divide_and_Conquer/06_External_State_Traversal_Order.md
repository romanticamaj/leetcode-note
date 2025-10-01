# External State 遍歷順序心法

> 本文為 [Conquer 策略對比](05_Conquer_Strategy_Comparison.md) 中 External State 策略的進階應用

## 🧠 核心哲學

在分治法中同步管理兩個獨立但相關的狀態：**遞迴結構狀態**（索引範圍）與**外部遍歷狀態**（資源指標）。這種技巧實現了用分治框架控制遞迴結構，同時按特定順序消費線性資源。

## 核心概念：雙軌狀態管理

### 狀態定義

```cpp
struct DualState {
    // 主軌：遞迴分治狀態
    int left, right;  // 索引範圍

    // 副軌：外部資源狀態
    Resource* current;  // 當前資源指標（全域或成員變數）
};
```

### 關鍵設計原則

1. **順序保證**：外部資源的消費順序必須與遞迴訪問順序一致
2. **狀態同步**：每次消費資源後立即推進外部狀態
3. **範圍對應**：索引範圍 `[left, right]` 對應外部資源的數量

## 通用模板

```cpp
template<typename ExternalResource, typename Result>
class DualStateTraversal {
    ExternalResource* current;  // 外部狀態指標

public:
    Result* build(ExternalResource* resource) {
        int n = getSize(resource);
        current = resource;  // 初始化外部狀態
        return construct(0, n - 1);
    }

private:
    Result* construct(int left, int right) {
        if (left > right) return nullptr;

        int mid = left + (right - left) / 2;

        // 根據遍歷順序選擇不同的實現
        return constructInOrder(left, mid, right);
        return constructPreOrder(left, mid, right);
        return constructPostOrder(left, mid, right);
    }
};
```

## 🧩 三種遍歷模式實現

### In-Order 模擬

```cpp
Result* constructInOrder(int left, int mid, int right) {
    // Step 1: 遞迴左子問題
    auto leftResult = construct(left, mid - 1);

    // Step 2: 消費當前資源（中序位置）
    Result* node = new Result(current->data);
    node->left = leftResult;
    current = current->next;  // 推進外部狀態

    // Step 3: 遞迴右子問題
    node->right = construct(mid + 1, right);

    return node;
}
```

### Pre-Order 模擬

```cpp
Result* constructPreOrder(int left, int mid, int right) {
    // Step 1: 先消費當前資源（前序位置）
    Result* node = new Result(current->data);
    current = current->next;

    // Step 2: 遞迴左子問題
    node->left = construct(left, mid - 1);

    // Step 3: 遞迴右子問題
    node->right = construct(mid + 1, right);

    return node;
}
```

### Post-Order 模擬

```cpp
Result* constructPostOrder(int left, int mid, int right) {
    // Step 1: 遞迴左子問題
    auto leftResult = construct(left, mid - 1);

    // Step 2: 遞迴右子問題
    auto rightResult = construct(mid + 1, right);

    // Step 3: 最後消費資源（後序位置）
    Result* node = new Result(current->data);
    node->left = leftResult;
    node->right = rightResult;
    current = current->next;

    return node;
}
```

## 適用場景

- **線性轉樹狀**：將 linked list、array 轉換為 tree
- **順序限制**：外部資源只能順序訪問（如 stream、linked list）或是透過遞迴順序決定的訪問順序
- **平衡構建**：需要構建平衡結構（如 balanced BST）

## ⏱️ 複雜度分析

| 操作     | 時間複雜度           | 空間複雜度        |
| -------- | -------------------- | ----------------- |
| 構建     | O(n)                 | O(log n) 呼叫堆疊 |
| 資源遍歷 | 每個資源恰好訪問一次 | O(1) 外部指標     |
