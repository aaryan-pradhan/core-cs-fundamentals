# Lecture 17: Conditional Variable and Semaphores for Threads synchronization

Earlier solutions to the critical section problem:

| Solution | Verdict |
|----------|---------|
| Single flag | Not good. It does not give progress. |
| Peterson's solution | Works only for two threads. |
| Locks (mutex) | Good. The count example (two threads incrementing a shared count) gives the correct result. |

- **Biggest problem with locks:** busy waiting.
  - T1 enters the C.S. and acquires the lock. T2 tries to enter and waits on that lock.
  - Internally that wait is a `while` loop spinning on some flag.
  - While spinning, T2 wastes very important CPU cycles.
- **Improved methods:** condition variables and semaphores.

## 1. Conditional variable

a. A condition variable is a synchronization primitive. It lets a thread wait until a certain condition occurs.
   - **Availability:** Every programming language provides it (e.g. `threading.Condition` in Python, `std::condition_variable` in C++).
   - **Operations:** wait and signal (notify).
   - **Waiting:** The thread waits for a signal without using CPU cycles. The signal comes as a (software) interrupt from the kernel. Until then the CPU can run some other thread or job.

b. It works with a lock.
   - **Internal mutex:** It uses a mutex (lock) internally.
   - **C++:** You pass the mutex yourself as an argument.
   - **Python:** The lock is created internally, so you do not pass one.

c. A thread can enter the wait state only when it has acquired a lock.
   - **On wait:** The thread releases the lock and waits until another thread notifies that the event has occurred.
   - **On wake:** Once the waiting thread is running again, it acquires the lock immediately and starts executing.
   - **Condition:** It becomes true only when some other thread notifies on the condition variable.
   - **Waiting thread flow:** Acquire lock, check condition, find it false, then wait. The thread is fully blocked and the CPU is freed. There is no busy waiting.
   - **Notify:** It sets the condition true. The kernel sends a software interrupt to the blocked thread: "wake up, check the condition again, and do what is needed".
   - **After waking:** The thread re-acquires the internal lock, rechecks the condition, finds it true, and continues.

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

   - **Start:** `done = 1`. T1 is started first.
   - **T1:** It sees `done == 1`, sets `done = 2`, finds the condition false (T2 has not notified yet), and blocks on `cv`.
   - **T2:** It sees `done == 2`, so the else part runs. It sleeps 5 seconds, prints "signaling", and calls `notify_all()`.
   - **T1 again:** It wakes, re-acquires the lock, rechecks the condition (now true) and prints "condition met".
   - **Output:** T1 prints that it is waiting. After 5 seconds T2 signals. Then T1 continues. T2 ran first even though T1 started first, without busy waiting.
   - **Use:** One thread must wait in the code until another thread finishes its work and notifies it.

d. Why use a conditional variable?
   i. To avoid busy waiting.
   - No CPU cycles are wasted. It is used extensively in industry.

e. **Contention** is not here.

## 2. Semaphores

a. A semaphore is a synchronization method.

b. It is an integer equal to the number of resources.
   - **Use:** One resource has multiple instances (copies).
   - **Example:** A big printer server (one resource) with 3 printers inside it is 3 instances of the printer.
   - **Parallelism:** With 3 instances, 3 threads can be sent in parallel. Out of 10 threads, only 3 are let in at a time.
   - **Mutex:** It fits one instance. Lock and unlock pass many threads through one C.S. sequentially, one at a time.

c. Multiple threads can execute the C.S. concurrently.

   Working (resource with 3 instances, threads T1..T10, semaphore S = 3):
   1. T1 comes. S = 3, so it is allowed. S becomes 2.
   2. T2 comes and is allowed. S becomes 1.
   3. T3 comes and is allowed. S becomes 0.
   4. S = 0, so other threads wait until T1, T2 or T3 frees its instance.
   5. T1 exits. S is incremented to 1 (S++).
   6. Waiting T4 sees S = 1 and gets the resource.

d. A semaphore lets multiple threads access a finite number of instances of a resource. A mutex lets threads access a single shared resource one at a time.

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

   - **5 threads, value 3:** T1, T2, T3 work together. Only when they finish do T4 and T5 get a chance.
   - **With a lock:** T1's loop runs 5 times, then T2's 5 times, then T3's, and so on.
   - **Semaphore value:** It is the number of threads that get parallel access to the C.S. at a point of time.
   - **Value 5:** All five threads execute in parallel.

e. Binary semaphore: the value can be 0 or 1.
   i. Also known as a mutex lock.
   - **Value 1:** Only one thread goes at a time. The output is exactly like a lock (each thread's loop runs 5 times, then the next thread's).
   - Some mutex implementations (e.g. in C++) work internally as a binary semaphore.

f. Counting semaphore
   i. It can range over an unrestricted domain.
   ii. It can control access to a resource with a finite number of instances.
   - **Value:** Greater than 1. It is called counting because the value keeps counting: minus 1 on wait, plus 1 on signal.

g. To avoid busy waiting, the wait() and signal() operations are modified.
   - **Wait:** A process that executes wait() and finds the semaphore value not positive must wait. Instead of busy waiting, the process blocks itself.
   - **Block operation:** It places the process into a waiting queue associated with the semaphore. The process state switches to Waiting.
   - **Then:** Control is transferred to the CPU scheduler, which selects another process to execute.

   Internal working (semaphore S = 2, i.e. 2 instances):
   1. T1 calls `wait()`. S-- gives 1. 1 is not less than 0, so T1 gets an instance.
   2. T2 calls `wait()`. S-- gives 0. T2 gets the second instance.
   3. T3 calls `wait()`. S-- gives −1. S is negative, so T3 is blocked. This is the same idea as the condition variable: thread blocked, CPU free.
   4. T4, T5, ... also get blocked, because only 2 instances exist.
   5. T1 finishes the C.S. and calls `signal()` to say it freed its instance. S++ runs, and a wakeup is sent to blocked T3.
   6. T3 gets the CPU again and continues from where it was blocked, straight into the C.S. T3 takes the instance T1 freed.
   7. When T3 exits it also calls `signal()`, and S++ runs again. So only 2 instances are held at any time.

   Code for each thread:

   ```
   wait(S);
   // critical section
   signal(S);
   ```

h. A process blocked on a semaphore S restarts when some other process executes signal().
   - **Wakeup:** The wakeup() operation restarts the process. It changes the process from the waiting state to the ready state.
   - **Then:** The process is placed in the ready queue.

- **Why semaphores:** They let a limited number of threads (not unlimited) into the C.S., because a resource has limited instances.
- **Practise:** Write these synchronisation methods yourself in C++, C, or Python (simplest).
