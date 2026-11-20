# Lecture 23: Solving LeetCode Problems on Concurrency

Creating threads is easy. The hard part is synchronizing them around critical sections, to avoid bugs like race conditions and deadlock.

- **Goal:** Solve concurrency problems on LeetCode and submit them.
- **Language:** C++. Python and Java have their own methods. Focus on the synchronization logic, not syntax.
- **Count:** Three problems in the first part.

## ① Print order

- **Problem:** LeetCode 1114, "Print in Order" (easy).
- **Class:** `Foo` has three methods `first()`, `second()`, `third()`. Each only prints "first", "second" or "third".
- **Threads:** The same instance of `Foo` goes to three threads. Thread A calls `first()`, thread B calls `second()`, thread C calls `third()`.
- **Goal:** `second()` runs only after `first()`, and `third()` only after `second()`, in whatever order the threads are scheduled.
- **Difference from normal DSA problems:** There, one thread calls the functions one after another. Here, three threads run in parallel.

```
                       ┌──→ T1 ──→ foo1.first()
foo ──→ obj ──→ [foo1] ┼──→ T2 ──→ foo1.second()
                       └──→ T3 ──→ foo1.third()
```

- **Why it breaks without sync:** With 3 CPUs, all three threads run independently from t = 0. Nobody knows which prints first.
  - **Observed:** The bare code once printed "first second third" by chance. The next run printed "first third second".

### locks & conditional variable

- **Condition variable (recap):** A thread waits on some condition. Another thread makes the condition true and notifies. Then the waiting thread moves ahead.

1. T1 runs `first()`.
2. When "first" is printed, T2 executes.
   - T2 waits on a condition. T1 makes it true after printing "first" and notifies T2. The same holds between T2 and T3.

- **Variables:** A mutex `m`, a condition variable `cv`, and an `int turn`.
- **`turn`:** It decides whose turn it is, meaning which thread may run now. Initially `turn = 0`, because "first" should print first.

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

How it works, with all three threads running concurrently:

1. `first()` has no condition. T1 prints "first", sets `turn = 1`, and calls `cv.notify_all()`.
2. T2 locks `m` and checks `while (turn != 1)`. At the start `turn` is 0, so this is true. T2 goes to `cv.wait(lock)`. Wait releases the lock while waiting.
3. T3 does the same. `turn != 2` is true at the start, so T3 also waits.
4. On `notify_all()`, both wake up, re-lock and re-check their `while` condition.
   - **T2:** `turn` is now 1, so `turn != 1` is false. T2 leaves the loop, prints "second", sets `turn = 2`, and notifies all.
   - **T3:** `turn` is 1, so `turn != 2` is still true. T3 goes back to waiting.
5. After T2's notify, T3 re-checks. `turn != 2` is false, so it prints "third".

- **Wait condition:** The `while` keeps the thread waiting while it is NOT its turn.
- **Result:** Whatever the scheduling, the output is first, second, third. Submitted: accepted.
- **Safer `first()`:** Also take the lock before changing `turn`. Its first line would be `std::unique_lock<std::mutex> lock(m);`. Without it, `turn = 1` plus the notify can land between T2's check of `turn` and its `cv.wait()`. Then T2 sleeps through the only notification.

## ② → Fizz buzz problem

- **Problem:** LeetCode 1195, "Fizz Buzz Multithreaded".
- **Single-threaded FizzBuzz:** Loop `i` from 1 to n.
  - Divisible by 3 and 5: print "fizzbuzz".
  - Divisible by 3, not by 5: print "fizz".
  - Divisible by 5, not by 3: print "buzz".
  - Otherwise: print `i`.
  - Example: for n = 15, 3 gives fizz, 5 gives buzz, 15 gives fizzbuzz. One loop with if/else does it.
- **Multithreaded version:** Class `FizzBuzz` has four functions. Each is called by a different thread, and all run concurrently.

| Thread | Function | Prints only |
|--------|----------|-------------|
| A | `fizz()` | "fizz" |
| B | `buzz()` | "buzz" |
| C | `fizzbuzz()` | "fizzbuzz" |
| D | `number()` | the integer |

- **Challenge:** The counter `i` (1 to n) is shared across all four functions, so access must be synchronized. Each value must be printed by the right thread.
- **Approach:** As before: one mutex, one condition variable, and a shared `i` starting at 1. Every function runs its own `while (i <= n)` loop. The threads take turns incrementing `i`.

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

Reading the wait condition, for example in `fizz()`:

- **Turn test:** `((i%3) == 0) && ((i%5) != 0)` is 1 exactly when it is fizz's turn (divisible by 3, not by 5).
- **Waiting:** `(...) == 0` means "not my turn", so the thread waits. When it is fizz's turn the expression is `1 == 0`, which is false, and the thread leaves the wait loop.
- **`i <= n` in the wait:** Once `i` passes n, waiting threads stop waiting and exit.
- **`if (i <= n)`:** It guards against printing after the last number.

Dry run:

1. `i = 1`. For A, `1%3 == 0` is false, so the expression is 0 and `0 == 0` is true. A waits. B and C also wait.
2. For D, 1 is divisible by neither, so the expression is 1 and `1 == 0` is false. D does not wait. It prints 1 and `i++` gives 2.
3. `i++` happens inside the critical section. No other thread touches `i`, because all others are waiting.
4. D calls `c.notify_all()`. A, B and C wake and re-check with `i = 2`. It is not their turn, so they wait again. D prints 2, sets `i = 3`, and notifies all.
5. At `i = 3`, D waits. A's condition is `1 == 0`, which is false. A prints "fizz", `++i` gives 4, and A notifies all.
6. At `i = 4`, D works again and the rest wait. And so on.

- **Result:** All four threads are scheduled, but only the right thread works for each `i`. Correct for n = 15. Submitted: accepted.

## ③ Dining philosopher's problem

- **Source:** Video no. 20. Revise Lecture 20 first for the problem and why deadlock happens.
- **Problem:** LeetCode 1226, "The Dining Philosophers".
- **Setup:** Five philosophers (ids 0 to 4) alternately think and eat. There are five forks. A philosopher needs both the left and right fork to eat.
- **Deadlock (recap):** If every philosopher picks the left fork (or every one the right fork), nobody can get a second fork. Nobody eats.
- **LeetCode framing:** `wantsToEat(philosopher, pickLeftFork, pickRightFork, eat, putLeftFork, putRightFork)`.
  - **Pick:** `pickLeftFork` and `pickRightFork` pick up that fork.
  - **Eat:** Call `eat` only once the philosopher holds both forks.
  - **Put:** After eating, call `putLeftFork` and `putRightFork` to put both forks down. The philosopher goes back to thinking and other philosophers can use those forks.
  - **Threads:** Five threads, one per philosopher, all call `wantsToEat` on the same object.
- **Approach:** Use the Lecture 20 tweak of picking up both forks inside a critical section. A philosopher eats only if he can pick both forks. If he cannot get the right fork, he does not hold the left one either.
- **Custom semaphore:** C++ before C++20 had no semaphore. So a custom `Semaphore` class is written with a mutex and a condition variable, with the same logic as the semaphore lecture.
  - **`wait()`:** `count--`. If `count < 0`, wait.
  - **`signal()`:** `count++`. If `count <= 0`, `notify_one()`.
- **Forks:** Each fork is a binary semaphore (`setCount(1)`).

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

How it works:

- **Critical section:** Picking is guarded by `m`. Only one thread at a time can be picking forks. It comes out holding both the left and the right fork.
- **After picking:** The thread picks both, eats, puts the left fork down and signals it, then puts the right fork down and signals it.
- **Example:** P0 is inside and gets both forks. P1 then enters the critical section. P0 holds a fork P1 needs, so P1 waits there until P0 puts it down. The others wait for the mutex.
- **No deadlock:** Whoever gets in gets both forks. So the deadlock condition (each holding one fork, waiting for the other) cannot occur.
- **Custom semaphore:** Its `while (count < 0)` is safe here. Every `wait()` happens while holding `m`, so at most one thread ever waits on a given fork.

Ran and submitted: accepted.

- **Homework:** On this LeetCode problem, try the other tweaks from Lecture 20 and check whether they also work.
- **Common tool:** All three problems were solved with condition variables. Here the semaphore itself is custom, built from a condition variable.

> **Interview:** "How will you build your own semaphore?" can be asked. Build it with a mutex and a condition variable, as above.

> **Interview:** Coding rounds rarely ask concurrency coding directly. It comes up in discussion, for example "how will you solve dining philosophers?".

## Part 2: More LeetCode concurrency problems (last lecture of the course)

This bonus lecture at the very end of the course has three more LeetCode concurrency problems.

- **Advice:** Try each problem yourself before seeing the solution. It trains you to think about how threads interact.

### ④ Print FooBar Alternately

- **Problem:** LeetCode 1115.
- **Class:** `FooBar` has `foo()`, which loops n times and prints "foo", and `bar()`, which loops n times and prints "bar".
- **Threads:** The same instance goes to two threads. T1 calls `foo()` and T2 calls `bar()`.
- **Goal:** The output must be "foobar" repeated n times.
- **Order:** With two threads the order must be T1, T2, T1, T2, and so on. T2 prints "bar" only after T1 printed "foo". T1 prints the next "foo" only after T2 printed "bar".
- **Without sync:** n = 1 printed correctly by chance, because the foo thread was scheduled first. For n = 10 it printed foo ten times, then bar ten times, because T1 finished its whole loop first.
- **Approach:** A mutex, a condition variable, and a `bool turn` (0 means foo's turn, 1 means bar's turn). It is initially 0.

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

How it works:

1. Initially `turn = 0`. T2 (bar) locks, sees `turn == 0`, and waits. `cv.wait` releases the lock and keeps waiting until another thread notifies.
2. T1 locks. `turn == 1` is false, so it prints "foo", sets `turn = 1`, and calls `notify_all()`. The notify is essential. Without it T2 would wait forever.
3. T2 wakes, re-locks and re-checks. `turn` is 1, so it prints "bar", sets `turn = 0`, and notifies. T1 was waiting, so it wakes and prints "foo" again.
4. So the threads run T1, T2, T1, T2, and so on, instead of randomly. Submitted: accepted.

- **Extension:** The same pattern extends to more than two threads that must run in sequence (T1, T2, T3, T4, and so on).

### ⑤ Print Zero Even Odd

- **Problem:** LeetCode 1116.
- **`printNumber(x)`:** It prints integer x. It is a `function<void(int)>`, a C++ `std::function` that behaves like a function pointer.
- **Class:** `ZeroEvenOdd` has `zero()`, `even()` and `odd()`. The same instance goes to three threads.
  - **A:** calls `zero()`, which prints only 0.
  - **B:** calls `even()`, which prints only even numbers.
  - **C:** calls `odd()`, which prints only odd numbers.
- **Output:** `0 1 0 2 0 3 ...` up to n (1 ≤ n ≤ 1000).
  - n = 2 gives `0102`. n = 5 gives `0102030405`.
- **Single thread:** Loop 1 to n, and print 0 then the number. Here 0 must come from the zero thread, odd numbers from the odd thread, and even numbers from the even thread.
- **Purpose:** No practical use. It teaches synchronizing three threads.
- **Approach:** A mutex and a condition variable (a thread waits on a condition until another thread tells it to continue). Also an `int turn` (0 means zero's turn, 1 means odd's turn, 2 means even's turn) and an `int i` going from 1 to n.
- **Who goes next:** The zero thread decides. After printing 0 it sets `turn = 1` if `i` is odd and `turn = 2` if `i` is even.

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

Dry run for n = 2:

1. All three start with `turn = 0` and `i = 1`. Odd sees `turn != 1` and waits. Even sees `turn != 2` and waits. Zero gets the chance and prints 0.
2. Zero does not change `i`. `i = 1` is odd, so `turn = 1`. `notify_all()` (essential) reaches both the even and odd threads.
3. Even re-checks. `turn != 2` is true, so it waits again. Odd checks `turn != 1`, which is false. Odd prints 1, `i++` gives 2, sets `turn = 0`, and notifies all.
4. Zero wakes and prints 0. `i = 2` is even, so `turn = 2` and it notifies. The even thread prints 2, `i++` gives 3, sets `turn = 0`, and notifies.
5. Exit: `i = 3 > n`. Zero wakes. `turn != 0` is false, so it leaves the wait loop. `if (i > n)` is true, so it does `break` and the zero thread exits. Even and odd also get the notification. `i <= n` is now false, so they leave the wait loop, hit `break`, and exit.

- **Result:** All three threads exit. Tested with n = 2 and n = 67. Submitted: accepted.
- **Key variable:** `turn` carries most of the responsibility. It decides which thread runs.
- **Tip:** Trace small cases by hand. Following concurrent value changes takes practice.

### ⑥ Building H2O

- **Problem:** LeetCode 1117.
- **Threads:** There are two kinds, oxygen and hydrogen. Each thread is one atom. The goal is to group them into water molecules.
- **Barrier:** Threads pass a barrier in complete sets. Each set of three is one oxygen and two hydrogen, in any order (HHO, HOH, OHH). You do not have to match specific threads to each other.
- **Functions:** `releaseHydrogen()` prints "H". `releaseOxygen()` prints "O".
- **Input:** Any order, for example `OOHHHH` (4 H threads, 2 O threads). It is not sequential.
- **Approach:** Give the chance to two hydrogen threads, then to one oxygen thread, then two hydrogen, then one oxygen, and so on. Use a mutex, a condition variable, and an `int turn` (the number of H released in the current molecule). It is initially 0.

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

How it works:

1. Start: `turn = 0`. The first H thread locks and enters the critical section. `turn == 2` is false, so it releases hydrogen, `turn++` gives 1, and it notifies.
2. O threads that arrive meanwhile lock and see `turn < 2`, so they wait. `cv.wait` unlocks the lock while waiting. That is what lets the H threads get in.
3. The second H thread sees `turn = 1`. It releases hydrogen, `turn` becomes 2, and it notifies all.
4. A third H thread arriving now sees `turn == 2` and waits.
5. An O thread wakes. `turn < 2` is false, so it releases oxygen, sets `turn = 0` (one water molecule is done), and notifies all.
6. The waiting H thread can now go. The pattern is H, H, O, H, H, O, and so on. Tested with small and larger inputs. Submitted: accepted.

- **Analogy:** Making water in real life. Release two hydrogen atoms, then one oxygen atom, and you get one molecule.

### Conclusion

All six concurrency problems use the same few things:

- **Mutex:** the lock.
- **Condition variables:** threads wait and notify on them.
- **`turn`-style variable:** It decides which thread gets the chance to run.
