# 資料持久性與一致性（Data Durability and Consistency）

在分散式系統中，**資料持久性（Durability）**與**資料一致性（Consistency）**是確保資料可靠性與正確性的兩大核心目標。

---

## 🔒 資料持久性（Durability）

**資料持久性**確保當系統回應「寫入成功」後，即使發生故障（如斷電、當機），資料仍然不會遺失。

### 常見實作方式：

- **預寫日誌（Write-Ahead Logging, WAL）**：先記錄變更再執行。
- **資料複製（Replication）**：將資料備份到多個節點。
- **持久性儲存（Persistent Storage）**：使用具備持久性的儲存設備（如 SSD、HDD、雲端儲存）。
- **確認機制（Acknowledgment Protocols）**：僅在資料安全寫入後才回應成功。

---

## 🔁 資料一致性（Consistency）

**資料一致性**指的是所有節點在同一時間看到的資料是一致的。

### 一致性類型：

- **強一致性（Strong Consistency）**：所有讀取都能取得最新寫入的值。
- **最終一致性（Eventual Consistency）**：資料最終會在所有節點達成一致。
- **因果一致性（Causal Consistency）**：保證有因果關係的操作順序一致。
- **讀寫一致性（Read-Your-Writes）**：使用者能讀到自己剛寫入的資料。

### 著名權衡：

- **CAP 理論（CAP Theorem）**：在網路分區（Partition）發生時，系統最多只能保證以下三者中的兩個：
  - **一致性（Consistency）**
  - **可用性（Availability）**
  - **分區容忍性（Partition Tolerance）**

---

## 🧠 小結

- **Durability** 確保資料不會遺失。
- **Consistency** 確保資料在多節點間保持同步與正確。
- 兩者常與可用性與效能產生衝突，需根據應用場景做出設計取捨。
