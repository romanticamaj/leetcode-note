# 快取機制（Caching）

**快取（Caching）** 是提升大型 Web 應用效能與可擴展性的關鍵技術，透過暫存常用資料，減少重複計算與資料庫存取。

---

## 🚀 為什麼要使用快取？

- **降低延遲（Latency）**：加快回應速度。
- **減少負載（Load Reduction）**：減輕資料庫與後端壓力。
- **提升可用性（Availability）**：即使後端暫時不可用，仍可回應快取資料。

---

## 🧩 快取類型

### 1. 用戶端快取（Client-side Caching）

- 瀏覽器快取、Service Worker。
- 適用於靜態資源（如圖片、CSS、JS）。

### 2. 邊緣快取（Edge Caching）

- CDN（Content Delivery Network）快取內容。
- 靠近使用者，降低延遲。

### 3. 伺服器端快取（Server-side Caching）

- 快取資料庫查詢結果、API 回應。
- 常用工具：Redis、Memcached。

---

## 🧠 快取策略

- **LRU（Least Recently Used）**：移除最久未使用的項目。
- **TTL（Time-To-Live）**：設定快取有效時間。
- **Write-through / Write-back / Write-around**：資料寫入與快取更新策略。

---

## ⚠️ 快取挑戰

- **快取失效（Cache Invalidation）**：何時更新或移除快取資料。
- **資料一致性（Stale Data）**：快取資料可能過期。
- **容量限制（Eviction Policy）**：如何選擇要移除的資料。

---

## ✅ 小結

快取是提升系統效能的利器，但需謹慎設計失效策略與一致性機制，才能兼顧速度與正確性。
