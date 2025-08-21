# Gary's DSA Cheatsheet

## Backtracking

| Category              | Keywords                                       |
| --------------------- | ---------------------------------------------- |
| **State Design**      | `Decision Boundary`, `Constraint`              |
| **Backtracking**      | `Promising Check`, `Choose, Explore, Unchoose` |
| **Solution Building** | `Base Case/Solution Reach`, `Combine/Collect`  |

---

## Dynamic Programming

**Progression:**

1. Exhaustive Search / Backtracking
2. Top-Down DP with Memoization
3. Bottom-Up DP with Tabulation
4. Bottom-Up DP with Space Optimization

**Advanced:**

- State Compression

---

## Sliding Window

**Mantra:** 擴張、修復、更新

---

## Number Theory

- **Primality Test**: `O(sqrt(n))` trial division. Loop condition: `for (long long i = 2; i * i <= n; ++i)`.
- **GCD / LCM**: Use `std::gcd` and `std::lcm` from `<numeric>` (C++17+).
- **Prime Factorization**: Trial division up to `sqrt(n)`. Remember to handle the remaining factor if `n > 1`.
