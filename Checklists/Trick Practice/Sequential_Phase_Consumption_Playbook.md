# 🎯 Sequential Phase Consumption - 練習路徑

Sequential Phase Consumption 是一種設計思維，用於處理需要依序消費 sequential input 的問題。核心哲學是「假設合法，遇錯即停」，讓程式的 sequential structure 本身成為 implicit state machine。

詳細心法請參考：[Sequential_Phase_Consumption.md](../Algorithms/Design_Principles/Sequential_Phase_Consumption.md)

---

## 🏁 目標題總覽

| 題號   | 題目名稱                 | Pattern 特徵                      | 難度   |
| ------ | ------------------------ | --------------------------------- | ------ |
| LC 8   | String to Integer (atoi) | whitespace → sign → digits        | ⭐⭐   |
| LC 13  | Roman to Integer         | 逐字元消費 + lookahead            | ⭐     |
| LC 165 | Compare Version Numbers  | delimiter 分隔 + 逐段比較         | ⭐⭐   |
| LC 71  | Simplify Path            | delimiter + stack 處理            | ⭐⭐   |
| LC 468 | Validate IP Address      | IPv4 vs IPv6 分支                 | ⭐⭐   |
| LC 65  | Valid Number             | sign → integer/decimal → exponent | ⭐⭐⭐ |

---

## 🧭 練習路徑（依 Pattern 變體）

### 1️⃣ 基礎 Phase Consumption

- 📙 LC 8. String to Integer (atoi) ← 入門：三階段消費（whitespace → sign → digits）
- 📙 LC 13. Roman to Integer ← 單字元消費 + lookahead 判斷特殊組合

### 2️⃣ Delimiter-Based Parsing

- 📙 LC 165. Compare Version Numbers ← 以 `.` 分隔，逐段比較
- 📕 LC 71. Simplify Path ← 以 `/` 分隔，結合 stack 處理 `.` 和 `..`

### 3️⃣ Multi-Branch Validation

- 📕 LC 468. Validate IP Address ← IPv4 vs IPv6 兩種結構，需要分支判斷
- 📕 LC 65. Valid Number ← 最難：多分支 phase（sign、integer、decimal、exponent）

---

## ✅ 建議練習順序

1. **LC 8** → 基礎三階段，學會 Phase 結構
2. **LC 13** → 單字元 + lookahead，理解 optional phase
3. **LC 165** → delimiter 分隔，處理不等長的兩個序列
4. **LC 71** → 結合 stack，處理相對路徑
5. **LC 65** → 終極挑戰，複雜的多分支 phase
