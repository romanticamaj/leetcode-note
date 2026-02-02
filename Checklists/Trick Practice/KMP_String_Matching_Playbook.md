# 🎯 KMP String Matching (字串匹配) - 練習路徑

KMP (Knuth-Morris-Pratt) 演算法是**線性時間字串匹配**演算法，核心技巧是透過 **prefix table (LPS array)** 在部分匹配失敗時**跳過已驗證的前綴**，避免重複比對。

**關鍵突破**：當 `pattern[j]` 匹配失敗時，不回溯 `text[i]`，而是利用 `lps[j-1]` 跳轉 `j`，達到 O(m+n) 時間複雜度。

---

## 🧠 核心概念

### TL;DR - KMP 公式速查

```cpp
// 1. 建立 LPS (Longest Proper Prefix which is also Suffix)
vector<int> buildLPS(string pattern) {
    int m = pattern.size();
    vector<int> lps(m, 0);
    int len = 0;  // 當前匹配長度

    for (int i = 1; i < m; i++) {
        while (len > 0 && pattern[i] != pattern[len]) {
            len = lps[len - 1];  // 回退到上一個可能的前綴
        }
        if (pattern[i] == pattern[len]) {
            len++;
        }
        lps[i] = len;
    }
    return lps;
}

// 2. KMP 搜尋
int kmpSearch(string text, string pattern) {
    int n = text.size(), m = pattern.size();
    vector<int> lps = buildLPS(pattern);

    int i = 0, j = 0;  // i: text index, j: pattern index
    while (i < n) {
        if (text[i] == pattern[j]) {
            i++; j++;
        }

        if (j == m) {
            return i - j;  // 找到匹配，返回起始位置
        } else if (i < n && text[i] != pattern[j]) {
            if (j > 0) {
                j = lps[j - 1];  // 跳轉而非回溯
            } else {
                i++;
            }
        }
    }
    return -1;  // 未找到
}
```

### LPS 陣列的意義

```
Pattern: "ABABACA"
LPS:     [0,0,1,2,3,0,1]
         ↑         ↑
         無前綴     "A" 既是前綴也是後綴

lps[i] = pattern[0..i] 中最長的「真前綴=真後綴」長度
```

### Naive vs KMP 比較

| 方法   | 失配時的動作     | 時間複雜度 |
| ------ | ---------------- | ---------- |
| Naive  | 回溯 text，重新掃描 | O(n × m)   |
| KMP    | 跳轉 pattern 指標，text 不回溯 | O(n + m)   |

---

## 🏁 目標題總覽

| 題號   | 題目名稱                               | Pattern 特徵               | 難度   |
| ------ | -------------------------------------- | -------------------------- | ------ |
| LC 28  | Find the Index of the First Occurrence | 基礎 KMP，單次匹配         | ⭐⭐   |
| LC 459 | Repeated Substring Pattern             | 檢測循環模式，LPS 應用     | ⭐⭐   |
| LC 686 | Repeated String Match                  | 循環串接，構造 text        | ⭐⭐   |
| LC 796 | Rotate String                          | 循環移位，`s2+s2` 包含 `s1` | ⭐     |
| LC 214 | Shortest Palindrome                    | 前綴匹配反向後綴           | ⭐⭐⭐ |
| LC 572 | Subtree of Another Tree                | 序列化 + KMP               | ⭐⭐   |
| LC 1392| Longest Happy Prefix                   | 直接返回 LPS[-1]           | ⭐⭐   |

---

## 🧭 練習路徑（依 Pattern 變體）

### 1️⃣ 基礎字串匹配（Classic String Matching）

**核心概念**：在 text 中查找 pattern 的出現位置

- 📙 **LC 28. Find the Index of the First Occurrence in a String** ← 入門：標準 KMP 模板
  - 實現 buildLPS + kmpSearch
  - 理解為何 `j = lps[j-1]` 而非 `j = 0`

- 📙 **LC 1392. Longest Happy Prefix** ← LPS 直接應用
  - 答案就是 `pattern[0..lps[m-1]]`
  - 檢驗對 LPS 的理解

### 2️⃣ 循環模式檢測（Cyclic Pattern Detection）

**核心概念**：利用 LPS 偵測字串的重複結構

- 📙 **LC 459. Repeated Substring Pattern** ← 經典：判斷是否由子模式循環構成
  - **技巧 1**：`lps[n-1] > 0 && n % (n - lps[n-1]) == 0`
  - **技巧 2**：`(s+s).substr(1, 2*n-2)` 包含 `s`
  - Key insight: 重複模式的最小單位長度 = `n - lps[n-1]`

- 📙 **LC 796. Rotate String** ← 變體：循環移位檢測
  - 技巧：`s2` 是 `s1` 的循環移位 ⇔ `s1` 是 `s2+s2` 的子字串
  - 用 KMP 在 `s2+s2` 中查找 `s1`

- 📙 **LC 686. Repeated String Match** ← 進階：最少串接次數
  - 構造 `text = a + a + ... (重複 k 次)`
  - 在 text 中用 KMP 查找 b
  - 估算：`k = ceil(len(b) / len(a))` 到 `k+1` 次

### 3️⃣ 前後綴匹配（Prefix-Suffix Matching）

**核心概念**：利用 KMP 找字串的前綴與某變換後綴的最長匹配

- 📕 **LC 214. Shortest Palindrome** ← 進階：找最短前綴使字串變回文
  - 構造 `s + "#" + reverse(s)`，計算 LPS
  - `lps[-1]` 表示 s 的前綴與 reverse(s) 的後綴最長匹配
  - 需要在前面補的字元 = `s[lps[-1]..]` 的反轉

### 4️⃣ 序列化 + KMP（Serialization + Pattern Matching）

**核心概念**：將結構問題轉換為字串匹配

- 📙 **LC 572. Subtree of Another Tree** ← 應用：判斷子樹
  - **步驟 1**：序列化兩棵樹為字串（preorder + null marker）
  - **步驟 2**：用 KMP 檢查 `subRoot序列` 是否為 `root序列` 的子字串
  - ⚠️ 注意：需要 node marker（如 `#` for null, `^` for node start）避免 `12` 匹配 `2`

---

## 🔑 Pattern 識別關鍵字

遇到以下關鍵字，考慮 KMP：

- ✅ "find substring" / "pattern matching"
- ✅ "repeated pattern" / "cyclic structure"
- ✅ "linear time string search" / O(n+m)
- ✅ "rotate string" / "circular"
- ✅ "prefix == suffix"
- ✅ "shortest palindrome" / "longest happy prefix"
- ✅ 結構序列化後的字串匹配

---

## ✅ 建議練習順序

### 階段 1：KMP 基礎（1-2 天）

1. **LC 28** → 實現標準 KMP 模板，理解 buildLPS 與跳轉邏輯
2. **LC 1392** → 驗證對 LPS 的理解

### 階段 2：循環模式應用（1-2 天）

3. **LC 459** → 學習利用 LPS 偵測重複結構
4. **LC 796** → 理解 `(s+s)` 包含 `s` 的技巧
5. **LC 686** → 循環串接，估算次數上界

### 階段 3：前後綴匹配（1-2 天）

6. **LC 214** → 構造 `s + "#" + reverse(s)`，經典技巧

### 階段 4：結構序列化（可選）

7. **LC 572** → 序列化樹 + KMP，展示演算法組合威力

---

## ⚠️ 常見陷阱

### 1. LPS 建立時的邊界條件

```cpp
// ❌ 錯誤：忘記 len > 0 檢查
if (pattern[i] != pattern[len]) {
    len = lps[len - 1];  // len=0 時會越界！
}

// ✅ 正確：先檢查 len > 0
while (len > 0 && pattern[i] != pattern[len]) {
    len = lps[len - 1];
}
```

### 2. 匹配時忘記 i < n 檢查

```cpp
// ✅ 正確：匹配失敗時檢查邊界
else if (i < n && text[i] != pattern[j]) {
    // 處理失配...
}
```

### 3. 序列化時的標記不足

```cpp
// ❌ 錯誤：node(12) 的子樹可能匹配到 node(2)
string serialize(TreeNode* root) {
    if (!root) return "null";
    return to_string(root->val) + "," + serialize(root->left) + "," + serialize(root->right);
}

// ✅ 正確：加入明確的 node 起始標記
string serialize(TreeNode* root) {
    if (!root) return "#";
    return "^" + to_string(root->val) + serialize(root->left) + serialize(root->right);
}
```

### 4. LPS 語意混淆

```
lps[i] = "pattern[0..i]" 的最長真前綴=真後綴長度
       ≠ "pattern[0..i)" 的長度

Example: pattern = "ABABC"
lps[4] = 0  (因為 "ABABC" 無真前綴=真後綴)
lps[3] = 2  (因為 "ABAB" 有 "AB"=前綴=後綴)
```

---

## ⏱️ 複雜度分析

| 操作        | 時間複雜度 | 空間複雜度 | 說明                     |
| ----------- | ---------- | ---------- | ------------------------ |
| buildLPS    | O(m)       | O(m)       | 每個字元最多訪問兩次     |
| kmpSearch   | O(n)       | O(m)       | text 指標單向前進，不回溯 |
| **總計**    | **O(n+m)** | **O(m)**   | 遠優於 naive O(n×m)      |

---

## 💡 關鍵心法總結

1. **LPS = 失配時的回退位置** → `lps[j-1]` 告訴你 pattern 指標該跳到哪
2. **text 指標永不回溯** → `i` 只增不減，這是 O(n) 的關鍵
3. **循環模式 = LPS 結構特徵** → `n % (n - lps[n-1]) == 0` 檢測重複
4. **構造技巧** → `s + "#" + reverse(s)` 或 `s + s` 展開問題空間
5. **序列化要明確標記** → 避免數字拼接產生的 false positive

---

## 🔄 替代方案：Z-Algorithm

Z-Algorithm 是另一個 O(n+m) 字串匹配演算法，在某些場景下更直觀：

```cpp
// Z[i] = s[i..] 與 s[0..] 的最長公共前綴長度
vector<int> z_algorithm(string s) {
    int n = s.size();
    vector<int> z(n);
    int l = 0, r = 0;
    for (int i = 1; i < n; i++) {
        if (i <= r) z[i] = min(r - i + 1, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] - 1 > r) { l = i; r = i + z[i] - 1; }
    }
    return z;
}
```

**應用**：構造 `pattern + "$" + text`，計算 Z-array，找 `z[i] == m` 的位置

**選擇建議**：
- KMP：經典面試題，LPS 有額外應用（LC 459, LC 214）
- Z-Algorithm：程式碼稍短，Z-array 語意更直觀（「與前綴匹配長度」）

---

這份路徑涵蓋了 KMP 演算法的所有核心應用，從基礎字串匹配到序列化結構比對，幫助你完整掌握這個重要的線性時間匹配技術。
