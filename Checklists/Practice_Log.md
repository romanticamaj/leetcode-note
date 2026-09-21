# 刷題日誌

---

## 2026-09-21

- 138. Copy List with Random Pointer
- 150. Evaluate Reverse Polish Notation
- 153. Find Minimum in Rotated Sorted Array

**心得**：
- 153：這次的解法是找到 inflection point 出現的那邊，排除其他邊。
- 153（二版，一行判斷式）：思考順序是——(1) 先確認 `i` 跟 `j` 互相比較得不到有用資訊（`nums[i] < nums[j]` 只夠用來提前結束）；(2) 再由 rotated sorted 的特性想到拿 `mid` 跟 `j` 比：`mid > j` 去掉左半，`mid <= j` 去掉右半（`mid` 也可能是答案）。至於為什麼不能拿 `mid` 跟 `i` 比——rotated sorted 保證的是「某一段已排序」，而 `nums[mid] > nums[i]` 不表示任何事情，不能當結構上的判斷式。
- 150：粗心兩次了，top1 是 operand 2、top2 是 operand 1，我是不是腦袋會漏東西，兩個運算元位置放錯。
- 138：hashmap + cache + two pointers，結果沒處理到 nullptr。自己也覺得這個解法一定哪裡怪怪的。想問：有辦法 one-pass 嗎？這題要 look forward，先檢查未來但不知道未來的位置（可以用 next 反查？）。另外好像可以先用 random 去存，可以省一個空間？

**LLM 點評**：
model: Opus 5 (1M context)
- 153（寫對了，而且兩個分支互斥是可以證明的）：`nums[i] > nums[mid]` 成立時，拐點落在 `[i, mid]`，所以 `[mid, j]` 必定是升冪的 → `nums[mid] < nums[j]`，第二個分支**不可能**同時成立。這代表分支的先後順序不影響正確性——這種「互斥可證」的結構值得當場確認一下，因為只要兩個條件會同時成立，先寫誰就變成一個藏在順序裡、沒被寫下來的決定。
- 153（第一個比較是冗餘的，repo 已有正規版）：`nums[i] > nums[mid]` 這一支的結論（`j = mid`）跟「`nums[mid] < nums[j]` → `j = mid`」完全重合，所以**一次比較就夠**：`if (nums[mid] > nums[j]) i = mid + 1; else j = mid;`，迴圈結束時 `i == j` 就是答案。這正是 `Algorithms/Binary_Search/07-Inflection_Point_Binary_Search.md` 的模板（`beforeInflection(m) → nums[m] > nums[r]`）。你的版本是「模板 + 一次冗餘比較 + 一個提前 break」。
- 153（真正該記住的是：為什麼跟**右**端比，不是左端）：因為 `nums[m] > nums[右端]` 這個謂詞在整個陣列上是**單調的**（false…false true…true 反過來也是一刀切），二分搜尋能work的前提就是謂詞單調。跟左端比不具這個性質——`[1,2,3]` 沒旋轉時 `nums[mid]=2 > nums[i]=1`，照「大於就往右」會直接丟掉答案。**選擇比較對象不是風格問題，是在選一個單調謂詞。**
- 153（break 的代價，以及它在 154 第一個死）：早退要付「每輪多一次比較」，而提前結束只在已排序的子區間才發生，平均省不到什麼。更重要的是它是**最脆弱的那一段**：`154 Find Minimum II`（可重複）一來，`[3, 3, 1, 3]` 會走到 `nums[i] == nums[mid] == nums[j]`，你的 `break` 直接回傳 `nums[i] = 3`，錯。有重複值時「兩端相等」根本無法判斷拐點在哪邊，只能 `j--` 退化成 O(n)。
- 153（`j = mid` 和 `i = mid + 1` 的不對稱不是隨意的）：往左收時 **mid 本身可能就是答案**，所以不能 `mid - 1`；往右收時 `nums[mid] > nums[j]` 已經證明 mid 不是最小值，所以可以也**必須** `+1`。而 `mid` 下取整保證 `mid < j`，`j = mid` 一定讓區間變小、不會死迴圈。不變量一句話：**答案永遠在 `[i, j]` 內**——邊界怎麼移是從它推出來的，不是試出來的（見 `Algorithms/Backtracking/07-Guards_from_Invariants.md` 的同一套讀法）。
- 153（二版收斂到模板了）：`if (nums[mid] > nums[j]) i = mid + 1; else j = mid;` 就是 `Algorithms/Binary_Search/07-Inflection_Point_Binary_Search.md` 的通用模板逐字對應（`beforeInflection(m) → nums[m] > nums[r]`）。三分支塌成二分支之後，`else` 那支自動涵蓋了原本要 `break` 的已排序情形——**不是把 break 刪掉，是它不再是一個獨立的 case**。
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
