# 刷題日誌

---

## 2026-11-09

- 957. Prison Cells After N Days
- 16. 3Sum Closest
- 165. Compare Version Numbers
- 348. Design Tic-Tac-Toe

**心得**：
- 957：靠 gpt-6.1-sol 提示的……其實滿難的。Simulation + Cycle Detection + Fast Forwarding。
  1. 要想到內部的狀態會重複（2^6 = 64 個可能）。
  2. 要想到可以用 cycle 加速；cycle 的循環設計要靠 unordered_map 去紀錄時間，這邊最難。

  - 看了解答後的補充：這題非常酷！純粹做狀態改變滿容易，但還能思考狀態是否重複（repetition）；對應 BUD optimization 的 duplicate，重複後進入 cycle，便能 fast forward。這是我第一次在這題看到 fast forward，很值得整理成一篇。
  - 表示法：只有 2^6 種後續狀態，可以用 bitmap／bitmask 表示，再用 bit manipulation 記錄與更新狀態。

- 16：3Sum 概念去改：sort + two pointers。

- 165：完全靠 gpt-6.1-sol 提示……這題完全是在考 getline 操作啊。getline 回傳值用 boolean 決定要不要往下。
  - Takeaway：getline 回傳可以轉 bool，判斷是否成功；取得的 token 可能保留舊值，所以 getline 沒有成功時不能使用 token。
  - `bool has1 = static_cast<bool>(getline(ss1, token1, '.'));` 搭配 `const int num1 = !has1 ? 0 : std::stoi(token1);`，這兩行太經典了，加入 C++ One-Liners。

- 348：hashmap + bit manipulation。不難，但是不好實作，很容易出錯。
  - 看完解答後，可以把 counting 跟 player 的貢獻數量結合，就不用兩個變數。這個優化滿有趣的，因為我就是想朝這個方向簡化程式，這樣才不容易在實作時出錯。

**LLM 點評**：
model: GPT-6
- 957：經提示完成週期加速版；11/8 的端點重設除錯與當時未完成狀態保留為歷程。有限狀態還要搭配「同一狀態的下一天唯一確定」，才能推論重複後整段未來也會重複；第一天後兩端為 0，只剩 64 種內部狀態，初始狀態可能在循環外，不必另找多組大循環。提供的實作用 map 存上次出現時的剩餘天數，第一次重複時 cycleLength=舊剩餘天數-目前剩餘天數，再 n%=cycleLength 跳過整輪。n+1 是找到週期前不影響取餘的哨兵值。首次跳躍後 map 混用不同剩餘天數基準，後續差值未必等於最小週期，但此版剩餘天數已不足一輪，後續取餘不再改變它；若想讓 invariant 更清楚，可只在第一次重複時跳躍。C++20 編譯提供的原始版本，全部 256 個初始狀態搭配 n=1..256、999999999、1000000000 與每個狀態 50 個隨機大天數，共 78848 組對照皆通過。固定 8 格時，找到重複並模擬餘數只需有界次數，時間及額外空間均 O(1)，不再隨原始 n 增長；目前是 hashmap cycle detection，Floyd 是另一種偵測方法，尚未實作。這題的重點是狀態數、確定性轉移、時間標記語義與餘數跳躍，不只是套一個 unordered_map。 延伸心得成立，但要補上確定性轉移前提，且初始兩端可能為 1，完整八格自然以 8-bit 編碼；2^6 是第一天後的狀態數上界。Fast forwarding 減少步數，bitmask 改善表示與轉移成本，不須綁在一起。已整理 [狀態循環與快速跳躍心法](../Algorithms/Simulation/02-Cycle_Detection_and_Fast_Forward.md)，連回 BUD 與既有 state compression；位元轉移為理解解答後的延伸，尚未回報獨立實作。
- 16：從 3Sum 延伸排序＋固定一個元素＋雙指標的方向成立；目標改為追蹤與 target 的最小絕對差，而不是只找相等或列舉不重複組合。每次移動前更新最佳候選；sum < target 時，對目前 left 而言，縮小 right 只會更小、更遠，因此可排除目前 left；sum > target 時對稱排除目前 right；相等已達差值 0，可提早結束。排序 O(n log n)、各固定元素的雙指標掃描 O(n)，合計 O(n²)。可對照既有 [3Sum 筆記](../Data_Structures/Arrays_and_Strings/K-Sum_Problems/02-Three_Sum.md)。本次僅依心得確認方法，未提供程式碼，不判定具體實作或執行結果。
- 165：依使用者回報記錄為經提示完成；最後貼出的完整程式漏了 has1 的宣告／第一次 getline，須補回隨後列出的那一行，不能將原樣程式視為可編譯版本。核心仍是逐段比較 revision 的數值、忽略前導零、缺少段補 0；getline 是本次卡住的 parsing API 契約。兩個 stream 必須每輪獨立讀取，不能放在 || 兩側造成短路；用兩次讀取的成功旗標決定停止與補零，不能由 token.empty() 判斷是否成功，因 stream 已在 EOF 時再次讀取可能保留舊值而無限迴圈。getline 回傳的是 stream，轉 bool 表示本輪成功，不是 stoi 轉換成功；一般輸入即使成功仍可能讀到空欄位，兩行補零寫法以題目的非空數字 revision 為前提。最後一段可成功讀出並設 eofbit，不能只用 eof() 當成功判斷。令 m,n 為兩字串長度，時間 O(m+n)（等價於 O(max(m,n))），兩個 stringstream 與 token 的額外儲存為 O(m+n)。已補入 [C++ One-Liners](../Cheatsheet/CPP_One_Liners.md)；前次已執行 EOF token 保留的重現測試，本次原樣缺行程式未執行。
- 348：修正後提供的實作，在合法落子、格子不重複、勝負確定後不再呼叫 move 的題目前提下，從 invariant 推理看正確，本次未編譯或執行該份 C++。具體分類是 Array Counting + Player Bitmask，而非實際使用 hashmap：每條線的 count 記落子格數，OR mask 記曾出現的玩家集合，count==n 且 mask==(1<<player) 表示線已滿且只有該玩家。一次落子只影響一行、一列，以及其所在的主／反對角線；count 與 mask 必須在相同的位置條件內更新，否則非對角線落子會污染 mask。原先誤將兩條 diagonal mask 無條件更新，已經修正為 row==col 與 row+col==n-1 分別包住 count／mask 更新；中心格可以同時更新兩條，不能改成 else if。每次 move O(1)，建構初始化 O(n)，額外空間 O(n)；不需要存整張 O(n²) 棋盤，因為題目保證落子合法。重點是局部更新的範圍與兩種摘要資訊保持一致，而不是每步重掃勝利線。 看解答後理解 Signed Contribution Counting：玩家 1 貢獻 +1、玩家 2 貢獻 -1，每條線只保存兩者數量差；由於一條線至多 n 個合法落子，sum==n 必為玩家 1 占滿，sum==-n 必為玩家 2 占滿，因此不需另外保存總格數與玩家集合。這是依「只判斷是否同玩家占滿」的目標選擇充分摘要，不需還原各玩家完整落子數；減少需要同步更新的狀態，降低漏改某個欄位的風險，仍須保留對角線的成員條件。時間／空間維持每步 O(1)／O(n)，主要改善狀態數與實作清晰度。此版目前為看解答後的理解，尚未回報獨立實作。 已整理 [Signed Contribution Counting 心法](../Algorithms/Design_Principles/Signed_Contribution_Counting.md)，保留每條線容量上界的證明與摘要不能回答的問題。

---

## 2026-11-08

- 937. Reorder Data in Log Files
- 126. Word Ladder II
- 387. First Unique Character in a String

**心得**：
- 937：string manipulation。comparator 寫錯了：小於沒問題，但是第二個判斷式要第一個判斷式是等於才觸發。

- 126：BFS with level-conditioned predecessor push + backtracking。
  1. BFS 需紀錄一個 distance。
  2. 每個被拜訪的 neighbor 要確認搭配 queue 中紀錄的 distance 值；level 比較大的那些 node 就不再放進 queue，但是要更新 predecessor 清單。
  3. 建構 path 的 walk 要用 recursive，然後反向順序。
  4. Edge case：要判斷 destination 存在。
  5. Pitfall：要確認有 path 才輸出 path。

- 387：hashmap。

- 957：Prison Cells After N Days（除錯中，尚未完成）。Simulation，使用 next buffer 與 cells.swap(next)，看不出來問題在哪。

**LLM 點評**：
model: GPT-6
- 937：最後提供的 comparator 從邏輯推理看正確，本次未編譯或執行原始 C++。排序 key 是 (content, identifier)：content 較小就排前面，只有 content 相等時才用 identifier 決勝；不能把兩個「小於」條件直接 OR，否則可能 comp(a,b) 與 comp(b,a) 同時為 true，違反 strict weak ordering。先分流再排序 letterLogs，digitLogs 依原順序 push_back，最後接回即可保留數字 log 的穩定順序，無需對它們排序。依題目每個 log 內容全為小寫字母或數字且無尾端空白的保證，isdigit(log.back()) 可正確分類；substr(mid) 雖包含分隔空格，但每份 content 都多同一個前導空格，不影響比較結果，可用 mid+1 讓意圖更清楚。令 n 為 log 數、a 為 letter-log 數、L 為最長 log 長度，分流與輸出涉及字串複製，單次 comparator 的 find／substr／compare 最壞 O(L)，總時間 O(nL+a log(a+1)·L)，最壞 O(nL log(n+1))；額外空間 O(nL)，不能只算字串物件個數。for (const auto& log : logs) 可省去迴圈變數複製，comparator 可用 const auto& a／b 表達唯讀。
- 126：分類是 BFS 建立最短路徑 predecessor DAG＋DFS/backtracking 列舉所有最短路徑；提供的程式在題目單字等長、唯一且 beginWord != endWord、每個 Solution 物件呼叫一次的前提下，從 invariant 推理看正確，本次未編譯或執行原始 C++。distances 追蹤從起點到各單字的最少邊數；首次發現 neighbor 才設定距離並入隊，之後已訪問的 neighbor 不重複入隊，但只有 dist+1 == distances[neighbor] 的到達才能補進 predecessor，較長路徑不能補。原碼的 <= 在單位邊權 FIFO BFS 下等價於 ==，因較短的新到達不可能發生；建議直接用 == 表達最短路徑邊的 invariant。每條 predecessor 邊都使距離減一，故形成 DAG，不會循環；walk 的 push／遞迴／pop 是 backtracking，從 endWord 走回 beginWord 後 reverse 即得到正向路徑。Recursive 是自然的實作選擇，並非唯一方法。endWord 出隊時才 break 安全，因所有距離 D-1 的父節點都已展開，所有最短 predecessor 已收齊；不能改成第一次發現 endWord 就立刻停止整個 BFS。reachDestination 避免把沒有 predecessor 的孤立終點錯當有效路徑；在已達終點且 predecessor 僅保留最短邊的前提下，walk 遇到無 predecessor 的節點必為 beginWord。現有 BFS 已能處理 endWord 不在字典或存在但不可達，皆回傳空結果；預先檢查字典是否含 endWord 是提早回傳優化，不是正確性必要條件。相較 127，不能照搬每次掃完 wildcard bucket 立即 clear 的優化，可能漏掉同層其他父節點。若支援同物件重複呼叫，入口需 paths.clear()。令 N 為字典大小、L 為字長、P 為最短路徑數、D 為每條路徑單字數；固定 26 字母與 hash table 平均查找假設下，建圖及 BFS 為 O((N+1)L²)，回溯與字串輸出為 O(PDL)，不能忽略可能很大的輸出量。
- 387：提供的實作在小寫英文字母的前提下，從 invariant 推理看正確，本次未編譯或執行原始 C++。第一輪取得全字串的頻率，第二輪按原索引遞增找第一個 frequency==1 的位置，因此同時滿足「唯一」與「最早」；全無則回傳 -1。概念是 frequency counting，具體用 array<int,26> 作 direct-address table，而非實際使用 hashmap。兩輪各 O(n)，合計 Θ(n)；frequency 固定 26 格，所以演算法額外工作空間 O(1)，不是 O(n)。若將 string s 值傳遞從 lvalue 產生的輸入副本也計入，該副本另占 O(n)，需與計數工作空間分開；一般字元集合則可寫 O(Σ)，Σ 為字母表大小。frequency{0} 會把其餘元素也零初始化。最壞必須檢查整個字串以確認是否唯一，故 Ω(n) 的 BCR 判斷成立。
- 957：核心 bug 是只在迴圈外把 next 的端點設為 0；swap 後 next 持有上一輪的 cells（第一次 swap 後就是原始輸入），下一輪只覆寫中間六格，可能把原始非零端點換回結果。應在每一輪、swap 前重新設定 next.front()=next.back()=0，以維持 next 完整表示下一天的 invariant。以 C++14 重現原邏輯：[1,0,0,0,0,0,0,0]、n=2 時原結果 [1,0,0,1,1,1,0,0]，正確為 [0,0,0,1,1,1,0,0]；將端點重設放進每輪後，全部 256 個初始狀態搭配 n=1..10 的 2560 組模擬對照皆通過。固定 8 格時逐日模擬時間 O(n)、額外空間 O(1) 的分析成立；但題目 n 可到 10^9，修正端點仍不足以支援完整限制，尚需加速，不記為整題完成。參考 [題目限制](https://leetcode.com/problems/prison-cells-after-n-days/)。

---

## 2026-11-07

- 819. Most Common Word

**心得**：
- 819：hashmap + string manipulation。

---

## 2026-11-06

- 253. Meeting Rooms II
- 239. Sliding Window Maximum
- 127. Word Ladder
- 297. Serialize and Deserialize Binary Tree
- 212. Word Search II

**心得**：
- 253：difference array，其他招我也想不到了……時間錯了，是 O(n log n)，因為要 sort。我不知道為什麼其他解答這麼麻煩。

- 239：天啊……Amazon OA 面試前夕，我拼了，竟然做出來。先想 brute force，再想重複的部分怎麼優化 → Sliding Window；Constraint Metric 用 hashmap 算數量，搭配 priority queue O(1) 求解；遇到 priority queue 內不該用的 top，用 hashmap 去維持 invariant。看了解答，好像有更好的解法？
- 127：BFS。最難的是 graph 的建立，這次使用 teleportation 概念。也可用暴力法，直接把每個 string 在每個位置換字母，然後查表。

- 297：關鍵設計：用直覺可以直接看出 root(left, right) pre-ordering 的設計。只要在設計上處理能找到 left 跟 right 切割位置的做法，就可以遞迴了。而這個做法跟左括號的個數有關。
  - 主要還是 gpt-6.1-sol 引導、給提示，這題我完全卡住。但是這個設計很好理解也很好實作，喜歡！討論了 preorder 的 root／left／right、如何找到中間逗號、遞迴處理、base case 與取值，還有遞迴的 contract。

- 212：超難……Dynamic Trie + backtracking。

**LLM 點評**：
model: GPT-6
- 253：提供的 ordered map 差分＋prefix sum／sweep line 寫法從 invariant 推理看正確，未編譯或執行原始 C++。掃過時間 t 的淨變化後，meetingRoom 等於 start <= t < end 的會議數；峰值是所需房間數的下界，而按開始時間安排、重用已結束會議的房間即可達到此界，因此答案等於最大併發數。同一時間的開始與結束合併成淨變化，自然處理半開區間，不會將端點相接誤算為重疊。令 U 為不同端點數，map 更新各 O(log(U+1))、掃描 O(U)，合計 O(n log(U+1)+U)，最壞 O(n log n)，額外空間 O(U)，最壞 O(n)；沒有顯式 sort，排序成本來自 std::map 維護 key 順序，且它不是 hashmap。只求房間數時這個表示已充分，不必為了其他解答更長而重寫；heap 保存活躍結束時間，若需追蹤具體房間可擴充搭配 room ID；分開排序 starts／ends 再用雙指標則是另一種掃描事件方式，皆可達 O(n log n)。參考既有 [Difference Array](../Algorithms/Prefix_Sum/05_Difference_Array.md)；可改用 const auto& interval 避免複製，minRoom 改名 maxConcurrent 讓峰值語意更清楚。既有 review 的 Chronological Ordering 變體仍待獨立完成。
- 239：自行從 brute force → sliding window → frequency hashmap＋max-heap lazy deletion 的推導成立；counting 精確記錄窗口頻率，heap 可留過期副本，但每個窗口中的值仍有 heap 代表，輸出前 top 必須是仍存在於窗口的值，因此 top 等於窗口最大值。重複值的歷史副本不會改變最大值；只有移出值頻率降為 0 時，才可能使原本合法的 top 失效，所以目前把清理 while 放在該分支內仍正確。以 C++20 編譯提供的實作，對 n=1..8、值域 {-1,0,1}、所有合法 k 的 73,812 組案例與 brute force 對照皆通過。top() 為 O(1)，push/pop 為 O(log H)，H 是 heap 大小；過期值只在堆頂才刪，遞增輸入且 k=2 時 heap 可累積到 n（另以 n=10000 驗證），故在 hashmap 平均 O(1) 操作假設下，最壞時間 O(n log n)、額外空間 O(n)，不含輸出；不是 O(n)／O(k)。更佳方法是 monotonic deque 保存候選 index：index 遞增、對應值嚴格遞減；隊首先移除過期 index，隊尾移除值 <= 新值的舊 index，因新值更大或相等且更晚過期，舊候選可永久淘汰。每個 index 入隊一次、最多出隊一次，總時間 O(n)、額外空間 O(k)，不需 hashmap。參考既有 [單調棧與單調隊列](../Data_Structures/Stacks_and_Queues/Monotonic_Stacks/01-Monotonic_Stack_and_Queue.md)；目前只確認完成 heap 版本，deque 版本尚未實作。
- 127：提供的 wildcard bucket＋BFS 版本，在題目單字等長、字典單字唯一、只含小寫英文字母且 beginWord != endWord 的前提下，從 invariant 推理看正確，未編譯或執行原始 C++。把只差一個字母的單字放進共同 pattern bucket，相當於以群組／虛擬中介點表示隱含邊；程式每次直接從 word 走到 bucket 中的 neighbor，仍算一次字母變換，不是多走兩條邊。level 從 1 起算符合回傳序列單字數，visited 在入隊時標記避免重複入隊；同組包含自己也會被 visited 擋掉，endWord 不在字典時提早回傳 0 正確。O(V+E) 只能概括 BFS 抽象圖遍歷，尚未計入建 bucket、字串複製與 hashing。令 N 為字典大小、L 為字長、b_p 為各 bucket 大小，原碼時間可寫 O((N+1)L² + LΣ b_p²)（hash table 平均查找假設）；每個單字有 L 個 pattern，同一 bucket 至多 26 個唯一單字，因此固定英文字母表下可簡化成 O((N+1)L²)。graph 的 key 和 vector<string> 副本占 O(NL²)，queue／visited 另占 O((N+1)L)。可在掃完一個 bucket 後 clear()，因首次展開已將該組所有未訪問單字以最早距離入隊；後續不需重掃，但不可在 range-for 迴圈內清空。逐位置換 26 個字母再查字典是 on-the-fly neighbor generation／隱含圖 BFS，不必視為低效暴力法：時間 O(26(N+1)L²)、額外空間 O((N+1)L)，省去 wildcard map。參考既有 [容器型頂點的複雜度分析](../Algorithms/BFS/04-Container_Vertex_Complexity_Analysis.md)。visited.contains 需要 C++20；C++14 可改成 visited.find(neighbor) == visited.end()，或利用 visited.insert(neighbor).second 合併存在檢查與標記。字典單字和 neighbor 可用 const auto& 避免不必要的複製。
- 297：經引導完成的括號格式版本正確：格式是 # 或 value(left,right)，serialize 回傳精確描述該子樹的字串，deserialize 回傳該段字串所描述子樹的根。leftCount 實際是尚未配對的括號深度，遇 '(' 加一、遇 ')' 減一；深度 1 的第一個逗號才是目前節點左右子樹分界，深層逗號不會被誤切。# 對應 nullptr、第一個 '(' 前由 stoi 解析根值，支援負數與多位數；此解析契約針對 serialize 產生的合法格式，不需另做任意輸入驗證。以 C++14 編譯原始 Codec，2058 組 round-trip 皆通過：0～8 節點的所有二元樹形，搭配 0、負數、多位數與 int 邊界值，再加左右各一棵 200 節點鏈狀樹，逐節點比較值與結構，並檢查再序列化結果一致。令 n 為節點數、h 為高度，固定 int 字寬下，不能只因每節點呼叫一次便標 O(n)：serialize 在祖先處反覆串接子樹字串；deserialize 反覆掃描及 substr 複製。兩者時間在平衡樹為 O(n log n)，鏈狀樹最壞 O(n²)。呼叫堆疊本身 O(h)，serialize 含輸出與中間字串為 O(n) 空間；deserialize 的各層 data 字串同時存活，鏈狀樹長度約 n、n-1、…、1，故最壞額外空間 O(n²)，另有 O(n) 還原樹節點。先保留這個易懂且正確的格式；若之後追求線性時間，可在相同格式上改成共用輸出字串追加、共用輸入字串與讀取位置的 parser，避免反覆切片，此延伸尚未實作。對照既有 [遞迴簽名契約](../Algorithms/Design_Principles/Recursion/05-Recursion_Signature_Contract.md)。本次為經提示完成，不視為獨立重做或完成 BFS 變體。
- 212：經提示採用 Trie lookup，將「逐字在 board 搜尋」改成「從每格出發，同時沿 Trie 前綴篩選候選」；board 的 # 標記限制同一路徑不可重用格子，回溯時還原。關鍵修正是區分局部搜尋失敗與全域候選淘汰：從某個 board 起點走不通，不能直接刪掉 Trie 分支；找到單字後清空 node->word 可去重，只有該節點沒有待找單字且沒有 children 時，才可斷開分支。最後貼出的版本在找到單字後檢查 leaf 再斷開，從 invariant 推理看正確，本次未執行該版本；只在此處檢查不會完整回收後來變空的祖先，但不影響正確性。討論確認：斷開 parent 的 child pointer 不等於釋放 node；若 delete node，必須 early return，且當時尚未標記 board，無需還原。令 S 為所有單字總長、L 為最長單字長度、D=min(L,mn)，寬鬆時間上界 O(S+mn·3^D)，額外空間 O(S+D)，不含輸出；Trie 剪枝改善實際搜尋，但不使每格只處理一次，也不能漏算 Trie 空間。本次為經提示及除錯討論後完成，不視為獨立重做。

---

## 2026-11-05

- 273. Integer to English Words
- 2221. Find Triangular Sum of an Array
- 545. Boundary of Binary Tree

**心得**：
- 273：標準的 finite state machine，這個好像也是可以給一個數值 mapping 順序，越過這個界，就加上對應字串。瘋狂的 edge case……然後一開始有先問一下 gpt-6.1-sol 單位有哪些，原來其實只有到 Billion。想到之前的羅馬數字轉換題。
- 2221：不確定這題要幹嘛……直接 in-place 模擬，每輪把相鄰兩數相加取 % 10，有效長度 n 每輪減一，直到 size == 1。時間 O(n²)、額外空間 O(1)。想到是不是可以 collapse。（Pascal’s Triangle 可以加速，但是變複雜滿多。）
- 545：理解題目才是最難的吧……多個遞迴要同時想。不確定這題還有更好的解法嗎。

**LLM 點評**：
model: GPT-6
- 545：在 root 非空、同一 Solution 物件只呼叫一次的前提下，提供的程式從 invariant 推理看正確，未編譯或執行原始 C++。可拆成四份輸出契約：root 一次；左邊界從 root->left 起，優先左、缺左走右，排除葉節點並在遞迴前加入；所有葉由左至右加入；右邊界從 root->right 起，優先右、缺右走左，排除葉節點並在遞迴返回後加入。左右邊界分屬不同子樹，葉節點統一由 constructLeaves 負責，避免重複；單節點時略過三個 helper，使 root 不重複。不要把邊界誤解成每層最左／最右的 view。葉搜尋 O(n)，兩條邊界各 O(h)，合計 O(n)，不會因有三個 helper 變成 O(n²)；呼叫堆疊應標 O(h)，只有平衡樹才是 O(log n)，鏈狀樹最壞 O(n)。輸出 boundary 另占 O(b)，b 是邊界節點數，最壞 O(n)。這個分段解法已達最壞時間最優；可用單次 DFS 加左右邊界旗標合併，但仍為 O(n)／O(h)，增加狀態管理，不必為減少 helper 而重寫。重點是各自想清楚契約，不必同時展開所有遞迴，見 [遞迴設計原則](../Algorithms/Design_Principles/Recursion/01-Recursion_Design_Principles.md)。若要讓物件可重複呼叫，需在入口 boundary.clear()；若另外支援空樹，再於讀取 root->val 前處理 nullptr。可在葉節點加入後直接 return，省去兩次空子樹呼叫，但不改變漸近複雜度。
- 2221：提供的程式在題目非空陣列的前提下，從 invariant 推理看正確，未編譯或執行原始 C++。每輪開始 nums[0..n-1] 代表目前那一列；由左往右更新時，nums[i] 與 nums[i+1] 都仍是本輪舊值，已覆寫的左側不會再被讀取，因此可安全原地產生下一列；n-- 只縮短有效前綴，尾端舊值不需刪除。原始長度 N 的更新總數為 (N-1)+...+1=N(N-1)/2，故時間 Θ(N²)、額外空間 O(1)；N<=1000 時至多 499,500 次更新。核心練習是忠實模擬、讀寫相依與有效長度，見 [Simulation 設計框架](../Algorithms/Simulation/01-Simulation_Design_Framework.md)。collapse 的觀察成立：三個元素 a,b,c 最後為 (a+2b+c)%10，一般結果為 Σ C(N-1,i)·原始 nums[i] mod 10，係數來自 Pascal 三角形。這是數學展開；若仍逐列產生係數，依舊 O(N²)，且不能直接在模 10 下套用含除法的組合數遞推（分母可能沒有模反元素），完整係數也可能溢位。尚未實作或驗證此延伸，不視為已完成。參考 [題目規格](https://leetcode.com/problems/find-triangular-sum-of-an-array/)。
  - 加速的關鍵是 Pascal 係數搭配 modular combinatorics，而非逐列重建三角形；例如用 Lucas 定理分別處理 mod 2／mod 5，再以 CRT 合併，可達 O(N log N) 時間、O(1) 額外空間，但增加數論與實作負擔。目前準備先掌握 O(N²)／O(1) 模擬及 Pascal 權重的觀察，進階加速理解即可，暫不列為必練或已完成。
- 273：相關的是 2026-10-16 的 12. Integer to Roman，當時已討論合法面額由大到小查表、扣減剩餘數值的 simulation／greedy。273 也可用有序數值門檻與字串 mapping，但單位前還要描述數量，例如 200 是 Two Hundred；較精確的分類是數值分解＋查表／simulation，不必然是標準 FSM，沒有程式碼不判定具體實作。可用每三位一組，將組內 1..999 的規則與 Thousand／Million／Billion 分開；注意 0 整體輸出 Zero、空的三位組略過、10..19 特例與空白。題目範圍為 0 <= num <= 2^31-1 = 2,147,483,647，因此最高只需 Billion，並非英文單位到此為止。參考既有 [Simulation 設計框架](../Algorithms/Simulation/01-Simulation_Design_Framework.md)；[273 題目規格](https://leetcode.com/problems/integer-to-english-words/)。本次只記錄使用者完成與心得，未檢視或執行程式；先詢問英文單位與取得演算法提示應分開記錄。

---

## 2026-11-04

- 567. Permutation in String
- 909. Snakes and Ladders

**心得**：
- 909：BFS + index mapping。
- 567：Sliding Window + hashmap + letter count。不知道為什麼 hashmap[c] 的 count 即使超過 target[c]，letterCount 不去減掉也不會影響正確性。

**LLM 點評**：
model: GPT-6
- 567：提供的程式從 invariant 推理看正確，未執行原始 C++。letterCount 實際追蹤 target 中 window[c] >= target[c] 的字元種類數，而非頻率恰好相等的種類數；加入時只有 target[c]-1 → target[c] 才加一，移除時只有 target[c] → target[c]-1 才減一，因此超額不需扣除。fix 後窗口長度至多 m，所有目標字元皆達標表示窗口至少含 m 個字元，兩者合起來迫使窗口長度恰為 m、每種頻率恰等於 target，且沒有額外字元；所以不會誤判，也不必另檢查長度 == m。例 s1="ab"、窗口 "aa" 時 a 雖達標，b 必不足，letterCount 仍只有 1。這是固定長度窗口，以長度枚舉候選，不需要頻率相等具有擴張單調性。平均時間 O(m+n)，目前兩張 map 空間 O(m+1)（m>=1 時為 O(m)），本題固定 26 個小寫字母可視為 O(1)。可對照 [Constraint Tracking](../Algorithms/Sliding_Window/01-Constraint_Tracking_and_Optimization.md) 的達標種類計數；與「恰好相等」計數器的狀態轉換須分清楚。
- 909：BFS 與 index mapping 方向正確；從程式推理看，最短步數邏輯正確，未執行原始 C++。每條邊代表一次擲骰，包含落點後的一次蛇／梯跳轉，因此邊權皆為 1，BFS 的層數就是擲骰次數；跳轉後才查 visited 正確，且用 if 而非 while 符合每次只跳一次。index(k) 先以 (k-1)/n 算由底往上的列偏移，再用其奇偶決定欄方向，能同時處理奇數與偶數邊長。初始化應將 visited[0]=true 改成 visited[1]=true，使起點入隊時即標記；原版遇到回到 1 的蛇時會多展開起點一次，但不影響最短答案。n 是邊長，最多 n² 個狀態、每個狀態至多 6 條出邊，index 為 O(1)，故時間 O(n²)、額外空間 O(n²)（visited 與 queue），不是 O(6^distance)。骰子迴圈可寫 for (int k=curr+1; k<=min(curr+6,destination); ++k)，並另存跳轉後的 next，讓候選落點與最終狀態分清楚。

---

## 2026-11-03

- 92. Reverse Linked List II
- 787. Cheapest Flights Within K Stops
- 371. Sum of Two Integers
- 437. Path Sum III
- 518. Coin Change II

**心得**：
- 92：combined technique：k-gap pointer 跟 reverse linked list。用 dummy 定位 left 前驅與 right，保存區間原頭與尾端後繼，反轉後重新接回。

- 787：滿慘的，第三次做，還是一塌糊塗。這次收穫是，從 Dijkstra's 去改，配上 distance 要 extend 成多維，才能記錄 k stops，但是觀察起來時間好像沒有更快。
  1. 一開始先設計 Dijkstra's 算 weighted shortest path。
  2. 後來加入 k stops 的限制。
  3. 前面先卡到 C++ 實作整個大錯亂，vector<pair<int, int>> 跟 vector<int> 混用。
  4. 演算法錯誤：沒有處理到 edges 數少、weighted path 大的可能性，需要用一個二維的 Distance 陣列去記錄可能的路徑。
  - 用 Dijkstra's 寫滿混亂的。
  - 後續：整理[題目出處與歷史](../Problem_History/LC_0787_Cheapest_Flights_Within_K_Stops.md)，加入 Problem Review；三種解法都可以玩看看：Bellman-Ford、BFS with condition k、better Dijkstra，分開獨立重練。

- 371：經提示做出來了，但是負數出現的處理，竟然 bit manipulation 是可以處理 sign bit，還是覺得很驚人。原來 ^ 跟 & 是整組 bits 直接做，不必逐 bit 取出；carry 往左移，直到 carry == 0。

- 437：用標準的雙遞迴，這好像不是第一次出現。因為數字範圍太大，要轉型成 long long 來處理，但是這版時間複雜度不好。
  - 後續經 gpt-sol-6.1 跟解答提示完成 prefix sum 版本。滿妙的這題……preorder + prefix sum；backtracking 記錄祖先的 running sum，查詢後加入、離開時撤銷，使用 prefix sum 的出現次數計數。
  - [歷史與教材出處](../Problem_History/LC_0437_Path_Sum_III.md)：CtCI 第六版 4.12 Paths with Sum，官方解答也有雙遞迴與 prefix sum＋回溯版本。

- 518：Top-down value range DP。這好像是很經典的 value range DP，想確認 Knapsack DP 筆記有沒有出現它。用 choose／not choose 的遞迴，加上候選 index 與剩餘 amount 的 cache。
  - 今天累了，二維 bottom-up 留到明天（2026-11-04）寫，先不做一維壓縮；已加入 Problem Review，尚未完成。

**LLM 點評**：
model: GPT-6
- 92：提供的程式在合法輸入下正確；以 Python 模擬相同指標操作，檢查 n=1..30 的全部 4,960 個合法區間，順序、節點數與最終無環皆通過，未執行原始 C++。left 減一後，k=right-left 等於原始 right-left+1；同步移動維持此間距，最後 slow 位於原始 left-1、fast 位於 right，符合 [K-Gap Pointers](../Algorithms/Two_Pointers/03_K_Gap_Pointers.md) 的 invariant。reverse(slow,fast) 實際連前驅一起反轉，之後兩次接線才修回；建議改成 reverse(headNext,fast)，使 helper 的範圍直接等於目標區間，仍由呼叫端補上原頭 next。令 m=原始 right-left+1，時間 O(right)，最壞 O(n)，遞迴堆疊 O(m)；註解的 k 會被 k-- 消耗，應另用未修改的區間長度說明。先定位右界再重走區間反轉，不符合本題 one-pass 的通常要求；one pass 並非看有幾個迴圈，而是能否到達左界後直接反轉，不先掃到右界再回頭處理。已知 left/right 時，K-gap 可用但非必要；可先定位前驅，再以長度 m 迭代反轉，達 O(n) 時間、O(1) 額外空間，未將此延伸視為本次已完成。
- 787：經提示完成的最終二維 distance 版本，從狀態與邊界推理看正確，未執行原始 C++。核心卡點是狀態定義：加入會影響後續合法選擇的邊數限制後，狀態必須由 city 擴成 (city, edgesUsed)，不能只在普通 Dijkstra 外加停止條件。distances[city][edgesUsed] 存恰好使用指定邊數的最小費用，不是記錄所有實際路徑；便宜但邊數多與昂貴但邊數少的候選，可能都要保留。最多 k 個中繼站即 k+1 條邊，包含 0 邊需 k+2 格；stops 建議改名 edgesUsed。二維表是修正錯誤剪枝，不保證提速；令 K=k+1，擴展圖最多 V(K+1) 個狀態、EK 條轉移，目前 lazy heap 實作時間 O(V(K+1)+EK log(EK+2))、空間 O(V(K+1)+EK)，且跑到 heap 清空。非負權重下，可在通過 stale-state 檢查後、邊數擴展 guard 前，於第一次彈出 dst 時提早返回，但實際加速需量測，不能憑單次平台時間斷言。混亂可拆成 C++ 型別表示與演算法狀態設計兩件事；下次先寫清楚狀態、支配條件與邊數界線，再選搜尋順序。另一個貼合限制的視角是 [Bellman-Ford 的邊數 DP](../Algorithms/Dynamic_Programming/Advanced_Techniques/Bellman-Ford/01-DP_Foundations_of_Bellman-Ford.md)：逐層放寬邊數、每層只讀上一層，與本次 expanded-state Dijkstra 可分開內化；本次未實作此版本。
- 371：XOR 得不含進位的和、AND 後左移得進位，演算法方向正確；未執行原始 C++。二補數的關鍵是固定 w 位下，負數 -x 編碼為 2^w-x，與 -x 在模 2^w 下同餘，因此加法可共用相同的逐位規則。sign bit 在二補數的數值解讀中權重為 -2^(w-1)，不是獨立符號旗標；最高位溢出的進位捨棄，若真實答案在 signed 範圍內，解讀即為正確整數。每輪 a+b 的 invariant 應理解成模 2^w 不變；carry 最低有效位每輪嚴格左移，最多 w 輪，時間 O(w)、空間 O(1)，固定 32 位可視為 O(1)。swap 無法改善迭代次數，因 XOR 與 AND 皆可交換，交換後第一輪 sum/carry 完全相同。實作需區分位元數學與語言規則：C++17 對負值左移屬 UB；較新標準的左移採模 2^w 定義，跨版本宜用 unsigned 中間值，舊版 unsigned 轉回超出範圍的 int 另有實作定義問題。見 [位元加法](../Algorithms/Bit_Manipulation/99-Case_Bitwise_Addition.md)；以 [C++17 草案](https://timsong-cpp.github.io/cppwp/n4659/expr.shift) 與 [目前草案](https://eel.is/c++draft/expr.shift) 區分版本，既有筆記的 invariant 與型別轉換敘述需帶此前提閱讀。
- 437：提供的雙遞迴版本從結構推理看正確，未執行原始 C++。pathSum 枚舉路徑起點，pathCount 固定起點、沿子孫枚舉終點；每條合法向下路徑依起點與終點被計數一次。這與 LC 572 的「外層找候選位置、內層從該位置檢查」有相同拆解。命中 sum == root->val 後仍繼續遞迴正確，因下方可能有總和為 0 的延伸；有負值時也不能以 remaining < 0 剪枝。helper 參數直接為 long long，因此 targetSum 傳入時已提升，sum-root->val 也在 long long 運算，不必等減完再轉型。精確時間為 Θ(Σ_v subtreeSize(v)) = Θ(n+Σ_v depth(v))，平衡樹 Θ(n log n)、鏈狀樹 Θ(n²)，堆疊 O(h)，不是 O(h²)。此版以值傳遞 remaining、沒有共享狀態的加入／撤銷，描述成 DFS 更精確。瓶頸是每個起點重掃子樹；後續經提示完成固定終點、重用祖先 prefix 頻率的版本，銜接既有 [Running State](../Algorithms/Prefix_Sum/02_Running_State_Pattern.md)。最終程式的 long long running sum、先查 prefixSum[sum-targetSum] 再加入、左右子樹後撤銷，以及 prefixSum[0]=1 的順序正確；從 invariant 推理看正確，未執行原始 C++。這裡是 preorder 更新／查詢加上離開時 backtracking；固定起終點的路徑唯一，但同終點仍有多個起點，且 prefix 可重複，因此要累加頻率。平均時間 O(n)，來自每節點固定次數 hash 操作；一般遞迴式應寫 T(n)=T(leftSize)+T(rightSize)+平均 O(1)，2T(n/2) 只適用平衡樹。空間為 O(U+h)，U 是實際保留的 map key 數而非 sum 值域；目前 operator[] 查詢會插入缺少的 key，撤銷只減次數而不 erase，故最壞 O(n)。若查詢用 find 且次數歸零時 erase，才可界為 O(h) 額外空間。
- 518：提供的 top-down memoization 在題目的正整數、互異面額及 amount <= 5000 前提下，從狀態推理看正確，未執行原始 C++。精確分類是「候選進度 i × 剩餘金額 r」的完全背包組合 Counting DP；F(i,r) 表示只使用 coins[i..] 湊出 r 的組合數，不能只說值域 DP 就省略 i。選取後保留 i，代表同面額可無限使用；跳過才 i+1，固定候選順序避免把同一組合的不同排列重算；amount=0 回傳 1 表示空選擇是一種完成方式。排序不必要，任意固定候選順序即可，且目前沒有利用排序做額外剪枝。建議 cache 改成 amount+1 格，刪除 sort 後，含初始化時間為 O(n(A+1))、表格空間 O(n(A+1))；另有 O(n+A/c_min) 遞迴堆疊，c_min 為最小面額，0 金額直接返回。原碼配置 n×5001，須計這份固定上界表格的初始化／空間成本，排序另需 O(n log n)。暴力法不能直接套 O(2^n)：選取分支不增加 i，遞迴深度還依賴 A/c_min。現有 [Counting DP](../Algorithms/Dynamic_Programming/Problem_Types/Counting_DP.md) 已明列 518 並示範一維 bottom-up 組合計數；[狀態壓縮](../Algorithms/Dynamic_Programming/State_Design/04-State_Reduction.md) 也對照 322／518，主要 [Knapsack Playbook](Trick%20Practice/Knapsack_Variations_Playbook.md) 則聚焦 0/1 且尚未明列本題。完成紀錄僅涵蓋本次 top-down，不視為完成一維 bottom-up 延伸。

---

## 2026-11-01

- 452. Minimum Number of Arrows to Burst Balloons
- 427. Construct Quad Tree

**心得**：
- 427：設計方向對了……但是實作一直錯，漏東漏西。
  - 經典的 divide and conquer，一開始 base case 想錯了，長度 1 是可以的。
  - 這就回到我們常常用的心法：要用 classic example 去測試程式，其中一個最重要的 example 就是 edge case。一測試就知道 base case 要怎麼設計，甚至 invariant 的驗證。
  - 加入 Essential Problems 的 Divide and Conquer。
  - 看完解答後，發現程式碼難寫是因為用起始、結尾座標；如果設計成 x、y、width 三個參數，會簡單很多。這算是需要靈感，或是常講的「simple is better and faster」？
- 452：有變化的 interval problem。

**LLM 點評**：
model: GPT-6
- 427：最終提供的四分遞迴＋同值 leaf 合併版本，在正方形且邊長為 2^k 的前提下正確；本次透過討論修正，未實際執行測試。具體卡點是 1×1 base case、topRight／bottomLeft 對調、閉區間後半段未從 mid+1 開始，以及 delete 後再次讀取指標。核心 invariant 是每次呼叫回傳精確表示指定正方形的 Quad Tree；四個子區域須不重疊、完整覆蓋且嚴格縮小，只有四個 child 都是同值 leaf 才能合併。edge case 很適合幫助設計並檢查 base case，但測試通過不等於證明一般 invariant：還需確認分割保留前提、遞迴嚴格縮小，以及合併維持表示正確。建議手算 1×1、僅 topRight 為 1 的 2×2、全同值與需多層切分的 4×4。令 n 為邊長，時間 Θ(n²)、遞迴 stack O(log n)，含建樹節點的峰值空間 O(n²)；即使全同值也會先展開再合併。見 [分治區間設計](../Algorithms/Divide_and_Conquer/03_Interval_Design_in_Divide_and_Conquer.md)。已加入 Essential Problems 的 Divide and Conquer。後續觀察到可將四個區間端點改成 (x,y,width)：這是利用每個子問題皆為正方形的 invariant 選擇更貼合結構的狀態表示。四端點之間需維持列長等於欄長的約束；起點＋邊長則只存獨立資訊，讓大小、1×1 base case 與四象限偏移直接可見，減少 end 是否包含、mid 與 mid+1 的協調。此簡化可由「子問題是什麼形狀、哪些參數可推導、最小充分表示是什麼」系統性導出，不必等待靈感；適用前提是正方形，任意矩形則需 height 與 width。simple 在這裡主要改善撰寫、推理與除錯速度，兩種表示的時間複雜度仍是 Θ(n²)，不能據此宣稱執行速度必然更快。x、y 仍須明確約定 row／column。
- 452：變化在於「用最少的點刺穿所有區間」：同一箭能處理的氣球必須有共同交集，不能只看重疊是否連成一串。例如 [1,2]、[2,3]、[3,4] 可合併成一段，卻不能一箭全破。標準 greedy 是依右端點遞增排序，在尚未處理的最早右端點射箭；將命中該區間的箭右移到此端點，不會失去其他尚未處理、原本被這支箭命中的區間，因此可保留最優解。閉區間端點相接仍可共用一箭，只有 start > arrow 才需新增箭；排序 O(n log n)、掃描 O(n)。後續提供的起點排序＋交集收縮版本正確：range 維持目前這組氣球的共同交集，新區間 start <= range.second 即可加入並縮小交集；否則必須新開一組。每組可在交集中用一箭處理；前組最小右端點所屬的氣球與下一組所有氣球分離，各組可取出兩兩不重疊的代表，因此至少需要組數支箭，達到最優。count 計的是成功加入既有組、節省的箭數，所以 n-count 等於組數；可改名 savedArrows，或直接從 arrows=1 開始、遇到新組才遞增。依起點排序後，range.first 每次等於目前 start，若只求答案可省略，只保留最小右端點。時間 O(n log n) 正確；常見 std::sort 實作需 O(log n) stack，掃描本身 O(1) 額外空間。points[0] 依賴非空輸入；本題符合此前提。

---

## 2026-10-31

- 240. Search a 2D Matrix II
- 743. Network Delay Time
- 846. Hand of Straights

**心得**：
- 846：一開始方向錯了……跑去直接 sort 原本 array，然後想要用 two-pointer。後來直接改成 ordered map，讓它小到大、可以計數，每次取最小，然後去消化一組 group。hashmap + sort + greedy。
- 240：這題可以用 divide and conquer，但是超難寫……然後最佳解也不是這個，加入 Problem Review。
- 743：這個就是標準的 DFS，但是要注意 minimum path 更新，因為可能有多條路徑，要選最短的。靠……這是最短路徑問題！！我用了最 naive 的解法。
  - 後續改寫 Dijkstra's 經典做法。有錯！！！pair 是 weight 當第一個，不是 node……會對，但是會多做。
  - 順便練了 Dijkstra's。

**LLM 點評**：
model: gpt-6.1-sol
- 846：提供的程式正確，核心是 ordered frequency map + greedy。當前最小剩餘值 base 不可能接在更小值之後，因此它的 count 份都必須各自作為一組的起點；一次從 base..base+groupSize-1 各扣 count，等於批次組出 count 組，不只一組，缺牌或數量不足即可判 false。std::map 本身依 key 排序，不是 hashmap；令 U 為不同值個數，建表 O(n log(U+1))，消耗階段每次成功扣減都至少消耗一張牌，因此扣減次數合計 O(n)，搭配 map 查找得到總時間 O(n log(U+1))，最壞 O(n log n)，額外空間 O(U)。auto [base,count] 是複製值，後續 erase 不會使這兩個變數失效。直接排序原 array 並非錯誤方向，也能搭配頻率表實作相同 greedy；卡點在重複牌的次數管理，單靠 two pointers 不容易表達「消耗每個連續值」的需求。
- 240：本次經討論修正後完成三區域 divide-and-conquer 搜尋。主要陷阱是矩形參數順序、start > end 的空區間 guard，以及排除 midpoint 時不能漏掉同列／同欄的候選；最終切分正確且每輪嚴格縮小。這不是只保留一個分支的 binary search，不能標 O(log(mn)) 時間；對 N×N 矩陣，由 T(N) ≤ 3T(⌈N/2⌉)+O(1) 可得 O(N^log₂3) 的時間上界，N 指邊長，遞迴空間 O(log N)。後續值得練習 O(m+n) 時間、O(1) 空間的階梯搜尋，重點是利用行列排序讓每次比較安全排除整列或整欄；本次尚未實作此版本。已列 ⭐⭐⭐⭐ 待重做，區分已完成的分治版本與待練的延伸。
- 743：提供的程式是以 DFS 排程的反覆 distance relaxation，不是每個節點／邊只處理一次的普通 DFS。在本題非負權重與數值範圍下可正確求最短距離：currCost >= costs[k] 時剪枝，較短路徑仍會重新展開節點；非負環無法改善距離，因而被擋住。答案是 max_v dist(source,v)，即所有節點最早收到訊號時間的最大值，不是圖上的最長路徑；不可達則回傳 -1。時間不能標 O(V+E)：同一節點每次距離改善都會重掃出邊，總成本取決於改善次數；一般圖上此深度優先排程可能出現大量、甚至指數級的改善，固定整數權重範圍則可另給依權重界的偽多項式分析。圖儲存 O(V+E)、costs O(V)、遞迴堆疊 O(V)，含建圖的總額外空間 O(V+E)。值得接著掌握非負權重的 Dijkstra：以目前最小距離候選優先處理，避免任意順序的反覆傳播；尚未提供此版本，不記為已實作。見 [Dijkstra 指南](../Algorithms/Greedy/Dijkstra's%20Algorithm/01-Dijkstra_Algorithm_Guide.md)。

  - 後續已提供 heap＋距離鬆弛版本；pair 原存 {node,cost}，greater<pair<int,int>> 依第一欄排序，因此實際按節點編號處理。正確優先鍵應是起點到候選節點的「累積距離 cost」，不是單條邊的 weight；入 heap、解構與後續 push 都須統一為 {cost,node}。原版在非負權重下可透過距離改善與重新入 heap 繼續收斂，但同一節點可能重複展開，不能套 Dijkstra 的效率保證。修正 pair 後，lazy heap 時間 O(V+E log(E+2))、總額外空間 O(V+E)；已辨認此錯誤，尚未提供修正後完整版本。

---

## 2026-10-30

- 222. Count Complete Tree Nodes
- 678. Valid Parenthesis String
- 721. Accounts Merge
- 309. Best Time to Buy and Sell Stock with Cooldown

**心得**：
- 309：multidimensional dynamic programming。這個多維的太經典了，記錄在 Archetype Problems 跟 Essential Problems。
- 721：建立 graph 的觀察比較難，其他就是標準的 connected component 題目而已。加入 Problem Review。
- 678：標準的 recursive 轉 top-down dynamic programming。但是這題解法有點多欸……而且直接想 bottom-up dynamic programming 也不容易，甚至有 O(n) 的解法。這題需要繼續練嗎？
- 222：這題經典地難，不看提示的話，我是不可能想出來的……加入 Problem Review。

**LLM 點評**：
model: gpt-6.1-sol
- 309：提供的程式在非空 prices 的題目前提下正確，時間 O(n)、空間 O(n)。狀態是「日期 × 是否持股」，兩個 array 只是分開儲存狀態維度；buy[i] 表示第 i 天結束時持股的最大淨收益，sell[i] 表示未持股的最大收益，不代表當天必須買／賣。buy[i] = max(buy[i-1], sell[i-2]-prices[i]) 將 cooldown 編入依賴：今天買入只能接到兩天前未持股的收益，不能接昨天剛賣出的收益；sell[i] = max(sell[i-1], buy[i-1]+prices[i]) 則比較休息與今天賣出。長度 1、前兩天初始化與最後回傳未持股狀態均合理；註解中的轉移也須保留 max 的「延續原狀態」分支。可只保存必要歷史壓成 O(1) 空間，但須保留舊值並確認更新順序；本次僅確認 O(n) 空間版本。已加入 State Machine DP 原型與 Essential Problems。
- 721：核心確實是建模：共同 email 連接帳戶，合併具有傳遞性，同名本身不能當成合併依據。提供的 email → account index → emails 寫法可找出連通分量，但只標記 email，沒有保證 account 只展開一次；設第 a 個帳戶有 k_a 個不同 email，其內容可被重掃 k_a 次，遍歷成本可達 O(Σk_a²)，另有各分量 email 的排序成本，不能標為每個 email 一次的 O(m)。改用 email → email 邊時，同帳戶只需建立保留連通性的星狀或鏈狀邊，不必兩兩相連；也可保留原模型、追蹤 account 是否已展開。重做聚焦節點／邊語意、visited 對象與實際掃描次數，再處理排序輸出。尚未提供另一版程式，不將優化版本記為已實作；已列 ⭐⭐⭐⭐ 待獨立重做。
- 678：本次回報完成 top-down DP；未提供程式碼，不判定具體實作。若使用 (index, balance) 表示目前位置與未配對左括號數，memoization 將重複路徑合併，狀態數 O(n²)、每個狀態常數種轉移，時間與 cache 空間 O(n²)，遞迴深度 O(n)。bottom-up 可先沿原遞迴依賴順序填表，不必直接憑空想新狀態；前綴可達性的寫法則需重新定義狀態語意。值得另練一次 O(n) 時間、O(1) 空間的區間摘要做法，重點是證明可達 balance 的結構能以端點完整表示，而非收集所有解法。可先結束本次練習，另日練此延伸，再獨立重寫；尚未完成 bottom-up 或 O(n) 版本，不將其記為已做。
- 222：本次經提示完成最後一層編號的 binary search，最終程式在 complete tree 與題目數值範圍內正確。關鍵是把結構轉成單調判定：以 1 為根的編號連續，最後一層的存在性為 true 前綴、false 後綴；搜尋第一個不存在的編號後減一，即總節點數。編號去掉最高位 1 後，其餘 bits 由高到低對應左 0／右 1 的路徑。每次存在性查詢 O(h)，搜尋 O(h) 輪，總時間 O(h²)=O(log² n)，遞迴堆疊 O(h)。base case 應回傳節點非空；空樹目前也能回傳 0。重做重點是獨立連結 complete tree、單調性、編號路徑與二分邊界，而非只背程式；整數的 2 次方可用適當寬度的位移取代浮點 pow，並確認位寬。已列待重做。

---

## 2026-10-29

- 173. Binary Search Tree Iterator
- 279. Perfect Squares
- 274. H-Index
- 380. Insert Delete GetRandom O(1)

**心得**：
- 380：hashmap + delete at the end of vector + rand。其實滿容易做錯的，值得再做一次。
- 274：其實小複雜……要先想到 value range hashmap，然後還要做 suffix sum。
- 279：很有趣欸……是 dynamic programming 經典設計。一開始沒處理到往下查每個可能的 sqrt，作為 last。這也是 value range DP？解法有點多，需要再做其他做法嗎？
- 173：就是用 iterative 的 inorder 去想的，應該是最佳解了。

**LLM 點評**：
model: gpt-6.1-sol
- 380：本次經討論修正刪除邏輯：維持 hashmap[store[i]] == i，非尾端刪除時以尾元素補位並更新其 index，再移除尾端與 val 的 map 紀錄；刪除尾端或唯一元素時不可重新插回 val。最後提供的 remove 寫法正確，resize(size-1) 可改為 pop_back()。重做應涵蓋刪中間、刪尾端、刪唯一元素與刪後重新插入。getRandom 的 rand()%n 可能有 modulo bias；已討論改用持久的 mt19937 引擎搭配 uniform_int_distribution，尚未看到整合後版本。insert 平均／攤銷 O(1)，remove 平均 O(1)，均勻取樣在固定字長下以期望常數成本處理；儲存 n 個元素需 O(n) 空間。見 [均勻亂數取樣](../CPP_Reference/Algorithm/Uniform_Random_Sampling.md)；獨立重做列為待做。
- 274：在 citations 值介於 0..1000 的前提下，提供的程式正確；array 是以值直接定址的頻率桶，不是 hashmap。由大到小掃描，在檢查 counts[i] >= i 時，counts[i] 已包含所有引用數 >= i 的論文，因此判斷的是「至少 i 篇論文各被引用至少 i 次」；第一個成立的 i 就是最大 h，未成立時再把累積值傳給 i-1。以 K 表示桶數，時間 O(n+K)、空間 O(K)；若固定 1001 為常數，則為 O(n) 時間、O(1) 額外空間。進一步利用 h <= n，可將引用數 c 歸入 min(c,n) 的桶，改用 n+1 個桶，得到不依賴引用數上界的 O(n) 時間、O(n) 空間版本。註解中的 brute force 若只測原始 citation 值會漏掉答案，例如 [100,100] 的 h=2；候選應是 0..n，目標是最大可行 h，不是最大論文數。
- 279：提供的 DP 程式正確。這是以目標總和值為狀態的 value-space／value-range DP，也可視為完全平方數作為可重複面額的 Coin Change／完全背包最小化問題；dp[i] 存湊出 i 的最少項數，並非以答案項數作索引。枚舉最後一項 q²，取 dp[i-q²]+1 的最小值；不能只取最大的平方數，例如 12 貪心取 9 需四項，但 4+4+4 只需三項。內層枚舉 floor(sqrt(i)) 個候選，時間 Θ(n√n)，不是 O(n log n)；空間 O(n)。平方根候選由大到小或由小到大皆可，因依賴的總和值嚴格小於 i；變數名可用 q 避免與 sqrt 函式混淆。註解中的 15=9+4+2、6=4+2 不是合法的平方數分解。當前優先內化最後一步枚舉與最小化轉移即可；BFS 可作等權最短路視角的選修，數論做法不必為收集解法而立即重做。見 [在值域上做 DP](../Algorithms/Dynamic_Programming/State_Design/03-On_Value_Space.md)。
- 173：提供的 lazy iterative inorder 程式正確，是不修改原樹、符合 O(h) 空間要求的標準最佳解法。每次操作前，stack top 是下一個尚未輸出的最小節點；store 沿左鏈保存尚待處理的節點，next 彈出後補入右子樹的左鏈，便恢復 invariant。constructor 最壞 O(h)，hasNext 最壞 O(1)，單次 next 最壞 O(h)；每個節點全程只 push、pop 各一次，因此完整遍歷 O(n)，next 為攤銷 O(1)，空間 O(h)。若只呼叫前 k 次 next，連同初始化總成本為 O(h+k)，不可將初始化成本忽略後宣稱任意短前綴都只需 O(k)。next 依賴仍有下一個元素的呼叫前提；store 命名為 pushLeftChain 可更直接表達用途。

---

## 2026-10-28

- 373. Find K Pairs with Smallest Sums
- 560. Subarray Sum Equals K
- 647. Palindromic Substrings
- 86. Partition List
- 695. Max Area of Island

**心得**：
- 695：經典的 one-liner DFS……跟 visited 狀態管理。
- 86：糟糕……我把它想難了＠＠……用 two pointer technique，最後 merge two lists 來做就很簡單。
- 647：dynamic programming……但是我寫不出漂亮的 i + 1、j - 1。要用 cut position 來設計的話，dp[i][i] 就是空字串？好像很複雜……解答很巧妙地先把 length 2 的做掉了，所以就不會踩到我的 case。
- 560：一開始設計錯，使用 sliding window。這個沒有單調性的 constraint metric，因為 sum 不是 monotonic。沒辦法有效地找到對應的 pair，後來才經由提示得到是 running hashmap。prefix sum + running hashmap。
- 373：k-way merge + heap。跟 gpt-6.1-sol 一路討論：暴力法先 sort／heap 取 top-k 沒問題，可是不用把 m*n 看完。使用 non-decreasing sorted 特性，總是取下一個最小的，只考慮下一個候選。這就是 k-way merge！heap 存 index，comparator 透過 nums1、nums2 比較總和。

**LLM 點評**：
model: gpt-6.1-sol（560、647、86、695）；GPT-6（373，保留原點評）
- 695：核心是每個陸地格只計數一次：通過邊界、水域與 visited 檢查後，先標記，再往四鄰遞迴，回傳本格 1 加上各方向新發現的面積。visited 跨整次掃描保留，回傳時不撤銷，與列舉路徑的 backtracking 不同。可另存 visited 或原地標記 grid；即使原地標記，遞迴堆疊最壞仍為 O(mn)，不能直接稱額外空間 O(1)。整張網格時間 O(mn)。未提供程式碼，不判定本次具體實作。
- 86：提供的程式正確，時間 O(n)、額外空間 O(1)，重用原節點完成 stable partition。head 實際是目前待檢查節點的前驅：抽出 head->next 後保持 head 不動，才能繼續檢查接上來的節點；只有保留 < x 的節點時才前進。ptr 是 >= x 串列的尾端，依遇到順序尾插，兩組都保留原相對順序。ptr->next = nullptr 切斷抽出節點的舊連結，維持抽出串列獨立並以空指標結尾；最後 head 停在保留串列尾端（或 dummy），接上 extracted.next 即可。這裡的 merge 更精確是串接 concatenate，不需像合併排序串列一樣逐一比較。head 自 dummy 起且只在 head->next 非空時前進，故 while 中的 head && 可省略；命名為 prev 更貼近角色。
- 647：提供的閉區間 DP 程式正確，時間與空間皆 O(n²)。dp[i][j] 表示 s[i..j] 是否為回文，因此 dp[i][i] 是單字元，不是空字串；若改成 cut position 的半開區間 [i,j)，才是 dp[i][i] 表示空字串（可設 true 作為轉移 base case，但不計入題目答案），右端字元改讀 s[j-1]。目前 length 2 時 i+1 > j-1 成立，C++ || 短路避免讀取反向區間，直接比較兩端即可，不必另外初始化 length 2；該條件可寫成 l == 2。依長度遞增，內部 length-2 的狀態已先算完。dp 是 boolean 回文判定，註解中的 dp[i+1][j-1] + 1 不符合狀態定義；計數應在判定成立後另做 count++。邊界表示選定後保持一致即可，不必強行改成 cut position。
- 560（model: gpt-6.1-sol）：本次經提示完成，最終程式正確。負數使區間和不具備可安全移動左界的單調性；建立 prefix sum 只讓區間和能 O(1) 計算，不會產生單調性。由 prefix[right] - prefix[previous] = k 移項，固定 right 後只需查先前 prefix[right] - k 的出現次數，將枚舉 pair 轉成頻率查詢；同值可能對應多個合法起點，須存次數。hashmap[0] = 1 表示空前綴；先查再加入目前 prefix，避免 k = 0 時計入空子陣列。平均時間 O(n)、空間 O(n)，key design 應標為 prefix sum + frequency hashmap。見 [Sliding Window 適用性與單調性](../Algorithms/Sliding_Window/00-Sliding_Window_Standard_Template.md)。
- 373：在兩陣列非空且 k 不超過配對總數的前提下，提供的程式正確。固定 i 後，(i,0)、(i,1)…形成總和非遞減的一列；heap 始終保存每列尚未取出的第一組，因此全域下一個最小值必在 heap 中。取出 (i,j) 後只補 (i,j+1)，每個索引配對只生成一次。這是利用有序性延後生成候選，不是證明後續配對永遠不會入選。初始化依 i 遞增 push (i,0)，總和非遞減，在標準 binary min-heap 中新元素不需上浮，故此特定初始化可為 O(m)；一般任意順序逐一 push 的上界則為 O(m log(m+1))。後續 k 次取出／補入為 O(k log(m+1))，heap 額外空間 O(m)，輸出另需 O(k)。while(k--) 依賴有足夠配對的前提，通用版本可加 !pq.empty()；nums2 為空也應先返回。還可只初始化前 min(m,k) 列：更後面的列首已有至少 k 個不大的前列列首，因此不影響取得任意合法的前 k 組。

---

## 2026-10-27

- 221. Maximal Square
- 684. Redundant Connection
- 289. Game of Life

**心得**：
- 221：做了這麼多次，還是覺得這題很難……再做一次，加入 Problem Review、Gary's Choice 與 Essential Problems 的 DP 分類。
- 684：先參考筆記的 Union-Find 怎麼寫，因為有點忘了。加入 Union-Find 原型題與 Essential Problems。
- 289：用 even / odd 來區分 simulation 後的值，難在要 in-place 處理。

**LLM 點評**：
model: GPT-6
- 289：重點是同步更新的語意：第一趟計算每格下一代時，所有鄰居都必須讀取上一代狀態，不能被已更新的格子污染。因此一格需暫存新舊兩個狀態，並明確定義奇偶代表哪一代；常見編碼為 old + 2 * next，此時奇偶（% 2）保留舊值，/ 2 取出新值，第二趟才統一還原。未提供程式碼，不推定本次採用的具體編碼。這是以值域編碼保留原資料的 in-place 技巧；固定檢查八個鄰居，兩趟合計 O(mn) 時間、O(1) 額外空間。見 [In-Place Marking：一格存兩個值](../Algorithms/Design_Principles/In_Place_Marking.md)。
- 684：本次參考筆記複習 Union-Find 寫法後完成。程式在「樹加一條邊」的本題條件下正確：首次 connected 為 true 的邊已是唯一環中輸入順序最後的邊，可直接回傳。原程式 break 後由後往前搜尋也能得到同一條邊：其後的邊若兩端都在當時的連通分量內，就會產生第二個環，與題設矛盾；但此掃描與 representation 均可省略。只有同分量不能在一般圖中區分環邊與橋，此論證依賴題設與輸入順序。實作有 path compression，但沒有 union by rank/size，不宜直接標為嚴格 O(n)；若加入按秩／大小合併，整體為 O(n α(n)) 均攤時間、O(n) 空間。見 [Union-Find 推薦實作](../Algorithms/Union_Find/06-Optimized_Implementation_and_Analysis.md)。
- 221：本次經 code review 修正後完成逐邊長 boolean DP。每輪 width 開始時，dp[i][j] 表示以 (i,j) 為右下角、邊長 width-1 的正方形是否全為 1；左上、左側、上方三個小正方形加當前格，恰好覆蓋目標正方形，故偏移固定為一格，不隨 width 增加。主要卡點是狀態定位與座標轉移的一致性，另需處理字元 '1'、邊長 1 的答案與全 0 情況。時間 O(mn · min(m,n))、額外空間 O(mn) 正確；後續完成 O(mn) 時間的 top-down memoization：將每個位置各邊長的可行性改存為最大可行邊長，以左上角為定位，取右、下、右下三者最小值加一。最後版本在判斷當前格之前必定呼叫三個方向，因此從 (0,0) 出發也能走訪所有位置；當前格為 0 只令本格答案為 0，不阻斷走訪。cache 為 O(mn)，遞迴堆疊為 O(m+n)，總空間 O(mn)。已完成討論後的版本與日後獨立重做分開追蹤。

---

## 2026-10-26

- 542. 01 Matrix
- 90. Subsets II
- 172. Factorial Trailing Zeroes
- 129. Sum Root to Leaf Numbers

**心得**：
- 542：Multi-source BFS。
- 90：一開始只有在 start == nums.size() 時才加入 solution list。但是 set 是空集合也會收集，所以收集的位置是在拜訪的時候。
- 129：滿無聊的遞迴。

**LLM 點評**：
model: GPT-6
- 129：程式正確。進入 sum(node, value) 時，value 表示從根到 parent 所形成數字的 10 倍（根節點為 0）；value + node->val 才是到當前節點的完整數字。葉節點直接回傳該數字，非葉節點把它乘 10 後傳給 children，左右回傳值相加就是此子樹所有 root-to-leaf 數字的總和；空節點回傳 0，不把缺少的 child 當成一條完成路徑。每個節點處理一次，時間 O(n)；呼叫堆疊 O(h)，平衡樹 O(log n)、最壞鏈狀樹 O(n)。練習點是向下傳遞路徑狀態、向上聚合結果；參數提前乘 10 的寫法可行，只要清楚維持其語意。
- 172：已完成逐一分解 1 到 n、累加因子 2 與 5 的數量並取 min 的正確版本，時間 Θ(n)、額外空間 O(1)；對固定因子 p，成功除法總次數為 floor(n/p) + floor(n/p²) + …，合計 O(n)，不因巢狀迴圈直接變成 O(n log n)。先算完整階乘再數尾零是合理的 brute force，但固定寬度整數會 overflow；改為只統計答案需要的因子，避開巨大中間結果。本次未確認完成更進一步的整體計數優化，不將其記為已實作。
- 90：若採用 for 迴圈枚舉下一個選取元素、遞迴傳 i + 1 的建樹方式，每個節點的 path 都已是合法子集，因此應在遞迴入口收集；根節點對應空集合，中間節點也不能漏掉。start == nums.size() 表示沒有下一個候選，不是子集唯一成立的條件；收集答案與停止擴展是兩件事。但若使用逐元素「選／不選」的二元決策樹，在 index == n 的葉節點收集也能涵蓋空集合與所有子集，不能只由空集合推出所有寫法都必須入口收集。Subsets II 另須去重：常見做法是排序後跳過同層相同值（i > start && nums[i] == nums[i-1]），仍允許跨層選取相同值。見 [收集時機與模式 B](../Algorithms/Backtracking/01-Backtracking_Templates_and_Patterns.md) 與 [由 invariant 推導 guard](../Algorithms/Backtracking/07-Guards_from_Invariants.md)；未提供程式碼，不判定具體實作。

---

## 2026-10-25

- 117. Populating Next Right Pointers in Each Node II
- 213. House Robber II
- 151. Reverse Words in a String

**心得**：
- 117：沒 trace 到 queue 裡面還是會有下一個 level 的 node……腦中要一直思考每個工具的狀態。
  - 後續完成不使用額外 queue 的 recursive 版本（經提示修正為先右後左）；一般空間分析仍計入 O(h) 呼叫堆疊。
  - 太酷了……這題的遞迴：divide and conquer。
    1. 先知道 root 的 next 可以用，從更新 child 的 link 的視角來設計。
    2. conquer 順序要對，invariant：進入某個節點處理 children 前，該節點及其右側所需的同層 next 鏈已建立。
  - **再做一次**：獨立重建先右後左的處理順序與 invariant，並用跨越多個無 child 節點的稀疏樹驗證；目前待做。

- 213：多了一個限制條件的 DP。特別注意 edge case：單一元素時，就可以選，沒有頭尾相鄰的問題。

- 151：這算是超經典的 two-pointer technique，裡面還有 reverse、in-place update，滿多技巧的。
  - Code review：j 在前進的時候，就可以先把它放到 k 上了……這個優化太重要，這樣 code 就又更精簡了！

**LLM 點評**：
model: GPT-6
- 117：這份 BFS 程式正確。每層先固定 count=q.size()，處理該層第 i 個節點並 pop 後，queue 前段是本層剩餘節點、後段是已加入的下一層節點；只有 i<count-1 時，q.front() 才保證是同層右鄰居。最後一個必須設 next=nullptr，即使 queue 還有下一層節點也不能接過去。時間 O(n) 正確，queue 空間應為 O(w)，w 為最大層寬，最壞 O(n)，不是 O(log n)；掃描中可能同時保存相鄰兩層的部分節點，但仍為 O(w)。本日接著完成不依賴 queue 的 recursive 版本；題目明確允許遞迴且不計 implicit stack，但一般空間分析仍須計入實際呼叫堆疊，不能把「無 queue」直接等同真正 O(1) 空間。見 [題目 follow-up](https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/)。 後續 recursive 程式的 parent 更新 children 觀點正確：用當前 next 鏈找到右側第一個有 child 的 parent，連接最右 child。初版先左後右會讀到尚未接好的右側鏈；先右後左修正此依賴，提供的稀疏樹反例已確認。使用者以 divide and conquer 理解遞迴拆分；更精確的執行結構是先連 children，再做 right-first preorder DFS，左右子樹因跨樹 next 鏈而有依賴，並非互相獨立的子問題。時間 O(n)：每個 parent 處理一次，每層搜尋時沒有 child 的連續區段只會由其左側最近有 child 的 parent 掃過一次，合計線性；一般空間 O(h)，最壞 O(n)。本次經提示完成與日後獨立重做分開追蹤。
- 213：單一元素確實應直接回傳 nums[0]，不能因頭尾是同一位置就把它視為與自己衝突。當 n>=2，新增限制是第一間與最後一間不能同時選；可分別求排除最後一間的 [0,n-2] 與排除第一間的 [1,n-1] 兩個線性 House Robber 問題，再取最大值。兩類可重疊（頭尾都不選），但求 max 不受影響，且完整涵蓋合法解。重點是限制的適用前提與 base case 一致；未提供程式碼，不判定具體 DP 實作。
- 151：程式正確，結合讀寫指標壓縮空白與雙重反轉。i 是目前掃描位置，j 是單字的半開右邊界，k 是有效前綴長度兼下一個寫入位置；每個單字先反轉，再依原單字順序寫入 s[0..k)，單字間只留一個空白，最後 resize(k) 並反轉整串，便同時反轉單字順序與恢復各字母順序。非首字前至少有一個分隔空白，因此插入一個空白後，寫入起點仍不超過來源 i；由左往右複製不會破壞尚未讀取字元。外層掃描、各單字反轉與搬移、最後整串反轉合計 O(n)，不是迴圈巢狀就相乘。後續 code review：找單字結尾與搬移可合併，在 j 前進時同步寫入 k，省掉另外的複製迴圈，總時間仍為 O(n)。需先記住寫入端的單字起點，再反轉壓縮後的單字區間；不能沿用原始 [i,j) 當反轉範圍。持續維持寫入位置不超過來源位置，才能安全原地掃描。原地處理 s 的額外工作空間 O(1)；函式參數 string s 為傳值，若以 lvalue 呼叫並將參數副本計入，則另有 O(n) 字串儲存，應明確說明分析範圍。

---

## 2026-10-24

- 394. Decode String
- 355. Design Twitter
- 433. Minimum Genetic Mutation
- 435. Non-overlapping Intervals

**心得**：
- 394：異常難欸……stack 處理不好做，finite state machine 也要想。
  - **這題一定要再做一次**：重新釐清解析狀態與 stack 操作，目前待做。

- 355：結果竟然是考 top-k priority_queue。

- 435：基本上算是跟 gpt-6.1-sol 討論，確認我的想法，因為我不想做白工。Greedy：sort by end time，最早結束的人留著，讓後面空間更大；維護最後保留區間的 end time，下一個 start 比它小就不能用。

**LLM 點評**：
model: GPT-6
- 394：難點同時包含字元分類／解析進度，以及巢狀括號中各層上下文的保存與恢復；可以用狀態轉移整理數字、字母與括號的處理，但一般不定深度的巢狀結構仍需 stack 或遞迴記憶，單靠有限狀態不夠。這次單一 stack＋sentinel 的修正版在合法輸入下解碼邏輯正確；已修正 string{1,c} 選到 initializer_list、產生兩字元的問題，應用 string(1,c)，以及最後組合時必須恢復 stack 的反向彈出順序。複雜度不能只依輸入長度 n 寫 O(n)：反覆前插會複製累積字串，即使純字母輸入也可能 Θ(n²)；還須計入解碼輸出長度 L，空間 O(n+L)。後續重練聚焦每層保存什麼、何時合併、片段順序與字串複製成本；原有 Two Stacks／Recursion 目標仍待完成，不以本次單一 stack 版本代替。

- 355：Top-k 可以用固定大小 min-heap 維持最新 10 則：依 timestamp 排序，超過 10 則就移除最舊者；取出時由舊到新，最後需反轉。另一種 k-way merge 才是用 max-heap 保存各作者的最新候選，每次取出全域最新者，再補同作者的前一則。先前未看到 priority_queue 程式碼就將心得指定為 k-way merge，過度推定，已更正。前面的全域時間線版本已修正追蹤方向，但查詢最壞 O(T)，使用者回報超時；heap 方向取決於維持 top 10 淘汰最舊，或直接逐次取最新，不能只由題目名稱決定。

- 435：程式正確。按 end 遞增排序，endTime 始終表示最後一個保留區間的結束時間，count 表示已移除數量；start<endTime 才算重疊，端點相接可以保留。重疊時只增加 count、不更新 endTime，保留已選且不晚結束的區間。Exchange argument：將最佳解的第一個可選區間換成最早結束者，不會妨礙原先後續選擇，故最大保留數不減；最少移除數就是總數減最大保留數。這次最早結束的 greedy 想法由使用者先提出，討論用於確認與補強證明。排序 O(n log n)、掃描 O(n)；掃描本身額外空間 O(1)，常見 std::sort 實作計入遞迴堆疊為 O(log n)。見 [Exchange Argument](../Proof_Techniques/Exchange_Argument.md)。

---

## 2026-10-23

- 106. Construct Binary Tree from Inorder and Postorder Traversal
- 120. Triangle

**心得**：
- 106：Divide and conquer，不是太難……但是一開始放錯 argument 位置。
  - **再做一次**：搭配 hashmap 預建 value → inorder index，獨立實作預期 O(n) 的解法；目前待做。

- 120：標準的 dynamic programming，上下都算好做。但是就要注意 invalid 位置的查表，要從 index check 去避開。

**LLM 點評**：
model: GPT-6
- 106：拆分思路正確：postorder 對應區間的最後一個值決定 root，再由它在 inorder 的位置確定左右子樹的範圍與大小。數值不重複使 value → inorder index 的查表結果唯一；若原本每個子問題都線性尋找 root，最壞時間 O(n²)，預先建表並以 index 區間傳遞、避免切片複製，可降為預期 O(n) 時間，查表空間 O(n)，另有 O(h) 遞迴堆疊。Argument 放錯可藉由固定兩種 traversal 的參數順序、明確命名區間，並確認兩區間長度相同且表示同一棵子樹來降低風險；未提供程式碼，不判定具體錯位原因。Hashmap 版本保留為待完成目標。

- 120：要區分兩種 invalid：索引越界必須在讀取前檢查；索引合法但沒有對應可達狀態，則可用無限大表示，不能初始化成免費的 0。這次一維前綴 DP 的右端 dp[j] 位於已配置陣列內，但上一列沒有該 parent，屬後者；最終以全陣列 INT_MAX、僅 dp[0]=0 初始化，正確統一左右邊界。每輪更新前 dp[j] 是上一列正上方答案、prev 是上一列左上方答案，先 prev=dp[j] 再覆寫才能保留依賴；每個有效位置至少有一個可達 parent，所以 min 不會選到 INT_MAX 再相加。相較原本從當前位置走到底的 suffix 狀態，這版改成從頂端走到當前位置的 prefix 狀態，末列取最小；n 列時時間 O(n²)、額外空間 O(n)。原 top-down 的 cache 檢查另須查 cache[i].contains(j)，不能把兩個座標都查在外層 map。

---

## 2026-10-22

- 80. Remove Duplicates from Sorted Array II
- 162. Find Peak Element（經提示解出）
- 82. Remove Duplicates from Sorted List II
- 137. Single Number II（經提示完成逐位計數版）
- 417. Pacific Atlantic Water Flow
- 209. Minimum Size Subarray Sum

**心得**：
- 80：[...checked, unchecked] + two pointer technique。好像滿經典的，只要想清楚 invariant 就算好做。

- 162：解出來了，靠 gpt-6.1-sol 給提示的……我不可能想到「擠壓」，去比較 mid 跟 mid + 1。

- 82：中規中矩……因為我現在狀態好嗎？Dummy head + ptr 指向最後加入的節點；相鄰節點比較，以 duplicate 記錄目前連續段是否重複。

- 137：經提示想到用 array<int,32> 記錄每個 bit 的次數，再取 % 3 重建答案。One-loop、用 ones / twos 當 state 的做法太 crazy 了，現在有點難思考，先當 follow-up，之後 problem review 再做；目前尚未完成此版本。

- 417：DFS + caching，起點要換位置，destination as source。

- 209：滿經典的 sliding window，要特別注意 update global answer 的時機（這次把 update 跟 fix 做在一起）。

**LLM 點評**：
model: GPT-6
- 80：關鍵確實是先定義區間語義：read 指向下一個待檢查元素，write 指向下一個寫入位置；nums[0..write) 是原始前綴 [0..read) 壓縮後的合法結果，每個值最多保留兩次，而 [write..read) 是已掃描但不屬於有效輸出的區域，不必維護內容。因此 checked 不等於全部保留。常見寫法在 write<2 或 nums[read]!=nums[write-2] 時接納元素；排序保證相同值連續，若與有效結果倒數第二個值相同，再保留就會超過兩次。維持 write<=read，寫入不會破壞未讀資料；read 每輪前進，時間 O(n)、額外空間 O(1)。後續提供的 counter 版本在非空、非遞減排序輸入下正確：每輪開始時 nums[0..k) 是原始前綴 [0..i) 的合法壓縮結果，nums[k-1] 仍等於上一個已掃描值；count 是該值在原始輸入當前連續段的已掃描次數，可能超過 LIMIT，並非已保留次數。相同值超額時雖不寫入，最後保留值仍相同；遇到不同值便重設為 0 再加 1，新段第一個元素必定寫入。寫入前 k<=i，故不破壞尚未讀取資料。k 是下一個寫入位置兼有效長度，註解 last position to place 應改為 next write position / valid length。空陣列會回傳 1；若要支援空輸入，需先回傳 0。此版本已足夠清楚，不必為了省 count 強制改寫。
- 162：這次提示補上的是「用局部坡度證明某一半必有答案」的觀察；之後你已自行說出沿上坡方向必遇到 peak（持續上升則邊界是 peak，否則在首次下降前形成 peak），並推導 [i,j] 至少包含一個 peak 的 invariant 與 i=mid+1 / j=mid 的更新。不是要求整段有序，也不是尋找唯一 peak；捨棄側仍可能有答案，只要保留側必有一個即可。更完整的存在性證明可維持區間端點高於各自外側鄰居（原陣列外視為負無限大），比較 mid 與 mid+1 後更新仍保留此性質；區間最大值因此必是原陣列的 peak。這次是經提示完成，尚不能據此認定已能獨立想到此觀察，但也不能從一次卡住斷定未來不可能推導。後續學習重點是從「哪半不可能有答案」擴展到「哪半能保證存在答案」。未提供完成版本程式碼，未驗證具體實作。
- 82：程式正確，時間 O(n)、額外空間 O(1)。排序讓相同值形成連續段；每輪開始時，duplicate 表示目前這一段在 head 之前是否已看過相同值，與下一個節點相同時設為 true，直到離開該段才結算並重設。ptr 是最後保留節點（尚未保留時為 dummy），dummy.next 到 ptr 的鏈段只含已確認出現一次的完整段；ptr->next 在掃描中仍可能連到待排除節點，需最後收尾。迴圈以 head 與 head->next 判斷段落結束，尾端沒有右鄰居，因此迴圈後依 duplicate 結算最後節點；空串列也能安全處理。最後 if (ptr) ptr->next=nullptr 是必要的斷尾，例如 [1,2,2] 若不斷尾仍會保留重複尾段。每輪 head 前進一步，寫入只修改已掃描節點的 next，不影響後續掃描。單次表現不足以判定精神狀態，但這份程式可觀察到 dummy、輸出尾指標、連續段旗標與收尾都有處理到；與 LC 80 共通的是把掃描位置和有效輸出邊界分開。
- 137：XOR 記錄各 bit 次數的奇偶性，無法消掉出現三次的數；逐位計數取 % 3 可消掉三倍貢獻並保留答案位元。固定 32 位時，計數陣列的額外空間 O(32)=O(1)，時間 O(32n)=O(n)，已符合題目漸近界。交換迴圈只會讓計數器可重用，並非本次指定的單次掃描狀態解法；ones / twos 狀態機版本保留為待完成的獨立目標。
- 417：關鍵是將「每格能否流到海洋」轉成「從各海洋邊界反向找哪些格子能流到它」；正向走向較低或等高，反向必須走向較高或等高。兩個海洋分別維護可達標記，最後取交集。若 caching 指的是這些標記，其作用是記錄已證明的可達性並避免重複展開，不必視為一般遞迴回傳值的 memoization；等高格子可以成環，標記應在展開鄰居前完成。每格對每個海洋最多展開一次，標準反向 DFS 時間 O(mn)、標記與最壞遞迴堆疊空間 O(mn)。後續程式的反向高度條件、分海洋標記與先標記再展開都正確，但邊界初始化漏掉 Pacific 的左下角與 Atlantic 的右上角：第二個 for 排除兩端，而第一個 for 只替 Pacific 初始化上排、Atlantic 初始化下排。反例 [[2,2],[1,2]] 中左下角直接接觸兩海，卻未被 Pacific 標記；已用獨立正向可達性搜尋核對。第二個 for 應遍歷 i=0..m-1，角落重複呼叫由 visited 擋掉即可，單列／單欄也適用。總時間是 O(mn)，不能把每個邊界起點都視為重新走完整張圖，因為同一海洋所有起點共用 visited；額外空間 O(mn)，含最壞 DFS stack。此版尚待確認邊界修正；見 [Destination-as-Source Reachability](../Algorithms/Design_Principles/Transformation_Patterns/Destination_as_Source_Reachability.md)。
- 209：把 update 放在 fix 裡是合理的：若以 while (sum>=target) 持續縮窗，應在移除左端元素前，用目前仍合法的窗口長度更新最小值；縮到不合法才離開迴圈，這時不能直接把該窗口當候選答案。全正數保證右擴增加總和、左縮減少總和，使左端能單向前進；每個元素最多加入與移除一次，時間 O(n)、額外空間 O(1)。更新位置取決於 fix 停下來時的 invariant，並非一律放在 fix 前或後：若改以「移除左端後仍合法」作為縮窗條件，則可在 fix 後確認合法再更新。未提供程式碼，此處只評估觀念；見 [Fix Condition from Invariant](../Algorithms/Sliding_Window/03-Fix_Condition_from_Invariant.md)。

---

## 2026-10-21

- 494. Target Sum（經提示練習，尚未掌握）
- 103. Binary Tree Zigzag Level Order Traversal
- 416. Partition Equal Subset Sum（經提示修正 bottom-up，仍待獨立重做）

**心得**：
- 494：recursive 到 top-down Counting DP 好寫，但是 bottom-up Counting DP 實在太難了……又是這種 bottom-up 超難的題目，第二次了（前一次是 91. Decode Ways）。
  - 這個 range 很難想：要先想到總和，然後還要處理值域超過 index 的問題。完全是靠 gpt-6.1-sol 幫忙 review……目前這題還是不行，尚未能獨立完成。
  - 複習重點：自己推導可達總和範圍、值域到下標的映射與轉移來源的邊界；本次經提示練習不代表已掌握。

**LLM 點評**：
model: GPT-6
- 416：本次 bottom-up 嘗試的轉移式正確：dp[i][w] 表示從 nums[0..i] 選取子集，能否恰好湊到 w；選／不選分別來自 dp[i-1][w-nums[i]] 與 dp[i-1][w]。主要問題是 base case 與表格維度：n 應與元素數 nums.size() 一致，目前減 1 卻仍拿來配置列數，單元素偶數輸入會配置零列後存取 dp[0]；即使一般等分判定可利用互補性省略一個元素，這也不是本次表格設計已說明的假設。需設定 dp[0][0]=true，讓不選第一個元素的後續分支能從空集合出發；只有 nums[0]<=target 時才能寫入 dp[0][nums[0]]，否則越界。以 [1,2,1] 為例，缺少空集合基底會漏掉單選 2 的合法方案；[3,1] 則在第一列初始化越界。尾端註解 dp[0,target]=true 也不符合狀態，target 不一定只用第一個元素就能達成。後續已依提示修正為 n=nums.size()、dp[0][0]=true，並以 if 保護 dp[0][nums[0]] 的存取，最終貼出的 bottom-up 程式正確。已釐清「比較式只決定寫入值，if 才能保護下標存取」；也討論了以前 i 個元素定義狀態，可用第 0 列表示空問題、統一第一個元素的轉移。這次經提示修正，不將待獨立重建的複習目標標為完成。見 [Knapsack DP](../Algorithms/Dynamic_Programming/Problem_Types/Knapsack_DP.md)。
- 494：這次難點可拆成狀態語義、計算順序與值域表示。你貼出的 bottom-up 定義是「使用 nums[0..i] 得到總和 W 的方法數」；若 top-down 問的是「從 i 開始，剩下能完成 target 的方法數」，兩者不只遞迴／迴圈不同，也改了子問題的意義。可先保留原遞迴狀態與轉移，再依依賴安排填表，避免同時改變多個設計。此表依最後一次符號選擇分成兩類：選負號由 W+nums[i] 轉入，選正號由 W-nums[i] 轉入，累加的是來源狀態的全部方法數。nums[i]=0 時兩種符號仍是不同選擇，故即使來源格相同也要加兩次，初始化須用 +=。另須區分元素數 n、數學總和 W 與陣列下標 W+S；初版缺 target 在 [-S,S] 外直接回傳 0 的檢查，否則讀取答案時可能越界；後續已貼出補上檢查的正確版本，但仍保留獨立推導的複習目標。令 S=sum(nums)，時間、空間為 O(n(S+1))，屬依數值範圍計算的偽多項式界。與 LC 91 的共同學習點是「狀態定義與求值順序分開設計」，不是所有 bottom-up 都必須改成前綴狀態；見 [Counting DP](../Algorithms/Dynamic_Programming/Problem_Types/Counting_DP.md) 與 [Knapsack DP](../Algorithms/Dynamic_Programming/Problem_Types/Knapsack_DP.md)。

---

## 2026-10-20

- 15. 3Sum
- 91. Decode Ways

**心得**：
- 91：top-down DP 好做，從 recursive 推導過來，但是 bottom-up Counting DP 異常難做。加入複習清單，再推導一次。
- 15：從 brute force 才有辦法推導出 O(n³) 到 O(n²) 的解法，關鍵是 brute force。這題最難的是移除重複的項目，要把 index 做聰明的移動。
  - Running hashmap：time O(n²)、space O(n)。內層去重複的邏輯不好想，很不直覺，很像湊出來的。關鍵就是：要先確認存在後，才跳 index（這樣相同值才有機會被加入，真的很像湊出來的判斷式）。
  - 後續狀態確認：sort + two pointers 已完成，目前只剩 no-sort 版本尚未嘗試，列入後續練習。

**LLM 點評**：
model: GPT-6
- 91：前綴計數轉移正確；`dp[i]` 是前 i 個字元 `s[0..i)` 的解碼方式數，i 是長度／切點，答案為 `dp[n]`。依最後一個編碼使用 1 或 2 字元分組，兩類互斥且完整：單字元合法時加 `dp[i-1]`，雙字元在 10..26 時加 `dp[i-2]`。加的是來源前綴的全部解法數，不是 +1；每種前綴解法接上固定合法編碼，各產生一種新解法。`dp[0]=1` 表示空前綴有一種完成方式。尾端註解的 +1、`dp[n-1]` 與實作不符，須修正。Top-down 若使用 suffix 狀態，可以保留同一語義由右往左填表，不必同時改成 prefix；先固定狀態，再依依賴關係決定填表方向。`count==0` 提前結束在本題成立：若完整解碼跨過該切點，跨界兩位編碼的首位必為 1 或 2，可暫時獨立解碼，因此任何可延伸的完整答案都會使此前綴可解碼。時間 O(n)、空間 O(n)，substr/stoi 僅處理固定 2 字元。另有整數風險：46 個 1 接一個 0，最終答案為 1836311903，但長度 46 的前綴計數為 2971215073，超過 signed 32-bit；已以任意精度計算確認，不能只憑最終答案界認定 int 中間狀態安全。複習聚焦狀態、最後一步分類、空前綴基底與 0 的合法性；見 [Counting DP](../Algorithms/Dynamic_Programming/Problem_Types/Counting_DP.md)。
- 15：這次推導從排序後枚舉 i < j < k 開始，先確保覆蓋所有三元組，再把第三層搜尋轉成補數存在性查詢：固定 i、j，只需判斷補數的最右 index 是否 > j，以預期 O(1) 查詢得到整體預期 O(n²) 時間、O(n) 額外空間。去重的依據是輸出比較 value 組合，而非 index 組合；同一層的目前值處理完後跳過相同值，下一層仍可使用另一個相同值的位置，因此不會漏掉含重複值的合法答案。對固定 i、j，找到一個合法補數位置即可，不應把所有相同補數的位置各輸出一次。你也已想到固定 i 後，在排序區間 [i+1, n-1] 用 two pointers 找和為 -nums[i]；目前未提供該版本程式碼，因此保留其獨立實作與去重驗證目標。這次經驗適合對照 [Brute Force 關鍵設計](../Algorithms/Brute_Force/README.md)：先建立正確枚舉，再辨認可替換的重複搜尋。 本日接著完成排序後的 running hashmap 版本：固定末端位置 end，在前綴用 set 查補數。查詢時 set 只包含目前位置之前看過的值，先查再加入可保證使用不同位置；找到答案前不能直接跳過相同值，因為相同值的第二個位置仍可能形成合法配對。固定 target 與目前值 x 後，補數 target-x 唯一；一旦已輸出這組值配對，後續相同 x 不會形成新答案，因此可跳到這段相同值的最後位置，再由 for 前進至下一個不同值。這是依輸出值等價性去重，有明確依據；重點是保留合法位置的機會，而不只是讓相同值加入 set。時間為預期 O(n²)，額外空間 O(n)，不含輸出；ans 為 member，重複呼叫時須清空。Running hashmap 已於 2026-10-20 完成，與先前誤記的九月完成狀態分開；稍後使用者亦確認 two pointers 完成，目前只剩 no-sort 待練。

---

## 2026-10-19

- 25. Reverse Nodes in k-Group
- 124. Binary Tree Maximum Path Sum
- 84. Largest Rectangle in Histogram
- 416. Partition Equal Subset Sum

**心得**：
- 25：一路最佳化才慢慢寫出來……其實思路很簡單：
  1. 使用 k-gap pointer 去找 tail。
  2. 實作 space O(1) 的 reverse。
  3. 處理 reverse 完的頭尾要前後接回去。
  4. 當尾巴不夠 k，就提前結束。
- 124：關鍵設計沒有處理好：path 只可以從一個 child 去組成。
  1. tree dp: top-down dynamic programming。
  2. global tracking。
  3. conquer 的部分要注意組成 path 的條件：path 只可以從一個 child 去組成。
- 84：我覺得這題的出發點跟裝水題還是很像，要先想到從自己出發，然後要去左右找比自己小的當邊界（可以擴展的最遠）。然後因為有 redundant work，所以要記錄下來。還是要從暴力法開始想，這個 O(n) 解才有可能想到。
  1. 要先想到假設自己全拿，從自己出發，往左往右找邊界。
  2. 找邊界可以用 monotonic stack 去記錄右邊跟左邊最大的（因為再來都比它小，就不可能是邊界了）。
  3. 只要最大的人比自己小，那就是邊界，所以就可以用 top 當邊界。
  4. 最後，two pass，拿邊界來算每個人擴展後的面積。
  - follow-up：這題要再做一次，優化 monotonic stack 解法；另外再做 divide and conquer 版本。
  - 下次想試單一 monotonic stack：從左到右掃描，彈出時直接計算面積，最後處理 stack 剩餘項目。感覺是某種設計模式，這次先不深入，下次再理解與實作；目前尚未完成此版本。
- 416：從頭到尾都是靠 gpt-6.1 提示的……而且我不知道這在幹嘛。這題根本就是經典的想從 backtracking（暴力法）推導到 top-down dynamic programming（caching）而已吧。
  - 補充：這題真的是經典的 Knapsack Problem、0/1 Knapsack、dynamic programming。感覺只要可以設計出數值（sum / remaining）的範圍，就幾乎可以改成查表；想釐清候選與值域的 pseudo-polynomial 類型。
  - 發現這題根本是把問題轉成「是否存在子集和為 target」。應該先做一些直接給定 target 的 Subset Sum 前置練習。
  - **必做、再做一次**：先理解固定 target 的原始問題，再回來獨立重做 416；目前經提示完成不代表已理解。

**LLM 點評**：
model: GPT-6
- 416：這條推導方向正確，但關鍵不是只加 cache，而是先確認哪些搜尋分支代表同一個剩餘問題。總和為 S 時，只需判定能否選出總和 S/2 的子集，另一組就是未選元素；S 為奇數直接失敗。`dp(i, remaining)` 的語義是「從 nums[i..n) 各元素最多選一次，能否湊出 remaining」。選／不選都前進到 i+1，維持每個元素只用一次；不同歷史只要 i 與 remaining 相同，可用元素及目標就相同，因此後續布林答案可以共用，這才是 memoization 成立的理由，也是 0/1 subset sum 的狀態。最終程式正確，cache 三態 0／1／-1 區分未算／可行／不可行；只在元素用完且 remaining 為 0 時成功也成立，因為中途湊滿後仍可一路不選到結尾。令 T=S/2，總和計算 O(n)，偶數分支配置與搜尋為 O(nT)，cache O(nT)，另有 O(n) 遞迴堆疊；更精確可寫 O(n(T+1))，且這是依數值目標 T 計算的偽多項式界。這次是經提示完成，不代表已能獨立重建狀態與轉移；見 [DP Problem-Solving Framework](../Algorithms/Dynamic_Programming/Fundamentals/02-Problem_Solving_Framework.md)。 數值有界只是可查表的重要訊號，還須確認狀態充分、依賴有進度、所有維度乘積與每格轉移成本可負擔；候選數 n 在 0/1 模型是進度軸，在可重用模型也可能是每格枚舉 choices 的成本。已補強 [候選進度 × 數值範圍與偽多項式時間](../Algorithms/Dynamic_Programming/Subset_Sum/01-Subset_Sum_and_NP_Completeness.md)。
- 84：最終雙 stack／左右邊界陣列版本正確，時間 O(n)、額外空間 O(n)。推導是先固定 `heights[i]` 為矩形高度，找左右最近嚴格較矮的位置，再計算 `heights[i] * (right[i] - left[i] - 1)`；任一矩形都有最低柱子，以它為高度延伸到完整合法區間，面積不會更小，因此涵蓋最優解。心得第 2、3 點要精確化：stack 存的是「最近較矮邊界的候選 index」，不是左右最大值；對應高度由底到頂嚴格遞增，彈掉所有 `>=` 自己的候選後，top 才是最近嚴格較矮的位置，相等高度不能阻擋擴張。被彈出的候選已被目前這根更近且不更高的柱子取代，對未來查詢不再有用；每個 index 在每個 stack 各入棧、出棧至多一次，避免暴力法反覆掃描，總時間才降為 O(n)。`left/right` 是 boundary arrays，沒有 hashmap。程式把左右兩個方向的掃描交錯在同一個迴圈，再用另一個迴圈算面積；邏輯上是兩次邊界掃描加一次求值，三次線性走訪仍是 O(n)。與裝水題共同點是從當前柱子分析邊界，但本題遇到較矮柱子即不能維持原高度擴張。見 [Monotonic Stack：Search Space Conversion](../Data_Structures/Stacks_and_Queues/Monotonic_Stacks/02-Search_Space_Conversion.md)。這次經提示完成兩側掃描與邊界記錄，尚不代表已能獨立重建。
- 124：要區分「回傳給父節點的可延伸路徑」與「更新全域答案的完整路徑」。前者以當前節點為端點，最多接一個 child，否則再接父節點會產生三叉；後者可以在當前節點接左右兩側，形成合法的 child → node → child 路徑。若左右回傳值為 L、R，向上回傳 `node->val + max(0, L, R)`，全域候選為 `node->val + max(0, L) + max(0, R)`。負貢獻可以不接，但答案必須包含至少一個節點，全域答案不能初始化為 0，以免全負數時錯誤。計算須先取得左右子樹結果再合併，因此是 postorder、由下而上的 Tree DP；遞迴呼叫從 root 開始，不代表狀態是 top-down DP。每條非空路徑都有唯一最高節點，在該節點合併兩側即可涵蓋所有候選；每個節點處理一次，時間 O(n)、遞迴空間 O(h)，最壞 O(n)。可對照 [Path-Based Thinking 與 Postorder 聚合](../Data_Structures/Trees/Path_Based_Thinking_Aggregation.md)。未提供程式碼，以上只評估概念與狀態設計。
- 25：最終程式在題目條件下正確，時間 O(n)、額外空間 O(1)。外層的 `head` 實際是「下一組的前驅」，可命名為 `groupPrev`；每輪開始時，它以前的完整群組皆已反轉並接好，`head->next` 是尚未處理的 suffix。先往前走 k 步確認整組存在，不足就不修改；反轉後舊 `start` 成為組尾，也是下一輪的前驅，因此每輪確實推進 k 個節點。`reverse` 先保存 `end = tail->next`，讓 `dummy.next` 初始指向後繼；逐一把節點前插到它前面，維持「已反轉前綴接到 end」，所以組尾會自動接回後段，外層只需把前驅接到新組頭。找組尾與反轉各走一次該組，合計仍為 O(n)，尾端不足 k 的區段最多再掃一次。真正要固定的是三個角色：組前驅、反轉後的組尾、區段後繼；見 [Linked Lists：K-Gap 與 Dummy Node](../Data_Structures/Linked_Lists/README.md)。註解 `if not enough, just reverse until end` 與題意及實作相反，應改為「不足 k 個時保持原順序」。

---

## 2026-10-18

- 77. Combinations
- 399. Evaluate Division

**心得**：
- 77：這題就是標準的 backtracking，但是在考數學以及極致的 promising 設計。
- 399：滿複雜的 DFS 問題搭配遞迴求值，尤其要小心倒數也成立；下次練習 weighted Union-Find。

**LLM 點評**：
model: GPT-6
- 77：`start` 限制後續只選更大的數，讓每個大小為 `k` 的組合恰好出現一次。promising 可從「剩餘數量至少要補足缺口」推導：目前還缺 `k - sol.size()` 個，候選 `i` 選下去後，`i..n` 至少要有這麼多數，因此 `i <= n - (k - sol.size()) + 1`；超過此界的分支不可能完成，可在選取前停止迴圈。完整解的檢查必須先於 `start > n`，否則最後選到 `n` 的合法組合會被略過。見 [Backtracking Templates and Patterns](../Algorithms/Backtracking/01-Backtracking_Templates_and_Patterns.md)。
- 399：你的 DFS 回傳值語意是 `node / dst`；邊權為 `node / neighbor`，乘上子遞迴的 `neighbor / dst` 即得到 `node / dst`，因此回溯時相乘正確。`a / b = v` 必須同時建立反向邊 `b / a = 1 / v`；同一 query 的 `visited` 不需還原，題目保證關係一致，找到任一路徑即可回傳。時間 O(E + Q(V + E))，額外空間 O(V + E)，另有 O(Q) 答案空間。下次另練 [Weighted Union-Find](../Algorithms/Union_Find/10-Weighted_Union_Find_with_Path_Compression.md)，目前只記錄 DFS 版本完成。

---

## 2026-10-17

- 61. Rotate List
- 63. Unique Paths II
- 71. Simplify Path

**心得**：
- 61：先算串列長度 `n`，把右旋步數縮成 `k % n`；新 head 在原 head 往前走 `n - k` 步的位置。這版切在新 head 前，再找到原 tail 接回原 head；時間 O(n)、額外空間 O(1)。小 trick：算長度時順便記住 tail，就能在處理完 `k % n` 後把 tail 接到 head，當成環來找切點。
- 63：Counting DP，沒有什麼特別的；加入 Archetype Problems 的 Counting DP。
- 71：string tokenization + stack；tokenization 還不太熟。看到 stack-like 容器可以用 for loop 從底到頂走訪，覺得很酷，想記進 C++ one-liner。

**LLM 點評**：
model: GPT-6
- 61：程式正確處理空串列、單節點、`k % n == 0`；其餘情況 `1 <= n - k <= n - 1`，因此 `prev`、`newHead` 和最後的 tail 都存在。切斷 `prev->next` 後，將舊 tail 接到舊 head，即得到右旋結果。最小的改進是在第一次走訪同時取得 `n` 與 tail，沿用目前切點寫法，直接用已保存的 tail 接回 head，不必再找一次。也可先算 `shift = k % n`，若非 0，再設 `tail->next = head` 形成環；從原 head 走到第 `n - shift - 1` 個節點作為 newTail，令 `newHead = newTail->next`，最後斷開 `newTail->next`。不要在 `shift == 0` 時留下環。兩種寫法都是 O(n) 時間、O(1) 額外空間；差別只有常數步數與接點順序。
- 63：分類正確；`dp[r][c]` 計算到達該格的路徑數，開放格累加上方與左方，障礙格的路徑數為 0。起點是障礙時答案為 0，否則起點要以 1 作為計數基底；第一列、第一欄也要遵守同一個規則。這是 LC 62 的轉移加上無法通行格的限制；見 [Counting DP](../Algorithms/Dynamic_Programming/Problem_Types/Counting_DP.md)。未看到程式碼，因此只評估題型與狀態設計。
- 71：用 `std::getline(stream, token, '/')` 切出路徑片段，空片段與 `.` 跳過，`..` 在非空時移除最後一個目錄，其他片段加入。若使用 `std::vector<std::string>` 當 stack，`push_back`／`pop_back` 是 LIFO，而 range-based `for` 會依插入順序從底到頂走訪，方便組回路徑。真正的 `std::stack` 是容器配接器，沒有 `begin()`／`end()`，不能直接用 range-based `for`；已補進 [C++ One-Liners](../Cheatsheet/CPP_One_Liners.md)，既有 [Container Iteration Order](../CPP_Reference/Container/Container_Iteration_Order.md) 也有相同區分。未看到程式碼，因此不判定具體實作。

---

## 2026-10-16

- 31. Next Permutation
- 8. String to Integer (atoi)
- 40. Combination Sum II
- 12. Integer to Roman
- 43. Multiply Strings

**心得**：
- 31：靠杯難...花了約 25 分鐘。先找到右半 reverse sorted 的起點，再把 suffix 反轉，找第一個比 pivot 大的值往前 swap；最麻煩的是 duplicate case。用 `i - 1` 看前一個 index，擔心越界；看到另一種從 `n - 2` 開始、看 `i + 1` 的作法，感覺自己沒練到往後看 pair 的肌肉記憶。這題再練習一次。
- 8：這題很硬...結合了 Finite State Machine 還要溢位判斷。溢位跟前幾天刷的 7. Reverse Integer 幾乎一樣，可以記錄兩題的關聯；起始式都是在 append digit 前檢查 `result * 10 + digit`。
- 40：關鍵兩個設計：1. sort，讓 state 可以往下，trim 掉不可能的 path。2. 在 candidate promising 確認時，同數值的只可以用一次，避免重複答案；但同數值仍可一起出現在答案裡，因為 backtracking 的下一個狀態從當前位置的下一個位置開始。確認同數值的起點要用 `start`，不要越界去確認。這題一定要再做一次。
- 12：鳥鳥的...想少用空間，結果判斷式變多。去年寫死全部數字，這次只寫死一半、用位數、`pow` 和 mapping 逐步扣掉 `num`；`6` 先扣 `1` 變成 `5`，下一輪就選到 `V`，所以這版仍正確，只是不夠有效率地讓 `num` 接近 0。最簡單的 simulation 應是把合法面額按大到小列成表；**羅馬面額的排序是重點**，每次選第一個扣得掉的面額，讓 `num` 逐步降到 0。
- 43：做了 35m 46s。這題太複雜了，這次沒辦法獨立完工，一路靠 gpt-6.1-sol 提示。先 reverse 兩個字串，讓 index 好處理；用大小為 `m + n` 的 extra space，把每對 digit 的 product 放到對應位置；最後走訪 extra space，處理進位並組成結果，再 reverse 回來。要去掉 leading zero，也要處理其中一個數值為零的情況（或一開始就特判）。列入 Essential Problem；體感 Medium 偏難。這題一定要重做一次。

**LLM 點評**：
model: GPT-6
- 31：程式在題目 `n >= 1` 的條件下正確；以含重複值的小陣列做了窮舉比對。`i` 是最長非遞增 suffix 的起點，`i - 1` 才是 pivot；`i > 0 && ...` 的短路判斷避免 `i - 1` 越界，`n = 1` 也安全。`>=` 把相等元素留在 suffix，反轉後它非遞減；從左找第一個嚴格大於 pivot 的值並交換後，suffix 仍非遞減，因此結果是恰好下一個排列。若 `i == 0`，整列已是最大排列，反轉即回到最小排列。常見寫法從 `n - 2` 找 pivot，先交換，再反轉 suffix；與目前「先反轉，再找最小較大值交換」等價。`j < n` 的保護在有 pivot 時其實不會觸發；註解 `first bigger then nums[i]` 應改為「比 pivot `nums[i - 1]` 大」。時間 O(n)、額外空間 O(1)。見 [LeetCode Tricks and Keywords](../Cheatsheet/LeetCode_Tricks_and_Keywords.md)。
- 8：FSM／階段解析決定哪些字元可被接受：前導空白、可選符號、連續數字，遇到後續非數字就停止；溢位判斷只在 append digit 時發生。與 LC 7 共用 `result * 10 + digit` 的「先檢查、再更新」模式；直接計算後才比較可能已溢位。若 LC 8 用非負 magnitude 累積，正數上限是 `2147483647`，負數上限可到 `2147483648`，所以末位臨界值分別是 7、8；判斷 `result > limit / 10` 或等於且 `digit > limit % 10`。LC 7 的 `% 10` 直接產生帶符號 digit，超界回傳 0；LC 8 從字元讀非負 digit 並另存 sign，超界要夾到對應上下界。見 [整數溢位防範心法](../CPP_Reference/Type/Integer_Overflow_Prevention.md#場景七overflow-判斷移項技巧)。未看到程式碼，故只評估概念關聯。
- 40：兩個設計要分清：`start` 限制下一層只能選目前位置以後的元素，遞迴傳 `i + 1` 才保證同一個輸入位置只用一次；排序讓較大的候選可用 `candidate > remaining` 安全剪枝，也讓相同值相鄰以便去重。去重只發生在同一層：`i > start && candidates[i] == candidates[i - 1]` 時跳過這個分支；下一層有新的 `start`，仍可選另一個相同值，例如 `[1,1,6]` 能構成 8。若寫成 `i > 0`，會錯刪合法答案。這是「同層同值只展開一次、不同層可選不同位置」的不變量；見 [Guards from Invariants](../Algorithms/Backtracking/07-Guards_from_Invariants.md)。未看到程式碼，因此不評斷具體實作。
- 12：先前誤判 `6` 會輸出 `IIIIII`，是漏看每輪的 `num -= value`；實際流程是 `6 → 5 → 0`，依序前置 `I`、`V`，得到 `VI`。重新以相同流程檢查題目範圍 `1..3999`，結果皆與標準表示相符。這版按位數處理，`6`、`7`、`8` 先逐次扣該位的 1，再落到 5；前置串接讓低位先產生也能排在高位後。固定表格的 Greedy 關鍵是**面額由大到小排序**（包含 `4/9` 的減法形式）：從頭找到第一個 `value <= num`，它才是目前最大的可用面額；扣掉並把符號接到尾端。若排序錯了，第一個可扣面額未必正確。每次都有正的扣減，因此會終止於 0。這是較直接的 simulation，但兩種寫法在本題固定範圍內都是 O(1) 額外空間；差別主要是選面額的規則與程式複雜度。
- 43：反轉後從低位開始，位於 `i`、`j` 的 digit 乘積貢獻到結果的 `i + j` 位；先全部累加，再從低位向高位統一傳遞進位。`m + n` 格足夠，因為兩個長度為 `m`、`n` 的非負整數相乘最多有 `m + n` 位。這樣把「乘積對齊」與「進位」拆成兩趟，避免在內層迴圈同步操作結果字串；最後移除前導零時要保留單一的 `"0"`。最後貼出的版本邏輯正確，時間 O(mn)、額外空間 O(m+n)；`num1`、`num2` 按值傳入並反轉，還包含兩份字串副本。可對照 [Simulation Design Framework](../Algorithms/Simulation/01-Simulation_Design_Framework.md)。

---

## 2026-10-15

- 746. Min Cost Climbing Stairs
- 763. Partition Labels
- 973. K Closest Points to Origin
- 981. Time Based Key-Value Store
- 51. N-Queens
- 1046. Last Stone Weight
- 7. Reverse Integer
- 24. Swap Nodes in Pairs

**心得**：
- 763：用 left & right bound 轉化成 interval merge 的問題...這是靈感吧？！程式碼好像可以更精簡？
- 981：根本就是在考 upper bound 的實作。
- 1046：沒注意到...至多一個回傳值，如果沒有剩餘，要回傳 0。超粗心...另外 priority_queue 輸出的第一個一定比較大，根本不用比較 top1 跟 top2 大小。
- 7：硬做正負兩個 case，把負轉正再做，還要排除最小負數，怕轉正會 overflow，整個很複雜。但發現負數 `% 10` 其實也會取出帶負號的 digit：`-3 % 10 == -3`，不是 7。這個我們筆記有嗎？

**LLM 點評**：
model: GPT-6
- 763：轉成區間合併是正確的結構推導：同一字元的所有出現位置必須同段，因此其 first～last 是不可拆的區間；交疊區間必須合併，互不交疊的合併結果可各自成段，得到最多段數。程式的排序與合併條件可行；不同字元的端點不會佔同一位置，故用 `>` 判斷交疊成立。令 k 為不同字元數，時間 O(n + k log k)、輔助空間 O(k)；英文小寫字元使 k ≤ 26，所以可寫 O(n) 時間、O(1) 輔助空間。可只預處理每個字元的 last index，再由左至右維持目前段的最遠結束位置 `end = max(end, last[s[i]])`，走到 `i == end` 就輸出段長；這是直接掃描已排序的出現位置，省去 first bound、區間列表、排序與合併列表。
- 981：`get(key, t)` 要找該 key 最後一個 timestamp `<= t`：`upper_bound(t)` 找第一個 `> t`，其前一筆才是答案；若結果位於開頭，代表沒有符合時間的版本，回傳空字串。每個 key 的時間序列因 `set` 的 timestamp 遞增保證而有序，才能二分搜尋。也可直接二分「最後一個 `<= t`」。目前沒有程式碼，因此只評估這個搜尋觀察；見 [Binary Search Standard Template](../Algorithms/Binary_Search/00-Binary_Search_Standard_Template.md)。
- 1046：使用預設的 `priority_queue<int>`（max heap），連續取出兩次時第一顆 `x` 必定不小於第二顆 `y`，直接計算 `x - y` 即可；若相等則兩顆都消失，不必放回 0。每輪取出兩顆後，石頭數至少減一，所以最後 heap 只可能空或剩一顆；回傳時先判斷 `empty()`，空則回傳 0，否則回傳 `top()`。未看到程式碼，因此不判定具體錯誤位置。
- 7：有， [LeetCode Tricks and Keywords](../Cheatsheet/LeetCode_Tricks_and_Keywords.md) 的 LC 7 條目已記「C++ Modulo Operator Returns Negative if input is negative」。C++ 有號整數除法向零截斷，且 `a == (a / b) * b + a % b`，所以 `-3 / 10 == 0`、`-3 % 10 == -3`；`-123` 依序取到 `-3, -2, -1`。可直接在負值上做 `% 10`、`/ 10` 並累積反轉，不必先取負而碰到 `-INT_MIN`。每次計算 `rev * 10 + digit` 前仍須檢查 32-bit 上下界：`rev > INT_MAX/10` 或等於時 `digit > 7`；`rev < INT_MIN/10` 或等於時 `digit < -8`。未看到程式碼，因此不判定原實作細節。

---

## 2026-10-14

- 438. Find All Anagrams in a String
- 621. Task Scheduler
- 739. Daily Temperatures
- 637. Average of Levels in Binary Tree
- 703. Kth Largest Element in a Stream

**心得**：
- 438：Sliding Window，關鍵是設計夠好的 constraint metrics（letter count and equal count）。
  - 程式用 `right - left + 1 > p.length()` 判斷何時 fix；固定大小 k 的視窗也可以由目前的 right 推得離開的 index 是 `right - k`。
- 621：一開始方向對，但是設計到 cold queue 時，沒想到可以把 next 可以執行時間直接放進去 queue，讓每回合可以看 queue 的頭。Simulation + Greedy / Priority Queue。
- 739：code review...不用存數值，存 index，拿 index 去取數值即可。糟糕...看完解答，我發現我做反了：其實很直觀地 maintain 一個 non-increasing 的 monotonic stack，判斷當前跟 top；如果比 top 大，那些被 pop 出來的人就找到答案了。原本是從右往左 traverse，維護下一個更高溫的候選。
- 637：nothing special...tree 的 level ordering 怎麼做？好像 BFS 最直覺；有需要做 DFS 版本嗎？
- 703：k-size min heap。code review...只要無腦 push 到 min heap 就好了，根本不用去比 top 是否比新的小，因為 push 進去後，小的就會被 pop 出來了。

**LLM 點評**：
model: GPT-6
- 438：實際程式的 `equal` 不是「目前頻率恰好相等」的種類數，而是目標字元中 `letters[c] >= target[c]` 的種類數：加入字元升到目標值時加一，移除字元從目標值降到不足時減一；超過目標值仍維持達標。先 expand、視窗長度超過 `k = p.size()` 時移除左端一字元，再 update，可維持長度至多 k。長度恰為 k 時，所有目標字元都達標當且僅當頻率完全相等；長度小於 k 時不可能全部達標，所以 `equal == targetCount` 的判定正確。若目前右端為 `right`，超長時移除的是 `right-k`，修正後 `left = right-k+1`；改用索引直接推導時仍須更新離開字元的計數。時間 O(|s|+|p|)、固定 26 字母的額外空間 O(1)。[Frequency Matching Counting Invariant](../Data_Structures/Hash_Tables/Frequency_Matching_Counting_Invariant.md) 使用的是「頻率恰好相等」的另一種計數定義，更新規則不同。
- 621：分開維護可執行的 task 與冷卻中的 task。時間 t 執行某 task 後，若還有剩餘次數，記錄 `readyTime = t + n + 1`；每回合先讓到期者回到候選集合，再從中挑選。因時間單調前進且 n 固定，後加入冷卻 queue 的 readyTime 不會早於前者，所以檢查 queue 頭就夠。這是冷卻 queue 可用 FIFO 的不變量；目前未看到完成版程式，僅評估設計思路。
- 739：貼出的反向走訪程式正確；方向與解答相反，但並未做錯。從右往左時，stack 保存右側仍可能成為「下一個嚴格較高溫」的候選 index；遇到 `temperatures[i] >= top` 就 pop，因目前 i 更近且溫度不低於被移除者，後者不可能再是更左側位置的最近較高溫。pop 後的 top 是 i 的最近較高溫位置；相等溫度必須 pop，因題目要求嚴格較高。正向走訪則保存尚未找到答案的 index，當前溫度嚴格高於 top 時，才替被 pop 的 index 填答案。兩種方向皆 O(n) 攤銷時間、O(n) stack 空間；只存 index 即可由 `temperatures[index]` 取值，也能直接算距離。見 [Monotonic Stack and Queue](../Data_Structures/Stacks_and_Queues/Monotonic_Stacks/01-Monotonic_Stack_and_Queue.md)。
- 637：按層 BFS 在每輪開始先固定 `levelSize = queue.size()`，只取出這麼多個節點並累加 sum；新加入的子節點留給下一輪，處理完用 `sum / levelSize` 得到該層平均。DFS 也可傳入 `depth`，對每個深度分別維護 sum 與 count；它會深入子樹，並不真的依層走訪。這題用 BFS 已足夠，DFS 只在想練「依深度聚合」時再做。兩者皆 O(N) 時間；BFS queue O(W)，DFS 遞迴堆疊加每層統計 O(H)。見 [BFS](../Data_Structures/Trees/BFS.md)、[DFS for Level Order Traversal](../Data_Structures/Trees/DFS_for_Level_Order_Traversal.md)。
- 703：每次 `add` 先 push，再於 heap 大小超過 k 時 pop 最小值；不變量是 heap 保留至今最大的 `min(k, 已見元素數)` 個值（包含重複值）。至少見過 k 個元素後，top 就是第 k 大。事前比較新值與 top 只是可省去部分 push/pop 的最佳化，並非必要。每次 `add` 時間 O(log k)，heap 空間 O(k)。

---

## 2026-10-13

- 530. Minimum Absolute Difference in BST
- 572. Subtree of Another Tree

**心得**：
- 530：一開始看錯題目，想成一般的 tree，用 hashmap + traverse hashmap。後來看到是 BST，改用 inorder + external state 解決。
- 572：就是無腦遞迴比較，過程中還要先做出一個 same tree 的函式，可以說是比 same tree 還要難一點的題目。

**LLM 點評**：
model: GPT-6
- 530：BST 的 inorder 會依值遞增走訪；在排序後的序列中，最小絕對差必定出現在相鄰值之間，因此只需用 external state 保存前一個值與目前最小差。第一個節點沒有前值，要跳過比較。若用遞迴走訪，時間 O(n)、遞迴堆疊 O(h)，其中 h 是樹高；未看到程式，無法判定具體實作細節。
- 572：可拆成兩層遞迴：對原樹每個節點試作候選根節點，再用 Same Tree 比較兩棵樹的值與左右結構。只要有一個候選完全相同就成立；所有候選都失敗才不成立。令原樹與目標樹分別有 n、m 個節點，逐點比較的最壞時間 O(nm)；遞迴堆疊最多 O(h₁+h₂)。

---

## 2026-10-12

- 290. Word Pattern
- 338. Counting Bits
- 4. Median of Two Sorted Arrays
- 392. Is Subsequence
- 310. Minimum Height Trees

**心得**：
- 290：Bijection……第二次遇到，就是做雙向 mapping 或是 used hashmap。但是要注意的東西還有數量，也許可先把兩邊拆解出來，然後再做 1-1 mapping？
- 338：Review 後，有一些 bit 的 trick 可以學：
  1. x % 2 就是看最後一位是不是 1，改成用 x & 1 即可。
  2. x &= x - 1; // zeroing out the least significant nonzero bit
  - 一開始用暴力法 O(nlogn)，這題可以進階到查表，是 CPU 最佳化很常出現的題目。
  - ans[x] = ans[x & (x - 1)] + 1 的定義滿跳脫思考的：原本是按「位數」拆，移除最低位再補回它的值；也可以按「答案的組成」拆，移除一個 1，剩下的答案再加一。先想到「拿掉一個 1 後仍是同一種問題」，再接上 x & (x - 1) 這個操作。
  - 兩種 DP 每個 x 都只查一次表，所以都是 O(n)；不能把暴力法「逐位移除」與「只移除 1」的迴圈次數差異，直接套到 DP 上。

- 4：還是做不出來……經 gpt-6.1-sol 討論後完成，目前還不能獨立推導。
  - 先理解 median 的定義：左側所有元素 <= 右側所有元素；偶數時左右數量相同，奇數時左側多一個。
  1. 維持 leftSize 是目標的數量：leftSize = (m + n + 1) / 2，讓 i + j = leftSize 成為不變量。
  2. Binary search i 應該在的位置；因為左側數量已固定，j = leftSize - i 自然出現，不需要同時搜尋兩個切點。
  3. 拿切點位置的左側最大跟右側最小比較；不合法時，根據哪個跨陣列順序被違反，縮小搜尋範圍。
  - 還有一個要特別設計的是左右側最大／最小值：l1、r1、l2、r2 是值，不是 index；空的左側用最小值、空的右側用最大值當 sentinel。
  - 這題用 string 問題常用的 cut position 去想設計，就很合理：empty 也是一種合法分割，所以設計成 [0, i) 與 [i, m)，i 是 0 ~ m。
  - 分成兩個 subarray，因為這是分段，不是搜尋空間，自然用 [0, i) 來表示更流暢；i 自然就是左段的數量。另用 [lo, hi] 表示候選切點的搜尋空間。
  - 背後設計比特定切點模板更重要：從答案定義拆出條件，先用構造固定數量不變量，再搜尋滿足左右順序條件的解。

- 392：Naive two pointers 已經做出來了。
  - Follow-up 用 hashmap + upper_bound binary search：固定 t，記錄 letter to index 的位置列表；對 s 找一組嚴格遞增的 index。實作使用 vector<vector<int>>(26) 作為字元到位置列表的對照。
  - 好像可以做 DP follow-up：預先建立 next-position table，讓每個 s 查詢只需 O(|s|)；尚待實作。

- 310：Kahn's algorithm like, keep removing degree 1 node until one or two left. 解答把剩下的節點稱作 centroid，但照最小樹高的定義，這裡應是 center。
  - 深入查出處：樹中心與重心是兩個不同目標；LeetCode 解答沿用 centroid 一詞，但最小樹高找的是 center。Jordan 1869 的樹研究、Harary 1969 的剝葉證明都早於此題；Kahn 1962 原論文處理 DAG 拓撲排序。詳見 [310. Minimum Height Trees：樹中心的出處與歷史](../Problem_History/LC_0310_Minimum_Height_Trees.md)。

**LLM 點評**：
model: GPT-6
- 290：程式正確。mapping 保證同一個 pattern 字元對應同一個 word，indexMapping 保證同一個 word 不被不同字元共用；每輪成功後，已處理的兩側前綴維持一對一映射。若用 forward mapping + used set，只在建立新 mapping 時檢查 word 是否已被使用。
  - 數量檢查與 mapping 檢查是兩個條件：迴圈內 i == pattern.length() 擋住 word 過多並防止越界；最後 i == pattern.length() 擋住 word 過少。這兩處註解寫「word 數量必須等於 pattern 長度」更精確。可先 tokenize 再比較數量，也可沿用目前邊讀邊配對，無須另存所有 words。
  - 空字串作為未設定標記安全，因為 ss >> word 不會讀出空 token。先填缺少的 mapping 再檢查也正確，衝突時立即 return false；若要讓 invariant 更好讀，可先驗證既有對應，再建立新對應。令 m = s.size()，一般雜湊分析下時間期望 O(m)、輔助空間 O(m)，stringstream 也保存字串副本；26 個 mapping slot 不代表字串儲存量是 O(1)。見 [Canonicalization：與直接驗證 Mapping 的比較](../Algorithms/Design_Principles/Canonicalization.md#與直接驗證-mapping-的比較)。
- 338：程式正確。bits[i] 定義為 i 的二進位表示中 1 的數量；i / 2 移除最低位，i % 2 補回該位的貢獻。bits[0] = 0，且 i / 2 < i，因此由小到大計算時依賴已完成。時間 O(n)，含回傳陣列的空間 O(n)，不計輸出時額外空間 O(1)，原註解應說清楚計算口徑。
  - 對本題非負整數，遞推可寫成 bits[i] = bits[i >> 1] + (i & 1)。i & (i - 1) 清掉最低位的 1，因此也可推得 bits[i] = bits[i & (i - 1)] + 1；每個 i 只查一次已完成狀態，同樣 O(n)。見 [Bit Manipulation Playbook](../Algorithms/Bit_Manipulation/01-Bit_Manipulation_Playbook.md)。
  - 從逐個數字反覆除以 2 的 O(n log n)，進步到重用較小數字答案的 O(n)，關鍵是子問題重用，並非只把除法換成位元運算。查表還可指預先存好固定寬度區塊（例如 8 bits）的 popcount，再拆塊加總；與目前 bottom-up DP 有關，但不是同一個實作，也不能僅憑改寫成 bit operator 就斷言實際 CPU 執行更快。
  - 可重用的子問題設計：移除一個對答案有固定貢獻的部分，讓剩下的仍是同一種問題。此處 ans[0] = 0；x > 0 時，x & (x - 1) 恰好少一個 1，故 ans[x] = ans[x & (x - 1)] + 1。移除後數值小於 x，保證 bottom-up 查到的狀態已完成。
- 4：最終程式在題目條件下正確，平均值先用 1.0 * 轉成浮點再相加，也避免 int 加法溢位。這次是經討論後完成，尚不代表能獨立推導。關鍵收穫是「答案條件 → 數量不變量 → 消去 j 的自由度 → 搜尋剩餘順序條件」；不是只記住切點的寫法。可連結 [Correct by Construction](../Algorithms/Design_Principles/Correct_by_Construction.md)。
  - [0,i) 與 [i,m) 描述資料分段，i 同時是切點與左段數量；[lo,hi] 描述尚未排除的候選切點。兩者層次不同，不應混用。先搜尋較短陣列，保證 i ∈ [0,m] 時 j ∈ [0,n]；sentinel 統一處理空段。固定 leftSize 是數量 invariant，不是終止條件。
  - l1 > r2 時，i 再增大只會讓 l1 不減、r2 不增，故可排除 i 及其右側；l2 > r1 時，i 再減小只會讓 l2 不減、r1 不增，故可排除 i 及其左側。合法切點始終留在候選範圍內，每次失敗至少排除目前切點，保證進展；兩個交錯都不存在時得到合法分界。時間 O(log(min(m,n)+2))、額外空間 O(1)。
- 392：位置列表 + upper_bound 的單次判斷正確。由左至右建表使每個列表自然有序；lastIndex 是目前 s 前綴可匹配到的最早結尾，upper_bound 找嚴格大於它的最早位置，避免重用同一個 t 元素，也為後續保留最多選擇。空 s 回傳 true；找不到下一個位置即失敗。實作是固定 26 格的直接索引表，不是 hashmap。
  - 令 m = s.size()、n = t.size()，建表 O(n)、索引空間 O(n)，所有列表合計只有 n 個位置；每個字元查詢 O(log(n+1)) 上界，整個 s 查詢 O(m log(n+1))，不是 O(log n)。目前函式每次重建索引，整次呼叫為 O(n + m log(n+1))，仍未實作 follow-up 的跨查詢重用；應把建表移到初始化階段，後續只傳入 s，並以 const string& 避免每次按值複製 t。
- 310：類似 Kahn's algorithm 的消除流程，但維護的是無向樹的 degree，門檻是 1；必須每輪移除完整一層葉節點，讓新葉留到下一輪，直到剩下 1 或 2 個節點。這些是最小化最大距離的樹中心（centers），與最小化最大分支大小的重心（centroids）不同。剝掉一層葉後，對剩餘節點而言最遠距離皆減 1，因此保留中心；n == 1 需直接回傳唯一節點。每個節點與每條邊只處理常數次，時間 O(n)、空間 O(n)。

---

## 2026-10-11

- 347. Top K Frequent Elements
- 1143. Longest Common Subsequence
- 283. Move Zeroes
- 210. Course Schedule II
- 211. Design Add and Search Words Data Structure

**心得**：
- 347：使用 count + sort O(nlogn)，中規中矩。
  - 使用 count + priority queue 可以達到 O(n + dlogk)。
  - 另外一個做法：先觀察到 frequency 一定在 1 到 n 的範圍內，因為就只有 n 個元素。每個數字的頻率一定落在這個範圍的其中一個位置，就可以用 bucket sort，然後 traverse 取 top k，達成 O(n) 時間。超神的做法，先記下來，下次做。

- 1143：Bottom-up dynamic programming 概念都懂，但是發現用「在 i、j 結尾的 LCS」去設計，其實滿難想的，因為初始值變得很醜。使用 m × n 的 dp，先處理 dp[0][0]，再讓第一列、第一欄傳遞先前找到的匹配；時間與空間 O(mn)。

- 283：Bubble sort-like，從右往左找 zero，透過相鄰 swap 移到尾端的下一個位置；two pointers，時間 O(n²)、space O(1)。這個太慢了，想要提示。
  - 一開始腦袋打結，想去 bubble-sort like，一路 swap；重新設計成 [...non-zero, zero...]。Two-pointer technique：前半用 k 維持 non-zero 的下一個位置，i 一路推進找下一個 non-zero，swap(nums[i], nums[k]) 後 k++，用 swap 維持 invariant。非零元素順序穩定；時間 O(n)、space O(1)。

- 210：用 Kahn's algorithm，沒什麼特別的，有學過就會，就是 BFS 的 indegree 變體。

- 211：Trie 跟 DFS 兩個技巧同時考。

**LLM 點評**：
model: GPT-6
- 347：令 d 為 distinct 元素數。計數後排序的是 d 個項目，因此時間更精確為期望 O(n + d log d)，O(n log n) 是有效上界。若用只保留 k 個候選的 min-heap，時間為期望 O(n + d log(k+1))；priority queue 本身不保證此界，要看 heap 大小如何維持。
  - Bucket 方法的關鍵是排序依據「頻率」有界，而非元素值有界。配置 n+1 個桶 O(n)、放入 d 個項目 O(d)，由高頻往下掃描並取滿 k 個，總計期望 O(n)、輔助空間 O(n)。以 unordered_map 計數時，線性時間依賴平均／期望常數時間的雜湊操作；bucket 版本尚待下次實作。


- 1143：提供的程式在兩個字串非空時正確，時間與空間皆 O(mn)。狀態實際是 text1[0..i] 與 text2[0..j] 兩個前綴的 LCS 長度，不要求答案使用 text1[i]、text2[j]；因此「截至 i、j」比「以 i、j 結尾」精確。第一列／欄需要傳遞先前找到的匹配，程式已處理，底下註解則未完整寫出。
  - 改以長度定義 dp[i][j]：text1[0,i) 與 text2[0,j) 的 LCS 長度。配置 (m+1) × (n+1)，讓空前綴自然成為 dp[0][j] = dp[i][0] = 0；從 i、j = 1 開始，比較 text1[i-1] 與 text2[j-1]，沿用相同遞推，答案為 dp[m][n]。這是把 base case 納入狀態空間，並非只為方便多開一列；也可自然處理空字串。

- 283：目前解法正確，逐次相鄰交換保留非零元素的相對順序；最壞 O(n²)，因為同一個非零元素可能被多個零反覆推動。提示：先想最終答案的前綴應該按順序包含哪些元素，再問能否讓每個保留元素直接到下一個應放的位置；目標 O(n) 時間、O(1) 輔助空間，尚待實作。
  - 已完成的線性 swap 版本正確。每輪開始時，[0,k) 是已掃描元素中依原順序排列的所有非零值，[k,i) 全為零，[i,n) 尚未處理。遇到非零值，若 k<i，nums[k] 必為零，交換後非零值接到前綴尾端、零留在已掃描區；若 k==i 則自我交換。故不會交換兩個不同的非零元素，非零順序穩定。i 每輪前進，結束時 [k,n) 全為零；總時間 O(n)、輔助空間 O(1)。k 同時是非零元素數量、下一個寫入位置，以及非零前綴的切點。

- 210：可用 queue-driven BFS 的形式理解，但入隊條件是剩餘 indegree 歸零，表示所有前置依賴已完成，而非首次被發現。indegree 維持的是尚未移除的入邊數；輸出數量等於課程數才得到完整拓撲序，否則剩餘依賴含環。使用 adjacency list 時時間與空間 O(V+E)。見 [Kahn Algorithm](../Algorithms/Topological_Sort/02-Kahn_Algorithm_BFS.md)。

- 211：Trie 保存共享字首，DFS 處理搜尋中的分支：一般字元只沿對應 child，遇到 . 才探索所有存在的 children。搜尋狀態可定義為 (node, i)，表示前 i 個字元已匹配；i 到字尾時仍須檢查 isWord，避免把存在的前綴誤認為完整單字。

---

## 2026-10-10

- 278. First Bad Version
- 6. Zigzag Conversion
- 409. Longest Palindrome
- 733. Flood Fill
- 235. Lowest Common Ancestor of a Binary Search Tree

**心得**：
- 278：就是 Binary Search，滿無聊的，練習 search space 設計。

- 6：硬做……
  1. 先分組出一個 zigzag 區塊。
  2. 用區塊內的 index 再推出是在直線還是斜線。
  3. 用暫存空間收集。
  - 不確定自己有得到什麼，這個算是 simulation 嗎？Simulate Zig-Zag Movement？
  - 加入複習清單：下次做 O(n) 時間、O(1) 額外空間的解法（不計回傳字串）。

- 409：用了很直觀的做法，先計數，每個字元取 count / 2 * 2，有奇數次數就再加一個放中間。
  - 一開始不小心搞錯，寫成單純只取出現偶數次的字元來用；像 "ccc" 也可以拿來用，只是要取偶數個 count / 2 * 2。
  - 一開始 input 要取什麼來做想錯，演算法設計就錯了。
  - 加入複習清單：下次做 one-pass traversal 版本，不再額外遍歷頻率表。
  - One-pass traversal 用 unordered_map 跟 unordered_set 都可以達成，個別想一下為什麼。

- 733：我是用 DFS 完成，程式碼精簡，但是要很小心設計 color 作為 visited 來使用。用 BFS 也可以，想問現在需要練嗎？

- 235：就是標準的 post-ordering / divide and conquer，去做 combine-centric 的解法；但是沒用到 BST 特性。想問需要再用 BST 特性寫一次嗎？
  - 補做利用 BST 特性的遞迴版本：root 跟 p、q 比較，若在同一側就往那側找，剪掉 root 與另一個子樹；若各在一側，root 就是答案。
  - 這比較像 top-down approach，從 root 開始 decrease，而且可以 early return。用 search pruning / decrease and conquer 來想，有機會變直觀。
  - 補做 iterative version，時間 O(height)、space O(1)。太酷了……因為 BST 特性，可以把 divide and conquer 變成 decrease and conquer；相較於 LC 236 的 O(n)，時間優化到 O(height)，space 甚至可以到 O(1)，是一個超酷的 recursion 轉 iterative 題目。

**LLM 點評**：
model: GPT-6
- 278：這題適合驗收 search space 設計：isBadVersion 是單調的 F…F T…T，目標是第一個 T；能說清楚答案為何不會被排除，以及首版／末版就是答案時仍能收斂，就抓到重點。見 [Binary Search 標準模板](../Algorithms/Binary_Search/00-Binary_Search_Standard_Template.md)。

- 6：程式正確，可歸類為 Simulation；更精確是用週期性 index mapping 直接求 row，再依 row 分桶。沒有逐步維護方向，而是把移動規律寫成公式。
  - 可複用的推導是「找週期 → 取餘得到週期內位置 → 分段映射」。r 行的 row 序列為 0,1,…,r-1,r-2,…,1，週期 C = (r-1)+(r-1) = 2r-2；對 t = i % C，下行用 t，上行用 C-t。你的 (r-1)-(t-(r-1)) 正是 C-t。r = 1 的提前回傳也避免了模零。
  - 另一個收穫是只建模輸出需要的資訊：輸出只需按 row 收集，欄位與二維空格不必保存。逐字掃描並 append，保留同 row 字元的原始先後順序。這可連結 [正交性心法](../Meta_Frameworks/Orthogonality-Problem-Solving.md)：分開處理 row 映射與結果收集。
  - 令 n 為字串長度、r 為 numRows，時間與額外空間嚴格說都是 O(n+r)，因為建立並走訪了 r 個 string；在 r <= n 時即 O(n)。若先對 r >= n 回傳 s，可避免配置大量空 row。字串 append 的時間以攤銷分析計。

- 409：提供的程式正確。關鍵區分是「原始頻率必須為偶數」與「選用數量必須能配對」：對稱位置用的是字元對，因此每個頻率 f 都能貢獻 2*floor(f/2)，不論 f 的奇偶；剩下的字元最多選一個當中心。"ccc" 能形成長度 3，但 "cccddd" 更能抓出錯誤模型：兩種奇數頻率都能提供一對，另取一個中心，答案為 5。
  - 這是把合法性條件誤套到原始輸入，而非可選取的結果；可先寫 ANSWER：「所有可用字元對的長度總和，加上至多一個剩餘字元」，再用多個奇數頻率測試。見 [答案定義與假設檢查](../Interview_Playbook/Problem_Solving_Process_and_Assumption_Checklist.md)。
  - 固定 52 種英文字母下，計數與掃描時間 O(n)、計數表額外空間 O(1)。但 string s 按值傳入，若計入從呼叫端複製輸入的成本，該副本另需 O(n) 空間；允許調整簽名時可用 const string& 避免複製。


- 733：改色能兼任 visited 的前提是保留 originalColor，且 newColor != originalColor；兩色相同時先回傳，否則改色無法讓格子退出可走訪集合。每格在展開鄰居前先改色，確保不被重複展開。
  - 現在不必為同一題補寫 BFS，除非 queue traversal 還不熟。能說清楚「入隊時就改色」以避免重複入隊即可；之後用最短路徑／多源擴散題練 BFS，更能體會它的用途。本題 DFS、BFS 都能找出連通區域，最壞時間與輔助空間皆 O(mn)，DFS 的遞迴堆疊也要計入。見 [連通性問題的 DFS 與 BFS](../Algorithms/Traversal_Strategies/DFS_vs_BFS_for_Connectivity.md)。


- 235：提供的通用 Binary Tree LCA 程式正確（題目保證 p、q 存在），時間 O(n)、遞迴空間 O(h)。回傳值是子樹找到的 p／q，或已合成的 LCA；左右都有結果時在當前節點合成，單側有結果則往上傳。遇到 p／q 提前回傳，涵蓋其中一個是另一個祖先的情況；因此是 post-order combine，但不必完整走訪所有後代。註解中「兩側都空再檢查 root」已由開頭 base case 處理。見 [遞迴剪枝與聚合](../Data_Structures/Trees/Recursive_Design_Pattern_Pruning_and_Aggregation.md)。
  - 建議現在再寫一次利用 BST 特性的 iterative 版本：目標 O(h) 時間、O(1) 輔助空間。練習把 BST 順序轉成只搜尋一側的依據，並說明何時當前節點就是 LCA；這是不同於左右搜尋後合成的設計。h 不保證是 log n，退化樹仍可能是 n。
  - 已補做的 BST 遞迴版本正確，分類為 top-down search pruning／decrease and conquer 很貼切：每次只保留一個子問題，回傳時不需 combine。Invariant 是目前子樹仍包含 p、q，因此也包含其 LCA；兩者同側時，LCA 必在該側子樹，各在一側時任何更低的節點都不能同時涵蓋兩者，所以當前 root 就是最低共同祖先。root 等於其中一個目標時，另一個仍在目前子樹內，也可直接回傳。每次下降一層，有限樹高保證終止。
  - 複雜度更精確為時間 O(h)、遞迴輔助空間 O(h)；原註解 O(n) 是退化樹的最壞界。此版尚非 iterative，不能算 O(1) 空間；BST 也不保證每次將搜尋規模減半。
  - 新增的 iterative 版本正確，時間 O(h)、輔助空間 O(1)。兩次優化來源分開看：BST 順序性使搜尋只沿一條路徑；尾遞迴沒有回程工作，才能只更新 root、消除 stack。Decrease and conquer 本身不保證 O(1) 空間。else 註解應是 p、q 分居左右子樹，不必是直接 children。已加入 Essential、Archetype 的「尾遞迴消除：單一路徑搜尋」與 Decrease and Conquer，並完成原 iterative review 項目。

---

## 2026-10-09

- 143. Reorder List
- 142. Linked List Cycle II
- 287. Find the Duplicate Number
- 167. Two Sum II - Input Array Is Sorted
- 189. Rotate Array
- 252. Meeting Rooms
- 268. Missing Number

**心得**：
- 143：這題是 middle to hard，因為結合 list reverse + merge。
  - 主要是卡在 middle 找到之後，因為後半被 reverse，而前半還串在後半的 tail。我一直設計不出一個好的 termination condition。
  - 後來想到之前有做過一個 intersection 的題目，只要他們有交會，最後一定會在同一個位置相遇。以這題為例，後半我用 pointer swap 的技巧（兩個 list 一直交換誰當頭），一定會有一個時間點，兩個人同時指向同一個位置。
  - 所以就用這個當終止條件：兩個人指向同一個位置時。最厲害的是，edge case 都會過，包含單一 node 以及空串列。
  - 一開始還在想辦法把前半鏈結斷掉……但是有好的 termination condition，其實不用斷掉前半。
  - 這個靈感……可遇不可求。
- 142：我不知道怎麼證明，但是我感覺跟找 intersection、交換 traverse 起點的 O(1) space 問題解法的感覺有點像……？
  - 我是想到，找到交匯處時，有什麼狀態可以用？發現有交匯處跟起頭，所以靈感來源是……交匯處的下一個就是起點？proof？
  - 從交匯處跟從頭再等速走一次？
- 287：這題太難了，解法也太多了，一定要重做，加入 review list，而且不同的做法都要試試看。
  - 超級難……難到不可思議……完全靠解答跟 gpt-6.1-sol 提示的。
  - 下次要做看看 Array as HashMap (Recursion) 與 Array as HashMap (Iterative)，space 分別是 O(n) 與 O(1)，也是短到不可思議；但我現在還不知道要做什麼，先記錄一下，下次先提示，再重做看看。
  - 1. 要先參考 LeetCode 142，先找到 intersect point。
    2. Two pointers：一個從頭，一個從 intersect point，等速走。
    3. 遇到的第一個 index 就是重複的 value。
  - 關鍵想法：**入口的 index 本身就是重複值**，因為有不同的 index，其 `nums[index]` 都指向它。
  - 就很像是 cycle detection 入口處，有「兩個人都指向它」的這個特性來設計出來的。
  - 關鍵設計：
    1. 先理解鴿籠原理，所以可以在 index [1, n] 裡面盡情地 traverse。
    2. 用「cycle 入口有不同來源 index 指向它」的觀察來找到重複值（同 LeetCode 142 的 cycle entry point 解法）。
    3. 把 duplicate 問題類比到 cycle entry point 問題。
  - Pitfall 1：開頭要讓 slow 跟 fast 同一個起點，這樣走過的量跟交會的點在後面做 cycle entry point 才有意義。
  - Pitfall 2：找到 cycle entry point 後，它的 index 就是我們發現的 duplicate 值，不用再去取那個位置對應的值（`nums[nums[slow]]` 這是多餘的）。可以想像，那個位置被走過兩次的概念，所以是重複值。

- 189：這題意外地難，reverse 基本上解法不可能想得出來。
  - 如果要暴力法，是 O(k * n)，但是為什麼是 k 要設計，暴力法值得再做一次。
  - 如果是先反轉整條，那就可以拆成 [0, k)、[k, n) 兩串再反轉（如果一開始就跳進去先反轉前半跟後半，這樣會遇到偶數長度時出錯，但是我不知道為什麼）。
  - 如果是用額外空間，則在拿值時，不要用 i - k % n 去做，一來減法會讓值 overflow，跟 % 運算也不友善。
  - 應該還是要用 i + k % n 位置，拿 i 值去填才不會錯，也不用處理 k 遠大於 n 的情況。

- 252：用 sort，依 start time 排序，比較目前的 start time 跟前一個 end time。好像沒什麼特別的，是不是可以做到 O(n)？是的話只給目標，不說作法。

- 268：做了 hashmap 跟加總找遺失數字的版本。
  - Bit manipulation 版本直接看解答無感、不直觀，加入複習清單，下次重做。

**LLM 點評**：
model: GPT-6
- 143：提供的程式正確，時間 O(n)、額外空間 O(1)，不需要先斷開前半。抓到共享節點可以作為 merge 的終止訊號，是把鏈結結構轉成控制條件。不過「有交會就一定會同時相遇」本身不夠：Intersection 題的換頭走訪靠路程對齊保證相遇，這題則靠兩段長度關係與交替消耗節點，不能直接套用同一個證明。
  - 令 m 為 reverse 前的中點。反轉後兩段只共享尾節點 m，且 m->next 為 nullptr。每輪 ptr1 是已接好前綴的最後一個節點，也是其中一段剩餘鏈的頭；ptr2 是下一個要接的另一段頭。先保存 ptr1->next、接上 ptr2，再交換角色，相當於消耗第一段的一個非共享節點。
  - 用 a、b 表示兩個指標距 m 的邊數，初始 a == b 或 a == b + 1；每輪變成 (b, a - 1)，仍維持同一關係，且 a + b 減一。因此 ptr1 != ptr2 時 ptr1 尚未到 m、可以安全讀取 next；最後必在 m 相遇。相遇即停，不會寫出 m->next = m，尾端保持 nullptr。空串列時 reverse(nullptr) 安全且兩指標皆為 nullptr；單節點時兩指標一開始就相同，皆跳過 merge。
  - 可把靈感整理成可重複推導的步驟：定義每輪兩個指標代表的未處理部分、確認共享節點與 next 的狀態，再證明每輪消耗未處理節點且不會越過相遇狀態；停止時檢查每個原節點恰好出現一次、尾端為 nullptr。空串列與單節點能否安全通過，也包含找中點和 reverse 階段，不能只看 merge 的終止條件。見 [相鄰指針：終止條件須配合循環操作](../Algorithms/Two_Pointers/04_Adjacent_Pointers.md)。
- 142：提供的程式正確。與 Intersection 換頭解法的共同心法是「利用路程關係對齊指標」；Intersection 靠交換路徑補齊長度差，本題靠 1:2 速度造成的模環長關係。相遇點的下一個不一定是環入口。
  - 令 a 為 head 到環入口的距離、L 為環長、b 為入口沿 next 到相遇點的距離。相遇時 slow 已走 t 步、fast 已走 2t 步；兩者位置相同，因此路程差 t 是 L 的整數倍。又 t ≡ a + b (mod L)，所以 a + b ≡ 0 (mod L)。從相遇點再走 a 步便回到入口，同時從 head 走 a 步也到入口；前 a 步 head 尚在環外，因此兩者首次相遇就在入口。a = 0 時兩者已在入口，第二段直接跳過。
  - 無環時 fast 或 fast->next 為 nullptr，直接回傳；空串列、單節點無環與單節點自環皆能處理。時間 O(a + L)、額外空間 O(1)；「two passes」宜說成兩階段，因為環內可能繞行，不是字面上的完整走訪兩次。見 [快慢指針](../Algorithms/Two_Pointers/02_Fast_and_Slow_Pointers.md)。
- 287：最後提供的版本正確，時間 O(n)、額外空間 O(1)，且不修改陣列。核心建模是 index 為節點、nums[index] 為 next。從完整路徑 0 出發，0 沒有入邊，必在環外；入口有環外與環內兩個不同前驅，因此入口編號是重複值。即使實作從 nums[0] 出發，也會找到同一入口。見 [快慢指針](../Algorithms/Two_Pointers/02_Fast_and_Slow_Pointers.md)。
  - Pitfall 1 更精確是兩階段使用同一個概念起點。兩指標同值初始化搭配 do-while 很清楚；slow = nums[0]、fast = nums[nums[0]] 也可以代表從 index 0 已先走一輪，第二階段就應重設到 0，不是要求初始化變數一定相等。
  - Pitfall 2：停止時回傳 slow；連 nums[slow] 都是再往下一個節點，更不用說 nums[nums[slow]]。理由是不同來源 index 指向同一入口，不是「同一位置被走過兩次」；繞環會反覆走過所有環節點，不能用重訪次數區分答案。已加入複習清單，安排重寫 Floyd 並嘗試其他做法、比較各自是否符合限制。
  - 關鍵設計可再分清三層：值域 [1, n] 保證每次 next = nums[index] 都落在合法 index；有限節點上持續沿固定 next 走，依鴿籠原理必重訪並形成環；從無入邊的 0 出發，入口有兩個不同前驅，才把「找重複值」轉成「找環入口」。鴿籠原理保證重複／重訪，走訪不越界則來自值域限制。
- 189：暴力法可以定義為每輪右移一格（先保存尾元素，再由右往左搬移，最後放回開頭），做 k 輪，因此時間 O(kn)、額外空間 O(1)；先令 k %= n，則實際是 O(n * (k mod n)) 的搬移工作，最壞 O(n²)。n 須非零才能取餘，k = 0 時不必搬移。已加入複習清單重做此版本。
  - Reverse 可從區塊交換推導：原陣列 A|B，其中 B 是最後 k 個元素，目標 B|A。整條反轉得到 reverse(B)|reverse(A)，在 k 切開各自反轉即可。先反轉兩段再反轉整條也正確，但原陣列要切在 n-k：reverse(A)|reverse(B) → B|A。若先切在 k，通常會變成左轉 k；不是奇偶長度造成，未看到程式碼不能判定實際錯誤。
  - 額外陣列版本用 out[(i + k) % n] = nums[i] 最直觀；括號必須包住 i + k，因為 i + k % n 等於 i + (k % n)。先 k %= n 可處理多餘圈數並縮小加法範圍，但一般整數範圍仍須注意。反向取值也可用 out[i] = nums[(i - k + n) % n]（k 已正規化、使用足夠寬的 signed 型別）。i-k 為負不等於 signed overflow，C++ 負數取餘可能仍為負，unsigned 減法則可能 wrap around；因此正向安排目的地較容易避免這些陷阱。

- 252：提供的程式正確。依 start 排序後，只要相鄰區間都不重疊，就能串起 end[i-1] <= start[i] < end[i]，因此不必兩兩比較；start == 前一個 end 可接續開會，使用 < 正確。屬於排序後線性掃描。
  - 時間 O(n log n)；掃描本身額外空間 O(1)，但常見 C++ std::sort 實作有 O(log n) 的 stack，整體額外空間通常記 O(log n)。
  - 一般未排序、只靠端點比較的模型，最壞需要 Ω(n log n)，目前已達該模型的最佳漸近時間。若額外利用有界整數時間範圍等條件，才可能追求線性時間；目標可設為 O(n + U)（U 為時間值域大小），僅在 U = O(n) 時可寫成 O(n)，此處不透露作法。見 [Interval 問題解題心法](../Algorithms/Greedy/Interval_Problem_Solving_Playbook.md)。

---

## 2026-10-07

- 876. Middle of the Linked List

**心得**：

---

## 2026-10-06

- 228. Summary Ranges
- 232. Implement Queue using Stacks
- 234. Palindrome Linked List

**心得**：
- 232：把兩個 stack invariant 想清楚就很好解了
  - 目前版本的 peek 是攤銷 O(1)；下次要做出單次最壞 O(1) 的 peek。
- 234：用遞迴 + 外部狀態，只要想到外部狀態，就可以在遞迴回來時，開始比較。
  - 至於 space O(1) 解法要想到可以破壞 input 的 reverse。

**LLM 點評**：
model: GPT-6
- 232：用 invariant 定義兩個 stack 的角色，確實能直接推導操作規則。以延遲搬移的版本為例：out 從頂到底是較早入隊、接下來要取出的元素；in 從底到頂是較晚入隊、尚未搬移的元素。整個 queue 的 FIFO 順序就是這兩段串接，因此只有 out 為空時，才能把 in 全部搬到 out，否則會讓新元素插到舊元素前面。每個元素最多搬移一次，所以 push、pop、peek 的攤銷時間皆為 O(1)，但觸發搬移的單次 pop／peek 最壞為 O(n)。
  - 提供的程式符合上述 invariant，peek 觸發搬移，因此 peek 與 pop 都是攤銷 O(1)。若要讓 peek 單次最壞也 O(1)，可在 pushStack 為空時的 push 快取其底部元素 front；peek 優先讀 popStack.top()，popStack 為空才讀 front，搬移則改由 pop 觸發。front 只在 pushStack 非空時有效，不需要隨 pop 更新。
- 234：兩個版本都正確。遞迴返回時 ptr 由尾向頭，外部 head 由頭向尾，每次比較一組鏡像位置；每成功比較一次才推進 head。時間 O(n)，call stack 深度 O(n)，所以空間 O(n)；此版會比較全部 n 組，包含重複的鏡像配對，但不影響正確性或複雜度。
  - 第二版從 index floor(n/2) 開始反轉，偶數長度比較後半，奇數長度包含中點、最後讓中點與自己比較，因此不必另外跳過中點。多次線性走訪的總時間仍為 O(n)，iterative reverse 只用固定數量指標，額外空間 O(1)。
  - compare 的指標按值傳入，不會改掉呼叫端保存的 ptr；即使比較失敗，也先保存 ret 再 reverse(ptr)，確保還原。前半段原本連到反轉區起點的 next 未被修改，第二次反轉會恢復整條鏈，不需要額外接回。心得可精確表達為「暫時重接 input 的指標，利用原節點完成反向走訪，再還原」。先算長度找中點已符合要求，快慢指標只是省掉一次完整的長度走訪。

---

## 2026-10-05

- 160. Intersection of Two Linked Lists
- 205. Isomorphic Strings
- 219. Contains Duplicate II
- 152. Maximum Product Subarray

**心得**：
- 205：這題沒有想像中簡單，已經做第二次了，都是漏 mapping 的項目不能重複的問題。
  - 而且幾乎都是用兩個 cache 的解法（一個放 mapping，一個放重複）。感覺有更簡單的、乾淨的做法才對。
  - 核心是設計「1–1 mapping」的實作：用 forward + reverse mapping，兩個方向各自記錄對應關係；已做出雙向 map 的版本。
  - 另一個思路是設計 mapping function，把兩個 input 各自轉到共同的值域，再比較轉換後的結果；這就是 canonicalization，repo 裡也有討論。
- 219：做了暴力法、hashmap。看了解答發現 hashmap 時間 O(n)，空間是 O(n)。有需要做看看 sliding window 版本嗎？
- 152：想超久……超超級久，有靈感，但是 invariant 一直寫不出來，寫出後就解了。
  - 關鍵設計：
    1. 要查兩個表：維護最大值來找最大，and 維護最小值來找最小。
    2. Kadane's Algorithm：當前更好的話，reset 值。
  - 比較單純的思路，是先解決最大值的 Kadane's invariant，然後因為負數出現兩次有機會變更大的值，所以要 maintain 一個最小值。
  - 很容易優化成 O(1) space。
  - 下次要重新講一次暴力法的做法跟時間。

**LLM 點評**：
model: GPT-6
- 205：Invariant 是已處理的字元配對維持一對一映射：同一來源不能映到不同目標，不同來源也不能共用目標。單向 mapping 允許多對一，例如 ab → aa；mapping + used set 分別維持來源對應一致、目標不被其他來源占用。提供的 forward + reverse map 程式正確，先檢查雙向衝突，再同時建立對應，兩份狀態與判斷對稱，適合作為通用 1–1 mapping 的基本實作。時間平均 O(n)，空間 O(k)，k 為不同字元數；固定字元集下可視為 O(1)。
  - Last-seen 是另一種驗證方式，不是 mapping + used set：兩側各記錄上次出現位置，每步比較目前兩字元是否曾在同一位置一起出現，再更新為 i + 1（0 表示未出現）。它間接檢查出現模式的一致性，不是檢查「這次與上次位置不同」，也不是實作一對一映射的必要步驟。
  - Canonicalization 則先把兩個輸入各自轉成共同標準形式，再比較。例如 paper 與 title 都依首次出現順序編成 0,1,0,2,3。每個輸入內的字元到編號是一對一，但整個字串的正規化不是一對一：等價字串刻意得到相同結果。雙向 mapping 直接驗證兩個輸入間的對應；正規化則保留重複模式、消去字元名稱。見 [Canonicalization：用於分組／判等](../Algorithms/Design_Principles/Canonicalization.md)。
- 219：若 hashmap 保存每個值最近一次出現的位置，時間平均 O(n)，空間最壞 O(n)；最近位置已足以判斷，因為它與目前 index 的距離最小。建議再做 sliding window，練習把「距離 <= k」轉成有效候選範圍：檢查 nums[i] 前，set 只保存 nums[max(0, i-k):i) 的值。只保留仍可能配對的最近 k 個元素，時間仍平均 O(n)，k >= 1 時空間 O(min(n,k))；k = 0 可直接判定 false。重點是過期資料何時移除，以及距離恰為 k 時仍須納入檢查；見 [Sliding Window 標準模板](../Algorithms/Sliding_Window/00-Sliding_Window_Standard_Template.md)。
- 152：關鍵 invariant 要加上「恰好以 i 結尾、非空且連續」：maxEnd 是這些子陣列的最大乘積，minEnd 是最小乘積；整體答案則是所有已處理 maxEnd 的最大值。兩個狀態互相依賴，不是各自獨立跑最大／最小 Kadane：令 x = nums[i]，兩者都從 x、x × prevMax、x × prevMin 中分別取最大／最小，負數乘法會反轉大小順序。Reset 的意思是選單獨的 x，而不是延伸上一段；0 也由相同候選自然處理。轉移只依賴上一輪的兩個極值，因此時間 O(n)，可用 rolling states 將額外空間降至 O(1)；更新前須保留舊值，避免第二個狀態讀到本輪已更新的值。見 [Kadane's Algorithm](../Algorithms/Dynamic_Programming/Advanced_Techniques/Kadane_Algorithm.md)。

---

## 2026-10-04

- 95. Unique Binary Search Trees II
- 118. Pascal's Triangle

**心得**：
- 95：這題的關鍵其實就是標準的 brute force backtracking，只要 recursive 可以設計出來就沒問題。
  - 關鍵是找到決定性的切點。這之前在某一篇有提到（但我現在忘記在哪一篇提到決定性的切點了），只要這個切點定好之後，自然就可以把遞迴式做出唯一解，然後遞迴進去就出來了。
  - 這題比較 confusing 的部分是那些 pointer 可不可以被 reuse。後來我做了 cache 的版本，reuse 是 work 的，所以應該是可以被 reuse。
  - 再來是因為這題的 backtracking 裡面很明顯有重複子問題，所以很自然就可以延伸到 dynamic programming，用 cache 的方式去記錄已經完成的項目。但不知道為什麼，cache 的版本執行時間反而變長了。
- 118：用定義，dynamic programming，好像沒什麼特別的。

**LLM 點評**：
model: GPT-6
- 95：你想到的是 [Canonical Anchor Decomposition](../Algorithms/Divide_and_Conquer/08_Canonical_Anchor_Decomposition.md)：每棵 BST 的 root 是唯一可讀出的錨點，固定 root 後，左右值域也確定。唯一的是每棵結果的分解，不是固定切點後只有一個解；左右各自仍可有多種樹，需組合所有配對。若遞迴回傳區間內的所有樹，再組合左右結果，更精確是枚舉式 divide and conquer，不必有共享 path 的 choose / undo。以值域區間作為狀態，保存重複區間的結果就是 memoization（top-down DP）。
  - Pointer reuse 代表不同結果可能共享同一棵 subtree；只讀、不修改共享節點時，邏輯樹形仍可正確。若要求各結果可獨立修改或釋放，就需複製或明確管理共享所有權，不能只由測試通過推論節點彼此獨立。
  - Cache 減少重複子問題計算，但仍要列舉與組合輸出。查表、容器配置、結果複製等成本可能抵銷收益，單次執行時間也有波動；未看到兩個版本程式碼，不能判定這次變慢的原因。比較時可先統計區間實際計算次數、cache hit，以及 vector 是否按值複製，再做多次同條件測量。
- 118：直接依定義逐列建構就是 bottom-up DP：兩側為 1，內部元素等於上一列相鄰兩項之和；計算順序自然符合依賴關係。

---

## 2026-10-03

- 88. Merge Sorted Array
- 94. Binary Tree Inorder Traversal
- 112. Path Sum
- 148. Sort List

**心得**：
- 88：設計出 invariant: `[... sorted, unsorted...]` + 3 pointers 就差不多了。

- 94：把 stack 跟 root 的角色確認清楚，演算法就出來了。
  - loop invariant:
    - stack: visited but not processed
    - root: next to visit
    - termination: stack empty and root is nullptr

- 148：異常的硬，bottom-up divide and conquer 難，list 的狀態管理難。
  - 一開始看到這一題的直覺，暴力法就是 selection sort，它的時間是 O(n²)。那如果要讓時間降到 O(n log n) 的話（這是 comparison-based sort 的 BCR），就可以用 divide and conquer 來做。
  - Divide and conquer 有 merge sort 或者是 quick sort。因為題目有問能不能做到 space 是 O(1)，所以我直覺就是 bottom-up 的 divide and conquer。
  - 方向正確之後，其實程式碼是非常非常難寫的。最終切入的點是要能夠先把長度算出來，然後要把欲比較的片段先 split 出來，讓它結尾先清空、指向空指標，才有辦法寫出比較漂亮的 while 迴圈。
  - 然後再做 interval 的設計，初值是 1，用 1 當作 interval 的初始值。但是因為每一段的段落要能夠正確，要去比較總長度，這邊也是另外一個坑。起手勢看起來就是：`interval = 1; until interval >= n`；所以判斷式 `interval < n`。
  - 再來就是每一段做完之後要存哪一些指標，讓它更新到 sorted 的 list，以及下一段要怎麼起頭。這些都是裡面 merge / combine 相關的部分，也是 divide and "conquer" 最難的部分。

**LLM 點評**：
model: GPT-6
- 88：先定義完成區與未處理區，再讓三個指標分別代表兩個來源和寫入位置，這個設計方向成立。若採用從尾端往前填的原地合併，區段應寫成 `[未處理區 | 已完成的 sorted suffix]`；兩個來源剩餘部分本來也各自有序，所以「未處理」比「unsorted」精確。Invariant 不只是 suffix 有序，而是它已放好合併結果中最大的那批元素；每次取兩個來源尾端的較大值，填入下一個寫入位置，並維持不覆蓋尚未讀取的 nums1 元素。

- 94：先定義 stack 與 root 的角色，再推導操作，是用 invariant 引導設計。這裡 visited 建議明確指「已遇到並入棧」，processed 指「已輸出」，避免與 traversal 常用的 visit = 處理／輸出混淆。Stack 保存已遇到但尚未輸出的節點與返回順序；root 指向下一棵要探索的子樹，非空時先往左探索，不一定是下一個要輸出的節點。當 root 為 nullptr 且 stack 非空，stack top 的左子樹已處理完，才可輸出它並轉往右子樹；不是所有 stack 節點都已完成左子樹。stack empty 且 root 為 nullptr 是停止條件；完整 correctness invariant 還應包含 ans 始終是整棵樹 inorder 序列的正確前綴。見 [Current Pointer 實作模式](../Data_Structures/Trees/Iterative_Traversal/03-Current_Pointer_Implementations.md)。

- 148：這次的關鍵是用 split 把區段邊界轉成 nullptr，讓 merge 只處理兩條獨立的有序 list，並回傳 head / tail；外層負責接回結果及保存下一段起點。最終程式的 length / interval 表示「單段長度」，合併後最多是 2 × interval；外層 invariant 是每輪開始時，各段各自有序，除最後一段外長度皆為 interval。內層已完成前綴由合併後的有序段組成，並非整個前綴已全域有序；curr 是其尾端，head 是尚未處理的區段起點。interval < n 才能處理不滿兩個完整段的最後一輪。單次 split / merge 是 O(interval)，整輪合計 O(n)，共 O(log n) 輪；沒有遞迴堆疊，額外空間 O(1)。O(n log n) 是一般比較排序的最壞情況下界，但不限定必須用 divide and conquer，quick sort 也不保證最壞 O(n log n)。按 divide / conquer / combine 的標準分工，你卡住的接回與合併主要是 combine。見 [Loop Invariant](../Proof_Techniques/Loop_Invariant.md)。

---

## 2026-10-02

- 131. Palindrome Partitioning
- 69. Sqrt(x)

**心得**：
- 131：做不出來，想了兩天。第二天用 backtracking 方向對了，可是實作不出來，很慘。問題不是在切法，在於紀錄方式。
  - [ Time taken: 50m 24s ]
  - 這題太驚人了……想了兩天，還想去 Catalan Number，什麼從中間找每個切點，然後用 Divide and Conquer。
    ```text
    a a b
    "" aab
    a ab
    aa b
    aab ""
    ```
    結果發現會有重複計算……
  - 最後跟 GPT-6.1-sol 討論，只要從 string 來想，其實就是超級經典 backtracking，而且它的結構跟 string permutation 超級像。
  - 設計邏輯：backtracking，從當下這個點去看後面的 search space，找 candidate 來，然後 save / restore。
  - invariant：`[chosen, non-chosen]`；`solution` 會 maintain 有哪些完成的 palindrome；promising 用 palindrome 設計。
  - 它甚至還有 dynamic programming 的優化……窩滴媽啊。
  - 然後遇到 string 問題，我發現現在都會跳進去用 character 當 state 在操作。其實做了不少，有些問題把 string 當 primitive type 好像比較好想？
  - 這題一定要再重做一次。
- 69：這類 easy 題目其實超多延伸的，而且很多時候跟 primitive type 操作很有關係。像這次寫，有一個 `k * k < x` 的運算，我用 integer 去乘法，就 overflow 了。
  - 我是先把 linear search 做出來，想知道有沒有需要再做 binary search 版本。
  - Binary search 版本一開始就搞錯 invariant，或是說 movement 條件：想成找第一個平方 >= x，又把回傳選錯成 i，整個大混亂。後來釐清是找第一個平方 > x，再減一。
  - 這應該是最基本最基本的 search on value，很重要。
  - 這題 follow-up 有點多，感覺很棒，之後再刷。

**LLM 點評**：
model: GPT-6
- 131：使用者指出卡在紀錄方式。實際程式同時保留「逐字合併／另開一段」和「枚舉下一段結尾」兩種決策方式，導致共享的字串 path 與段落列表 solution 難以一起還原。既然 for 已枚舉整段，就讓候選字串是 local variable，solution 保存已選段落；加入候選、遞迴、pop_back，修改與還原一一對應。另有兩個具體錯誤：遞迴仍傳 start，沒有前進；非回文時反而加入 solution。完整解用 ans.push_back(solution) 複製保存，這行本身正確。
  - 完成後的關鍵觀察是「選擇的單位」：本題每次選一整段 substring，遞迴狀態仍可用 start index 表示剩餘後綴，不必逐字維護未完成段落。精確 invariant 是 solution 串接後恰好等於 `s[0:start)`，且每段都是回文；剩餘區是 `s[start:n)`。與 permutation 共用 choose / recurse / unchoose 骨架，但本題依原順序切段，不重排字元。可對照 [State and Solution Design](../Algorithms/Backtracking/04-State_and_Solution_Design.md)。
  - DP 優化可預先計算各區間是否為回文，讓候選檢查變成 O(1)；列舉所有分割的 backtracking 仍保留，最壞輸出規模仍是指數級。
- 69：這次的重點是中間運算的型別與值域：兩個 int 相乘仍以 int 計算，即使最後存進 long long，也可能在賦值前就發生 signed overflow（undefined behavior）。要在乘法前提升型別，例如 `1LL * k * k` 或 `static_cast<long long>(k) * k`；`static_cast<long long>(k * k)` 則太晚。32-bit signed int 的 `46341 * 46341` 已超出上限，候選值的平方可能超界，即使 x 與最後答案都放得進 int。見 [整數溢位防範心法](../CPP_Reference/Type/Integer_Overflow_Prevention.md)。
  - 建議再做 binary search，練習從已完成的基準解推導優化。若 linear search 從 0 逐一試到平方超過 x，時間為 O(√x)；BUD 的瓶頸是候選值逐一檢查，`k² <= x` 在非負候選區間呈現 true → false 的單調性，因而能二分尋找最後一個可行值，把搜尋降到 O(log x)（x ≥ 2），額外空間 O(1)。目標是 floor sqrt(x)，判定要包含等號並防止平方溢位；完成後用 x = 0、1、完全平方數、相鄰非平方數與 int 上限 dry run。見 [答案空間上的二分搜尋](../Algorithms/Binary_Search/Answer_Space/01-Answer_Space_Modeling.md)。
  - 提供的 binary search 版本正確，是 search on value 的基本題：候選數值本身有序，predicate `ok(k) = k² > x` 為 false → true。找第一個 true，再減一得到 floor sqrt；若改成 >=，完全平方數會被錯誤減一。Invariant：`[1, i)` 的平方都 <= x，`[j, x]` 的平方都 > x；未判定候選是 `[i, j)`，邊界答案在 `[i, j]`。x > 1 時 x² > x，因此 j = x 可作已知 true 的右界，不必設 x + 1；x = 0、1 由開頭處理。迴圈结束時 i == j，回傳 i - 1 或 j - 1 都正確，差別在 predicate 與答案轉換，不在變數名稱。口訣：定 predicate → 定空間 → 定移動 → 定回傳。見 [Binary Search 標準模板](../Algorithms/Binary_Search/00-Binary_Search_Standard_Template.md)。

---

## 2026-10-01

- 28. Find the Index of the First Occurrence in a String
- 58. Length of Last Word
- 134. Gas Station

**心得**：
- 28：這題可延伸的太多了，必再做，必再做，再做!!
- 134：這題要觀察的東西太多了，要先想出所有 cost diff / remaining，然後要去判斷 reset 的位置，又有點像 Kadane's algorithm...這題幾乎是 brain teaser 等級。

**LLM 點評**：
model: GPT-6
- 134：令每站變化量為 `gas[i] - cost[i]`。若掃描到 `j` 時累積油量首次變負，下一個候選起點是 `j + 1`，並將局部累積歸零；全程總和小於 0 則無解，否則最後留下的候選起點可走完全程。它和 Kadane 一樣有累積失敗後重設的形式，但保留候選起點的理由來自路段可排除性。

---

## 2026-09-30

- 26. Remove Duplicates from Sorted Array
- 27. Remove Element
- 130. Surrounded Regions

**心得**：
- 26：寫了兩個版本：
  1. 從 0 開始 check，current 跟 next 比較；如果不同，就更新進 `k`（next position to write）。因為往後看，要注意 `n - 1` 的位置。
  2. 從 1 開始 check，current 跟 previous 比較，設計方式同 1。不用注意 `n - 1`，因為比較位置都合法；但我先處理了 `n == 1` 的 base case。
- 27：第一個做法用 two pointers，設計成 `[...checked, not checked...]`，需要掃完 array。另一個做法類似荷蘭國旗問題，設計成 `[...keep, ..., discard...]`，把不要的往後丟；當 `keep > discard` 就停止。
- 130：這題重點是 graph 問題的判斷跟轉化：從邊界點出發，標記可達的點，最後整體調整一次 board。本來一直想邊 visit 邊調整內容，如果可達就還原，但程式碼和邏輯都變得超難 maintain；改成先標記邊界可達的人，最後再清理標記符號，整個解法就簡單很多。

**LLM 點評**：
model: GPT-6
- 26：兩版的差異是比較方向決定邊界落在哪裡。第二版若設 `k = 1`、`i = 1`，迴圈只在 `i < n` 時讀 `nums[i]` 和 `nums[i-1]`，`n == 1` 會直接回傳 1，不必另設 base case；若實作會在迴圈前讀 `nums[1]`，才需要先 guard。
- 27：第二版可把三段明確寫成 `[keep | unchecked | discard]`；從右邊換來的值尚未檢查，所以換完後左指標不能前進。它能在未檢查區清空時停止，但最壞時間仍是 O(n)。
- 130：關鍵轉換是先找「不會被包圍」的邊界可達區；標記與改寫分成兩趟後，不必在搜尋途中猜測整個連通塊是否要還原。既有心法見 `Algorithms/Design_Principles/Transformation_Patterns/Destination_as_Source_Reachability.md`。

---

## 2026-09-29

- 9. Palindrome Number
- 13. Roman to Integer
- 14. Longest Common Prefix
- 114. Flatten Binary Tree to Linked List

**心得**：
- 9：其實這題滿有面試性的，因為可以做滿多最佳化概念的。然後已經遇到第二次 `std::pow` 是浮點數、`%` 只能吃整數導致編譯不過的問題。
- 13：follow-up：之後練習從右到左解析。
- 14：其實覺得沒有很好寫。看了答案，這題最一開始沒這麼複雜，只是考 string 操作；我用 pointer / state 設計方式非常 overkill。延伸可以做 divide and conquer、binary search、Trie 等等。
  - 設計上最有趣的觀察：比較時，第一個人／初值很難設計，因為 `compare(x, y)` 本來就是二元運算子，要先決定一個 operand。當沒有假設時，第一個 string 在某個位置可能已經沒有字元。觀察到 common prefix 不可能比 `strs[0]` 長後，就能直接拿 `strs[0]` 當初值，實作會變簡單；vertical scan 只要顧好比較初值，也可以很精簡。
- 114：這題超好玩：tree + divide and conquer + linked list，conquer 部分不容易設計。真正的 O(1) extra space 用的是 iterative；in-place 滿難的＠＠。關鍵是先想到遞迴／子問題，再正確設計回傳值；最難的是回傳值和如何 conquer。這就是 divide and conquer 等級的題目。
  - 看到一個有趣解法：先 visit right，再 visit left，最後用一個 head 串接訪問過的 node。
  - Code review：`leftLast->right = root->right`、`root->right = root->left`、`root->left = nullptr` 可以合併在一個判斷式裡，因為子問題有回傳 Node 就代表子問題非空。
  - 這題一定要再做一次，超好玩！
  - 下次目標：自己做出 time O(n)、extra space O(1) 的 iterative 作法。

**LLM 點評**：
model: Opus 5.5
- 9（`pow` 踩第二次，根治法是不用它）：`std::pow` 永遠回傳 `double`，就算參數都是 `int`；`%` 只吃整數型別，所以編譯錯誤。硬要用的話得 `(long long)std::pow(10, k)`，但浮點誤差可能讓 `pow(10, k)` 變成 `99.999…` 截成 99。整數次方直接用迴圈 `p *= 10` 累乘。這題最佳解（反轉後半：`while (x > rev) { rev = rev * 10 + x % 10; x /= 10; }`，最後比 `x == rev || x == rev / 10`；前提是先排除負數和 `x % 10 == 0 && x != 0`）本來就不需要算位數或次方，也順便避開 overflow。`CPP_Reference/Type/Floating_Point_and_Scientific_Notation.md` 目前只寫到 `ceil` 回傳浮點數，已補上第 3 節 `pow` + `%` 這個坑。
model: GPT-6
- 14：以 `strs[0]` 為候選前綴的觀察是對的；如果它是空字串，答案也必定是空字串。Vertical scan 可以直接用它的字元當比較基準，每次讀其他字串前先檢查長度，就不需要 `'-'` sentinel 或額外的 `common` 狀態。時間 O(字串數 × 最短字串長度)，額外空間 O(1)（不含輸出字串）。
- 114：若 helper 對非空左子樹必定回傳尾節點，`leftLast != nullptr` 就足以 guard 那三行串接，這個簡化成立。先右後左、用 head 串接是反向 preorder；若透過遞迴實作，head 指標雖然只佔 O(1)，呼叫堆疊仍需 O(h) 空間。真正 O(1) 額外空間要看迭代版。

---

## 2026-09-28

- 704. Binary Search
- 75. Sort Colors
- 97. Interleaving String

**心得**：
- 75：
  - 腦袋當機了，在想 [sorted, unsorted]，結果直接用 insertion + swap 直接炸掉……
  - 後來想到 [sorted, unsorted]，要 in-place，那其實是在 unsorted 內找 minimum，那就是 selection；否則整個 unsorted 要 reallocation（input 是 array，除非用 linked list）。
  - 這個就是 insertion sort，沒有 select one then swap in 的概念，就是找到某個位置，然後其他人不能動，要把選的人 "insert"。以 array 的例子，除非額外開空間，否則要大量 reallocation，所以常見就是沒辦法 in-place。理解正確嗎？
  - 第二次做：荷蘭國旗問題的標準解法，要使用到 input 的特性：只有 0, 1, 2。invariant：[sorted 0, unsorted, sorted 2]，`[0...left)` 是 0，`(right...n-1]` 是 2；`left` 是下一個放 0 的位置，`right` 是下一個放 2 的位置。
  - movement：`nums[i] == 0` 跟 `left` swap，`left++`、`i++`；`== 1` 什麼都不做，`i++`；`== 2` 跟 `right` swap，`right--`，`i` 不動。
  - search space 是 `i <= right`：每一格都要檢查，`i == right` 那格也可能沒放對（例如 `[1, 0]`）。time O(n)，space O(1)。
- 97：
  - Top-Down Dynamic Programming。標準可以從 dfs / backtracking / brute force 一路走到 cache 的題目，其實不好寫。尤其是這種字串類的，我好像常常搞不清楚何時是 index、何時設計 length。
  - 像這一次 cache，其實它是有一點像 lens 的概念來做，但是 traverse 的時候是用 index 去往下遞增的。兩個混在一起之後，我反而會讓 index 跟 lens 有點搞混。然後它的 base case 是 index 越界嗎？還是兩個相加變成某一個長度的比較然後越界？我覺得好像也沒那麼清楚。
  - Code review：1. 幾乎跟 #6 一樣；2. `if (i + j > s3.length()) return 0;` 這個 base case 是多餘的，因為開頭已排除。

**LLM 點評**：
model: Opus 5.5
- 75（insertion sort 是 in-place 的，這個理解要修正）：[sorted | unsorted] 的框架對 selection 和 insertion 都成立，差別在**哪一邊是固定的**：selection 是「位置固定（邊界那格），去 unsorted 裡**挑人**（找 min）再 swap 進來」；insertion 是「人固定（unsorted 的第一個），去 sorted 裡**找位置**」。找位置時不需要 reallocation：先把 key 存到 temp，sorted 裡比 key 大的元素往右挪一格（或一路相鄰 swap 往左推），空出來的洞放 key。額外空間 O(1)，所以是 in-place（`Algorithms/Sorting/Comparison_Based_Sorting/03-Insertion_Sort.md` 也這樣寫）。代價是**時間**：每次插入最多挪 O(n) 格，總共 O(n²)，但這是元素搬移，不是記憶體重配。in-place 的意思是 O(1) 額外空間，不是「元素不能動」。
- 75（所以「insertion + swap 炸掉」是實作 bug，不是概念錯）：n ≤ 300，O(n²) 完全能過，insertion sort 本身寫對就會 AC。常見的炸法：內層 `j` 從 `i - 1` 往左走時越界（`j >= 0` 要先判斷），或是 swap 後沒有跟著 `j--` 繼續往左推。
- 75（這題真正要考的）：值只有 0/1/2，不需要一般排序。**荷蘭國旗 / 三向切分**：三個指標維持 `[0, lo) = 0`、`[lo, mid) = 1`、`[mid, hi]` 未處理、`(hi, n) = 2`，一次掃描 O(n)、O(1) 空間。坑是 `nums[mid] == 2` 跟 `hi` swap 後 **`mid` 不能前進**，因為換回來的值還沒看過。見 `Algorithms/Sorting/Comparison_Based_Sorting/07-Quicksort_Advanced.md` 三向切分那段；兩趟的 counting sort（`Non_Comparison_Based_Sorting/01-Counting_Sort.md`）也可以，但 follow-up 要求 one pass。
- 75（第二次，正確；invariant 少寫了一段）：code 沒問題，`i <= right` 和「換 2 之後 `i` 不動」都對。但 invariant 其實是**四段**：`[0, left)` 是 0、`[left, i)` 是 1、`[i, right]` 未處理、`(right, n)` 是 2。只寫 [0 | unsorted | 2] 的話，解釋不了換 0 之後為什麼 `i` **可以**前進：因為從 `left` 換過來的一定是 `[left, i)` 裡的 1（或 `left == i`，換自己），是已經看過的值；而從 `right` 換過來的在未處理區，還沒看過，所以 `i` 不能動。兩個分支不對稱的原因就在這個 1 的區段。
- 97（index 跟 length 是同一個數字，不用二選一）：`i` 同時是「s1 **已經用掉幾個字元**」（length）和「s1 **下一個要用的 index**」，因為用掉 `i` 個，下一個就是 `s1[i]`。你註解最後一行已經寫出來了。把狀態講成**後綴**就不會混：`dp(i, j)` = 「`s1[i:]` 和 `s2[j:]` 能不能交錯成 `s3[i+j:]`」。
- 97（兩種邊界檢查，分開想）：① **終止狀態**：兩個後綴都空了，也就是 `i == m && j == n`；開頭已檢查 `m + n == s3.length()`，所以等價於 `i + j == s3.length()`。`i == m` 是**合法狀態**（s1 用完了），不是越界，所以 cache 開 `(m+1) × (n+1)`。② **轉移守衛**：要讀 `s1[i]` 之前先確認 `i < m`，這是「還能不能再拿一個」，不是 base case。你的 code 兩個都有，而且放在對的位置。Review 第 2 點也對：`i ≤ m`、`j ≤ n` 保證 `i + j` 不會超過 `m + n`，那行永遠不會執行。Top-down 的邊界放法見 `Algorithms/Dynamic_Programming/Implementation/Boundary_Condition_Handling.md`（入口剪枝）。
- 97（複雜度註解要改）：暴力法每一步最多兩個分支，深度 `m + n`，所以是 O(2^(m+n))，不是 O(2^mn)。加 cache 之後每個 `(i, j)` 只算一次，**time O(mn)**；**space O(mn)**（cache），外加遞迴深度 O(m + n)。你寫的 O(max(m, n)) 漏了 cache。Follow-up 常問 O(n) 空間：改 bottom-up，只留一列 `dp[j]`，見 `Algorithms/Dynamic_Programming/Fundamentals/03-TopDown_to_BottomUp.md`。
- 97（index / length 混淆的根源：`i` 是**切點**，不是元素）：`i` 指的是字元之間的縫（0..m，共 m + 1 個），左邊 `[0, i)` 是已用、長度 `i`，右邊 `[i, m)` 是剩下、從 `s1[i]` 開始。「已用長度 = 下一個 index」不是巧合，是 0-indexed + 半開區間造成的，從後往前走就會分開，所以要記「切點」而不是「i 就是長度」。今天 75 的 `[0, left)` 是同一件事。會搞混是因為腦中用 prefix 的長度，函式卻在回答 suffix 的問題。一個讀法只負責一件事：狀態定義講一邊（top-down 講 suffix、bottom-up 講 prefix），長度只拿來定邊界（`i == m` 合法 → 表開 m + 1）。試金石：「`i` 可不可以等於 `m`？」整理在 `Data_Structures/Arrays_and_Strings/Index_as_Cut.md`；bottom-up + 滾動陣列的 follow-up 已加進 `Checklists/Learning_Roadmap.md`。

---

## 2026-09-27

- 217. Contains Duplicate
- 383. Ransom Note
- 50. Pow(x, n)
- 64. Minimum Path Sum
- 295. Find Median from Data Stream

**心得**：
- 383：看了解答後，他的時間複雜度可以設計在 O(m)，不是我們的 O(max(m, n))，因為他多了長度比較：如果 ransom 比 magazine 長的話，一定組不出來，就直接回傳。
- 50：
  - recursive divide and conquer 寫完，還是超時，現在要考什麼？
  - 這題一直給提示，而且其實蠻多 edge case 的坑。要處理的包括：1. 負數的反轉值域；2. 遞迴深度超過，需要用 subproblem 的問題。
- 295：
  - 因為之前寫過了，是很經典的 two heaps 問題，所以就是順順把它想出來。你一定要先知道時間的 bottleneck 在哪，還有 invariant 的設計是最重要的。
  - 我的第一版還漏了一個很大的問題：沒有先把 max heap（左邊）的 top 跟插入的值比較，找出比較大的那個再插入右邊，然後才去 rebalance 來 maintain invariant。一開始就直接插入右邊，會導致我的 invariant 被 break，也就是左邊的 heap 裡不總是放左半部比較小的元素。因為如果先插到右邊，就會有元素插錯位置，導致有 test case 不會過。

**LLM 點評**：
model: Opus 5.5
- 383（長度檢查不會讓複雜度變成 O(m)）：early return 只處理 `m > n` 的情況；`m <= n` 時還是得把 magazine 整個數完，O(m + n) = O(n)，所以整體仍是 O(m + n)（跟 O(max(m, n)) 是同一件事）。長度檢查是常數級的捷徑，不是複雜度的改進。而且 O(n) 是下界：你需要的那個字母可能就在 magazine 最後一格，不讀完無法確定。能改的只有「提前結束」：先數 ransom（O(m)），再掃 magazine 扣需求，需求歸零就停，平均快一些，最壞還是 O(n)。
- 383（真正的 bug：`array<int, 26> counts;` 沒有初始化）：區域變數的 `std::array<int, N>` 不會自動歸零，裡面是垃圾值，能過是運氣。要寫 `array<int, 26> counts{};`（或 `= {}`）。`int cnt[26];` 也一樣，要寫 `int cnt[26] = {};`；`vector<int>(26)` 才會自動歸零。
- 50（只給提示，未給解）：① 超時的原因：`myPow(x, n / 2) * myPow(x, n / 2)` 呼叫了**兩次**同一個子問題，遞迴式是 T(n) = 2T(n/2) + O(1)，展開後是 O(n)，不是 O(log n)，跟暴力法一樣。問自己：同一個值需要算兩次嗎？② 修好之後的下一個坑：`n` 的範圍是 `[-2³¹, 2³¹ - 1]`，`n = INT_MIN` 時 `-n` 是多少？③ 這題要考的是**快速冪**（binary exponentiation）：每一層把指數砍半，只算一次子問題，再依奇偶決定要不要多乘一個 `x`。會了遞迴版之後，可以想想 iterative 版怎麼用 `n` 的二進位表示來做。
- 50（通過，修正一個說法）：超時不是「遞迴深度超過」，深度一直都是 O(log n)；問題是同一個子問題算了兩次，**呼叫次數**變成 O(n)。存成 `cache` 只算一次，就回到 T(n) = T(n/2) + O(1) = O(log n)。`INT_MIN` 用 `1 / (x^INT_MAX · x)` 繞過是對的；另一個常見寫法是先轉 `long long` 再取負號（`CPP_Reference/Type/Integer_Overflow_Prevention.md` 場景六就是用這題當範例）。快速冪（遞迴版、迭代版、陷阱）整理在 `Algorithms/Math/Fast_Exponentiation.md`。
- 295（正確，而且第一版的 bug 有名字）：`Data_Structures/Heaps/04-Two_Heaps_Balancing.md` 把這題拆成兩個不變式：**分割**（左邊全部 ≤ 右邊全部）和**平衡**（`left.size() == right.size()` 或多 1），對應三步「插入 → 轉移 → 再平衡」。你第一版直接插右邊，就是跳過了「轉移」這一步，所以壞掉的是分割不變式，不是大小。你最後的版本等價於筆記的模板：筆記是無條件 `left.push(num)` 再把 `left.top()` 移到右邊，你用 `if (left.top() > num)` 只在需要時才繞一圈，省一組 push/pop；無條件版少一個分支、比較不會寫錯，兩者都 O(log n)。註解裡 `always add to heap 2` 要改成「把 `max(num, left.top())` 加到 heap 2」，不然下次讀會以為是第一版。小細節：`right.top() + left.top()` 是 `int` 相加，這題值域 ±10⁵ 不會溢位，一般情況先轉 `double` 或 `long long` 再加比較保險。

---

## 2026-09-26

- 190. Reverse Bits
- 191. Number of 1 Bits
- 202. Happy Number
- 34. Find First and Last Position of Element in Sorted Array
- 36. Valid Sudoku

**心得**：
- 190：有需要練 divide and conquer 嗎？還是留著之後 follow-up 就好？divide and conquer 會變成 medium 到 hard。
- 191：跟 190 之後一起排 follow-up：divide and conquer 和 fixed precalculated（查表）。
- 36：
  - 這題超級白痴的。題目只有問數獨是否合法，不是有沒有解（合法也不一定要有解），結果一開始就跳下去做 backtracking 看有沒有解。
  - 合法狀態發生的條件，就是那三個限制沒有出現重複的，所以直覺用 hash map 一次就可以做完了。
  - 主要的流程概念拆解應該是：暴力法（brute force）的時間會到 N 三次方，然後可以用 hash map 降到 N 平方。
  - 一開始題目搞錯了，後面花了超多時間都是浪費的，直接把 medium 變 hard，而且還不會通過，因為根本搞錯題目了。

**LLM 點評**：
model: Opus 5.5
- 190（不用練，知道一句話就夠）：這裡的 divide and conquer 不是會把題目升級成 medium/hard 的那種遞迴分治，而是固定 5 行的 bit trick：先交換左右 16 bits，再用 mask 在每一半裡交換 8 bits、4、2、1（`0xFF00FF00`、`0xF0F0F0F0`、`0xCCCCCCCC`、`0xAAAAAAAA`），O(log w) 次操作、沒有迴圈。它屬於「背 mask」的技巧，不是可遷移的思考方式，練了 CP 味道重、面試回報低。面試官對這題常見的 follow-up 是「被呼叫很多次怎麼優化」，比較好講的答案是**查表**：預先算好 256 個 byte 的反轉結果，每次拆成 4 個 byte 查表再拼回去。能口頭講出「查表」和「mask 分治交換」這兩句就夠，不用實作。同一組 mask 也用在 191 Number of 1 Bits 的 popcount follow-up，真的想練時兩題一起看。
- 36（「合法」被換成了「可解」）：動詞沒讀錯，錯在把「合法」的定義換成了自己的直覺。題目明確定義了合法：已填的格子在行、列、宮裡沒有重複，Note 還特地寫了 *valid but not necessarily solvable*。但數獨的日常語感是「合法 = 能解完」，這個直覺蓋過了題目的定義，目標就從「檢查約束」變成「搜尋一個解」，backtracking 是被錯的目標帶出來的。教訓：**題目有自己定義的詞（valid、balanced、happy…），就照字面用它的定義，不要帶入領域常識**；開始設計前，先把「合法」改寫成可以直接檢查的條件（這題是「三組 set 都沒有重複」），寫得出來，目標就不會跑掉。解法本身：三組 set（row、col、box），box 編號 `(r / 3) * 3 + c / 3`，每格查一次。複雜度你的分析是對的（每格掃整行整列整宮是 O(N³)，hash 是 O(N²)），但面試時可以補一句：棋盤固定 9×9，嚴格說兩者都是 O(1)，N² 是對一般 N×N 的推廣。

---

## 2026-09-25

- 76. Minimum Window Substring
- 110. Balanced Binary Tree

**心得**：
- 76：
  - 大概念是：hashmap 跟 `matchCount`，我是用我最熟悉的心法 expand → fix → update 來想。一直卡在 fix 要怎麼設計，一直設計不出來。
  - 主要概念就是我希望 expand 之後，要可以有效的 fix，就想到要看 window 最左邊的人，而最左邊的人只有兩種可能：在 target 或不在 target。
  - 問題被收斂到：他是否值得移除？如果不在 target，當然就無腦移除；如果在，就要確認數量是不是有貢獻最終的合法 window，沒有貢獻，就可以安全移除。
  - 最後歸納下來是滿簡單的……但是這個過程繞了滿多的＠＠
- 110：
  - 把「遞迴」跟「全局追蹤」兩個狀態拆開，比較簡單直覺。
  - 但是可以嘗試另一個做法，都用 return value 來處理，但是因為兩個狀態，所以實務上拆兩個遞迴式比較好實作。

**LLM 點評**：
model: Opus 5.5 (1M context)
- 76（你的框架不用換，要重新定義的是 fix）：我一開始的提示推你改成「while 合法就縮、update 放在 fix 裡」那套，其實沒必要。expand → fix → update 對求最短一樣成立，只要把 fix 定義成「**丟掉左邊多餘的字元**」：`while (多餘(s[i])) { counting[s[i]]--; i++; }`，fix 完就是以 `j` 結尾的最短窗口，update 照樣放在 fix 後面。關鍵是把「在不在 t 裡」換成「**砍掉它還 match 嗎**」→ `counting[x] > target[x]`（不在 t 裡的字元，需要量是 0，自動涵蓋）。因為只丟多餘的字元，窗口不會被砍到不合法，`matchCount` 全程只增不減：**fix 管最短，`matchCount` 管合法**，兩件事分開。實作陷阱：`target[x]` 對不存在的 key 會插入 0，讓 `target.size()` 變大，你用 `!target.contains(x) ||` 短路避開了。過程中的 bug：`while` 條件寫成 `matchCount == target.size()`（迴圈裡不會變，一路砍到空）、每輪覆寫答案沒比大小、用迴圈結束時的 `i`/`j` 切答案。最終版：update 只在合法且更短時記 `start` + `length`，最後切一次。
- 110（「拆兩個遞迴式」要看怎麼拆）：如果是 `isBalanced(root)` 每層呼叫 `height(left)`、`height(right)` 再遞迴自己，每個節點的高度會被重算，**worst case（歪斜樹）O(n²)**，這是這題的經典陷阱，面試會被追問。你的「height 遞迴 + 全局 flag」是 O(n)，沒問題。
- 110（兩個狀態用一個 return value 帶）：不用拆，用**哨兵值編碼**：`height()` 回 `-1` 代表「這棵子樹已經不平衡」，否則回真實高度。子樹是 `-1` 或 `abs(l - r) > 1` 就往上傳 `-1`。高度永遠 `>= 0`，所以 `-1` 不會跟合法值撞，一個 `int` 就同時帶了「高度」跟「是否平衡」，還能提早剪枝。判斷準則：第二個狀態是**「失敗了就不用再算」的 bool**時，把它塞進回傳值的不可能區域；兩個狀態都是**獨立的真實數值**（例如 543 直徑要回傳高度、同時更新全局最長路徑）時，才用 `pair` 或全局變數。

---

## 2026-09-24

- 100. Same Tree
- 101. Symmetric Tree
- 108. Convert Sorted Array to Binary Search Tree
- 110. Balanced Binary Tree

**心得**：
- 100：有需要做 queue iterative 版本嗎？
- 101：這次可以做 iterative 版本了？
- 108：需要做其他解法嗎？
- 110：多嘗試了雙遞迴，從定義設計去解決（balanced ⇔ 左右子樹都 balanced 且高度差 <= 1，所以需要 `isBalanced` 跟 `height` 兩個遞迴），我覺得不錯，但是需注意時間分析。

**LLM 點評**：
model: Opus 5.5 (1M context)
- 100（iterative 要不要練）：不必當成另一題練。recursive 就是這題的標準答案：base case 是「兩個都 null → true；只有一個 null 或 `val` 不同 → false」，然後 `left && right`。iterative 版本只是把**同一段比較搬進迴圈**：queue（或 stack）裡放 `pair<TreeNode*, TreeNode*>`，pop 出來做一模一樣的三個判斷，再成對 push `(p->left, q->left)`、`(p->right, q->right)`。重點是「**成對**入隊」，不是 BFS 本身，所以 queue 還是 stack 都行。值得會寫的理由只有一個：面試官 follow-up「樹很深會 stack overflow 怎麼辦」時能當場改寫。會了 101 Symmetric Tree（成對 push 改成交叉：`(l->left, r->right)`、`(l->right, r->left)`）就等於一起練到了。
- 101（對，這題就是練 iterative 的時機）：跟 100 是同一個骨架，只改兩處：① **起點**是一棵樹拆成兩半，push `(root->left, root->right)`，不是兩棵樹；② **成對 push 改交叉**：`(l->left, r->right)`、`(l->right, r->left)`（外側對外側、內側對內側）。pop 後的三個判斷一字不改。所以寫 iterative 時要驗證的只有「配對規則」，這也說明 100/101 的本質都是**同步走兩個指標**（見 `Data_Structures/Trees/DFS.md`），recursive 與 iterative 只是 call stack 顯式或隱式的差別。
- 108（不用另練解法，要練的是下一題）：「取中點當 root、左半建左子樹、右半建右子樹」就是這題唯一值得記的解法，O(n)。iterative（stack 放 `(node, lo, hi)`）只是把遞迴手動展開，沒有新觀念，不必練。偶數長度時取左中或右中都對（題目允許多解），重點是**區間定義一開始就定死**（`[lo, hi)` 半開 → `lo == hi` 回 null，見 `Algorithms/Divide_and_Conquer/03_Interval_Design_in_Divide_and_Conquer.md`）。真正「換一個解法」的是 **109 Convert Sorted List to BST**：linked list 不能 O(1) 取中點，改成先算長度、照 **inorder 順序**遞迴建樹，外部指標每建一個節點就往前走一步，O(n)，也就是 `Algorithms/Divide_and_Conquer/06_External_State_Traversal_Order.md` 在講的：遞迴區間管結構，外部指標管取值。
- 110（雙遞迴的時間，`O(n²)?` 其實猜鬆了）：這版是 top-down，成本 = 每個「被走到的節點」各付一次 `height` = 其子樹大小。但 `&&` 會**先檢查高度差、失敗就短路**，所以最常被舉的「歪斜鏈」反而在 root 就 return false，只花 O(n)；完全平衡樹則是每層 O(n) × O(log n) 層 = **O(n log n)**。真正的上界：一個節點 x 被重算的次數 = 它「通過檢查」的祖先數 k；每個通過的祖先，另一側子樹高度至少要跟 x 這側差不到 1，這些旁支互不重疊，總節點數 ≳ k²/2 ≤ n，所以 k = O(√n)，最壞 **Θ(n√n)**，不是 O(n²)。面試時說「O(n·h)，平衡時 O(n log n)」最穩。那段 `looks lots of redundant` 的直覺是對的：重算來自「高度」和「是否平衡」分兩趟算，合成一趟就是 09-25 點評講的 `-1` 哨兵 bottom-up，O(n)。定義先寫出雙遞迴、再看出重算、再融合，這個推導順序本身就是面試想看的。

---

## 2026-09-23

- 35. Search Insert Position
- 66. Plus One
- 67. Add Binary

**心得**：
- 35：這是 easy?! 我是用 search space 去想的，知道這題是問 lower bound（我的反射），但最後做出來是因為慢慢從 search space 跟「answer = 第一個 `nums[i] >= target` 的 i」推，search space 是 `[0, n]`，然後配上適當的 movement（less → `[mid + 1, j]`；otherwise → `[i, mid]`，保留 mid）。但是之前筆記的思考方式好像不是這樣。
- 67：媽媽樂……這題意外難寫！！
  - 因為它有三個狀態要 maintain，有點難直接控制三個狀態在 while 迴圈上。一開始為了寫漂亮的 guard，一直在設計怎麼減少狀態，想說可不可以只保留一個 index 跟一個 carry。愈寫愈發現，少一個狀態後沒有比較簡單，因為當 while 不成立時反而要繼續做——只要還有狀態合法（search space 合法），就要繼續做。
  - 最後想一個簡單的 invariant：`i || j || carry`，任一個人有效就繼續做，才比較簡單地思考這題。
  - 另外在思考時設計了兩個讓我頭腦混亂的變數：
    1. 為了讓回傳值可以直接沿用 input，我做 swap 把長的人放前面，然後直接更新長的人，反而把事情搞複雜，一直在處理長的變成 return 值時的更新。
    2. 因為長的跟回傳值卡在一起，腦袋很混亂。

**LLM 點評**：
model: Opus 5.5 (1M context)
- 35（你的感覺是對的：筆記裡有兩套互相打架的模板）：`Algorithms/Binary_Search/04-Legacy_Closed_Interval_Search.md` 是**閉區間 `[0, n-1]` + `left <= right` + 三路比較（`==` 就 return）**，插入點靠「迴圈結束時 `left` 恰好停在對的地方」這個事後解釋；`01-Boundary_Search_Guide.md` 的 lower_bound 才是你今天這套：**半開 `[0, n]` + `i < j` + 二分判斷**。你這次的推法（先定義答案 = 第一個滿足 predicate 的位置 → 答案可能是 n 所以 search space 含 n → 不滿足就丟掉 mid、滿足就留住 mid → 收斂到 `i == j` 那格就是答案）是**從定義推出來的**，比 01 那套「背下來、結束時 left 剛好是插入點」可靠得多，也能直接推廣到 04 的 binary search on answer。照 repo 慣例，Binary_Search 資料夾還缺 `00-*_Standard_Template.md`，今天這版就是該升格的那一個，01 應該降為 ⚠️ rejected alternative。
- 35（程式碼最後的 note 寫反了）：`nums[i] <= target → lower bound`、`nums[i] < target → upper bound` 是錯的。正確是看「往右丟」的條件：`nums[mid] < target` 時 `i = mid + 1` → **lower_bound**（第一個 `>=`）；`nums[mid] <= target` 時 `i = mid + 1` → **upper_bound**（第一個 `>`）。記法：丟掉的是「不是答案」的那一側，**predicate 的否定就是 move-right 條件**。
- 67（「少一個狀態」為什麼沒有變簡單）：你縮減的不是狀態，是**迴圈條件**。`i`、`j`、`carry` 是三個**獨立的剩餘工作來源**，少寫一個進 `while`，那份工作就被推到迴圈外，得再補一段收尾（「while 不成立時反而要繼續做」正是這個症狀）。`while (i >= 0 || j >= 0 || carry)` 的意思是「**還有任何一份工作沒做完就繼續**」，迴圈體內用 `i >= 0 ? a[i--] - '0' : 0` 把「已經用完的來源」補成 0，三條路徑合成一條，外面就不需要任何收尾。跟 994 把 `fresh > 0` 寫進 `while` 是同一個動作：**讓迴圈條件精確等於「還有事要做」**（`Algorithms/Design_Principles/Correct_by_Construction.md`）。同一個骨架直接套 2 Add Two Numbers、415 Add Strings、66 Plus One（66 就是只有一個來源 + `carry` 初值為 1）。
- 67（用詞小修正）：`i || j || carry` 是**迴圈的繼續條件**，不是 invariant。這題的 invariant 是「`res` 已經存了兩個字串低位部分的和，`carry` 是還沒寫出去的進位」——它說明了**為什麼**三者都耗盡時 `res` 就是答案。
- 67（swap + 原地改長的那個：一個變數扛兩個角色）：輸入和輸出共用同一個字串，就要一直在腦中追蹤「這一格現在是加數還是結果」，而且最後進位還可能讓長度 +1，原地改也省不了。先讓**輸入唯讀、輸出另開**（`res.push_back` 後 `reverse`，O(n)），寫對之後再考慮省空間。這個 O(n) 本來就是答案本身的大小，省不掉什麼。

---

## 2026-09-22

- 300. Longest Increasing Subsequence
- 未完成：416. Partition Equal Subset Sum
- 994. Rotting Oranges

**心得**：
- 300：
  1. 一開始很關鍵的暴力法想錯級數，導致我一直以為往前查全部表的概念是錯的 O(n²)。
  2. 這是最近第二次，dp / cache 初值填錯。
  - follow-up：O(n log n) 關鍵技巧是什麼，我有開文件嗎？記錄下來之後做。
- 416：
  - 不能用 backtracking ?!?!?! 可能還是因為 `1 <= nums.length <= 200`，我本來就有一個感覺，這個 size 還是有點大……
  - 不能用 sort 然後加總，因為竟然有反例？！`[2, 2, 1, 1]` → 答案是 `{1, 2}` `{1, 2}`，這個演算法不 work!!!!!!!!
  - 受不了了，去看了提示的 tag：Junior, Array, Dynamic Programming, Knapsack Problem, 0-1 Knapsack。
  - subset sum 會讓我想到 backtracking → NP-problem → dynamic programming，這樣我感覺 #2 的方向可以往下優化。
  - 純紀錄，先不給提示或回饋，我要衝一發。
- 994：
  1. 關鍵失誤：edge case 沒有測試清楚——`[[0]]`，所以 minute 算錯。修正方式是最後用 guard（`std::max(level - 1, 0)`），還是覺得哪裡怪怪的，感覺應該有地方可以消掉那個 `std::max`。
  2. 這個其實不好實作，要設計的狀態除了 multi-source BFS 外，還要處理 fresh 個數、level 計數。
  3. space 也錯了，最差是全部都是 rotten orange，塞滿 queue，O(mn)。

**LLM 點評**：
model: Opus 5 (1M context)
- 300（暴力法算錯級數的代價，比算錯本身大）：LIS 真正的暴力法是**列舉所有子序列**，O(2ⁿ · n)。O(n²) 的「往前查全部表」**已經是優化過的版本**——它把指數級的子序列壓成 n 個狀態，每個狀態 O(n) 轉移。把 O(n²) 誤當成暴力，就會以為這個方向「還沒優化、是錯的」而去找別條路，其實人已經站在正確的路上。教訓：**暴力法的級數是整趟推導的座標原點**，原點錯了，後面每一步對「我優化了多少」的判斷都會偏。先寫下「暴力 = 列舉什麼、共幾個」再開始想。
- 300（初值不是用填的，是從定義讀出來的）：第二次錯同一類，照 `Algorithms/Design_Principles/Correct_by_Construction.md` 的判準，這已經不是粗心、是結構問題。修法：**先把 `dp[i]` 的定義一字不差寫成第一行註解**（「以 `nums[i]` **結尾**的 LIS 長度」），初值就是這個定義在最小情況下的值——任何元素自己就是長度 1 的遞增子序列，所以是 `1`，不是 `0`。答案也從同一句推出來：「以 i 結尾」→ LIS 可能在任何位置結束 → 取 `max(dp)` 而不是 `dp[n-1]`。**定義、初值、答案位置三者是同一句話的三個推論**，只要其中一個是「填的」，就會錯。（同一個形狀：139 用 length 定義讓 `dp[0] = true` 自然存在。）
- 300（O(n log n) 的關鍵技巧：把 dp 的索引和值**對調**）：O(n²) 版是「索引 = 結尾位置、值 = 長度」。O(n log n) 版把它翻過來：`tails[k]` = **所有長度為 `k+1` 的遞增子序列中，最小的結尾值**——索引變成長度、值變成結尾。翻過來之後 `tails` **必然嚴格遞增**（更長的子序列，最小結尾一定更大），單調 → 可以二分 → 每個元素 `lower_bound` 一次，替換或延長。為什麼「留最小結尾」是對的：同長度下結尾越小，**後面能接的數越多**，它支配其他候選（exchange argument）。
- 300（有文件，但缺的正好是「為什麼」）：`Data_Structures/Arrays_and_Strings/Subsequence_Problem_Solving_Strategies.md` §2 已經寫了 `tails` + `lower_bound` 的**步驟**，但沒寫**對調索引與值**這個動機、`tails` 為何單調、為何留最小結尾。只有步驟的筆記就是這次召回不到的原因。兩個實作陷阱一併記：(1) **嚴格遞增用 `lower_bound`，非遞減要換 `upper_bound`**；(2) `tails` **不是**真正的 LIS 本身（`[3,4,1]` 跑完是 `[1,4]`，但 `1,4` 不是子序列），只有長度是對的——要還原序列得另存 predecessor。已加進 `Checklists/Learning_Roadmap.md`。
- 994（怪在哪：`level` 數的東西跟答案要的東西不一樣）：`level` 數的是「**處理了幾層**」，答案要的是「**過了幾分鐘**」＝層與層之間的**間隔數**＝層數 − 1——典型的 fencepost。最後一層一定是「被處理、但什麼都沒感染」的那層，所以要 `- 1`；而層數為 0（一開始就沒有腐爛橘子，如 `[[0]]`）時 `0 - 1 = -1` 不成立，`std::max` 就是在補這個洞。**guard 在修正一個語意錯了的計數器**，跟 153 選錯參照點、236 回傳型別太弱是同一個形狀（見 `Algorithms/Design_Principles/Correct_by_Construction.md`）。
- 994（消掉 `std::max`：把目標寫進迴圈條件）：`while (!q.empty() && fresh > 0)`，結尾 `return fresh == 0 ? level : -1;`。現在每跑一圈都**真的過了一分鐘、而且感染了東西**，`level` 的語意直接就是「經過的分鐘數」：沒有新鮮橘子 → 迴圈一次都不跑 → 0（`[[0]]`、`[[2]]` 自動正確）；感染完最後一顆就停 → 不會多數那一層空轉。`-1` 和 `max` 同時消失，`fresh` 也從「只拿來驗答案」升級成同時負責**提前結束**。另一條路是 `Algorithms/BFS/MultiSource_BFS_Thinking_Framework.md` 的 `dist` 寫法：來源的距離是 0，答案＝最大距離，**根本不需要 level 計數器**，fencepost 也就不存在。
- 994（space 的修正是對的，原本的直覺從哪來也值得說清楚）：O(max(m, n)) 是**單源** BFS 在空曠網格上的直覺——波前是一條對角線，長度 O(m + n)。**多源**時這個上界不成立：初始 queue 本身就可以是全部格子（全是 2），所以是 O(mn)。一般化：**BFS 的空間看的是「最寬的一層」有多寬，multi-source 的第 0 層就可能是全部。**
- 994（小地方）：`for (const auto neighbor : neighbors)` 每次迭代都**複製一個 `vector<int>`**，改成 `const auto&`，或乾脆用 `int dirs[5] = {0, 1, 0, -1, 0}` 配 `dirs[k], dirs[k+1]`。另外 `grid[x][y] = 2` 會改到輸入，面試時先問一句可不可以改。心得第 1 點正好就是昨天加進 checklist 的「至少跑一個 classic、一個 edge」——這題範例全都過，只有 `[[0]]` 會爆。

---

## 2026-09-21

- 138. Copy List with Random Pointer
- 150. Evaluate Reverse Polish Notation
- 153. Find Minimum in Rotated Sorted Array
- 198. House Robber
- 215. Kth Largest Element in an Array
- 236. Lowest Common Ancestor of a Binary Tree

**心得**：
- 236：第二次做，還是只有想到 maintain 兩個回傳值去做 or operator。兩個回傳值都 true 表示找到，但還要去處理 stack rewind 後面遇到的 node 不能再次更新的問題，總之就很醜。follow-up：空間不夠好，因為會 maintain 兩個 boolean，**如何用 LCA 本身來當回傳值——必重做一次**。
- 215：top-k min heap 就解了。紀錄一下要做 quickselect，必做——quickselect 我似乎一直沒整理，這題感覺就可以做很多 follow-up。
- 153：這次的解法是找到 inflection point 出現的那邊，排除其他邊。
- 153（二版，一行判斷式）：思考順序是——(1) 先確認 `i` 跟 `j` 互相比較得不到有用資訊（`nums[i] < nums[j]` 只夠用來提前結束）；(2) 再由 rotated sorted 的特性想到拿 `mid` 跟 `j` 比：`mid > j` 去掉左半，`mid <= j` 去掉右半（`mid` 也可能是答案）。至於為什麼不能拿 `mid` 跟 `i` 比——rotated sorted 保證的是「某一段已排序」，而 `nums[mid] > nums[i]` 不表示任何事情，不能當結構上的判斷式。
- 150：粗心兩次了，top1 是 operand 2、top2 是 operand 1，我是不是腦袋會漏東西，兩個運算元位置放錯。
- 138：hashmap + cache + two pointers，結果沒處理到 nullptr。自己也覺得這個解法一定哪裡怪怪的。想問：有辦法 one-pass 嗎？這題要 look forward，先檢查未來但不知道未來的位置（可以用 next 反查？）。另外好像可以先用 random 去存，可以省一個空間？

**LLM 點評**：
model: Opus 5 (1M context)
- 153（寫對了，而且兩個分支互斥是可以證明的）：`nums[i] > nums[mid]` 成立時，拐點落在 `[i, mid]`，所以 `[mid, j]` 必定是升冪的 → `nums[mid] < nums[j]`，第二個分支**不可能**同時成立。這代表分支的先後順序不影響正確性——這種「互斥可證」的結構值得當場確認一下，因為只要兩個條件會同時成立，先寫誰就變成一個藏在順序裡、沒被寫下來的決定。
- 153（第一個比較是冗餘的，repo 已有正規版）：`nums[i] > nums[mid]` 這一支的結論（`j = mid`）跟「`nums[mid] < nums[j]` → `j = mid`」完全重合，所以**一次比較就夠**：`if (nums[mid] > nums[j]) i = mid + 1; else j = mid;`，迴圈結束時 `i == j` 就是答案。這正是 `Algorithms/Binary_Search/03-Peak_and_Rotated_Array_Search.md` 的模板（`beforeInflection(m) → nums[m] > nums[r]`）。你的版本是「模板 + 一次冗餘比較 + 一個提前 break」。
- 153（真正該記住的是：為什麼跟**右**端比，不是左端）：因為 `nums[m] > nums[右端]` 這個謂詞在整個陣列上是**單調的**（false…false true…true 反過來也是一刀切），二分搜尋能work的前提就是謂詞單調。跟左端比不具這個性質——`[1,2,3]` 沒旋轉時 `nums[mid]=2 > nums[i]=1`，照「大於就往右」會直接丟掉答案。**選擇比較對象不是風格問題，是在選一個單調謂詞。**
- 153（break 的代價，以及它在 154 第一個死）：早退要付「每輪多一次比較」，而提前結束只在已排序的子區間才發生，平均省不到什麼。更重要的是它是**最脆弱的那一段**：`154 Find Minimum II`（可重複）一來，`[3, 3, 1, 3]` 會走到 `nums[i] == nums[mid] == nums[j]`，你的 `break` 直接回傳 `nums[i] = 3`，錯。有重複值時「兩端相等」根本無法判斷拐點在哪邊，只能 `j--` 退化成 O(n)。
- 153（`j = mid` 和 `i = mid + 1` 的不對稱不是隨意的）：往左收時 **mid 本身可能就是答案**，所以不能 `mid - 1`；往右收時 `nums[mid] > nums[j]` 已經證明 mid 不是最小值，所以可以也**必須** `+1`。而 `mid` 下取整保證 `mid < j`，`j = mid` 一定讓區間變小、不會死迴圈。不變量一句話：**答案永遠在 `[i, j]` 內**——邊界怎麼移是從它推出來的，不是試出來的（見 `Algorithms/Backtracking/07-Guards_from_Invariants.md` 的同一套讀法）。
- 236（先確認：你的版本是對的，別被「醜」蓋過去）：`pair<bool,bool>` + 全域 + reset 的組合**正確性沒問題**（p 是 q 的祖先那種 case 也對），複雜度 O(n) / O(h)，跟正規解同級。所以這不是解法錯，是**表達**的問題——而且醜在哪裡可以精確指出來，見下一條。
- 236（醜的根源只有一個：回傳型別太弱）：`pair<bool,bool>` 只回報「子樹裡有沒有」，**丟掉了「是哪個節點」**。答案是一個節點，回傳值卻答不出節點，於是那個資訊只能另外找地方存 → 全域 `LCA`。而全域一旦可以被寫第二次，就得再補兩個補丁：`found = {false,false}` 的 reset 和 `if (LCA) return found` 的早退。**兩個補丁都是在防止同一件事：祖先把答案覆蓋掉。** 這跟 153 選錯參照點就得補「已排序」特判、138 用 `int` 中介就得補 `nullptr` 特判，是同一個形狀（見 `Algorithms/Design_Principles/Correct_by_Construction.md`）。
- 236（可直接複用的判準）：**遞迴需要全域變數 + guard 來維持正確性時，先回頭質疑回傳型別，而不是去加固 guard。** 骨架 `ReturnType solve(root)` 裡那個 `ReturnType` 應該是**子問題的答案型別**，不是「子樹的狀態」——見 `Data_Structures/Trees/Recursive_Design_Pattern_Pruning_and_Aggregation.md` 的萬用骨架。你已經在註解裡寫出 `TreeNode*` 這個方向了，這題就是照它重寫一次。
- 236（重做時給自己的三個問題，不看答案）：(1) base case 回傳什麼才能讓上層不用特判？(2) 走到 `root == p` 或 `root == q` 時，該繼續往下找還是可以直接回傳？為什麼不會漏掉「p 是 q 的祖先」？(3) 左右各自回傳結果後，只有**一邊非空**代表什麼、**兩邊都非空**又代表什麼——這兩句話寫出來，aggregation 就只剩一行。寫完檢查：**全域變數和 reset 應該都不存在了**。
- 236（你的布林直覺不是錯的，只是用早了）：正規解能省掉布林，是因為本題**保證 p、q 都在樹裡**。一旦不保證（`1644. LCA of a Binary Tree II`），「回傳非空」就不再等於「找到 LCA」，那時才真的需要補計數／布林（回傳 `pair<TreeNode*, int>` 或先驗證存在）。所以正確的記憶方式是：**布林是 1644 的工具，236 不需要**——條件放寬才引入它，不是反過來。
- 215（min heap 是對的選擇，先把取捨講清楚）：`priority_queue` 維持大小 k 的 **min heap**，堆頂就是目前第 k 大，時間 O(n log k)、空間 O(k)。相對 quickselect 的平均 O(n)：**n 很大而 k 很小時 heap 常常更快**（log k 是小常數且 cache 友善），而且它天然支援 **streaming / 資料放不進記憶體**，quickselect 則必須整份在手上、還會改動輸入。面試講出這組取捨，比直接寫 quickselect 更有價值。
- 215（quickselect 的核心是「只遞迴一邊」）：跟 quicksort 唯一的差別——partition 完看 pivot 落點，**只往包含答案的那半邊繼續**，另一半直接丟掉。均攤 T(n) = T(n/2) + O(n) = **O(n)**；最壞 O(n²)（每次都切在邊界），修法是**隨機選 pivot**（或 median-of-medians 保證最壞 O(n)，但常數大、面試只需口述）。repo 已有 `Algorithms/Partition/01-Lomuto_Partition_Scheme.md` 可以直接接上去，缺的是「選擇」這一層。
- 215（實作最容易錯的兩點，先記下來）：(1) **k 要先轉成索引**——第 k 大 = 排序後的索引 `n - k`，之後整趟都用索引比較，別在迴圈裡反覆換算；(2) 遞迴/迴圈的**終止條件是 `pivot_index == target`**，不是區間長度 1。另外務必寫成 while 迴圈而非遞迴（尾遞迴，省 stack）。
- 215（follow-up 你的直覺對，它是一整個家族的入口）：**347 Top K Frequent**（同一招套在 frequency 上，另有 bucket sort O(n) 解）、**703 Kth Largest in a Stream**（streaming → 只有 heap 能做，quickselect 出局）、**973 K Closest Points**、**295 Find Median from Data Stream**（雙 heap）、**4 Median of Two Sorted Arrays**（同樣是選擇問題，但要 O(log) → 改用 binary search on partition）。這條線值得開一篇 `Algorithms/Partition/` 底下的 Quickselect 心法，已加進 `Checklists/Learning_Roadmap.md`。
- 153（二版收斂到模板了）：`if (nums[mid] > nums[j]) i = mid + 1; else j = mid;` 就是 `Algorithms/Binary_Search/03-Peak_and_Rotated_Array_Search.md` 的通用模板逐字對應（`beforeInflection(m) → nums[m] > nums[r]`）。三分支塌成二分支之後，`else` 那支自動涵蓋了原本要 `break` 的已排序情形——**不是把 break 刪掉，是它不再是一個獨立的 case**。
- 153（「mid 跟 i 比沒有意義」要修正——真正的差別更有用）：`nums[mid] < nums[i]` 其實**是**有意義的，它確定拐點在左半（這正是你第一版的第一條分支，而且它是對的）。沒有意義的是**反過來**：`nums[mid] > nums[i]` 什麼都不能斷定。所以精確的說法是——**跟 `i` 比只有一個方向能下結論，跟 `j` 比兩個方向都能**。二分搜尋要的是每個 mid 都能做出決定的**完整二分**，只能單向決定的謂詞湊不出 `if/else`。
- 153（更漂亮的判準，而且跟 138 是同一件事）：拿 `i` 當參照其實**也做得出來**（`P(m) = nums[m] < nums[i]` 在區間上同樣單調），但它有一個洞：完全沒旋轉時 `[1,2,3]` 沒有任何元素滿足 `P`，答案就漏掉了——**必須**靠「已排序就提前結束」那個特判把它補回來。拿 `j` 當參照則不需要，已排序的情形自動落進 `else`。兩個參照點的真正差別不是「有沒有意義」，是**其中一個讓特殊情況消失，另一個讓特殊情況變成必要條件**。這跟 138 換成 `map<Node*, Node*>` 之後 `nullptr` 特判自動消失是同一個形狀，見 `Algorithms/Design_Principles/Correct_by_Construction.md`：選對承載結構的東西，例外就不存在。
- 153（所以你二版的 break 現在是純優化）：留著沒錯（已排序區間可以早退），但它不再扛正確性。判斷方式很簡單：**把它刪掉，答案還是對的**——這就是「優化」和「特判」的分界線，值得每次都確認一下自己留的是哪一種。
- 150（不是粗心，是你在記一件「會被順序翻轉」的事）：`a - b` 唸起來左邊先，但 stack 吐出來右邊先。人腦記「第一個 pop = 第一個 operand」是自然的類比，而它**每次都會錯**，所以這不是注意力問題，是**類比本身錯了**。修法是把順序從記憶移出來、寫進命名：**`int rhs = st.top(); st.pop(); int lhs = st.top(); st.pop();` 然後寫 `lhs - rhs`**。`lhs` / `rhs` 直接說出「它在算式的哪一側」，不需要任何約定去解碼，pop 的先後就退化成實作細節。（`a`/`b` 差一步，它靠「字母序 = 左到右」這個外部約定，只是把記憶搬家；`op1`/`op2` 最糟，`1`/`2` 同時可以指 pop 順序和算式順序，正好把有歧義的維度編進名字裡。）
- 150（檢查成本極低，養成 reflex）：commutative 的 `+`、`*` 怎麼放都對，所以**錯只會在 `-` 和 `/` 上現形**——送出前心算一個 `["3","1","-"]` → 應得 **2**（不是 -2），一秒就能抓到這個 bug 的全部兩種形態。把「非交換運算就用最小例子試一次」當固定動作，比提醒自己「別粗心」有效得多。
- 150（整數除法的暗礁）：C++ 的 `/` 對負數是**向零截斷**（`-7/2 == -3`），這題要的正是這個，所以直接用 `/` 就對；但別換成 `floor` 或 Python 的 `//`（向下取整，`-7//2 == -4`）。同一顆地雷在 29. Divide Two Integers 和 `%` 取模那一類題還會再踩到。
- 138（怪怪的具體位置）：你用了**兩張 map 組成一個函數的複合**——`hashmap: Node* → int` 和 `cache: int → Node*`，而 `cache[hashmap[x]]` 逐字就是 `map[x]`。中間那個 `index` 給舊節點編號、再把編號解回新節點，繞一圈回到原點，**沒有任何一行程式碼真的需要那個整數**。直接一張 `unordered_map<Node*, Node*> map`（舊 → 新）就好。怪怪的感覺是對的，而且它不只是冗餘，它是 bug 的來源（下一點）。
- 138（nullptr 那行是「對的結果、錯的理由」）：`hashmap[nullptr] = index` 存在的真正原因是——**`int` 的零值 `0` 是一個合法的索引**。少了這行，`hashmap[nullptr]` 會被 `operator[]` 預設建構成 `0`，`cache[0]` 是**第一個新節點**，於是 random 指到頭去了。而你補上的那行之所以能救，是因為 `cache[n]` 從沒被寫過，`operator[]` 又 value-initialize 出一個 `nullptr` 還給你（順便靜默插入一筆）。換成 `Node* → Node*` 之後，`map[nullptr]` 的預設值**剛好就是正確答案 nullptr**，特判不是被省掉，是根本不存在。心法：**多一層 int 編碼，就多一個「零值有歧義」的破口**；見 `CPP_Reference/Container/Operator_Bracket_Behavior_Vector_vs_Map.md`。
- 138（one-pass 可以，靠 lazy 建立）：你卡在「要 look forward，但未來的節點還沒建」。解法是**不要等走到才建，而是遇到就建**——寫一個 `get(p)`：`p == nullptr` 回 nullptr，否則 `auto& q = map[p]; if (!q) q = new Node(p->val); return q;`。然後一趟就結束：`Node* c = get(cur); c->next = get(cur->next); c->random = get(cur->random);`。關鍵是**節點的「建立」和「填欄位」解耦**：建立可以亂序、提前，填欄位才需要照順序。這個 lazy-create 是處理「圖有前向引用」的通用手法（反序列化、克隆圖 LC 133 同一招）。
- 138（「先用 random 去存」方向對、載體挑錯）：想省掉那 O(n) 的 map 是對的直覺，但真正的 O(1) 額外空間做法是把新節點**交錯塞進 next**：A→A'→B→B'→…；第二趟 `A'->random = A->random->next`（舊節點的 random 的「下一個」正好是它的複製品，**這就是那張 map，只是存在輸入裡**）；第三趟拆開並還原原鏈。這正是 `Algorithms/Design_Principles/In_Place_Marking.md` 的「把輸入當作輔助空間」，只是載體從陣列的正負號換成**指標欄位**——挑載體的判準一樣是「原值能不能還原」，next 能（拆的時候寫回去），所以可行。三趟 O(n)、額外空間 O(1)。
- 138（要不要真的寫 O(1)）：**不用寫，但要能口述。** 面試的期待答案就是 hashmap 版；交錯法是 follow-up，而且它**破壞輸入**（真的要寫之前得先問面試官「可以改原鏈嗎」）。優先級：**one-pass lazy-create > 交錯法**——前者能遷移到 133 Clone Graph、tree/graph 反序列化這一整類「前向引用」問題，後者基本上只服務這一題。

---

## 2026-09-20

- 74. Search a 2D Matrix
- 78. Subsets
- 128. Longest Consecutive Sequence
- 133. Clone Graph

**心得**：
- 128：**覺得做出 time O(n) 太難了**。自己推到「排序 O(n log n) → 要打敗它就不能用比較排序 → 雜湊」就卡住，最後看 tag 提示做 hashmap + connected component（DFS 找最大連通分量）。答案對，但執行時間很差。[14m 21s → 20m 58s]
- 78：自己寫的是「每個元素選 / 不選」的二元遞迴，解答是「用不同的起點探索新的子問題」。takeaway 只有一個——**`first` 的真正身分不是「起點」，是不變量的守衛。它存在的理由是防止重複，不是為了切子問題。**

**LLM 點評**：
model: Opus 5 (1M context)
- 128（為什麼慢）：複雜度標 O(n) 沒錯，但常數極大：**兩個 hash 容器**（每個節點約 4 次雜湊：`visited.contains` + `insert` + 兩次 `cache[...]`）、**遞迴深度等於序列長度**（`[1..1e5]` 會遞迴十萬層）、**index 根本沒用到**（`cache` 存 value→index 又繞回 `nums[index]` 取原值，真正需要的只是「值的集合」）。
- 128（潛在 bug，碰巧沒爆）：`cache[nums[i] + delta]` 用 `operator[]`，**找不到 key 時會預設插入 `key:0`**，於是遞迴到 `index 0`，同時讓 map 長到約 3n。之所以答案還是對，是因為最外層第一件事就是 `dfs(nums, 0, ...)`，`nums[0]` 在一切開始前就被標記，那條 fallback 永遠 return 0 ——**換個遍歷順序就會錯**。該用 `cache.find()` / `contains` 擋掉。（隨機兩萬組測試確認目前版本輸出正確。）
- 128（真正的解法：只從起點出發）：不需要 DFS、不需要 union-find、**不需要 `visited`**。`unordered_set` 裝所有值，然後 `for (int x : s) { if (s.count(x-1)) continue; int len=1; while (s.count(x+len)) len++; ... }`。**整題只有 `if (s.count(x-1)) continue;` 這一行是關鍵。** O(n) 的理由：`x` 是某段的起點 ⟺ `x-1` 不在集合裡，每段只有唯一一個起點，所以每個值一生只被「它自己那段的起點」走過一次。
- 128（這就是三天前寫的錨點心法）：起點 = **沒有前驅的元素**，是由結構本身決定、不是我們挑的錨點 → `Divide_and_Conquer/08_Canonical_Anchor_Decomposition.md`。對照：自己的版本**每個元素都當起點試一次**，產生重複工作再靠 `visited` 善後；錨點版本讓重複工作**根本不會發生**。那篇的那句話原封不動適用：**「不需要檢查」永遠優於「檢查得很周全」。** 與 42 two-pointer、45 壓縮 BFS 同一條線——**把檢查換成結構保證**。
- 128（下次怎麼自己走到）：推導鏈只有四步，已經走到第三步了 —— (1) 排序版 O(n log n) ✅ (2) 要打敗它 ⟹ 不能比較排序 ⟹ 雜湊 ✅ (3) 最直覺的雜湊版「對每個 x 往前走 x+1, x+2…」其實是 **O(n²)**（`[1..n]` 每個起點都走完全程）(4) **問「哪些工作是重複的？」→ 同一段被走了 k 次 → 只讓起點走 → O(n)**。**在第 3 步看到 O(n²) 就去翻 tag 了，而 tag 給的 union-find 是一條又對又繞的路。卡住時該問的不是「該用什麼資料結構」，是「哪些工作重複了」**——跟 42 從 prefix/suffix 推到 two-pointer 是同一個動作（當時自己的總結：「Duplicate 的 work 在持續找最大的人」）。
- 78（兩個版本的名字 repo 已經有了）：自己的版本是 `Backtracking/01-Backtracking_Templates_and_Patterns.md` 的**模式 A：解在葉節點**，解答是**模式 B：解在所有節點**（那篇舉的模式 B 例子正是子集）。量化差別：A 的樹有 `2^(n+1) - 1` 個節點、**一半是純路過**；B 恰好 `2^n` 個節點、**每個節點都是一個解，零浪費**。兩者都是 Θ(2ⁿ·n)，瓶頸在複製 `path`。
- 78（兩者都不會重複，但機制不同）：A 是「每個元素恰好被決策一次」→ 子集 ↔ 位元向量一一對應；B 是「選取的索引嚴格遞增」→ 每個子集只有一種遞增寫法。**都是結構上不可能重複，所以都不需要去重 guard** —— 對應 `07-Guards_from_Invariants.md` 去重型表格裡 78 那一列。
- 78（該優先記哪個）：**B 是通用形狀，A 是特例。** 判準：**A 只在「每個元素獨立地選或不選」時才寫得出來；一旦候選變成「從一個集合裡挑下一個」，二元形式就不存在**（46 排列、131 切回文、39 可重複選、77 要剪「剩下的不夠湊滿」都只有 B）。**78 是少數兩種都寫得出來的題**，這是它當子集原型題的價值。反過來，A 有 B 沒有的長處：簽章 `f(i)` 直接就是 DP 的狀態，是通往背包 / 股票那一類的橋（見 72 的零件對照表）。
- 78（不變量讀法的立即兌現）：**39 Combination Sum 遞迴傳 `i` 而不是 `i + 1`。** 用「起點」讀會以為是隨手的 off-by-one；用「不變量」讀，它是規格變更——不變量從**嚴格遞增**放寬成**非遞減**，因為允許重複選同一個元素。`first` 怎麼傳由「要維持哪條不變量」決定，不是由「下一個子問題從哪開始」決定。
- 78（解答 code 的瑕疵）：`void backtrack(int first, vector<int> curr, ...)` 的 `curr` **傳值**，每次遞迴整份複製 O(n)，應該是 `vector<int>&`（push/pop 紀律它已經有了）。量級不變但是白付的常數，而且傳值版同時依賴「複製」和「pop_back」兩套機制維持正確，語意是混的。自己的版本用 `vector<int>& path` 是對的。另外 `space: O(n), call stack` 正確，但照 LC 2 / 57 的慣例要註明「**額外**空間 O(n)，輸出 O(2ⁿ·n)」。

---

## 2026-09-19

- 62. Unique Paths
- 72. Edit Distance
- 73. Set Matrix Zeroes

**心得**：
- 72：從 brute force / backtracking 去想，得到 choice（choice 就是查表）。發現有重複子問題，就推進到 dynamic programming。
  - 想問：**backtracking 的 choice 推往 dynamic programming 的查表方向**，這個概念連結是對的嗎？
- 73：**space O(1) 的最佳化沒有做出來**——想到把 0 的紀錄吸收進 matrix 本身，也選了「最後一列 + 最後一行」當標記區，但整個矩陣照掃，結果錯了。in-place 的關鍵心法沒有學下來：
  1. **標記區 ∩ 掃描區 = ∅？** 否則分不出資料與標記
  2. **有沒有哪一格身兼兩職？** 有就拉一個 flag 出來
  3. **消費標記的順序，會不會先毀掉還沒用到的標記？** 用遍歷方向化解
  - 一句話：**in-place 標記的頭號陷阱，是資料區和中繼資料區重疊了。**
  - 先記下來，之後再練一次。今天先這樣。

**LLM 點評**：
model: Opus 5 (1M context)
- 72（概念連結對不對）：**方向完全對，但「choice 就是查表」少了一層**。查表取代的是**遞迴呼叫**，不是 choice 本身。正確的對應是：**函式參數（state）→ 表的索引**、**回傳值 → 格子內容**、**每個 choice → 轉移式中 `min/max` 底下的一個項**、**遞迴呼叫 → 查表**、**base case → 邊界初始化**。差別的實用價值：**寫不出表的維度時，該回去看函式簽章，不是選擇清單**——維度來自 state，項數才來自 choice。已把這張零件對照表補進 `Dynamic_Programming/Fundamentals/02-Problem_Solving_Framework.md`。
- 72（repo 早就寫過）：這條推導是 repo 既有的主線，不需要新開一篇 —— `Fundamentals/02-Problem_Solving_Framework.md` 的「決策選擇視角」就是它，`State_Design/01-Essentials.md` 的「**問題狀態 vs 決策空間**」更是它的精確版（含「試金石測試」：固定 `index` 只改 `k`，答案會不會變？會 → `k` 是狀態維度；不會 → 只是路徑累加器）。
- 72（真正缺的那塊：什麼時候跳不過去）：兩篇都沒寫**前提**，今天補上了——**遞迴的回傳值必須是可聚合的純量**。枚舉並收集所有解的 backtracking（22、46、78）**不能記憶化**，因為答案本身的大小就是指數級，快取只是把指數級的東西存起來。判準一句話：**問「有幾種 / 最少幾步 / 最大值」→ 跳得過去；問「列出所有解」→ 跳不過去。** 同一道題換個問法就會換邊。
- 73（為什麼錯）：反例 `[[1,1,1],[1,0,1],[1,1,1]]` —— **原始的 0 在正中央，完全沒碰到最後一列/行，照樣錯**。兩個獨立的 bug：(1) **標記寫進了還要繼續掃描的區域** → 迴圈走到 `(1, n-1)` 時看到的 0 是自己剛寫的標記，卻被當成原始資料，於是又去標記別的東西，**標記像傳染病一樣擴散**；(2) **角落 `matrix[m-1][n-1]` 身兼兩職** —— 它同時是 row `m-1` 和 col `n-1` 的標記，宣告一個就連帶宣告另一個（`[[1,0],[1,1]]` 死在這條）。修法：標記改放第 0 列/第 0 行、**第一趟只掃 `(1..m-1, 1..n-1)`**、角落的第二職用一個 `bool firstColZero` 接走、**第二趟由下而上**讓標記線最後才被覆蓋。已對 3×3 以內所有 0/1 矩陣窮舉驗證通過。
- 73（那句被自己劃掉的話其實是對的）：「用 reverse traversal」是對的，後來劃掉了。第二趟**必須**由下而上——標記在第 0 列，正向會在處理 row 0 時把整排 column 標記抹掉。這是 LC 57 同一條規則的再現：**寫出去之前，先確認沒有人還要讀它。**
- 73（抽出來的通則，已寫成筆記）：`Algorithms/Design_Principles/In_Place_Marking.md`。核心是一句話——**原地標記的本質是每一格要同時存「原值」和「標記」，所以先問這一格的表示能力有沒有多餘的部分可以挖**：值域非負 → 借正負號（442/448/41）；值域有上界 → 取模編碼（289 Game of Life）；值域=索引域 → 直接搬位置（41/268）；**都沒有** → 才犧牲一條線（73），並付出三項檢查的代價。關鍵判準是**標記與原值能不能靠編碼分辨**：能分辨（負數一定是標記）就隨便掃；不能分辨（`0` 既是資料也是標記）才必須靠**區域分離**，於是掃描範圍、身兼兩職、消費順序三件事全部浮現。另附「不屬於這一類」的對照（283/26/189 只是原地重排，沒有一格兩義，用不上這三項檢查）。

---

## 2026-09-18

- 45. Jump Game II（續昨天，自己推出 O(n) 壓縮版，31 分鐘）
- 42. Trapping Rain Water
- 49. Group Anagrams
- 55. Jump Game
- 57. Insert Interval

**心得**：
- 45：extreme compressed BFS。(1) 用 **next level 的 index**（`farthest`，需持續更新）以及 **current level 的 index**（`levelEnd`），來分別取代 queue 的 **push** 跟 **pop**；(2) 用 current level 的更新來表示進到下一個 level，藉此計算 distance。這個真的太神了，沒遇過這麼硬的狀態壓縮問題。
- 42：一路從 brute force → prefix/suffix max → two-pointer 推導過來。關鍵設計是用 `leftMax` 跟 `rightMax` 的比較去取代掉 `min(L, R)`，把 duplicate work 清除；除此之外還要搭配 two-pointer 的 invariant 設計。超級難，今天沒力寫 monotonic stack 了，先記錄下來，安排後面練習。
  - 自己的總結：**Duplicate 的 work 在持續找出最大的人，但是其實我們不用馬上找到。只要一邊有持續推進，另一邊只要保留最大值的下界就好。**
- 49：用 hashmap + sort 秒殺，但 best conceivable runtime 是 O(nk)（n 是清單長度、k 是字串長度）。想知道需不需要做一次 counting sort。
- 57：一開始檢查的時候忽略了一個可能性——插入後，後面的 interval 可能會被一路 merge，所以插入當下要 check merge，後面每個也要 check merge。另外不懂為什麼要強調 binary search 的解法。
- 55：可能是因為今天有做 Jump Game II 的關係，腦袋會去記得「最遠可以到哪」，所以自然就設計得出來。想問這種紀錄最遠的做法，概念上算是什麼？也是一種 BFS 可達性的簡化版嗎？（解答是寫 greedy）

**LLM 點評**：
model: Opus 5 (1M context)
- 57（code review）：正確，五個 case 都過（前插、後插、一路吞併、空輸入、恰好接觸 `[1,3]+[3,5]` 要合併）。結構上漂亮的地方：**把「新區間」和「剩下的舊區間」丟進同一個 `insertMerge`**，所以心得裡那個「插入後可能一路 merge」的情況不需要特別處理，自動被同一條路徑吃掉——**消除特例，而不是為特例加分支**。小記：`space: O(1)` 要註明「**額外**空間 O(1)，輸出 O(n)」（同 LC 2 那條）；`insertMerge` 第二個參數可以是 `const vector<int>&`。
- 57（為什麼強調 binary search）：**先算 BCR 就知道答案 — BCR 是 O(n)，因為必須輸出最多 n 個區間。** 所以 `O(log n)` 找插入點 + `O(n)` 輸出還是 `O(n)`，**binary search 不可能改善這題的總複雜度**；說「用二分更快」是錯的。教材提它的兩個真實原因：(1) 它是「input 已排序」的標準反射，面試官想確認你**注意到**這個前提——要能說出「我知道可以二分找插入點，只是輸出本身就 O(n)，所以不影響總複雜度」，這句展示的是複雜度判斷力；(2) **它通往動態版本**——follow-up 是「如果要連續插入 m 個區間呢？」，每次掃 O(n) 就變 O(mn)，正解是把區間存在**有序容器**（`std::map`，key 是起點）：二分找受影響的那段 → 刪掉被吞併的 → 插入合併後的，每次 `O(log n + k)`，且每個區間一生只被刪一次 → 均攤 O((n+m) log n)。這條線是 **LC 715 Range Module**、**729/731/732 My Calendar I/II/III**。**binary search 在 57 是多餘的，但它是那些題的地基。** 結論：要能講出「為什麼不需要」以及「什麼時候就需要了」，這兩句比寫出二分版本值錢。
- 55（「紀錄最遠」算什麼概念）：**直覺完全正確，而且今天剛寫的 `BFS/05-Frontier_Compression.md` 已經預言了這題** — 它的階梯表裡，45 在「兩個整數（層邊界）」那一階，55 在「一個整數」那一階。45 需要 `levelEnd` + `farthest` 兩個數是因為要**數層數**；55 只問可達性、不問幾步，**層的概念整個消失**，`levelEnd` 跟著消失，只剩一個 `farthest`。**55 是 45 再壓一階。**
- 55（三種等價說法，第三種最機械）：BFS 視角 = 可達集合是前綴、前綴只需一個右界；Greedy 視角 = 官方標籤，但跟 45 一樣是**壓縮後的外觀**而非思路來源；**Running prefix max 視角** = `farthest` 就是 `max_{k ≤ i}(k + nums[k])`，也就是一個 prefix max。第三種最值得記，因為它把整題化約成一句話：**計算 `k + nums[k]` 的 prefix max，檢查它在每個位置都沒有落後於 `i`** — 這就是 repo 的 Running State Pattern（`Prefix_Sum/02_Running_State_Pattern.md`），`farthest` 是 running state，`max` 是它的結合運算。
- 55（break 條件的真身）：整段程式的不變量只有一條 `I: i ≤ farthest`（目前這格是可達的）。寫的 `farthest == i` 代表下一圈就要違反 `I`——**這正是 `07-Guards_from_Invariants.md` 說的：guard 不是邊界條件，是不變量的守衛**。（另一個 `farthest >= n-1` 只是提前退出的優化，拿掉也正確。）推導鏈完整版：**可達性問題 → BFS → frontier 是前綴 → 壓成一個右界 → 看起來像 greedy**。能講出這條鏈比說「這是 greedy」強得多，因為前者解釋了為什麼正確，後者只是分類。
- 49（要不要 counting sort）：**要，但理由不是「更快」，是「它是 BCR」** — 而且實務上它未必更快，這個矛盾正是這題能講的東西。概念升級：**你要的不是排序，是 canonical form（正規形式）** — `sort(word)` 只是讓同一組 anagram 映射到同一代表的**其中一種手段**；計數陣列是另一種，而且更直接（跳過「排出順序」這個中間步驟）。key 可以是 26 格計數：`string key(26,'0'); for (char c : word) key[c-'a']++;`，O(k) 建 key、總計 **O(n·k)** = BCR。
- 49（為什麼未必更快）：排序 key 每字 `k log k`，計數 key 每字 `26 + k`。題目 `k ≤ 100` ⟹ `log k ≤ 7`，交叉點約在 **k ≈ 12**，**短字串用排序反而快**（排 3 個字元 vs 開 26 格）。真正的複雜度是 `O(n·(k + Σ))` vs `O(n·k log k)`。面試話術：先寫排序版（三行、不會錯），再主動補一句「字母表固定 26 所以可換成計數變 O(nk) 即 BCR，但 k ≤ 100 時 log k ≤ 7 而計數要付 26 的常數，短字串排序反而快」——**展示取捨判斷比直接寫計數版更值錢**。
- 49（計數 key 的經典 bug）：用數字串接當 key 時 `[1, 11]` 和 `[11, 1]` 會產生同一個 `"111"`。**必須加分隔符**（`"1#11#"`）或用固定長度的字元陣列。這是這題最常見的錯誤。
- 42（三個解法的推導路徑）：卡在暴力法的原因是**選錯分解方式** — 原本用「逐區段」（從 i 找下一根夠高的柱子），那其實是**單調棧解法的雛型**，不是暴力解的思路，難怪難寫。暴力解是**逐格**：`water[k] = min(左邊最高, 右邊最高) - height[k]`，負的當 0。把這條 `ANSWER` 式子寫下來，後面全是機械的：哪一項被重複算了？→ `maxLeft`/`maxRight` 每格重算 → BUD 的 **D** → prefix/suffix 陣列（跟 238 的 prefix/suffix **乘積**是同一個動作，這裡換成**最大值**）。**這是 45 踩過的同一個坑**：跳過「先寫答案的定義式」，直接進到一個聰明但難寫的框架。另外附帶一個有趣對照：暴力版的 `if (bar > height[i])` 是**擋得到**的 guard（`[1,5,1]` 會觸發），跟 19 / 22 那兩個 dead guard 剛好相反 — 判準一樣，問「什麼路徑會讓它成立？」，這裡答得出來。
- 42（two-pointer 的關鍵引理）：不需要 `R` 的精確值，只需要「`R` 至少多大」的**下界** — 若已知 `L = 3` 且確定 `R ≥ 5`，`min(3, R) = 3`，R 是 5 還是 100 都一樣。下界哪來？從右端往左走，一路看到的最大值就是合法下界。不變量：`leftMax == max(height[0..left])`、`rightMax == max(height[right..n-1])`、`left 的真右最高 ≥ rightMax`、`right 的真左最高 ≥ leftMax`。引理：**若 `leftMax < rightMax`，`left` 這格的水 = `leftMax - height[left]`，與中間那一大段長什麼樣完全無關**（真右最高 ≥ rightMax > leftMax ⟹ 取 min 時左側必勝）。每輪安全淘汰較矮那側的一格 → 標準的雙指針單調淘汰，與 **LC 11** 同構。
- 42（三個訂正）：(1) 「等號因為差值就是 0，所以放哪個判斷都可以」— **結論對但理由錯**：`leftMax == rightMax` 時差值不一定是 0（`[2,1,2]` 走到 `left=1` 時是 1）。真正的理由是**相等時兩邊都滿足「自己是較小的那個」，所以兩個分支都合法**；這個理由同時解釋了不相等時為何**只有一邊**能結算。(2) **為什麼最後一格不用結算**（面試會問）：兩指標相遇那格必定是全域最高之一，水量為 0，所以 `while (left < right)` 漏掉它是安全的。(3) `leftMax = 0` 的初值**依賴「高度非負」**這個約束，值得記進 `LIMIT`。
- 42（可脫離本題的通則）：**當運算是「取 min / 比大小」時，不需要精確值，只需要足以決勝負的下界。** 這是 O(n) space → O(1) space 那一類優化的通用鑰匙，不只這題。
- 45（推導過程）：昨天卡住的那一步今天自己走出來了，關鍵是把定義寫死再動手。最準的一句是自己寫的：**「`farthest` 就是原本 queue 內存的狀態」** — queue 裡那一堆 index，唯一被用到的資訊就是「它們合起來能摸到多遠」，所以整個 queue 塌縮成一個數字。這句精確地命名了「狀態壓縮」的實質。過程中修掉的一個關鍵誤解：`levelEnd` **不是** `i + nums[i]`（那是單格），而是**這一層所有成員 `i + nums[i]` 的最大值**；`farthest` 和 `levelEnd` 是同一個量的兩個時間點——前者正在長，後者已封存。
- 45（不變量）：`I1: i ≤ levelEnd`、`I2: distance == 到達 i 的最少步數`、`I3: levelEnd == 用 ≤ distance 步能到的最遠位置`。`I2` 是靈魂，其餘都是推論：`i == levelEnd` 時必須結算（否則違反 I1），而 `farthest` 必須在該判斷**之前**更新（因為 `i` 自己也是當前層成員）。
- 45（最終優化，Gary 自己提的方向）：把迴圈縮到 `i < n - 1` 之後，**連檢查都不用做**——`if (farthest >= n-1) break`、`n == 1` 的 guard、`distance + 1` 的 off-by-one **三個同時消失**，直接 `return distance`。理由是 `I2` 自然延伸一格：`n-1` 與 `n-2` 同層時不觸發換層、`distance` 不變；`n-1` 在下一層時此刻 `levelEnd == n-2`、剛好 +1。**`n-2` 不是技巧，是不變量的後置條件。** 這是這幾天反覆出現的同一主題：**把邊界吃進迴圈條件，比額外寫 guard 更不容易錯**（LC 2 的 `while (l1 || l2 || carry)`、LC 22 的 dead guard 都是同一件事）。
- 45（面試會追問）：現在這版依賴「題目保證可達」。拿掉保證後的破口是 **`levelEnd` 停止前進**——某層的 `farthest` 沒超過 `levelEnd` 就代表跳不出去。能口頭講出這句就夠，不用真的寫。

---

## 2026-09-17

- 19. Remove Nth Node From End of List
- 22. Generate Parentheses
- 45. Jump Game II

**心得**：
- 19：直覺是先算 size，再算 `n - k + 1` 個 gap 的 pointer，這樣需要 two-pass；follow-up 是 one-pass，直覺想到用遞迴可以做。另外發現自己一個很嚴重的問題：有些題目會**直接跳進去解法**。
- 22：不知道為什麼判斷式可以簡化成只看 solution 長度 = `2 * n`。這題感覺最沒把握的就是 boundary condition 的設計。
- 45：用 DP 做出來了（forward push 式，`O(n^2)`）。想知道有沒有 follow-up。後來自己推到 BFS 分層版（一開始 `distance++` 放錯位置，改成 `q.size()` 快照後正確）。但看了 O(n) 解法之後，怎麼想都還是覺得很難，不知道自己到底 miss 什麼。

**LLM 點評**：
model: Opus 5 (1M context)
- 45（code review）：正確。三個短評：(1) `j` 從 0 開始是無效迭代（`steps[i] = min(steps[i]+1, steps[i])`），從 1 開始更誠實。(2) **sentinel 選 `10001` 選得好** — 這是 322 那次 `INT_MAX` 溢位教訓的正確應用：用「比任何合法答案都大、但不會溢位」的有限值。(3) `LIMIT` 那格寫的是**移動規則**（`0 ~ nums[i]`）不是題目約束；這題最該記的是**「保證一定能到達最後一格」**，正因為有它才不用處理回傳 −1。
- 45（「有 followup 嗎」— 框架要先糾正）：**O(n) 解法不是 follow-up，它是正解；你寫的 DP 是 brute force。** 面試出 45 幾乎必然要走到 O(n)，那是及格線不是加分題。心法一句話：**它就是 BFS 分層，只是不需要 queue**——因為只能往右跳，「走 k 步能到的位置」永遠是一段**連續區間**，既然是區間就只要記邊界、不必存節點。`jumps` 就是 BFS 的層數，而 BFS 層數 = 最短步數，這就是 greedy 為什麼正確的證明，不需要另外做交換論證。唯一的坑是 `for (i = 0; i < n - 1; ++i)`：走到最後一格時若剛好 `i == curEnd` 會多算一步。用 BUD 看：DP 的瓶頸是「每個 i 都重新枚舉所有落點」，但落點是連續區間，**只需要知道邊界** → O(n²) → O(n)。
- 45（BFS 分層的錯誤）：`distance++` 放在每 pop 一個節點就加一，數的是「處理過幾個節點」不是 BFS 深度。修法是**層要用 `q.size()` 快照**：`int sz = q.size();` 必須在迴圈外先取（推入新節點後 `q.size()` 會變），整層處理完才 `++distance`。等價寫法是不用單一計數器、改存每個節點的距離 `dist[i+j] = dist[i] + 1` — **距離跟著節點走，而不是跟著時間走**，就沒有「什麼時候加一」的問題。兩種都要會。
- 45（「我到底 miss 什麼」）：**miss 的不是觀察** — 註解裡已經寫了「只要紀錄第一個跟最後一個」，那句就是答案。卡住的是觀察之後的**改寫動作**：BFS 有兩層迴圈（層 × 層內成員），O(n) 版只有一層。壓縮之所以難想，是因為它依賴一個很安靜的事實：**所有層首尾相接、不重疊、剛好鋪滿 `[0, n-1]`**，所以「逐層、層內逐個」展開就是 `0..n-1` 一路掃——**兩層迴圈不是被優化掉的，是被攤平的**。攤平後「層的邊界」從**結構**（迴圈範圍）退化成一個**比較**（`i == curEnd`），原本看得見的東西變成看不見的，這就是它讀起來像魔法的原因。這個手法本身就少見。
- 45（標籤誤導）：**這題根本不是 greedy。** greedy 的故事（「每次選能跳最遠的」）需要交換論證才站得住，很多人講不清楚；**它的真身是 BFS，greedy 外觀是壓縮後的副產品**。一直想把 greedy 想通所以想不通——那個方向本來就是事後合理化。自己推到 BFS 分層，方向完全正確。
- 45（處置：這題屬於「背形狀」）：有一小類題目正解是**壓縮形式**，沒有人在面試現場重推——45、Boyer-Moore（169 已接受過一次）、Morris traversal、三路快排。正確做法是**形狀背起來 + 能講出正確性論證**。形狀：`farthest` = 這一層能摸到的最遠、`curEnd` = 這一層的右邊界、撞到 `curEnd` 就步數 +1 並把 `curEnd` 推到 `farthest`、掃到 `n-2` 為止。口訣：**「掃過每一格，累積最遠；踩到邊界，換層加一」**。正確性論證一句話：**`jumps` 是 BFS 的層數，BFS 層數 = 最短步數** — 面試講這句就夠，不需要交換論證。
- 45（想要直覺就換題目外衣）：翻譯成**最少區間覆蓋** — 每個 `i` 給一個區間 `[i, i + nums[i]]`，問最少幾個區間能從 0 接龍覆蓋到 `n-1`。這個外衣下貪心非常自然：**在所有「起點已被覆蓋」的區間裡挑右端最大的**（選右端小的絕不會更好）。同一個演算法但直覺順很多。**LC 1024 Video Stitching 和 1326 Minimum Taps 就是這題換皮**；覆蓋視角比較順的話，做完那兩題再回頭看 45 會突然變簡單。
- 45（真正的 follow-up）：**55 Jump Game**（只問能不能到，維護一個 `farthest`）；🔥 **1306 Jump Game III**（可左可右 → **區間性質破裂**，可達集合不再連續，必須老實用 queue 做 BFS）；**1345 Jump Game IV**（可跳到任何相同值的位置，BFS + 值分組 + 用完清空該組）；🔥 **1696 Jump Game VI**（求最大分數，同一個 DP 骨架但瓶頸變成「區間最大值」→ 單調佇列）。**1306 最值得做**，因為它精準回答「為什麼 45 可以不用 queue」：只能往右 ⟹ 可達集合是區間 ⟹ 只記邊界；可左可右 ⟹ 區間性質消失 ⟹ 退回真正的 BFS。**同一個問題換一個移動規則就換一種資料結構**，這個對照比多刷五題有用。口頭 follow-up 兩個常見：「要回傳路徑？」（記 parent）、「如果不保證能到達？」（`curEnd` 卡住不前進就回 −1）。
- 22（為什麼 `size == 2n` 等價）：**不是「簡化」，是把 guard already 保證的東西省略不寫。** 兩個 guard 各維護一條不變量：`if (left < n)` ⟹ 恆有 `left ≤ n`；`if (left > right)` ⟹ 恆有 `right ≤ left ≤ n`。又 `solution.size() == left + right`，所以 `left + right == 2n` 且兩者各 `≤ n` ⟹ **只可能兩個都打滿** ⟹ `left == right == n`。你那版把條件寫明白反而更誠實；面試時兩種寫法都行，能講出這段推導才是重點。
- 22（「boundary condition 沒把握」的解法）：反過來想——**backtracking 的 guard 不是「邊界條件」，是不變量。邊界條件靠猜，不變量可以推。** 先寫兩行：`I1: 0 ≤ left ≤ n`（左括號不超過 n）、`I2: right ≤ left`（任何前綴的右括號不多於左括號 ← 這就是「合法」的定義）。剩下全部機械：加 `(` 前檢查加完 I1 還成立 → `left < n`；加 `)` 前檢查加完 I2 還成立 → `right < left`；答案 = I1、I2 都飽和 → `left == right == n`。三個條件沒有一個是猜的。**下次沒把握就做這個動作：先寫不變量，guard 從不變量倒推。**
- 22（code review）：(1) **`if (left > n) return;` 是 dead code — 昨天 LC 19 的同一個毛病**。已經有 `if (left < n)` 才遞迴，`left` 不可能超過 n。連續兩天寫出擋不到的防禦，記一條規則：**防禦性 guard 出現時先問「什麼路徑會讓它成立？」答不出來就刪掉**。註解寫 `// base case` 也不對，真正的 base case 是下面收集答案那個分支。(2) **`LIMIT` 寫 `n/a` 錯過重點** — 這題約束是 `1 <= n <= 8`，這個小到誇張的上界正是在說「指數級枚舉就是預期解法」。LIMIT 欄位的價值不只「禁止了什麼」，也包括**規模暗示該找什麼量級的解**（若寫 `n ≤ 10^5`，枚舉整個方向就錯了）。(3) `solutions` 是成員變數且是**累積**的，物件被重用時上一組答案會留著（比 543 的 `best` 更嚴重，`n` 因每次重新指派所以沒事）；入口加 `solutions.clear();` 即可。做得好：`string& solution` + `push_back`/`pop_back` 是正確的 backtracking 寫法（傳值複製會變成 O(n) × 指數）。複雜度可更精確：每個完整解要 O(n) 複製進 `solutions`，時間 **O(n · Catalan(n)) = O(4ⁿ/√n)**，空間 O(n)**（不含輸出）**。
- 19（code review）：正確，`n=1,k=1`、刪頭、刪尾三個邊界都對。四點：(1) **`prev` 是多餘的** — 關鍵是走到「要刪的**前一個**」而不是走到「要刪的」再回頭，`for (int i = 0; i < n - k; ++i) prev = prev->next; prev->next = prev->next->next;` 就結束了。dummy 存在的唯一理由就是讓「前一個」永遠存在（刪頭時前一個是 dummy），你用了 dummy 又維護 `prev`/`ptr` 一對指標，等於把它的功能做了兩次。(2) **`if (prev && ptr)` 是 dead code** — 題目保證 `1 <= k <= n`，這個 guard 永遠擋不到東西；面試時「擋不到的防禦」反而扣分，透露你對不變量沒把握，正確做法是把它**講出來**而不是寫成 if。(3) `k = n - k + 1` **覆寫參數**，同一個名字中途換語意（倒數第幾個 → 正數第幾個），二刷最容易看錯，給它新名字。(4) 你自己的註解底下寫了 `// k gap pointer // from the end of the list` — **答案已經在紙上卻沒用**；one-pass 的全部技巧就是那兩行字：兩個指標保持 k 的固定間距，前面撞到 null 時後面就在正確位置，這是「從尾巴數」轉成「從頭走」的機器。遞迴也能一趟但付 O(n) call stack，不是這題要的。
- 19（依序還是跳最佳解）：**面試一定依序，但 brute force 用 15 秒講完。** 面試官買的是「你怎麼從 A 走到 B」，不是 B。這題有個必須講出來的細節：**two-pass 已經是 O(n)/O(1) 最優複雜度**，follow-up 的 one-pass 不是漸進改善而是 pass 數的改善，只在「資料只能讀一次」（streaming、超大檔案、input 是 iterator）時才有意義 — 講得出這句話比寫出 one-pass 更值錢。**練習則是依序「想」、不必依序「寫」**：brute force 口頭成立就夠，手寫留給最佳解；例外是像 42 那種「同一題多解互相對照」本身就是教材的題。
- 19（「直接跳進解法」這個診斷要改）：翻 log — 543 搞錯 diameter 定義、238 沒讀出「不能用除法」、15 沒釐清輸入輸出格式、139 Trie 方向錯。四個裡有三個**不是選錯演算法，是還沒把題目寫成規格就開始選演算法**。選解法快是實力不是毛病；問題在選之前沒有一個能檢驗它的靶。**重新框：不是「太快跳解法」，是「在還沒立靶之前就開始射」。**
- 19（可執行的修正）：`Interview_Playbook/Problem_Solving_Process_and_Assumption_Checklist.md` 第 1 步「OBSERVATION：仔細觀察問題」執行不了 — 它沒有產出物，做完也不知道有沒有做。改成**必須留下三行字**（30 秒，寫在 code 上面）：`// IN/OUT` 輸入形狀/範圍/找不到回傳什麼、`// ANSWER` 一行話把「答案是什麼」寫死、`// LIMIT` 題目禁止了什麼/保證了什麼。套回舊坑：543 寫「答案 = 對某節點 v，左深+右深 的最大值」就不會以為要經過 root；238 寫 `ans[i] = 左邊全部乘積 × 右邊全部乘積`，prefix/suffix 是機械的下一步；19 寫「答案 = 刪掉第 `n-k+1` 個節點」就看得見 `n` 是唯一未知數，one-pass 的目標就是消掉它。**檢驗標準：寫不出 ANSWER 那一行，就代表還沒讀懂題目，這時想到的任何解法都是猜的。** 這也解釋了為什麼 brute force 不能跳過 — **暴力解是規格的可執行版本**，用途不是當優化起點，是確認「我理解的題目是對的」。

---

## 2026-09-16

- 136. Single Number
- 206. Reverse Linked List
- 242. Valid Anagram
- 543. Diameter of Binary Tree
- 2. Add Two Numbers

**心得**：
- 206：這次想 recursive 版本還是很久。可以用 post-ordering 來想，然後 post processing 就是更新 next pointer，這麼單純而已。
- 543：一開始就搞錯 longest path between two nodes（或者說是 diameter）的定義，我一直假設它會經過 root。但是因為它不一定會經過 root，所以必須在遞迴的過程中去記錄最大的 diameter，這時候就會多一個狀態。而這個狀態可以設計成 structure（也就是在這一個 class 底下），或者是在 function signature 內帶。不過我覺得在 function signature 內帶難寫多了，所以直接在 data structure 裡面帶。

**LLM 點評**：
model: Opus 5 (1M context)
- 206：「post-order + post processing 只是更新 next pointer」這個總結是對的，但可以再收緊一句，變成下次能直接套用的判準：**這題的回傳值從頭到尾沒有被計算過，它只是一路往上傳的「錨點」**。
  ```cpp
  ListNode* reverseList(ListNode* head) {
      if (!head || !head->next) return head;   // base case 就決定了最終答案
      ListNode* newHead = reverseList(head->next);
      head->next->next = head;                 // post-processing：只掉頭「我 → 兒子」這一條邊
      head->next = nullptr;
      return newHead;                          // 原封不動往上傳
  }
  ```
  想久的原因通常是**把兩件事混在一起想**：(1) 誰是新的頭、(2) 指標怎麼接。其實 (1) 在 base case 就定了（原串的尾巴），中間每一層都不碰它；每一層真正負責的只有 (2)，而且只負責**自己和兒子之間那一條邊**。一旦把「回傳值 = 不變的錨點」和「post-processing = 只處理本地那條邊」拆開，遞迴就沒有東西要想了。
- 206（`head->next = nullptr` 為什麼不能省）：除了原始 head 以外，每個節點的 `next` 都會被它的父層用 `head->next->next = head` 覆寫掉；唯一沒有父層的就是原 head，不清掉它就會和第二個節點互指形成環。寫在每一層是無害的冗餘，但這行的存在理由只有原 head 一個。
- 206（歸類）：這是 repo `Design_Principles/Recursion/05-Recursion_Signature_Contract.md` 裡沒收的第三種形態 — 回傳值既不是「算出來的」（110）也不是「撞到的」（230），而是**base case 決定、中間層純傳遞**。判斷方式：如果每一層都對回傳值寫 `return f(...)` 而不做加工，那個回傳值就是錨點，遞迴的實際工作全在 post-processing 那幾行。
- 2（要不要寫 recursive 版本）：**不用。** 這題的 recursive 只是把 `while` 換成尾遞迴，還多付 O(n) call stack，沒有任何 iterative 做不到的事——和 104/226 不同（那兩題是遞迴太快寫完、面試官要看你手動管 stack）。要練直接跳 **445. Add Two Numbers II**：高位在前且不准反轉 list，進位方向與走訪方向相反，非得用 stack 或遞迴不可（遞迴回溯的順序天然就是從低位往高位）。是「為了 445 學遞迴」，不是「為了 2 寫遞迴」。
- 2（Code review）：正確，邊界都吃乾淨（`[9,9] + [1]` → `[0,0,1]` 會過）。加分項：`ListNode head;` 放 **stack** 上，不像 `new ListNode()` 那樣會 leak，面試時值得主動講一句。兩個小改進：(1) `bool carry` 改成 `int carry` — 現在正確（進位最多 1，因 `9+9+1=19`），但 `int` 可以寫成 `int sum = carry; ... carry = sum / 10;` 少一個分支，而且**推廣時不會壞**（加 k 條 list 或非十進位時進位可能 > 1，`bool` 版要整個重寫）；順手把「取值」和「前進」併進同一個 `if (l1) { sum += l1->val; l1 = l1->next; }`，三組 `if` 變一組。(2) 註解只寫 time，補上 space：輸出 O(max(m,n))、**額外**空間 O(1)——把「輸出不算輔助空間」講清楚是小加分。
- 2（真正的考點在迴圈條件）：`while (l1 || l2 || carry)` 一行吃掉三種邊界——長度不等、一條先結束、最後還有進位。經典 bug 是漏掉最後的 `carry`（`[9,9] + [1]` 要得到 `[0,0,1]`）。跟 LC 5 學到的「把邊界拉進條件裡吃掉」同一個動作；carry 本身就是 running state（`Prefix_Sum/02_Running_State_Pattern.md`），配 dummy node（`Data_Structures/Linked_Lists/Dummy_Node_for_Insertion.md`）。
- 543：「不一定經過 root」這個觀察對，但它的**正解形式**不是「多處理幾種情況」，而是換一個枚舉方式：**任何一條路徑都有唯一的最高點（= 兩端點的 LCA）**。所以不要問「路徑經不經過 root」，改成**讓每個節點都當一次最高點**——走到 `v` 時，以 `v` 為最高點的最長路徑就是 `depth(left) + depth(right)`。每個節點輪一次，所有路徑不重不漏被涵蓋。這句話是通解，124、687、1522 原封不動照套。
- 543（「多一個狀態」的真正原因）：更精準的說法是**回傳值和答案本來就是兩個不同的量**。函式回傳的是「從 `v` 往下**單邊**的最大深度」——那是給父親接著用的；而答案是「以 `v` 為最高點的**雙邊**路徑長」——父親不需要它，所以它無處可回傳，只能往外部累積。看清這兩者不同，就不會再糾結「怎麼把答案塞進 return value」。這正是 repo `Design_Principles/Recursion/05-Recursion_Signature_Contract.md` 說的「答案是**撞到的**」形態（對照 206 是「base case 決定、往上傳的錨點」，110 是「算出來的」——三種形態這兩天剛好各碰到一次）。
- 543（成員變數 vs 參數）：兩種寫法其實是**同一個 pattern**（external accumulator），差別只在 reentrancy。成員變數的坑：某些判題設定會**重用同一個 Solution 物件**跑多組測資，上一組的 `best` 會留著 → 必須在對外入口顯式 `best = 0;`（就是 `Prefix_Sum/02_Running_State_Pattern.md` 講的 explicit reset）。另外「參數版難寫」這個感覺，通常來自想同時回傳深度和答案；只要接受 out-parameter `int depth(TreeNode* v, int& best)`，其實只多一個參數，不比成員變數難——面試時這版更能直接講清楚「誰在算、誰在累積」。
- 543（參數版的結論，Gary 自己收斂的）：外部變數**只被寫、不被讀**——沒有任何一層會根據它決定怎麼往下走，它純粹是個「信箱」。所以一路帶進 signature 的成本就只是多一個參數，沒有差。寫法：`int best = 0;` 宣告在**入口函式裡**，helper 收 `int&`。這比成員變數更好——局部變數每次呼叫天生是新的，reentrancy 問題自動消失，不需要 explicit reset（那行只有成員變數版才要）。⚠️ 必須是 `int&`；傳值的話每層拿到副本，更新全丟掉。
- 543（判準：什麼該下傳）：**會不會影響子問題怎麼算？** 不會 → 只是答案往上的信箱（543 的 `best`），帶不帶都對，順手帶著就好。會 → 是真正的下傳約束（98 的 `(min, max)` range、path sum 的累積和），少傳就錯。兩者在 signature 裡長得一樣，但一個是答案往上的通道，一個是約束往下的通道。
- 543（最常見的 off-by-one）：diameter 數的是**邊數**不是節點數。若 `depth` 定義成節點數（葉節點回 1），`left + right` 剛好就是邊數，不用 -1；若 `depth` 定義成邊數（葉節點回 0），`left + right` 也是邊數但每層的 +1 位置會不同。寫之前先把 depth 的定義講死，這題就不會卡在 ±1。
- 543（延伸）：**124 Binary Tree Maximum Path Sum** 是同一個模子的加強版——一樣枚舉最高點、一樣回傳單邊，只多一個 `max(0, child)` 把負貢獻砍掉。這兩題一起做，「枚舉 apex + 回傳單邊」這個套路就固定下來了。
- 206（延伸）：這題是 92 / 25 / 234 / 143 的地基，這些 follow-up 都是「反轉一小段再接回去」。接回去時必須抓住 **反轉前的頭 = 反轉後的尾**，所以會需要 dummy node 固定前驅（repo `Data_Structures/Linked_Lists/Dummy_Node_for_Insertion.md`）。迭代版 `prev/cur/next` 三指標也值得跟遞迴版並列記：遞迴是從尾巴往回接，迭代是從頭一路掉頭 — 同一件事的兩個方向。

---

## 2026-09-15

- 238. Product of Array Except Self
- 322. Coin Change
- 23. Merge k Sorted Lists
- 125. Valid Palindrome
- 169. Majority Element

**心得**：
- 238：寫得蠻糟糕的。一開始一直想到 Divide and Conquer，但實際上這題沒那麼複雜，用 Prefix Sum / Running Sum，概念其實很簡單。所以這題的關鍵是：沒辦法盲想到演算法的設計；關鍵的設計如果沒出來，後面就會卡住。
- 238（最大心得）：**要先釐清它的限制**。這題的限制是不能用除法——暴力解其實是先把全部數字乘一次、再除以自己（但要注意 0）。有了這個限制之後，才會去展開其他解法，進而考慮到 prefix sum 跟 suffix sum，然後才會有用 return value 和 running sum 去壓空間的概念。
- 322：這題很精彩。一開始還是會做成二維陣列，然後必須往前找到「所有可能的換法下最好的換法」。一開始就直接往前找 `dp[k-coins[i]]` 那個，想了一下不對——那整排 `dp[k]` 都要看看，找最小的。這版還沒去算那個。但想到那個算法之後，就可以直接整合成一維，因為只要記錄一個最小換法即可。
- 322（完成版）：最大的 take away 是——查表時腦中要分清楚 **state** 和 **choice/candidate**，才不會把 choice 變成 state；而且既然是 choice，就**都要查過**；然後如果只記錄最佳解，choice 對應的答案可以被**壓縮成一個值**來記錄。
- 23：最麻煩的是 (1) 暴力法不知道怎麼做——解答說直接取值出來排序、重新建 linked list，但我覺得怪怪的；(2) 時間複雜度很難分析。我的做法是 divide and conquer，時間 O(N log k)（k 是 lists 數量），空間 O(log k) 是 call stack。有趣的延伸：用 priority_queue 整理 `vector<ListNode*>`，時間剛好也是 O(N log k)；第二個延伸是 **bottom-up divide and conquer**，用長度 / interval 決定 combine 的項目，從長度 2 開始——對這個有興趣，之後回來練。
- 125：完成。我的寫法是單層 while + 三分支（跳左 / 跳右 / 比對）。解答用 for + 兩個內層 while，覺得滿複雜的，想知道這樣有什麼好處。
- 169：Boyer-Moore Voting Algorithm 很經典，但這題解法太多了。感覺這題應該是要考其他延伸？比方說 divide and conquer，覺得很值得寫。

**LLM 點評**：
model: Opus 5 (1M context)
- 238：「盲想不到關鍵設計」這個診斷可以更具體——**這題的設計是被「不能用除法」這個約束逼出來的，不是靈感**。想到 prefix 的路徑是機械的：`ans[i] = (左邊全部乘積) × (右邊全部乘積)`，而「某一側的全部乘積」就是 prefix/suffix product。所以流程是**先寫出答案的定義式，再看式子裡哪一項可以預先算好**——這跟 DP 的「先定義 state 再找遞推」是同一個動作。會滑向 D&C 是因為看到「每個位置都要一個答案」就想切分治，但 D&C 需要「子問題的解能合併成父問題的解」，這題沒有那個結構（跟你 09-07 在 LC 11 判斷「有沒有單調淘汰 → 才是雙指針」是同一類判準）。repo 對應：`Prefix_Sum/01_Prefix_Sum_Intro.md`、`02_Running_State_Pattern.md`；另外這題正是 BUD 的 **D（Duplicated work）**——暴力解每個 i 都重算一次左右乘積，prefix 就是把重複的部分存起來。
- 322：**貼的這版會給錯答案**，不只是「還沒算那個」。轉移 `dp[k][i] = min(dp[k][i], dp[k-coins[i]][i] + 1)` 右邊固定在同一個 `i`，所以 `dp[k][i]` 的語意變成「**只用第 i 種硬幣湊出 k**」。`coins=[1,2,5], amount=11` → `dp[11][0]=11`、`dp[11][1]`、`dp[11][2]` 都是 MAX，取 min 得 **11**，正解是 3（5+5+1）。你說的「整排 `dp[k]` 都要看」正是修法：右邊要跨所有硬幣取最好的。
- 322（維度為何會消失）：關鍵在**狀態 vs 選擇**——你自己的註解寫對了（`state is the "amount"` / `coins is the "choice"`），但下一行又寫 `array is n * k` 把選擇當成了維度。硬幣可無限重複使用，所以「上一步用了哪種硬幣」對未來沒有影響，不需要被記住；真正的狀態只有「還剩多少金額」。一旦轉移改成跨所有硬幣取 min，`i` 這個維度就自動消失 → `dp[k] = min(dp[k - coins[i]] + 1)`。對比 0/1 背包（416、494）：每個物品只能用一次，「處理到第幾個物品」**必須**進狀態，維度就消不掉——這是完全背包 vs 0/1 背包最本質的差別。repo：`Checklists/Trick Practice/Knapsack_Variations_Playbook.md`、`DP/State_Design/01-Essentials.md`。
- 322（小處）：`NOT_CHANGEABLE = INT_MAX` 逼得你必須先擋 `== NOT_CHANGEABLE` 才能 `+1`（否則溢位）。改用 `amount + 1` 當 sentinel（合法答案最多 `amount` 枚）就不用那個 guard，`min` 直接寫——跟你 09-04 在 LC 5 學的「把邊界拉進 base case 吃掉」同一個想法。
- 322（完成版點評）：最終版正確（`coins=[1,2,5], amount=11` → 3）。你的 take away 很準，補一條可直接套用的判準：**「這個 choice 會不會改變未來可用的選項？」** 會 → 必須進 state（0/1 背包：用過的物品不能再用，所以「處理到第幾個」消不掉）；不會 → 只是每輪要枚舉的候選（完全背包：這輪用 coin i 不影響下輪還能用 coin i）。這一句同時解釋了「為什麼都要查過」和「為什麼可以壓成一個值」——正因為選項集合不隨歷史改變，每個 state 只需保留最佳值，不需要保留「靠哪個 choice 達成」。
- 23：D&C 版正確。三件事。(1) **暴力法「怪怪的」是對的直覺**：取值 → 排序 → 重建是 O(N log N)，它之所以是暴力解，正是因為它**把「每條 list 已排序」這個給定結構整個丟掉**；你覺得浪費，就是察覺到這點。所有「已排序」的題都該問：我有沒有用上這個前提？(2) **程式碼註解的複雜度是舊的**（`O(n*m)`、`O(logn)`），你在文字裡已自己更正為 O(N log k) / O(log k)——註解要跟著改，不然二刷會被自己誤導（跟 139 的 `dp[n-1]` 殘留註解同一個毛病）。分析方法：每一層把全部 N 個節點各碰一次 = O(N)，共 log k 層。(3) 小處：`lists.size() - 1` 在空 vector 時 `size_t` 會下溢成巨大值再轉 int，C++20 定義為 -1 所以能動，但寫 `(int)lists.size() - 1` 更穩。
- 23（bottom-up D&C 的起手式）：**repo 已有專文** `Divide_and_Conquer/04_Bottom_Up_Divide_and_Conquer.md`，裡面就是你問的那個雙層迴圈。for loop 難寫的癥結只有一句話：**內層條件 `i + interval < n` 的意思是「右半邊還存在嗎」**——不是 `i < n`。因為 `interval` 這一輪要合併的是 `[i, i+interval)` 和 `[i+interval, i+2*interval)` 兩塊，若 `i + interval >= n` 就沒有右半可合，那塊直接留著進下一輪。LC 23 的版本比陣列版更簡單，因為 linked list 自己知道結尾、不需要 end index：`for (interval=1; interval<k; interval*=2) for (i=0; i+interval<k; i+=interval*2) lists[i] = merge(lists[i], lists[i+interval]); return lists[0];`
- 125：**沒有好處，你的版本反而更安全。** 解答版唯一的優點是讀起來貼近口語描述（「兩邊各跳過雜訊 → 再比對」），但代價是 `i < j` 這個守衛要在**三個地方**各寫一次（for + 兩個 while）；漏掉任一個內層的 `i < j`，遇到 `",,,"` 這種全是雜訊的輸入就會越界——這是這題的經典 bug。你的三分支寫法**結構上不可能有這個 bug**，因為 `i < j` 只出現一次，而且比對只在兩邊都確定是 alnum 的 else 分支裡發生。解答版還有個小彆扭：兩個 while 可能讓 `i == j`，於是拿同一個字元跟自己比（無害，但要多想一步才確定沒事）。兩版都 O(n)，面試寫哪個都行，壓力下你的版本更不容易出錯。
- 125（C++ 陷阱）：`std::isalnum` / `std::tolower` 的參數必須是**可用 `unsigned char` 表示的值或 EOF**；直接傳 `char`，當它是負數（非 ASCII 位元組）時是 **UB**。正確寫法 `isalnum(static_cast<unsigned char>(s[i]))`。LC 125 保證純 ASCII 所以沒事，但這是很常被問到的 C++ 細節，repo 的 `CPP_Reference/Type/ASCII_for_LeetCode.md` 第 5 節列了這些函式但沒提這個坑，值得補一行。
- 169：**「解法太多」本身就是這題的考點**——它不是要你會某一招，是要你能在多個解法之間**做取捨並說明理由**（hash map O(n)/O(n)、排序取中位 O(n log n)/O(1)、隨機化期望 O(n)、D&C O(n log n)/O(log n)、Boyer-Moore O(n)/O(1)）。面試真正的問題是「你為什麼選這個」，而 Boyer-Moore 是唯一同時 O(n) 時間 + O(1) 空間的，所以它是正解，其餘是討論素材。
- 169（D&C 值不值得寫）：**值得，但理由是「它是 D&C 的非典型用例」，不是為了解這題。** 大多數 D&C 題切的是「結構」（陣列/區間），這題切完之後的 combine 很特別：左右各自的多數元素**未必是整體的多數元素**，所以 combine 階段必須回頭數一次 → 這正是 `O(n log n)` 的來源（`T(n) = 2T(n/2) + O(n)`）。它示範了「**子問題的解不能直接合併，需要額外驗證**」這種 combine 型態，跟你 09-15 在 23 寫的「兩個已排序 list 直接接起來」形成對照。repo 的 `Boyer_Moore_Voting_Algorithm.md` 目前沒收這個對照，`Divide_and_Conquer/05_Conquer_Strategy_Comparison.md` 倒是講 combine 策略的，那才是它該去的地方。
- 169（真正的延伸）：比 D&C 更該做的是 **LC 229 Majority Element II**（>n/3，最多兩個候選）——它逼你面對 Boyer-Moore 的推廣形式（n/k 需要 k-1 個候選）以及**第二輪驗證為何是必須的**（169 因為題目保證多數元素存在才能省掉驗證，229 不保證）。`Boyer_Moore_Voting_Algorithm.md` 的 Pattern 2 已經寫好了。

---

## 2026-09-14

- 200. Number of Islands
- 207. Course Schedule
- 208. Implement Trie (Prefix Tree)
- 230. Kth Smallest Element in a BST

**心得**：
- 200：DFS 滿 trivial 的。想知道有沒有需要做 disjoint set 版本。
- 207：用 Kahn's algorithm，BFS 變形，注意 incoming edge count（in-degree）的概念就可以了，算好實作。想知道要不要寫一個 DFS 版本。
- 207（DFS 版）：用三色標記寫出來了。雖然知道核心是找 back edge，但還是先被 Opus 5 提示了技法名稱。看完 review 後這個做法越看越不妙——的確沒有在進 dfs 時把自己變 GREY，剛好沒 loop 所以不會踩到問題；有 loop 的話要第二次進去才會擋掉自己，等於有些 case 要多進去一次。要改成 entry-style。
- 230：意外卡了超．級．久，一直卡在怎麼樣不遞迴下去，結果寫出很醜的 code（member `count` + `NOT_FOUND = -1` sentinel 往上傳）。第一版方向完全錯誤（把 `k-1`、`k-2` 往下傳），花了 20m34s。結論：只要用 k 來判斷就可以，把 k 當成 internal state 來用。
- 230（重做）：再做了一次，錯誤的次數異常的多……主要三個關鍵設計：(1) 把 k 當成遞迴的 internal state 來用，要用 call-by-reference，不然至少要另外拉一個 internal state；(2) k 還可以作為遞迴要不要繼續的條件，來 early return；(3) 因為有設計 early return，所以需要另一個變數來存答案，才方便帶答案回去——不然用 return value 很難實作，會多很多賦值跟判斷式。

**LLM 點評**：
model: Opus 5 (1M context)
- 200：**單就 200 不用寫**，DFS/BFS 是這題的正解（O(mn)，UF 加上 α 反而略慢，還要多一個 parent 陣列）。但 **Union-Find 本身一定要練**，只是不該挑 200 當練習題——200 的網格是靜態的，一次掃完就結束，用不到 UF 的招牌能力：**動態加邊、即時查連通數**。真正逼出 UF 的是 305 Number of Islands II（陸地一格一格長出來，每次問島數）——那題 DFS 每次重掃是 O(k·mn)，UF 是 O(k·α)，這才是「非 UF 不可」。判準：**問題是不是增量的**？靜態一次性連通 → DFS/BFS；動態合併/反覆查詢 → UF。repo 的 `Union_Find/08-Connectivity_Problem_Strategy_Guide.md` 就是在講這個選擇，`07-LeetCode_Tips.md` 有題單。建議：200 到此為止，把 UF 的練習排在 305 / 684 / 547 / 721 上。
- 207：**要寫，而且這次跟 200 的 UF 情況相反。** DFS 版不是 Kahn's 的機械改寫，它是另一個獨立技法：**三色標記**（WHITE 未訪 / GRAY 在遞迴堆疊上 / BLACK 已完成），偵測到指向 GRAY 的邊 = back edge = 有環。差別在**判準不同**：Kahn's 是「還有點沒被排出來就有環」（數量），DFS 是「走到正在堆疊上的點」（結構）。後者可遷移到 Kahn's 做不到的題：找出環本身、SCC（Tarjan/Kosaraju）、DAG 上的記憶化（GRAY 代表「正在算」，BLACK 代表「算完可用 memo」）。repo 有兩篇現成的：`Algorithms/DFS/03-Node_Coloring_DFS.md`（三色 + 邊分類）、`Algorithms/Topological_Sort/03-DFS_Based_Implementation.md`（含 post-order 逆序得拓撲序，直接餵 210）。一個常踩的坑：只用一個 `visited` 陣列偵測不出環——必須區分「這條路徑上」和「以前走過」，這正是 GRAY/BLACK 存在的理由。
- 207（DFS code review）：**結果正確，但有一個不對稱**：`canFinish` 的外層迴圈沒有把起點染成 GREY，只有遞迴時才把 neighbor 染 GREY。起點永遠是 WHITE 進入 dfs、結束才變 BLACK。它之所以還對，是因為若有邊指回起點 r，dfs 會把 r 當成未訪問而**第二次進入** dfs(r)，這時通往 r 的那條路徑上的 child 已經是 GREY，於是被抓到；而 DAG 中不可能有邊指回 r（否則就是環），所以不會誤判。但這個正確性要繞一圈才證得出來，面試時很難說服自己。乾淨的寫法是 **entry-style**：`dfs` 一進來就 `color[node] = GREY`，離開時 `= BLACK`，呼叫端完全不用染色——repo 的 `Topological_Sort/03-DFS_Based_Implementation.md` 把這兩種寫法分成「實作一 Pruning-on-Push」和「實作二 Pruning-on-Entry」，你現在是兩種混用。其餘：邊的方向 `neighbors[edge[1]].push_back(edge[0])` 對（b → a）；複雜度 O(V+E) 對；小處 `for (auto edge: prerequisites)` 每圈複製一個 vector，改 `const auto&`；三個顏色常數是可變的 member，改 `static constexpr int` 或 `enum`。
- 207（補充）：自己看出重複進入的問題，判讀正確。兩點精確化：(1) **只有外層迴圈的起點會被重複進入**，非起點都是被 parent 在 push 前染 GREY 的，在 dfs 裡時已是 GREY；起點是唯一「WHITE 狀態下待在 dfs 裡」的節點。(2) 多進一次的成本**有界**（那些 WHITE 子樹本來就要走，仍是 O(V+E)），所以**不是效能問題，是可驗證性問題**：現在的正確性依賴「DAG 裡不可能有邊指回 r」這個繞一圈的論證；改 entry-style 後不變量變成一句話「GREY = 正在當前遞迴路徑上」，對每個節點都成立、不用分 case，面試時要證的正是這個。
- 230：三件事。(1) **`count` 當 member 跟 146 的 `solutions` 是同一個病**：同一個 Solution 物件呼叫兩次就壞，而且 `k` 在遞迴中從未改變、只是被一路傳下去——這就是為什麼寫起來覺得醜：**公開 API 和遞迴 helper 被硬塞成同一個函式**。拆出 `void inorder(node, int& k, int& ans)` 立刻變乾淨。(2) **`NOT_FOUND = -1` sentinel 在這題剛好安全**（題目保證 `0 <= val`），但它是「用資料值兼任控制訊號」，換一題有負值就爆——你 09-11 做 139 時 `-1` 在 `||` 裡被當 true 也是同一類問題。(3) **「怎麼樣不遞迴下去」的標準答案是 iterative in-order（顯式 stack）**：`while (cur || !st.empty())` 往左推到底、pop 一個就 `--k`、`k == 0` 直接 return——**它天然就停，不需要任何 sentinel 往上傳**。這是你待補的「迭代版」清單裡唯一一題迭代比遞迴**更好**而不只是等價的，值得現在就寫。repo：`Trees/Iterative_Traversal/03-Current_Pointer_Implementations.md`、`Binary_Search_Trees/02-In-order_Traversal_Strategy.md`。另外：你註解裡「算左子樹 node count + 1」**不是方向錯誤，那是這題的官方 follow-up**（BST 頻繁改動時如何優化）——答案就是在節點上augment subtree size，repo 已有 `Binary_Search_Trees/Augmented_BST_for_Order_Statistics.md`。你自己想到了，只是誤以為它錯。
- 230（重做點評）：你這三點其實是**同一個設計契約的三個欄位**，而且是可複用的：遞迴要「邊走邊改狀態 + 提早停 + 帶答案回來」時，簽名就長成 `void f(node, State& st, Result& out)`——(1) 是可變狀態、(2) 是 guard、(3) 是輸出參數，缺一個另外兩個就會變醜。特別是 (3) 的因果你抓得很準：**一旦要 early return，用 return value 就得讓「找到了」這個訊號穿過每一層 frame**，這正是你第一版 `NOT_FOUND = -1` sentinel 的由來；換成輸出參數後，訊號不用傳播，寫起來自然短。(1) 的兩個選項裡 by-ref 明顯優於 member——member 就是你 146 `solutions` 和第一版 `count` 踩過的同一個坑。repo 對應：`Divide_and_Conquer/06_External_State_Traversal_Order.md`、`Recursion/State_Design_Across_Recursive_Paradigms.md`。另外**同一天重做還錯很多次，代表這個 pattern 還沒內化**，已排進 Problem_Review 二刷；下次直接寫 iterative in-order 版，那版根本不需要這三個欄位（stack 自帶狀態、`return` 自帶 early exit），對照著寫會更快固化。

---

## 2026-09-11

- 139. Word Break（Trie + DFS TLE → 改 bottom-up DP + hash set 通過）
- 146. LRU Cache（四版才過）
- 155. Min Stack
- 199. Binary Tree Right Side View

**心得**：
- 139：用 Trie 來做，但會 TLE，不知道為什麼。卡了滿久，寫了 40 分鐘，覺得還滿難的，應該是 Medium 到 Hard。之後一定要再做一次。
- 139（第二次）：跟 Fable 5.1 來來回回，看了解答知道是 DP。靈感是「從後面切斷、馬上查找，前面看 cache」。最難的是設計 `dp[i]` 要用 index 還是 length——為了實作簡化，直接用字串長度來查，比較直覺。前一版把查找的項目寫錯成 index（`cache[j-1]`），改成 look backward 後就能直覺看「前面那個位置的長度」`cache[i-j]`。
- 139（回顧）：一開始 Trie 這個方向本身就錯了。Trie 是 hash map 的優化，不是這個演算法的重點；重點是**不要重複計算**，所以本質是 DP。在 DP 之上再加 Trie 才會優化查找時間，這樣才有意義。
- 146：這題真的有點太難了，觀念全部對，但是實作一直錯（四版才過）。Medium to Hard!! 整理成幾個重點：
  1. 關鍵是 get 跟 put 的 O(1)，所以要用一個 hash map 來達成 O(1)。
  2. 要記錄最新被查找的項目、以及下一個可以刪除的節點，所以需要 doubly linked list。為了讓實作簡單，頭跟尾都加 dummy 是比較簡單的做法。
  3. 更新的時機很重要：被取用了，node 就要放到最近被使用的地方；被更新值了，也要放到最近被取用的地方。
  4. doubly linked list 移除 / 插入 node 一直重複出現類似的程式碼，拉一個 function 出來，整體實作會容易很多。
  5. 有類似 push-pop 的 technique——k-top 那個「先更新，再 balance」的概念去更新 linked list。
- 155：直覺是 monotonic stack。因為 monotonic stack 常常要 maintain 一個 property，直覺就聯想到 while——判斷 non-increasing 或 increasing 的那個判斷式。不過這題很特別，只要 maintain 一個 stack，不用一直更新 stack 的值：每個時間點都有一個戳記，戳記一次一次判斷就解決了。一開始用 while 只是把 monotonic stack 的習慣聯想過來，這個 case 不用。Monotonic stack 最麻煩的就是那個判斷式：要想清楚我要的是 non-increasing 還是 increasing，來決定配不配等號。
- 199：DFS + level + pre-order，先用「每層覆寫 `view[level]`」做出來。這不是最佳解，因為每次都要更新回傳陣列。可以改 traverse 的方向從右到左：這樣每次遇到的第一個一定是還不存在的 level，直接 push 到尾巴就好；已存在的自然不用更新，因為右邊先走過了。所以更簡單的思路是：由右到左的 pre-order，一碰到回傳陣列還不存在的 level 就一定是答案。修改 traverse 方向是一個很有趣的設計概念。

**LLM 點評**：
model: Fable 5.1
- 139：TLE 的原因不在 Trie，在 **DFS 沒有記憶化**。每次 `next->word` 成立就從 `&root` 重新開始，等於在問「`s[i..]` 能不能被切」——這個子問題會被反覆問，`"aaaa…"` + `["a","aa","aaa"]` 就是指數級的切法數。所以你註解的 `O(n)` 是錯的，實際是指數。修法只要一行思維：**`ptr == &root` 時的狀態就是 `dp[i]`**，加一個 `memo[i]` 在進入 root 分支時查/存，時間就變 `O(n · L)`（L 是最長單字，Trie 走訪最多 L 步）。Trie 本身是正確的加速：它把「s[i..j) 在不在字典」從 O(L) hash 變成一路走下去、所有可能的 j 一次掃完。這題的本質是 **1-D DP（`dp[i]` = 後綴可切）+ 一個查字典的結構**，Trie 是第二部分的好選擇，但你把兩部分揉在同一個 DFS 裡，就看不出第一部分少了 memo。建議二刷時先寫最樸素的 `dp[i] = any(dp[j] && s[j..i) ∈ set)`，再把 set 換成 Trie，兩層分開會清楚很多。小處：`return ptr->word || ptr == &root` 那個 `|| ptr == &root` 只在 `s` 為空時觸發，可以直接在最外層處理。
- 139（DP 版）：**index vs length 這個選擇有標準答案：用 length。** `dp[len]` 讓 `dp[0]` = 空前綴 = `true` 這個 sentinel 自然存在，內層 `cache[i-j]` 永遠合法、不用判 `j-1 < 0`——這就是你 09-04 做 LC 5 時寫的「把邊界拉成 base case 吃掉，子問題就不用判邊界」。用 index 版 `dp[i]` = 以 i 結尾，就得特判 `j == 0` 的情況。前一版的 bug 正是 `j` 一半當長度、一半當 index；統一成「look backward 的長度」後語意就對齊了。複雜度 `O(n² · L)`（substr 複製 L），內層 `j` 可用最長單字截斷。註解還停在 `dp[n-1]` / `dp[0] if s[0] in hashmap`，是 index 版的殘留，改一下。下一步把 set 換回 Trie，就能看出昨天那版少的是什麼。
- 139（回顧）：這個結論完全對，而且可以推廣成一個先問的問題：**這題的瓶頸是「搜尋空間太大」還是「單次查找太慢」？** 前者靠 DP / memo 砍重複子問題，後者靠資料結構（hash / Trie / BIT）砍每次的成本。139 的瓶頸是前者——切法數指數級——所以先 DP 再談 Trie；你第一版直接上 Trie，是把第二層的優化當成第一層的解法。反過來的例子是 208/211 這種純 Trie 題，瓶頸在查找本身，沒有重複子問題可砍。以後看到「字典 + 字串」先問這一句，就不會再從 Trie 進場。
- 146：最終版乾淨，`refresh()` 抽出來是對的。四版的錯各是一個獨立的課：(1) 成員函式**參數型別**在宣告點解析、**本體**在 class 完整後解析，巢狀型別要先宣告；(2) `end` 指向真實節點就得處處判「移的是不是 end」，**頭尾都 dummy** 讓 `removeNode` 永遠不碰 nullptr、`insert` 不用維護狀態——是 09-04「邊界拉成 base case」在資料結構上的版本；(3) 淘汰是三件事：斷鏈、erase map、delete，漏一個就是懸空指標或 size 不降；(4) LRU 的 U 是 used，`get` 也算。**這題的本質不是演算法，是「兩個資料結構要同步維護不變量」**，每個操作都要問「map 和 list 是否仍一致」。值得二刷，重點是一次寫對而不是想出來。 第 5 點的連結很準：淘汰寫成「先 insert 再看 size 超了就 pop 最舊」，跟 `Data_Structures/Heaps/03-Push_Pop_Fixed_Size_Heap.md` 的 push-then-pop 是同一個形狀，好處是永遠不用分「滿 / 沒滿」兩條路徑。
- 155：你發現「不用 while」是對的。輔助 stack 存的形狀**確實是** non-increasing，但要分「單調是不變量」和「單調是技法」：技法意義的 monotonic stack（739/84/42）靠 push 時 **while-pop** 掉違反的元素來**主動維護**單調，被 pop 的元素是被淘汰的候選；Min Stack 的輔助 stack 是每個位置記「到此為止的 min」的戳記，prefix min 天生 non-increasing，單調是**免費的副產品**，沒有元素因 push 被淘汰——這是 `Prefix_Sum/02_Running_State_Pattern.md` 的 running min 套在 stack 上。所以它是一個單調的 stack，但不是「monotonic stack」這個技法；技法的名字指的是 while-pop 那個機制，而那正是你說最麻煩的判斷式所在。會混淆是因為有一個常見優化：輔助 stack 只在 `val <= curMin` 時才 push，這樣輔助 stack 看起來是 non-increasing 的——**而這裡就是你最後一段那個等號問題的真正出場點**：一定要 `<=` 不能 `<`，否則有重複 min 時 pop 掉一個就把另一個的紀錄弄丟了。所以你的兩段心得其實對應兩個版本：戳記版不用判斷式；優化版要判斷式且等號必須帶。
- 199：右到左的洞察對，且 repo 已寫在 `Trees/DFS_for_Level_Order_Traversal.md` 範例 2（根→右→左，每層第一個訪到的就是答案），這是你 09-10 做 102 時我提的那篇的變形——你自己推出來了。兩個補充：(1) 兩版都是 O(n)，「不是最佳解」是指**不變量更乾淨**（「第一次到達即答案」vs「最後一次覆寫才對」），不是複雜度差異；面試講這個差別比講 big-O 有價值。(2) 「**改走訪順序讓『第一次遇到』直接成為答案**」可以推廣：left side view 就是根→左→右；`Arrays_and_Strings/Reverse_Processing_Patterns.md` 是同一個哲學在陣列上的版本（從右到左避免覆蓋）。覆寫版有一個隱含風險：`view[level] = val` 依賴「左後右」的順序才對，把遞迴順序調換就錯，而 push 版天然不會。

---

## 2026-09-10

- 54. Spiral Matrix
- 56. Merge Intervals
- 79. Word Search
- 98. Validate Binary Search Tree
- 102. Binary Tree Level Order Traversal
- 105. Construct Binary Tree from Preorder and Inorder Traversal

**心得**：
- 54：方向正確，可是寫太久了。另外，在設計初始狀態跟 index boundary 的時候，可以再想一下，也許程式碼可以更精簡。如果看到 redundant 的 code，應該有地方可以再優化。
- 56：我太小看這題了。方向是對的，但沒有正確想清楚，做 interval 這種題要先假設排序過。再來，overlap 其實是判斷「前一個的尾巴」跟「後一個的頭」：如果前一個尾巴小於後一個頭，就沒有 overlap 了；剩下的 case 就是有 overlap，這時才去更新 merge 的尾端。一直漏掉 overlap 的一些 case，太憑直覺在寫，沒有真正思考 normal case 和 test case，也沒有想清楚真正的 merge 概念，只考慮到很 naive 的 merge case。
- 98：用 in-order（previous checking）解決了，接著也把 range 版寫出來了（用 `TreeNode*` 的 nullptr 當無界）。關鍵就是設計兩個 range，把父親的狀態往下傳遞——所以關鍵是父親要傳遞什麼狀態到下一個子問題去。
- 102：BFS 完成，DFS 版也練到了——用 parent 的狀態往下傳遞（level numbering），pre-ordering。
- 105：有做出來，但每次找 middle（root 在 inorder 的位置）都要花額外時間，想知道這樣時間複雜度是多少。看到一個優化是先用 O(n) 把值→index 的 map 建起來，查找降到 O(1)，覺得蠻不錯。自己的版本 review 後也看到第二個優化：traverse 時 preorder 的 index 可以做成全域的——只要遞迴結構是照 preorder 建，index 就會自然前進，不用複雜運算去記 k 值。

**LLM 點評**：
model: Sonnet 5
- 54：實際做法是 direction array + 原地 visited 標記，撞到邊界或 visited 就轉向（`d = (d+1) % 4`）。看過實際 code 後找到兩處 redundant：(1) `while` 迴圈條件跟迴圈內的 if 判斷是同一組 boundary/visited check，做了兩次；(2) 「move → 發現撞牆 → undo 這步 → 轉向 → 再 move 一次」可以省掉，因為總步數已知是 `m*n`，改成 `for (k < m*n)` 驅動迴圈，並用暫存的 `ni, nj` 算出下一步候選座標、決定完方向後一次到位，不用先移動再退回。演算法本身（direction array + sentinel）沒問題，純粹是這兩處檢查重複。
- 56：你抓到的兩點正是這題的全部核心，而且 repo 已有一篇完整對應：`Algorithms/Greedy/Interval_Problem_Solving_Playbook.md`（第 1 節「排序是第一步」、第 2 節「Overlap 判定」）。你講的判準可以再精確一句：merge 後的區間尾巴要取 `max(prev.end, cur.end)`，不能直接假設 `cur.end` 更大——因為排序只保證按 start 排序，某個區間可能被前一個完全包住（`cur.end < prev.end`），這時如果直接覆寫成 `cur.end` 會把已經合併好的範圍縮小，是這題常見的隱藏 bug。一直漏 case 的根源，通常是把「merge」想成只有一種情況（相鄰兩個部分重疊、取後者的 end），但實際要覆蓋三種：(1) 完全不重疊，直接放進 result；(2) 部分重疊，`end = max(prev.end, cur.end)`；(3) `cur` 被 `prev` 完全包住（`cur.end <= prev.end`），這時 merge 後的 end **不變**，如果沒想到這個 case、順手寫成 `prev.end = cur.end`，範圍反而會縮小。這也是為什麼要先想 normal case（隨機幾個重疊區間）+ edge case（單一區間、完全包住、首尾相接 `[1,4],[4,5]` 算不算重疊），而不是看一眼題目就開始寫——**先列出這三種 merge 情況，再對每一種寫測資，程式碼會自然對，不用邊寫邊補洞。**
- 98：**值得寫，這次跟 104/226 的迭代版不同**——range-passing 不是同一個解法的機械改寫，是另一個 pattern：「把約束由上往下傳」（top-down constraint propagation），in-order 版則是「利用 BST 的序列性質」。前者可遷移到 LC 1373、333 這類「子樹要滿足某個從祖先繼承的界」的題，也是遞迴設計裡「參數帶約束、回傳帶結果」的標準範例。寫的時候注意一個坑：初始界不能用 `INT_MIN / INT_MAX`，節點值可能剛好等於它們，用 `long long` 或 `optional<int>` / 指標當「無界」。兩種都會之後，面試被問「還有別的做法嗎」可以直接切。
- 98（range 版 review）：正確，且用 `nullptr` 當無界比 `long long` 乾淨，直接繞過 INT 邊界陷阱。兩處修：空間是 `O(h)` 不是 `O(n)`（平衡 `O(log n)`，鏈才 `O(n)`）；註解「parent 是右子樹最小值」不精確，parent 不在右子樹裡，它是右子樹的**嚴格下界**，這對應 code 用 `>=` 判失敗。兩版差別：in-order 是**子問題回傳狀態給父親**（`prev` 往上帶），range 是**父親傳狀態給子問題**——同一棵樹、資訊流方向相反。看樹題先問：資訊往上匡還是往下傳？ repo 對應：`Algorithms/Design_Principles/Recursion/04-Top_Down_vs_Bottom_Up_Recursion.md`（參數向下 vs 返回值向上）、`Data_Structures/Trees/Path_Based_Thinking_Aggregation.md`（祖先約束 → 沿 path 傳狀態，表格「限制範圍」列就是這題）。
- 102：**值得，而且很便宜（5 分鐘）**。DFS 版的關鍵決策是「把 depth 當參數往下傳，用它當 `result` 的 index」——`if (depth == result.size()) result.push_back({})`。這跟 104/226 的迭代版不同，它是一個可遷移的小技巧：199 Right Side View、103 Zigzag、107、515、637 全是同一招，而且面試確實會問「不用 queue 能做嗎」。同時它又是今天 98 那個 Top-Down「參數往下傳」pattern 的再一次練習。repo 有專文：`Data_Structures/Trees/DFS_for_Level_Order_Traversal.md`。
- 105：線性掃 inorder 找 root 的版本是 **worst case O(n²)**（每個節點掃一次，總長度加起來是 n + (n-1) + … 在退化成鏈的樹上），平衡樹是 O(n log n)。建 `val → index` 的 hashmap 後是 **O(n)**——這題保證值唯一，所以 map 才成立，這是要先確認的前提。另一個常見的隱藏 O(n²)：如果每層遞迴用 `vector(begin+a, begin+b)` 切子陣列，複製本身就是 O(n)/層，map 也救不回來；要**傳 index 範圍**不傳副本。再進一步的寫法是 preorder 用一個全域遞增的 `preIdx` 指標（root 永遠是下一個），遞迴只需帶 inorder 的 `[lo, hi]`——參數從四個變兩個，也是「parent 傳狀態給子問題」的形狀。repo 目前沒有 105 專文。
- 105（code review）：正確，`k + (mid-start) + 1` 算對，有傳 index 沒複製。`if (k == preorder.size())` 多餘——`start > end` 已涵蓋所有終止，`k` 的合法性由算術保證。全域 `preIdx` 的真正價值不是省參數，是**把那個最易錯的算術整個消掉**：照 preorder 建樹、每 new 一個就 `preIdx++`，左子樹建完指標自然停在右子樹 root；代價是必須先左後右，這個依賴要寫進註解。兩個優化疊上後 O(n) / O(n)，到頂。

---

## 2026-09-07

- 未完成：15. 3Sum（running hashmap 版本未實作；2026-10-20 更正先前誤記的完成狀態）
- 17. Letter Combinations of a Phone Number
- 33. Search in Rotated Sorted Array
- 39. Combination Sum
- 46. Permutations
- 53. Maximum Subarray

**心得**：
- 15：我個人覺得是 medium 到 hard。思路一開始是先處理 duplicate，用 sort 解決之後，開始想 loop iterate (i, j) 這個 pair、再去找對應的 k。直覺是放一個 cache 做快速查找，但發現 hash map 一直沒辦法很好地建構出來，特別是去掉重複出現的 index 這部分，就是 build 不出來。
- 15（紀錄更正，2026-10-20）：先前「用 running hashmap 做出來了」是誤記，實際沒有寫過此版本。Running hashmap 與 sort + two pointers 都仍待實作；2026-10-20 完成的是先建立完整索引表、用補數最右 index 判斷合法位置的版本。
- 17：大概沒什麼問題，就想到 backtracking。不小心又把 const 的 `unordered_map` 忘記用 `.at()` 存取，這樣 compile 會有問題。
- 33：已經做了蠻多次，每次都還是錯得一塌糊塗。這次的關鍵點在於，它確實會有一個 inflection point，但用 inflection point 去切出左半跟右半其實很沒有效率。更直覺的做法是看哪一半是 normal sorted，然後去 sorted 的那一半裡找：在裡面就往那個方向前進；沒有的話就直接把另外一半 prune 掉。所以應該是判斷哪一半 sorted → 往 sorted 那半前進，其餘 prune。
- 39：我的做法是「選或不選」。常見方式是直接做成多叉決策樹，我做的是二元決策樹。最麻煩的是時間複雜度計算：選或不選是 2 的某個次方，次方看有幾個元素，也就是 target 最大除以最小值，就知道指數級數了。一開始沒想到可以用數字的範圍來推導需要分叉幾次。之後可以再回來算一次，用 N 多叉決策樹的做法做一遍。
- 53：太經典了。直覺是 Kadane's，一時間被轉去 sliding window，但知道要用 DP。卡了蠻久，完全解不出 Kadane 的解法。偷看解答後做了 bottom-up DP，但在算最大值時忘記為什麼全域最大值要在每個子陣列的可能性裡 globally tracking — 每個位置都有可能，而不是最後那個項目。現在沒辦法直觀地看出這個東西。

**LLM 點評**：
model: Fable 5.1
- 15（2026-10-20 更正）：先前將 hashmap 方向判為不適合 3Sum 的評論過度武斷。固定 i、j 後查詢補數，配合合法 index 判斷與值去重，可以得到正確解；2026-10-20 已提供完整索引表版本。Running hashmap 尚未實作，不應記為通過；sort + two pointers 也仍待實作。
- 15（第二次）：你做出來的就是「固定 i，內層跑 Two Sum I（seen-set）」— 「往前找曾經看過的」正是 LC 1 的 seen-set 概念，只是把 target 換成 `-nums[i]`，所以 hash map 其實是內層 2Sum 的 cache，不是 3Sum 層級的。它和 two-pointer 一樣 O(N²)，差別在 dedup：two-pointer 靠有序跳過三處相同值就乾淨；seen-set 版要在 i 跳重複 + 內層用 set 收 (j, k) 值對，比較容易漏。二刷時兩種都寫，重點感受「排序讓 two-pointer 成立」這件事。
- 17：queue（BFS）版不用另外寫。它和 backtracking 是同一棵 state space tree 的 BFS / DFS 兩種走法，沒有新的設計決策，面試也極少追問（這題的 follow-up 通常是 digits 為空、或 mapping 動態給定）。真正值得留意的是這題把 backtracking 的三要素展示得很乾淨：path、candidates 由 `digits[depth]` 決定、terminate 在 `depth == digits.size()`。`const` map 用 `.at()` 這個坑 repo 已有：`CPP_Reference/Container/Const_Map_and_Operator_Bracket.md`。
- 33：你這次抓到的判準是對的，而且它和 153 是**兩種不同的 binary search**，混用就是你一直錯的原因。153 找 inflection point，predicate 是 `nums[m] > nums[r]`（跟右端比）；33 不找 inflection，每輪只問「`[l, m]` 是否 sorted」（`nums[l] <= nums[m]`），sorted 那半可以用普通 range check 決定 target 在不在，不在就整半 prune。**是「兩段 binary search」壓成一段**，不是「先找 pivot 再二分」。注意 `<=` 而非 `<`：`l == m` 時單元素也算 sorted，否則會漏。repo 的 `03-Peak_and_Rotated_Array_Search.md` 目前只收 153 / 162，這個「找 sorted 半邊」的 predicate 還沒寫進去，值得補一段對照。
- 39：你的推導方向對，補一個精確化：二元樹的深度不是 `T/M`，而是 `N + T/M` — 每個「不選」讓 `i` 前進一格（最多 N 次），每個「選」讓 `target` 減至少 M（最多 T/M 次），所以 `O(2^(N + T/M))`；多叉樹版是 `O(N^(T/M))`，兩者都是同一個 state space `(i, remaining)` 的不同枚舉方式。**「用數值範圍推遞迴深度」這個感覺是 backtracking 複雜度分析的核心**：深度 = 「還能做幾次決策直到終止」，這題的終止由 target 給，所以深度由 T/M 給。二元 vs 多叉在 repo 有專文：`Algorithms/Backtracking/05-State_Space_Tree_and_N_Tuple_Representation.md`。
- 39（code review）：演算法正確，排序後 `candidates[i] > remaining` 同時砍掉選/不選兩支是亮點；開頭的 input/output 註解是 3Sum 教訓的落實。要改：複雜度註解 `O(n^n * n)` 錯，應為 `O(2^(N+T/M) · T/M)`，空間是遞迴深度 `O(T/M)` 不是 `O(n)`；`solutions` 做 member 會讓重複呼叫累加，改 by-ref 傳或開頭 clear；`sol` 改名 `path`。
- 53：你卡的點是 **state 的定義跟答案的形狀不一樣**。`dp[i]` 定義的是「**以 i 結尾**的最大子陣列和」，這是一個被限制的子問題，不是答案；答案是 `max(dp[0..n-1])`，因為最優子陣列可以在任何位置結尾，`dp[n-1]` 只是「必須包含最後一個元素」那一種。為什麼要這樣定義？因為「以 i 結尾」才能讓遞推 O(1)：`dp[i] = max(nums[i], dp[i-1] + nums[i])` — 要嘛接上前面，要嘛重新開始。如果把 state 定成答案的形狀「`[0..i]` 內的最大子陣列和」，遞推就寫不出來（不知道前面的最優段有沒有碰到 i-1，無法延伸）。所以這是一個交易：**把 state 綁死在「必須包含 i」換取乾淨的遞推，代價是最後要多一層 global max**。這正是 repo 的 `Kadanes_Pattern_DP.md`（dp[i] 必須包含位置 i）和 `State_Design/05-Local_State_vs_Global_Optimum.md` 在講的東西。順帶：sliding window 在這題失效是因為有負數 — 窗口不知道該不該縮，單調性不成立。

---

## 2026-09-05

- 104. Maximum Depth of Binary Tree
- 121. Best Time to Buy and Sell Stock
- 141. Linked List Cycle
- 226. Invert Binary Tree
- 5. Longest Palindromic Substring
- 11. Container With Most Water
- 15. 3Sum（未通過）

**心得**：
- 104：recursive tree DP 可以秒殺，但是要練習 followup iterative 版本
- 121：標記是 easy，但感覺解題難度是 medium。以前是用 Bottom-up DP 設計 buying / selling 兩個狀態，再推導到 Kadane's；這次直接做出類似 Kadane's 的解法，反而看不懂為什麼 Bottom-up DP 是有辦法想出來的，它其實蠻複雜的
- 226：同 104，迭代版待補
- 5：我感覺是 medium 到 hard，因為必須從 DP 突破，要設計的東西滿多的。DP 設計有一個大關鍵是 table 的 traverse 方向。目前這一塊比較弱，如果可以把 table traverse 的方向很快地透過 index 的 loop 建構好，解題才會相對容易，特別注意 index 的邊界。我認為這是 Array 底層 traverse 方向設計的能力之一，它直接影響 DP 的解題效率。另外，有人會把 base case 或需要邊界判斷的條件都拉成 base case 一起處理掉，程式碼就會比較乾淨。所以遇到子問題的合法性需要多判斷時，可以考慮用邊界 case 直接處理掉，讓子問題不會碰到邊界、還要去判斷數值的情況。
- 11：一看到題目直覺是 divide and conquer，可能被 container 類的裝水題影響了，但很明顯這個方向不對。看了提示後知道是 two pointer，只要把 move 策略定好解法就出來了。可是我還沒辦法連結，為什麼可以把 O(N²) 透過這種 two pointer greedy 降到 O(N)？
- 15：有做但失敗了，沒有成功處理 duplicate 的問題。跟 Gemini 討論後，這類「回傳結果不能有 duplicate」的切入點通常都是排序。更大的問題是沒有馬上釐清輸入與輸出的格式：這次一直把輸出誤會成 index，到最後才發現是「值」，而「值」沒辦法直接對應到重複的項目，這才是最大的問題。如果一開始就發現，切入方向也許就對了。

---

## 2026-09-04

- 1. Two Sum
- 3. Longest Substring Without Repeating Characters
- 20. Valid Parentheses
- 21. Merge Two Sorted Lists
- 70. Climbing Stairs

**心得**：
