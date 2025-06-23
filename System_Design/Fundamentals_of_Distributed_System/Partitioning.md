# 資料分區（Partitioning）

**資料分區（Partitioning）**，又稱為分片（Sharding），是將資料拆分成多個子集，分散儲存在不同節點上的技術，目的是提升系統的可擴展性與效能。

---

## 🎯 為什麼要做分區？

- **可擴展性（Scalability）**：可橫向擴充節點，分散儲存與計算壓力。
- **效能提升（Performance）**：每個節點只需處理部分資料。
- **容錯隔離（Fault Isolation）**：單一分區故障不會影響整體系統。

---

## 🧩 分區策略

### 1. 區間分區（Range-Based Partitioning）

- 根據資料值的範圍進行分區（例如：userId 1–1000）。
- 簡單直觀，但容易產生資料傾斜（hotspot）。

### 2. 雜湊分區（Hash-Based Partitioning）

- 對 key 做雜湊後決定分區。
- 分布較平均，但不利於範圍查詢。

### 3. 目錄分區（Directory-Based Partitioning）

- 使用查詢表記錄 key 與分區的對應關係。
- 彈性高，但需額外維護目錄資訊。

---

## ⚠️ 分區挑戰

- **重分佈（Rebalancing）**：新增或移除節點時需重新分配資料。
- **資料傾斜（Skew）**：某些分區資料量或流量過高。
- **跨分區查詢（Cross-Partition Queries）**：JOIN 或交易操作變得複雜。
- **網路分區（Partition Tolerance）**：分區之間可能因網路問題而失聯（見 CAP 理論）。

---

## 🧠 設計建議

- 選擇能平均分布的分區鍵（Partition Key）。
- 監控各分區的資料量與存取頻率。
- 使用一致性雜湊（Consistent Hashing）降低重分佈成本。

---

## ✅ 小結

資料分區是打造可擴展分散式系統的關鍵技術。選擇合適的分區策略，需考量資料特性、查詢模式與系統彈性。
