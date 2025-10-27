# Movement Constraint Transformation 解題心法

## 🧠 核心哲學

Transform complex swap/operation rules into simple movement constraints. Don't simulate the process - analyze the invariants.

**心法：從操作規則到移動約束**

```
Swap Rules → Movement Analysis → Position Constraints
    ↓              ↓                    ↓
"XL→LX"     "L moves left"      "i ≥ j"
"RX→XR"     "R moves right"     "i ≤ j"
```

## 核心概念：Three-Step Framework

### Step 1: Identify Invariants

What stays constant despite transformations?

```cpp
// Remove noise, check if relative order preserved
string s1 = extract_signal(start);
string s2 = extract_signal(result);
return s1 == s2;  // Invariant check
```

### Step 2: Extract Movement Rules

```cpp
// From swap rules to directional constraints
struct MovementRule {
    bool can_move_to(char element, int from, int to) {
        if (element == 'L') return from >= to;  // Can only move left
        if (element == 'R') return from <= to;  // Can only move right
        return from == to;
    }
};
```

### Step 3: Validate with Two Pointers

```cpp
bool can_transform(const string& start, const string& result) {
    int i = 0, j = 0;

    while (i < start.size() || j < result.size()) {
        // Skip noise
        while (i < start.size() && is_noise(start[i])) i++;
        while (j < result.size() && is_noise(result[j])) j++;

        if (i >= start.size() || j >= result.size()) break;

        // Check invariant and movement constraint
        if (start[i] != result[j]) return false;
        if (!can_move_to(start[i], i, j)) return false;

        i++; j++;
    }

    return i == start.size() && j == result.size();
}
```

## 適用場景 / Use Cases

- **Swap-based transformation**: LC 777, 809
- **Sliding puzzle validation**: 8-puzzle, 15-puzzle
- **String manipulation**: Character reordering with constraints
- **Game state validation**: Move legality checks

## ⏱️ 複雜度分析

| Approach             | Time                 | Space |
| -------------------- | -------------------- | ----- |
| Simulation (DFS/BFS) | O(n²) or exponential | O(n)  |
| Constraint Analysis  | O(n)                 | O(1)  |

## ✅ 關鍵要點 / Key Points

- [ ] **Analyze, don't simulate** - Find invariants instead of executing operations
- [ ] **Extract signal from noise** - Identify which elements are movable vs ignorable
- [ ] **Derive movement direction** - Each element type has directional constraints
- [ ] **Preserve relative order** - Most swap problems maintain element ordering
- [ ] **Validate positions directly** - Check if movement from `i` to `j` is legal

## 🎯 Mental Model

**Four Questions:**

1. **What changes?** Positions of elements
2. **What stays constant?** Relative ordering, element types
3. **What's allowed?** Directional movement constraints
4. **How to check?** Position relationship validation

**Anti-patterns:**

- ❌ Implementing DFS/BFS to try all swaps
- ❌ Tracking intermediate states
- ❌ Step-by-step simulation

**Correct approach:**

- ✅ Identify invariants (what cannot change)
- ✅ Extract movement constraints from rules
- ✅ Validate final positions directly
