# C++ 同步處理必備 std

本文以 **C++14** 為基準，整理實作 Producer–Consumer（產生資料／取用資料的執行緒分工）、Thread-safe Queue 與 Ring Buffer 需要的標準函式庫。先讀 one-liner 與註解，再看需要多個步驟的同步範例。

## 1. 先記工具的責任

| 工具 | 用途 |
|:---|:---|
| `std::thread`／`join()` | 啟動工作／等待工作結束 |
| `std::mutex` | 讓共享狀態的操作互斥，建立同步關係 |
| `std::lock_guard<std::mutex>` | 進入 scope 上鎖，離開時解鎖；一般 critical section 優先用它 |
| `std::unique_lock<std::mutex>` | 可暫時解鎖、重新上鎖；搭配 condition variable |
| `std::condition_variable` | 條件未滿足時休眠，收到通知後重新檢查 |
| `std::atomic<T>` | 對單一物件做原子讀寫／read-modify-write |

```cpp
#include <thread>             // thread、this_thread
#include <mutex>              // mutex、lock_guard、unique_lock、lock、call_once
#include <condition_variable> // condition_variable
#include <atomic>             // atomic
#include <functional>         // ref：將參數以 reference 傳進 thread
#include <chrono>             // milliseconds、steady_clock
```

## 2. `thread`／`join`：啟動與收尾

### 2.1 用 lambda capture：在 worker 裡存取外面的變數

```cpp
int result = 0;
std::thread worker([&] { result = 42; }); // 建立新執行緒，執行傳入的 lambda
// [&] 以 reference 存取外面的 result；result 必須活到 worker 使用完畢。
// worker 何時取得 CPU 由 OS 排程決定；主執行緒也繼續往下，worker 可能先完成。
bool needsJoin = worker.joinable();      // true；表示仍有可 join／detach 的執行緒關聯，不代表還在執行
worker.join();                          // 主執行緒等 worker 完成；若已完成，就不必再等它執行
int received = result;                  // 42；成功 join 返回後，可以安全讀取 worker 的這次寫入
// joinable() 本身不等待；join() 才等待。成功 join 後，worker.joinable() 變成 false。

// 執行時序：兩種情況都合法。
// A：主執行緒先抵達 join → 等待；worker 寫入 42 並結束後，主執行緒才繼續。
// B：worker 先寫入 42 並結束 → 主執行緒稍後呼叫 join，完成收尾後繼續。
// 共同保證：join 成功返回時，worker 已完成，其寫入對呼叫端可見。
```

### 2.2 傳入 callable 與參數：用 std::ref 保留原物件

```cpp
int value = 0;
auto increment = [](int& x) { ++x; };           // callable 接受 int&，修改傳入的物件
std::thread worker(increment, std::ref(value)); // worker 執行 increment，參數指向原本的 value
// 建構子 signature：template<class F, class... Args> explicit thread(F&& f, Args&&... args);
// 第一個參數 f 是 callable（increment）；其餘 args... 是傳給它的參數（std::ref(value)）。
// 此例使用 std::ref(value)，讓 increment 的 int& 綁到原本的 value；直接傳 value 無法滿足這個 int& 參數。
worker.join();                                // value == 1；value 的生命週期涵蓋整段 worker 執行

// 傳參數原理：
// F&&／Args&&... 是 forwarding references；C++14 的 thread 內部保存 callable 與參數經 decay 後的值。
// 一般參數會複製／移動；std::ref(value) 回傳 reference_wrapper<int>，wrapper 本身也會被複製。
// 呼叫 increment 時，wrapper 可轉成 int&，因此仍操作原本的 value；它不擁有 value，也不延長其生命週期。
// [&] 從 lambda 的 capture 取得外部物件；std::ref 則用在 thread 的參數傳遞，兩者的入口不同。
```

### 2.3 多個 workers：先啟動，再逐一 join

以下用兩個可無參數呼叫的 lambda 代表工作；兩個區塊各自獨立。

```cpp
auto taskA = [] { /* 工作 A */ };
auto taskB = [] { /* 工作 B */ };
std::thread a(taskA); // 啟動 A
a.join();           // 主執行緒等 A 完成，才會執行下一行
std::thread b(taskB); // A 已完成，現在才啟動 B
b.join();            // 等 B 完成；兩份工作的執行期間不會重疊
```

```cpp
auto taskA = [] { /* 工作 A */ };
auto taskB = [] { /* 工作 B */ };
std::thread a(taskA); // 啟動 A
std::thread b(taskB); // 啟動 B；此時 A 可能還在執行，兩份工作有機會重疊
a.join();           // 主執行緒等 A；B 仍可繼續執行
b.join();            // 再確認 B 也完成；若 B 已完成，就不必再等它執行
// join 的呼叫順序不保證 workers 的執行／完成順序；B 可能比 A 更早完成。
// 實際能否同時使用不同 CPU 核心，還取決於硬體與 OS 排程。
```

<a id="thread-lifecycle"></a>

### 2.4 Thread 生命週期與程式終止

**thread 物件解構時若仍 `joinable()`，會呼叫 `std::terminate()`，預設終止整個程式。** 記得在離開 scope 前 `join()`；即使 worker 已執行完，也仍需收尾（成功 `detach()` 亦會解除關聯）。

以下是 **GCC libstdc++ 標準庫原始碼節錄**，條件是 `joinable()` 為 true；`std::__terminate()` 是該實作的內部入口，這段不能直接放進使用者的 `main`。

```cpp
~thread()
{
  if (joinable())
	std::__terminate();
}
```

- [原始碼：std_thread.h，固定 commit](https://github.com/gcc-mirror/gcc/blob/173072492587491dea9e2b0a9d02da9e4dff2c65/libstdc%2B%2B-v3/include/bits/std_thread.h#L181-L185)。
- [標準契約：thread destructor](https://eel.is/c++draft/thread.thread.destr)。

### 2.5 C++ Thread 常見陷阱

Data race 指缺乏同步的共享記憶體衝突存取（至少一方寫入、至少一方非 atomic），會造成 undefined behavior（語言不保證結果）；deadlock 指工作互相等待而無法前進。

| 容易誤會 | 實際後果 | 正確做法 |
|:---|:---|:---|
| worker 做完就不用管了 | thread 物件仍 joinable，解構時觸發 terminate | 離開 scope 前 `worker.join()`；詳見 [2.4](#thread-lifecycle) |
| 最後 join，期間就能放心修改共享資料 | 兩個 workers 仍可能同時修改資料，產生 data race | 共享讀寫用同一把 mutex 保護；見第 3 節 |
| 拿著 mutex 等 worker 完成沒關係 | worker 若也需要這把鎖，雙方會互等 | 先離開持鎖 scope，再 `join()` |
| detach 後，區域變數也會跟著活著 | worker 可能存取已被銷毀的變數 | 引用區域變數時，優先在它銷毀前 `join()` |

## 3. `mutex`＋RAII：選擇鎖的管理方式

**RAII（Resource Acquisition Is Initialization）** 用物件生命週期管理資源的取得與釋放，離開 scope 時自動收尾；此處的 scope 是 `{ ... }` 區塊，ownership 是持鎖與負責解鎖的管理責任。Critical section 是持鎖保護共享資料的程式區段。

**兩者都是 RAII：`lock_guard` 在整個 scope 持鎖；`unique_lock` 追蹤持鎖狀態，期間可釋放、重取或移交 ownership。** 兩者管理的是鎖定狀態，不負責銷毀 mutex。

```cpp
std::mutex m;
{ std::lock_guard<std::mutex> guard(m); } // scope 守衛：建構時上鎖，離開 scope 就解鎖
{ std::unique_lock<std::mutex> lock(m); } // 唯一 ownership：此例同樣自動收尾，也支援中途調整持鎖狀態
// 兩個例子各用獨立 scope；不可在持鎖時再次鎖住同一把 std::mutex。
```

一般 critical section 優先使用 `lock_guard`；需要中途解鎖、延遲上鎖或搭配 `condition_variable` 時，使用 `unique_lock`。

### 3.1 `lock_guard`：scope 內持鎖，自動解鎖

```cpp
std::mutex m; int count = 0;
auto increment = [&] {
    std::lock_guard<std::mutex> guard(m);
    ++count;
}; // 此例更新 count；若有依 count 決定後續操作的檢查，也要放在同一段鎖內

std::thread a(increment), b(increment);
a.join(); b.join(); // count == 2；兩個 workers 的 ++ 由同一把 mutex 保護

// guard 建構時 lock，解構時 unlock：RAII 讓 return／例外離開 scope 也會釋放鎖。
// mutex 必須是大家共用的同一把；每個函式自己建立一把 local mutex 無法保護同一份資料。
// 讀共享的非 atomic 狀態也要遵守相同鎖定規則；只鎖「寫入」仍可能有 data race（undefined behavior）。
// mutex 不只避免同時修改；同一把 mutex 的 unlock 與後續成功 lock 也建立記憶體可見性的同步。
```

```cpp
std::mutex m; int count = 0;
{
    std::lock_guard<std::mutex> guard(m);
    ++count;
} // scope 結束即解鎖，後面的耗時工作可放在鎖外

// 使用 m.lock(); ...; m.unlock(); 容易在 early return／例外時漏 unlock，日常優先使用 RAII。
// C++14 要明寫 <std::mutex>；std::lock_guard guard(m) 的型別推導是 C++17。
// lock_guard 沒有 unlock()；也不要直接 m.unlock()，否則 guard 解構會再次 unlock。
```

### 3.2 `unique_lock`：追蹤 ownership，可調整持鎖狀態

```cpp
std::mutex m;
std::unique_lock<std::mutex> lock(m);          // 立即上鎖；lock 物件記錄自己是否持有鎖
bool owns = lock.owns_lock();                 // true；只說明這個 lock 物件的 ownership
lock.unlock();                               // 暫時釋放；必須原本就持鎖
lock.lock();                                 // 再取得 mutex；離開 scope 時仍由 RAII 收尾
// lock／unlock 是 unique_lock 的 member；它需要追蹤 ownership，別繞過它直接操作 m。
```

```cpp
std::mutex m;
std::unique_lock<std::mutex> lock(m, std::defer_lock); // 先綁定 mutex，不上鎖
lock.lock();                                        // 稍後才取得鎖
lock.unlock();                                      // 釋放後，才能示範下一次嘗試
bool acquired = lock.try_lock();                    // 嘗試一次；即使鎖當下可用，也允許回傳 false（假性失敗）

// 只有 acquired==true 時才能存取受保護狀態；離開 scope 時只在持鎖時自動 unlock。
// try_lock 不是「保證立刻成功」；不要在持有同一把鎖時再對它嘗試上鎖。
```

## 4. `condition_variable`：等待的是條件，不是通知本身

以下是一次資料交接；`ready` 與 `value` 都由同一把 `m` 保護。

```cpp
std::mutex m;
std::condition_variable cv;

bool ready = false;
int value = 0;

std::thread producer([&] {
    {
        std::lock_guard<std::mutex> guard(m);
        value = 42;
        ready = true;
    } // 先在鎖內更新狀態
    cv.notify_one(); // 喚醒最多一個 waiter；此處選擇解鎖後通知，鎖內通知也合法
});
// producer 不需要等待條件，只在 scope 內更新資料，因此可以使用 lock_guard。

int received; // 主執行緒在這裡扮演 consumer，等待 producer 準備資料
{
    std::unique_lock<std::mutex> lock(m); // RAII 取得鎖；wait 會暫時解鎖／重新上鎖
    cv.wait(lock, [&] { return ready; }); // true 才繼續；false 時原子地「解鎖＋進入等待」
    received = value;                    // 42；wait 返回時已重新取得 mutex，可讀共享資料
} // lock 解構，自動解鎖；不需要手動 unlock
// consumer 這裡必須用 unique_lock 等待時釋放 m，producer 才能取得同一把 m 並更新 ready／value
// 醒來後重新取得 m 才能檢查／讀取。
// lock_guard 無法中途解鎖／重取，也不符合 cv.wait(unique_lock<mutex>&, predicate) 的參數型別。
producer.join();

// wait(lock, pred) 等價於 while (!pred()) wait(lock)，不是 if。
// spurious wakeup 指未收到通知也可能醒來；條件也可能被另一個 consumer 改掉，所以必須重新檢查。
// 若 producer 先完成，ready 已是 true，consumer 不必等待；正確性依靠狀態，不依靠通知被保存。
// notify 不會釋放 mutex，也不會保證被喚醒者立即執行；waiter 必須重新競爭並取得鎖。
// 同一個 cv 的並行 waiters 必須使用同一把 mutex；不要持有其他會阻礙條件成立的鎖再 wait。
```

```cpp
std::mutex m;
std::condition_variable cv;
bool ready = false;

std::unique_lock<std::mutex> lock(m); // 建構時已取得 m；下方 wait_for 只在等待期間暫時釋放它
bool ok = cv.wait_for(lock, std::chrono::milliseconds(2), [&] { return ready; }); // 無人設 ready，此例回傳 false
if (ok) {
    // 已持有 m，且 ready 已成立；可以安全使用受 m 保護的資料。
} else {
    // 已重新取得 m，但已逾時且 ready 仍不成立；仍持鎖，可回報或決定重試，不能假設資料已準備好。
}
// 兩條路徑此時都仍持有 mutex；到期後也必須重新取得鎖，wait_for 才會返回。
// 持鎖流程：建構 lock 取得 m → 等待時暫時放鎖 → 返回前重新持鎖 → lock 離開 scope 自動解鎖。
// timeout 不會讓 wait_for 帶著未上鎖的狀態返回；若 predicate 一開始就成立，則不必進入等待。
// predicate 版：true 表示條件成立；false 表示期限內未等到條件成立；返回時仍持鎖。
// 時限不是精準排程保證：醒來與重新取得 mutex 都可能延後返回。
```

## 5. `atomic`：單一原子操作與複合規則分開思考

```cpp
std::atomic<int> count{0};               // C++14 明確給初始值；不要假設預設建構已初始化數值
int before = count.fetch_add(1);        // 原子 read-modify-write（不可分割地讀取並更新）；before == 0，count 現在是 1
int snapshot = count.load();            // 1；取得當下快照，下一刻可能已改變
count.store(5);                         // 原子寫入 5
int previous = count.exchange(0);      // 原子替換；previous == 5，count 現在是 0
// count.store(count.load() + 1) 是兩次操作，兩個 threads 可能讀到同一舊值而遺失更新；用 fetch_add。
// 預設 memory order 是 seq_cst；先熟悉預設語義，再另外學 acquire／release／relaxed。
// 多個變數各自是 atomic，不代表跨變數的整組操作也具有原子性。
// volatile 不提供 thread synchronization；atomic 也不保證底層一定 lock-free。
```

## 6. 延伸速查：多把鎖與一次性初始化

### 6.1 `std::lock`：取得多把鎖，再交給 RAII 收尾

**`std::lock(a, b)` 成功返回時，呼叫端已持有兩把鎖。** 底層不必同時鎖住兩把，而是透過 `lock`／`try_lock`／`unlock` 協調取得過程，避免 deadlock。

若自己分開鎖，可能形成互等：

```text
Thread 1：拿到 a → 等 b
Thread 2：拿到 b → 等 a
結果：互相等待
```

```cpp
std::mutex a, b;
std::lock(a, b); // 取得兩把鎖；成功返回後，兩把都已持有
std::lock_guard<std::mutex> first(a, std::adopt_lock);  // 接管 a 的解鎖責任
std::lock_guard<std::mutex> second(b, std::adopt_lock); // 接管 b 的解鎖責任
// adopt = 接管：目前執行緒已持鎖，guard 沿用這個狀態並接管解鎖責任；建構時不再 lock，解構時 unlock。
// adopt_lock 不會替你檢查是否已持鎖；呼叫端必須確保前提成立，否則違反使用契約。
// 呼叫 std::lock 前，不可已持有其中一把 std::mutex；它也不保證整個程式的其他等待關係沒有 deadlock。
```

**`std::lock` 負責取得多把鎖，兩個 guards 負責 RAII 收尾。**

### 6.2 `call_once`：一次性初始化

`once_flag` 保存這組初始化的共用狀態；`call_once` 協調多個呼叫者，讓初始化最多成功完成一次，其餘呼叫者等待成功完成後才返回。

```cpp
std::once_flag flag;
// 多次 call_once 必須共用同一個 flag；不同 flag 各自管理一次成功初始化。
int initialized = 0;
auto initialize = [&] { ++initialized; };
std::thread a([&] { std::call_once(flag, initialize); }); // 同一 flag 對應一次成功的執行
std::thread b([&] { std::call_once(flag, initialize); });
a.join(); b.join(); // 此例初始化成功，initialized == 1
// 初始化丟例外時，call_once 會往外拋並允許重試；worker 內須處理例外，避免直接終止程式。
// flag 必須活到所有相關呼叫結束；每次重建 flag 就是新的初始化狀態。
// call_once 保護初始化流程；初始化後若多個 threads 繼續修改同一資料，仍需另外同步。
```

## 補充工具：sleep_for 延遲執行

`sleep_for` 常用於延遲下一次操作、控制重試間隔，或模擬耗時工作。

```cpp
std::this_thread::sleep_for(std::chrono::milliseconds(100)); // 讓呼叫它的 thread 暫停至少 100ms，實際可能更久
// 若主執行緒呼叫，暫停的就是主執行緒；worker 仍由 OS 排程執行。
// 睡醒只表示等待時間已過，不代表 worker 已完成；worker 可能工作較久，也可能尚未取得執行機會。
// 要確認 worker 完成，使用 worker.join()；要等共享狀態符合條件，使用 condition_variable。
```

## 參考來源

以下標準草案是持續更新的文件；本文只示範 C++14 已有的 API 用法。

- [Thread members](https://eel.is/c++draft/thread.thread.member)：join／joinable／detach。
- [Thread destructor](https://eel.is/c++draft/thread.thread.destr)、[terminate handler](https://eel.is/c++draft/exception.terminate)：joinable 解構規則與整個程式的異常終止。
- [Mutex requirements](https://eel.is/c++draft/thread.mutex.requirements.mutex)：互斥與同步契約。
- [lock_guard](https://eel.is/c++draft/thread.lock.guard)、[unique_lock](https://eel.is/c++draft/thread.lock.unique)：RAII 與 ownership。
- [condition_variable](https://eel.is/c++draft/thread.condition.condvar)：wait、predicate、通知與 timeout。
- [Atomic operations](https://eel.is/c++draft/atomics.types.operations)：原子操作與 lock-free 性質。
