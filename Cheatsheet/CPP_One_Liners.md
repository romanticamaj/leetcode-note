# C++ One-Liners for LeetCode

C++14 的多執行緒同步：見 [同步處理必備 std](../CPP_Reference/Concurrency/CPP14_Synchronization_One_Liners.md)，包含 `thread`、`mutex`、RAII locks、`condition_variable` 與 `atomic`。

## Common

```cpp
std::string sub = s.substr(start, length);

const auto& v = m.at(key);  // const map/unordered_map 不能用 []，要用 .at()
```

## Useful

```cpp
// Convert integer to binary string using std::bitset
// Template argument <32> specifies bit width; adjust as needed
std::string binaryString = std::bitset<32>(num).to_string();

// Default is max-heap; uses std::less internally so parent > child
std::priority_queue<int> maxHeap;
// min-heap: uses std::greater so parent <= child
std::priority_queue<int, std::vector<int>, std::greater<int>> minHeap;
// Custom Priority Queue
auto cmp = [](...) {...};
using Item = ...;
std::priority_queue<Item, std::vector<Item>, decltype(cmp)> q(cmp);

// Need LIFO operations and bottom-to-top traversal? Use vector as a stack.
std::vector<std::string> dirs;
dirs.push_back("home");
dirs.push_back("user");
for (const auto& dir : dirs) { /* home, then user: bottom -> top */ }
if (!dirs.empty()) dirs.pop_back(); // remove top ("user")
// std::stack has no begin()/end(); it cannot be used in a range-based for.

std::string s = std::to_string(num);
int n = std::stoi(s);
long long n = std::stoll(s);

std::reverse(s.begin(), s.end());

std::sort(v.begin(), v.end());                      // ascending
std::sort(v.begin(), v.end(), std::greater<int>()); // descending
std::sort(v.begin(), v.end(), [](const auto& a, const auto& b) {
    return a.second < b.second;
});

int maxVal = *std::max_element(v.begin(), v.end());
int minVal = *std::min_element(v.begin(), v.end());

// Returns iterator to first element >= target
auto it = std::lower_bound(v.begin(), v.end(), target);
// Returns iterator to first element > target
auto it = std::upper_bound(v.begin(), v.end(), target);

// Use 0LL to avoid overflow when sum exceeds int range
int sum = std::accumulate(v.begin(), v.end(), 0);
long long sum = std::accumulate(v.begin(), v.end(), 0LL);

// Remove duplicates: must sort first, then erase-unique idiom
std::sort(v.begin(), v.end());
v.erase(std::unique(v.begin(), v.end()), v.end());

std::vector<std::vector<int>> dp(m, std::vector<int>(n, 0));

std::isalpha(c);   // is letter
std::isdigit(c);   // is digit (0-9)
std::isxdigit(c);  // is hex digit (0-9, A-F, a-f)
std::isalnum(c);   // is letter or digit
std::tolower(c);
std::toupper(c);

if (mp.count(key)) { /* exists */ }
if (mp.find(key) != mp.end()) { /* exists */ }
if (mp.contains(key)) { /* exists, C++20 */ }

// C++17 structured binding
auto [a, b] = std::make_pair(1, 2);
auto [x, y, z] = std::make_tuple(1, 2, 3);

std::swap(a, b);

int x = std::abs(n);
long long x = std::llabs(n);
double x = std::fabs(n);

// pow returns double; use static_cast when mixing with % operator
// Example: extract digit at position p from integer x
// pow is double, % is int - cannot mix directly
const int digit = (x / static_cast<int>(std::pow(10, p))) % 10;

double p = std::pow(base, exp);
double s = std::sqrt(n);

std::fill(v.begin(), v.end(), value);
std::memset(arr, 0, sizeof(arr));  // only works correctly for 0 or -1

// ===== Character Conversion =====

// ASCII arithmetic: '0'-'9' are contiguous (48-57)
int digit = c - '0';      // '7' -> 7
char c = digit + '0';     // 7 -> '7'

// Map lowercase to 0-25 index for frequency arrays
int idx = c - 'a';        // 'a' -> 0, 'z' -> 25
int idx = c - 'A';        // 'A' -> 0, 'Z' -> 25

// Manual case conversion using ASCII distance (32)
char upper = lower - 'a' + 'A';
char lower = upper - 'A' + 'a';

// ✅ 尾部插入 + reverse = O(n) (Note: 頭部插入 = O(n²) 陷阱)
s += c;                           // amortized O(1)
std::reverse(s.begin(), s.end()); // 最後一次 O(n)

// ===== String Operations =====

// O(1) space comparison - avoids creating temporary substring
// exactly compare at start_pos_s for target_length with target
if (s.compare(start_pos_s, target_length, target) == 0) { /* equals zero means matched */ }

size_t pos = s.find("pattern");
if (pos != std::string::npos) { /* found */ }
s.find("pattern", start_pos);      // search from position
s.rfind("pattern");                // search from right
s.find_first_of("aeiou");          // find any char in set

// ===== Tokenization: getline vs operator>>（皆可用於 C++14） =====
// 指定分隔字元：getline 不跳過前導／連續分隔符，可能產生空 token。
std::stringstream delimiterStream("a   b");
std::string token;
while (std::getline(delimiterStream, token, ' ')) { /* "a", "", "", "b" */ }
// getline(..., ' ') 只認空格；tab／換行不會因此被切開。
// 注意：最後一個分隔符之後若直接 EOF，不會額外成功讀出一個空 token。

// 讀取單字：>> 預設略過前導／連續 whitespace（空格、tab、換行），不產生空 token。
std::stringstream wordStream("a   b");
while (wordStream >> token) { /* "a", "b" */ }

// ⚠️ LC 819：非字母換成空格後，"a!!!" 會變成 "a   "。
// getline(..., ' ') 讀到 "a", "", ""；若把空字串計數，答案可能變成 ""。
// 單字統計優先用 >>；若用 getline，先略過空 token。
std::stringstream filteredStream(s);
while (std::getline(filteredStream, token, ' ')) {
    if (token.empty()) continue;
    /* process token */
}

// 逗號等自訂分隔符仍使用 getline；上面範例各用獨立 stream，避免重用已讀到 EOF 的 stream。
std::stringstream commaStream(s);
while (std::getline(commaStream, token, ',')) { /* process token */ }
// For paths, use '/' as delimiter; repeated '/' can produce empty tokens.
std::stringstream pathStream("/a//b");
while (std::getline(pathStream, token, '/')) { if (token.empty()) continue; /* process token */ }

// ===== getline 成功狀態與 token 內容（LC 165；C++14） =====
// getline 回傳 stream；轉 bool 檢查本次讀取成功，不是檢查數字轉換成功。
// 下列兩行假設：成功讀到的欄位是非空、可由 stoi 解析的整數；缺欄位補 0。
bool has1 = static_cast<bool>(std::getline(ss1, token1, '.'));
const int num1 = !has1 ? 0 : std::stoi(token1);
// 成功時才使用本次 token；失敗時 token 不保證清空，可能保留舊值。
// 一般分隔輸入也可能成功讀到空 token（如 "a..b"）；has1 不保證 token 非空或是合法數字。
// 最後一段可以成功讀到並同時設 eofbit；不要用 !ss.eof() 取代本次成功判斷。

// 兩個 stream 每輪都要各讀一次，不能把兩次 getline 放在 || 兩側：左成功會短路右邊。
// while (std::getline(ss1, token1, '.') || std::getline(ss2, token2, '.'))
bool has2 = static_cast<bool>(std::getline(ss2, token2, '.'));
// if (!has1 && !has2) break; // 放在讀取迴圈內：雙方都無資料才結束。
const int num2 = !has2 ? 0 : std::stoi(token2);

// Parse with specified base (2=binary, 16=hex)
int bin = std::stoi("1010", nullptr, 2);   // -> 10
int hex = std::stoi("FF", nullptr, 16);    // -> 255

// ===== Numeric Operations =====

// 0-indexed prefix sum
std::partial_sum(v.begin(), v.end(), prefix.begin());
// 1-indexed prefix sum (prefix[0] = 0 for easier range queries)
std::partial_sum(v.begin(), v.end(), prefix.begin() + 1);

// Product of all elements
long long product = std::accumulate(v.begin(), v.end(), 1LL, std::multiplies<long long>());

// Check if two ranges are equal
bool eq = std::equal(v1.begin(), v1.end(), v2.begin());

int cnt = std::count(v.begin(), v.end(), target); // 可以直接找目標，不用寫 predicate
int cnt = std::count_if(v.begin(), v.end(), [](int x) { return x > 0; });

// Fill with incrementing sequence starting from 0
std::iota(v.begin(), v.end(), 0);

// Use member lower_bound for set/map - O(log n) vs O(n) for std::lower_bound
auto it = s.lower_bound(target);
auto it = m.lower_bound(key);

// Extract lowest set bit (useful for Fenwick tree)
int lowbit = n & (-n);

// Promote before multiply to avoid overflow
long long result = 1LL * a * b;

// Safe midpoint calculation (avoids left + right overflow)
int mid = left + (right - left) / 2;

// Modular subtraction: add MOD to handle negative result
int result = ((a - b) % MOD + MOD) % MOD;

// Use numeric_limits for type-safe min/max initialization
int minVal = std::numeric_limits<int>::max();
int maxVal = std::numeric_limits<int>::min();

// std::min / std::max require both arguments to be the same type
// Common pitfall: container.size() is size_t (unsigned), not int
int n = std::min((int)v.size(), 5);       // Option 1: Cast size to int
int m = std::max<int>(v.size(), 5);       // Option 2: Explicit template argument

// ===== Random Numbers =====

// 均勻分布、modulo bias 與拒絕採樣：CPP_Reference/Algorithm/Uniform_Random_Sampling.md
// Modern C++ random (recommended for production)
std::mt19937 rng(std::random_device{}());
std::uniform_int_distribution<int> dist(1, 100);
int val = dist(rng);

// Fisher-Yates shuffle
std::shuffle(v.begin(), v.end(), rng);

// ✅ 零初始化（所有元素為 0）
std::array<int, 5> arr{};

// std::array<int, 5> arr(0);
// std::array 沒有這種構造函數，因此會報錯
// array initializer must be an initializer list（陣列初始化器必須是大括號清單）
// 因為 std::array 在 C++ 中是一個聚合類別（Aggregate Class）
// 它內部包裝的是標準的 C 語言風格陣列，沒有提供接受單一數值的構造函數（Constructor）
```
