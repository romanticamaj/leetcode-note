# WebSocket

**WebSocket** 是一種先進的網路通信協定，它在單一的、持久的 TCP 連接上提供**全雙工 (Full-Duplex)** 的通信通道。這意味著客戶端和伺服器可以在任何時候獨立地向對方發送資料，從而實現真正的即時 (Real-time) 互動。

WebSocket 被設計用來解決傳統 HTTP 協定的無狀態和請求-回應模式在即時應用中的低效率問題。

---

## 核心概念

1. **全雙工通信 (Full-Duplex Communication)**：與半雙工（一次只能一方發送）或單工（只能單向發送）不同，WebSocket 允許資料在兩個方向上同時流動，延遲極低。

2. **單一 TCP 連接 (Single TCP Connection)**：一旦建立連接，該連接將保持開放狀態，直到客戶端或伺服器明確將其關閉。所有後續的資料交換都透過這個連接進行，避免了重複建立和銷毀連接的開銷。

3. **狀態協定 (Stateful Protocol)**：與無狀態的 HTTP 不同，WebSocket 連接是有狀態的。伺服器需要維護每個活動連接的狀態，這增加了伺服器的複雜性，但也使得通信更加高效。

---

## WebSocket 握手 (Handshake)

WebSocket 連接的建立過程始於一個稱為「握手」的 HTTP 請求。

**運作流程：**

1. **客戶端發起升級請求**：客戶端（通常是瀏覽器）向伺服器發送一個標準的 HTTP GET 請求，但其中包含特殊的標頭 (Headers)，表示希望將連接「升級」到 WebSocket。

   ```http
   GET /chat HTTP/1.1
   Host: server.example.com
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
   Sec-WebSocket-Version: 13
   ```

   - `Upgrade: websocket`：明確告知伺服器，客戶端希望建立 WebSocket 連接。
   - `Connection: Upgrade`：表示這是一個協定升級請求。
   - `Sec-WebSocket-Key`：一個隨機生成的 Base64 編碼字串，用於基本的安全驗證，防止代理伺服器誤解請求。

2. **伺服器回應握手**：如果伺服器支援 WebSocket，它會返回一個 HTTP `101 Switching Protocols` 的回應，表示同意升級。

   ```http
   HTTP/1.1 101 Switching Protocols
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
   ```

   - `Sec-WebSocket-Accept`：伺服器使用客戶端的 `Sec-WebSocket-Key` 加上一個固定的 GUID 字串進行 SHA-1 加密和 Base64 編碼後生成，客戶端會驗證此金鑰以確認伺服器是真正的 WebSocket 伺服器。

3. **連接建立**：握手成功後，底層的 TCP 連接就從 HTTP 協定轉換為 WebSocket 協定。之後的所有通信都使用 WebSocket 的**資料幀 (Data Frames)** 格式，而不是 HTTP 請求/回應。

---

## 優點與缺點

### 優點

- **極低的延遲**：資料可以立即從伺服器推送到客戶端，無需等待客戶端請求，非常適合即時應用。
- **高效能與低開銷**：連接建立後，資料幀的標頭非常小（通常只有 2-10 字節），與龐大的 HTTP 標頭相比，大大減少了網路開銷。
- **真正的雙向通信**：伺服器和客戶端地位平等，都可以是資料的主動發起者。

### 缺點

- **伺服器狀態管理**：伺服器需要維護大量持久連接的狀態，這對伺服器的記憶體和架構設計提出了更高的要求。
- **瀏覽器支援性**：雖然現代瀏覽器都已支援，但在一些非常陳舊的環境中可能不可用。
- **代理與防火牆**：一些舊的網路代理或防火牆可能不理解 WebSocket 的升級請求，從而阻止連接建立。
- **沒有自動重連機制**：與 Server-Sent Events (SSE) 不同，如果 WebSocket 連接中斷，開發者需要自行實現重連邏輯。

---

## 應用場景

WebSocket 是需要高頻率、低延遲、雙向互動的應用的理想選擇：

- **線上多人遊戲**
- **即時聊天應用** (如 Slack, Discord)
- **協同編輯工具** (如 Google Docs, Figma)
- **金融交易平台和即時股票報價**
- **即時地理位置追蹤** (如 Uber)
- **體育賽事直播的比分更新**
