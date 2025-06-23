# Server-Sent Events (SSE)

**Server-Sent Events (SSE)** 是一種伺服器推送技術，允許伺服器在任何時候透過一個持久的 HTTP 連接，**單向**地將更新（事件）推送到客戶端。

它為需要從伺服器獲取即時更新，但不需要從客戶端向伺服器發送大量資料的場景提供了一種輕量級、標準化的解決方案。

---

## 核心概念

1. **單向通信 (Unidirectional Communication)**：SSE 的資料流是從**伺服器到客戶端**的。客戶端發起連接後，只能被動接收事件，而不能透過同一個連接向伺服器發送資料。這與 WebSocket 的全雙工通信形成鮮明對比。

2. **標準 HTTP 協定**：SSE 完全基於傳統的 HTTP/HTTPS 協定，不需要像 WebSocket 那樣進行協定「升級」。這使得它更容易部署，並且與現有的網路基礎設施（如代理、防火牆）有更好的相容性。

3. **自動重連 (Automatic Reconnection)**：這是 SSE 的一個關鍵特性。如果客戶端與伺服器之間的連接意外中斷，瀏覽器的 `EventSource` API 會自動嘗試重新建立連接。開發者可以自訂重連的間隔時間。

---

## 運作流程

1. **客戶端建立連接**：客戶端（通常是瀏覽器中的 JavaScript）創建一個 `EventSource` 物件，並指向伺服器上的一個特定端點 (Endpoint)。

   ```javascript
   const evtSource = new EventSource("/events");
   ```

2. **伺服器發送事件流**：伺服器接收到請求後，會發送一個特殊的 HTTP 回應，其 `Content-Type` 標頭為 `text/event-stream`，並保持該連接打開。

   ```http
   HTTP/1.1 200 OK
   Content-Type: text/event-stream
   Cache-Control: no-cache
   Connection: keep-alive
   ```

3. **伺服器推送事件**：伺服器會以一種特定的純文字格式，持續地向客戶端發送事件資料。每個事件由一個或多個 `key: value` 行組成，並以兩個換行符（`\n\n`）作為結束。

   ```
   event: user-login
   data: {"username": "JohnDoe", "timestamp": 1678886400}

   data: This is a simple message.

   id: 12345
   data: Another message with an ID.
   retry: 5000
   ```

   - `data`: 事件的資料內容。
   - `event`: 自訂事件類型，客戶端可以監聽特定類型的事件。如果省略，則為預設的 `message` 事件。
   - `id`: 事件的唯一標識符。如果連接中斷，瀏覽器會將最後收到的 `id` 透過 `Last-Event-ID` 標頭發送給伺服器，以便伺服器可以從中斷的地方繼續發送事件。
   - `retry`: 指示瀏覽器在連接中斷後應等待多少毫秒再嘗試重連。

4. **客戶端接收事件**：客戶端的 `EventSource` 物件會觸發相應的事件，開發者可以透過添加事件監聽器來處理這些資料。

   ```javascript
   // 監聽預設的 "message" 事件
   evtSource.onmessage = function (event) {
     console.log("Message received:", event.data);
   };

   // 監聽自訂的 "user-login" 事件
   evtSource.addEventListener("user-login", function (event) {
     const userData = JSON.parse(event.data);
     console.log("User logged in:", userData.username);
   });

   evtSource.onerror = function (err) {
     console.error("EventSource failed:", err);
   };
   ```

---

## 優點與缺點

### 優點

- **實現簡單**：基於標準 HTTP，客戶端和伺服器端的實現都比 WebSocket 簡單得多。
- **輕量級**：開銷小，特別適合只需要從伺服器接收更新的場景。
- **自動重連**：內建的重連機制簡化了錯誤處理。
- **相容性好**：可以輕鬆地通過大多數代理和防火牆。

### 缺點

- **單向通信**：最大的限制。如果客戶端需要向伺服器發送資料，必須透過另一個獨立的 HTTP 請求（如 `fetch` 或 `axios`），這會增加複雜性。
- **瀏覽器連接數限制**：瀏覽器對來自同一個域的 HTTP 連接數有限制（通常是 6 個）。打開一個 SSE 連接會佔用其中一個，可能會影響同頁面中其他資源的載入。
- **不支援二進位資料**：SSE 只能傳輸 UTF-8 格式的文字資料。

---

## 應用場景

SSE 是**伺服器到客戶端**單向更新的絕佳選擇：

- **新聞 Feed 或社交媒體動態更新** (如 Twitter 的即時動態)
- **股票市場或加密貨幣價格的即時看板**
- **體育賽事比分直播**
- **系統監控儀表板**的狀態更新
- **網站通知** (例如，"您的訂單已發貨")
