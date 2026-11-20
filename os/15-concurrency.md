# Lecture 15: Introduction to Concurrency

- Starts a new module: Concurrency. It covers:
  - What a thread is, why threads are needed, how threads are scheduled, how a thread differs from a process, advantages of threads.
  - Problems that come after breaking a process into threads: synchronization problems, and how to solve them.
  - The strategies used to solve synchronization bring another problem (bug): deadlock.
- This lecture: what concurrency is, what a thread is, how threads are scheduled, benefits of multi-threading, and a hands-on multi-threaded C++ program.
- Revise Lecture 3 (Multitasking vs Multithreading) first; threads were introduced there.

1. **Concurrency** is the execution of the multiple instruction sequences at the same time. It happens in the operating system when there are several process threads running in parallel.
   - Concurrency = ability of the OS to execute multiple instructions at the same time.
   - How it is achieved: divide a process into threads (T1, T2, ...), and use the threads to execute multiple instructions of the same process at the same time (try to run them in parallel).
2. **Thread**:
   - Single sequence stream within a process.
   - An independent path of execution in a process.
   - Light-weight process.
     - Not an actual process, but a light-weight process (LWP); a sub-process inside one process.
   - Used to achieve parallelism by dividing a process’s tasks which are independent path of execution.
     - E.g., a process has two tasks, Task A and Task B, independent of each other (they do not disturb each other; each has its own execution path/flow).
     - Divide the process into two threads: Task A → thread T1, Task B → thread T2.
     - Give T1 to CPU 1 and T2 to CPU 2; both execute independently, in parallel.
     - Threads give an advantage only with a multi-core CPU (more than one core). With a single core, threads are scheduled just like two processes, with context switching between them, so there is no real gain.
   - E.g., Multiple tabs in a browser, text editor (When you are typing in an editor, spell checking, formatting of text and saving the text are done concurrently by multiple threads.)
     - E.g., MS Word is one process with three tasks: text editor, spell checker, text formatting. Break it into three light-weight processes: thread 1, thread 2, thread 3, each working independently.
     - As one single process, these run sequentially: you type, then spell checking happens, then text formatting happens. A long, sequential process; the user waits.
     - With threads the work is parallel: while you type, spell checking runs alongside (red underlines appear) and formatting runs alongside (pressing Enter moves text, bold, etc.).
     - Benefit: responsiveness increases; the user sees no delay, everything is fast. This is the biggest advantage of concurrency.
   - Memory: process vs thread
     - Process: each process gets its own address space, isolated from (independent of) other processes' address spaces.
     - Threads: process P1 broken into threads T1, T2, T3; all three use the same address space, the one allocated to P1. A shared memory space is used among the threads.
     - This is the most important difference between a process and a thread.

     ```
     Process                     Threads of one process
     ┌──────────────┐            ┌───────────────────────┐
     │ P1           │            │ P1:  T1   T2   T3     │
     │ own address  │            │   └────┼────┘         │
     │ space        │            │  one shared address   │
     └──────────────┘            │  space                │
     (isolated from others)      └───────────────────────┘
     ```

   - Memory layout:
     - Process: text, data, heap and stack; stack and heap grow towards each other.
     - Multi-threaded process: same text, data and heap, but multiple stacks are implemented, one per thread (stack 1 for thread 1, stack 2 for thread 2, ...). Number of stacks = number of threads. The heap area stays one, shared by all threads.

     ```
     Process            Multi-threaded process
     ┌─────────┐        ┌─────────┐
     │ Stack   │        │ Stack 1 │  (T1)
     │   ↓     │        │ Stack 2 │  (T2)
     │         │        │   ↓     │
     │   ↑     │        │   ↑     │
     │ Heap    │        │ Heap    │  (shared by all threads)
     │ Data    │        │ Data    │
     │ Text    │        │ Text    │
     └─────────┘        └─────────┘
     ```

3. **Thread Scheduling:** Threads are scheduled for execution based on their priority. Even though threads are executing within the runtime, all threads are assigned processor time slices by the operating system.
   - Like process (CPU) scheduling, threads also have scheduling.
   - Higher priority thread gets more CPU access; others get less.
4. **Threads context switching**
   - OS saves current state of thread & switches to another thread of same process.
     - Saves the state of one thread and retrieves the state of the other, within the same process.
   - Doesn’t includes switching of memory address space. (But Program counter, registers & stack are included.)
     - Memory space does not change because both threads belong to the same process and use the address space allocated to it.
   - Fast switching as compared to process switching
     - Address space is not switched; only a few things (PC, registers) are switched, so the switching overhead is lower.
   - CPU’s cache state is preserved.
     - Same process, same address space, so the cached instructions/address-space info stay valid; no need to reset the cache.
5. **How each thread get access to the CPU?**
   - Each thread has its own program counter.
   - Depending upon the thread scheduling algorithm, OS schedule these threads.
   - OS will fetch instructions corresponding to PC of that thread and execute instruction.
6. **I/O or TQ, based context switching is done here as well**
   - We have TCB (Thread control block) like PCB for state storage management while performing context switching.
     - Every thread has its own TCB, similar to the PCB of a process; the TCB holds the thread's own program counter.
7. **Will single CPU system would gain by multi-threading technique?**
   - Never.
   - As two threads have to context switch for that single CPU.
   - This won’t give any gain.
     - The process is divided into two threads for two independent tasks, but there is still only one CPU. Sometimes T1 gets the CPU, and when it doesn't, T2 is scheduled. The work is effectively sequential; parallelism is not achieved.
     - Best solution: use multi-threading only on multi-core systems (more CPUs). If CPU 1 is free, T1 runs on CPU 1 while T2 runs on CPU 2, independently, and the parallelism benefit is real.
8. **Benefits of Multi-threading.**
   - Responsiveness
     - E.g., an interactive app that needs user input, does I/O, fetches something from the internet, syncs to the cloud, and runs a backup in the background. Each of these is an independent path; divide them into threads.
     - If one thread is blocked on I/O (e.g. waiting for keyboard input), the other threads keep doing formatting or other tasks. The process as a whole is not blocked.
     - Without threads, everything is sequential: either back up, or take user input, or format.
     - So multi-threading makes interactive apps more responsive; one blocked thread does not block other independent tasks.
   - Resource sharing: Efficient resource sharing.
     - Hypothetically, if the independent tasks were made separate processes instead of threads, they would need IPC (inter-process communication, via shared memory or message passing) to communicate. Because of isolation between processes, establishing that communication is itself a big overhead (inefficient).
     - Threads share the address space and the resources of their process (they are threads of the same process), so resource sharing between them is very efficient, with the least overhead and no communication gap.
   - Economy: It is more economical to create and context switch threads.
     1. Also, allocating memory and resources for process creation is costly, so better to divide tasks into threads of same process.
     - Context switching between processes is slower than between threads.
     - Creating a process needs separate resources and space to be allocated; threads come out of the resources already allocated to the process.
   - Threads allow utilization of multiprocessor architectures to a greater scale and efficiency.
     - Scalability: with an 8-core (octa-core) CPU, one process can be divided into 8 independent tasks, each given to one of the 8 CPUs. Much better responsiveness and much faster execution.
     - See the JPG-to-PNG converter example from Lecture 3 for how multiple cores give the benefit of threads.

## Hands-on: multi-threaded C++ program

- A process with two tasks, Task A and Task B, independent of each other (two functions). Each runs a loop that prints something, with `sleep(1)` in the loop.
- To divide the process into threads, include the header `<thread>`.
- `std::thread t1(taskA);` creates thread T1 that runs Task A. If the task had arguments, they would be passed after a comma: `std::thread t1(taskA, arg1, ...);`.
- `std::thread t2(taskB);` creates thread T2 that runs Task B.

```cpp
#include <iostream>
#include <thread>
#include <unistd.h>
using namespace std;

void taskA() {
    for (int i = 0; i < 10; ++i) {
        sleep(1);
        printf("TaskA: %d\n", i);
        fflush(stdout);
    }
}

void taskB() {
    for (int i = 0; i < 10; ++i) {
        sleep(1);
        printf("TaskB: %d\n", i);
        fflush(stdout);
    }
}

int main() {
    thread t1(taskA);
    thread t2(taskB);

    t1.join();
    t2.join();
    return 0;
}
```

- Running the program gives three threads: the main thread (`int main`) plus T1 and T2. Once launched, T1 and T2 work independently.
- Without `join()`: nothing makes main wait, so the main thread reaches the end and exits immediately. The program terminates with an error ("terminate called ..."), because the parent of T1 and T2 (the main thread) has gone.
- `t1.join()`: the main thread waits until T1 completes and does not exit before that. Same for `t2.join()`.
- With `join()`: both tasks run in parallel. On an 8-core machine, T1 probably got CPU 1 and T2 got CPU 2. T1 was launched first, so it was scheduled first; the outputs of both tasks come interleaved.
- This is how one process is divided into threads to get the benefit of concurrency (multi-threading).
