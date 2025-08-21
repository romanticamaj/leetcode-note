# 數論應用：LeetCode 實戰模式

本篇文檔旨在將前面介紹的質數判斷、質因數分解、GCD 和 LCM 等理論知識，與 LeetCode 中常見的算法問題模式相結合。

## 1. 利用質因數分解

質因數分解是解決許多與「因數」相關問題的萬能鑰匙。一旦我們將一個數 `n` 分解為 `p1^a1 * p2^a2 * ... * pk^ak` 的形式，許多問題便迎刃而解。

### 模式一：計算因數個數

一個數 `n` 的因數個數，可以通過其質因數分解的指數快速計算得出。

- **公式**: `(a1 + 1) * (a2 + 1) * ... * (ak + 1)`
- **原理**: 對於每個質因數 `pi`，它可以貢獻 `0, 1, ..., ai` 共 `(ai + 1)` 種冪次到最終的因數中。根據乘法原理，將所有質因數的冪次選擇數相乘，即為總的因數個數。

### 模式二：計算因數之和

一個數 `n` 的所有正因數之和，同樣可以通過質因數分解計算。

- **公式**: `(1+p1+...+p1^a1) * (1+p2+...+p2^a2) * ... * (1+pk+...+pk^ak)`
- **原理**: 每一項都是一個等比數列的和。最終結果是這些等比數列和的乘積。

## 2. GCD 與 LCM 的應用

### 模式三：分數化簡

- **概念**: 化簡分數 `a/b`，只需要將分子和分母同時除以它們的最大公因數。
- **公式**: `simplified_a = a / gcd(a, b)`，`simplified_b = b / gcd(a, b)`。

### 模式四：數組的 GCD / LCM

- **概念**: 求解一個數組中所有元素的 GCD 或 LCM，可以通過迭代的方式完成。
- **遞推關係**:
  - `gcd(a, b, c) = gcd(gcd(a, b), c)`
  - `lcm(a, b, c) = lcm(lcm(a, b), c)`

### 模式五：判斷互質

- **概念**: 判斷兩個數 `a` 和 `b` 是否互質（coprime），即它們是否沒有大於 1 的公因數。
- **條件**: `gcd(a, b) == 1`
- **應用**: 在許多問題中作為一個關鍵的約束條件出現，例如與中國剩餘定理相關的某些問題。

## 3. 相關 LeetCode 問題類型

- **因數與倍數**:
  - LeetCode 2427. Number of Common Factors
  - LeetCode 507. Perfect Number
- **GCD/LCM 應用**:
  - LeetCode 914. X of a Kind in a Deck of Cards (GCD)
  - LeetCode 1979. Find Greatest Common Divisor of Array
  - LeetCode 2413. Smallest Even Multiple (LCM)
- **質數相關**:
  - LeetCode 204. Count Primes (需要篩法)

## 4. 相關主題

- [質數判斷](01-Primality_Test.md)
- [質因數分解](02-Prime_Factorization.md)
- [最大公因數 (GCD) 和最小公倍數 (LCM)](03-GCD_and_LCM.md)
