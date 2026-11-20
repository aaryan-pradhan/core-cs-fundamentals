# Lecture 16: Critical Section Problem and How to address it

- **Context:** A process is divided into threads (independent paths of execution). But since they belong to one process, two or three threads may work on the same data, write to the same place, or update the same database. This lecture covers the problems that arise and how to address them.

### What `count++` really does

- In C/C++ you write `count++`, meaning `count = count + 1`.
- At the machine-code (CPU) level it is not one step. A temporary variable is involved:

```
temp  = count + 1;   // step 1: current count + 1 stored in temp
count = temp;        // step 2: actual count replaced by temp
```

- **Root of the problem:** A context switch can happen between step 1 and step 2.

### Example: Aadhaar count

- **Setup:** The Aadhaar head office keeps a database with the total count of Aadhaar cards. Many centres (A, B, C, D) update it. Each time a citizen is added, a centre asks for `count++`.
- **Shared resource:** The database is the shared resource. Each centre is like a thread.
- **Current count:** 11.
  1. Request from A: `temp = count + 1` gives temp = 12 (count is still 11).
  2. Context switch to B's request: `temp = count + 1`. Count is still 11, so B's temp = 12.
  3. Back to A: `count = temp` gives count = 12.
  4. B: `count = temp` gives count = 12.
- **Result:** Two requests, but the final count is 12, not 13. One update is lost.
- **Four requests:** If A, B, C, D each send one request at the same time, the value should become 15. It may come out as 12 or 13, and it changes from run to run.
- **Race condition:** This data inconsistency is the race condition. The final result cannot be relied on.

1. Process synchronization techniques play a key role in maintaining the consistency of shared data.

2. **Critical Section (C.S)**
   1. The critical section is the segment of code where processes or threads access shared resources, such as common variables and files, and perform write operations on them. Any process can be interrupted mid-execution.
      - **Aadhaar example:** The database (the `count++` code) is the critical section.
      - **Why "critical":** Updates to the shared resource must be done carefully, or data inconsistency arises.

3. **Major Thread scheduling issue**
   1. **Race Condition**
      1. A race condition occurs when two or more threads can access shared data and try to change it at the same time. The thread scheduling algorithm can swap between threads at any time, so you do not know the order of access. The result depends on the thread scheduling algorithm. Both threads are "racing" to access and change the data.
         - **Example:** B says "let me update first". A says "let me update first". Whichever is scheduled first changes the data its way. The output is never reliable.
         - **Also called:** the critical section problem.
      2. Demo (Python): two threads each run a task that does `count += 1` ten lakh (1,000,000) times.

         ```python
         import threading

         count = 0

         def task():
             global count
             for _ in range(1000000):
                 count += 1

         t1 = threading.Thread(target=task)
         t2 = threading.Thread(target=task)
         t1.start(); t2.start()
         t1.join(); t2.join()
         print(count)
         ```

         - **Expected:** 20 lakh (2,000,000).
         - **Actual:** Less than 20 lakh, and different on every run.
         - **Cause:** `count + 1` is stored in a temp first. If a context switch happens before `count` is updated, the other thread reads the old count.

4. **Solution to Race Condition**
   1. **Atomic operations:** Make the critical code section an atomic operation, executed in one CPU cycle.
      - `count++` (temp, +1, store back) must finish in one cycle, not be split across two.
      - **C++:** It supports atomic variables. An atomic variable is thread safe. A manipulation on it completes before any context switch.
      - **Not universal:** Not all languages support this.
   2. **Mutual Exclusion using locks.**
      - T1 and T2 must not execute the critical section simultaneously. T1 executes and exits, then T2 enters (or the reverse). The critical section becomes sequential instead of parallel.
      - **Mutex:** Languages provide locks (mutex). In C++ you can create a mutex and lock it.
      - Until T1 unlocks, T2 cannot enter the critical section.
      - **Analogy:** A lock on a room. One person goes in at a time.
      - **Demo with lock:** The same code, with a lock acquired before `count += 1` and released after it.

        ```python
        lock = threading.Lock()

        def task():
            global count
            for _ in range(1000000):
                lock.acquire()
                count += 1        # critical section
                lock.release()
        ```

        - Every run now gives the same, determinate value (2,000,000). Both threads are never inside the critical section at once.
   3. **Semaphores**
      - Covered in the next lecture.

### Conditions for a solution of the critical section problem

Any solution should have three conditions:

1. **Mutual exclusion:** Only one thread is inside the critical section at a time.
2. **Progress:** If no thread is inside the critical section (say T1 and T2 are both outside), a thread not in the C.S must not stop another thread from entering it.
   - If the C.S is free, any thread that wants to enter can enter. Every thread gets an equal opportunity.
   - There must be no fixed order like "T2 cannot go until T1 goes". Whichever wants to go first goes.
3. **Bounded waiting:** No thread waits infinitely.
   - **Example:** Of 4 threads, 3 keep getting chances to enter the C.S but T1 never does. This is not allowed.
   - There must be a time bound (a hard stop) after which a waiting thread surely enters the C.S.
   - This condition is not as mandatory. Mutual exclusion and progress must be present in any solution you propose.

5. **Can we use a simple flag variable to solve the problem of race condition?**
   1. **No.**
      - **Single flag solution:** A `turn` variable shared by two threads, with value 0 or 1.

        ```
        T1:                          T2:
        while (turn != 0);           while (turn != 1);
        // critical section          // critical section
        turn = 1;                    turn = 0;
        ```

      - **Case `turn = 0` initially:** For T1, `0 != 0` is false, so T1 enters the C.S. For T2, `0 != 1` is true, so T2 waits in the while loop. After the C.S, T1 sets `turn = 1`. Now `1 != 1` is false for T2, so T2 enters.
      - **Case `turn = 1` initially:** T2 goes first, then T1.
      - **Mutual exclusion:** It is achieved.
      - **Progress:** It is not achieved. The initial value of `turn` fixes the order (turn = 0 means T1 first, then T2). A thread cannot freely enter even though the C.S is free.
      - So the single flag solution is not correct. It was improved into Peterson's solution.

6. **Peterson's solution** avoids race condition. It holds good for only 2 processes or threads.
   - It uses two variables:
     - **`flag[2]`** (array of size 2): `flag[i] = true` indicates thread i is ready to enter the critical section.
     - **`turn`:** It indicates whose turn it is. The value is 0 or 1, like the single flag.

     ```
     T1 (i = 0):                        T2 (i = 1):
     flag[0] = true;                    flag[1] = true;
     turn = 1;                          turn = 0;
     while (flag[1] && turn == 1);      while (flag[0] && turn == 0);
     // critical section                // critical section
     flag[0] = false;                   flag[1] = false;
     ```

   - How it works:
     - **Case 1:** T1 sets `flag[0] = true` and `turn = 1`. Then T2 sets `flag[1] = true`. At T1's while loop, `flag[1]` is true and `turn == 1`, so T1 waits. T2 sets `turn = 0`. Now T1's condition is false and T1 enters. T2's condition (`flag[0]` true, `turn == 0`) is true, so T2 waits.
     - **Case 2:** T2 sets `flag[1] = true` and `turn = 0`, then a context switch happens. Since `flag[0]` is true and `turn == 0`, T2 waits and T1 enters the C.S.
     - **Rule:** Whichever thread writes `turn` last waits. The other enters.
   - **Mutual exclusion:** It is maintained.
   - **Progress:** It is also achieved. No fixed sequence depends on an initial variable value (unlike `turn` in the single flag). Either T1 or T2 can go first, depending on CPU scheduling and context switches. Both get an equal chance.
   - **Problem:** It is safe for only two threads, so it is not used extensively. It is a classic, basic solution.

7. **Mutex/Locks**
   1. Locks implement mutual exclusion and avoid race condition. Only one thread or process accesses the critical section.
      - A thread locks around the C.S, executes it, then unlocks and leaves.
   2. **Disadvantages:**
      1. **Contention:** One thread has acquired the lock and others busy wait. If the thread that acquired the lock dies, all others wait infinitely.
         - T2 and T3 busy wait. They keep eating CPU cycles waiting for the lock variable.
         - If T1 hits an exception inside the C.S and dies, its lock is never unlocked. T2 and T3 wait infinitely.
         - So code must be written carefully. Even if an exception comes, do not let the thread exit until it has unlocked.
      2. **Deadlocks**
         - **Hint (covered later):** Processes or threads P1 and P2, resources R1 and R2. R1 is allocated to P1, and R2 to P2. P1 cannot proceed until it gets R2. P2 cannot proceed until it gets R1.
         - Each holds one resource and waits for the other's. The locks are never freed and the system hangs.
      3. **Debugging**
         - Multithreaded code is hard to debug. While stepping with a debugger (next, next) or adding small `printf`s, threads run simultaneously, so you land in one thread, then another. There is no sequential flow.
      4. **Starvation of high priority threads.**
         - A low priority thread acquires the lock on the C.S. A high priority thread arrives but cannot enter until the low priority thread leaves. So the high priority job starves.
