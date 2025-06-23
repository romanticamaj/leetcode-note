# 資料複製（Replication）

**資料複製（Replication）**是將相同資料儲存於多個節點的技術，目的是提升容錯性、可用性與效能。

---

## 🎯 為什麼要做資料複製？

- **容錯（Fault Tolerance）**：某個節點故障時，其他副本仍可提供服務。
- **高可用性（High Availability）**：系統在部分失效下仍能運作。
- **負載平衡（Load Balancing）**：讀取請求可分散至多個副本。
- **降低延遲（Latency Reduction）**：可從地理上較近的副本讀取資料。

---

## 🧩 複製類型

### 1. 同步複製（Synchronous Replication）

- 所有副本都確認寫入成功後，才回應客戶端。
- 保證強一致性（Strong Consistency）。
- 延遲較高，效能受限於最慢副本。

### 2. 非同步複製（Asynchronous Replication）

- 主節點寫入後立即回應，副本稍後再同步。
- 效能佳、可用性高。
- 可能出現短暫不一致。

### 3. 半同步複製（Semi-Synchronous Replication）

- 至少一個副本確認後才回應。
- 在一致性與效能間取得平衡。

---

## 🔁 複製架構

- **主從架構（Master-Slave / Primary-Replica）**

  - 主節點負責寫入，從節點僅做讀取。
  - 架構簡單，但主節點可能成為瓶頸。

- **多主架構（Multi-Master）**

  - 多個節點皆可寫入。
  - 需處理衝突解決（Conflict Resolution）。

- **仲裁式架構（Quorum-Based）**
  - 使用投票機制決定操作是否成功（如多數決）。
  - 常見於 Cassandra、DynamoDB 等系統。

---

## ⚠️ 挑戰

- **一致性 vs 可用性**（CAP 著名權衡）
- **衝突處理**（特別是在多主架構中）
- **複製延遲**（非同步架構下）
- **網路分區與腦裂（Split-Brain）**

---

## ✅ 小結

資料複製是建構高可用分散式系統的基礎。選擇合適的複製策略，需根據系統需求在一致性、效能與容錯性間做出取捨。
