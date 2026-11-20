# Lecture 16: Critical Section Problem and How to address it

- Context: a process is divided into threads (independent paths of execution). The paths are independent, but since they belong to one process, some areas of the code may have two or three threads working on the same data, writing to the same place, or updating the same database. This lecture covers the problems that arise there and how to address them.

### What `count++` really does

- In C/C++ you write `count++`, meaning `count = count + 1`.
- At the machine-code (CPU) level it is not one step. A temporary variable is involved:

```
temp  = count + 1;   // step 1: current count + 1 stored in temp
count = temp;        // step 2: actual count replaced by temp
```

- A context switch can happen between step 1 and step 2. This is the root of the problem below.

### Example: Aadhaar count

- Aadhaar head office keeps a database with the total count of Aadhaar cards. Many Aadhaar centres (A, B, C, D) update it; every time a citizen is added, a centre asks for `count++`.
- The database is a shared resource; each centre is like a thread updating it.
- Current count = 11.
  1. Request from A: `temp = count + 1` → temp = 12 (count is still 11).
  2. Context switch to B's request: `temp = count + 1` → count is still 11, so B's temp = 12.
  3. Back to A: `count = temp` → count = 12.
  4. B: `count = temp` → count = 12.
- Two requests, but the final count is 12, not 13. One citizen's update is lost.
- If A, B, C, D each send one request at the same time, the value should become 15, but it may come out as 12 or 13, and it changes from run to run.
- This data inconsistency is the race condition. The code is multithreaded, but its final result cannot be relied on.

1. Process synchronization techniques play a key role in maintaining the consistency of shared data
2. **Critical Section (C.S)**
   1. The critical section refers to the segment of code where processes/threads access shared resources, such as common variables and files, and perform write operations on them. Since processes/threads execute concurrently, any process can be interrupted mid-execution.
      - In the Aadhaar example the database (the `count++` code) is the critical section.
      - Named "critical" because it is a shared resource whose updates must be done so carefully that, if not, data inconsistency arises.
3. **Major Thread scheduling issue**
   1. **Race Condition**
      1. A race condition occurs when two or more threads can access shared data and they try to change it at the same time. Because the thread scheduling algorithm can swap between threads at any time, you don't know the order in which the threads will attempt to access the shared data. Therefore, the result of the change in data is dependent on the thread scheduling algorithm, i.e., both threads are "racing" to access/change the data.
         - In the example, B says "let me update first", A says "let me update first"; whichever gets scheduled first changes the data its way, so the output depends on thread scheduling and is never reliable.
         - This problem is also called the critical section problem.
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

         - Expected: 20 lakh (2,000,000), since two instances run in parallel.
         - Actual: less than 20 lakh, and a different value on every run. The output is inconsistent.
         - Cause: `count + 1` is stored in a temp first; if a context switch happens before `count` is updated, the other thread still reads the old count.
4. **Solution to Race Condition**
   1. Atomic operations: Make Critical code section an atomic operation, i.e., Executed in one CPU cycle.
      - `count++` (temp, +1, store back) must not be split across two CPU cycles; it must finish in one.
      - C++ supports atomic variables. An atomic variable is thread safe: it never gives an inconsistent result, because a manipulation on it completes before any context switch.
      - Not all languages support this.
   2. Mutual Exclusion using locks.
      - T1 and T2 must not execute the critical section simultaneously. T1 executes and exits, then T2 enters (or T2 first, then T1). The critical section is made sequential instead of parallel.
      - Languages provide locks (mutex). In C++ you can create a mutex and lock it.
      - When T1 locks, T2 cannot enter; until T1 unlocks, T2 cannot enter the critical section.
      - Analogy: a lock on a room; one person goes in at a time, and the next cannot go in until that person comes out.
      - Demo with lock: same code, the `count += 1` is made the critical section by acquiring a lock before and releasing it after.

        ```python
        lock = threading.Lock()

        def task():
            global count
            for _ in range(1000000):
                lock.acquire()
                count += 1        # critical section
                lock.release()
        ```

        - Now every run gives the same, determinate value (2,000,000). If T1 is scheduled first, T2 can enter only after T1; both are never inside the critical section at once.
   3. Semaphores
      - Covered in the next lecture.

### Conditions for a solution of the critical section problem

Any solution of the critical section problem should have three conditions:

1. Mutual exclusion: only one thread is inside the critical section at a time.
2. Progress: if no thread is inside the critical section (say T1 and T2 are both outside), a thread that is not in the C.S must not stop another thread from entering it.
   - If the C.S is free, any thread that wants to enter can enter; every thread gets an equal opportunity.
   - There must be no fixed order like "T2 cannot go until T1 goes" or "T1 cannot go until T2 goes". Whichever wants to go first goes.
3. Bounded waiting: no thread waits infinitely.
   - E.g. of 4 threads, 3 keep getting chances to enter the C.S but T1 never does: not allowed.
   - There must be a time bound (a hard stop) after which a waiting thread surely gets entry into the C.S.
   - This condition is not as mandatory; the first two (mutual exclusion and progress) must be present in any solution you propose.

5. Can we use a simple flag variable to solve the problem of race condition?
   1. No.
      - Single flag solution: a `turn` variable shared by two threads, value 0 or 1.

        ```
        T1:                          T2:
        while (turn != 0);           while (turn != 1);
        // critical section          // critical section
        turn = 1;                    turn = 0;
        ```

      - Case `turn = 0` initially: for T1, `0 != 0` is false, so T1 enters the C.S. For T2, `0 != 1` is true, so T2 is stuck waiting in the while loop. After the C.S, T1 sets `turn = 1`; now `1 != 1` is false for T2, so T2 enters.
      - Case `turn = 1` initially: T2 gets the chance first, then T1.
      - Mutual exclusion is achieved.
      - Progress is not: the order is fixed by the initial value of `turn` (turn = 0 means T1 must go first, then T2). When both threads are outside the C.S they are not free to choose; a thread cannot freely enter even though the C.S is free.
      - So the single flag solution is not a correct solution. It was improved into Peterson's solution.
6. **Peterson’s solution** can be used to avoid race condition but holds good for only 2 process/threads.
   - Uses two variables:
     - `flag[2]` (array of size 2): `flag[i] = true` indicates thread i is ready to enter the critical section.
     - `turn`: indicates whose turn it is; value 0 or 1, like the single flag.

     ```
     T1 (i = 0):                        T2 (i = 1):
     flag[0] = true;                    flag[1] = true;
     turn = 1;                          turn = 0;
     while (flag[1] && turn == 1);      while (flag[0] && turn == 0);
     // critical section                // critical section
     flag[0] = false;                   flag[1] = false;
     ```

   - How it works:
     - Case 1: T1 sets `flag[0] = true`, `turn = 1`; then T2 runs and sets `flag[1] = true`. At T1's while loop, `flag[1]` is true and `turn == 1`, so T1 waits. T2 sets `turn = 0`: now T1's condition is false and T1 enters, while T2's condition (`flag[0]` true, `turn == 0`) is true, so T2 waits. Only one passes.
     - Case 2: T2 sets `flag[1] = true`, `turn = 0`, then a context switch happens. Since `flag[0]` is true and `turn == 0`, T2 goes to wait and T1 enters the C.S.
     - Whichever thread writes `turn` last waits; the other enters. Which one that is depends on the interleaving.
   - Mutual exclusion is maintained.
   - Progress is also achieved: when neither thread is in the C.S, there is no fixed sequence based on an initial variable value (unlike `turn` in the single flag). Either T1 or T2 can go first, depending on how the CPU schedules / context switches; both get an equal chance.
   - Problem: safe for only two threads; not built for more than two, so not used extensively. A classic, basic solution.
7. **Mutex/Locks**
   1. Locks can be used to implement mutual exclusion and avoid race condition by allowing only one thread/process to access critical section.
      - A thread sets a lock around the C.S, executes it, then unlocks and leaves. Only one thread can be inside at a time.
   2. **Disadvantages**:
      1. **Contention**: one thread has acquired the lock, other threads will be busy waiting, what if thread that had acquired the lock dies, then all other threads will be in infinite waiting.
         - T1 is inside the C.S; T2 and T3 also want to enter, so they busy wait: they keep eating CPU cycles waiting on the lock variable to become available.
         - If T1 hits an exception inside the C.S and dies, the lock it acquired is never unlocked, so T2 and T3 go into infinite waiting.
         - So code must be written very carefully: even if an exception comes, do not let the thread exit until it has unlocked.
      2. **Deadlocks**
         - Hint (covered in detail in a later lecture): processes/threads P1 and P2, resources R1 and R2. R1 is allocated to P1, R2 to P2. P1 cannot proceed until it gets R2; P2 cannot proceed until it gets R1.
         - Each holds one resource and waits for the other's, so the locks are never freed and the system hangs.
      3. Debugging
         - Multithreaded code is hard to debug: while stepping with a debugger (next, next) or adding small `printf`s, threads run simultaneously, so you unexpectedly land in one thread, then another. There is no sequential flow, and it is hard to follow how variables move.
      4. Starvation of high priority threads.
         - A low priority thread acquires the lock on the C.S. Then a high priority thread arrives. It cannot acquire the lock and enter until the low priority thread leaves, so the high priority job starves.
