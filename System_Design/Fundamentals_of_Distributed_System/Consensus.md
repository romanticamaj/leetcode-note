# 共識機制（Consensus）

**共識（Consensus）**是分散式系統中，讓多個節點在面對故障與網路延遲的情況下，仍能就某個值或決策達成一致的關鍵技術。

---

## 🎯 為什麼需要共識？

- 確保**資料一致性（Consistency）**
- 實現**領導者選舉（Leader Election）**
- 支援**狀態機複製（State Machine Replication）**
- 是**容錯協調（Fault-Tolerant Coordination）**的基礎

---

## 🧩 常見共識演算法

### 1. Paxos

- 理論基礎最完整的共識演算法。
- 容錯性強，但實作與理解較複雜。
- 被 Google Chubby 等系統採用。

### 2. Raft

- 為了易於理解而設計的共識演算法。
- 將共識拆解為：領導者選舉、日誌複製、安全性。
- 被 etcd、Consul 等廣泛採用。

### 3. Viewstamped Replication

- 與 Paxos/Raft 類似。
- 著重於主備架構與視圖切換（View Change）。

---

## ⚠️ 共識挑戰

- **網路分區（Network Partition）**：節點可能對領導者或狀態產生分歧。
- **腦裂（Split-Brain）**：若無法正確取得多數，可能出現多個領導者。
- **效能瓶頸（Performance）**：需多輪通訊與日誌同步。
- **一致性 vs 可用性**：共識偏向保證一致性（見 CAP 理論）。

---

## 🧠 核心概念

- **多數決（Quorum）**：需取得多數節點同意才能達成共識。
- **領導者選舉（Leader Election）**：由一個節點負責協調決策。
- **日誌複製（Log Replication）**：確保所有節點依序執行相同操作。

---

## ✅ 小結

共識是分散式系統中協調與一致性的基石。Raft 與 Paxos 提供強一致性保證，但需在效能與複雜度間做出取捨。
