# Map as Unified Validation-Transformation 心法

## 🧠 核心哲學

When a problem requires both **validation** (is X valid?) and **transformation** (what does X map to?), using a **map unifies both concerns** into a single elegant data structure. The map's presence validates, and its value transforms.

## 核心概念：Validation-Transformation Duality

```cpp
// ❌ Scattered approach: separate validation and transformation
unordered_set<char> invalid = {'2', '3', '4', '5', '7'};
unordered_set<char> same = {'0', '1', '8'};
// ... then multiple if-statements for transformation logic

// ✅ Unified approach: map does both
unordered_map<char, char> mapping = {
    {'0','0'}, {'1','1'}, {'8','8'},  // self-mapping
    {'6','9'}, {'9','6'}              // pair-mapping
};
// Not in map = invalid, map[key] = transformation
```

**Key Insight**: If `key ∉ map` → invalid; if `key ∈ map` → valid, and `map[key]` gives the transformation.

## 通用模板

```cpp
// Problem: Check if input satisfies bidirectional/symmetric constraints
bool validateWithTransform(const string& input) {
    // Define all valid mappings (presence = validation)
    unordered_map<char, char> mapping = {
        // Add all valid transformations
    };

    int left = 0, right = input.size() - 1;

    while (left <= right) {
        // Validation via map lookup
        if (!mapping.contains(input[left])) return false;  // Invalid

        // Transformation check
        if (input[right] != mapping[input[left]]) return false;

        left++;
        right--;
    }
    return true;
}
```

## 🧩 設計模式對比

### Pattern 1: Scattered Sets + Conditionals (Anti-Pattern)

```cpp
// Multiple sets for different validation categories
const unordered_set<char> invalid = {'2', '3', '4', '5', '7'};
const unordered_set<char> selfMap = {'0', '1', '8'};

if (invalid.contains(c)) return false;
if (selfMap.contains(c) && other != c) return false;
if (c == '6' && other != '9') return false;  // Scattered transformation
if (c == '9' && other != '6') return false;
```

**Issues**: Logic scattered across multiple structures, transformation rules hardcoded in conditionals.

### Pattern 2: Unified Map (Recommended)

```cpp
unordered_map<char, char> mp = {
    {'0','0'}, {'1','1'}, {'8','8'}, {'6','9'}, {'9','6'}
};

if (!mp.contains(c)) return false;        // Validation
if (other != mp[c]) return false;         // Transformation
```

**Benefits**: Single source of truth, declarative mapping, easy to extend.

## 適用場景

| Problem Type                                 | Map Pattern             | Set Pattern             |
| -------------------------------------------- | ----------------------- | ----------------------- |
| **Bidirectional validation** (A↔B)           | ✅ `map[A]=B`           | ❌ Need separate logic  |
| **Symmetric constraints** (palindrome-like)  | ✅ Self + pair mappings | ❌ Multiple sets needed |
| **Character substitution cipher**            | ✅ Explicit mapping     | ❌ Can't represent      |
| **Pure existence check** (no transformation) | ❌ Overkill             | ✅ `set.contains()`     |

## ⏱️ 複雜度分析

Both approaches have O(1) lookup, but map pattern has:

- **Better maintainability**: Single data structure
- **Cleaner logic**: No scattered conditionals
- **Easier to extend**: Add new mappings without touching code

## ✅ 關鍵要點

- [ ] Use **map** when validation implies a specific transformation/mapping
- [ ] Use **set** when you only need existence checks (no transformation)
- [ ] Map's `.contains()` returning false = validation failure (not in valid set)
- [ ] Map's `.second` = the expected transformation result
- [ ] Declarative mappings > imperative conditionals for clarity

## 相關題目

- LeetCode 246 (Strobogrammatic Number) - bidirectional digit mapping
- LeetCode 205 (Isomorphic Strings) - character bijection validation
- LeetCode 290 (Word Pattern) - pattern matching with transformation
