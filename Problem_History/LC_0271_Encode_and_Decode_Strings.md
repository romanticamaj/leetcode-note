# 271. Encode and Decode Strings：字串邊界與分框的歷史

**記憶線索：串接會丟掉邊界；用長度保存邊界，或用分隔符搭配 escaping。**

Technique summary：`Length-Prefixed Serialization + Metadata/Payload Separation + Cursor Parsing`

來源查證與整理日期：2026-11-20。練習日期：2026-11-19。

## 1. 題目真正要保存什麼？

[LC 271](https://leetcode.com/problems/encode-and-decode-strings/)要求把字串序列轉成單一字串，再完整還原。這是 **serialization**；其中辨認各筆資料起訖的部分稱為 **framing**。

單純串接無法區分 `["ab", "c"]` 與 `["a", "bc"]`；單純用 `|` 分隔，又會與內容原有的 `|` 衝突。**必須額外表示邊界，且讓空列表與空字串也能區分。**

## 2. 可確認的歷史與教科書脈絡

| 資料 | 已確認的概念 | 與本題的關係 |
|---|---|---|
| Sun Microsystems，XDR，RFC 1014，1987 年 6 月，§3.9–3.12 | 可變長度資料／字串以前置長度表示；陣列可保存元素數，再逐一編碼元素 | 長度前綴與字串序列編碼的早期標準文獻證據 |
| D. J. Bernstein，Netstrings，1997-02-01 草案 | `decimal length:payload,`；可編碼任意 bytes，並將多個 netstrings 串接 | 非常接近本題的逐筆長度前綴設計 |
| Tanenbaum，《Computer Networks》，Framing 主題；WPI 2013 課程投影片第 7、9 頁 | Byte count、分隔符與 byte stuffing | 解釋為何「長度」與「escaping」是經典的邊界設計選擇 |

**這些證明概念早於 LeetCode，不證明 LC 271 直接改編自某書。** 目前未確認題目的官方首次發布日期、最初出題者或這類技術的最早發明者。Netstrings 文件是過期的 Internet-Draft，並非正式 RFC 標準。

## 3. 最經典的設計概念與關鍵行

以下為設計示意，假設輸入格式合法；不是完整 codec，也不是原文程式的逐字轉錄。

### A. 長度前綴：先知道讀多少，再讀內容

**關鍵：只在長度欄位尋找分隔符；內容一律按長度擷取。** 因此 payload 中出現數字、分隔符或空字串都不會破壞邊界。

```text
["a|b", ""] → 3|a|b0|
                  ↑ 讀完 3 bytes 後，才開始讀下一個長度
```

```cpp
encoded += to_string(part.size()) + '|' + part;
auto end = s.find('|', pos);
auto len = stoull(s.substr(pos, end - pos));
result.push_back(s.substr(end + 1, len));
pos = end + 1 + len;  // 下一個長度欄位
```

這是適合記憶的簡單基準。Netstrings 採相同的長度主導思路，但格式另要求 `:` 與尾端 `,`；尾端逗號可檢查預期邊界，不能用「搜尋下一個逗號」取代按長度讀取。[來源：Netstrings §2–3](https://datatracker.ietf.org/doc/html/draft-bernstein-netstrings-02#section-2)

### B. 固定寬度長度欄位：連長度本身的邊界也固定

**關鍵：前固定數量 bytes 是長度，後面指定數量 bytes 是資料。** 不必用文字分隔符結束長度欄位；跨機器時需約定 byte order。

```text
[4-byte length][payload][padding（若協定要求）]
```

```cpp
write_u32_be(length);  // 示意 helper：以固定 4 bytes、大端序寫入
write_bytes(payload);
```

XDR 的長度是 4-byte unsigned integer，字串後另補 0–3 個零 bytes 對齊；這些是 XDR 的格式要求，不能省略後仍稱為 XDR 編碼。它也區分 ASCII string 與可存任意 bytes 的 opaque data。[來源：RFC 1014 §3.9–3.10](https://www.rfc-editor.org/rfc/rfc1014.html)

### C. 分隔符＋escaping：讓控制符號與資料符號可區分

**關鍵：內容若包含分隔符或 escape 本身，先加 escape；解碼必須記得「下一個字元是普通資料」。**

```cpp
if (c == separator || c == escape) encoded += escape;
encoded += c;
// 解碼：遇 escape 就按字面讀下一個字元；未跳脫的 separator 才結束一筆
```

只有「挑一個少見符號」不夠；輸入可能包含任意符號。另需明確約定空列表、空字串與每筆結束符號的表示。網路教材的 byte stuffing 說明的就是避免控制符號與 payload 衝突，但完整網路 frame 不等同 LC 字串格式。[來源：WPI，第 9–10 頁](https://web.cs.wpi.edu/~rek/Grad_Nets/Spring2013/Framing_and_Stuffing_S13.pdf)

### D. 本次實作：集中長度表，分開 metadata 與 payload

**關鍵：先界定長度表本身的邊界，再用表中長度逐段消耗內容。** 這是本次程式的配置方式，不宣稱它就是 XDR 或 netstrings 格式。

```text
[metadata byte 長度]|[每筆長度|...][串接的 payload]
["a", "saf"] → 4|1|3|asaf
```

```cpp
return to_string(meta.size()) + '|' + meta + content;
const auto metaEnd = metaPos + metaLength;
auto contentPos = metaEnd;
result.push_back(s.substr(contentPos, length));
metaPos = lengthEnd + 1;  // 下一個長度欄位
contentPos += length;    // 下一段內容
```

Invariant：`metaPos` 指向下一個長度欄位；`contentPos` 指向尚未消耗內容的起點。`metaEnd` 是 metadata 的 **exclusive end**，也是 content 起點。

與逐筆長度前綴相比，這個版本多維護一條 metadata cursor；正確性同樣來自按長度讀 payload，不必搜尋內容中的分隔符。

## 4. 這次 index／length 的重點

- `substr(start, length)` 第二參數是**長度**，不是結束 index：區間 `[start, end)` 要寫 `end - start`。
- 最前面保存的是 metadata 的 **byte 長度**；content 起點由 `metaPos + metaLength` 算出，不是直接儲存的絕對 index。
- C++ `string::size()` 計 bytes；長度與擷取必須採同一單位，不要混用 Unicode 字元數。
- 空列表是 `0|`；一個空字串是 `2|0|`，格式可區分兩者。

## 5. 參考資料

1. **Sun Microsystems，RFC 1014: XDR: External Data Representation Standard，1987。** [原文](https://www.rfc-editor.org/rfc/rfc1014.html)。§3.9 opaque bytes、§3.10 string、§3.12 variable-length array；支持長度前綴、對齊與序列表示的歷史證據，不據此聲稱首創。
2. **D. J. Bernstein，Netstrings，draft-bernstein-netstrings-02，1997-02-01。** [原文與文件狀態](https://datatracker.ietf.org/doc/html/draft-bernstein-netstrings-02)。§1–3 說明任意 byte string、串接、遞迴編碼與關鍵讀寫方式。
3. **WPI，Framing and Stuffing，Spring 2013 課程教材。** [PDF](https://web.cs.wpi.edu/~rek/Grad_Nets/Spring2013/Framing_and_Stuffing_S13.pdf)。第 7 頁將 byte count／stuffing 分類標註來源為 Tanenbaum；第 9–10 頁說明 escaping。用於對照《Computer Networks》的 framing 主題，並非已核對所有版次的原書頁碼。
