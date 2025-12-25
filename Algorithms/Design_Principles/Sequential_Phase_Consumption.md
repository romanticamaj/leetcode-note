# Sequential Phase Consumption 心法

## 🧠 核心哲學

當處理需要依序消費 sequential input（如 string parsing）的問題時，有兩種截然不同的設計思維：

| 思維                   | 特徵                                         | 問題                    |
| ---------------------- | -------------------------------------------- | ----------------------- |
| **追蹤狀態，逐一驗證** | 大量 boolean flags (`spaceRead`, `signRead`) | flag 爆炸、if-else 地獄 |
| **假設合法，遇錯即停** | Phase 結構，每個 phase 專注一件事            | 清晰、可維護            |

**關鍵洞察**：程式的 sequential structure 本身就是 implicit state machine，不需要 explicit `enum State`。

- **Phase 順序即 FSM**：Phase 1 結束 → 隱含「已離開該狀態」
- **Declarative（聲明式）設計**：定義「期望什麼」，而不是「遇到什麼做什麼」

---

## 核心概念

### 1️⃣ Phase 順序即 FSM

不需要 `bool spaceRead, signRead, zeroRead` 等狀態追蹤。

```
Phase 1 完成 → 隱含「已經離開 Space 狀態」
Phase 2 完成 → 隱含「已經離開 Sign 狀態」
Phase 3 進行中 → 隱含「正在 Digit 狀態」
```

程式的結構本身就是狀態機。

### 2️⃣ Optional Phase 自然退化

每個 phase 都是 optional 的，不 match 就 fall through：

- Phase 1 (Whitespace)：沒有空白？直接進入 Phase 2
- Phase 2 (Sign)：沒有符號？直接進入 Phase 3
- Phase 3 (Digits)：沒有數字？while 不進入，自然 return 0

**不需要特別處理「沒有 X」的情況**。

### 3️⃣ 數學公式吸收 Corner Cases

| Corner Case   | 如何被吸收                        |
| ------------- | --------------------------------- |
| 空字串        | Phase 3 的 while 不進入，return 0 |
| 只有空白      | 同上                              |
| 只有 sign     | 同上                              |
| Leading zeros | `0 * 10 + 0 = 0`，自然處理        |

**讓數學公式和 loop 條件自然處理邊界**，而不是逐一特判。

### 4️⃣ Grammar-as-Pattern

用簡化 regex 視角看合法輸入，例如 `atoi` 的合法格式：

```
^\s*[+-]?\d+
```

- `^\s*`：leading spaces（greedy）
- `[+-]?`：optional sign（at most one）
- `\d+`：at least one digit

**Corner case 不是逐個記，而是看是否 match grammar**。

---

## ⚠️ 紅旗警告

> 當你開始出現一堆 `spaceRead / signRead / zeroRead` 這種 boolean flag 時，就代表該用 Phase 結構重構了。

---

## 🧩 核心設計模式

```
Phase N: Attempt to consume expected pattern
         → Match: consume and advance
         → No match: fall through to next phase (不是 error)
```

**Phase 的三種消費模式**：

| 消費模式                            | 語義               | 適用場景                       |
| ----------------------------------- | ------------------ | ------------------------------ |
| **Greedy (`while`)**                | 消費所有符合條件的 | prefix, main content           |
| **Single (`if`)**                   | 最多消費一個       | delimiter, sign                |
| **Conditional (`if` + validation)** | 消費並驗證         | main content with bounds check |

**設計要點**：

- **順序即狀態**：不需要 explicit state variable
- **Fall-through 即轉移**：不需要 explicit transition logic
- **Loop 不進入即終止**：不需要 explicit error handling

---

## 📚 適用場景

- String to Integer (atoi) - LC 8
- Parse decimal/hex/binary numbers
- Simple tokenizer
- Version string parsing (e.g., "v1.2.3")
- URL/path component parsing

---

## 相關模式

**Boundary-Driven Processing**：處理重複性區段結構（如 run-length encoding）時，採用「先找邊界，再處理」的策略。詳見 [Boundary_Driven_Processing.md](Boundary_Driven_Processing.md)。

---

## 與 Explicit DFA（Deterministic Finite Automaton）的區別

| Pattern                          | 特徵                          | 適用場景                       |
| -------------------------------- | ----------------------------- | ------------------------------ |
| **Sequential Phase Consumption** | 隱式 FSM，程式結構即狀態      | 簡單線性 parsing               |
| **Explicit DFA**                 | `enum State` + `transition()` | 複雜狀態轉移、需要回溯或多路徑 |

當問題變得更複雜（如 LC 65 Valid Number），可能需要考慮 Explicit DFA 設計。
