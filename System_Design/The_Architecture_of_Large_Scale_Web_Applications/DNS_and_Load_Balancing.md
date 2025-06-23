# DNS 與負載平衡（DNS and Load Balancing）

在大型 Web 應用中，**DNS（Domain Name System）** 與 **負載平衡（Load Balancing）** 是實現高可用性與可擴展性的關鍵基礎設施。

---

## 🌐 DNS（Domain Name System）

DNS 是將人類可讀的網域名稱（如 `example.com`）轉換為 IP 位址的系統。

### 功能與特性

- **名稱解析（Name Resolution）**：將域名轉換為伺服器 IP。
- **快取（Caching）**：減少查詢延遲與 DNS 伺服器負載。
- **TTL（Time-To-Live）**：控制快取有效時間。
- **DNS 負載平衡**：透過多個 A 記錄實現簡單的流量分散。

---

## ⚖️ 負載平衡（Load Balancing）

負載平衡器負責將進來的請求分配到多個後端伺服器，以提升效能與容錯能力。

### 類型

#### 1. DNS 層級負載平衡

- 透過 DNS 回傳多個 IP。
- 簡單但無法感知後端健康狀態。

#### 2. 第四層（L4）負載平衡

- 基於 TCP/UDP 層（如 IP、Port）進行分流。
- 效能高，常用於內部服務。

#### 3. 第七層（L7）負載平衡

- 基於 HTTP 層（如 URL、Header）進行智慧分流。
- 支援路由、認證、快取等功能。

---

## 🧠 策略與演算法

- **輪詢（Round Robin）**
- **最少連線（Least Connections）**
- **IP 雜湊（IP Hashing）**
- **健康檢查（Health Checks）**

---

## ✅ 小結

DNS 與負載平衡是大型系統的第一道防線，能有效分散流量、提升可用性與容錯能力。選擇合適的策略與層級，對系統穩定性至關重要。
