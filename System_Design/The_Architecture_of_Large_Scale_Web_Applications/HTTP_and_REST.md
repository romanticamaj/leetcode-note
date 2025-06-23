# HTTP 與 REST 架構風格（HTTP and REST）

**HTTP（HyperText Transfer Protocol）** 是網際網路上最常見的通訊協定，而 **REST（Representational State Transfer）** 是一種基於 HTTP 的架構風格，廣泛應用於 Web API 設計。

---

## 🌐 HTTP 基礎

- **協定層級**：應用層協定，基於 TCP。
- **無狀態（Stateless）**：每個請求獨立，伺服器不保留前一請求的狀態。
- **常見方法（HTTP Methods）**：
  - `GET`：取得資源
  - `POST`：建立資源
  - `PUT`：更新整個資源
  - `PATCH`：部分更新資源
  - `DELETE`：刪除資源

---

## 🧩 REST 架構風格

REST 是一種設計原則，並非標準。其核心理念是透過統一介面與資源導向的方式設計 API。

### REST 特性（六大約束）

1. **用戶端-伺服器（Client-Server）**
2. **無狀態（Stateless）**
3. **可快取（Cacheable）**
4. **統一介面（Uniform Interface）**
5. **分層系統（Layered System）**
6. **按需程式碼（Code on Demand, optional）**

---

## 🧱 RESTful API 設計實例

- `GET /users/123`：取得使用者資料
- `POST /users`：建立新使用者
- `PUT /users/123`：更新使用者資料
- `DELETE /users/123`：刪除使用者

---

## ✅ 小結

HTTP 是 Web 應用的基礎通訊協定，而 REST 則提供一套簡潔、可擴展的 API 設計方式。理解兩者對於設計現代 Web 系統至關重要。
