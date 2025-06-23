# 多層式應用架構（N-tier Applications）

**N-tier 架構**是大型網路應用中常見的設計模式，將系統劃分為多個邏輯層（Tier），每層負責不同的功能，提升可維護性、可擴展性與安全性。

---

## 🎯 為什麼使用 N-tier 架構？

- **模組化（Modularity）**：每層專注於單一職責。
- **可擴展性（Scalability）**：可獨立擴充特定層級。
- **安全性（Security）**：可在層與層之間設置防火牆與存取控制。
- **可測試性（Testability）**：單元測試與整合測試更容易。

---

## 🧩 常見的三層架構（3-tier）

### 1. 表現層（Presentation Tier）

- 使用者介面（UI）
- 負責與使用者互動
- 例如：Web 前端、行動 App

### 2. 應用層（Application Tier / Logic Tier）

- 商業邏輯處理
- 接收請求、執行邏輯、調用資料層
- 例如：後端 API、服務層

### 3. 資料層（Data Tier）

- 資料儲存與存取
- 例如：資料庫、快取、檔案系統

---

## 🧱 延伸層級

- **快取層（Caching Tier）**：如 Redis、Memcached
- **訊息佇列層（Messaging Tier）**：如 Kafka、RabbitMQ
- **分析層（Analytics Tier）**：如 Spark、Presto

---

## ✅ 小結

N-tier 架構是設計大型應用的基礎，透過分層設計可提升系統的彈性、可維護性與可擴展性。
