# 刷題日誌

---

## 2026-09-11

- 139. Word Break（Trie + DFS TLE → 改 bottom-up DP + hash set 通過）
- 146. LRU Cache（四版才過）
- 155. Min Stack

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

**LLM 點評**：
model: Fable 5.1
- 139：TLE 的原因不在 Trie，在 **DFS 沒有記憶化**。每次 `next->word` 成立就從 `&root` 重新開始，等於在問「`s[i..]` 能不能被切」——這個子問題會被反覆問，`"aaaa…"` + `["a","aa","aaa"]` 就是指數級的切法數。所以你註解的 `O(n)` 是錯的，實際是指數。修法只要一行思維：**`ptr == &root` 時的狀態就是 `dp[i]`**，加一個 `memo[i]` 在進入 root 分支時查/存，時間就變 `O(n · L)`（L 是最長單字，Trie 走訪最多 L 步）。Trie 本身是正確的加速：它把「s[i..j) 在不在字典」從 O(L) hash 變成一路走下去、所有可能的 j 一次掃完。這題的本質是 **1-D DP（`dp[i]` = 後綴可切）+ 一個查字典的結構**，Trie 是第二部分的好選擇，但你把兩部分揉在同一個 DFS 裡，就看不出第一部分少了 memo。建議二刷時先寫最樸素的 `dp[i] = any(dp[j] && s[j..i) ∈ set)`，再把 set 換成 Trie，兩層分開會清楚很多。小處：`return ptr->word || ptr == &root` 那個 `|| ptr == &root` 只在 `s` 為空時觸發，可以直接在最外層處理。
- 139（DP 版）：**index vs length 這個選擇有標準答案：用 length。** `dp[len]` 讓 `dp[0]` = 空前綴 = `true` 這個 sentinel 自然存在，內層 `cache[i-j]` 永遠合法、不用判 `j-1 < 0`——這就是你 09-04 做 LC 5 時寫的「把邊界拉成 base case 吃掉，子問題就不用判邊界」。用 index 版 `dp[i]` = 以 i 結尾，就得特判 `j == 0` 的情況。前一版的 bug 正是 `j` 一半當長度、一半當 index；統一成「look backward 的長度」後語意就對齊了。複雜度 `O(n² · L)`（substr 複製 L），內層 `j` 可用最長單字截斷。註解還停在 `dp[n-1]` / `dp[0] if s[0] in hashmap`，是 index 版的殘留，改一下。下一步把 set 換回 Trie，就能看出昨天那版少的是什麼。
- 139（回顧）：這個結論完全對，而且可以推廣成一個先問的問題：**這題的瓶頸是「搜尋空間太大」還是「單次查找太慢」？** 前者靠 DP / memo 砍重複子問題，後者靠資料結構（hash / Trie / BIT）砍每次的成本。139 的瓶頸是前者——切法數指數級——所以先 DP 再談 Trie；你第一版直接上 Trie，是把第二層的優化當成第一層的解法。反過來的例子是 208/211 這種純 Trie 題，瓶頸在查找本身，沒有重複子問題可砍。以後看到「字典 + 字串」先問這一句，就不會再從 Trie 進場。
- 146：最終版乾淨，`refresh()` 抽出來是對的。四版的錯各是一個獨立的課：(1) 成員函式**參數型別**在宣告點解析、**本體**在 class 完整後解析，巢狀型別要先宣告；(2) `end` 指向真實節點就得處處判「移的是不是 end」，**頭尾都 dummy** 讓 `removeNode` 永遠不碰 nullptr、`insert` 不用維護狀態——是 09-04「邊界拉成 base case」在資料結構上的版本；(3) 淘汰是三件事：斷鏈、erase map、delete，漏一個就是懸空指標或 size 不降；(4) LRU 的 U 是 used，`get` 也算。**這題的本質不是演算法，是「兩個資料結構要同步維護不變量」**，每個操作都要問「map 和 list 是否仍一致」。值得二刷，重點是一次寫對而不是想出來。 第 5 點的連結很準：淘汰寫成「先 insert 再看 size 超了就 pop 最舊」，跟 `Data_Structures/Heaps/03-Push_Pop_Fixed_Size_Heap.md` 的 push-then-pop 是同一個形狀，好處是永遠不用分「滿 / 沒滿」兩條路徑。
- 155：你發現「不用 while」是對的。輔助 stack 存的形狀**確實是** non-increasing，但要分「單調是不變量」和「單調是技法」：技法意義的 monotonic stack（739/84/42）靠 push 時 **while-pop** 掉違反的元素來**主動維護**單調，被 pop 的元素是被淘汰的候選；Min Stack 的輔助 stack 是每個位置記「到此為止的 min」的戳記，prefix min 天生 non-increasing，單調是**免費的副產品**，沒有元素因 push 被淘汰——這是 `Prefix_Sum/02_Running_State_Pattern.md` 的 running min 套在 stack 上。所以它是一個單調的 stack，但不是「monotonic stack」這個技法；技法的名字指的是 while-pop 那個機制，而那正是你說最麻煩的判斷式所在。會混淆是因為有一個常見優化：輔助 stack 只在 `val <= curMin` 時才 push，這樣輔助 stack 看起來是 non-increasing 的——**而這裡就是你最後一段那個等號問題的真正出場點**：一定要 `<=` 不能 `<`，否則有重複 min 時 pop 掉一個就把另一個的紀錄弄丟了。所以你的兩段心得其實對應兩個版本：戳記版不用判斷式；優化版要判斷式且等號必須帶。

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

- 15. 3Sum（重做，通過 — running hash map）
- 17. Letter Combinations of a Phone Number
- 33. Search in Rotated Sorted Array
- 39. Combination Sum
- 46. Permutations
- 53. Maximum Subarray

**心得**：
- 15：我個人覺得是 medium 到 hard。思路一開始是先處理 duplicate，用 sort 解決之後，開始想 loop iterate (i, j) 這個 pair、再去找對應的 k。直覺是放一個 cache 做快速查找，但發現 hash map 一直沒辦法很好地建構出來，特別是去掉重複出現的 index 這部分，就是 build 不出來。
- 15（第二次）：用 running hash map 做出來了。關鍵是透過 sort 去 eliminate output duplicate。running hash map 的關鍵是：candidate 一路往下找，最後那個補數用 hash map 來記 — 但它不是往後找，是找**前面曾經看過的**；沒有的話就繼續往下，而當下 traverse 到的那個人，就成為 running hash map 裡「曾經出現過」的項目。
  ```
  // [i, ...., j, ...]
  //      *      <- 往前找有沒有出現過可用的人，有就把它當 k 取出來
  ```
  再過幾天要回來用 2-pointer 再做一次，也要熟悉「running hash map 是查看當前，然後它成為下一個 candidate 可查找的項目」這個核心概念。
- 17：大概沒什麼問題，就想到 backtracking。不小心又把 const 的 `unordered_map` 忘記用 `.at()` 存取，這樣 compile 會有問題。
- 33：已經做了蠻多次，每次都還是錯得一塌糊塗。這次的關鍵點在於，它確實會有一個 inflection point，但用 inflection point 去切出左半跟右半其實很沒有效率。更直覺的做法是看哪一半是 normal sorted，然後去 sorted 的那一半裡找：在裡面就往那個方向前進；沒有的話就直接把另外一半 prune 掉。所以應該是判斷哪一半 sorted → 往 sorted 那半前進，其餘 prune。
- 39：我的做法是「選或不選」。常見方式是直接做成多叉決策樹，我做的是二元決策樹。最麻煩的是時間複雜度計算：選或不選是 2 的某個次方，次方看有幾個元素，也就是 target 最大除以最小值，就知道指數級數了。一開始沒想到可以用數字的範圍來推導需要分叉幾次。之後可以再回來算一次，用 N 多叉決策樹的做法做一遍。
- 53：太經典了。直覺是 Kadane's，一時間被轉去 sliding window，但知道要用 DP。卡了蠻久，完全解不出 Kadane 的解法。偷看解答後做了 bottom-up DP，但在算最大值時忘記為什麼全域最大值要在每個子陣列的可能性裡 globally tracking — 每個位置都有可能，而不是最後那個項目。現在沒辦法直觀地看出這個東西。

**LLM 點評**：
model: Fable 5.1
- 15：hash map build 不出來，是因為方向選錯，不是 dedup 沒做好。「固定 (i, j)、用 map 找 k」在 2Sum 可行是因為它回傳 index 且只要一組；3Sum 回傳**值**、要**所有不重複組合**，map 這條路要同時處理「k 的 index ≠ i, j」和「值重複」，天生就髒。排序後的標準解只用一個 outer loop：固定 i，剩下區間用對向雙指針找 j, k — 就是 LC 11 那個 greedy 淘汰（`sum < 0` 丟左、`sum > 0` 丟右）。排序的價值不只是 dedup，**它讓 two pointer 成立**，所以 map 根本不需要；dedup 只剩三處 `while (nums[x] == nums[x-1]) skip`。看 `K-Sum_Problems/02-Three_Sum.md` 後重寫，通過後 16、18 是同一個模板。
- 15（第二次）：你做出來的就是「固定 i，內層跑 Two Sum I（seen-set）」— 「往前找曾經看過的」正是 LC 1 的 seen-set 概念，只是把 target 換成 `-nums[i]`，所以 hash map 其實是內層 2Sum 的 cache，不是 3Sum 層級的。它和 two-pointer 一樣 O(N²)，差別在 dedup：two-pointer 靠有序跳過三處相同值就乾淨；seen-set 版要在 i 跳重複 + 內層用 set 收 (j, k) 值對，比較容易漏。二刷時兩種都寫，重點感受「排序讓 two-pointer 成立」這件事。
- 17：queue（BFS）版不用另外寫。它和 backtracking 是同一棵 state space tree 的 BFS / DFS 兩種走法，沒有新的設計決策，面試也極少追問（這題的 follow-up 通常是 digits 為空、或 mapping 動態給定）。真正值得留意的是這題把 backtracking 的三要素展示得很乾淨：path、candidates 由 `digits[depth]` 決定、terminate 在 `depth == digits.size()`。`const` map 用 `.at()` 這個坑 repo 已有：`CPP_Reference/Container/Const_Map_and_Operator_Bracket.md`。
- 33：你這次抓到的判準是對的，而且它和 153 是**兩種不同的 binary search**，混用就是你一直錯的原因。153 找 inflection point，predicate 是 `nums[m] > nums[r]`（跟右端比）；33 不找 inflection，每輪只問「`[l, m]` 是否 sorted」（`nums[l] <= nums[m]`），sorted 那半可以用普通 range check 決定 target 在不在，不在就整半 prune。**是「兩段 binary search」壓成一段**，不是「先找 pivot 再二分」。注意 `<=` 而非 `<`：`l == m` 時單元素也算 sorted，否則會漏。repo 的 `07-Inflection_Point_Binary_Search.md` 目前只收 153 / 162，這個「找 sorted 半邊」的 predicate 還沒寫進去，值得補一段對照。
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
