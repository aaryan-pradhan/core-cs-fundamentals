# Lecture 23: Solving LeetCode Problems on Concurrency

- Previous lectures: threads, multithreading, the bugs thread synchronization causes (race conditions, deadlock). Creating threads is easy; the hard part is synchronizing them around critical sections.
- This lecture: solve concurrency problems on LeetCode and submit them, to see how threads are synchronized in real code.
- Language here is C++. Syntax is not the point (Python/Java have their own methods); focus on the synchronization logic.

③ → three problems:

## ① Print order

- LeetCode 1114, "Print in Order" (easy).
- Problem: class `Foo` has three methods `first()`, `second()`, `third()`; each only prints ("first", "second", "third").
- The same instance of `Foo` is passed to three different threads: thread A calls `first()`, thread B calls `second()`, thread C calls `third()`.
- Design a mechanism so that `second()` runs only after `first()`, and `third()` only after `second()`, whatever the order the threads are scheduled in.
- Unlike normal DSA problems: there one thread calls the functions one after another (sequential). Here three threads run in parallel.

```
                       ┌──→ T1 ──→ foo1.first()
foo ──→ obj ──→ [foo1] ┼──→ T2 ──→ foo1.second()
                       └──→ T3 ──→ foo1.third()
```

- Why it breaks without sync: assume 3 CPUs; all three threads get a CPU at t = 0 and run independently. Nobody knows which prints first.
  - Running the bare code: once it printed "first second third" by chance; on the next run it printed "first third second". Expected is always "first second third".

### locks & conditional variable

- Condition variable (recap): a thread waits on some condition; another thread makes the condition true and notifies; then the waiting thread moves ahead. (Revise the condition variable lecture if unclear.)

1. first → printfirst() → T1 execute.
2. when first is printed → T2 execute.
   - So T2 waits on a condition, and T1 makes that condition true (after printing "first") and notifies T2. Same between T2 and T3.

- Take a mutex `m`, a condition variable `cv`, and an `int turn`.
- `turn` → decide turn: it decides whose turn it is (which thread may run now). Initially `turn = 0`, because "first" should print first.

```cpp
class Foo {
    std::mutex m;
    std::condition_variable cv;
    int turn;              // decide turn
public:
    Foo() {
        turn = 0;
    }

    void first(function<void()> printFirst) {           // T1

        // printFirst() outputs "first". Do not change or remove this line.
        printFirst();
        turn = 1;
        cv.notify_all();
    }

    void second(function<void()> printSecond) {         // T2
        std::unique_lock<std::mutex> lock(m);
        while(turn != 1){
            cv.wait(lock);
        }
        // printSecond() outputs "second". Do not change or remove this line.
        printSecond();
        turn = 2;
        cv.notify_all();
    }

    void third(function<void()> printThird) {           // T3
        std::unique_lock<std::mutex> lock(m);
        while(turn != 2){
            cv.wait(lock);
        }
        // printThird() outputs "third". Do not change or remove this line.
        printThird();
    }
};
```

- How it works (all three threads run concurrently):
  1. `first()` has no condition. T1 prints "first", sets `turn = 1`, calls `cv.notify_all()`.
  2. Meanwhile T2 locks `m` and checks `while (turn != 1)`. At the start `turn` is 0, so this is true and T2 goes to `cv.wait(lock)` (wait releases the lock while waiting).
  3. T3 does the same: `turn != 2` is true at the start, so T3 also waits.
  4. On `notify_all()` both wake up, re-lock and re-check their `while` condition.
     - T2: `turn` is now 1, so `turn != 1` is false; T2 leaves the loop, prints "second", sets `turn = 2`, notifies all.
     - T3: `turn` is 1, so `turn != 2` is still true; T3 goes back to waiting.
  5. After T2's notify, T3 re-checks: `turn != 2` is false, so it prints "third".
- The `while` holds the condition the "wrong way round": it keeps the thread waiting while it is NOT its turn.
- So whatever way the threads are scheduled, the output is always first, second, third. Submitted: accepted.
- Safer version of `first()`: also take the lock before changing `turn` (`std::unique_lock<std::mutex> lock(m);` as its first line). Without it, `turn = 1` plus the notify can land between T2's check of `turn` and its `cv.wait()`, and T2 then sleeps through the only notification.

## ② → Fizz buzz problem

- LeetCode 1195, "Fizz Buzz Multithreaded".
- Single-threaded FizzBuzz: loop `i` from 1 to n:
  - divisible by 3 and 5 → print "fizzbuzz"
  - divisible by 3, not by 5 → print "fizz"
  - divisible by 5, not by 3 → print "buzz"
  - else → print `i`
  - e.g. n = 15: 3 → fizz, 5 → buzz, 15 → fizzbuzz. One loop with if/else does it.
- Multithreaded version: class `FizzBuzz` has four functions, each called by a different thread, all running concurrently:
  - A calls `fizz()` → may only print "fizz"
  - B calls `buzz()` → may only print "buzz"
  - C calls `fizzbuzz()` → may only print "fizzbuzz"
  - D calls `number()` → may only print the integer
- Problem: the counter `i` (1 to n) becomes a shared variable across all four functions, so access to it must be synchronized, and each value must be printed by the right thread.
- Approach: same as the previous problem. One mutex, one condition variable, and a shared `i` starting at 1. Every function runs a `while (i <= n)` loop (each thread runs its own loop); the threads take turns incrementing `i`.

```cpp
class FizzBuzz {
private:
    int n;
    mutex m;
    condition_variable c;
    int i;
public:
    FizzBuzz(int n) {
        this->n = n;
        this->i = 1;
    }

    // printFizz() outputs "fizz".
    void fizz(function<void()> printFizz) {               // A
        while(i<=n){
            {
                unique_lock<mutex> lock(m);
                while(i<=n && (((i%3) == 0) && ((i%5) != 0)) == 0) {
                    c.wait(lock);
                }
                if(i<=n){
                    printFizz();
                    ++i;
                }
                c.notify_all();
            }
        }
    }

    // printBuzz() outputs "buzz".
    void buzz(function<void()> printBuzz) {               // B
        while(i<=n){
            {
                unique_lock<mutex> lock(m);
                while(i<=n && (((i%5) == 0) && ((i%3) != 0)) == 0) {
                    c.wait(lock);
                }
                if(i<=n){
                    printBuzz();
                    ++i;
                }
                c.notify_all();
            }
        }
    }

    // printFizzBuzz() outputs "fizzbuzz".
    void fizzbuzz(function<void()> printFizzBuzz) {       // C
        while(i<=n){
            {
                unique_lock<mutex> lock(m);
                while(i<=n && (((i%5) == 0) && ((i%3) == 0)) == 0) {
                    c.wait(lock);
                }
                if(i<=n){
                    printFizzBuzz();
                    ++i;
                }
                c.notify_all();
            }
        }
    }

    // printNumber(x) outputs "x", where x is an integer.
    void number(function<void(int)> printNumber) {        // D
        while(i<=n){
            {
                unique_lock<mutex> lock(m);
                while(i<=n && (((i%5) != 0) && ((i%3) != 0)) == 0) {
                    c.wait(lock);
                }
                if(i<=n){
                    printNumber(i++);
                }
                c.notify_all();
            }
        }
    }
};
```

- Reading the wait condition, e.g. in `fizz()`:
  - `((i%3) == 0) && ((i%5) != 0)` is 1 exactly when it is fizz's turn (divisible by 3, not by 5).
  - `(...) == 0` means "not my turn" → wait. When it is fizz's turn the expression is `1 == 0` = false, and the thread leaves the wait loop.
  - Same "opposite condition" trick as before: the `while` states when to keep waiting.
  - `i <= n` is also in the wait condition so that, once `i` passes n, waiting threads stop waiting and exit.
  - `if (i <= n)` guards against printing after the last number.
- Dry run:
  1. `i = 1`. A: `1%3 == 0` is false → expression 0 → `0 == 0` true → A waits. B and C also get 0 → wait.
  2. D: 1 is divisible by neither → expression 1 → `1 == 0` false → D does not wait. Prints 1, `i++` → 2.
  3. `i++` always happens inside the critical section; no other thread touches `i` then, because all others are waiting.
  4. D calls `c.notify_all()`. A, B, C wake, re-check with `i = 2`: still not their turn → back to waiting. D's own check passes again → prints 2, `i = 3`, notify all.
  5. `i = 3`: now D's condition makes it wait; A's condition becomes `1 == 0` false → A prints "fizz", `++i` → 4, notify all.
  6. `i = 4`: D works again, the rest wait. And so on.
- The condition variable lets all four threads be scheduled, but only the right thread does the work for each `i`. Ran for n = 15: correct. Submitted: accepted.

## ③ Dining philosopher's problem

- video no. 20 (revise Lecture 20 before this solution: what the problem is and why deadlock happens).
- LeetCode 1226, "The Dining Philosophers".
- Five philosophers (ids 0 to 4) alternately think and eat; five forks; a philosopher needs both the left and right fork to eat.
- Deadlock (recap): if every philosopher picks his left (or every one his right) fork, nobody can get a second fork and nobody eats.
- LeetCode framing: `wantsToEat(philosopher, pickLeftFork, pickRightFork, eat, putLeftFork, putRightFork)`.
  - `pickLeftFork` / `pickRightFork` pick up that fork.
  - Call `eat` only once the philosopher holds both forks.
  - After eating, call `putLeftFork` / `putRightFork` (put both forks down); he goes back to thinking and other philosophers can use those forks.
  - Five threads, one per philosopher, all calling `wantsToEat` on the same object.
- Approach: use the Lecture 20 tweak of picking up both forks inside a critical section. A philosopher gets to eat only if he can pick both forks; if he cannot get the right fork, he does not hold the left one either.
- C++ (before C++20) had no semaphore available, so a custom `Semaphore` class is written using a mutex and a condition variable (same logic as the semaphore lecture):
  - `wait()`: `count--`; if `count < 0`, wait.
  - `signal()`: `count++`; if `count <= 0`, `notify_one()`.
- Each fork is a binary semaphore (`setCount(1)`).

```cpp
class Semaphore
{
public:
    Semaphore() {}
    Semaphore(int c) : count(c){};

    void setCount(int a)
    {
        count = a;
    }

    inline void signal()
    {
        std::unique_lock<std::mutex> lock(mtx);
        count++;
        if(count <= 0)
            cv.notify_one();
    }

    inline void wait()
    {
        std::unique_lock<std::mutex> lock(mtx);
        count--;
        while (count < 0)
        {
            cv.wait(lock);
        }
    }

private:
    std::mutex mtx;
    std::condition_variable cv;
    int count;
};

class DiningPhilosophers {
    Semaphore fork[5];
    std::mutex m, l;
public:
    DiningPhilosophers() {
        for (int i = 0; i < 5; ++i) {
            fork[i].setCount(1);
        }
    }

    void wantsToEat(int philosopher,
                    function<void()> pickLeftFork,
                    function<void()> pickRightFork,
                    function<void()> eat,
                    function<void()> putLeftFork,
                    function<void()> putRightFork) {
        {
            std::lock_guard<std::mutex>lock(m);
            fork[(philosopher + 1) % 5].wait();
            fork[philosopher].wait();
        }
        pickLeftFork();
        pickRightFork();

        eat();

        putLeftFork();
        fork[(philosopher + 1) % 5].signal();
        putRightFork();
        fork[philosopher].signal();
    }
};
```

- How it works:
  - Picking is the critical section (guarded by `m`), so only one thread at a time can be picking forks; it comes out holding both the left and the right fork.
  - Then it picks both, eats, puts the left fork down and signals it, puts the right fork down and signals it. So one philosopher is taken fully into the eating state and back out.
  - e.g. P0 is inside and gets both forks. P1 then enters the critical section; P0 holds a fork P1 needs, so P1 waits there until P0 puts it down. The others wait for the mutex meanwhile. Whoever gets in gets both forks, so the deadlock condition (each holding one fork, waiting for the other) cannot occur.
  - The custom semaphore's `while (count < 0)` is safe here because every `wait()` happens while holding `m`, so at most one thread ever waits on a given fork.
- Ran and submitted: accepted.
- Homework: on this LeetCode problem, try the other tweaks from Lecture 20 and check whether they also work.
- All three problems were solved with condition variables (here the semaphore itself is custom, built from a condition variable).
- Interview tip: "how will you build your own semaphore?" can be asked; build it with a mutex and a condition variable as above.
- Coding rounds rarely ask concurrency coding directly; it comes up in discussion (e.g. "how will you solve dining philosophers?").

## Part 2: More LeetCode concurrency problems (last lecture of the course)

- A bonus lecture at the very end of the course: three more LeetCode concurrency problems.
- Advice: read each problem and try it yourself before seeing the solution; it trains you to think about how threads interact and how to synchronize them.

### ④ Print FooBar Alternately

- LeetCode 1115.
- Problem: class `FooBar` has `foo()` (loop n times, print "foo") and `bar()` (loop n times, print "bar"). The same instance is passed to two threads: T1 calls `foo()`, T2 calls `bar()`. Output must be "foobar" repeated n times.
- Single thread: just print foo, bar, foo, bar. With two threads the order must be T1, T2, T1, T2, …: T2 prints "bar" only after T1 printed "foo", and T1 prints the next "foo" only after T2 printed "bar".
- Without sync: n = 1 printed correctly by chance (the foo thread was started first and got scheduled first). For n = 10 it printed foo ten times, then bar ten times: T1 got scheduled first and finished its whole loop.
- Approach: mutex + condition variable + a `bool turn` (0 = foo's turn, 1 = bar's turn), initially 0.

```cpp
class FooBar {
private:
    int n;
    mutex m;
    condition_variable cv;
    bool turn;             // 0 = foo's turn, 1 = bar's turn

public:
    FooBar(int n) {
        this->n = n;
        turn = 0;
    }

    void foo(function<void()> printFoo) {
        for (int i = 0; i < n; i++) {
            unique_lock<mutex> lock(m);
            while (turn == 1) {
                cv.wait(lock);
            }
            // printFoo() outputs "foo". Do not change or remove this line.
            printFoo();
            turn = 1;
            cv.notify_all();
        }
    }

    void bar(function<void()> printBar) {
        for (int i = 0; i < n; i++) {
            unique_lock<mutex> lock(m);
            while (turn == 0) {
                cv.wait(lock);
            }
            // printBar() outputs "bar". Do not change or remove this line.
            printBar();
            turn = 0;
            cv.notify_all();
        }
    }
};
```

- How it works:
  1. Initially `turn = 0`, so T2 (bar) locks, sees `turn == 0`, and waits. `cv.wait` releases the lock and keeps waiting until another thread notifies.
  2. T1 locks, `turn == 1` is false, prints "foo", sets `turn = 1`, calls `notify_all()`. The notify is essential: without it T2 would wait forever.
  3. T2 wakes, re-locks, re-checks: `turn` is 1, not 0, so it prints "bar", sets `turn = 0`, notifies. T1 was waiting (its turn was 1); it wakes and prints "foo" again.
  4. So the threads run T1, T2, T1, T2, … instead of randomly. Submitted: accepted.
- Same pattern extends to more than two threads that must run in sequence (T1, T2, T3, T4, …).

### ⑤ Print Zero Even Odd

- LeetCode 1116.
- `printNumber(x)` prints integer x. It is a `function<void(int)>` (C++ `std::function`, behaves like a function pointer).
- Problem: class `ZeroEvenOdd` with `zero()`, `even()`, `odd()`; the same instance goes to three threads: thread A calls `zero()` (prints only 0), B calls `even()` (prints only even numbers), C calls `odd()` (prints only odd numbers). Output must be `0 1 0 2 0 3 …` up to n (1 ≤ n ≤ 1000).
  - n = 2 → `0102`; n = 5 → `0102030405`.
- Single thread: loop 1 to n, print 0 then the number. Here 0 must come from the zero thread, odd numbers from the odd thread, even numbers from the even thread.
- No practical use; it exists to teach synchronizing three threads.
- Approach: mutex + condition variable (a thread waits on a condition until another thread tells it to continue: that is synchronization) + `int turn` (0 = zero's turn, 1 = odd's turn, 2 = even's turn) + `int i` going from 1 to n.
- The zero thread decides who goes next: after printing 0 it sets `turn = 1` if `i` is odd, `turn = 2` if `i` is even.

```cpp
class ZeroEvenOdd {
private:
    int n;
    mutex m;
    condition_variable cv;
    int turn;              // 0 = zero, 1 = odd, 2 = even
    int i;

public:
    ZeroEvenOdd(int n) {
        this->n = n;
        turn = 0;
        i = 1;
    }

    // printNumber(x) outputs "x", where x is an integer.
    void zero(function<void(int)> printNumber) {
        while (i <= n) {
            unique_lock<mutex> lock(m);
            while (turn != 0 && i <= n) {
                cv.wait(lock);
            }
            if (i > n) break;
            printNumber(0);
            if (i % 2 == 0) turn = 2;
            else turn = 1;
            cv.notify_all();
        }
    }

    void even(function<void(int)> printNumber) {
        while (i <= n) {
            unique_lock<mutex> lock(m);
            while (turn != 2 && i <= n) {
                cv.wait(lock);
            }
            if (i > n) break;
            printNumber(i);
            i++;
            turn = 0;
            cv.notify_all();
        }
    }

    void odd(function<void(int)> printNumber) {
        while (i <= n) {
            unique_lock<mutex> lock(m);
            while (turn != 1 && i <= n) {
                cv.wait(lock);
            }
            if (i > n) break;
            printNumber(i);
            i++;
            turn = 0;
            cv.notify_all();
        }
    }
};
```

- Dry run for n = 2:
  1. All three start; `turn = 0`, `i = 1`. Odd sees `turn != 1` → waits. Even sees `turn != 2` → waits. Zero gets the chance: prints 0.
  2. Zero does not change `i`. `i = 1` is odd → `turn = 1`. `notify_all()` (essential) reaches both even and odd threads.
  3. Even re-checks: `turn != 2` true → back to waiting. Odd: `turn != 1` false → prints 1, `i++` → 2, sets `turn = 0`, notifies all.
  4. Zero wakes, prints 0; `i = 2` is even → `turn = 2`, notify. Even thread prints 2, `i++` → 3, `turn = 0`, notify.
  5. Exit: `i = 3 > n`. Zero wakes: `turn != 0` is false, so it leaves the wait loop; `if (i > n)` is true → `break`, zero thread exits. Even and odd also get the notification: `i <= n` is now false, so they leave the wait loop, hit `break`, and exit.
- So after everything is printed, all three threads exit. Tested with n = 2 and n = 67; submitted: accepted.
- The `turn` variable carries most of the responsibility: it decides which thread runs.
- To understand it, trace small cases by hand; keeping concurrent value changes in your head takes practice.

### ⑥ Building H2O

- LeetCode 1117.
- Two kinds of threads: oxygen and hydrogen; each thread is one atom. Goal: group them into water molecules.
- Threads pass a barrier in complete sets: each set of three is one oxygen and two hydrogen (in any order: HHO, HOH, OHH). You do not have to match specific threads to each other.
- `releaseHydrogen()` prints "H", `releaseOxygen()` prints "O".
- Input arrives in any order, e.g. `OOHHHH` (4 H threads, 2 O threads), not sequential.
- Approach: give the chance to two hydrogen threads, then to one oxygen thread, then two hydrogen, then one oxygen, and so on. Mutex + condition variable + `int turn` (number of H released in the current molecule), initially 0.

```cpp
class H2O {
private:
    mutex m;
    condition_variable cv;
    int turn;              // H atoms released for the current molecule

public:
    H2O() {
        turn = 0;
    }

    void hydrogen(function<void()> releaseHydrogen) {
        unique_lock<mutex> lock(m);
        while (turn == 2) {
            cv.wait(lock);
        }
        // releaseHydrogen() outputs "H". Do not change or remove this line.
        releaseHydrogen();
        turn++;
        cv.notify_all();
    }

    void oxygen(function<void()> releaseOxygen) {
        unique_lock<mutex> lock(m);
        while (turn < 2) {
            cv.wait(lock);
        }
        // releaseOxygen() outputs "O". Do not change or remove this line.
        releaseOxygen();
        turn = 0;
        cv.notify_all();
    }
};
```

- How it works:
  1. Start: `turn = 0`. The first H thread locks, enters the critical section, `turn == 2` is false → releases hydrogen, `turn++` → 1, notifies.
  2. O threads that arrive meanwhile lock and see `turn < 2` → wait. `cv.wait` unlocks the lock while waiting, which is what lets the H threads get in.
  3. The second H thread sees `turn = 1` → releases hydrogen, `turn` → 2, notify all.
  4. A third H thread arriving now sees `turn == 2` → waits.
  5. An O thread wakes, `turn < 2` is false → releases oxygen, sets `turn = 0` (one water molecule is done), notify all.
  6. The waiting H thread can now go. Pattern: H, H, O, H, H, O, … Tested with small and larger inputs; submitted: accepted.
- Like making water in real life: release two hydrogen atoms, then one oxygen atom, and you get one molecule.

### Conclusion

- All six concurrency problems use the same few things: a mutex (lock), condition variable(s), and a `turn`-style variable that decides which thread gets the chance to run.
