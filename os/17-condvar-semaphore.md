# Lecture 17: Conditional Variable and Semaphores for Threads synchronization

- Recap of the earlier solutions to the critical section problem:
  - Single flag solution: not good, because it does not give progress.
  - Peterson's solution: works only for two threads.
  - Locks (mutex): a good solution; the count example (two threads incrementing a shared count) gives the correct result.
- Biggest problem with locks: busy waiting.
  - T1 enters the C.S. and acquires the lock. T2 tries to enter and waits on that lock.
  - Internally that wait is a `while` loop spinning on some flag.
  - While spinning, T2 keeps using CPU cycles that are very important, and they are wasted.
- Improved methods below: condition variables and semaphores.

## 1. Conditional variable

a. The condition variable is a synchronization primitive that lets the thread wait until a certain condition occurs.
   - Every programming language provides it (e.g. `threading.Condition` in Python, `std::condition_variable` in C++).
   - Two operations on it: wait and signal (notify).
   - The thread waits for a signal without using CPU cycles. The signal comes as a (software) interrupt from the kernel; until then the CPU can execute some other thread or job.

b. Works with a lock
   - Internally a condition variable uses a mutex (lock).
   - In C++ you pass the mutex yourself as an argument; in Python the lock is created internally, so you do not pass one explicitly.

c. Thread can enter a wait state only when it has acquired a lock. When a thread enters the wait state, it will release the lock and wait until another thread notifies that the event has occurred. Once the waiting thread enters the running state, it again acquires the lock immediately and starts executing.
   - The condition becomes true only when some other thread notifies on the condition variable.
   - Flow for the waiting thread: acquire lock → check condition → condition false → wait: the thread is fully blocked and the CPU is freed (no busy waiting).
   - Notify: sets the condition true and sends a software interrupt (done by the kernel) to the blocked thread: "wake up, check the condition again, and do what is needed".
   - After waking: the thread acquires the internal lock again, checks the condition again, finds it true, and continues with the next line.

   Example (two threads, T2 must run before T1):

   ```
   T1: enters → wait() on the condition       (blocked, CPU free)
   T2: does its work in the C.S. → signal()   (notifies the condition)
   T1: wakes up → continues in the C.S.
   ```

   Python code from the lecture:

   ```python
   import threading, time

   cv = threading.Condition()   # uses a lock internally
   done = 1

   def task(name):
       global done
       with cv:
           if done == 1:
               done = 2
               print(name, "waiting on condition variable cv")
               cv.wait()          # releases the lock, blocks, CPU freed
               print(name, "condition met")
           else:
               time.sleep(5)
               print(name, "signaling")
               cv.notify_all()    # wakes the waiting thread
               print(name, "notification done")

   t1 = threading.Thread(target=task, args=("t1",))
   t2 = threading.Thread(target=task, args=("t2",))
   t1.start()
   t2.start()
   t1.join()
   t2.join()
   ```

   - At the start `done = 1`. Ideally T1 would run completely first (it is started first).
   - T1 sees `done == 1`, sets `done = 2`, and waits on `cv`: it acquires the lock, finds the condition false (T2 has not notified yet), and is blocked.
   - T2 sees `done == 2`, so the else part runs: sleeps 5 seconds, prints "signaling", calls `notify_all()`.
   - T1 wakes, re-acquires the lock, rechecks the condition (now true) and prints "condition met".
   - Output: T1 prints it is waiting; after 5 seconds T2 signals; then T1 continues. So T2 executed first even though T1 was started first: the threads are synchronised without busy waiting.
   - Use: whenever one thread must wait in the code until another thread finishes its work and notifies it, before it enters.

d. Why to use conditional variable?
   i. To avoid busy waiting.
   - No busy waiting, so no CPU cycles are wasted. Used extensively in industry.

e. **Contention** is not here.

## 2. Semaphores

a. Synchronization method.

b. An integer that is equal to number of resources
   - Used when one resource has multiple instances (copies).
   - Example: a big printer server (one resource) with 3 printers inside it = 3 instances of the printer.
   - With 3 instances, 3 threads can be sent in parallel. Out of 10 threads, only 3 are let in at a time.
   - A mutex fits one instance: lock/unlock passes many threads through one C.S. sequentially, one at a time.

c. Multiple threads can go and execute C.S concurrently.

   Working (resource with 3 instances, threads T1..T10, semaphore S = 3):
   1. T1 comes; S = 3, so it is allowed; S decremented to 2.
   2. T2 comes; allowed; S = 1.
   3. T3 comes; allowed; S = 0.
   4. S = 0, so other threads wait until T1, T2 or T3 frees its instance.
   5. T1 exits; S incremented to 1 (S++).
   6. Waiting T4 sees S = 1 and gets the resource.

d. Allows multiple program threads to access the finite instance of resources whereas mutex allows multiple threads to access a single shared resource one at a time.

   Python code from the lecture:

   ```python
   import threading, time

   sem = threading.Semaphore(3)   # 3 threads in the C.S. at a time

   def task(name):
       sem.acquire()              # wait()
       for i in range(5):
           print(name, "working")
           time.sleep(1)
       sem.release()              # signal()

   threads = [threading.Thread(target=task, args=("t" + str(i),)) for i in range(1, 6)]
   for t in threads:
       t.start()
   for t in threads:
       t.join()
   ```

   - 5 threads, semaphore value 3: T1, T2, T3 work together; only when they finish do T4 and T5 get a chance.
   - With a lock: T1's loop runs 5 times, then T2's 5 times, then T3's, and so on.
   - Semaphore value = number of threads that get parallel access to the C.S. at a point of time.
   - Semaphore value 5: all five threads execute in parallel.

e. Binary semaphore: value can be 0 or 1.
   i. Aka, mutex locks
   - Semaphore value 1: only one thread goes at a time; the output is exactly like a lock (each thread's loop runs 5 times, then the next thread's).
   - Some mutex implementations (e.g. in C++) internally work as a binary semaphore; the abstraction hides it.

f. Counting semaphore
   i. Can range over an unrestricted domain.
   ii. Can be used to control access to a given resource consisting of a finite number of instances.
   - Semaphore value greater than 1. Called counting because the value keeps counting: −1 on wait, +1 on signal.

g. To overcome the need for busy waiting, we can modify the definition of the wait () and signal () semaphore operations. When a process executes the wait () operation and finds that the semaphore value is not positive, it must wait. However, rather than engaging in busy waiting, the process car block itself. The block- operation places a process into a waiting queue associated with the semaphore, and the state of the process is switched to the Waiting state. Then control is transferred to the CPU scheduler, which selects another process to execute.

   Internal working (semaphore S = 2, i.e. 2 instances):
   1. T1 calls `wait()`: S-- → 1. 1 is not less than 0, so T1 gets an instance.
   2. T2 calls `wait()`: S-- → 0. T2 gets the second instance.
   3. T3 calls `wait()`: S-- → −1. S is negative, so T3 is blocked (same idea as the condition variable: thread blocked, CPU free).
   4. T4, T5, ... also get blocked: only 2 instances exist.
   5. T1 finishes the C.S. and calls `signal()` to say it freed its instance: S++, and a wakeup is sent to blocked T3.
   6. T3 gets the CPU again and continues from where it was blocked, straight into the C.S. (T3 takes the instance T1 freed).
   7. When T3 exits it also calls `signal()`, S++ again. So only 2 instances are held at any time.

   Code for each thread:

   ```
   wait(S);
   // critical section
   signal(S);
   ```

h. A process that is blocked, waiting on a semaphore S, should be restarted when some other process executes a signal () operation. The process is restarted by a wakeup () operation, which changes the process from the waiting state to the ready state. The process is then placed in the ready queue.

- Why semaphores: to let more than one thread into the critical section, but not unlimited threads; a limited number, because a resource has only a limited number of instances.
- Practise: write these synchronisation methods yourself in C++, C, or Python (simplest).
