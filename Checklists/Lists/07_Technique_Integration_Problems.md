# 🎯 Technique Integration Problems

A curated list of problems that require integrating multiple advanced techniques. These problems are excellent for:

- Developing multi-dimensional problem-solving skills
- Understanding how different algorithmic paradigms synergize
- Preparing for challenging technical interviews

Problems are organized by interview frequency, from most common to advanced challenges.

---

## 🔥🔥🔥 High Frequency (Must Practice)

### LC 42. Trapping Rain Water

**Techniques**: Prefix Max/Suffix Max + Two Pointers + Monotonic Stack (optional)
**Why Important**: 經典「同題多解」題目，強迫你在 prefix、two pointers、stack 之間切換視角

### LC 56. Merge Intervals

**Techniques**: Sorting + Sweep/Merge Pattern
**Why Important**: 幾乎所有 interval/calendar/booking 題目的母題，後面很多題都在玩它的變形

### LC 146. LRU Cache

**Techniques**: Hash Table + Doubly Linked List + System Design
**Why Important**: Tests data structure design and O(1) operation implementation

### LC 239. Sliding Window Maximum

**Techniques**: Sliding Window + Monotonic Deque
**Why Important**: 把「window 視角」跟「資料結構不變量」綁在一起，是 window 題裡最經典的整合題

### LC 295. Find Median from Data Stream

**Techniques**: Two Heaps + Streaming/Online Algorithm
**Why Important**: 經典 data-structure + invariant 題，練「如何用兩個 heap 維持中位數」

### LC 253. Meeting Rooms II

**Techniques**: Sweep Line (start/end events) + Min Heap OR Two-Pointer on Sorted Arrays
**Why Important**: 比 Skyline 簡化版，但很常考；練時間線思維 + 狀態計數

---

## 🔥🔥 Medium-High Frequency (Recommended)

### LC 23. Merge k Sorted Lists

**Techniques**: Divide and Conquer + Min Heap
**Why Important**: 練「兩種整合策略」的比較：pairwise merge vs heap merge

### LC 53. Maximum Subarray

**Techniques**: Prefix Sum View + Greedy/Kadane's Algorithm + Divide and Conquer (optional)
**Why Important**: 從線性掃描推到 divide & conquer 版本，是練習「同一題不同維度思考」的好素材

### LC 57. Insert Interval

**Techniques**: Interval Classification + Merge Pattern + Binary Search (optional)
**Why Important**: 練「先分 case 再合併」的整體結構設計

### LC 76. Minimum Window Substring

**Techniques**: Sliding Window + Hash Table + Two Pointers
**Why Important**: Core sliding window problem, foundation for many substring problems

### LC 4. Median of Two Sorted Arrays

**Techniques**: Binary Search on Answer Space + Partition Invariant
**Why Important**: 純 binary search 之上還要維持 partition 不變量，是「不在 array 上找 index，而在『切割條件』上 binary search」的代表

### LC 124. Binary Tree Maximum Path Sum

**Techniques**: Tree DFS + Tree DP + Recursion Design
**Why Important**: Classic tree DP, tests recursive state management

### LC 218. The Skyline Problem

**Techniques**: Sweep Line + Sorting + Max Heap/Multiset
**Why Important**: 練線段事件排序 + 狀態結構維護，是 sweep line 綜合題

### LC 315. Count of Smaller Numbers After Self

**Techniques**: Index Compression + Fenwick/Segment Tree OR Divide and Conquer + Merge Sort
**Why Important**: 跟 inversion count 類似，但多了一維資訊；很適合跟 327/493 放在同一個 block 比較

### LC 327. Count of Range Sum

**Techniques**: Divide and Conquer + Prefix Sum + Merge Sort + Two Pointers
**Why Important**: Prefix sum 先轉問題；divide & conquer + merge sort 維持排序；two pointers 在 merge 過程中數合法區間，是少見四技合一的經典

---

## 🔥 Medium Frequency (Good Practice)

### LC 84. Largest Rectangle in Histogram

**Techniques**: Monotonic Stack + Two Pointers + Divide and Conquer
**Why Important**: Foundation for 2D rectangle problems (LC 85)

### LC 85. Maximal Rectangle

**Techniques**: 2D → 1D Transformation + DP (height array) + Monotonic Stack
**Why Important**: 把 84. Largest Rectangle in Histogram 拿來當子問題，是很典型的「問題轉型 + 套用已知 pattern」

### LC 212. Word Search II

**Techniques**: Trie + DFS + Pruning + Backtracking
**Why Important**: 把字典樹、搜尋剪枝、backtracking 全包在一起；很適合練「資料結構 + 搜尋策略」的組合拳

### LC 297. Serialize and Deserialize Binary Tree

**Techniques**: Tree DFS/BFS + String Manipulation + System Design
**Why Important**: Tests tree traversal mastery and serialization design

### LC 460. LFU Cache

**Techniques**: Hash Table + Doubly Linked List + Design + Multiple Data Structures
**Why Important**: More complex than LRU, tests advanced caching strategies

### LC 493. Reverse Pairs

**Techniques**: Divide and Conquer + Merge Sort + Two Pointers
**Why Important**: 結構跟 327 超像，是練「同一類 divide-and-count pattern 的遷移能力」的好標的

### LC 560. Subarray Sum Equals K

**Techniques**: Prefix Sum + HashMap (counting)
**Why Important**: 跟 327 同樣是 prefix sum + counting，只是用 hash map 而不是 sort + divide & conquer，是「同一核心、不同實作維度」的好對照題

### LC 862. Shortest Subarray with Sum at Least K

**Techniques**: Sliding Window + Prefix Sum + Monotonic Queue
**Why Important**: Advanced sliding window with negative numbers

### LC 992. Subarrays with K Different Integers

**Techniques**: Sliding Window + Hash Table + Two Pointers + "At Most K" Trick
**Why Important**: Advanced sliding window pattern transformation

### LC 1235. Maximum Profit in Job Scheduling

**Techniques**: Dynamic Programming + Binary Search + Sorting + Greedy
**Why Important**: Interval DP with binary search optimization

---

## 💎 Advanced Challenges (For Mastery)

### LC 630. Course Schedule III

**Techniques**: Greedy + Heap + Sorting + Exchange Argument
**Why Important**: Tests greedy proof and heap-based optimization

### LC 1675. Minimize Deviation in Array

**Techniques**: Heap + Greedy + Two Pointers + Transformation
**Why Important**: Creative problem transformation with heap

### LC 1703. Minimum Adjacent Swaps for K Consecutive Ones

**Techniques**: Sliding Window + Prefix Sum + Median + Greedy
**Why Important**: Multiple optimizations working together

---

## 📚 Learning Path

### Phase 1: Foundation Patterns

1. **LC 56** (Merge Intervals) - Interval pattern 母題
2. **LC 57** (Insert Interval) - Case classification
3. **LC 146** (LRU Cache) - Data structure design
4. **LC 42** (Trapping Rain Water) - Multiple solution perspectives

### Phase 2: Core Integration

5. **LC 23** (Merge k Lists) - D&C vs Heap trade-offs
6. **LC 53** (Maximum Subarray) - Greedy + D&C perspectives
7. **LC 239** (Sliding Window Maximum) - Monotonic deque
8. **LC 295** (Find Median) - Two heaps
9. **LC 76** (Minimum Window) - Sliding window mastery
10. **LC 253** (Meeting Rooms II) - Sweep line basics

### Phase 3: Advanced Synthesis

11. **LC 560** (Subarray Sum = K) - Prefix sum + HashMap
12. **LC 327** (Count of Range Sum) - Four-technique synthesis ⭐
13. **LC 315** (Count Smaller Numbers) - Merge sort variant
14. **LC 493** (Reverse Pairs) - D&C pattern transfer
15. **LC 218** (Skyline) - Sweep line comprehensive
16. **LC 84/85** (Rectangle problems) - Problem transformation

### Phase 4: Expert Challenges

17. **LC 4** (Median of Two Arrays) - Binary search on partition
18. **LC 212** (Word Search II) - Trie + DFS + Pruning
19. **LC 862** (Shortest Subarray) - Advanced sliding window
20. **LC 992** (K Different Integers) - "At Most K" transformation

---

## 💡 Key Insights

1. **Pattern Recognition**: Many problems can be solved with multiple technique combinations
2. **Trade-offs**: Understanding which technique combination gives optimal time/space complexity
3. **Modularity**: Break complex problems into recognizable sub-patterns
4. **Transformation**: Sometimes the key is transforming the problem to fit known patterns

---

## 🔗 Related Resources

- [Divide and Conquer Hard Problems](../Trick%20Practice/Divide_and_Conquer_Hard_Problem_Playbook.md)
- [Essential Problems](05_Essential_Problems.md)
- [Hard Techniques Reference](../../Interview_Playbook/Hard_Techniques_Reference.md)
